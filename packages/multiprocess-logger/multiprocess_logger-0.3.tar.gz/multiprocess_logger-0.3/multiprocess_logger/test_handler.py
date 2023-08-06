import logging

from multiprocessing import Process
from logging import Formatter

from multiprocess_logger import MultiprocessingHandler


handler = MultiprocessingHandler(filename='./ppp.log',
                                 maxBytes=1024 * 1024, backupCount=10)
fmt = Formatter(fmt='%(asctime)s - %(process)d - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
handler.setFormatter(fmt=fmt)
logger = logging.getLogger('SHIT')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(process)d - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def write_log():
    while True:
        logger.info('Hello World!------------Hello World!')


if __name__ == '__main__':
    # write_log()
    p_list = []
    for i in range(6):
        p_list.append(Process(target=write_log))

    for i in p_list:
        i.start()
