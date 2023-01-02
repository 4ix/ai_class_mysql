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