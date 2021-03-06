import os
from flask import Blueprint
from flask import *
from flask import redirect
import datetime
from user import logins
from pymysql import IntegrityError
from sqlalchemy.orm.exc import FlushError

from libs.db import db


# 定义蓝图
from libs.until import gen_password, check_password
from user.logins import save_avatar, login_required
from user.models import User, Follow

user_bp = Blueprint('user',import_name='user')
user_bp.template_folder='./templates'
# 登陆
@user_bp.route('/login', methods=('GET', 'POST'))
def login():
    '''登陆页面'''
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(nickname=nickname).first()
        if user is None:
            return render_template('login.html', error='用户名有误，请重新输入')
        if check_password(password, user.password):
            # 记录用户登陆状态
            session['uid'] = user.id
            session['avatar'] = user.avatar
            return redirect('/user/info')
        else:
            return render_template('login.html', error='密码有误，请重新输入')
    else:
        if 'uid' in session:
            return redirect('/user/info')
        else:
            return render_template('login.html')

# 注册
@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # 先取出所有的参数   如果没有提交就是空格
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()
        gender = request.form.get('gender', '').strip()
        bio = request.form.get('bio', '').strip()
        city = request.form.get('city', '').strip()
        birthday = request.form.get('birthday', '').strip()
        avatar = request.files.get('avatar')
        if avatar:
            avatar_path = '/static/upload/%s' % nickname
        else:
            avatar_path = '/static/upload/default'
        # 创建用户
        user = User(
            nickname=nickname,
            password=gen_password(password),
            # 选择性别
            gender=gender if gender in ['male', 'female'] else 'male',
            bio=bio,
            city=city,
            birthday=birthday,
            # 处理头像地址  保存在某一个文件中   出问题再加上   手动写进来
            avatar=avatar_path,
            created=datetime.datetime.now()
        )
        db.session.add(user)
        # 进行一个异常处理
        try:
            # 会设计事务的提交和回滚的处理
            db.session.commit()
        except IntegrityError:
            # 数据回滚
            db.session.rollback()
            return render_template('register.html', error='昵称已被占用，请换一个')

        save_avatar(nickname,avatar)
        flash('注册成功！')
        return redirect('/user/login')
    else:
        return render_template('register.html')

# 退出
@user_bp.route('/logout')
def logout():
    '''退出'''
    session.pop('uid')
    return redirect('/')

# 信息
@user_bp.route('/info')
def info():
    '''用户个人资料页'''
    uid = session.get('uid')
    fid = int(request.args.get('uid', 0))

    # 查看自己页面
    if uid == fid or fid == 0:
        user = User.query.get(uid)
        return render_template('info.html', user=user)

    # 查看其他人的页面  检查uid
    if fid and uid != fid:
        user = User.query.get(fid)
        is_exist = Follow.query.filter_by(uid=uid, fid=fid).exists()
        followed = db.session.query(is_exist).scalar()
        return render_template('info.html', user=user, followed=followed)

    return render_template('login.html', error='请先登录！')
# 采集人脸
@user_bp.route('/take_face')
def take_face():
    logins.take_face()
    uid = session.get('uid')
    user = User.query.get(uid)
    return render_template('info.html', user=user)
#人脸登录
@user_bp.route('/face_login')
def face_login():
    log = logins.face_recognize()
    if log == 1:
        avatar = User.query.filter_by(id=session['uid']).first().avatar
        session['avatar'] = avatar
        return redirect('/user/info')
# 粉丝列表
@user_bp.route('/fans')
def fans():
    '''粉丝列表'''
    uid = session.get('uid')
    sql ='select * from follow where uid=uid'
    followid =db.session.execute(sql)
    # 查看其他人的页面  检查uid
    user_list = []
    fod_list = {fid.fid for fid in followid}
    for fid in fod_list:
        user_list.append(User.query.get(fid))
    return render_template('fans.html', fans=user_list)

@user_bp.route('/face_check',methods=('GET', 'POST'))
def face_check():
    uid = session['uid']
    filenames = os.listdir('./static/face_certification')
    for name in filenames:
        num = name.split('.',1)[0]
        print(num)
        if num == str(uid):
            return jsonify({"success": 200,"check":1})
    return jsonify({"success": 200,"check":0})

@user_bp.route('/change_avatar')
def change_avatar():
    uid = session.avatar
    user = User.query.filter_by(uid=uid)
    avatar = request.files.get('avatar')
    if avatar:
        avatar_path = '/static/upload/%s' % user.nickname
    else:
        avatar_path = '/static/upload/default'
    logins.save_avatar(user.nickname, avatar)