import pymysql
import click
from flask import g
from flask.cli import with_appcontext
from HITBlog.triggers import *
# 支持 ';' 分隔的sql文件，不含有注释，不含有含begin end等特殊开始结束标志的语句（如触发器）
def read_sql_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as sql_file:
        file_str = sql_file.read()
        sql_statements = file_str.split(';')
        sql_file.close()
    return sql_statements

def execute_sql(cmd_all, cursor):
    for cmd in cmd_all:
        try:
            cursor.execute(cmd)
        except:
            pass
        # except Exception as msg:
        #    print("Error: ", msg)
    # print("OK")

def sql_run(filepath, cursor):
    cmd_all = read_sql_file(filepath)
    execute_sql(cmd_all, cursor)

# 缓存数据库创建者（博客网站管理员）信息
def write_cache(cache):
    path_cache = './HITBlog/cache/info.txt'
    with open(path_cache, 'w', encoding='utf-8') as fd:
        fd.write(cache)
    fd.close()

def load_cache():
    path_cache = './HITBlog/cache/info.txt'
    with open(path_cache, 'r', encoding='utf-8') as fd:
        cache = fd.read()
    return cache.split(' ')

def create_db(password, host, dbname):
    # password: password when connect your mysql database
    db = pymysql.connect(
        host=host,
        password=password,
        port=3306,
        user='root',
        charset='utf8'
    )
    cursor = db.cursor()
    # 创建数据库
    cursor.execute("drop database if exists {}".format(dbname))
    cursor.execute("create database if not exists {}".format(dbname))
    cursor.close()


@click.command('init-db')
@click.option('--password', help='The password to connect your mysql server')
@click.option('--host', default="localhost", help='The host ip address to connect your mysql server')
@click.option('--dbname', default="HITBlog", help='The name to this new database for this app')
@with_appcontext
def init_db(password, host, dbname):
    create_db(password, host, dbname)
    cache = password+" "+host+" "+dbname
    write_cache(cache)
    # 连接新建的（或者已有的）数据库
    db_blog = pymysql.connect(
        host=host,
        password=password,
        port=3306,
        user='root',
        db=dbname,
        charset='utf8'
    )
    cursor = db_blog.cursor()
    # 执行建表语句
    sql_run('./HITBlog/NewDatabase.sql', cursor)
    # 添加trigger
    try:
        cursor.execute(trigger_com_appcnt)
        cursor.execute(trigger_default_collector)
        cursor.execute(trigger_delcom)
        cursor.execute(trigger_passage_appcnt)
        cursor.execute(trigger_upd_comappcnt)
        cursor.execute(trigger_upd_pasappcnt)
        cursor.execute(trigger_update_pascomcnt)
        cursor.execute(trigger_ins_cp)
        cursor.execute(trigger_del_cp)
#   except Exception as msg:
#   print(msg)
    except :
        pass
    click.echo("OK, database is ready")

def get_db():
    if "blog_db" not in g:
        args = load_cache()
        if not args:
            return
        db_blog = pymysql.connect(
            host=args[1],
            password=args[0],
            port=3306,
            user='root',
            db=args[2],
            charset='utf8'
        )
        g.blog_db = db_blog
    return g.blog_db

def close_db(e=None):
    db = g.pop('blog_db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
