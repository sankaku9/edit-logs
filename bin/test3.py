import wx


if __name__ == '__main__':

    # Window設定
    application = wx.App()
    frame = wx.Frame(None, wx.ID_ANY, title='セパレータ変換', size=(602, 820))
    #frame = wx.Frame(None, wx.ID_ANY, title='セパレータ変換', size=(602, 820), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
    #frame = wx.Frame(None, wx.ID_ANY, title='セパレータ変換')

    # メニュー
    menu_conf = wx.Menu()
    menu_conf.Append(1, '開く')
    menu_conf.Append(2, '保存')

    menu_bar = wx.MenuBar()
    menu_bar.Append(menu_conf, '設定ファイル')

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
    # tab_base向け設定
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



    # frame表示
    frame.Show()
    # なんか変なのが表示される対処
    #notebook.Refresh()
    # Window表示
    application.MainLoop()