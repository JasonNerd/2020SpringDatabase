"""
SELECT `blog_passage`.`passage_id`,
    `blog_passage`.`user_id`,
    `blog_passage`.`passage_title`,
    `blog_passage`.`public_date`,
    `blog_passage`.`passage_content`,
    `blog_passage`.`applause_counts`,
    `blog_passage`.`comments_count`,
    `blog_passage`.`collection_count`
FROM `hitblog`.`blog_passage`;
"""
import json

from flask import (
    Flask, url_for, request, flash, g, Blueprint, render_template, redirect
)
from werkzeug.exceptions import abort
from .login import BLOG_USER_ID
from .login import login_required
from .sqlexcute import get_db
from .functool import *

bp = Blueprint('blog', __name__)
PASSAGE_TITLE = 2
USER_ID = 1
PASSAGE_CONTENT = 4
NICK_NAME = 5
PUBLIC_DATE = 3
PASSAGE_ID = 0
@bp.route('/', methods=['POST', 'GET'])
def index():
    # 主页的显示设置，显示 “最热” 的十篇文章
    db = get_db()
    cursor = db.cursor()
    sql_get_10 = """
            select blog_passage.passage_id, blog_passage.user_id, blog_passage.passage_title, 
                   blog_passage.public_date, blog_passage.passage_content, blog_user.nick_name
            from blog_passage, blog_user
            where blog_passage.user_id=blog_user.user_id
            order by (applause_counts+comments_count+collection_count)
            desc limit 15
            """
    cursor.execute(sql_get_10)
    posts = cursor.fetchall()
    cursor.close()
    return render_template('/blog/index.html', posts=posts)


@bp.route("/homepage/<int:user_id>")
def homepage(user_id):
    # 查看个人主页：游客、别的用户、自己
    if g.user and user_id == g.user[BLOG_USER_ID]:   # 查看用户的人是自己
        is_me = 1
    else:
        is_me = 0
    user_blog_info, user_passages, user_base_info, guan_zhu_list, fen_si_list, clshu, collectors_all = get_post(user_id)
    return render_template("/blog/homepage.html", blog_info=user_blog_info,
                           passages=user_passages, user_base_info=user_base_info,
                           fen_si_list=fen_si_list, fensishu=len(fen_si_list),
                           guan_zhu_list=guan_zhu_list, guanzhushu=len(guan_zhu_list),
                           clshu=clshu, collectors_all=collectors_all, is_me=is_me)

