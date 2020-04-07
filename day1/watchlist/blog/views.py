from blog import db,app

from blog.models import User,Movie

from flask import redirect,render_template,flash,request

from flask_login import login_required,LoginManager,logout_user,current_user,login_user

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
