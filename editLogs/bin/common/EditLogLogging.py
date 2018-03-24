import os
import re
import logging
import configparser
import common.EditLogBase

class EditLogLogging:

    def __init__(self, loggerName):
        self.thisLogger = self.setLogger(loggerName)

    # logger初期設定処理
    # return: logger : logging.getLogger()
    def setLogger(self, logger_name):
    
        comE = common.EditLogBase.EditLogBase('')
        
        thisFileFullPath = os.path.abspath(__file__)
        
        CONF = comE.chgRel2AbsPath(''.join(['../conf/',re.sub(r'\..*','',os.path.basename(__file__)),'.conf']),thisFileFullPath,'/../')
        CONF_ENC = 'utf-8'
        # configファイルのsection名
        LOG_CAT = 'logging'
        # 設定ファイル読み込み
        confParser = configparser.RawConfigParser()
        confParser.read(CONF,CONF_ENC)
        
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
        

