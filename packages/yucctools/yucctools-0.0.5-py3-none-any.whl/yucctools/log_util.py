"""
记录日志
"""

import logging


def logger(log_file='log.log'):
    """
    生成logger实例
    :return: logger实例
    """
    # create logger with a name
    logger = logging.getLogger()
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        # create file handler which logs even debug messages
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(10)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(10)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
