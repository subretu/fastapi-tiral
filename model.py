def read_user(cur, user):
    cur.execute(f"select * from public.user where username= '{user}';")
    rows = cur.fetchall()
    return rows


def read_task(cur, user_id):
    cur.execute(f"select * from public.task where user_id = '{user_id[0]}';")
    rows = cur.fetchall()
    return rows


def read_task2(cur, user_id, deadline_date):
    cur.execute(
        f"select * from public.task where user_id = '{user_id[0]}' and deadline::date = '{deadline_date}';"
    )
    rows = cur.fetchall()
    return rows


def insert_user(conn, cur, user_data):
    cur.execute(
        f"insert into public.user (username, password, mal) values ('{user_data[0]}', '{user_data[1]}', '{user_data[2]}');"
    )
    conn.commit()


def update_tsak(conn, cur, task_id):
    # 先にSQL文を作ってexecuteの方がクエリ実行が1回なのでいいかもしれない
    for id in task_id:
        cur.execute(f"update public.task set done = True where id = {id};")
    conn.commit()


def add_tsak(conn, cur, user_id, content, deadline, now_time):
    cur.execute(
        f"insert into public.task (user_id, content, deadline, date, done) values ('{user_id[0]}', '{content}', '{deadline}','{now_time}', false);"
    )
    conn.commit()
