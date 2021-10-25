from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from model import read_task, read_user_admin
import db

app = FastAPI(
    version="0.9 beta",
)


# テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="templates")
# Jinja2.Environment : filterやglobalの設定用
jinja_env = templates.env


def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def admin(request: Request):
    # ユーザとタスクを取得
    # とりあえず今はadminユーザのみ取得
    cur = db.get_connection()
    user = read_user_admin(cur)
    task = read_task(cur)
    cur.close()

    return templates.TemplateResponse(
        "admin.html", {"request": request, "user": user, "task": task}
    )
