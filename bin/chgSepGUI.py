import wx

from configparser import RawConfigParser
from os import linesep, chdir, walk, path
from logging import getLogger, FileHandler, StreamHandler, Formatter
from common import EditLogConstant, EditLogBase, ComChgSep
from re import sub
from shutil import copytree
from traceback import format_exc

class MainFrame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, wx.ID_ANY, title='セパレータ変換', size=(602, 820))

        # readした時の設定ファイル情報をsave時にも使用する為、クラス変数にしてメソッド間で使いまわす。
        self.load_cfg_path = ''
        self.load_cfg_dir = ''
        self.load_cfg_file = ''

        ID_FILE_OPEN = wx.NewIdRef(count=1)
        ID_FILE_SAVE = wx.NewIdRef(count=1)

        # メニュー
        menu_conf = wx.Menu()
        menu_conf.Append(ID_FILE_OPEN, '開く\tCtrl+o')
        menu_conf.Append(ID_FILE_SAVE, '保存\tCtrl+s')

        menu_bar = wx.MenuBar()
        menu_bar.Append(menu_conf, '設定ファイル')

        self.Bind(wx.EVT_MENU, self.open_file, id=ID_FILE_OPEN)
        self.Bind(wx.EVT_MENU, self.save_file, id=ID_FILE_SAVE)

        self.SetMenuBar(menu_bar)

        # main_panelの上にnotebookとbottom_panelを設置
        main_panel = wx.Panel(self, wx.ID_ANY)

        # bottom_panel 向け要素
        bottom_panel = wx.Panel(main_panel, wx.ID_ANY)
        bottom_panel.SetBackgroundColour('#FFFFFF')
        memo_stext = wx.StaticText(bottom_panel, wx.ID_ANY, 'メモ')
        self.memo_textc = wx.TextCtrl(bottom_panel, wx.ID_ANY, style=wx.TE_MULTILINE, size=(560, 70))
        exechg_button = wx.Button(bottom_panel, wx.ID_ANY, '変換実行')

        exechg_button.Bind(wx.EVT_BUTTON, self.change_sep)

        # bottom_panel 向け Sizer
        bottom_panel_sizer = wx.FlexGridSizer(rows=3, cols=1, gap=(0, 0))
        bottom_panel_sizer.Add(memo_stext, 0, wx.LEFT | wx.TOP, 10)
        bottom_panel_sizer.Add(self.memo_textc, 0, wx.LEFT | wx.BOTTOM, 10)
        bottom_panel_sizer.Add(exechg_button, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, 10)
        bottom_panel.SetSizer(bottom_panel_sizer)

        # Notebook Pages
        notebook = wx.Notebook(main_panel, wx.ID_ANY)
        tab_base = wx.Panel(notebook, wx.ID_ANY)
        tab_quote = wx.Panel(notebook, wx.ID_ANY)
        tab_tgtlimit = wx.Panel(notebook, wx.ID_ANY)
        tab_date = wx.Panel(notebook, wx.ID_ANY)
        tab_extract = wx.Panel(notebook, wx.ID_ANY)
        tab_log = wx.Panel(notebook, wx.ID_ANY)
        notebook.AddPage(tab_base, '基本設定')
        notebook.AddPage(tab_quote, '変換設定')
        notebook.AddPage(tab_tgtlimit, '変換制限機能')
        notebook.AddPage(tab_date, '日時抽出付与機能')
        notebook.AddPage(tab_extract, '行抽出機能')
        notebook.AddPage(tab_log, 'ログ設定')

        # main_panel 向け Sizer
        main_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel_sizer.Add(notebook, 4, wx.EXPAND)
        main_panel_sizer.Add(bottom_panel, 1, wx.EXPAND)
        main_panel.SetSizerAndFit(main_panel_sizer)

        ######
        # tab_base 向け設定
        ######
        # io_path_panel向け要素
        io_path_panel = wx.Panel(tab_base, wx.ID_ANY)
        io_path_panel2 = wx.Panel(io_path_panel, wx.ID_ANY)

        # io_path_panel2向け要素
        workdir_stext = wx.StaticText(io_path_panel2, wx.ID_ANY, 'ワークディレクトリ[WORK_DIR]: \n※絶対パス指定')
        sourcedir_stext = wx.StaticText(io_path_panel2, wx.ID_ANY, '変換前ファイルディレクトリ[SOURCE_DIR]: \n※WORK_DIRからの相対パス指定')
        writedir_stext = wx.StaticText(io_path_panel2, wx.ID_ANY, '変換後ファイルディレクトリ[WRITE_DIR]: \n※WORK_DIRからの相対パス指定')
        self.workdir_textc = wx.TextCtrl(io_path_panel2, wx.ID_ANY, size=(350, -1))
        self.sourcedir_textc = wx.TextCtrl(io_path_panel2, wx.ID_ANY, size=(350, -1))
        self.writedir_textc = wx.TextCtrl(io_path_panel2, wx.ID_ANY, size=(350, -1))

        # io_path_panel2向けSizer
        io_path_panel2_sizer = wx.FlexGridSizer(rows=3, cols=2, gap=(8, 10))
        io_path_panel2_sizer.Add(workdir_stext)
        io_path_panel2_sizer.Add(self.workdir_textc)
        io_path_panel2_sizer.Add(sourcedir_stext)
        io_path_panel2_sizer.Add(self.sourcedir_textc)
        io_path_panel2_sizer.Add(writedir_stext)
        io_path_panel2_sizer.Add(self.writedir_textc)
        io_path_panel2.SetSizer(io_path_panel2_sizer)

        # io_path_panel向けSizer
        io_path_panel_box = wx.StaticBox(io_path_panel, wx.ID_ANY, '入出力パス設定')
        io_path_panel_sizer = wx.StaticBoxSizer(io_path_panel_box, wx.VERTICAL)
        io_path_panel_sizer.Add(io_path_panel2)
        io_path_panel.SetSizer(io_path_panel_sizer)

        # sep_panel向け要素
        sep_panel = wx.Panel(tab_base, wx.ID_ANY)
        sep_panel2 = wx.Panel(sep_panel, wx.ID_ANY)

        # sep_panel2向け要素
        inputsep_stext = wx.StaticText(sep_panel2, wx.ID_ANY, '入力ファイル区切り文字[INPUT_SEP]')
        outputsep_stext = wx.StaticText(sep_panel2, wx.ID_ANY, '出力ファイル区切り文字[OUTPUT_SEP]')
        self.inputsep_cbox = wx.ComboBox(sep_panel2, wx.ID_ANY, 'COMMA', choices=('COMMA', 'TAB', 'SPACE'), style=wx.CB_READONLY)
        self.outputsep_cbox = wx.ComboBox(sep_panel2, wx.ID_ANY, 'COMMA', choices=('COMMA', 'TAB', 'SPACE'), style=wx.CB_READONLY)
        sep_stext = wx.StaticText(sep_panel2, wx.ID_ANY, '\
    COMMA, TAB, SPACE のどれかを選択。\n\
    INPUT_SEPにSPACEを選択した場合のみ、連続するセパレータは1つと解釈されます。\n\n\
    <例>\n\
    （変換前）行：　"foo"␣␣␣"var"␣␣␣␣␣"hoge"　（<--半角スペースを␣で表示）\n\
    （変換後）行：　"foo" ,"var","hoge"\n\
    ※連続するスペースは一つのスペースセパレータと解釈されます。\n\
    　【行：　"foo",,,"var",,,,,"hoge"】とはなりません。')

        # sep_panel2向けSizer
        sep_panel2_sizer = wx.GridBagSizer(8, 10)
        sep_panel2_sizer.Add(inputsep_stext, (0, 0), (1, 1))
        sep_panel2_sizer.Add(self.inputsep_cbox, (0, 1), (1, 1))
        sep_panel2_sizer.Add(outputsep_stext, (1, 0), (1, 1))
        sep_panel2_sizer.Add(self.outputsep_cbox, (1, 1), (1, 1))
        sep_panel2_sizer.Add(sep_stext, (2, 0), (1, 3))
        sep_panel2.SetSizer(sep_panel2_sizer)

        # sep_panel向けSizer
        sep_panel_box = wx.StaticBox(sep_panel, wx.ID_ANY, '区切り文字指定')
        sep_panel_sizer = wx.StaticBoxSizer(sep_panel_box, wx.VERTICAL)
        sep_panel_sizer.Add(sep_panel2, 1, wx.EXPAND)
        sep_panel.SetSizer(sep_panel_sizer)

        # enc_panel向け要素
        enc_panel = wx.Panel(tab_base, wx.ID_ANY)
        enc_panel2 = wx.Panel(enc_panel, wx.ID_ANY)

        # enc_panel2向け要素
        inputenc_stext = wx.StaticText(enc_panel2, wx.ID_ANY, '入力ファイル文字コード[INPUT_ENCODE]')
        outputenc_stext = wx.StaticText(enc_panel2, wx.ID_ANY, '出力ファイル文字コード[OUTPUT_ENCODE]')
        self.inputenc_cbox = wx.ComboBox(enc_panel2, wx.ID_ANY, '', choices=('utf_8', 'cp932', 'shift_jis', 'euc_jp'), style=wx.CB_DROPDOWN)
        self.outputenc_cbox = wx.ComboBox(enc_panel2, wx.ID_ANY, '', choices=('utf_8', 'cp932', 'shift_jis', 'euc_jp'), style=wx.CB_DROPDOWN)
        enc_stext = wx.StaticText(enc_panel2, wx.ID_ANY, '\
    エンコードはpythonのcodecsに準拠します。<https://docs.python.jp/3/library/codecs.html>\n\n\
    ※変換不可能な文字が含まれている場合は「●」に置き換えます。\n\
    ※出力ファイルの文字コードをcp932にした場合、「IBM拡張文字」は「NEC選定IBM拡張文字」となります。\n\
    　入力ファイルの文字コードがcp932で「IBM選定IBM拡張文字」が含まれている場合は\n\
    　「NEC選定IBM拡張文字」に変換されます（Pythonの仕様）。')

        # enc_panel2向けSizer
        enc_panel2_sizer = wx.GridBagSizer(8, 10)
        enc_panel2_sizer.Add(inputenc_stext, (0, 0), (1, 1))
        enc_panel2_sizer.Add(self.inputenc_cbox, (0, 1), (1, 1))
        enc_panel2_sizer.Add(outputenc_stext, (1, 0), (1, 1))
        enc_panel2_sizer.Add(self.outputenc_cbox, (1, 1), (1, 1))
        enc_panel2_sizer.Add(enc_stext, (2, 0), (1, 3))
        enc_panel2.SetSizer(enc_panel2_sizer)

        # enc_panel向けSizer
        enc_panel_box = wx.StaticBox(enc_panel, wx.ID_ANY, 'エンコード指定')
        enc_panel_sizer = wx.StaticBoxSizer(enc_panel_box, wx.VERTICAL)
        enc_panel_sizer.Add(enc_panel2, 1, wx.EXPAND)
        enc_panel.SetSizer(enc_panel_sizer)

        # tab_base向けSizer
        tab_base_sizer = wx.BoxSizer(wx.VERTICAL)
        tab_base_sizer.Add(io_path_panel, 2, wx.EXPAND | wx.ALL, 5)
        tab_base_sizer.Add(sep_panel, 3, wx.EXPAND | wx.ALL, 5)
        tab_base_sizer.Add(enc_panel, 3, wx.EXPAND | wx.ALL, 5)
        tab_base.SetSizer(tab_base_sizer)

        ######
        # tab_quote 向け設定
        ######
        # quote_panel
        quote_panel = wx.Panel(tab_quote, wx.ID_ANY)

        # quote_panel 向け要素
        self.quote_cbox = wx.ComboBox(quote_panel, wx.ID_ANY, 'FALSE', choices=('FALSE', 'SINGLE', 'DOUBLE', 'QUOTES', 'SQUARE_BRACKETS', 'ALL'), style=wx.CB_READONLY)
        quote_stext = wx.StaticText(quote_panel, wx.ID_ANY, '\
    囲み文字内に区切り文字が存在しても区切り文字として認識されません。\n\
        （例）\'fo,o\' "va,r" [h,oge]\n\n\
    設定可能なパラメータは以下の通り。\n\
        ・FALSE : 囲み文字処理無し\n\
        ・SINGLE : <\'\'>\n\
        ・DOUBLE : <"">\n\
        ・QUOTES : <\'\'> + <"">\n\
        ・SQUARE_BRACKETS : <[]>\n\
        ・ALL : <\'\'> + <""> + <[]>\n\n\
    <QUOTES, ALLを選択した場合の注意点>\n\
    １．囲み文字内に区切り文字が含まれていて、囲み文字の始まりと終わりが異なる場合はエラーとなります。\n\
        （例）\'fo,o" "va,r\' [h,oge" \n\n\
    ２．囲み文字内に区切り文字が無い場合は囲み文字の不整合はエラーにならず、そのまま出力します。\n\
        （例）\'foo" "var\' [hoge"')

        # quote_panel 向けSizer
        quote_panel_box = wx.StaticBox(quote_panel, wx.ID_ANY, '1カラムであることを示す囲み文字[QUOTE]')
        quote_panel_sizer = wx.StaticBoxSizer(quote_panel_box, wx.VERTICAL)
        quote_panel_sizer.Add(self.quote_cbox, 0, wx.BOTTOM, 5)
        quote_panel_sizer.Add(quote_stext, 0, wx.BOTTOM, 5)
        quote_panel.SetSizer(quote_panel_sizer)

        # newline_panel
        newline_panel = wx.Panel(tab_quote, wx.ID_ANY)

        # newline_panel 向け要素
        self.newline_cbox = wx.ComboBox(newline_panel, wx.ID_ANY, 'CRLF', choices=('CRLF', 'LF', 'CR', 'FALSE'), style=wx.CB_READONLY)
        newline_stext = wx.StaticText(newline_panel, wx.ID_ANY, '\
    CRLF, LF, CR, FALSE のどれかを選択。\n\
    FALSEの場合は元ファイルの改行コードに従う。')

        # newline_panel 向けSizer
        newline_panel_box = wx.StaticBox(newline_panel, wx.ID_ANY, '出力改行コード[NEW_LINE]')
        newline_panel_sizer = wx.StaticBoxSizer(newline_panel_box, wx.VERTICAL)
        newline_panel_sizer.Add(self.newline_cbox, 0, wx.BOTTOM, 5)
        newline_panel_sizer.Add(newline_stext, 0, wx.BOTTOM, 5)
        newline_panel.SetSizer(newline_panel_sizer)

        # tab_quote 向けSizer
        tab_quote_sizer = wx.BoxSizer(wx.VERTICAL)
        tab_quote_sizer.Add(quote_panel, 0, wx.EXPAND | wx.ALL, 5)
        tab_quote_sizer.Add(newline_panel, 0, wx.EXPAND | wx.ALL, 5)
        tab_quote.SetSizer(tab_quote_sizer)

        ######
        # tab_tgtlimit 向け設定
        ######
        # tgtlimit_panel
        tgtlimit_panel = wx.Panel(tab_tgtlimit, wx.ID_ANY)

        # tgtlimit_panel 向け要素
        self.tgtlimit_textc = wx.TextCtrl(tgtlimit_panel, wx.ID_ANY, 'FALSE', size=(50, -1))
        self.tgtlimit_stext = wx.StaticText(tgtlimit_panel, wx.ID_ANY, '\
    INPUT_SEPにSPACEを選択した場合の変換対象のカラム数を数値で指定（左から数える）。\n\
    全カラムを変換対象とする場合及び、INPUT_SEPにSPACEを選択しない場合は\n\
    「FALSE」を入力しておく。\n\n\
    <例:6カラムのデータを3カラム分だけ変換する。（スペース区切りをカンマ区切りに変換）>\n\
    （設定値）INPUT_SEP_SPACE_COL_CHG_LIMIT = 3\n\
    （変換前）行：　foo var hoge foo1 var1 hoge1\n\
    （変換後）行：　foo,var,hoge')
        self.tgtlimit_chkbox = wx.CheckBox(tgtlimit_panel, wx.ID_ANY, '変換対象外カラムを結果ファイルに残す。')
        self.tgtlimit_stext2 = wx.StaticText(tgtlimit_panel, wx.ID_ANY, '\
    <例:6カラムのデータを3カラム分だけ変換する。残カラムは末尾付与。（スペース区切りをカンマ区切りに変換）>\n\
    （設定値）INPUT_SEP_SPACE_COL_CHG_LIMIT = 3\n\
    （変換前）行：　foo var hoge foo1 var1 hoge1\n\
    （変換後）行：　foo,var,hoge,foo1 var1 hoge1')

        # tgtlimit_panel 向けSizer
        tgtlimit_panel_box = wx.StaticBox(tgtlimit_panel, wx.ID_ANY, '変換対象カラム数制限[INPUT_SEP_SPACE_COL_CHG_LIMIT]')
        tgtlimit_panel_sizer = wx.StaticBoxSizer(tgtlimit_panel_box, wx.VERTICAL)
        tgtlimit_panel_sizer.Add(self.tgtlimit_textc, 0, wx.BOTTOM, 5)
        tgtlimit_panel_sizer.Add(self.tgtlimit_stext, 0, wx.BOTTOM, 30)
        tgtlimit_panel_sizer.Add(self.tgtlimit_chkbox, 0, wx.BOTTOM, 5)
        tgtlimit_panel_sizer.Add(self.tgtlimit_stext2, 0, wx.BOTTOM, 5)
        tgtlimit_panel.SetSizer(tgtlimit_panel_sizer)

        # tab_tgtlimit 向けSizer
        tab_tgtlimit_sizer = wx.BoxSizer(wx.VERTICAL)
        tab_tgtlimit_sizer.Add(tgtlimit_panel, 0, wx.EXPAND | wx.ALL, 5)
        tab_tgtlimit.SetSizer(tab_tgtlimit_sizer)

        ######
        # tab_date 向け設定
        ######
        # date_panel
        date_panel = wx.Panel(tab_date, wx.ID_ANY)

        # date_panel 向け要素
        date_line_regex_stext = wx.StaticText(date_panel, wx.ID_ANY, '日時文字列取得用正規表現[DATE_LINE_REGEX]')
        self.date_line_regex_textc = wx.TextCtrl(date_panel, wx.ID_ANY, size=(560, -1))
        input_date_format_stext = wx.StaticText(date_panel, wx.ID_ANY, '入力日時フォーマット[INPUT_DATE_FORMAT]')
        self.input_date_format_textc = wx.TextCtrl(date_panel, wx.ID_ANY, size=(560, -1))
        output_date_format_stext = wx.StaticText(date_panel, wx.ID_ANY, '出力日時フォーマット[OUTPUT_DATE_FORMAT]')
        self.output_date_format_textc = wx.TextCtrl(date_panel, wx.ID_ANY, size=(560, -1))
        date_ext_stext = wx.StaticText(date_panel, wx.ID_ANY, '\
    正規表現DATE_LINE_REGEXに従って行内に存在する日時に関わる\n\
    文字列を取得してINPUT_DATE_FORMATで日付型に変換し、該当行及び\n\
    以降の行の行頭にOUTPUT_DATE_FORMATの形式で日時を付与する。\n\
    ※行頭付与される日時は「変換制限」の制限カラム数に含まれません。\n\n\
    使用しない場合は空白とする。\n\
    DATE_FORMATの形式はpythonのdatetimeに準拠\n\
    <https://docs.python.jp/3/library/datetime.html>\n\n\
    <例:行頭に日時を付与する。（スペース区切りをカンマ区切りに変換）>\n\
    （設定値）\n\
    ・DATE_LINE_REGEX = [0-9]{2,2}/[a-zA-Z]{3,3}/[0-9]{4,4}:[0-9]{2,2}:[0-9]{2,2}:[0-9]{2,2}\n\
    ・INPUT_DATE_FORMAT = %d/%b/%Y:%H:%M:%S\n\
    ・OUTPUT_DATE_FORMAT = %Y/%m/%d %H:%M:%S\n\
    （変換前）\n\
    1行目：　foo var 21/Aug/2017:10:10:10 hoge\n\
    2行目：　foo1 var1 hoge1 hoge11\n\
    3行目：　foo2 var2 hoge2 hoge22\n\
    （変換後）\n\
    1行目：　2017/08/21 10:10:10,foo,var,21/Aug/2017:10:10:10,hoge\n\
    2行目：　2017/08/21 10:10:10,foo1,var1,hoge1,hoge11\n\
    3行目：　2017/08/21 10:10:10,foo2,var2,hoge2,hoge22')

        # date_panel 向けSizer
        date_panel_box = wx.StaticBox(date_panel, wx.ID_ANY, '日時文字列取得用パラメータ')
        date_panel_sizer = wx.StaticBoxSizer(date_panel_box, wx.VERTICAL)
        date_panel_sizer.Add(date_line_regex_stext, 0, wx.BOTTOM, 5)
        date_panel_sizer.Add(self.date_line_regex_textc, 0, wx.BOTTOM, 5)
        date_panel_sizer.Add(input_date_format_stext, 0, wx.BOTTOM, 5)
        date_panel_sizer.Add(self.input_date_format_textc, 0, wx.BOTTOM, 5)
        date_panel_sizer.Add(output_date_format_stext, 0, wx.BOTTOM, 5)
        date_panel_sizer.Add(self.output_date_format_textc, 0, wx.BOTTOM, 5)
        date_panel_sizer.Add(date_ext_stext, 0, wx.BOTTOM, 5)
        date_panel.SetSizer(date_panel_sizer)

        # tab_date 向けSizer
        tab_date_sizer = wx.BoxSizer(wx.VERTICAL)
        tab_date_sizer.Add(date_panel, 0, wx.EXPAND | wx.ALL, 5)
        tab_date.SetSizer(tab_date_sizer)

        ######
        # tab_extract 向け設定
        ######
        # extract_panel
        extract_panel = wx.Panel(tab_extract, wx.ID_ANY)

        # extract_panel 向け要素
        self.extract_textc = wx.TextCtrl(extract_panel, wx.ID_ANY, size=(560, -1))
        self.extract_stext = wx.StaticText(extract_panel, wx.ID_ANY, '\
    正規表現に一致する文字列を含む行のみ出力する。\n使用しない場合は空白とする。')

        # extract_panel 向けSizer
        extract_panel_box = wx.StaticBox(extract_panel, wx.ID_ANY, '\
    抽出用正規表現[EXTRACT_ON_REGEX]')
        extract_panel_sizer = wx.StaticBoxSizer(extract_panel_box, wx.VERTICAL)
        extract_panel_sizer.Add(self.extract_textc, 0, wx.BOTTOM, 5)
        extract_panel_sizer.Add(self.extract_stext, 0, wx.BOTTOM, 5)
        extract_panel.SetSizer(extract_panel_sizer)

        # tab_extract
        tab_extract_sizer = wx.BoxSizer(wx.VERTICAL)
        tab_extract_sizer.Add(extract_panel, 0, wx.EXPAND | wx.ALL, 5)
        tab_extract.SetSizer(tab_extract_sizer)

        ######
        # tab_log 向け設定
        ######
        # log_panel
        log_panel = wx.Panel(tab_log, wx.ID_ANY)

        # log_panel 向け要素
        log_path_stext = wx.StaticText(log_panel, wx.ID_ANY, 'ログ出力パス[PATH]')
        self.log_path_textc = wx.TextCtrl(log_panel, wx.ID_ANY, './editLogs.log', size=(560, -1))
        log_enc_stext = wx.StaticText(log_panel, wx.ID_ANY, 'ログ文字コード[ENCODING]')
        self.log_enc_textc = wx.TextCtrl(log_panel, wx.ID_ANY, EditLogConstant.CONF_ENC, size=(560, -1))
        log_date_stext = wx.StaticText(log_panel, wx.ID_ANY, 'ログ日時フォーマット[DATE_FMT]')
        self.log_date_textc = wx.TextCtrl(log_panel, wx.ID_ANY, '%Y/%m/%d %H:%M:%S', size=(560, -1))
        log_fmtconsole_stext = wx.StaticText(log_panel, wx.ID_ANY, 'コンソール向けログフォーマット[FORMAT_CONSOLE]')
        self.log_fmtconsole_textc = wx.TextCtrl(log_panel, wx.ID_ANY, '%(asctime)s.%(msecs)d : %(name)s : %(levelname)s : %(lineno)d : "%(message)s"', size=(560, -1))
        log_fmtfile_stext = wx.StaticText(log_panel, wx.ID_ANY, 'ファイル向けログフォーマット[FORMAT_FILE]')
        self.log_fmtfile_textc = wx.TextCtrl(log_panel, wx.ID_ANY, '"%(asctime)s"	"%(msecs)d"	"%(name)s"	"%(levelname)s"	"%(lineno)d"	"%(message)s"', size=(560, -1))

        # log_panel 向けSizer
        log_panel_box = wx.StaticBox(log_panel, wx.ID_ANY, 'ログ設定')
        log_panel_sizer = wx.StaticBoxSizer(log_panel_box, wx.VERTICAL)
        log_panel_sizer.Add(log_path_stext, 0, wx.BOTTOM, 5)
        log_panel_sizer.Add(self.log_path_textc, 0, wx.BOTTOM, 5)
        log_panel_sizer.Add(log_enc_stext, 0, wx.BOTTOM, 5)
        log_panel_sizer.Add(self.log_enc_textc, 0, wx.BOTTOM, 5)
        log_panel_sizer.Add(log_date_stext, 0, wx.BOTTOM, 5)
        log_panel_sizer.Add(self.log_date_textc, 0, wx.BOTTOM, 5)
        log_panel_sizer.Add(log_fmtconsole_stext, 0, wx.BOTTOM, 5)
        log_panel_sizer.Add(self.log_fmtconsole_textc, 0, wx.BOTTOM, 5)
        log_panel_sizer.Add(log_fmtfile_stext, 0, wx.BOTTOM, 5)
        log_panel_sizer.Add(self.log_fmtfile_textc, 0, wx.BOTTOM, 5)
        log_panel.SetSizer(log_panel_sizer)

        # tab_log
        tab_log_sizer = wx.BoxSizer(wx.VERTICAL)
        tab_log_sizer.Add(log_panel, 0, wx.EXPAND | wx.ALL, 5)
        tab_log.SetSizer(tab_log_sizer)

        self.Show()


    def open_file(self, evt):

        open_dialog = wx.FileDialog(None, '設定ファイル読込', self.load_cfg_dir, '', '設定ファイル(*.conf)|*.conf|全てのファイル(*.*)|*.*', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if open_dialog.ShowModal() == wx.ID_CANCEL:
            return

        self.load_cfg_path = open_dialog.GetPath()
        self.load_cfg_dir = open_dialog.GetDirectory()
        self.load_cfg_file = open_dialog.GetFilename()

        if len(self.load_cfg_path) != 0 :
            cfg_parser_read = RawConfigParser()
            cfg_parser_read.read(self.load_cfg_path , encoding=EditLogConstant.CONF_ENC)

            # ==========
            # baseset
            # ==========
            self.workdir_textc.SetValue(cfg_parser_read.get('baseset', 'WORK_DIR'))
            self.sourcedir_textc.SetValue(cfg_parser_read.get('baseset', 'SOURCE_DIR'))
            self.writedir_textc.SetValue(cfg_parser_read.get('baseset', 'WRITE_DIR'))
            self.memo_textc.SetValue(cfg_parser_read.get('baseset', 'MEMO'))

            # ==========
            # formatparams
            # ==========
            self.inputenc_cbox.SetValue(cfg_parser_read.get('formatparams', 'INPUT_ENCODE'))
            self.outputenc_cbox.SetValue(cfg_parser_read.get('formatparams', 'OUTPUT_ENCODE'))
            self.inputsep_cbox.SetStringSelection(cfg_parser_read.get('formatparams', 'INPUT_SEP'))
            self.outputsep_cbox.SetStringSelection(cfg_parser_read.get('formatparams', 'OUTPUT_SEP'))
            self.newline_cbox.SetStringSelection(cfg_parser_read.get('formatparams', 'NEW_LINE'))
            self.quote_cbox.SetStringSelection(cfg_parser_read.get('formatparams', 'QUOTE'))
            self.tgtlimit_textc.SetValue(cfg_parser_read.get('formatparams', 'INPUT_SEP_SPACE_COL_CHG_LIMIT'))
            self.tgtlimit_chkbox.SetValue(int(cfg_parser_read.get('formatparams', 'INPUT_SEP_SPACE_COL_CHG_LIMIT_OPTION1')))
            self.date_line_regex_textc.SetValue(cfg_parser_read.get('formatparams', 'DATE_LINE_REGEX'))
            self.input_date_format_textc.SetValue(cfg_parser_read.get('formatparams', 'INPUT_DATE_FORMAT'))
            self.output_date_format_textc.SetValue(cfg_parser_read.get('formatparams', 'OUTPUT_DATE_FORMAT'))
            self.extract_textc.SetValue(cfg_parser_read.get('formatparams', 'EXTRACT_ON_REGEX'))

            # ==========
            # logging
            # ==========
            self.log_path_textc.SetValue(cfg_parser_read.get('logging', 'PATH'))
            self.log_enc_textc.SetValue(cfg_parser_read.get('logging', 'ENCODING'))
            self.log_date_textc.SetValue(cfg_parser_read.get('logging', 'DATE_FMT'))
            self.log_fmtconsole_textc.SetValue(cfg_parser_read.get('logging', 'FORMAT_CONSOLE'))
            self.log_fmtfile_textc.SetValue(cfg_parser_read.get('logging', 'FORMAT_FILE'))


    def save_file(self, evt):

        cfg_parser_write = RawConfigParser()

        cfg_parser_write.add_section('baseset')
        cfg_parser_write.set('baseset', 'WORK_DIR', self.workdir_textc.GetValue())
        cfg_parser_write.set('baseset', 'SOURCE_DIR', self.sourcedir_textc.GetValue())
        cfg_parser_write.set('baseset', 'WRITE_DIR', self.writedir_textc.GetValue())
        cfg_parser_write.set('baseset', 'MEMO', self.memo_textc.GetValue())

        cfg_parser_write.add_section('formatparams')
        cfg_parser_write.set('formatparams', 'INPUT_ENCODE', self.inputenc_cbox.GetValue())
        cfg_parser_write.set('formatparams', 'OUTPUT_ENCODE', self.outputenc_cbox.GetValue())
        cfg_parser_write.set('formatparams', 'INPUT_SEP', self.inputsep_cbox.GetValue())
        cfg_parser_write.set('formatparams', 'OUTPUT_SEP', self.outputsep_cbox.GetValue())
        cfg_parser_write.set('formatparams', 'NEW_LINE', self.newline_cbox.GetValue())
        cfg_parser_write.set('formatparams', 'QUOTE', self.quote_cbox.GetValue())
        cfg_parser_write.set('formatparams', 'INPUT_SEP_SPACE_COL_CHG_LIMIT', self.tgtlimit_textc.GetValue())
        cfg_parser_write.set('formatparams', 'INPUT_SEP_SPACE_COL_CHG_LIMIT_OPTION1', int(self.tgtlimit_chkbox.GetValue()))
        cfg_parser_write.set('formatparams', 'DATE_LINE_REGEX', self.date_line_regex_textc.GetValue())
        cfg_parser_write.set('formatparams', 'INPUT_DATE_FORMAT', self.input_date_format_textc.GetValue())
        cfg_parser_write.set('formatparams', 'OUTPUT_DATE_FORMAT', self.output_date_format_textc.GetValue())
        cfg_parser_write.set('formatparams', 'EXTRACT_ON_REGEX', self.extract_textc.GetValue())

        cfg_parser_write.add_section('logging')
        cfg_parser_write.set('logging', 'PATH', self.log_path_textc.GetValue())
        cfg_parser_write.set('logging', 'ENCODING', self.log_enc_textc.GetValue())
        cfg_parser_write.set('logging', 'DATE_FMT', self.log_date_textc.GetValue())
        cfg_parser_write.set('logging', 'FORMAT_CONSOLE', self.log_fmtconsole_textc.GetValue())
        cfg_parser_write.set('logging', 'FORMAT_FILE', self.log_fmtfile_textc.GetValue())

        save_dialog = wx.FileDialog(None, '設定をファイルに保存', self.load_cfg_dir, self.load_cfg_file, '設定ファイル(*.conf)|*.conf|全てのファイル(*.*)|*.*', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save_dialog.ShowModal() == wx.ID_CANCEL:
            return

        self.load_cfg_path = save_dialog.GetPath()
        self.load_cfg_dir = save_dialog.GetDirectory()
        self.load_cfg_file = save_dialog.GetFilename()

        if len(self.load_cfg_path) != 0:
            try:
                with open(self.load_cfg_path, 'w', encoding=EditLogConstant.CONF_ENC, newline=linesep) as f:
                    cfg_parser_write.write(f)
            except:
                wx.MessageBox('ファイル保存に失敗しました。', 'ファイル出力エラー', wx.ICON_ERROR)
                return


    def change_sep(self, evt):

        application.ResetLocale()

        wx.MessageBox('変換処理を開始します。', '処理の開始', wx.ICON_INFORMATION)

        # loggerのHandler格納用。終了共通処理の引数向け
        logger_nl = []
        logger = ''

        # 当処理で共通的に使用するLogger名
        LOGGER_NAME = 'chg_sep_log'

        # 共通クラスインスタンス取得
        com_elb = EditLogBase.EditLogBase()
        com_cs = ComChgSep.ComChgSep()

        try:
            # ワークディレクトリ移動
            chdir(com_elb.delQuoteStartEnd(self.workdir_textc.GetValue()))
        except:
            print(format_exc())
            com_elb.end_gui_func(logger, logger_nl, application)
            wx.MessageBox('パス > ワークディレクトリ[WORK_DIR] ' + com_elb.delQuoteStartEnd(self.workdir_textc.GetValue()) + 'への移動に失敗しました。', 'エラー終了', wx.ICON_ERROR)
            return

        logger = getLogger(LOGGER_NAME)
        # ログレベル設定
        logger.setLevel(11)
        try:
            # ファイル出力設定
            log_fh = FileHandler(self.log_path_textc.GetValue(), encoding=self.log_enc_textc.GetValue())
        except LookupError:
            print(format_exc())
            com_elb.end_gui_func(logger, logger_nl, application)
            wx.MessageBox('ログ > ログ文字コード[ENCODING] ' + self.log_enc_textc.GetValue() + 'は不正です。', 'エラー終了', wx.ICON_ERROR)
            return
        except:
            print(format_exc())
            com_elb.end_gui_func(logger, logger_nl, application)
            wx.MessageBox('ログ > ログ出力パス[PATH] ' + self.log_path_textc.GetValue() + 'には出力できません。', 'エラー終了', wx.ICON_ERROR)
            return

        logger.addHandler(log_fh)
        logger_nl.append(log_fh)
        # コンソール出力設定
        log_sh = StreamHandler()
        logger.addHandler(log_sh)
        logger_nl.append(log_sh)
        # 出力形式設定
        log_format_for_stream = Formatter(fmt=self.log_fmtconsole_textc.GetValue(), datefmt=self.log_date_textc.GetValue())
        log_format_for_file = Formatter(fmt=self.log_fmtfile_textc.GetValue(), datefmt=self.log_date_textc.GetValue())
        log_sh.setFormatter(log_format_for_stream)
        log_fh.setFormatter(log_format_for_file)

        # 起動共通
        com_elb.start(logger)

        try:
            # 出力先ディレクトリ作成
            com_elb.makeDir(com_elb.delQuoteStartEnd(self.writedir_textc.GetValue()))

            # ソースディレクトリのファイルを出力ディレクトリにコピー
            # 出力先ディレクトリに指定ディレクトリからのディレクトリ構成を再現する
            copytree(com_elb.delQuoteStartEnd(self.sourcedir_textc.GetValue()).replace(path.sep, '/'),
                      path.join(com_elb.delQuoteStartEnd(self.writedir_textc.GetValue()),
                                   sub('[:*\?"<>\|]', '', com_elb.delQuoteStartEnd(self.sourcedir_textc.GetValue()).strip('./\\'))).replace(path.sep, '/'))
        except:
            logger.exception(format_exc())
            com_elb.end_gui_func(logger, logger_nl, application)
            wx.MessageBox('[WRITE_DIR] ' + com_elb.delQuoteStartEnd(self.writedir_textc.GetValue()) + 'の作成に失敗しました。', 'エラー終了', wx.ICON_ERROR)
            return

        try:
            for walk_root, dirs, files in walk(com_elb.delQuoteStartEnd(self.writedir_textc.GetValue())):
                logger.log(20, '処理中ディレクトリ: ')
                logger.log(20, walk_root.replace('\\', '/'))
                for file in files:
                        # 区切り文字変更
                        com_cs.chg_sep(LOGGER_NAME,
                                   path.join(walk_root, file).replace(path.sep, '/'),
                                   com_elb.delQuoteStartEnd(self.inputenc_cbox.GetValue()),
                                   com_elb.delQuoteStartEnd(self.outputenc_cbox.GetValue()),
                                   com_elb.delQuoteStartEnd(self.inputsep_cbox.GetValue()),
                                   com_elb.delQuoteStartEnd(self.outputsep_cbox.GetValue()),
                                   com_elb.delQuoteStartEnd(self.newline_cbox.GetValue()),
                                   com_elb.delQuoteStartEnd(self.quote_cbox.GetValue()),
                                   com_elb.delQuoteStartEnd(self.tgtlimit_textc.GetValue()),
                                   int(self.tgtlimit_chkbox.GetValue()),
                                   com_elb.delQuoteStartEnd(self.date_line_regex_textc.GetValue()),
                                   com_elb.delQuoteStartEnd(self.input_date_format_textc.GetValue()),
                                   com_elb.delQuoteStartEnd(self.output_date_format_textc.GetValue()),
                                   com_elb.delQuoteStartEnd(self.extract_textc.GetValue()))
        except:
            logger.exception(format_exc())
            com_elb.end_gui_func(logger, logger_nl, application)
            wx.MessageBox('変換中にエラーが発生しました。', 'エラー終了', wx.ICON_ERROR)
            return

        # 終了共通
        com_elb.end_gui_func(logger, logger_nl, application)
        wx.MessageBox('変換処理が正常に完了しました。', '処理の終了', wx.ICON_INFORMATION)
        return


if __name__ == '__main__':

    application = wx.App()
    MainFrame()
    application.MainLoop()

