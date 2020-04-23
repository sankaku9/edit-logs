from tkinter import ttk, Tk, messagebox, Menu, Text


def open_file():
    pass


def save_file():
    pass


def change_sep():
    input_value = input_encode_entry.get()
    combo_value = input_sep_combo.get()
    combo_index = input_sep_combo.current()
    messagebox.showinfo("クリックイベント", input_value + combo_value + str(combo_index) + "が入力されました。")


if __name__ == '__main__':

    root = Tk()
    root.title('セパレータ変換')

    sep_mn = Menu(root)
    sep_mn_cmd = Menu(sep_mn, tearoff=False)
    sep_mn_cmd.add_command(label='開く', command=open_file)
    sep_mn_cmd.add_separator()
    sep_mn_cmd.add_command(label='保存', command=save_file)
    sep_mn.add_cascade(label='設定ファイル', menu=sep_mn_cmd)

    mainFrame = ttk.Frame(root)
    mainFrame.pack()

    frame1 = ttk.Frame(mainFrame)
    frame1['height'] = 600
    frame1['width'] = 550
    frame1['relief'] = 'flat'
    frame1['borderwidth'] = 1
    frame1.grid(row=1, column=0)

    main_nb = ttk.Notebook(frame1, width=535, height=562)
    tab_change = ttk.Frame(main_nb)
    tab_quote = ttk.Frame(main_nb)
    tab_tgtlimit = ttk.Frame(main_nb)
    tab_date = ttk.Frame(main_nb)
    tab_extract = ttk.Frame(main_nb)
    tab_path = ttk.Frame(main_nb)
    tab_log = ttk.Frame(main_nb)
    main_nb.add(tab_change, text='変換', padding=3)
    main_nb.add(tab_quote, text='囲み文字', padding=3)
    main_nb.add(tab_tgtlimit, text='変換制限', padding=3)
    main_nb.add(tab_date, text='日時抽出付与', padding=3)
    main_nb.add(tab_extract, text='行抽出', padding=3)
    main_nb.add(tab_path, text='パス', padding=3)
    main_nb.add(tab_log, text='ログ', padding=3)
    main_nb.pack(expand=1, fill='both')

    # ==========
    # tab_change
    # ==========
    encode_label = ttk.Label(tab_change, text="## エンコード指定\n\n")
    encode_label.place(x=10, y=10)
    input_encode_label = ttk.Label(tab_change, text="入力ファイル文字コード[INPUT_ENCODE]")
    input_encode_label.place(x=10, y=30)
    input_encode_entry = ttk.Entry(tab_change, width=15)
    input_encode_entry.place(x=230, y=30)
    output_encode_label = ttk.Label(tab_change, text="出力ファイル文字コード[OUTPUT_ENCODE]")
    output_encode_label.place(x=10, y=55)
    output_encode_entry = ttk.Entry(tab_change, width=15)
    output_encode_entry.place(x=230, y=55)
    encode_label_dtl = ttk.Label(tab_change, text="エンコードはpythonのcodecsに準拠します。<https://docs.python.jp/3/library/codecs.html>\n\n\
※日本語文字コード以外は動作確認していません。\n\
※変換不可能な文字が含まれている場合はエラーとなります。\n\
※出力ファイルの文字コードをcp932にした場合、「IBM拡張文字」は「NEC選定IBM拡張文字」となります。\n\
　入力ファイルの文字コードがcp932で「IBM選定IBM拡張文字」が含まれている場合は\n\
　「NEC選定IBM拡張文字」に変換されます（Pythonの仕様）。")
    encode_label_dtl.place(x=10, y=80)

    sep_label = ttk.Label(tab_change, text="## 区切り文字指定")
    sep_label.place(x=10, y=200)
    input_sep_label = ttk.Label(tab_change, text="入力ファイル区切り文字[INPUT_SEP]")
    input_sep_label.place(x=10, y=220)
    input_sep_combo = ttk.Combobox(tab_change, state='readonly', width=8)
    input_sep_combo["values"] = ("COMMA", "TAB", "SPACE")
    input_sep_combo.current(0)
    input_sep_combo.place(x=230, y=220)
    output_sep_label = ttk.Label(tab_change, text="出力ファイル区切り文字[OUTPUT_SEP]")
    output_sep_label.place(x=10, y=245)
    output_sep_combo = ttk.Combobox(tab_change, state='readonly', width=8)
    output_sep_combo["values"] = ("COMMA", "TAB", "SPACE")
    output_sep_combo.current(0)
    output_sep_combo.place(x=230, y=245)
    sep_label_dtl = ttk.Label(tab_change, text="COMMA, TAB, SPACE のどれかを選択。\n\
INPUT_SEPにSPACEを選択した場合のみ、連続するセパレータは1つと解釈されます。\n\n\
<例>\n\
（変換前）行：　""foo""␣␣␣""var""␣␣␣␣␣""hoge""　（<--半角スペースを␣で表示）\n\
（変換後）行：　""foo"" ,""var"",""hoge""\n\
※連続するスペースは一つのスペースセパレータと解釈されます。【行：　""foo"",,,""var"",,,,,""hoge""】とはなりません。")
    sep_label_dtl.place(x=10, y=270)

    new_line_label = ttk.Label(tab_change, text="## 出力改行コード[NEW_LINE]")
    new_line_label.place(x=10, y=390)
    new_line_combo = ttk.Combobox(tab_change, state='readonly', width=6)
    new_line_combo["values"] = ("CRLF", "LF", "CR", "FALSE")
    new_line_combo.current(0)
    new_line_combo.place(x=10, y=410)
    new_line_label_dtl = ttk.Label(tab_change, text="CRLF, LF, CR, FALSE のどれかを選択。\n\
FALSEの場合は元ファイルの改行コードに従う。")
    new_line_label_dtl.place(x=10, y=440)

    # ==========
    # tab_quote
    # ==========
    quote_label = ttk.Label(tab_quote, text="1カラムであることを示す囲み文字[QUOTE]")
    quote_label.place(x=10, y=10)
    quote_combo = ttk.Combobox(tab_quote, state='readonly')
    quote_combo["values"] = ("FALSE", "SINGLE", "DOUBLE", "QUOTES", "SQUARE_BRACKETS", "ALL")
    quote_combo.current(0)
    quote_combo.place(x=10, y=30)
    quote_combo_label_dtl = ttk.Label(tab_quote, text="囲み文字内に区切り文字が存在しても区切り文字として認識されません。\n\
    （例）'fo,o' \"va,r\" [h,oge]\n\n\
設定可能なパラメータは以下の通り。\n\
    ・FALSE : 囲み文字処理無し\n\
    ・SINGLE : <''>\n\
    ・DOUBLE : <\"\">\n\
    ・QUOTES : <''> + <\"\">\n\
    ・SQUARE_BRACKETS : <[]>\n\
    ・ALL : <''> + <\"\"> + <[]>\n\n\
<QUOTES, ALLを選択した場合の注意点>\n\
１．囲み文字内に区切り文字が含まれていて、囲み文字の始まりと終わりが異なる場合はエラーとなります。\n\
    （例）'fo,o\" \"va,r' [h,oge\" \n\n\
２．囲み文字内に区切り文字が無い場合は囲み文字の不整合はエラーにならず、そのまま出力します。\n\
    （例）'foo\" \"var' [hoge\"")
    quote_combo_label_dtl.place(x=10, y=60)

    # ==========
    # tab_tgtlimit
    # ==========
    input_sep_limit_label = ttk.Label(tab_tgtlimit, text="変換対象カラム数制限[INPUT_SEP_SPACE_COL_CHG_LIMIT]")
    input_sep_limit_label.place(x=10, y=10)
    input_sep_limit_entry = ttk.Entry(tab_tgtlimit, width=6)
    input_sep_limit_entry.place(x=10, y=30)
    input_sep_limit_entry.insert(0, "FALSE")
    input_sep_limit_label_dtl = ttk.Label(tab_tgtlimit, text="INPUT_SEPにSPACEを選択した場合の変換対象のカラム数を数値で指定（左から数える）。\n\
全カラムを変換対象とする場合及び、INPUT_SEPにSPACEを選択しない場合はFALSEとする。\n\n\
<例:6カラムのデータを3カラム分だけ変換する。（スペース区切りをカンマ区切りに変換）>\n\
（設定値）INPUT_SEP_SPACE_COL_CHG_LIMIT = 3\n\
（変換前）行：　foo var hoge foo1 var1 hoge1\n\
（変換後）行：　foo,var,hoge,foo1 var1 hoge1")

    input_sep_limit_label_dtl.place(x=10, y=60)

    # ==========
    # tab_date
    # ==========
    date_ext_label = ttk.Label(tab_date, text="## 日時文字列取得用パラメータ")
    date_ext_label.place(x=10, y=10)
    date_line_regex_label = ttk.Label(tab_date, text="日時文字列取得用正規表現[DATE_LINE_REGEX]")
    date_line_regex_label.place(x=10, y=40)
    date_line_regex_entry = ttk.Entry(tab_date, width=80)
    date_line_regex_entry.place(x=10, y=60)
    input_date_format_label = ttk.Label(tab_date, text="入力日時フォーマット[INPUT_DATE_FORMAT]")
    input_date_format_label.place(x=10, y=90)
    input_date_format_entry = ttk.Entry(tab_date, width=80)
    input_date_format_entry.place(x=10, y=110)
    output_date_format_label = ttk.Label(tab_date, text="出力日時フォーマット[OUTPUT_DATE_FORMAT]")
    output_date_format_label.place(x=10, y=140)
    output_date_format_entry = ttk.Entry(tab_date, width=80)
    output_date_format_entry.place(x=10, y=160)
    date_ext_label_dtl = ttk.Label(tab_date, text="正規表現DATE_LINE_REGEXに従って行内に存在する日時に関わる\n\
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
3行目：　2017/08/21 10:10:10,foo2,var2,hoge2,hoge22")
    date_ext_label_dtl.place(x=10, y=190)

    # ==========
    # tab_extract
    # ==========
    extract_label = ttk.Label(tab_extract, text="抽出用正規表現[EXTRACT_ON_REGEX]")
    extract_label.place(x=10, y=10)
    extract_entry = ttk.Entry(tab_extract, width=80)
    extract_entry.place(x=10, y=30)
    extract_label_dtl = ttk.Label(tab_extract, text="正規表現に一致する文字列を含む行のみ出力する。\n使用しない場合は空白とする。")
    extract_label_dtl.place(x=10, y=60)

    # ==========
    # tab_path
    # ==========
    work_dir_label = ttk.Label(tab_path, text="ワークディレクトリ[WORK_DIR]\n※絶対パス指定")
    work_dir_label.place(x=10, y=10)
    work_dir_entry = ttk.Entry(tab_path, width=80)
    work_dir_entry.place(x=10, y=45)

    source_dir_label = ttk.Label(tab_path, text="変換前ファイルディレクトリ[SOURCE_DIR]\n※WORK_DIRからの相対パス指定")
    source_dir_label.place(x=10, y=80)
    source_dir_entry = ttk.Entry(tab_path, width=80)
    source_dir_entry.place(x=10, y=115)

    write_dir_label = ttk.Label(tab_path, text="変換後ファイルディレクトリ[WRITE_DIR]\n※WORK_DIRからの相対パス指定")
    write_dir_label.place(x=10, y=150)
    write_dir_entry = ttk.Entry(tab_path, width=80)
    write_dir_entry.place(x=10, y=185)

    # ==========
    # tab_log
    # ==========
    log_path_label = ttk.Label(tab_log, text="ログ出力パス[PATH]")
    log_path_label.place(x=10, y=10)
    log_path_entry = ttk.Entry(tab_log, width=80)
    log_path_entry.place(x=10, y=30)
    log_path_entry.insert(0, "./editLogs.log")

    log_enc_label = ttk.Label(tab_log, text="ログ文字コード[ENCODING]")
    log_enc_label.place(x=10, y=60)
    log_enc_entry = ttk.Entry(tab_log, width=5)
    log_enc_entry.place(x=10, y=80)
    log_enc_entry.insert(0, "utf_8")

    log_date_label = ttk.Label(tab_log, text="ログ日時フォーマット[DATE_FMT]")
    log_date_label.place(x=10, y=110)
    log_date_entry = ttk.Entry(tab_log, width=80)
    log_date_entry.place(x=10, y=130)
    log_date_entry.insert(0, "%Y/%m/%d %H:%M:%S")

    log_fmtconsole_label = ttk.Label(tab_log, text="コンソール向けログフォーマット[FORMAT_CONSOLE]")
    log_fmtconsole_label.place(x=10, y=160)
    log_fmtconsole_entry = ttk.Entry(tab_log, width=80)
    log_fmtconsole_entry.place(x=10, y=180)
    log_fmtconsole_entry.insert(0, '%(asctime)s.%(msecs)d : %(name)s : %(levelname)s : %(lineno)d : "%(message)s"')

    log_fmtfile_label = ttk.Label(tab_log, text="ファイル向けログフォーマット[FORMAT_FILE]")
    log_fmtfile_label.place(x=10, y=210)
    log_fmtfile_entry = ttk.Entry(tab_log, width=80)
    log_fmtfile_entry.place(x=10, y=230)
    log_fmtfile_entry.insert(0, '"%(asctime)s"	"%(msecs)d"	"%(name)s"	"%(levelname)s"	"%(lineno)d"	"%(message)s"')


    frame3 = ttk.Frame(mainFrame)
    frame3['height'] = 160
    frame3['width'] = 550
    frame3['relief'] = 'flat'
    frame3['borderwidth'] = 5
    frame3.grid(row=2, column=0)

    memo_label = ttk.Label(frame3, text="メモ")
    memo_label.place(x=5, y=0)
    memo_text = Text(frame3, width=75, height=5)
    memo_text.place(x=5, y=18)

    exe_change_btn = ttk.Button(frame3, text="変換実行", command=change_sep)
    exe_change_btn.place(x=460, y=120)

    root.config(menu=sep_mn)
    root.resizable(width=False, height=False)
    root.mainloop()
