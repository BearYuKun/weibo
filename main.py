#分层清晰会让别人更容易的看你的代码
# 也会更容易的区分pythonweb的交互方式
from flask import Flask
from flask import redirect

from comment.views import comment_bp
from user import user_bp
from libs.db import db
# 注册App
from weibo.views import weibo_bp

app = Flask(__name__)
# 去除数据表模型警告的特殊字符
app.secret_key = 'M\\xD6\\xD0\\xB9\\xFA\\xB1\\xEA'
app.register_blueprint(user_bp,url_prefix='/user')
app.register_blueprint(weibo_bp,url_prefix='/weibo')
app.register_blueprint(comment_bp, url_prefix='/comment')

# 初始化数据库的设置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/weibo_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



# # 初始化APP
db.init_app(app)

#跳到微博首页
@app.route('/')
def home():
    return redirect('/weibo/')

if __name__ == '__main__':
    # 机房  同一个IP段  进行互相访问
    app.debug = True
    #app.run(host='0.0.0.0',port=80)
    app.run()