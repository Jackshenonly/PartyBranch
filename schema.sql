drop table if exists communists;
create table communists (
  id int primary key not null AUTO_INCREMENT,
  depart varchar(50) not null,
  name varchar(10) not null,
  sex varchar(2) not null,
  major varchar(20) not null,
  status varchar(20) not null,
  score double default 0,
  count double default 0,
  average double default 0 
);



drop table if exists user;
create table user(
  id int primary key not null AUTO_INCREMENT,
  no varchar(10) not null,
  name varchar(10) null,
  password varchar(20) null,
  nickname varchar(20) default null,
  sex varchar(2)  default null,
  major varchar(20) default null,
  admin bit default 0,
  sadmin bit default 0
);
insert into user(no) values ('1212300104');
insert into user(no) values ('1212300105');
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
insert into user(no,admin,sadmin) values ('jackshen',1,1);

update user set password = no;
update user set nickname = no;

drop table if exists comments;
create table comments(
  id int primary key not null AUTO_INCREMENT,
  name varchar(10) not null,
  nickname varchar(20) not null,
  cname varchar(10) not null,
  score double not null,
  date datetime not null,
  text varchar(200) not null
  
);
drop table if exists performance;
create table performance(
  id int primary key not null AUTO_INCREMENT,
  no varchar(20) default 'jackshen',
  depart varchar(50) default 'jackshen',
  mm1 double  not null,
  mm2 double  not null,
  mm3 double  not null,
  mm4 double  not null,
  mm5 double  not null
  
);
insert into performance(mm1,mm2,mm3,mm4,mm5) values (20,20,20,20,20);

drop table if exists announcement;
create table announcement(
  id int primary key not null AUTO_INCREMENT,
  date datetime not null,
  author varchar(20) not null,
  title varchar(100) not null,
  text text not null
);
insert into announcement(date,author,title,text) values('2015-04-01 11:00:00','jackshen','this is a test','jack jack jackshen test the announcement!');
insert into announcement(date,author,title,text) values('2015-03-01 12:00:00','jackshen','this is a test222','22222222222222222222222222222222222');