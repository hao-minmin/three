# 命令
from blog import db,app

from blog.models import User,Movie

import click


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
        db.session.add(user)
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