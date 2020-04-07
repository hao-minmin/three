import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)


# 得到当前平台
WIN = sys.platform.startswith('win')
if WIN:
    # 请求头
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


# 配置要在实例化之前
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix+os.path.join(os.path.dirname(app.root_path),os.getenv('SECRET_FILE','data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY']=os.getenv('SECRET_KEY','dev')

# 传入app实例 在配置之后
db=SQLAlchemy(app)

# 实例化登录扩展类  
login_manager = LoginManager(app)
# 用户加载的函数
@login_manager.user_loader
def load_user(user_id):
    from blog.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view='login'
login_manager.login_manage="您未登录"



# 模板上下文处理函数
@app.context_processor
def inject_user():
    from blog.models import User
    user = User.query.first()
    return dict(user=user)


from blog import views,error,commands 