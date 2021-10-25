from controllers import *


# FastAPIのルーティング用関数
app.add_api_route("/", index)

# 管理者用
app.add_api_route("/admin", admin)
