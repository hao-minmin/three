
from flask import render_template
from blog import app
# 错误处理 404
@app.errorhandler(404)
def page_not_found(e):
    # user = User.query.first()
    # return render_template("404.html",user=user),404
    # 返回模板和状态码
    return render_template("errors/404.html"),404
