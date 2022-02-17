trigger_com_appcnt = """
create trigger com_appcnt
after insert on comment_applause
for each row
begin
    update comments
    set comments.comment_apcnt = comments.comment_apcnt + 1
    where comments.comment_id = new.comment_id;
end
"""
trigger_update_pascomcnt = """
create trigger update_pascomcnt
after insert on comments
for each row
begin
    update blog_passage
    set comments_count = comments_count + 1
    where blog_passage.passage_id = new.passage_id;
end
"""
trigger_passage_appcnt = """
create trigger passage_appcnt
after insert on passage_applause
for each row
begin
    update blog_passage
    set blog_passage.applause_counts = blog_passage.applause_counts + 1
    where blog_passage.passage_id = new.passage_id;
end
"""
trigger_upd_comappcnt = """
create trigger upd_comappcnt
after update on comment_applause
for each row
begin
    update comments
    set comment_apcnt = comment_apcnt + (new.ap_status - old.ap_status)
    where comments.comment_id = new.comment_id;
end
"""
trigger_upd_pasappcnt = """
create trigger upd_pasappcnt
after update on passage_applause
for each row
begin
    update blog_passage
    set blog_passage.applause_counts = blog_passage.applause_counts + (new.ap_status - old.ap_status)
    where blog_passage.passage_id = new.passage_id;
end
"""
trigger_delcom = """
create trigger delcom
after delete on comments
for each row
begin
    update blog_passage
    set blog_passage.comments_count = blog_passage.comments_count - 1
    where blog_passage.passage_id=old.passage_id;
end
"""
trigger_default_collector = """
create trigger default_collector
after insert on blog_user
for each row
begin
    insert into collector values(new.user_id, '001', '默认收藏夹');
end
"""
trigger_ins_cp = """
create trigger ins_cp
after insert on collector_passages
for each row
begin
    update blog_passage
    set collection_count = collection_count + 1
    where blog_passage.passage_id = new.passage_id;
end
"""
trigger_del_cp = """
create trigger del_cp
after delete on collector_passages
for each row
begin
    update blog_passage
    set collection_count = collection_count - 1
    where blog_passage.passage_id = old.passage_id;
end
"""
