# -*- coding=utf-8 -*-
import os
class Config:
    SECRET_KEY = 'mr_devops'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/uploads/")  # 文件上传路径
    FC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/uploads/users/")  # 用户头像上传路径

    @staticmethod
    def init_app(app):
        pass

# the config for development
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:jim@123456@47.106.113.39:3307/deopstor'
    DEBUG = True

# define the config
config = {
    'default': DevelopmentConfig
}
