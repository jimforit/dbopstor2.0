from app import db
from flask import render_template, url_for, redirect, flash, session, request
from werkzeug.security import generate_password_hash
from functools import wraps
from app.home.forms import UserForm,RegisterForm,UserEditForm,PwdEditForm
from app.home import home
from app.models import User,Userlog,Role,Order
import json

def user_login(f):
    @wraps(f)
    def function_decorator(*args,**kwargs):
        if "user_id" not in session:
            flash("请先登录","err")
            return redirect(url_for("home.login"))
        return f(*args, **kwargs)
    return function_decorator

@home.route("/login/", methods=["GET", "POST"])
def login():
    form =UserForm()
    if form.validate_on_submit():
        data=form.data
        user = User.query.filter_by(username=data["user_name"]).first()
        if not user:
            flash("用户不存在","err")
            return redirect(url_for("home.login"))
        else:
            if not user.check_pwd(data["password"]):
                flash("密码不正确","err")
                return redirect(url_for("home.login"))
            if not user.status:
                flash("用户未启用","err")
                return redirect(url_for("home.login"))
            else:
                session["user_id"]=user.id
                session["user_name"]=user.username
            userlog= Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.index"))
    return render_template("home/login.html", form=form)


@home.route("/index/", methods=["GET"])
@user_login
def index():
    return render_template("home/index.html")

@home.route("/welcome/", methods=["GET"])
@user_login
def system_detail():
    form={}
    user_info=Userlog.query.filter_by(user_id=session["user_id"]).all()
    if len(user_info)>1:
        form["addtime"]=user_info[-2].addtime

    else:
        form["addtime"] = user_info[0].addtime
    form["username"] = session["user_name"]
    return render_template("home/welcome.html",user=form)


@home.route("/logout/", methods=["GET"])
def logout():
    """退出登录清理会话信息"""
    session.pop("user_id",None)
    flash("用户已退出","ok")
    return redirect(url_for("home.login"))

@home.route("/data_center/", methods=["POST","GET"])
@user_login
def data_center():
    """退出登录清理会话信息"""
    return render_template("home/cate.html")

@home.route("/data_center/add", methods=["POST","GET"])
@user_login
def data_center_add():
    """退出登录清理会话信息"""
    return render_template("home/datacenter-add.html")

@home.route("/host", methods=["POST","GET"])
@user_login
def host():
    """服务器维护列表"""
    return render_template("home/host_list.html")

@home.route("/host/add", methods=["POST","GET"])
@user_login
def host_add():
    """服务器新增页面"""
    return render_template("home/host-add.html")


@home.route("/user_list/", methods=["POST","GET"])
@user_login
def user_list():
    """退出登录清理会话信息"""
    form = UserForm()
    if request.method=="GET":
        user = User.query.filter_by().all()
    else:
        uname = request.form["username"]
        start = request.form["start"]
        end = request.form["start"]
        user = User.query.filter_by(username=uname).all()
    count = len(user)
    return render_template("home/member-list.html", form=user, count=count)

@home.route("/user/disable/", methods=["POST"])
@user_login
def user_disable():
    form=json.loads(request.data.decode())
    user = User.query.filter_by(id=form["id"]).first()
    if form["action"]=="active":
        user.status=1
    else:
        user.status=0
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home.user_list'))

@home.route("/user/edit/<int:id>/", methods=["POST","GET"])
@user_login
def user_edit(id=None):
    """退出登录清理会话信息"""
    form = UserEditForm()
    user = User.query.get_or_404(id)
    if request.method=="GET":
        pass
    else:
        if form.validate_on_submit():
            flash("修改成功","ok")
            user.phone = request.form['phone']
            user.email = request.form['email']
            user.role_id=request.form['role']
            db.session.add(user)
            db.session.commit()
        else:
            flash("修改失败", "err")
    return render_template("home/member-edit.html", form=form, user=user)


@home.route("/user/password/<int:id>/", methods=["POST","GET"])
@user_login
def user_cpwd(id=None):
    form = PwdEditForm()
    user = User.query.get_or_404(id)
    if request.method=="GET":
        pass
    else:
        print(form.data)
        if form.validate_on_submit():
            if user.check_pwd(form.data["oldpwd"]):
                user.pwd=generate_password_hash(form.data["pwd"])
                db.session.add(user)
                db.session.commit()
                flash("修改成功","ok")
            elif form.data["pwd"]==user.pwd:
                flash("不能与旧密码一致！")
            else:
                flash("旧密码不正确", "err")
        else:
            flash("修改失败", "err")
    return render_template("home/member-password.html", form=form, user=user)

@home.route("/user/delete/", methods=["POST"])
@user_login
def user_del():
    form = json.loads(request.data.decode())
    data = form['cid']
    if type(data)=='dict':
        for key in data.keys():
            user=User.query.filter_by(id=int(data[key])).first()
            db.session.delete(user)
            db.session.commit()
    else:
        user = User.query.filter_by(id=int(data)).first()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('home.user_list'))

@home.route("/user/add/", methods=["POST","GET"])
@user_login
def user_add():
    """退出登录清理会话信息"""
    return render_template("home/member-add.html")

@home.route("/order_list/", methods=["POST","GET"])
@user_login
def order_list():
    """工单信息列表"""
    order = Order.query.filter(Order.order_status==0).all()
    for item in order:
        print(item.order_status)
    return render_template("home/order-list.html",order=order)

@home.route("/order_apply/", methods=["POST","GET"])
@user_login
def order_apply():
    """工单信息列表"""
    #apply_info = User.query.join(order)(User.id==order.order_apply_id).all()
    #handler_info = User.query.join(order)(User.id==order.order_hander_id).all()

    return render_template("home/order-apply.html")

@home.route("/order_add/", methods=["POST","GET"])
@user_login
def order_add():
    """工单信息列表"""
    return render_template("home/order-add.html")

@home.route("/register/", methods=["GET", "POST"])
def register():
    """
    注册功能
    """
    form = RegisterForm()           # 导入注册表单
    if form.validate_on_submit():   # 提交注册表单
        data = form.data            # 接收表单数据
        # 为User类属性赋值
        user = User(
            username = data["username"],            # 用户名
            email = data["email"],                  # 邮箱
            phone =data["phone"],  # 手机号
            role_id = data["role"],  #用户角色
            pwd = generate_password_hash(data["pwd"]),# 对密码加密
        )
        db.session.add(user) # 添加数据
        db.session.commit()  # 提交数据
        flash("注册成功！", "ok") # 使用flask存储成功信息
        return redirect(url_for("home.login"))  # 渲染模板
    return render_template("home/register.html", form=form) # 渲染模板
