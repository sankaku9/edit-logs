import os
import logging
import common.EditLogBase

class EditLogLogging:

    def __init__(self, loggerName, confParser):
        self.thisLogger = self.setLogger(loggerName, confParser)

    # logger初期設定処理
    # return: logger : logging.getLogger()
    def setLogger(self, logger_name, confParser):

        comE = common.EditLogBase.EditLogBase()

        thisFileFullPath = os.path.abspath(__file__)

        # configファイルのsection名
        LOG_CAT = 'logging'

        logFilePath = comE.chgRel2AbsPath(confParser.get(LOG_CAT, 'PATH'), thisFileFullPath, '/../')

        logger = logging.getLogger(logger_name)
        # ログレベル設定
        logger.setLevel(10)
        # ファイル出力設定
        logFh = logging.FileHandler(logFilePath, encoding=confParser.get(LOG_CAT, 'ENCODING'))
        logger.addHandler(logFh)
        # コンソール出力設定
        logSh = logging.StreamHandler()
        logger.addHandler(logSh)
        # 出力形式設定
        logFormatForStream = logging.Formatter(fmt=confParser.get(LOG_CAT, 'FORMAT_CONSOLE'), datefmt=confParser.get(LOG_CAT, 'DATE_FMT'))
        logFormatForFile = logging.Formatter(fmt=confParser.get(LOG_CAT, 'FORMAT_FILE'), datefmt=confParser.get(LOG_CAT, 'DATE_FMT'))
        logSh.setFormatter(logFormatForStream)
        logFh.setFormatter(logFormatForFile)


