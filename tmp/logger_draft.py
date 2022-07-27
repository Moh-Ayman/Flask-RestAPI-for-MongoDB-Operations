import logging
########### appLog Logging ######################

appLog_logger = logging.getLogger("appLog")
appLog_logger.setLevel(logging.DEBUG)

if (appLog_logger.hasHandlers()):
    appLog_logger.handlers.clear()

appLog_file_handler = logging.FileHandler('./appLog.log')
appLog_logger.addHandler(appLog_file_handler)

appLog_formatter = logging.Formatter('%(asctime)s - %(levelname)s  - %(message)s')
appLog_file_handler.setFormatter(appLog_formatter)











appLog_logger.error("TEstI")
