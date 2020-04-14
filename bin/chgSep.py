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
import common.ComChgSep

if __name__ == '__main__':

    ########
    # 固定値
    ########
    CONF_ENC = 'utf-8'
    # 当処理で共通的に使用するLogger名
    LOGGER_NAME = 'chg_sep_log'

    # 引数チェック
    if len(sys.argv) != 2:
        print('Usage: > chgSep.exe [Config File Path]')
        sys.exit()

    # 設定ファイル読み込み
    confParser = configparser.RawConfigParser()
    confParser.read(sys.argv[1] , encoding=CONF_ENC)

    common.EditLogLogging.EditLogLogging(LOGGER_NAME, confParser)


    # 共通クラスインスタンス取得
    # 共通クラス内で使用するLoggerNameを指定する。
    comE = common.EditLogBase.EditLogBase()
    comCS = common.ComChgSep.ComChgSep()

    # pyinstallerでexe化した時を想定して__file__ではなくsys.argv[0]を使用する
    thisFileFullPath = os.path.abspath(sys.argv[0])

    # 当処理内で使用するLoggerオブジェクト取得
    # ※LOGGER_NAMEのLogger設定は共通クラスCommonRootインスタンスinit内で実施済み。
    logger = logging.getLogger(''.join([LOGGER_NAME, '.', re.sub('\.[^/\\\.]*', '', os.path.basename(__file__))]))
    # 起動共通
    comE.start(logger)

    # config格納ディレクトリリスト
    confPaths = []

    try:
        # 出力先ディレクトリ作成
        comE.makeDir(comE.chgRel2AbsPath(comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR')), thisFileFullPath,'/'))
    except Exception as e:
        logger.exception(e)
        comE.end(logger)

    # 出力先ディレクトリに指定ディレクトリからのディレクトリ構成を再現する
    # ソースディレクトリのファイルを出力ディレクトリにコピー
    comE.copyTreeAll(comE.delQuoteStartEnd(confParser.get('baseset', 'SOURCE_DIR')), comE.delQuoteStartEnd(confParser.get('baseset', 'WRITE_DIR')))

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
            tmp_input_sep = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'INPUT_SEP'))
            tmp_output_sep = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'OUTPUT_SEP'))
            tmp_new_line = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'NEW_LINE'))
            tmp_quote = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'QUOTE'))
            tmp_input_sep_space_col_chg_limit = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'INPUT_SEP_SPACE_COL_CHG_LIMIT'))
            tmp_date_line_regex = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'DATE_LINE_REGEX'))
            tmp_input_date_format = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'INPUT_DATE_FORMAT'))
            tmp_output_date_format = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'OUTPUT_DATE_FORMAT'))
            tmp_extract_on_regex = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'EXTRACT_ON_REGEX'))

            # configを読み込んだ時点のrootパスを格納
            confPaths.append(root)

        # パスの親子関係を判定して、子であれば親のconfigを引き継ぐ
        elif parentTreeConfig != '':
            onDirConfParser = configparser.SafeConfigParser()
            tmpConfPath = ''.join([parentTreeConfig, '/', comE.delQuoteStartEnd(confParser.get('baseset', 'CONFIG_NAME'))])
            onDirConfParser.read(tmpConfPath, encoding=CONF_ENC)

            tmp_input_encode = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'INPUT_ENCODE'))
            tmp_output_encode = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'OUTPUT_ENCODE'))
            tmp_input_sep = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'INPUT_SEP'))
            tmp_output_sep = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'OUTPUT_SEP'))
            tmp_new_line = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'NEW_LINE'))
            tmp_quote = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'QUOTE'))
            tmp_input_sep_space_col_chg_limit = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'INPUT_SEP_SPACE_COL_CHG_LIMIT'))
            tmp_date_line_regex = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'DATE_LINE_REGEX'))
            tmp_input_date_format = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'INPUT_DATE_FORMAT'))
            tmp_output_date_format = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'OUTPUT_DATE_FORMAT'))
            tmp_extract_on_regex = comE.delQuoteStartEnd(onDirConfParser.get('formatparams', 'EXTRACT_ON_REGEX'))

        # それ以外はデフォルト値を読み込み
        else:
            # CSV変換向けパラメータデフォルト値
            tmpConfPath = 'デフォルト設定を使用します。'
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

        logger.log(20, 'configファイル: ')
        logger.log(20, tmpConfPath.replace('\\', '/'))

        for file in files:
            # 設定ファイルは変換対象としない。
            if file != comE.delQuoteStartEnd(confParser.get('baseset', 'CONFIG_NAME')):
                try:
                    # 区切り文字変更
                    comCS.chgSep(LOGGER_NAME,
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
                    #何かしらエラーが発生した際はログ出力して終了
                    logger.exception(e)
                    comE.end(logger)

    # 終了共通
    comE.end(logger)
