import psycopg as pg

from app.config import *


def get_connection():
    return pg.connect(str(DATABASE_URL))
