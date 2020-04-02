import os
import sys
import click

from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy 

# 得到当前平台

WIN = sys.platform.startswith('win')
if WIN:
    # 请求头
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

# 配置要在实例化之前
app.config['SQLALCHEMY_DATABASE_URI'] = prefix+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #关闭对模型修改的监控

# 传入app实例 在配置之后
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
class Movie(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route("/")
# @app.route("/index")
# @app.route("/home")
def index():
    # name = "haominmin"
    # movies = [
    #     {"title":"大赢家","year":"2020"},
    #     {"title":"囧妈","year":"2000"},
    #     {"title":"战狼","year":"2018"},
    #     {"title":"心花怒放","year":"2017"},
    #     {"title":"速度与激情","year":"2019"},
    #     {"title":"我的父亲母亲","year":"2010"},
    # ]
    user = User.query.first()  #读取用户记录
    movie = Movie.query.all()  #读取所有的电影记录 

    return render_template("index.html",user=user,movies=movie)

#     #动态url 
# @app.route('/index/<name>')
# def home(name):
#     print(url_for("home",name="haominmin"))
#     return "<h1>hello,%s</h1>"%name


# 自定义命令 
@app.cli.command() #装饰器注册命令
@click.option('--drop',is_flag=True,help='删除之后再创建')
def initdb(drop):
    if drop:
  
        db.drop_all()

    db.create_all()

    click.echo("初始化数据库完成")

# 自定义命令 装饰器
@app.cli.command()
def forge():
    # 初始化数据库
    db.create_all()
    name = "haominmin"
    movies = [
        {"title":"大赢家","year":"2020"},
        {"title":"囧妈","year":"2000"},
        {"title":"战狼","year":"2018"},
        {"title":"心花怒放","year":"2017"},
        {"title":"速度与激情","year":"2019"},
        {"title":"我的父亲母亲","year":"2010"},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo("导入数据完成")
