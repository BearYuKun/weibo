from libs.db import db

class User(db.Model):
    '''用户表'''
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)  #id
    nickname = db.Column(db.String(20), unique=True, nullable=False, index=True)  #昵称
    password = db.Column(db.String(128), nullable=True)  #密码
    gender = db.Column(db.String(10), default='unknow')  #性别
    bio = db.Column(db.String(200))   #经历
    city = db.Column(db.String(16), default='上海')  #所在城市
    avatar = db.Column(db.String(128))  #头像
    birthday = db.Column(db.Date, default='1990-01-01')  #生日
    created = db.Column(db.DateTime)  #创建时间

class Follow(db.Model):
    '''关注表'''
    __tablename__ = 'follow'
    uid = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, primary_key=True)