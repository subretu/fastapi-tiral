from starlette.testclient import TestClient
from fastapi.security import HTTPBasic
from main.main import app
from requests.auth import HTTPBasicAuth


security = HTTPBasic()

client = TestClient(app)


def test_get(cursor):
    auth = HTTPBasicAuth(username="xxxxx", password="yyyyy")
    response = client.get("/get", auth=auth)

    print("以下、デバッグ")
    print(response.json())

    # データ取得
    select_query = "select * from public.task_test where user_id = '1';"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": rows[0][0],
            "user_id": rows[0][1],
            "content": rows[0][2],
            "deadline": rows[0][3].strftime("%Y-%m-%d %H:%M:%S"),
            "date": rows[0][4].strftime("%Y-%m-%d %H:%M:%S"),
            "done": rows[0][5],
        }
    ]
