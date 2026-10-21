import pymysql
import pytest
import os
from config.config import *


@pytest.fixture(scope="session", autouse=True)
def destroy_data():

    yield

    sqls = [SQL1, SQL2]

    conn = pymysql.Connect(
        # host=DB_HOST,
        # port=DB_PORT,
        # database=DB_NAME,
        # user=DB_USER,
        # password=DB_PASSWORD,
        **eval(os.environ["DB"]),
        charset="utf8",
        autocommit=True
    )
    cur = conn.cursor()

    for sql in sqls:
        cur.execute(sql)

    cur.close()
    conn.close()
