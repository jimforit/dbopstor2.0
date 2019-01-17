from app import db
from datetime import datetime


# 会员数据模型
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(100))  # 用户名
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号
    status = db.Column(db.Integer())  # 用户状态0：未启用 1：已启用
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    userlogs = db.relationship('Userlog', backref='user')  # 用户日志外键关系关联
    hosts = db.relationship('Host',backref='user')#用户负责主机外检关联
    role_id = db.Column(db.Integer, db.ForeignKey("role.id")) # 用户角色 1管理员 2部门主管 3开发人员

    def __repr__(self):
        return '<User %r>' % self.name

    def check_pwd(self, pwd):
        """
        检测密码是否正确
        :param pwd: 密码
        :return: 返回布尔值
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

class Role(db.Model):
    __tablename__="role"
    id = db.Column(db.Integer(),primary_key=True) #角色编号
    role_name = db.Column(db.String(24),unique=True) #角色名称

    Users = db.relationship('User',backref="role") #用户

# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    adminlogs = db.relationship("Adminlog", backref='admin')  # 管理员登录日志外键关系关联
    oplogs = db.relationship("Oplog", backref='admin')  # 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        """
        检测密码是否正确
        :param pwd: 密码
        :return: 返回布尔值
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id

#订单
class Order(db.Model):
    __tablename__ = "order_detail"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    order_name = db.Column(db.String(64))  # 项目名称
    order_type = db.Column(db.Integer)  # 工单类型
    order_hander_id = db.Column(db.Integer,db.ForeignKey("user.id")) # 工单处理人
    order_config_type = db.Column(db.Integer) #申请架构类型
    order_status = db.Column(db.Integer)  #工单状态 0：待处理 1：已处理
    order_dead_line = db.Column(db.DateTime()) #期望解决日期
    order_node_num = db.Column(db.Integer) #申请节点数量
    order_cpu_cores = db.Column(db.Integer) #申请服务器CPU核心配置
    order_mem_volmn = db.Column(db.Integer) #申请服务器内存容量配置
    order_disk_type = db.Column(db.Integer)  #申请服务器硬盘类型
    order_disk_volmn = db.Column(db.Integer) #申请服务器硬盘容量配置
    order_disk_array = db.Column(db.Integer) #申请服务器磁盘阵列配置
    order_apply_id = db.Column(db.Integer,db.ForeignKey("user.id"))  #申请人ID
    order_comment = db.Column(db.Text) #申请备注

    def __repr__(self):
        return "<Order %r>" % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 操作IP
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


# 地区

# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    # 设置外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # ip地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return '<User %r>' % self.id


# 数据中心
class Datacenter(db.Model):
    __tablename__ = "datacenter"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    data_center_name = db.Column(db.String(64), unique=True)  # 数据中心名称
    data_center_type = db.Column(db.String(20))  # 数据中心类型
    data_center_address = db.Column(db.String(255))  # 数据中心地址
    ip_addr_range = db.Column(db.String(64))  # 网段
    data_center_status = db.Column(db.Integer)  #数据中心状态


    # 设置外键
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))  # 所属服务器
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Datacenter %r>" % self.title

        # 主机信息

class Host(db.Model):
    __tablename__ = "host"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    host_name = db.Column(db.String(64), unique=True)  # 主机名
    host_type = db.Column(db.String(64))  # 主机类型
    ip_addr = db.Column(db.Integer)  # IP地址
    host_status = db.Column(db.Integer)  # 主机状态

    # 设置外键
    data_center_id = db.Column(db.Integer, db.ForeignKey('datacenter.id')) #归属数据中心
    host_admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属管理员
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Host %r>" % self.title


# 景区收藏
"""class Collect(db.Model):
    __tablename__ = "collect"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号

    scenic_id = db.Column(db.Integer, db.ForeignKey('scenic.id'))  # 所属景区
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Collect %r>" % self.id


# 意见建议
class Suggestion(db.Model):
    __tablename__ = "suggestion"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(255))  # 昵称
    email = db.Column(db.String(100))  # 邮箱
    content = db.Column(db.Text)  # 意见内容
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间

    def __repr__(self):
        return "<Suggestion %r>" % self.id"""