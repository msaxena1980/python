use eduai;

select * from chathistory;
select * from content_block_feedback;

select * from session_model_switch;
select * from session_progress;
select * from student;

delete from chathistory where id < 1000;
delete from content_block_feedback where id < 1000;
delete from session_model_switch where id < 1000;
delete from session_progress where id < 1000;
delete from student where id < 1000;





