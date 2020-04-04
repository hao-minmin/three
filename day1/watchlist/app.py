import os
import sys
import click

from flask import Flask,url_for,render_template,request,url_for,redirect,flash
# 数据库
from flask_sqlalchemy import SQLAlchemy 
# 生成密码 验证密码
from werkzeug.security import generate_password_hash,check_password_hash
# 登录
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user


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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY']='dev'
#关闭对模型修改的监控

# 传入app实例 在配置之后
db=SQLAlchemy(app)

# 实例化登录扩展类  
login_manager = LoginManager(app)
# 用户加载的函数
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user
login_manager.login_view='login'
login_manager.login_manage="您未登录"


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    # 生成密码
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    # 验证密码
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)


class Movie(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# 表单添加
@app.route("/",methods=['GET','POST'])
def index():
    if request.method =="POST":
        if not current_user.is_authenticated:
            return redirect(url_for("index"))
        name = request.form.get("movie_name")
        year = request.form.get("movie_year")
        # 验证数据不为空  year长度不能超过4 name 不能超过60
        if not name or not year or len(year)>4 or len(name)>60:
            flash("输入有误")
            return redirect(url_for("index"))
        movie = Movie(title=name,year=year)
        db.session.add(movie)
        db.session.commit()
        flash("数据插入成功")
        return redirect(url_for("index"))
    movie = Movie.query.all()  #读取所有的电影记录 
    return render_template("index.html",movies=movie)


# 表单编辑 
@app.route('/movie/edit/<int:movies_id>',methods=['GET','POST'])
@login_required
def edit(movies_id):
    mm = Movie.query.get_or_404(movies_id)
    print(mm)
    if request.method=="POST":
        title = request.form['movie_name']
        year = request.form['movie_year']
        # 验证数据不为空  year长度不能超过4 name 不能超过60
        if not title or not year or len(year)>4 or len(title)>60:
            flash("输入有误")
            return redirect(url_for("edit"),movie_id=movies_id)
        mm.title =title
        mm.year = year
        # db.session.add(movie)
        db.session.commit()
        flash("数据编辑成功")
        return redirect(url_for("index"))
    return render_template("edit.html",movie=mm)


# 表单删除
@app.route('/movie/delete/<int:movies_id>',methods=['POST'])
@login_required
def delete(movies_id):
    movie = Movie.query.get_or_404(movies_id)
    db.session.delete(movie)
    db.session.commit()
    flash("数据删除成功")
    return redirect(url_for('index'))



# 登录
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method =="POST":
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash("输入错误")
            return redirect(url_for('login'))
        user = User.query.first()
        # 验证用户名和密码是否一致
        if username==user.username and user.validate_password(password):
            login_user(user)
            flash("登录成功")
            return redirect(url_for('index'))
        flash('用户名或密码错误')
        return redirect(url_for('login'))
    return render_template('login.html')



# 登出
@app.route('/logout')
def logout():
    logout_user()
    flash("退出成功")
    return redirect(url_for('index'))



# 设置
@app.route('/settings',methods=["GET","POST"])
@login_required
def settings():
    if request.method=='POST':
        name = request.form['name']
        if not name or len(name)>20:
            flash("输入有误")
            return redirect("settings")
        current_user.name=name
        # 等于下面两句
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash("设置name成功")
        return redirect(url_for('index'))
    return render_template('settings.html')


#     #动态url 
# @app.route('/index/<name>')
# def home(name):
#     print(url_for("home",name="haominmin"))
#     return "<h1>hello,%s</h1>"%name



# 自定义命令 创建用户的
@app.cli.command()
# 接收用户名   prompt=True提示  
@click.option('--username',prompt=True,help='管理员账号') 
# 接收密码  再次确认密码 需要输入两次 confirmation_prompt=True  hide_input=True秘文
@click.option('--password',prompt=True,help='密码',confirmation_prompt=True,hide_input=True)
def admin(username,password):
    db.create_all()
    user = User.query.first()
    # 如果存在
    if user is not None:
        click.echo('更新用户')
        user.username=username
        user.set_password(password)
        # user.password_hash=password
    else:
        click.echo('创建用户')
        user = User(username=username,name='minmin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo("完成")



# 初始化数据库
@app.cli.command() #装饰器注册命令
@click.option('--drop',is_flag=True,help='删除之后再创建')
def initdb(drop):
    if drop:
  
        db.drop_all()

    db.create_all()

    click.echo("初始化数据库完成")



# 自定义命令导入数据
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


# 错误处理 404
@app.errorhandler(404)
def page_not_found(e):
    # user = User.query.first()
    # return render_template("404.html",user=user),404
    # 返回模板和状态码
    return render_template("404.html"),404


# 模板上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)




