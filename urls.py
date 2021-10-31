from controllers import *


# FastAPIのルーティング用関数
app.add_api_route("/", index)

# 管理者用
app.add_api_route("/admin", admin)

# ユーザー登録用
app.add_api_route('/register', register, methods=['GET', 'POST'])

# 予定の詳細ページ用
app.add_api_route('/todo/{username}/{year}/{month}/{day}', detail)