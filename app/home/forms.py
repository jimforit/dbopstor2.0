from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField,DateTimeField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError
from app.models import User
import time


class UserForm(FlaskForm):
    user_name = StringField(
        label="用户名",
        validators=[
            DataRequired("用户名不能为空"),
        ],
        description="请输入用户名",
        render_kw={
            "class": "layui-input",
            "placeholder": "请输入账号！",
        }
    )
    password = StringField(
        label="密码",
        validators=[
            DataRequired("密码不能为空"),
        ],
        description="请输入密码",
        render_kw={
            "class": "layui-input",
            "placeholder": "请输入密码"
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )


class UserEditForm(FlaskForm):
    username = StringField(
        label="用户名",
        validators=[
            DataRequired("用户名不能为空！"),
        ],
        description="用户名",
        render_kw={
            "placeholder": "请输入用户名！",
        }
    )
    phone = StringField(
        label="手机号",
        validators=[
            DataRequired("手机号不能为空！"),
            Regexp("1[34578]\\d{9}", message="手机号码格式不正确！")
        ],
        description="手机号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码！",
        }
    )
    role = SelectField(
        label="角色",
        validators=[
            DataRequired("请选择角色！")
        ],
        # star的数据类型
        coerce=int,
        choices=[(1, "管理员"), (2, "部门主管"), (3, "开发人员")],
        description="角色",
        render_kw={
            "class": "layui-input",
        }
    )
    email = StringField(
        label="邮箱地址",
        validators=[
            DataRequired("邮箱不能为空！"),
            Email("邮箱格式不正确！")
        ],
        description="邮箱",
        render_kw={
            "type": "email",
            "placeholder": "请输入邮箱！",
        }
    )
    submit = SubmitField(
        '确认',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )


class PwdEditForm(FlaskForm):
    username = StringField(
        label="用户名",
        validators=[
            DataRequired("用户名不能为空！"),
        ],
        description="用户名",
        render_kw={
            "placeholder": "请输入用户名！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空！")
        ],
        description="密码",
        render_kw={
            "placeholder": "请输入密码！",
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('pwd', message="两次密码不一致！")
        ],
        description="确认密码",
        render_kw={
            "placeholder": "请输入确认密码！",
        }
    )
    oldpwd = StringField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！"),
        ],
        description="旧密码",
        render_kw={
            "placeholder": "请输入旧密码！",
        }
    )
    submit = SubmitField(
        '确认',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

class Endvalidators(object):
    '''自定义验证规则'''

    def __init__(self, message):
        self.message = message

    def __call__(self, form, field):
        cur_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if field.data < cur_date:
            raise ValidationError(self.message)

class OrderApplyForm(FlaskForm):
    ordername = StringField(
        label="项目名称",
        validators=[
            DataRequired("项目名称不能为空！"),
        ],
        description="项目名称",
        render_kw={
            "placeholder": "请输入项目名称！",
        }
    )
    order_end = StringField(
        label="期望时限",
        validators=[
            Endvalidators(message='期望日期小于当前日期')

        ],
        description="期望时限",
        render_kw={
            "type": "end_date",
            "placeholder": "请选择期望时限！",
        }
    )

class RegisterForm(FlaskForm):
    """
    用户注册表单
    """
    username = StringField(
        label="用户名",
        validators=[
            DataRequired("用户名不能为空！"),
        ],
        description="用户名",
        render_kw={
            "placeholder": "请输入用户名！",
        }
    )
    phone = StringField(
        label="手机号",
        validators=[
            DataRequired("手机号不能为空！"),
            Regexp("1[34578]\\d{9}", message="手机号码格式不正确！")
        ],
        description="手机号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码！",
        }
    )
    role = SelectField(
        label="角色",
        validators=[
            DataRequired("请选择角色！")
        ],
        # star的数据类型
        coerce=int,
        choices=[(1, "管理员"), (2, "部门主管"), (3, "开发人员")],
        description="角色",
        render_kw={
            "class": "layui-input",
        }
    )
    email = StringField(
        label="邮箱地址",
        validators=[
            DataRequired("邮箱不能为空！"),
            Email("邮箱格式不正确！")
        ],
        description="邮箱",
        render_kw={
            "type": "email",
            "placeholder": "请输入邮箱！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空！")
        ],
        description="密码",
        render_kw={
            "placeholder": "请输入密码！",
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('pwd', message="两次密码不一致！")
        ],
        description="确认密码",
        render_kw={
            "placeholder": "请输入确认密码！",
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validate_email(self, field):
        """
        检测注册邮箱是否已经存在
        :param field: 字段名
        """
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在！")


    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("用户名已经存在！")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("手机号码已经存在！")
