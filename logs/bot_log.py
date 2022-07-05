import sys
import os
sys.path.insert(0, '../')

import logging
import logging.handlers

# создаём формировщик логов (formatter):
formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# path = os.getcwd().split('/')
# path = '/'.join(path[0:(path.index('EGR_bot'))+1])+'/logs/bot.log'

# создаём потоки вывода логов
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(formatter)
steam.setLevel(logging.INFO)
log_file = logging.handlers.TimedRotatingFileHandler('bot.log', encoding='utf8', interval=1, when='D')
log_file.setFormatter(formatter)

# создаём регистратор и настраиваем его
logger = logging.getLogger('botlog')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    logger.critical('Test critical event')
    logger.error('Test error ivent')
    logger.debug('Test debug ivent')
    logger.info('Test info ivent')