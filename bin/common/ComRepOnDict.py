import shutil
import re
import tempfile
import common.EditLogBase

class ComRepOnDict:

    def __init__(self):
        pass

    def replaceOnRegexDict(self, loggername, filePath, regexDict, inenc, outenc, nl):
    # 置換リストOrderedDictに従ってファイル内文字列を全て置換する。
        comR = common.EditLogBase.EditLogBase()

        # 置換対象ファイルを読み込む。
        with open(filePath, newline='', encoding=inenc) as f:
            # 一時ファイルを作成して、置換後文字列を書き込む。
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                line = f.readline()
                i = 1
                while line:
                    lineReplaced = line
                    for k,v in regexDict.items():
                        lineReplaced = re.sub(k,v,lineReplaced)

                    # 改行コード変換
                    lineReplaced = comR.replaceNewLine(lineReplaced, nl)

                    # エンコード不可文字を●で塗りつぶしつつファイル書き込み
                    lineReplaced = comR.replaceEncErrorWrite(loggername, filePath, i, tf, lineReplaced, inenc, outenc)

                    line = f.readline()
                    i+=1

                tfName = tf.name
            # 一時ファイルを置換対象ファイルに上書きする。
            shutil.move(tfName, filePath)




