import os
import sys
import wx
from logging import getLogger
from csv import reader
from shutil import copy, move
from re import sub, match, search
from collections import OrderedDict
from datetime import datetime
import distutils.dir_util

class EditLogBase:

    def __init__(self):
        pass

    # 起動処理
    def start(self, logger):
        logger.log(20, '---start--------------------')
        pass

    # 終了処理
    def end(self, logger):
        logger.log(20, '---end--------------------')
        sys.exit()

    # 終了処理
    def end_gui_func(self, logger, loggerNL, application: wx):
        if logger != '':
            logger.log(20, '---end--------------------')
            for loggerName in loggerNL:
                logger.removeHandler(loggerName)
        application.InitLocale()


    # クリーンなディレクトリ作成
    def makeDir(self, path):
        # 出力先ディレクトリ存在確認
        if os.path.isdir(path):
            # 　設定誤り等により、意図しないディレクトリを誤って削除してしまうことを防止するため、自動削除しません。
            # rmtree(path)
            # raise RuntimeError(''.join(['出力先ディレクトリが存在しています。手動で削除してください。',path]))
            # →消すの面倒だしmoveにしようかな・・・
            while True:
                addPath = ''.join([sub(r'[/\\]+$', '', path), datetime.now().strftime("_%Y%m%d%H%M%S%f")])
                if not os.path.isdir(addPath):
                    move(path, addPath)
                    break

        # 出力先ディレクトリ作成
        os.makedirs(path)

    # tsvファイルの内容をOrderedDictに格納
    # tsvファイルの列数は2固定
    # return : dict : collections.OrderedDict
    def updateDictFromTsv(self, tsvFilePath, enc):
        # 置換順序を保証するためDictではなくOrderedDictを使用する。
        kvDict = OrderedDict()

        with open(tsvFilePath, newline='', encoding=enc) as f:
            tsv_reader = reader(f, delimiter='\t')
            for row in tsv_reader:
                kvDict.update({row[0]:row[1]})

        return kvDict

    # ディレクトリ階層構造を維持した状態でファイルをコピーする。
    def copyFileAsTree(self, root, file, writeDir):
        dirName = os.path.join(writeDir, sub('[:*\?"<>\|]', '', root.strip('./\\'))).replace(os.path.sep, '/')
        sourceFileName = os.path.join(root, file).replace(os.path.sep, '/')
        resultFileName = os.path.join(writeDir,
                                      sub('[:*\?"<>\|]', '', root.strip('./\\')),
                                      file).replace(os.path.sep, '/')

        # ディレクトリ作成
        os.makedirs(dirName, exist_ok=True)
        # ファイルコピー
        copy(sourceFileName, resultFileName)

        return resultFileName

    # 特定ディレクトリ配下のファイル/ディレクトリをまとめて全てコピーする。
    def copyTreeAll(self, root, writeDir):
        # キャッシュクリア
        distutils.dir_util._path_created = {}

        distutils.dir_util.copy_tree(root.replace(os.path.sep, '/'),
                  os.path.join(writeDir,
                               sub('[:*\?"<>\|]', '', root.strip('./\\'))).replace(os.path.sep, '/'))

    # 改行コード置換
    def replaceNewLine(self, targetStr, nl):
        strend = targetStr[-2:]
        if nl == 'CRLF':
            if strend == '\r\n':
                pass
            elif match('[^\r]\n', strend):
                targetStr = targetStr.replace('\n', '\r\n')
            elif match('.\r', strend):
                targetStr = targetStr.replace('\r', '\r\n')
        elif nl == 'LF':
            if strend == "\r\n":
                targetStr = targetStr.replace('\r\n', '\n')
            elif match('[^\r]\n', strend):
                pass
            elif match('.\r', strend):
                targetStr = targetStr.replace('\r', '\n')
        elif nl == 'CR':
            if strend == "\r\n":
                targetStr = targetStr.replace('\r\n', '\r')
            elif match('[^\r]\n', strend):
                targetStr = targetStr.replace('\n', '\r')
            elif match('.\r', strend):
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
            elif match('[^\r]\n', strend):
                targetStr = targetStr.replace('\n', '\r\n')
            elif match('.\r', strend):
                targetStr = targetStr.replace('\r', '\r\n')
            else:
                targetStr = ''.join([targetStr, '\r\n'])
        elif nl == 'LF':
            if strend == "\r\n":
                targetStr = targetStr.replace('\r\n', '\n')
            elif match('[^\r]\n', strend):
                pass
            elif match('.\r', strend):
                targetStr = targetStr.replace('\r', '\n')
            else:
                targetStr = ''.join([targetStr, '\n'])
        elif nl == 'CR':
            if strend == "\r\n":
                targetStr = targetStr.replace('\r\n', '\r')
            elif match('[^\r]\n', strend):
                targetStr = targetStr.replace('\n', '\r')
            elif match('.\r', strend):
                pass
            else:
                targetStr = ''.join([targetStr, '\r'])
        else:
            pass

        return targetStr

    # 改行コード取得
    def getNewLine(self, targetStr):

        nlCode = ''

        strend = targetStr[-2:]
        if strend == '\r\n':
            nlCode = 'CRLF'
        elif match('[^\r]\n', strend):
            nlCode = 'LF'
        elif match('.\r', strend):
            nlCode = 'CR'
        else:
            pass

        return nlCode

    # 改行コード除去
    def deleteNewLine(self, targetStr):

        strend = targetStr[-2:]
        if strend == '\r\n':
            targetStr = targetStr.replace('\r\n', '')
        elif match('[^\r]\n', strend):
            targetStr = targetStr.replace('\n', '')
        elif match('.\r', strend):
            targetStr = targetStr.replace('\r', '')
        else:
            pass

        return targetStr

    # 文字列両端クォート除去
    def delQuoteStartEnd(self, targetStr):
        targetStr = sub('(^["\']|["\']$)', '', targetStr)
        return targetStr

    # 相対パスは絶対パスに変換
    # 絶対パスはそのまま
    def chgRel2AbsPath(self, targetpath, basefilepath, addRel):
        if match('^(\.\./|\./)', targetpath):
            targetpath = ''.join([os.path.dirname(basefilepath), addRel, targetpath])
            targetpath = self.cutDDot(targetpath)
        else:
            pass
        return targetpath

    # パス内の[foo/../]を再帰的に除去
    def cutDDot(self, targetpath):
        if search(r'[^/\\]+[/\\]\.\.[\\/]', targetpath):
            targetpath = self.cutDDot(sub(r'[^/\\]+[/\\]\.\.[\\/]', '', targetpath))
        return targetpath

    # エンコード不可文字を●で塗りつぶしつつファイル書き込み
    def replaceEncErrorWrite(self, loggername, filePath, i, tf, lineReplaced, inenc, outenc):

        logger = getLogger(''.join([loggername, '.', sub('\.[^/\\\.]*', '', os.path.basename(__file__))]))

        try:
            tf.write(lineReplaced.encode(outenc))
        except UnicodeEncodeError as e:
            # 文字エンコードエラーの場合はエラー出力して処理を続ける。
            # logger.exception(e)
            logger.log(30, ''.join(['line ', str(i), ' : encode error', ' <file path> ', filePath]))
            # logger.log(30, 'Output by character encoding of the input file.')
            logger.log(30, 'Replace [●]')

            # ファイルには入力ファイルのエンコードで出力しておく。　　・・・のはやめて・・・
            # tf.write(lineReplaced.encode(inenc))

            # エラー文字列からデコード不可文字を取得して置換。エラー文言の仕様が変更される可能性を考えると微妙な処理だが・・・
            colList = search(r"'\\u[^']+'", str(e)).group().split(r'\u')
            for col in colList:
                col = self.delQuoteStartEnd(col)
                if col != '':
                    lineReplaced = sub(chr(int(col, 16)), '●', lineReplaced)
                    self.replaceEncErrorWrite(loggername, filePath, i, tf, lineReplaced, inenc, outenc)

        return lineReplaced

    # configが格納されているパス一覧に指定パスの親パスに当たるものが含まれている場合はそのパスを返す。
    # 逆順でサーチ
    def getPathStartsWithInListRev(self, path, confPathsList):
        for parentConfPath in confPathsList[::-1]:
            if path.startswith(parentConfPath):
                return parentConfPath

        return ''
