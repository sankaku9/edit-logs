import os
import sys
import logging
import csv
import shutil
import re
from collections import OrderedDict
from distutils.dir_util import copy_tree
from datetime import datetime
# importの指定は当ファイルからではなく実行ファイルのディレクトリからの相対で指定
import common.EditLogLogging

class EditLogBase:

    def __init__(self, loggerName):
        if loggerName != '':
            common.EditLogLogging.EditLogLogging(loggerName)
            self.thisLogger = logging.getLogger(''.join([loggerName, '.', re.sub('\..*', '', os.path.basename(__file__))]))


    # 起動処理
    def start(self):
        self.thisLogger.log(20, '---start--------------------')
        pass

    # 終了処理
    def end(self):
        self.thisLogger.log(20, '---end--------------------')
        sys.exit()

    # クリーンなディレクトリ作成
    def makeDir(self, path):
        # 出力先ディレクトリ存在確認
        if os.path.isdir(path):
            #　設定誤り等により、意図しないディレクトリを誤って削除してしまうことを防止するため、自動削除しません。
            # shutil.rmtree(path)
            # raise RuntimeError(''.join(['出力先ディレクトリが存在しています。手動で削除してください。',path]))
            # →消すの面倒だしmoveにしようかな・・・
            while True:
                addPath = ''.join([re.sub(r'[/\\]+$','',path), datetime.now().strftime("_%Y%m%d%H%M%S%f")])
                if not os.path.isdir(addPath):
                    shutil.move(path, addPath)
                    break

        # 出力先ディレクトリ作成
        os.makedirs(path)

    # tsvファイルの内容をOrderedDictに格納
    # tsvファイルの列数は2固定
    # return : dict : collections.OrderedDict
    def updateDictFromTsv(self,tsvFilePath,enc):
        # 置換順序を保証するためDictではなくOrderedDictを使用する。
        kvDict = OrderedDict()

        with open(tsvFilePath, newline='', encoding=enc) as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                kvDict.update({row[0]:row[1]})

        return kvDict

    # ディレクトリ階層構造を維持した状態でファイルをコピーする。
    def copyFileAsTree(self, root, file, writeDir):
        dirName = os.path.join(writeDir, re.sub('[:*\?"<>\|]','',root.strip('./\\'))).replace(os.path.sep, '/')
        sourceFileName = os.path.join(root, file).replace(os.path.sep, '/')
        resultFileName = os.path.join(writeDir,
                                      re.sub('[:*\?"<>\|]','',root.strip('./\\')),
                                      file).replace(os.path.sep, '/')

        # ディレクトリ作成
        os.makedirs(dirName, exist_ok=True)
        # ファイルコピー
        shutil.copy(sourceFileName,resultFileName)

        return resultFileName

    # 特定ディレクトリ配下のファイル/ディレクトリをまとめて全てコピーする。
    def copyTreeAll(self, root, writeDir):
        copy_tree(root.replace(os.path.sep, '/'),
                  os.path.join(writeDir,
                               re.sub('[:*\?"<>\|]','',root.strip('./\\'))).replace(os.path.sep, '/'))

    # 改行コード置換
    def replaceNewLine(self, targetStr, nl):
        strend = targetStr[-2:]
        if nl == 'CRLF':
            if strend == '\r\n':
                pass
            elif re.match('[^\r]\n',strend):
                targetStr = targetStr.replace('\n', '\r\n')
            elif re.match('.\r',strend):
                targetStr = targetStr.replace('\r', '\r\n')
        elif nl == 'LF':
            if strend == "\r\n":
                targetStr = targetStr.replace('\r\n', '\n')
            elif re.match('[^\r]\n',strend):
                pass
            elif re.match('.\r',strend):
                targetStr = targetStr.replace('\r', '\n')
        elif nl == 'CR':
            if strend == "\r\n":
                targetStr = targetStr.replace('\r\n', '\r')
            elif re.match('[^\r]\n',strend):
                targetStr = targetStr.replace('\n', '\r')
            elif re.match('.\r',strend):
                pass
        else:
            pass

        return targetStr

    # 改行コード付与
    def addNewLine(self, targetStr, nl):
        strend = targetStr[-2:]
        if nl == 'CRLF':
            if strend == '\r\n':
                pass
            elif re.match('[^\r]\n',strend):
                targetStr = targetStr.replace('\n', '\r\n')
            elif re.match('.\r',strend):
                targetStr = targetStr.replace('\r', '\r\n')
            else:
                targetStr = ''.join([targetStr, '\r\n'])
        elif nl == 'LF':
            if strend == "\r\n":
                targetStr = targetStr.replace('\r\n', '\n')
            elif re.match('[^\r]\n',strend):
                pass
            elif re.match('.\r',strend):
                targetStr = targetStr.replace('\r', '\n')
            else:
                targetStr = ''.join([str, '\n'])
        elif nl == 'CR':
            if strend == "\r\n":
                targetStr = targetStr.replace('\r\n', '\r')
            elif re.match('[^\r]\n',strend):
                targetStr = targetStr.replace('\n', '\r')
            elif re.match('.\r',strend):
                pass
            else:
                targetStr = ''.join([str, '\r'])
        else:
            pass

        return targetStr

    # 改行コード取得
    def getNewLine(self, targetStr):

        nlCode = ''

        strend = targetStr[-2:]
        if strend == '\r\n':
            nlCode = 'CRLF'
        elif re.match('[^\r]\n',strend):
            nlCode = 'LF'
        elif re.match('.\r',strend):
            nlCode = 'CR'
        else:
            pass

        return nlCode

    # 改行コード除去
    def deleteNewLine(self, targetStr):

        strend = targetStr[-2:]
        if strend == '\r\n':
            targetStr = targetStr.replace('\r\n', '')
        elif re.match('[^\r]\n',strend):
            targetStr = targetStr.replace('\n', '')
        elif re.match('.\r',strend):
            targetStr = targetStr.replace('\r', '')
        else:
            pass

        return targetStr

    # 文字列両端クォート除去
    # stripを使用すべきかreで行くか悩み中
    def delQuoteStartEnd(self, targetStr):
        targetStr = re.sub('(^["\']|["\']$)','',targetStr)
        return targetStr

    # 相対パスは絶対パスに変換
    # 絶対パスはそのまま
    def chgRel2AbsPath(self, targetpath, basefilepath, addRel):
        if re.match('^(\.\./|\./)',targetpath):
            targetpath = ''.join([os.path.dirname(basefilepath),addRel,targetpath])
            targetpath = self.cutDDot(targetpath)
        else:
            pass
        return targetpath

    # パス内の[foo/../]を再帰的に除去
    def cutDDot(self, targetpath):
        if re.search(r'[^/\\]+[/\\]\.\.[\\/]',targetpath):
            targetpath = self.cutDDot(re.sub(r'[^/\\]+[/\\]\.\.[\\/]','',targetpath))
        return targetpath

    # エンコード不可文字を●で塗りつぶしつつファイル書き込み
    def replaceEncErrorWrite(self, loggername, filePath, i, tf, lineReplaced, inenc, outenc):

        logger = logging.getLogger(''.join([loggername, '.', re.sub('\.[^/\\\.]*', '', os.path.basename(__file__))]))
        comR = common.EditLogBase.EditLogBase('')

        try:
            tf.write(lineReplaced.encode(outenc))
        except UnicodeEncodeError as e:
            # 文字エンコードエラーの場合はエラー出力して処理を続ける。
            #logger.exception(e)
            logger.log(30, ''.join(['line ',str(i),' : encode error',' <file path> ',filePath]))
            #logger.log(30, 'Output by character encoding of the input file.')
            logger.log(30, 'Replace [●]')

            # ファイルには入力ファイルのエンコードで出力しておく。　　・・・のはやめて・・・
            # tf.write(lineReplaced.encode(inenc))

            # エラー文字列からデコード不可文字を取得して置換。エラー文言の仕様が変更される可能性を考えると微妙な処理だが・・・
            colList = re.search(r"'\\u[^']+'",str(e)).group().split(r'\u')
            for col in colList:
                col = comR.delQuoteStartEnd(col)
                if col != '':
                    lineReplaced = re.sub(chr(int(col, 16)),'●',lineReplaced)
                    self.replaceEncErrorWrite(loggername, filePath, i, tf, lineReplaced, inenc, outenc)

        return lineReplaced

    # configが格納されているパス一覧に指定パスの親パスに当たるものが含まれている場合はそのパスを返す。
    # 逆順でサーチ
    def getPathStartsWithInListRev(self, path, confPathsList):
        for parentConfPath in confPathsList[::-1]:
            if path.startswith(parentConfPath):
                return parentConfPath

        return ''
