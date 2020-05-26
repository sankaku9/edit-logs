import re
import shutil
import tempfile
import datetime
import common.EditLogBase

class ComChgSep:

    def __init__(self):
        pass

    # 区切り文字変更
    def chg_sep(self, loggername, filePath, inenc, outenc, insep, outsep, nl, quote, spaceChgLim, dateRegex, indateform, outdateform, extregex):

        # 入力値チェック
        insepList = ['COMMA','TAB','SPACE']
        if insep not in insepList:
            raise ValueError('INPUT_SEPを正しく設定してください')

        outsepList = ['COMMA','TAB','SPACE']
        if outsep not in outsepList:
            raise ValueError('OUTPUT_SEPを正しく設定してください')

        nlList = ['CRLF','LF','CR','FALSE']
        if nl not in nlList:
            raise ValueError('NEW_LINEを正しく設定してください')

        quoteList = ['SINGLE','DOUBLE','QUOTES','SQUARE_BRACKETS','ALL','FALSE']
        if quote not in quoteList:
            raise ValueError('QUOTEを正しく設定してください')

        if not spaceChgLim.isdigit() and not spaceChgLim == 'FALSE':
            raise ValueError('INPUT_SEP_SPACE_COL_CHG_LIMITを正しく設定してください')

        # 共通処理インスタンス取得
        comE = common.EditLogBase.EditLogBase()

        # デフォルト初期値は何もマッチさせない。
        splitColumStartRegex = '$^'
        splitColumEndRegex = '$^'
        if quote == 'SINGLE':
            splitColumStartRegex = '^[\'][^\']*$'
            splitColumEndRegex = '^[^\']*[\']$'
        elif quote == 'DOUBLE':
            splitColumStartRegex = '^["][^"]*$'
            splitColumEndRegex = '^[^"]*["]$'
        elif quote == 'SQUARE_BRACKETS':
            splitColumStartRegex = '^[\[][^\]]*$'
            splitColumEndRegex = '^[^\[]*[\]]$'
        elif quote == 'QUOTES':
            splitColumStartRegex = '^[\'"][^\'"]*$'
            splitColumEndRegex = '^[^\'"]*[\'"]$'
        elif quote == 'ALL':
            splitColumStartRegex = '^[\'"\[][^\'"\]]*$'
            splitColumEndRegex = '^[^\'"\[]*[\'"\]]$'

        # 書き込み用日時文字列
        dateStr = ''

        # 対象ファイルを読み込む。
        with open(filePath, newline='', encoding=inenc) as fo:
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                foLine = fo.readline()
                i = 0
                while foLine:
                    foLineReplaced = foLine
                    # オリジナル改行コード取得
                    orgNl = comE.getNewLine(foLineReplaced)

                    # 改行コード除去
                    foLineReplaced = comE.deleteNewLine(foLineReplaced)

                    foLineReplacedList = []
                    # insepでsplit
                    if insep == 'COMMA':
                        foLineReplacedList = foLineReplaced.split(',')
                    elif insep == 'TAB':
                        foLineReplacedList = foLineReplaced.split('\t')
                    elif insep == 'SPACE':
                        foLineReplacedList = foLineReplaced.split(' ')

                    # ["]で始まる要素は次の["]で終わる要素と結合。[']を使用している場合は引数で指定。
                    renewFoLineReplacedList = []
                    renewFoLineReplacedListTmp = []
                    renewFoLineReplacedListTmpForSpace = []
                    for foLineReplacedListCol in foLineReplacedList:

                        # INPUT_SEPにSPACEを選択して、変換対象要素数が指定されている場合
                        if insep == 'SPACE' and (not spaceChgLim == 'FALSE' and len(renewFoLineReplacedList) > int(spaceChgLim)-1):
                            #renewFoLineReplacedListTmpForSpace.append(foLineReplacedListCol)
                            pass

                        # QUOTE文字から始まり、QUOTE文字で終わらない要素であり、分割されてしまった同一カラムと判断される場合
                        elif re.match(splitColumStartRegex, foLineReplacedListCol) and not re.match(splitColumEndRegex, foLineReplacedListCol):
                            if len(renewFoLineReplacedListTmp) != 0:
                                raise RuntimeError('入力ファイルのQUOTE文字に不正の可能性があります: ' + foLine)
                            #　要素が'"で始まる場合は次の要素も同一要素なので一時要素格納リストに追加
                            renewFoLineReplacedListTmp.append(foLineReplacedListCol)
                        # 分割されてしまった同一カラム格納リストrenewFoLineReplacedListTmpが空でなく、QUOTE文字で終わらない要素の場合
                        elif len(renewFoLineReplacedListTmp) != 0 and not re.match(splitColumEndRegex, foLineReplacedListCol):
                            #　renewFoLineReplacedListTmpが0でない
                            # 要素の終端'"でもない
                            # 場合は同一要素内なので一時要素格納リストに追加
                            renewFoLineReplacedListTmp.append(foLineReplacedListCol)
                        # 分割されてしまった同一カラム格納リストrenewFoLineReplacedListTmpが空でなく、QUOTE文字で終わる要素の場合
                        elif len(renewFoLineReplacedListTmp) != 0 and re.match(splitColumEndRegex, foLineReplacedListCol):
                            # 結合対象Listの0番目要素1文字目と最終コードが一致しない場合はエラー
                            if renewFoLineReplacedListTmp[0][:1] != foLineReplacedListCol[-1:] :
                                # 但し括弧の場合は開始と閉じで対になっていればOK
                                if renewFoLineReplacedListTmp[0][:1] == '[' and foLineReplacedListCol[-1:] == ']':
                                    pass
                                else:
                                    raise RuntimeError('入力ファイルのQUOTE文字に不正の可能性があります: ' + foLine)

                            #　要素が'"で終わる場合は前までの要素と同一要素なので一時要素格納リストに追加
                            renewFoLineReplacedListTmp.append(foLineReplacedListCol)

                            # 分割されてしまった同一カラム格納リストを結合
                            # insepでjoinしてリストに追加
                            if insep == 'COMMA':
                                renewFoLineReplacedList.append(','.join(renewFoLineReplacedListTmp))
                            elif insep == 'TAB':
                                renewFoLineReplacedList.append('\t'.join(renewFoLineReplacedListTmp))
                            elif insep == 'SPACE':
                                renewFoLineReplacedList.append(' '.join(renewFoLineReplacedListTmp))

                            # 分割されてしまった同一カラム格納リスト初期化
                            renewFoLineReplacedListTmp = []

                        # INPUT_SEPにSPACEを選択した場合で、foLineReplacedListColが空の場合はSPACEセパレータが連続していると判断してrenewFoLineReplacedListにappendしない。
                        elif insep == 'SPACE' and foLineReplacedListCol == '':
                            pass

                        # QUOTE文字を含まないカラムの場合
                        else:
                            renewFoLineReplacedList.append(foLineReplacedListCol)

                    # INPUT_SEPにSPACEを選択して、変換対象カラム数が指定されている場合
                    # 変換対象外要素がrenewFoLineReplacedListTmpForSpaceに格納されているので、それらをjoinしてからrenewFoLineReplacedListにappend
                    if len(renewFoLineReplacedListTmpForSpace) != 0:
                        renewFoLineReplacedList.append(' '.join(renewFoLineReplacedListTmpForSpace))

                    # オリジナル行から日時文字列取得
                    if dateRegex != '' and re.search(dateRegex, foLine):
                        dateStr = re.findall(dateRegex, foLine)[0]
                        dateStr = datetime.datetime.strptime(dateStr, indateform).strftime(outdateform)

                    # 書き込み用文字列
                    tmpLineReplaced = ''
                    # outsepでjoin
                    if outsep == 'COMMA':
                        tmpLineReplaced = ','.join(renewFoLineReplacedList)
                        # 日時文字列が取得されている場合は行頭に付与
                        if dateStr != '':
                            tmpLineReplaced = ','.join([dateStr, tmpLineReplaced])

                    elif outsep == 'TAB':
                        tmpLineReplaced = '\t'.join(renewFoLineReplacedList)
                        # 日時文字列が取得されている場合は行頭に付与
                        if dateStr != '':
                            tmpLineReplaced = '\t'.join([dateStr, tmpLineReplaced])

                    elif outsep == 'SPACE':
                        tmpLineReplaced = ' '.join(renewFoLineReplacedList)
                        # 日時文字列が取得されている場合は行頭に付与
                        if dateStr != '':
                            tmpLineReplaced = ' '.join([dateStr, tmpLineReplaced])


                    # 引数の改行コード判定
                    if nl == 'FALSE':
                        nl = orgNl

                    # 改行コード付与
                    tmpLineReplaced = comE.addNewLine(tmpLineReplaced, nl)

                    if extregex != '':
                        if re.search(extregex, foLine):
                            # エンコード不可文字を●で塗りつぶしつつファイル書き込み
                            tmpLineReplaced = comE.replaceEncErrorWrite(loggername, filePath, i, tf, tmpLineReplaced, inenc, outenc)
                            # 一時ファイルへの書き込み
                            # tf.write(tmpLineReplaced.encode(outenc))
                    else:
                        # エンコード不可文字を●で塗りつぶしつつファイル書き込み
                        tmpLineReplaced = comE.replaceEncErrorWrite(loggername, filePath, i, tf, tmpLineReplaced, inenc, outenc)
                        # 一時ファイルへの書き込み
                        #tf.write(tmpLineReplaced.encode(outenc))

                    # 入力ファイルの次の行を読み込む
                    foLine = fo.readline()

                    i+=1

                tfName = tf.name
            # 一時ファイルを対象ファイルに上書きする。
            shutil.move(tfName, filePath)



