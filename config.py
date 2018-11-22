import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    TESTING = False
    MAX_LOG_SIZE = 5120
    MAX_LOGS = 5