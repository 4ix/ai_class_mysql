# mysql_python
## 2023-01-06(금)
1. flask 실습

## 2023-01-05(목)
1. 조인
- 사용자 테이블과 구매 테이블의 userID가 같은거 기준으로
```
select * from buytbl join usertbl on buytbl.userID = usertbl.userID;
```

- natural join: 양쪽 테이블의 같은 컬럼명을 inner join의 결과로 검색
```
select * from buytbl natural join usertbl;
select u.name, b.prodName, b.price, b.amount from usertbl u natural join buytbl b;
select u.name, prodName, sum(amount*1000) from usertbl u natural join buytbl b group by name, prodName;
```

- 2개 이상의 테이블 조인
```
select stdName, clubName, roomNo from stdtbl s join stdclubtbl sc using (stdName) join clubtbl c using(clubName);
```

- 크로스 조인: 두 개의 테이블을 조인 조건 없이 결합
```
select * from stdtbl cross join clubtbl;
```

- outer join: 조건에 만족되지 않는 행도 출력
```
select * from stdtbl s left outer join stdclubtbl sc using (stdName) left outer join clubtbl c using(clubName);
select * from stdtbl s right outer join stdclubtbl sc using (stdName) right outer join clubtbl c using(clubName);
```

2. exists 를 활용해서 존재 여부만 판단
```
select userid ID, u.name 이름, u.addr 주소 from usertbl u where exists (select 1 from buytbl where userid = u.userID);
```

3. 데이터베이스 삭제
```
drop database if exists shopdb1;
```

4. 데이터베이스 생성
```
create database tabledb;
```

5. 테이블 생성
```
create table usertbl(userID char(8) not null primary key, name varchar(10) not null, birthYear int, addr char(2), mobile1 char(3), mobile2 char(8), height smallint, mDate date);
create table buytbl(num int not null auto_increment primary key, userID char(8) not null, prodName char(6) not null, groupName char(4) null, price int not null, amount smallint not null, foreign key(userID) references usertbl(userID));
```

6. 테이블 수정
- 생성된 테이블에 primary key 추가
```
alter table prodtbl add constraint prodtbl_code_id_pk primary key(prodcode, prodid);
```
- 테이블명 변경
```
rename table prodtbl to newprod;
```

## 2023-01-04(수)
1. 관계 연산자의 사용
- and (둘다 true인 경우)
```
select userID, name, birthYear, height from usertbl where birthYear >= 1970 and height >= 182;
```

- 170과 180 사이(값 포함)
```
select userID, name 이름, height from usertbl where height between 170 and 180;
```

- or (둘중 하나가 true인 경우)
```
select name, addr from usertbl where addr = '경남' or addr = '전남' or addr ='경북';
```

- 컬럼명이 같고 or와 같은 경우 in 사용
```
select name, addr from usertbl where addr in ('경남','전남','경북');
```

- 시작이 김으로 시작하는 경우
```
select name, height from usertbl where name like '김%';
```

- 마지막이 우로 끝나는 경우
```
select name, height from usertbl where name like '%우';
```

- 김으로 시작하고 나머지가 두글자인 경우
```
select name, height from usertbl where name like '김__';
```

- subquery
```
select name, height from usertbl where height > (select height from usertbl where name = '김경호');
```

- 평균 구해서 적용
```
select name, height from usertbl where height < (select avg(height) from usertbl);
```

- 부등호(또는 =) any 검색된 값들 중에 하나라도 true 이면
```
select name, height, addr from usertbl where height >= any(select height from usertbl where addr = '경남');
```

- 부등호(또는 =) all 검색된 모든 값들을 비교해서 true 이면
```
select name, height, addr from usertbl where height >= all(select height from usertbl where addr = '경남');
```

2. order by 절(키를 기준으로 내림차순 정렬(desc 입력))
```
select name 이름, height 키 from usertbl order by height desc, 1;
```

3. 중복을 제거하고 하나만 출력(distinct)
```
select distinct(addr) from usertbl;
```

