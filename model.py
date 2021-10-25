def read_task(con):
    cur = con.cursor()
    cur.execute('select * from public.task;')
    rows = cur.fetchall()
    cur.close()
    return rows


def read_user_admin(con):
    cur = con.cursor()
    cur.execute("select * from public.user where username= 'admin';")
    rows = cur.fetchall()
    cur.close()
    return rows
