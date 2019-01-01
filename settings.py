from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
def getBool(text):
    return True if text == 'True' else False

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWD = os.getenv('DB_PASSWD')
DB_NAME = os.getenv('DB_NAME')
DB_DEBUG = getBool(os.getenv('DB_DEBUG'))