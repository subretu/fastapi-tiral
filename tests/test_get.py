from starlette.testclient import TestClient
from fastapi.security import HTTPBasic
from main.main import app
from requests.auth import HTTPBasicAuth


security = HTTPBasic()


def test_get(cursor, cursor2):
    auth = HTTPBasicAuth(username="dddd", password="dddd")
    response = cursor.get("/get", auth=auth)

    print("以下、デバッグ")
    print(response.json())

    # データ取得
    select_query = "select * from public.task where user_id = '1';"
    cursor2.execute(select_query)
    rows = cursor2.fetchall()

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
