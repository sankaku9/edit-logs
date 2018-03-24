#!/usr/bin/env python3
#
# 追加パッケージ: configparser
#
# 置換文字列リストファイルに従って一括置換します。
#
import os
import re
import logging
import configparser
import common.EditLogBase
import common.ComRepOnDict

if __name__ == '__main__':

    ########
    # 固定値
    ########
    CONF_ENC = 'utf-8'
    # 当処理で共通的に使用するLogger名
    LOGGER_NAME = 'rec_search_log'

    # 共通クラスインスタンス取得
    # 共通クラス内で使用するLoggerNameを指定する。
    comE = common.EditLogBase.EditLogBase(LOGGER_NAME)
    comRORD = common.ComRepOnDict.ComRepOnDict()

    thisFileFullPath = os.path.abspath(__file__)

    # 設定値取得用
    CONF = comE.chgRel2AbsPath(''.join(['../conf/',re.sub(r'\..*','',os.path.basename(__file__)),'.conf']),thisFileFullPath,'/')

    # 当処理内で使用するLoggerオブジェクト取得
    # ※LOGGER_NAMEのLogger設定は共通クラスCommonRootインスタンスinit内で実施済み。
    logger = logging.getLogger(''.join([LOGGER_NAME, '.', re.sub('\.[^/\\\.]*', '', os.path.basename(__file__))]))

    # 起動共通
    comE.start()

    # 設定ファイル読み込み
    confParser = configparser.SafeConfigParser()
    confParser.read(CONF, encoding=CONF_ENC)

    # config格納ディレクトリリスト
    confPaths = []

    try:
        # 出力先ディレクトリ作成
        comE.makeDir(comE.chgRel2AbsPath(comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR')), thisFileFullPath,'/'))
    except Exception as e:
        logger.exception(e)
        comE.end()

    # 置換文字列リストファイルをOrderedDictに格納
    # 文字コードはutf-8固定
    try:
        replaceListDict = comE.updateDictFromTsv(comE.chgRel2AbsPath(comE.delQuoteStartEnd(confParser.get('baseset', 'REPLACE_LIST_FILE')), thisFileFullPath,'/'), 'utf-8')
    except Exception as e:
        #　置換リストファイル読み込み処理で何かしらエラーが発生した際はログ出力して終了。主に文字コード周りでのエラーを想定。
        #　inputファイルの構成が保障されないので、あらゆるエラーを捕まえてログ出力してから終了させる。
        logger.exception(e)
        comE.end()

    # 出力先ディレクトリに指定ディレクトリからのディレクトリ構成を再現する
    # 検索ディレクトリのファイルを出力ディレクトリにコピー
    comE.copyTreeAll(comE.delQuoteStartEnd(confParser.get('baseset', 'SEARCH_DIR')), comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR')))

    for root, dirs, files in os.walk(comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR'))):
        logger.log(20, '処理中ディレクトリ: ')
        logger.log(20, root.replace('\\', '/'))

        # ディレクトリツリーの親configが格納されたパス
        parentTreeConfig = comE.getPathStartsWithInListRev(root, confPaths)

        tmpConfPath = ''
        # CSV変換向けパラメータconfigファイルが個別に配備されているディレクトリはそのconfigを読み込む
        if os.path.isfile(''.join([root, '/', comE.delQuoteStartEnd(confParser.get('baseset', 'CONFIG_NAME'))])):
            onDirConfParser = configparser.SafeConfigParser()
            tmpConfPath = ''.join([root, '/', comE.delQuoteStartEnd(confParser.get('baseset', 'CONFIG_NAME'))])
            onDirConfParser.read(tmpConfPath, encoding=CONF_ENC)

            tmp_input_encode = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'INPUT_ENCODE'))
            tmp_output_encode = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'OUTPUT_ENCODE'))
            tmp_new_line = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'NEW_LINE'))

            # configを読み込んだ時点のrootパスを格納
            confPaths.append(root)

        # パスの親子関係を判定して、子であれば親のconfigを引き継ぐ
        elif parentTreeConfig != '':
            onDirConfParser = configparser.SafeConfigParser()
            tmpConfPath = ''.join([parentTreeConfig, '/', comE.delQuoteStartEnd(confParser.get('baseset', 'CONFIG_NAME'))])
            onDirConfParser.read(tmpConfPath, encoding=CONF_ENC)

            tmp_input_encode = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'INPUT_ENCODE'))
            tmp_output_encode = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'OUTPUT_ENCODE'))
            tmp_new_line = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'NEW_LINE'))

        # それ以外はデフォルト値を読み込み
        else:
            # CSV変換向けパラメータデフォルト値
            tmpConfPath = 'デフォルト設定を使用します。'
            tmp_input_encode = comE.delQuoteStartEnd(confParser.get('formatparams', 'INPUT_ENCODE'))
            tmp_output_encode = comE.delQuoteStartEnd(confParser.get('formatparams', 'OUTPUT_ENCODE'))
            tmp_new_line = comE.delQuoteStartEnd(confParser.get('formatparams', 'NEW_LINE'))

        logger.log(20, 'configファイル: ')
        logger.log(20, tmpConfPath.replace('\\', '/'))


        for file in files:
            # 設定ファイルは変換対象としない。
            if file != comE.delQuoteStartEnd(confParser.get('baseset', 'CONFIG_NAME')):
                try:
                    comRORD.replaceOnRegexDict(LOGGER_NAME,
                                       os.path.join(root, file).replace(os.path.sep, '/'),
                                       replaceListDict,
                                       tmp_input_encode,
                                       tmp_output_encode,
                                       tmp_new_line)
                except Exception as e:
                    #何かしらエラーが発生した際はログ出力して終了
                    logger.exception(e)
                    comE.end()


    # 終了共通
    comE.end()
