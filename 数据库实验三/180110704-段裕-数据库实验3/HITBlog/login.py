# 处理用户登录与注册请求
"""
user_id, nick_name, password, gender, reg_date, phone_num, mail_addr, birthday, state
登录设置为 手机号/用户名/邮箱 + 密码 登录，后期如果有验证码，可以利用邮箱实现
初次注册会 自动分配ID，用户名+密码 为必选项，其它为可选项，并且用户名不可重复（参考b站的规则）
(180110101, 逆行者, nxz101, F, 2021-04-03, 07550101520, nxznb@qq.com,2019-02-11,1)
"""
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from HITBlog.sqlexcute import get_db
from HITBlog.functool import *

bp = Blueprint("auth", __name__, url_prefix="/auth")
BLOG_USER_NAME = 1
BLOG_USER_KEY = 2
BLOG_USER_PHONE = 5
BLOG_USER_MAIL = 6
BLOG_USER_ID = 0
BLOG_USER_REGDATE = 4
# 注册视图
@bp.route('/register', methods=("GET", "POST"))
def register():
    if request.method == "POST":
        blog_db = get_db()
        cursor = blog_db.cursor()
        username = request.form['username']  # 必选
        password = request.form['password']  # 必选
        phone = request.form['phone']
        mail_address = request.form['mail_address']
        gender = request.form['gender']
        birthday = request.form['birthday']
        error = None

        print(username+"\n"+password+"\n"+phone+"\n"+mail_address+"\n"+
              gender+"\n"+birthday)
        if not phone and not mail_address:
            error = "请至少填入手机或邮箱中的一项"
        elif len(username) > 15:
            error = "昵称过长，尝试换一个吧"
        elif phone and not is_phone_number(phone):
            error = "请输入正确格式的手机号"
        elif mail_address and not is_mail_addr(mail_address):
            error = "请输入常用格式的邮箱"
        elif not is_password_valid(password):
            error = "密码必须是6至15位的字母数字组合！"
        else:
            cursor.execute("select * from blog_user where nick_name=%s",
                           (username,))
            data = cursor.fetchone()
            if data is not None:
                error = "昵称已存在！"

        if error is None:
            print("------------进入数据库区域-------------")
            cursor.execute("insert into blog_user(nick_name, "
                           "password, gender, reg_date, phone_num, "
                           "mail_addr, birthday, state) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (username, generate_password_hash(password),
                            gender, get_current_date(), phone,
                            mail_address, birthday, '1'))
            flash("恭喜你正式成为HITBlogger!!!")
            blog_db.commit()    # 如果不commit, 数据库将不会更新
            return redirect(url_for('auth.login'))
        cursor.close()
        flash(error)
    return render_template('/auth/register.html')

@bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == "POST":
        usr = request.form['username']
        key = request.form['password']
        error = None
        db = get_db().cursor()
        info = None
        if not usr:
            error = "请填入手机/邮箱/昵称"
        elif not key:
            error = "请输入密码"
        elif is_mail_addr(usr):  # 是邮箱
            db.execute("select * from blog_user where mail_addr=%s", (usr, ))
            mail = db.fetchone()
            if mail is None:
                error = "该邮箱未绑定！"
            elif not check_password_hash(mail[BLOG_USER_KEY], key):
                error = "密码不正确"
            info = mail
        elif is_phone_number(usr):  # 是手机号
            db.execute("select * from blog_user where phone_num=%s", (usr, ))
            phone = db.fetchone()
            if phone is None:
                error = "该手机号未绑定！"
            elif not check_password_hash(phone[BLOG_USER_KEY], key):
                error = "密码不正确"
            info = phone
        else:  # 不是邮箱也不是手机号，默认它是用户名
            db.execute("select * from blog_user where nick_name=%s", (usr,))
            name = db.fetchone()
            if name is None:
                error = "账号不存在！"
            elif not check_password_hash(name[BLOG_USER_KEY], key):
                error = "密码不正确"
            info = name
        # 最后还要查看用户的status是否已注销
        if info and info[8] != '1':
            error = "账户已注销"
        if error is None:
            session.clear()
            session['user_id'] = info[BLOG_USER_ID]
            return redirect(url_for('blog.index'))
        db.close()
        flash(error)
    return render_template('/auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        cursor = get_db().cursor()
        cursor.execute(
            "SELECT * FROM blog_user WHERE user_id=%s",
            (user_id, )
        )
        g.user = cursor.fetchone()
        g.BLOG_USER_NAME = BLOG_USER_NAME
        g.BLOG_USER_KEY = BLOG_USER_KEY
        g.BLOG_USER_PHONE = BLOG_USER_PHONE
        g.BLOG_USER_ID = BLOG_USER_ID
        g.BLOG_USER_REGDATE = BLOG_USER_REGDATE
        # 将用户的收藏夹信息加载到g
        cursor.execute("select * from collector where user_id=%s", (user_id, ))
        g.collector = cursor.fetchall()
        cursor.close()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


