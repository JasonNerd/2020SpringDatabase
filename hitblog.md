# HITBlog校园博客系统

## 基本步骤
* 需求分析
* 表结构设计
* 前端学习
* 前后端数据交互
* 遵循原则：先做好顶层设计，然后先做一个最基本的应用框架，这里最初是flask官方中文手册给出的博客示例，再一步步的添加功能模块，先用户信息管理，然后是文章发布管理，最后是评论与收藏模块的实现


## 基本需求分析
* 用户管理，对于游客，仅展示文章以及简略的作者信息，可以通过昵称、密码进行注册或登录，通过手机号、邮箱可以辅助验证
* 文章管理，已登录的用户可以发表文章，仅支持文字，发布文章时可以带上标签，发布后文章标题、时间、作者、内容（前几行）会出现在个人主页
* 登录用户可以为他人文章点赞收藏和评论，评论按楼层显示，也可以关注其他用户，对于收藏功能，用户可以新建收藏夹（支持一级）

## 数据模型与表结构设计
* 确定哪些实体以及各个实体的属性，确定每个实体的关键字，再确定实体间的联系，考虑参与联系的实体是一对一、一对多还是多对多的，是否是部分参与联系等等，表设计尽量按数据库设计范式来设计，使用power designer工具辅助设计，采用crow's foot方法表示ER模型
* 文章
    ```sql
    create table blog_passage
    (
    passage_id           int(9) zerofill not null auto_increment,
    user_id              int(8) not null,
    passage_title        char(30) not null,
    public_date          date,
    passage_content      text,
    applause_counts      int,
    comments_count       int,
    collection_count     int,
    primary key (passage_id)
    ) auto_increment=100110001;
    ```
* 用户
    ```sql
    create table blog_user
    (
    user_id              int(8) zerofill not null auto_increment,
    nick_name            char(16),
    password             text,
    gender               char(1),
    reg_date             date,
    phone_num            char(11),
    mail_addr            char(25),
    birthday             date,
    state                char(1),
    primary key (user_id)
    )auto_increment=10010001;
    ```
* 评论
    ```sql
    create table comments
    (
    comment_id           int(9) zerofill not null auto_increment,
    passage_id           int(9) not null,
    user_id              int(8) not null,
    parent_id            int(9),
    comment_apcnt        int,
    comment_date         date,
    comment_content      text,
    primary key (comment_id)
    )auto_increment=101100110;
    ```
* 联系: 用户发布文章、用户关注另一个用户、用户在某一文章下进行评论、用户回复了另一用户的评论、用户喜欢或收藏了某一篇文章

## 其他
* 此外还实现了按用户或文章标题检索的功能，首页展示评论、点赞、收藏数较多的几篇文章
