import logging

LOG_LOCATION = '/var/log/monzo/'
LOG_NAME = 'monzo.log'


def get_logger(level='INFO'):
    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(level)

    file_handler = logging.FileHandler('../logs/%s' % LOG_NAME, 'w', 'utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d in %(funcName)s]')  # NOQA
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    return logger
