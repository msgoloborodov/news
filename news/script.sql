create table category (
  id number,
  title varchar2(255)
);

create table news (
  id number,
  id_category (38,0) number,
  title varchar2(255),
  anons varchar2(1024),
  body clob,
  image varchar2(255)
);

alter table news
add constraint f_category_id foreign key (id_category)
references category (id) on delete cascade;

alter table news
add constraint f_user_id foreign key (id_user)
references auth_user (id) on delete cascade;    
    
    
    
    