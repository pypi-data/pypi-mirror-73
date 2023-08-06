"""
记录日志
"""

import os
import logging


def logger(filepath=None):
    """
    生成logger实例
    :return: logger实例
    """
    if (not filepath) or (not os.path.isfile(filepath)):
        filepath = 'log_by_yucctools.log'
    # create logger with a name
    logger = logging.getLogger()
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
                '%(asctime)s %(filename)s:%(lineno)5s %(funcName)20s() %(levelname)-8s %(message)s')
        # create file handler which logs even debug messages
        fh = logging.FileHandler(filepath, encoding='utf-8')
        fh.setLevel(10)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(10)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
