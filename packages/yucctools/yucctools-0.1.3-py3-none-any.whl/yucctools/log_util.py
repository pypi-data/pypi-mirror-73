"""
记录日志
"""

import os
import logging
import datetime


def logger(filepath=None, filehandler=True, streamhandler=True):
    """
    生成logger实例
    :return: logger实例
    """
    # 生成日志路径
    # 1. 如果为文件夹，则返回文件夹下的路径名称
    # 2. 如果为文件，则直接使用
    # 3. 如果为空、非文件、非文件夹、文件夹或文件不存在等其他情况，则指定当前路径下写入日志
    # 一并返回绝对路径
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d.%H-%M-%S')}.log"
    if filepath and os.path.isdir(filepath):
        filepath = os.path.join(filepath, filename)
    elif (not filepath) or (not os.path.isfile(filepath)):
        filepath = filename
    filepath = os.path.abspath(filepath)
    # create logger with a name
    logger = logging.getLogger()
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
                '%(asctime)s %(filename)s:%(lineno)5s %(funcName)20s() %(levelname)-8s %(message)s',
                datefmt="%m/%d/%Y %H:%M:%S")
        # 是否写入文件
        if filehandler:
            # create file handler which logs even debug messages
            fh = logging.FileHandler(filepath, encoding='utf-8')
            fh.setLevel(10)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        # 是否写入控制台
        if streamhandler:
            ch = logging.StreamHandler()
            ch.setLevel(10)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

    # 第一条日志，记录日志文件所在位置
    logger.info(f'filepath: {filepath}')
    return logger
