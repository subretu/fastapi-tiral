from starlette.testclient import TestClient
from fastapi.security import HTTPBasic
from main.main import app
from requests.auth import HTTPBasicAuth


security = HTTPBasic()

client = TestClient(app)


def test_insert():
    auth = HTTPBasicAuth(username="xxxxxx", password="yyyyyy")
    response = client.post(
        "/add_task",
        auth=auth,
        data={
            "content": "テスト",
            "deadline": "2021-11-19 19:20:13",
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 27,
            "content": 'テスト',
            "deadline": '2021-11-19 19:20:13',
            "date": '2021-11-19 19:20:13',
            "done": False,
        }
    ]
