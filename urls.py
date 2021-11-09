from controllers import *


# FastAPIのルーティング用関数
app.add_api_route("/", index)

# 管理者用
# POSTリダイレクト対策
app.add_api_route("/admin", admin, methods=['GET', 'POST'])

# ユーザー登録用
app.add_api_route('/register', register, methods=['GET', 'POST'])

# 予定の詳細ページ用
app.add_api_route('/todo/{username}/{year}/{month}/{day}', detail)

# 予定完了機能
app.add_api_route('/done', done, methods=['POST'])

# 予定追加機能
app.add_api_route('/add', add, methods=['POST'])

# 予定を削除
app.add_api_route('/delete/{t_id}', delete)

# JSONで返すAPI
app.add_api_route('/get', get)

# タスクを追加するAPI
app.add_api_route('/add_task', insert, methods=['POST'])
