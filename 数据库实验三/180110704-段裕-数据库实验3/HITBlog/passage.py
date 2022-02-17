"""
本文件主要处理 文章详情页面、评论 收藏 喜欢 等问题
"""
import json

from flask import (
    Flask, url_for, request, flash, g, Blueprint, render_template, redirect,
    jsonify)
from werkzeug.exceptions import abort
from .login import BLOG_USER_ID
from .login import login_required
from .sqlexcute import get_db
from .functool import *

bp = Blueprint('passage', __name__)


@bp.route('/<int:passage_id>/details', methods=('POST', 'GET'))
def passages(passage_id):
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        comments = request.form['comment']
        # 处理用户评论
        if g.user is None:
            flash("请先登录！")
        elif comments is not None and len(comments.strip()) != 0:
            cursor.execute("""
                    insert into comments(passage_id, user_id, parent_id, comment_apcnt, comment_date, 
                    comment_content) values (%s, %s, %s, %s, %s, %s)
                    """, (passage_id, g.user[BLOG_USER_ID], 0, 0, get_current_date(), comments))
            cursor.close()
            db.commit()
        else:
            flash("评论失败，请稍后再试")
        return redirect(url_for('passage.passages', passage_id=passage_id))

    cursor.execute("""
                select blog_passage.passage_id, blog_passage.user_id, blog_passage.passage_title, 
                       blog_passage.public_date, blog_passage.passage_content, blog_user.nick_name, 
                       blog_passage.applause_counts, blog_passage.comments_count, blog_passage.collection_count
                from blog_passage, blog_user
                where blog_passage.passage_id=%s and blog_passage.user_id=blog_user.user_id
                """, (passage_id,))
    details = cursor.fetchone()
    # 关于评论
    sql_a = """select * from comments where comments.passage_id=%s"""
    cursor.execute(sql_a, (passage_id, ))
    comments = cursor.fetchall()
    # 用户昵称
    sql_b = """select nick_name from blog_user where blog_user.user_id=%s"""
    nicknames = []
    for cm in comments:
        cursor.execute(sql_b, (cm[2]))
        nicknames.append(cursor.fetchone()[0])
    # 文章标签
    sql_passage_labels = "select label_name, passage_label.label_id from passage_label, passage_labels " \
                         "where passage_label.label_id=passage_labels.label_id and passage_labels.passage_id=%s"
    cursor.execute(sql_passage_labels, passage_id)
    passage_labels = cursor.fetchall()
    cursor.close()
    return render_template('/blog/passage.html', post=details, comments=comments,
                           nicknames=nicknames, passage_labels=passage_labels)

@bp.before_app_request
def prepare():
    g.APPLAUSE_STATE = 0

