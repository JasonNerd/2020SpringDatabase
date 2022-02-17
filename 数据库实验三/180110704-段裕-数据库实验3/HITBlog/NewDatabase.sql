drop trigger if exists com_appcnt;
drop trigger if exists update_pascomcnt;
drop trigger if exists passage_appcnt;
drop trigger if exists upd_comappcnt;
drop trigger if exists upd_pasappcnt;
drop trigger if exists delcom;
drop trigger if exists default_collector;
drop trigger if exists del_cp;
drop trigger if exists ins_cp;

drop  table  if   exists   user_blogs_info;
drop  table  if   exists   query_user_base_info;
drop  table  if   exists   blog_passage;
drop  table  if   exists   blog_user;
drop  table  if   exists   passage_labels;
drop  table  if   exists   passage_label;
drop  table  if   exists   passage_applause;
drop  table  if   exists   concern;
drop  table  if   exists   collector;
drop  table  if   exists   collector_passages;
drop  table  if   exists   comment_applause;
drop  table  if   exists   comments;
create table Collector
(
   user_id              int(8) not null,
   collector_id         tinyint(3) not null,
   collector_name       char(20)
);
alter table Collector comment '用户的收藏夹
一个确定的收藏夹
由用户ID和收藏夹ID组成
同时仅允许创建一级收藏夹';
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
alter table blog_passage comment '博客文章';
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
alter table blog_user comment '博客账号主体';
create table collector_passages
(
   user_id              int(8) not null,
   collector_id         tinyint(3) not null,
   passage_id           int(9) not null
);
create table comment_applause
(
   comment_id           int(9) not null,
   user_id              int(8) not null,
   ap_date              date,
   ap_status            char(1)
);
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
create table concern
(
   concern_date         date,
   from_user_id         int(8) not null,
   to_user_id           int(8) not null
);
alter table concern comment '不同的用户间可以互相关注';
create table passage_applause
(
   passage_id           int(9) not null,
   user_id              int(8) not null,
   passage_ap_date      date,
   ap_status            char(1)
);
create table passage_label
(
   label_id             char(4) not null,
   label_name           char(30),
   primary key (label_id)
);
alter table passage_label comment '文章标签';
create table passage_labels
(
   label_id             char(4) not null,
   passage_id           char(12) not null,
   primary key (label_id, passage_id)
);
alter table passage_labels comment '一篇文章至少有一个标签
一个标签下也会有0到多篇文章';
create  VIEW      query_user_base_info  as select blog_user.user_id, blog_user.nick_name, blog_user.gender, blog_user.reg_date, blog_user.mail_addr, blog_user.birthday, blog_user.phone_num
                                           from blog_user;
create  VIEW      user_blogs_info  as select bp.user_id, SUM(bp.applause_counts) as apcnt, SUM(bp.comments_count) as cocnt, COUNT(*) as pacnt
                                      from blog_passage bp
                                      group by bp.user_id;
alter table Collector add constraint FK_user_collector foreign key (user_id)
      references blog_user (user_id) on delete restrict on update restrict;
alter table blog_passage add constraint FK_passage_distribute foreign key (user_id)
      references blog_user (user_id) on delete restrict on update restrict;
alter table comment_applause add constraint FK_comment_applause foreign key (comment_id)
      references comments (comment_id) on delete restrict on update restrict;
alter table comment_applause add constraint FK_user_comap foreign key (user_id)
      references blog_user (user_id) on delete restrict on update restrict;
alter table comments add constraint FK_passsage_comments foreign key (passage_id)
      references blog_passage (passage_id) on delete restrict on update restrict;
alter table comments add constraint FK_user_comments foreign key (user_id)
      references blog_user (user_id) on delete restrict on update restrict;
alter table passage_applause add constraint FK_applause_passage foreign key (passage_id)
      references blog_passage (passage_id) on delete restrict on update restrict;
alter table passage_applause add constraint FK_user_pasap foreign key (user_id)
      references blog_user (user_id) on delete restrict on update restrict;
alter table passage_labels add constraint FK_passage_labels foreign key (label_id)
      references passage_label (label_id) on delete restrict on update restrict;
alter table passage_labels add constraint FK_passage_labels2 foreign key (passage_id)
      references blog_passage (passage_id) on delete restrict on update restrict;
insert into passage_label values('0001', '技术');
insert into passage_label values('0002', '校园');
insert into passage_label values('0003', '数学');
insert into passage_label values('0004', '解题');
insert into passage_label values('0005', '生活');
insert into passage_label values('0006', '杂感');
insert into passage_label values('0007', '面试');
insert into passage_label values('0008', '考研');
insert into passage_label values('0009', '实验');
insert into passage_label values('0010', '运动');
insert into passage_label values('0011', '安利');
insert into passage_label values('0012', '历史');
insert into passage_label values('0013', '时事');
insert into passage_label values('0014', '游戏');
insert into passage_label values('0015', '影评');
insert into passage_label values('0016', '音乐');
insert into passage_label values('0017', '穿搭');
insert into passage_label values('0018', '手工');
insert into passage_label values('0019', '美妆');
insert into passage_label values('0020', '日记');
insert into passage_label values('0021', '吐槽');
insert into passage_label values('0022', '食堂');
insert into passage_label values('0023', '茶馆');