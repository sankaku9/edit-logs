import wx
from configparser import RawConfigParser
from common import EditLogConstant, EditLogBase, ComChgSep

load_cfg_file = ''


'''
def select_submenu(event):
    event_id = event.GetId()
    if event_id == 1:
        open_file
    elif event_id == 2:
        pass
'''


def open_file(self):
    global load_cfg_file
    dialog = wx.FileDialog(None, '設定ファイル読込', '', '', '設定ファイル(*.conf)|*.conf|全てのファイル(*.*)|*.*', style=wx.FD_OPEN)
#    load_cfg_file = filedialog.askopenfilename(title='設定ファイル読込', filetypes=[('設定ファイル', '*.conf'), ('全てのファイル', '*.*')])
    if dialog.ShowModal() == wx.ID_CANCEL:
        return

    load_cfg_file = dialog.GetPath()

    if len(load_cfg_file) != 0 :
        cfg_parser_read = RawConfigParser()
        cfg_parser_read.read(load_cfg_file , encoding=EditLogConstant.CONF_ENC)

        # ==========
        # baseset
        # ==========
        workdir_textc.SetValue(cfg_parser_read.get('baseset', 'WORK_DIR'))

        sourcedir_textc.SetValue(cfg_parser_read.get('baseset', 'SOURCE_DIR'))

        writedir_textc.SetValue(cfg_parser_read.get('baseset', 'WRITE_DIR'))

        if len(cfg_parser_read.get('baseset', 'MEMO')) != 0 :
            memo_textc.SetValue(cfg_parser_read.get('baseset', 'MEMO'))

        # ==========
        # formatparams
        # ==========
        inputenc_textc.SetValue(cfg_parser_read.get('formatparams', 'INPUT_ENCODE'))

        outputenc_textc.SetValue(cfg_parser_read.get('formatparams', 'OUTPUT_ENCODE'))

        try:
            inputsep_cbox.SetStringSelection(cfg_parser_read.get('formatparams', 'INPUT_SEP'))
        except:
            wx.MessageBox('パラメータエラー', 'INPUT_SEPの値が不正です。', wx.ICON_ERROR)

        try:
            outputsep_cbox.SetStringSelection(cfg_parser_read.get('formatparams', 'OUTPUT_SEP'))
        except:
            wx.MessageBox('パラメータエラー', 'OUTPUT_SEPの値が不正です。', wx.ICON_ERROR)

        try:
            newline_cbox.SetStringSelection(cfg_parser_read.get('formatparams', 'NEW_LINE'))
        except:
            wx.MessageBox('パラメータエラー', 'NEW_LINEの値が不正です。', wx.ICON_ERROR)

        try:
            quote_cbox.SetStringSelection(cfg_parser_read.get('formatparams', 'QUOTE'))
        except:
            wx.MessageBox('パラメータエラー', 'QUOTEの値が不正です。', wx.ICON_ERROR)

        tgtlimit_textc.SetValue(cfg_parser_read.get('formatparams', 'INPUT_SEP_SPACE_COL_CHG_LIMIT'))

        date_line_regex_textc.SetValue(cfg_parser_read.get('formatparams', 'DATE_LINE_REGEX'))

        input_date_format_textc.SetValue(cfg_parser_read.get('formatparams', 'INPUT_DATE_FORMAT'))

        output_date_format_textc.SetValue(cfg_parser_read.get('formatparams', 'OUTPUT_DATE_FORMAT'))

        extract_textc.SetValue(cfg_parser_read.get('formatparams', 'EXTRACT_ON_REGEX'))

        # ==========
        # logging
        # ==========
        log_path_textc.SetValue(cfg_parser_read.get('logging', 'PATH'))

        log_enc_textc.SetValue(cfg_parser_read.get('logging', 'ENCODING'))

        log_date_textc.SetValue(cfg_parser_read.get('logging', 'DATE_FMT'))

        log_fmtconsole_textc.SetValue(cfg_parser_read.get('logging', 'FORMAT_CONSOLE'))

        log_fmtfile_textc.SetValue(cfg_parser_read.get('logging', 'FORMAT_FILE'))