@bp.route('/reply_op', methods=['POST'])
def reply_op():
    data = json.loads(request.form['data'])
    db = get_db()
    cursor = db.cursor()
    sql_s = "select * from comments where comment_id = %s"
    cursor.execute(sql_s, (data['parent_id'], ))
    parent = cursor.fetchone()
    # 查看parent是否也是回复
    print(parent)
    if parent[3] == 0:
        p_con = rectify_10('#'+str(data['lou'])+'楼: '+parent[6])+"... ..."
    else:
        p_con = rectify_10('#'+str(data['lou'])+'楼: '+parent[6][20:])+"... ..."
    sql = """
    insert into comments(passage_id, user_id, parent_id, comment_apcnt, comment_date, comment_content)
    values (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (data['passage_id'], g.user[BLOG_USER_ID],
                         data['parent_id'], 0, get_current_date(),
                         p_con+data['comment_content']))
    db.commit()
    cursor.close()
    return jsonify({"success": 200})

def rectify_10(p):
    if(len(p)) > 13:
        return p[:13]
    else:
        return p.ljust(13, ' ')

@bp.route('/del_comment', methods=['POST'])
def del_comment():
    data = json.loads(request.form['data'])
    db = get_db()
    cursor = db.cursor()
    cursor.execute("delete from comments where comment_id=%s", (data['comment_id'], ))
    cursor.execute("delete from comments where parent_id=%s", (data['comment_id'], ))
    db.commit()
    cursor.close()
    return jsonify({"success": 200})

@bp.route('/cope/favourite', methods=['POST'])
def cope_favour():
    data = json.loads(request.form['data'])
    passage_id = data['passage_id']
    user_id = data['user_id']
    like_cnt = data['like_cnt']
    # 先查询 1、有没有记录，若有则查看状态status，为1则转0，取消喜欢，否则喜欢
    # 没有记录则插入记录，表示喜欢
    db = get_db()
    cursor = db.cursor()
    sql_get = """
    select ap_status from passage_applause where passage_id=%s and user_id=%s
    """
    cursor.execute(sql_get, (passage_id, user_id))
    if_record = cursor.fetchone()
    sql_insert = """
    insert into passage_applause(ap_status, passage_ap_date, passage_id, user_id) values (%s, %s, %s, %s)
    """
    sql_update = """
    update passage_applause set ap_status=%s, passage_ap_date=%s where passage_id=%s and user_id=%s
    """
    print(if_record)
    if if_record is None:   # 表示没有记录
        # 则插入该条记录
        cursor.execute(sql_insert, (1, get_current_date(), passage_id, user_id))
        db.commit()
        cursor.close()
        return jsonify({'status': 0, 'favor': like_cnt+1})
    elif if_record[0] == '0':
        # 表示曾经取消喜欢，但又回心转意
        cursor.execute(sql_update, (1, get_current_date(), passage_id, user_id))
        db.commit()
        cursor.close()
        return jsonify({'status': 1, 'favor': like_cnt+1})
    elif if_record[0] == '1':
        # 我喜欢过，但现在不爱了
        cursor.execute(sql_update, (0, get_current_date(), passage_id, user_id))
        db.commit()
        cursor.close()
        return jsonify({'status': 2, 'favor': like_cnt-1})

@bp.route('/cope/collector', methods=['POST'])
@login_required
def cope_collector():
    data = json.loads(request.form['data'])
    print(data)
    try:
        passage_id = data['passage_id']
        user_id = data['user_id']
        collector_id = data['collector_id']
    except:
        return {"status": 500}
    db = get_db()
    cursor = db.cursor()
    # 查看文章是否已收藏
    sql_sel = "select * from collector_passages where user_id=%s and collector_id=%s and passage_id=%s"
    cursor.execute(sql_sel, (user_id, collector_id, passage_id))
    rec = cursor.fetchone()
    if rec is not None:
        return {'status': 0}
    # 将文章收藏
    sql = "insert into collector_passages(user_id, collector_id, passage_id) values (%s, %s, %s)"
    cursor.execute(sql, (user_id, collector_id, passage_id))
    db.commit()
    cursor.close()
    return {'status': 1}

@bp.route('/inc/collector', methods=['POST'])
@login_required
def create_collector():
    data = json.loads(request.form['data'])
    print(data)
    user_id = data['user_id']
    collector_name = data['collector_name']
    sql_id = "select count(*) from collector where user_id=%s group by user_id"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql_id, user_id)
    collector_id = cursor.fetchone()[0]+1
    print(collector_id)
    # 插入收藏夹
    sql_insert = "insert into collector(user_id, collector_id, collector_name) values (%s, %s, %s)"
    cursor.execute(sql_insert, (user_id, collector_id, collector_name))
    db.commit()
    cursor.close()
    return {'status': 200}

@bp.route('/comment/applause', methods=['POST'])
@login_required
def comment_applause():
    data = json.loads(request.form['data'])
    user_id = data['user_id']
    comment_id = data['comment_id']
    db = get_db()
    cursor = db.cursor()
    sql_select = "select * from comment_applause where user_id=%s and comment_id=%s"
    # 查看点赞状态
    cursor.execute(sql_select, (user_id, comment_id))
    status = cursor.fetchone()
    if status is None:
        # 用户未点赞
        sql_insert = """insert into comment_applause(comment_id, user_id, ap_date, ap_status)
        values (%s, %s, %s, %s)
        """
        try:
            cursor.execute(sql_insert, (comment_id, user_id, get_current_date(), 1))
            db.commit()
            cursor.close()
        except Exception as e:
            print(e)
            return {'status': 0}
        return {'status': 1}
    else:
        # 有用户的行为记录
        if status[3] == '1':
            cursor.execute("""
            update comment_applause
            set ap_status=%s, ap_date=%s
            where user_id=%s and comment_id=%s
            """, (0, get_current_date(), user_id, comment_id))
            db.commit()
            cursor.close()
            return {'status': 1}
        if status[3] == '0':
            cursor.execute("""
            update comment_applause
            set ap_status=%s, ap_date=%s
            where user_id=%s and comment_id=%s
            """, (1, get_current_date(), user_id, comment_id))
            db.commit()
            cursor.close()
            return {'status': 1}
