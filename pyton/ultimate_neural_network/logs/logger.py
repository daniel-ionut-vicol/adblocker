import logging

# Create a logger
logger = logging.getLogger('mylogger')

# Set logging level
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('mylog.log')

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)