#!/usr/bin/env python3
#
# 追加パッケージ: configparser
#
# 置換文字列リストファイルに従って一括置換します。
#
import os
import re
import sys
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

    # 引数チェック
    if len(sys.argv) != 2:
        print('Usage: > replaceOnDict.exe [Config File Path]')
        sys.exit()

    # 設定ファイル読み込み
    confParser = configparser.RawConfigParser()
    confParser.read(sys.argv[1] , encoding=CONF_ENC)

    # 起動時のカレントワークディレクトリを保存しておく。
    orgCwd = os.getcwd()

    # 共通クラスインスタンス取得
    comE = common.EditLogBase.EditLogBase()
    comRORD = common.ComRepOnDict.ComRepOnDict()

    # ワークディレクトリ移動
    os.chdir(comE.delQuoteStartEnd(confParser.get('baseset', 'WORK_DIR')))

    # ログ出力設定初期化
    common.EditLogLogging.EditLogLogging(LOGGER_NAME, confParser)

    # pyinstallerでexe化した時を想定して__file__ではなくsys.argv[0]を使用する
    thisFileFullPath = os.path.abspath(sys.argv[0])

    # 当処理内で使用するLoggerオブジェクト取得
    logger = logging.getLogger(''.join([LOGGER_NAME, '.', re.sub('\.[^/\\\.]*', '', os.path.basename(__file__))]))

    # 起動共通
    comE.start(logger)

    try:
        # 出力先ディレクトリ作成
        comE.makeDir(comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR')))
    except Exception as e:
        logger.exception(e)
        comE.end(logger)

    # 置換文字列リストファイルをOrderedDictに格納
    # 文字コードはutf-8固定
    try:
        replaceListDict = comE.updateDictFromTsv(comE.delQuoteStartEnd(confParser.get('baseset', 'REPLACE_LIST_FILE')), 'utf-8')
    except Exception as e:
        # 置換リストファイル読み込み処理で何かしらエラーが発生した際はログ出力して終了。主に文字コード周りでのエラーを想定。
        # inputファイルの構成が保障されないので、あらゆるエラーを捕まえてログ出力してから終了させる。
        logger.exception(e)
        comE.end(logger)

    # 出力先ディレクトリに指定ディレクトリからのディレクトリ構成を再現する
    # 検索ディレクトリのファイルを出力ディレクトリにコピー
    comE.copyTreeAll(comE.delQuoteStartEnd(confParser.get('baseset', 'SEARCH_DIR')), comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR')))

    # CSV変換向けパラメータデフォルト値
    tmp_input_encode = comE.delQuoteStartEnd(confParser.get('formatparams', 'INPUT_ENCODE'))
    tmp_output_encode = comE.delQuoteStartEnd(confParser.get('formatparams', 'OUTPUT_ENCODE'))
    tmp_new_line = comE.delQuoteStartEnd(confParser.get('formatparams', 'NEW_LINE'))

    for root, dirs, files in os.walk(comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR'))):
        logger.log(20, '処理中ディレクトリ: ')
        logger.log(20, root.replace('\\', '/'))

        for file in files:
            try:
                comRORD.replaceOnRegexDict(LOGGER_NAME,
                                   os.path.join(root, file).replace(os.path.sep, '/'),
                                   replaceListDict,
                                   tmp_input_encode,
                                   tmp_output_encode,
                                   tmp_new_line)
            except Exception as e:
                # 何かしらエラーが発生した際はログ出力して終了
                logger.exception(e)
                comE.end(logger)


    # 終了共通
    comE.end(logger)
