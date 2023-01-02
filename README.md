# mysql_python
## 2023-01-02(월)
1. mysql 접속
```
mysql -u root -p
```
2. 데이터베이스 생성
```
create databse shopdb;
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