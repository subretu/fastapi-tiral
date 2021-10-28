from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from model import read_task, read_user, insert_user
import db
import re  # new

pattern = re.compile(r'\w{4,20}')  # 任意の4~20の英数字を示す正規表現
pattern_pw = re.compile(r'\w{6,20}')  # 任意の6~20の英数字を示す正規表現
pattern_mail = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')  # e-mailの正規表現

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
        error = "ユーザ名かパスワードが間違っています"
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Basic"},
        )

    return templates.TemplateResponse(
        "admin.html", {"request": request, "user": user, "task": task}
    )


async def register(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse(
            "register.html", {"request": request, "username": "", "error": []}
        )

    if request.method == "POST":
        # POSTデータ
        data = await request.form()
        username = data.get("username")
        password = data.get("password")
        password_tmp = data.get("password_tmp")
        mail = data.get("mail")

        user_data = (username, password, mail)

        error = []

        conn = db.get_connection()
        cur = conn.cursor()

        # ユーザとタスクを取得
        user = read_user(cur, username)

        # 怒涛のエラー処理
        if user != []:
            error.append("同じユーザ名のユーザが存在します。")
        if password != password_tmp:
            error.append("入力したパスワードが一致しません。")
        if pattern.match(username) is None:
            error.append("ユーザ名は4~20文字の半角英数字にしてください。")
        if pattern_pw.match(password) is None:
            error.append("パスワードは6~20文字の半角英数字にしてください。")
        if pattern_mail.match(mail) is None:
            error.append("正しくメールアドレスを入力してください。")

        # エラーがあれば登録ページへ戻す
        if error:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "username": username, "error": error},
            )

        # 問題がなければユーザ登録
        insert_user(conn, cur, user_data)
        cur.close()
        conn.close()

        return templates.TemplateResponse(
            "complete.html", {"request": request, "username": username}
        )
