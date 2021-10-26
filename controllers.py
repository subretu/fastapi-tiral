from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from model import read_task, read_user
import db

app = FastAPI(
    version="0.9 beta",
)

security = HTTPBasic()

# テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="templates")
# Jinja2.Environment : filterやglobalの設定用
jinja_env = templates.env


def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def admin(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # Basic認証で受け取った情報
    username = credentials.username
    password = credentials.password

    # ユーザとタスクを取得
    cur = db.get_connection()
    user = read_user(cur, username)
    task = read_task(cur, user[0])
    cur.close()

    # 該当ユーザがいない場合
    if user == [] or user[0][2] != password:
        error = 'ユーザ名かパスワードが間違っています'
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Basic"},
        )

    return templates.TemplateResponse(
        "admin.html", {"request": request, "user": user, "task": task}
    )