def get_post(user_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("select * from user_blogs_info where user_id=%s", (user_id, ))
        user_blog_info = cursor.fetchone()
    except Exception as e:
        user_blog_info = ()
        print(e)
    try:
        cursor.execute("select * from query_user_base_info where user_id=%s", (user_id, ))
        user_base_info = cursor.fetchone()
    except Exception as e:
        user_base_info = ()
        print(e)
    try:
        cursor.execute("select passage_content, passage_title, passage_id from blog_passage where user_id=%s", (user_id, ))
        user_passages = cursor.fetchall()
    except Exception as e:
        user_passages=()
        print(e)
    # 获取用户的粉丝列表和关注列表
    try:
        cursor.execute("select concern_date, to_user_id "
                       "from concern, blog_user "
                       "where from_user_id=%s and blog_user.user_id=concern.from_user_id", user_id)
        guan_zhu_list = cursor.fetchall()
    except Exception as e:
        guan_zhu_list = ()
        print(e)
    try:
        cursor.execute("select concern_date, from_user_id "
                       "from concern, blog_user "
                       "where to_user_id=%s and blog_user.user_id=concern.to_user_id", user_id)
        fen_si_list = cursor.fetchall()
    except Exception as e:
        fen_si_list = ()
        print(e)
    # 获取用户收藏了多少文章
    try:
        cursor.execute("select count(*) from collector_passages where user_id=%s group by user_id", user_id)
        clshu = cursor.fetchone()[0]
    except Exception as e:
        clshu = 0
        print(e)
    # 用户有多少收藏夹
    try:
        cursor.execute("select count(*) from collector where user_id=%s group by user_id", user_id)
        ds_clt = cursor.fetchone()[0]
    except Exception as e:
        ds_clt = 0
        print(e)
    collectors_all = []
    for i in range(ds_clt):
        collectors_all.append(collector_details(user_id, i+1))
    cursor.close()
    print(user_blog_info)
    return user_blog_info, user_passages, user_base_info, guan_zhu_list, fen_si_list, clshu, collectors_all

@bp.before_app_request
def prepare_home_page():
    g.PASSAGE_TITLE = PASSAGE_TITLE
    g.USER_ID = USER_ID
    g.PASSAGE_CONTENT = PASSAGE_CONTENT
    g.NICK_NAME = NICK_NAME
    g.PUBLIC_DATE = PUBLIC_DATE
    g.PASSAGE_ID = PASSAGE_ID

@bp.route('/<int:user_id>/publish/article', methods=('POST', 'GET'))
@login_required
def publish(user_id):
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        data = json.loads(request.form['data'])
        title = data['title']
        body = data['body']
        labels = data['labels']
        if len(title) > 30:
            flash("标题字数过长")
            return {'status': 0}
        # 前端已保证接收到的数据不会为空
        cursor.execute("""
                    insert into blog_passage(user_id, passage_title, public_date, passage_content, 
                    applause_counts, comments_count, collection_count) values (%s, %s, %s, %s, %s, %s, %s)
                    """, (user_id, title, get_current_date(), body, 0, 0, 0)
                       )
        cursor.execute('select last_insert_id()')
        passage_id = cursor.fetchone()[0]
        # 将文章标签插入
        sql_label = "insert into passage_labels(label_id, passage_id) values (%s, %s)"
        for label in labels:
            cursor.execute(sql_label, (label, passage_id))
        db.commit()
        cursor.close()
        return {'status': user_id}
    cursor.execute("select * from passage_label")
    labels = cursor.fetchall()
    cursor.close()
    return render_template('/blog/create.html', user_id=user_id, labels=labels)

@bp.route('/<int:user_id>/update/article/<int:passage_id>', methods=('POST', 'GET'))
@login_required
def update_passage(passage_id, user_id):
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = "标题不可以为空！"
        if error is not None:
            flash(error)
        else:
            cursor = db.cursor()
            cursor.execute("""update blog_passage 
            set passage_title=%s, passage_content=%s 
            where passage_id=%s""", (title, body, passage_id))
            cursor.close()
            db.commit()
            return redirect(url_for('blog.homepage', user_id=user_id))
    cursor = db.cursor()
    cursor.execute("select * from blog_passage where passage_id=%s", (passage_id, ))
    post = cursor.fetchone()
    cursor.close()
    return render_template('/blog/update.html', post=post)


@bp.route('/<int:user_id>/delete/article/<int:passage_id>', methods=('POST', 'GET'))
@login_required
def delete_passage(passage_id, user_id):
    # 当一个用户删除一篇文章时，附带的评论点赞等等都会连带着删除
    db = get_db()
    cursor = db.cursor()
    # 删除文章
    cursor.execute("delete from blog_passage where passage_id=%s", (passage_id, ))
    # 删除评论
    cursor.execute("select comment_id from comments where comments.passage_id=%s", (passage_id, ))
    pas_comments = cursor.fetchall()
    try:
        cursor.executemany("delete from comments where comment_id=%s", pas_comments)
    except Exception as e:
        db.rollback()
        print(e)
    db.commit()
    # 删除关于文章点赞
    try:
        cursor.execute("delete from passage_applause where passage_applause.passage_id=%s", passage_id)
    except Exception as e:
        db.rollback()
        print(e)
    db.commit()
    # 删除关于文章标签
    try:
        cursor.execute("delete from passage_labels where passage_labels.passage_id=%s", passage_id)
    except Exception as e:
        db.rollback()
        print(e)
    db.commit()
    # 删除对于评论的点赞
    try:
        cursor.executemany("delete from comment_applause where comment_applause.comment_id=%s", pas_comments)
    except Exception as e:
        db.rollback()
        print(e)
    db.commit()
    # 删除收藏夹文章
    try:
        cursor.execute("delete from collector_passages where collector_passages.passage_id=%s", passage_id)
    except Exception as e:
        db.rollback()
        print(e)
    db.commit()
    return redirect(url_for('blog.homepage', user_id=user_id))

@bp.route('/fans/followee', methods=['POST'])
@login_required
def follower():
    try:
        data = json.loads(request.form['data'])
        from_user_id = data['from_user_id']
        to_user_id = data['to_user_id']
    except Exception as e:
        print(e)
        return {'error': 500}
    db = get_db()
    cursor = db.cursor()
    # 应该先查询是否重复
    cursor.execute("""select * from concern where from_user_id=%s and to_user_id=%s""",
                   (from_user_id, to_user_id))
    is_conflict = cursor.fetchone()
    if is_conflict is not None:
        return {'conflict': 1}
    cursor.execute("""
    insert into concern(concern_date, from_user_id, to_user_id) values (%s, %s, %s)
    """, (get_current_date(), from_user_id, to_user_id))
    db.commit()
    cursor.close()
    print("whadask")
    return {"conflict": 0}


def collector_details(user_id, collect_id):
    sql_sig = """select passage_id from collector_passages where user_id=%s and collector_id=%s"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql_sig, (user_id, collect_id))
    ps_ids = cursor.fetchall()
    sql_passage = """select passage_title, public_date
            from blog_passage where passage_id = %s
            """
    passages = []
    for ps_id in ps_ids:
        cursor.execute(sql_passage, ps_id[0])
        mes = cursor.fetchone()
        if mes:
            data = (ps_id[0], mes[0], str(mes[1]))
            passages.append(data)
    return passages

@bp.route('/label/<label_id>')
def label_list(label_id):
    # 主页的显示设置，显示 “最热” 的十篇文章
    db = get_db()
    cursor = db.cursor()
    sql_get_10 = """
    select blog_passage.passage_id, blog_passage.user_id, blog_passage.passage_title, 
           blog_passage.public_date, blog_passage.passage_content, blog_user.nick_name
    from blog_passage, passage_labels, blog_user
    where blog_passage.passage_id=passage_labels.passage_id and 
          blog_user.user_id=blog_passage.user_id and 
          passage_labels.label_id=%s
    order by (applause_counts+comments_count+collection_count)
    """
    cursor.execute(sql_get_10, label_id)
    posts = cursor.fetchall()
    cursor.close()
    return render_template('/blog/index.html', posts=posts)

@bp.route('/<int:user_id>/remove_user')
@login_required
def remove_user(user_id):
    pass

@bp.route('/<int:user_id>/update_user', methods=['POST'])
@login_required
def update_user(user_id):
    username = request.form['username']
    phone = request.form['phone']
    mail_address = request.form['mail_address']
    print(username+"\n"+mail_address+"\n"+phone+"\n")
    error = None
    db = get_db()
    cursor = db.cursor()
    if not phone and not mail_address:
        error = "请至少填入手机或邮箱中的一项"
    elif len(username) > 15:
        error = "昵称过长，尝试换一个吧"
    elif phone and not is_phone_number(phone):
        error = "请输入正确格式的手机号"
    elif mail_address and not is_mail_addr(mail_address):
        error = "请输入常用格式的邮箱"
    if error is None:
        sql_upd = """
        update blog_user
        set nick_name=%s, phone_num=%s, mail_addr=%s
        where user_id=%s
        """
        cursor.execute(sql_upd, (username, phone, mail_address, user_id))
        db.commit()
        cursor.close()
    else:
        flash(error)
    return redirect(url_for('blog.homepage', user_id=user_id))

@bp.route("/search/", methods=[ 'POST'])
def search():
    db = get_db()
    cursor = db.cursor()
    key = request.form['search']
    error = None
    if not key:
        error = "搜索内容为空！"
    print(key)
    if error is None:
        sql_get_10 = """
                select blog_passage.passage_id, blog_passage.user_id, blog_passage.passage_title, 
                blog_passage.public_date, blog_passage.passage_content, blog_user.nick_name
                from blog_passage, blog_user
                where passage_title like %s and blog_passage.user_id=blog_user.user_id
                order by public_date desc 
                """
        cursor.execute(sql_get_10, "%"+key+"%")
        posts = cursor.fetchall()
        cursor.close()
    else:
        flash(error)
        return redirect(url_for('blog.index'))
    return render_template('/blog/index.html', posts=posts)