if __name__ == '__main__':

    ID_FILE_OPEN = wx.NewIdRef(count=1)
    ID_FILE_SAVE = wx.NewIdRef(count=1)

    # Window設定
    application = wx.App()
    frame = wx.Frame(None, wx.ID_ANY, title='セパレータ変換', size=(602, 820))
    #frame = wx.Frame(None, wx.ID_ANY, title='セパレータ変換', size=(602, 820), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
    #frame = wx.Frame(None, wx.ID_ANY, title='セパレータ変換')

    # メニュー
    menu_conf = wx.Menu()
    menu_conf.Append(ID_FILE_OPEN, '開く')
    menu_conf.Append(ID_FILE_SAVE, '保存')

    menu_bar = wx.MenuBar()
    menu_bar.Append(menu_conf, '設定ファイル')

    #frame.bind(wx.EVT_MENU, select_submenu)
    frame.Bind(wx.EVT_MENU, open_file, id=ID_FILE_OPEN)

    frame.SetMenuBar(menu_bar)

    # main_panelの上にnotebookとbottom_panelを設置
    #main_panel = wx.Panel(frame,wx.ID_ANY, pos=(0, 0), size=(600, 810))
    #bottom_panel = wx.Panel(frame,wx.ID_ANY, pos=(0, 601), size=(600, 160))
    main_panel = wx.Panel(frame,wx.ID_ANY)

    # bottom_panel 向け要素
    bottom_panel = wx.Panel(main_panel,wx.ID_ANY)
    bottom_panel.SetBackgroundColour('#FFFFFF')
    memo_stext = wx.StaticText(bottom_panel, wx.ID_ANY, 'メモ')
    memo_textc = wx.TextCtrl(bottom_panel, wx.ID_ANY, style=wx.TE_MULTILINE, size=(560, 70))
    exechg_button = wx.Button(bottom_panel, wx.ID_ANY, '変換実行')

    # bottom_panel 向け Sizer
    bottom_panel_sizer = wx.FlexGridSizer(rows=3, cols=1, gap=(0, 0))
    bottom_panel_sizer.Add(memo_stext, 0, wx.LEFT | wx.TOP, 10)
    bottom_panel_sizer.Add(memo_textc, 0, wx.LEFT | wx.BOTTOM, 10)
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
    #io_path_panel.SetBackgroundColour('#AA0000')
    io_path_panel2 = wx.Panel(io_path_panel, wx.ID_ANY)
    #io_path_panel2.SetBackgroundColour('#AA0DD0')

    # io_path_panel2向け要素
    workdir_stext = wx.StaticText(io_path_panel2, wx.ID_ANY, 'ワークディレクトリ[WORK_DIR]: \n※絶対パス指定')
    sourcedir_stext = wx.StaticText(io_path_panel2, wx.ID_ANY, '変換前ファイルディレクトリ[SOURCE_DIR]: \n※WORK_DIRからの相対パス指定')
    writedir_stext = wx.StaticText(io_path_panel2, wx.ID_ANY, '変換後ファイルディレクトリ[WRITE_DIR]: \n※WORK_DIRからの相対パス指定')
    workdir_textc = wx.TextCtrl(io_path_panel2, wx.ID_ANY, size=(350,-1))
    sourcedir_textc = wx.TextCtrl(io_path_panel2, wx.ID_ANY, size=(350,-1))
    writedir_textc = wx.TextCtrl(io_path_panel2, wx.ID_ANY, size=(350,-1))

    # io_path_panel2向けSizer
    io_path_panel2_sizer = wx.FlexGridSizer(rows=3, cols=2, gap=(8, 10))
    io_path_panel2_sizer.Add(workdir_stext)
    io_path_panel2_sizer.Add(workdir_textc)
    io_path_panel2_sizer.Add(sourcedir_stext)
    io_path_panel2_sizer.Add(sourcedir_textc)
    io_path_panel2_sizer.Add(writedir_stext)
    io_path_panel2_sizer.Add(writedir_textc)
    #io_path_panel2_sizer.AddGrowableCol(0, 2)
    #io_path_panel2_sizer.AddGrowableCol(1, 1)
    io_path_panel2.SetSizer(io_path_panel2_sizer)

    # io_path_panel向けSizer
    io_path_panel_box = wx.StaticBox(io_path_panel, wx.ID_ANY, '入出力パス設定')
    io_path_panel_sizer = wx.StaticBoxSizer(io_path_panel_box, wx.VERTICAL)
    io_path_panel_sizer.Add(io_path_panel2)
    io_path_panel.SetSizer(io_path_panel_sizer)


    # sep_panel向け要素
    sep_panel = wx.Panel(tab_base, wx.ID_ANY)
    #sep_panel.SetBackgroundColour('#ff00ff')
    sep_panel2 = wx.Panel(sep_panel, wx.ID_ANY)
    #sep_panel2.SetBackgroundColour('#EE00EE')

    # sep_panel2向け要素
    inputsep_stext = wx.StaticText(sep_panel2, wx.ID_ANY, '入力ファイル区切り文字[INPUT_SEP]')
    outputsep_stext = wx.StaticText(sep_panel2, wx.ID_ANY, '出力ファイル区切り文字[OUTPUT_SEP]')
    inputsep_cbox = wx.ComboBox(sep_panel2, wx.ID_ANY, 'COMMA', choices=('COMMA', 'TAB', 'SPACE'), style=wx.CB_READONLY)
    outputsep_cbox = wx.ComboBox(sep_panel2, wx.ID_ANY, 'COMMA', choices=('COMMA', 'TAB', 'SPACE'), style=wx.CB_READONLY)
    sep_stext = wx.StaticText(sep_panel2, wx.ID_ANY, 'COMMA, TAB, SPACE のどれかを選択。\n\
INPUT_SEPにSPACEを選択した場合のみ、連続するセパレータは1つと解釈されます。\n\n\
<例>\n\
（変換前）行：　"foo"␣␣␣"var"␣␣␣␣␣"hoge"　（<--半角スペースを␣で表示）\n\
（変換後）行：　"foo" ,"var","hoge"\n\
※連続するスペースは一つのスペースセパレータと解釈されます。\n\
　【行：　"foo",,,"var",,,,,"hoge"】とはなりません。')

    # sep_panel2向けSizer
    sep_panel2_sizer = wx.GridBagSizer(8,10)
    sep_panel2_sizer.Add(inputsep_stext, (0,0), (1,1))
    sep_panel2_sizer.Add(inputsep_cbox, (0,1), (1,1))
    sep_panel2_sizer.Add(outputsep_stext, (1,0), (1,1))
    sep_panel2_sizer.Add(outputsep_cbox, (1,1), (1,1))
    sep_panel2_sizer.Add(sep_stext, (2,0), (1,3))
    sep_panel2.SetSizer(sep_panel2_sizer)

    # sep_panel向けSizer
    sep_panel_box = wx.StaticBox(sep_panel, wx.ID_ANY, '区切り文字指定')
    sep_panel_sizer = wx.StaticBoxSizer(sep_panel_box, wx.VERTICAL)
    sep_panel_sizer.Add(sep_panel2, 1, wx.EXPAND)
    sep_panel.SetSizer(sep_panel_sizer)

    # enc_panel向け要素
    enc_panel = wx.Panel(tab_base, wx.ID_ANY)
    #enc_panel.SetBackgroundColour('#00ffff')
    enc_panel2 = wx.Panel(enc_panel, wx.ID_ANY)
    #enc_panel2.SetBackgroundColour('#00ccff')

    # enc_panel2向け要素
    inputenc_stext = wx.StaticText(enc_panel2, wx.ID_ANY, '入力ファイル文字コード[INPUT_ENCODE]')
    outputenc_stext = wx.StaticText(enc_panel2, wx.ID_ANY, '出力ファイル文字コード[OUTPUT_ENCODE]')
    inputenc_textc = wx.TextCtrl(enc_panel2, wx.ID_ANY, size=(100,-1))
    outputenc_textc = wx.TextCtrl(enc_panel2, wx.ID_ANY, size=(100,-1))
    enc_stext = wx.StaticText(enc_panel2, wx.ID_ANY, 'エンコードはpythonのcodecsに準拠します。<https://docs.python.jp/3/library/codecs.html>\n\n\
※日本語文字コード以外は動作確認していません。\n\
※変換不可能な文字が含まれている場合は「●」に置き換えます。\n\
※出力ファイルの文字コードをcp932にした場合、「IBM拡張文字」は「NEC選定IBM拡張文字」となります。\n\
　入力ファイルの文字コードがcp932で「IBM選定IBM拡張文字」が含まれている場合は\n\
　「NEC選定IBM拡張文字」に変換されます（Pythonの仕様）。')

    # enc_panel2向けSizer
    enc_panel2_sizer = wx.GridBagSizer(8,10)
    enc_panel2_sizer.Add(inputenc_stext, (0,0), (1,1))
    enc_panel2_sizer.Add(inputenc_textc, (0,1), (1,1))
    enc_panel2_sizer.Add(outputenc_stext, (1,0), (1,1))
    enc_panel2_sizer.Add(outputenc_textc, (1,1), (1,1))
    enc_panel2_sizer.Add(enc_stext, (2,0), (1,3))
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
    quote_cbox = wx.ComboBox(quote_panel, wx.ID_ANY, 'FALSE', choices=('FALSE', 'SINGLE', 'DOUBLE', 'QUOTES', 'SQUARE_BRACKETS', 'ALL'), style=wx.CB_READONLY)
    quote_stext = wx.StaticText(quote_panel, wx.ID_ANY, '囲み文字内に区切り文字が存在しても区切り文字として認識されません。\n\
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
    quote_panel_sizer.Add(quote_cbox, 0, wx.BOTTOM, 5)
    quote_panel_sizer.Add(quote_stext, 0, wx.BOTTOM, 5)
    quote_panel.SetSizer(quote_panel_sizer)

    # newline_panel
    newline_panel = wx.Panel(tab_quote, wx.ID_ANY)

    # newline_panel 向け要素
    newline_cbox = wx.ComboBox(newline_panel, wx.ID_ANY, 'CRLF', choices=('CRLF', 'LF', 'CR', 'FALSE'), style=wx.CB_READONLY)
    newline_stext = wx.StaticText(newline_panel, wx.ID_ANY, 'CRLF, LF, CR, FALSE のどれかを選択。\n\
FALSEの場合は元ファイルの改行コードに従う。')

    # newline_panel 向けSizer
    newline_panel_box = wx.StaticBox(newline_panel, wx.ID_ANY, '出力改行コード[NEW_LINE]')
    newline_panel_sizer = wx.StaticBoxSizer(newline_panel_box, wx.VERTICAL)
    newline_panel_sizer.Add(newline_cbox, 0, wx.BOTTOM, 5)
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
    tgtlimit_textc = wx.TextCtrl(tgtlimit_panel, wx.ID_ANY, 'FALSE', size=(50,-1))
    tgtlimit_stext = wx.StaticText(tgtlimit_panel, wx.ID_ANY, 'INPUT_SEPにSPACEを選択した場合の変換対象のカラム数を数値で指定（左から数える）。\n\
全カラムを変換対象とする場合及び、INPUT_SEPにSPACEを選択しない場合は\n\
「FALSE」を入力しておく。\n\n\
<例:6カラムのデータを3カラム分だけ変換する。（スペース区切りをカンマ区切りに変換）>\n\
（設定値）INPUT_SEP_SPACE_COL_CHG_LIMIT = 3\n\
（変換前）行：　foo var hoge foo1 var1 hoge1\n\
（変換後）行：　foo,var,hoge,foo1 var1 hoge1')

    # tgtlimit_panel 向けSizer
    tgtlimit_panel_box = wx.StaticBox(tgtlimit_panel, wx.ID_ANY, '変換対象カラム数制限[INPUT_SEP_SPACE_COL_CHG_LIMIT]')
    tgtlimit_panel_sizer = wx.StaticBoxSizer(tgtlimit_panel_box, wx.VERTICAL)
    tgtlimit_panel_sizer.Add(tgtlimit_textc, 0, wx.BOTTOM, 5)
    tgtlimit_panel_sizer.Add(tgtlimit_stext, 0, wx.BOTTOM, 5)
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
    date_line_regex_textc = wx.TextCtrl(date_panel, wx.ID_ANY, size=(560, -1))
    input_date_format_stext = wx.StaticText(date_panel, wx.ID_ANY, '入力日時フォーマット[INPUT_DATE_FORMAT]')
    input_date_format_textc = wx.TextCtrl(date_panel, wx.ID_ANY, size=(560, -1))
    output_date_format_stext = wx.StaticText(date_panel, wx.ID_ANY, '出力日時フォーマット[OUTPUT_DATE_FORMAT]')
    output_date_format_textc = wx.TextCtrl(date_panel, wx.ID_ANY, size=(560, -1))
    date_ext_stext = wx.StaticText(date_panel, wx.ID_ANY, '正規表現DATE_LINE_REGEXに従って行内に存在する日時に関わる\n\
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
    date_panel_sizer.Add(date_line_regex_textc, 0, wx.BOTTOM, 5)
    date_panel_sizer.Add(input_date_format_stext, 0, wx.BOTTOM, 5)
    date_panel_sizer.Add(input_date_format_textc, 0, wx.BOTTOM, 5)
    date_panel_sizer.Add(output_date_format_stext, 0, wx.BOTTOM, 5)
    date_panel_sizer.Add(output_date_format_textc, 0, wx.BOTTOM, 5)
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
    extract_textc = wx.TextCtrl(extract_panel, wx.ID_ANY, size=(560, -1))
    extract_stext = wx.StaticText(extract_panel, wx.ID_ANY, '正規表現に一致する文字列を含む行のみ出力する。\n使用しない場合は空白とする。')

    # extract_panel 向けSizer
    extract_panel_box = wx.StaticBox(extract_panel, wx.ID_ANY, '抽出用正規表現[EXTRACT_ON_REGEX]')
    extract_panel_sizer = wx.StaticBoxSizer(extract_panel_box, wx.VERTICAL)
    extract_panel_sizer.Add(extract_textc, 0, wx.BOTTOM, 5)
    extract_panel_sizer.Add(extract_stext, 0, wx.BOTTOM, 5)
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
    log_path_textc = wx.TextCtrl(log_panel, wx.ID_ANY, './editLogs.log', size=(560, -1))
    log_enc_stext = wx.StaticText(log_panel, wx.ID_ANY, 'ログ文字コード[ENCODING]')
    log_enc_textc = wx.TextCtrl(log_panel, wx.ID_ANY, EditLogConstant.CONF_ENC, size=(560, -1))
    log_date_stext = wx.StaticText(log_panel, wx.ID_ANY, 'ログ日時フォーマット[DATE_FMT]')
    log_date_textc = wx.TextCtrl(log_panel, wx.ID_ANY, '%Y/%m/%d %H:%M:%S', size=(560, -1))
    log_fmtconsole_stext = wx.StaticText(log_panel, wx.ID_ANY, 'コンソール向けログフォーマット[FORMAT_CONSOLE]')
    log_fmtconsole_textc = wx.TextCtrl(log_panel, wx.ID_ANY, '%(asctime)s.%(msecs)d : %(name)s : %(levelname)s : %(lineno)d : "%(message)s"', size=(560, -1))
    log_fmtfile_stext = wx.StaticText(log_panel, wx.ID_ANY, 'ファイル向けログフォーマット[FORMAT_FILE]')
    log_fmtfile_textc = wx.TextCtrl(log_panel, wx.ID_ANY, '"%(asctime)s"	"%(msecs)d"	"%(name)s"	"%(levelname)s"	"%(lineno)d"	"%(message)s"', size=(560, -1))

    # log_panel 向けSizer
    log_panel_box = wx.StaticBox(log_panel, wx.ID_ANY, 'ログ設定')
    log_panel_sizer = wx.StaticBoxSizer(log_panel_box, wx.VERTICAL)
    log_panel_sizer.Add(log_path_stext, 0, wx.BOTTOM, 5)
    log_panel_sizer.Add(log_path_textc, 0, wx.BOTTOM, 5)
    log_panel_sizer.Add(log_enc_stext, 0, wx.BOTTOM, 5)
    log_panel_sizer.Add(log_enc_textc, 0, wx.BOTTOM, 5)
    log_panel_sizer.Add(log_date_stext, 0, wx.BOTTOM, 5)
    log_panel_sizer.Add(log_date_textc, 0, wx.BOTTOM, 5)
    log_panel_sizer.Add(log_fmtconsole_stext, 0, wx.BOTTOM, 5)
    log_panel_sizer.Add(log_fmtconsole_textc, 0, wx.BOTTOM, 5)
    log_panel_sizer.Add(log_fmtfile_stext, 0, wx.BOTTOM, 5)
    log_panel_sizer.Add(log_fmtfile_textc, 0, wx.BOTTOM, 5)
    log_panel.SetSizer(log_panel_sizer)

    # tab_log
    tab_log_sizer = wx.BoxSizer(wx.VERTICAL)
    tab_log_sizer.Add(log_panel, 0, wx.EXPAND | wx.ALL, 5)
    tab_log.SetSizer(tab_log_sizer)



    # frame表示
    frame.Show()
    # なんか変なのが表示される対処
    #notebook.Refresh()
    # Window表示
    application.MainLoop()


