def read_user(con, user):
    cur = con.cursor()
    cur.execute(f"select * from public.user where username= '{user}';")
    rows = cur.fetchall()
    cur.close()
    return rows


def read_task(con, user_id):
    cur = con.cursor()
    cur.execute(f"select * from public.task where user_id = '{user_id[0]}';")
    rows = cur.fetchall()
    cur.close()
    return rows