4. 출력하는 개수를 제한(limit)
- 입사일자가 빠른 5명만 출력
```
select emp_no 사번, birth_date 생일, hire_date 입사일자 from employees.employees order by hire_date limit 5;
```
- limit 0,10 (0부터 10개 출력)
```
select emp_no 사번, birth_date 생일, hire_date 입사일자 from employees.employees order by hire_date limit 0,10;
```

5. 테이블 생성 관련
- 기존의 테이블을 복사해서 새로운 테이블 생성
```
create table new_buytbl (select * from buytbl);
```
- 기존 테이블의 구조만 복사, 데이터는 복사하지 않음
```
create table new_buytbl (select * from buytbl where 1 = 2);
```
- 새로운 컬럼명 부여하면서 생성
```
create table new1_buytbl (select userID 사용자, prodName 제품명 from buytbl);
```

6. group by 절(그룹으로 묶어주는 역할)
- 각 사용자 별로 구매한 개수를 합쳐 출력
```
select userID as '유저 아이디', sum(amount) as '총 구매 개수' from buytbl group by userId;
```
[그룹바이] (https://velog.io/@devjooj/MySQL-EP-1.-GROUP-BY).

- 소수점 첫째자리 까지만 남기고 버림
```
select userid, truncate(avg(amount),1) from buytbl group by userid;
```

- 가장 큰 키와 가장 작은 키를 가진 사람 출력
```
select name, height from usertbl where height = (select max(height) from usertbl) or height = (select min(height) from usertbl);
```

- having 그룹에 대한 조건식
```
select userid, sum(amount*1000) '총 구매액' from buytbl group by userid having sum(amount*1000) >= 4000;
```

- 그룹별, num 별 총 구매액, 소계 및 총계 구하기(with rollup)
```
select groupname, num, sum(amount*1000) from buytbl group by groupname, num with rollup
```

7. 테이블 삭제
```
drop table new1_buytbl;
```

8. 데이터 추가
```
insert into testtbl1(id, username, age) values(1, '홍길동', 25);
insert into testtbl1(id, username) values(2, '김철수');
INSERT INTO testTbl1(userName, age, id) VALUES ('하니', 26,  3);

```

9. auto increment
- 테이블 생성
```
CREATE TABLE testTbl2 
  (id  int AUTO_INCREMENT PRIMARY KEY, 
   userName char(3), 
   age int );
```

- 데이터 추가
```
INSERT INTO testTbl2 VALUES (NULL, '지민', 25);
INSERT INTO testTbl2 VALUES (NULL, '유나', 22);
INSERT INTO testTbl2 VALUES (NULL, '유경', 21);
```

- 마지막 순번 확인
```
select last_insert_id();
```

- 시작 순번을 변경하고자 할 경우
```
alter table testtbl2 auto_increment = 100;
```

- auto_increment 증가값 설정
```
CREATE TABLE testTbl3 
  (id  int AUTO_INCREMENT PRIMARY KEY, 
   userName char(3), 
   age int );
ALTER TABLE testTbl3 AUTO_INCREMENT=1000;
SET @@auto_increment_increment=3;
```

```
insert into testtbl3(username, age) values('나연',20),('정연',18),('모모',19);
```

- 대량의 데이터 입력
```
INSERT INTO testTbl4 
  SELECT emp_no, first_name, last_name
    FROM employees.employees ;
```

10. 데이터 삭제
```
delete from testtbl4 where fname = 'Aamer';
```
```
delete from testtbl4 where fname = 'Aamer' limit 5;
```

11. 프라이머리 키 지정
```
alter table membertbl add constraint pk_membertbl primary key (userid);
```

12. 조건부 insert
- ignore (에러가 났다는거를 단순 표현, 키가 중복일 경우 그 다음 명령으로 넘어감)
```
insert ignore into membertbl values('BBK', '비비코','미국');
```

- on duplicate key (중복이 나면 업데이트를 해라)
```
insert into membertbl values('BBK','비비코','미국') on duplicate key update name='비비코', addr='미국';
insert into membertbl values('DJM','동짜몽','일본') on duplicate key update name='동짜몽', addr='일본';
```

13. 변수
- 선언
```
set @var1 = 'test';
```

- 호출
```
select @var1;
```

14. 데이터 형식 변환 함수
- 실수를 정수형으로
```
select cast(avg(amount) as signed integer) '평균구매개수' from buytbl;
select convert(avg(amount), signed integer) '평균구매개수' from buytbl;
```

- 문자를 날짜형으로
```
select cast('20230101' as date);
```

15. null 데이터 찾기
```
select * from buytbl where groupName is null;
```

16. 조건문(if)
```
select if (100>200, '참이다','거짓이다');
select if (groupname is not null, groupname,'자료없음') from buytbl;
select ifnull (groupname, '자료없음');
select ifnull(groupname, '자료없음') groupname, sum(amount) from buytbl group by 1;
```

## 2023-01-03(화)
1. 테이블 명 확인
```
show tables;
```
2. 테이블의 컬럼명 조회
```
desc employees;
```
3. first_name 이름, gender 성별, hire_date 회사 입사일로 출력
```
select first_name as 이름, gender as 성별, hire_date as '회사 입사일' from employees;
```

4. autocommit 상태 확인 (1이 기본값, autocommit을 하겠다.)
```
SELECT @@AUTOCOMMIT;
```

## 2023-01-02(월)
1. mysql 접속
```
mysql -u root -p
```
2. 데이터베이스 생성
```
create database shopdb;
```
3. 데이터베이스 사용
```
use shopdb;
```
4. 테이블 생성
```
CREATE TABLE `shopdb`.`membertbl` (
  `memberid` CHAR(5) NOT NULL,
  `membername` VARCHAR(20) NOT NULL,
  `memberaddr` VARCHAR(45) NULL,
  PRIMARY KEY (`memberid`));
  ```

5. 행 추가 방법
```
INSERT INTO `shopdb`.`membertbl` (`memberid`, `membername`, `memberaddr`) VALUES ('Dang', '당탕이', '경기 부천시');
```

6. 조회 방법
```
select * from product;
```

```
SELECT * FROM employees.titles;
```

```
select * from membertbl where membername = '지운이';
```

```
select memberid, membername from membertbl where membername = '지운이';
```

7. 기존 테이블에서 데이터 가져온 후 새로운 테이블 생성
```
create table indextbl
select first_name, last_name, hire_date
from employees.employees
limit 500;
```

8. first_name이 'Mary'인 사람의 정보를 출력 -> indextbl에서
```
select * from indextbl
where first_name = 'Mary';
```

```
select * from indextbl
where first_name like 'Ma%';
```

9. index 검색 가능하게 하는 방법
```
create index indextbl_firstname_idx on indextbl(first_name);
```

10. view (가상의 테이블 생성)
```
create view v_member
as select membername, memberaddr from membertbl
where membername = '지운이';
```

11. 프로시저(함수) 만들어서 사용하는 방법
```
DELIMITER //
CREATE PROCEDURE myProc()
BEGIN
    SELECT * FROM memberTBL WHERE memberName = '당탕이' ;
    SELECT * FROM product WHERE productName = '냉장고' ;
END // 
DELIMITER ;
```
```
call myProc();
```

12. 기존의 자료는 가져오지 않고 테이블의 구조만 복사
```
create table deletemember
select * from membertbl
where 1 = 2;
```

13. 트리거(자동으로 행동해줌)
```
DELIMITER //
CREATE TRIGGER trg_deleteMember  -- 트리거 이름
    AFTER DELETE -- 삭제 후에 작동하게 지정
    ON memberTBL  -- 트리거를 부착할 테이블
    FOR EACH ROW -- 각 행마다 적용시킴
BEGIN 
    -- OLD 테이블의 내용을 백업테이블에 삽입
    INSERT INTO deleteMember
        VALUES (OLD.memberID, OLD.memberName, OLD.memberAddr); 
END //
DELIMITER ;
```

14. delete 방법 (데이터 구조는 살리고 내용은 지움)
```
set autocommit = 0;
delete from indextbl;
```

```
rollback;
```

15. truncate (명령어에 대해 DB에 영구 반영, rollback 해도 안먹힘)
```
truncate indextbl;
```