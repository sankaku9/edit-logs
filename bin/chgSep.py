#!/usr/bin/env python3
#
# 追加パッケージ: configparser
#
# CSV形式等の区切り文字を変換します。
#
import os
import re
import sys
import logging
import configparser
import common.EditLogBase
import common.EditLogLogging
import common.EditLogConstant
import common.ComChgSep

if __name__ == '__main__':

    ########
    # 固定値
    ########
    # 当処理で共通的に使用するLogger名
    LOGGER_NAME = 'chg_sep_log'

    # 引数チェック
    if len(sys.argv) != 2:
        print('Usage: > chgSep.exe [Config File Path]')
        sys.exit()

    # 設定ファイル読み込み
    confParser = configparser.RawConfigParser()
    confParser.read(sys.argv[1] , encoding=common.EditLogConstant.CONF_ENC)

    # 起動時のカレントワークディレクトリを保存しておく。
    orgCwd = os.getcwd()

    # 共通クラスインスタンス取得
    comE = common.EditLogBase.EditLogBase()
    comCS = common.ComChgSep.ComChgSep()

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

    # ソースディレクトリのファイルを出力ディレクトリにコピー
    # 出力先ディレクトリに指定ディレクトリからのディレクトリ構成を再現する
    comE.copyTreeAll(comE.delQuoteStartEnd(confParser.get('baseset', 'SOURCE_DIR')), comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR')))

    # CSV変換向けパラメータ設定
    tmp_input_encode = comE.delQuoteStartEnd(confParser.get('formatparams', 'INPUT_ENCODE'))
    tmp_output_encode = comE.delQuoteStartEnd(confParser.get('formatparams', 'OUTPUT_ENCODE'))
    tmp_input_sep = comE.delQuoteStartEnd(confParser.get('formatparams', 'INPUT_SEP'))
    tmp_output_sep = comE.delQuoteStartEnd(confParser.get('formatparams', 'OUTPUT_SEP'))
    tmp_new_line = comE.delQuoteStartEnd(confParser.get('formatparams', 'NEW_LINE'))
    tmp_quote = comE.delQuoteStartEnd(confParser.get('formatparams', 'QUOTE'))
    tmp_input_sep_space_col_chg_limit = comE.delQuoteStartEnd(confParser.get('formatparams', 'INPUT_SEP_SPACE_COL_CHG_LIMIT'))
    tmp_date_line_regex = comE.delQuoteStartEnd(confParser.get('formatparams', 'DATE_LINE_REGEX'))
    tmp_input_date_format = comE.delQuoteStartEnd(confParser.get('formatparams', 'INPUT_DATE_FORMAT'))
    tmp_output_date_format = comE.delQuoteStartEnd(confParser.get('formatparams', 'OUTPUT_DATE_FORMAT'))
    tmp_extract_on_regex = comE.delQuoteStartEnd(confParser.get('formatparams', 'EXTRACT_ON_REGEX'))

    for root, dirs, files in os.walk(comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR'))):
        logger.log(20, '処理中ディレクトリ: ')
        logger.log(20, root.replace('\\', '/'))
        for file in files:
            try:
                # 区切り文字変更
                comCS.chg_sep(LOGGER_NAME,
                           os.path.join(root, file).replace(os.path.sep, '/'),
                           tmp_input_encode,
                           tmp_output_encode,
                           tmp_input_sep,
                           tmp_output_sep,
                           tmp_new_line,
                           tmp_quote,
                           tmp_input_sep_space_col_chg_limit,
                           tmp_date_line_regex,
                           tmp_input_date_format,
                           tmp_output_date_format,
                           tmp_extract_on_regex)

            except Exception as e:
                # 何かしらエラーが発生した際はログ出力して終了
                logger.exception(e)
                comE.end(logger)

    # 終了共通
    comE.end(logger)
