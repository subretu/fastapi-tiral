import pytest
import psycopg2
import os
from main.main import app
from main.db import get_connection
from starlette.testclient import TestClient


# DB接続用関数
def get_test_connection():

    user = os.getenv("POSTGRES_USER", None)
    pwd = os.getenv("POSTGRES_PASS", None)
    server = os.getenv("POSTGRES_HOST", None)
    port = os.getenv("POSTGRES_HOST", None)
    db = os.getenv("POSTGRES_PORT", None)

    con = psycopg2.connect(
        "host="
        + server
        + " port="
        + port
        + " dbname="
        + db
        + " user="
        + user
        + " password="
        + pwd
    )

    return con

@pytest.fixture
def cursor():
    app.dependency_overrides[get_connection] = get_test_connection

    client = TestClient(app)

    yield client


@pytest.fixture
def cursor2():

    conn = get_test_connection()
    cur = conn.cursor()

    yield cur
