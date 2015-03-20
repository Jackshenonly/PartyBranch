drop table if exists communists;
create table communists (
  id integer primary key autoincrement,
  depart string not null,
  name string not null,
  sex string not null,
  major string not null,
  status string not null,
  score REAL default 0,
  count REAL default 0,
  average REAL default 0 
);
insert into  communists(major,name,sex,depart,status) values ('计科12A','申太良','男','计信学生二支部（计科专业）','正式党员');
insert into  communists(major,name,sex,depart,status) values ('计科1201','郑卜毅','男','计信学生二支部（计科专业）','正式党员');
insert into  communists(major,name,sex,depart,status) values ('计科1201','郑幸','男','计信学生二支部（计科专业)','正式党员');
insert into  communists(major,name,sex,depart,status) values ('计科1201','张建','男','计信学生二支部（计科专业)','预备党员');
insert into  communists(major,name,sex,depart,status) values ('计科1201','周奎君','男','计信学生二支部（计科专业)','预备党员');
insert into  communists(major,name,sex,depart,status) values ('计科12A','林豪','男','计信学生二支部（计科专业）','预备党员');
insert into  communists(major,name,sex,depart,status) values ('计科1201','陈珊珊','女','计信学生二支部（计科专业)','预备党员');
insert into  communists(major,name,sex,depart,status) values ('计科1201','邱园','女','计信学生二支部（计科专业)','预备党员');
insert into  communists(major,name,sex,depart,status) values ('计科12A','项美康','女','计信学生二支部（计科专业)','预备党员');
insert into  communists(major,name,sex,depart,status) values ('计科12A','王蓓蓓','女','计信学生二支部（计科专业)','预备党员');
insert into  communists(major,name,sex,depart,status) values ('计科1301','毕嘉妮','女','计信学生二支部（计科专业)','预备党员');
insert into  communists(major,name,sex,depart,status) values ('计科1301','冯诗文','女','计信学生二支部（计科专业)','预备党员');
insert into  communists(major,name,sex,depart,status) values ('计科1301','沈慕','男','计信学生二支部（计科专业)','预备党员');

drop table if exists user;
create table user(
  id integer primary key autoincrement,
  no string not null,
  name string null,
  password string null,
  nickname string default null,
  sex string  default null,
  major string default null
);
insert into user(no) values ('1212300110');
insert into user(no) values ('1212300113');
insert into user(no) values ('1212300114');
insert into user(no) values ('1212300116');
insert into user(no) values ('1212300117');
insert into user(no) values ('1212300118');
insert into user(no) values ('1212300119');
insert into user(no) values ('1212300121');
insert into user(no) values ('1212300123');
insert into user(no) values ('1212300126');
insert into user(no) values ('1212300127');
insert into user(no) values ('1212300128');
insert into user(no) values ('1212300129');
insert into user(no) values ('1212300130');
insert into user(no) values ('1212300202');
insert into user(no) values ('1212300205');
insert into user(no) values ('1212300206');
insert into user(no) values ('1212300208');
insert into user(no) values ('1212300219');
insert into user(no) values ('1212300223');
insert into user(no) values ('1212300225');
insert into user(no) values ('1212300234');
insert into user(no) values ('1212800202');
insert into user(no) values ('jackshen');

update user set password = no;

drop table if exists comments;
create table comments(
  id integer primary key autoincrement,
  name string not null,
  cname string not null,
  score REAL not null,
  date string not null,
  text string not null
  
);
drop table if exists performance;
create table performance(
  id integer primary key autoincrement,
  mm1 REAL  not null,
  mm2 REAL  not null,
  mm3 REAL  not null,
  mm4 REAL  not null,
  mm5 REAL  not null
  
);
insert into performance(mm1,mm2,mm3,mm4,mm5) values (20,20,20,20,20);