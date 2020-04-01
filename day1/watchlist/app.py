from flask import Flask,url_for,render_template

app = Flask(__name__)

@app.route("/")
# @app.route("/index")
# @app.route("/home")
def index():
    name = "haominmin"
    movies = [
        {"title":"大赢家","year":"2020"},
        {"title":"囧妈","year":"2000"},
        {"title":"战狼","year":"2018"},
        {"title":"心花怒放","year":"2017"},
        {"title":"速度与激情","year":"2019"},
        {"title":"我的父亲母亲","year":"2010"},
    ]
    return render_template("index.html",name=name,movies=movies)

#     #动态url 
# @app.route('/index/<name>')
# def home(name):
#     print(url_for("home",name="haominmin"))
#     return "<h1>hello,%s</h1>"%name