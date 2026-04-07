import logging
import sys
from datetime import datetime

#configuration du logger
def setup_logging():
    logger=logging.getLogger("fastapi-api")
    logger.setLevel(logging.INFO)

    #Format des loggs
    formatter=logging.Formatter(
        '%(asctime)s-%(name)s-%(levelname)s-%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    #Handler pour la console
    console_handler=logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    #Handler pour fichier
    # file_handler=logging.FileHandler(f"api_{datetime.now().strftime('%Y%m%d')}.log")
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    return logger

#Logger globale
logger=setup_logging()