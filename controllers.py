from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from model import read_task, read_user, insert_user, read_task2
import db
import re
from mycalendar import MyCalendar
from datetime import datetime, timedelta
from auth import auth
from starlette.responses import RedirectResponse


pattern = re.compile(r"\w{4,20}")  # 任意の4~20の英数字を示す正規表現
pattern_pw = re.compile(r"\w{6,20}")  # 任意の6~20の英数字を示す正規表現
pattern_mail = re.compile(
    r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
)  # e-mailの正規表現

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

    username = auth(credentials)

    # ユーザとタスクを取得
    conn = db.get_connection()
    cur = conn.cursor()
    user = read_user(cur, username)
    task = read_task(cur, user[0])
    cur.close()
    conn.close()

    today = datetime.now()
    next_w = today + timedelta(days=7)  # １週間後の日付

    # カレンダーをHTML形式で取得
    cal = MyCalendar(
        username, {t[3].strftime("%Y%m%d"): t[5] for t in task}
    )  # 予定がある日付をキーとして渡す

    cal = cal.formatyear(today.year, 4)  # カレンダーをHTMLで取得

    # 直近のタスクだけでいいので、リストを書き換える
    task = [t for t in task if today <= t[3] <= next_w]
    links = [t[3].strftime("/todo/" + username + "/%Y/%m/%d") for t in task]  # 直近の予定リンク

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "user": user,
            "task": task,
            "links": links,
            "calender": cal,
        },
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

        # ユーザ-を取得
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


def detail(
    request: Request,
    username,
    year,
    month,
    day,
    credentials: HTTPBasicCredentials = Depends(security),
):

    """URLパターンは引数で取得可能"""
    # 認証OK？
    username_tmp = auth(credentials)

    # もし他のユーザが訪問してきたらはじく
    if username_tmp != username:
        return RedirectResponse("/")

    # ユーザとタスクを取得
    conn = db.get_connection()
    cur = conn.cursor()
    user = read_user(cur, username)
    # 該当の日付と一致するものだけのリストにする
    deadline_date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    task = read_task2(cur, user[0], deadline_date)

    cur.close()
    conn.close()

    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "username": username,
            "task": task,
            "year": year,
            "month": month,
            "day": day,
        },
    )
