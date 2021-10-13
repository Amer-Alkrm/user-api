import logging
from os import getenv

logging.basicConfig(filename='logger.log', level=getenv('LOG_LEVEL'),
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', filemode='w')
logger = logging.getLogger()
