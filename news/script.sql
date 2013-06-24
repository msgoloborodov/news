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

create unique index i_category_title on category (title);

create sequence category_sequence minvalue -1 maxvalue 9999999999999999999999999999 increment by 1;
create sequence news_sequence minvalue -1 maxvalue 9999999999999999999999999999 increment by 1;

create or replace trigger T_BI_CATEGORY before
  insert on category for each row declare curr_val number;
  diff_val number;
  pragma AUTONOMOUS_TRANSACTION;
  begin
    if :new.id is not null then
      execute immediate 'SELECT category_sequence.nextval FROM dual' into curr_val;
      diff_val    := :new.id - curr_val - 1;
      if diff_val != 0 then
        execute immediate 'alter sequence category_sequence increment by '|| diff_val;
        execute immediate 'SELECT category_sequence.nextval FROM dual' into curr_val;
        execute immediate 'alter sequence category_sequence increment by 1';
      end if;
    end if;
    select category_sequence.nextval into :new.id from dual;
  end;
  /
  
create or replace trigger t_bi_news before
  insert on news for each row declare curr_val number;
  diff_val number;
  pragma autonomous_transaction;
  begin
    if :new.id is not null then
      execute immediate 'SELECT news_sequence.nextval FROM dual' into curr_val;
      diff_val    := :new.id - curr_val - 1;
      if diff_val != 0 then
        execute immediate 'alter sequence news_sequence increment by '|| diff_val;
        execute immediate 'SELECT news_sequence.nextval FROM dual' into curr_val;
        execute immediate 'alter sequence news_sequence increment by 1';
      end if;
    end if;
    select news_sequence.nextval into :new.id from dual;
  end;
  /
    