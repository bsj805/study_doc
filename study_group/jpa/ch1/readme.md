# 1 JPA 소개

`SQL Mapper`를 사용하더라도, 코드와 `SQL` 사이의 의존성을 떼내기 어려웠고, 객체와 관계형 데이터베이스의 차이들 때문에 SQL문을 더더욱 많이 작성하게 된다.

# 1.1 SQL을 직접 다룰 때 발생하는 문제점

JAVA application은 JDBC API를 통해 SQL문을 전달하고, DB는 그 결과를 JDBC API를 통해 반환하게 
 
## 1.1.1 반복, 반복 그리고 반복
 이를테면 회원 객체 하나 저장하려면 `INSERT INTO MEMBER(member_id, name, email ...) VALUES(...)`
1.  SQL 작성
2.  회원객체 하나별로 `member.getMemberId()`, `member.getName()` ... 이런식으로 쭉 써야하고,
3.  마지막에 `JDBC API`를 통해 SQL까지 실행해야 한다.

근데, 객체를 메모리에 저장한다고 하면, list.add(member); 하나로 간편하게 저장되지 않는가? 

## 1.1.2 SQL에 의존적인 개발

원래 `member_id`, `name` , `email` 만 저장했다가 `password` column이 추가되야 한다면 어떻게 되는가? 
1. SQL문 변경
2. 회원객체에서 `member.getPassword()`도 insert문에 들어가게 수정
3. 회원객체의 연락처 값을 꺼내서 등록 SQL에 전달한다.

어휴, 이 `Member`객체와 관련된 모든 `SQL`문을 찾아다니면서 수정해야 한다.
근데 만약 메모리에 객체를 저장한다면, `list.add(member)` 이렇게 된 상태에서, `member.setPW()` 만 하면 ㄷ끝이다.

또, 에러가 나면 어떤 문제인지 각 SQL문을 DAO를 열어서 확인해야 깨닫는다. 이렇게 DAO를 두어서 `encapsulation`하려고 해도, 결국 `SQL`문을 신뢰할 수 없어, 다시 들여다 보게 된다.

- 진정한 의미의 계층 분할이 어렵다.
- 엔티티를 신뢰할 수 없다(DAO가 100% 맞는 객체만을 만들어서 반환해주지 않아)
- SQL에 의존적인 개발을 피하기 어렵다

## 1.1.3 JPA와 문제 해결

JPA는 객체를 컬렉션에 저장하듯 `jpa.persist(member)`과 같이 객체를 저장할 수 있게 한다. 
JPA가 객체와 매핑정보를 보고 적절한 SQL문을 생성한다.

SELECT: `Member member = jpa.find(Member.class, 15)` 와 같이 객체에 대한 조회가 가능
UPDATE: `Member member = jpa.find(Member.class, 15)` 후에, `member.setName("이름변경")` 이런식으로 수정가능

연관된 객체 조회도,

`Member member = jpa.find(Member.class, 15)`
`Team team = member.getTeam()`

우리가 굳이 member.foreignKey이름() 식의 메서드를 불러서 key를 가져와 TEAM을 다시 조회할 필요가 없다.


# 1.2 패러다임의 불일치


객체는 속성(필드)와 기능(메서드)를 가진다.
그러니 속성을 죄다 DB에 저장해버리면 되는 것 아닌가 생각하지만, 상속을 받아 더 많은 속성을 가진다거나, 다른 객체를 속성으로 가진다면 어려워진다.

그럼 `serialize`해서 파일로 저장하는 직렬화는 어떠한가? 이런 객체는 속성에 대한 검색이 불가능하다.
DB저장할 때 발생하는 문제는 추상화, 상속, 다형성 개념이 없다는 것이다. 결국 개발자가 이런 문제들을 해결하는데 시간을 쓰게 된다.

## 1.2.1 상속

테이블엔 상속이 없다. 대신 `supertype`과 `subtype` 관계가 있다. 이를테면 `TYPE`이라는 칼럼을 두어서 `CAT` `DOG` `TIGER` 등을 지정할 수 있다.
그럼 상속과 비슷하다.

`ANIMAL`을 상속한 `CAT` 객체를 저장해보자. 
`jpa.persist(cat)` 하면, `ANIMAL` 테이블, `CAT` 테이블 두 곳에 객체를 저장해둔다.
그래서 `ANIMAL`에서 조회해도 우리는 `cat`을 돌려빧을 수 있다.

JPA가 `CAT`과 `ANIMAL` 두 테이블을 조인해서 필요한 데이터를 조회하고 결과를 반환한다.

```sql
select C.*, A.*
    FROM CAT C
    JOIN ANIMAL A ON C.cat_id = animal_id
```

## 1.2.2 연관관계

객체는 참조를 사용해서 다른 객체와 연관관계를 가지지만, 테이블은 외래 키를 사용해서 조인을 사용해 연관 테이블을 조회한다.

*실제 테이블처럼 객체가 참조가 아닌 FK 를 가지도록 클래스를 설계하면 어떻게 될까?*

근데 이렇게되면 `Team team = memberList.getTeam(member.getFK이름())` 이 모양이되고, 사실 참조를 보관하는 것이 맞다.
이런식으로 하게되면 객체지향의 특징을 잃어버리게 된다.

즉, 객체 모델은 외래 키가 아니라 참조값을 가져야 하고, 개발자가 테이블이 FK를 써서 참조를 찾을 수 있도록 번역하는 과정을 해주어야 한다.
`member.getTeam().getId()` 이게 외래키가 되어주는 방식이 되야 한다.

JPA는 이 불일치 문제를
```java
member.setTeam(team)
jpa.persist(member);
```
이런식으로 해결한다. 연관관계를 설정하고 저장을 해서 JPA가 team의 참조를 외래 키로 변환해서 적절한 INSERT 를 수행하도록 하고,
`Member member = jpa.find(Member.class, memberId)`
`Team team = member.getTeam()` 이런식으로 객체를 찾게 된다.


## 1.2.3 객체 그래프 탐색

근데 연관관계와 관련해 극복하기 어려운 패러다임의 불일치도 있다.
참조를 사용해서 다른 객체들을 찾아나가는 것을 객체 그래프 탐색이라고 한다.
객체라면 모름지기 객체 그래프를 마음껏 탐색할 수 있어야 하는데, SQL을 직접 다루면 처음 실행하는 SQL문의 `SELECT` 범위에 따라서 객체 그래프를 어디까지 탐색하는지 정해지게 된다.
근데 매번 `SELECT *`으로 가져오면 메모리의 낭비다. 

`JPA와 객체 그래프 탐색`
JPA를 사용하면 객체 그래프를 마음껏 탐색할 수 있다. 
연관된 객체를 사용하는 시점에 적절한 SQL를 실행하게 된다.

`지연 로딩`이라고 한다. 실제 사용할 때 까지 조회를 미룬다. 이건 config로 설정할 수 있다.


## 1.2.4 비교

DB는 기본 키 값을 이용해 각 row를 구분하고, 객체는 
* identity 비교:  == 비교 -> 객체 인스턴스의 주소값 비교
* equals()비교: equals()메서드로 객체 내부의 값을 비교

JDBC에서

`var a= member.getMember(1)`
`var b= member.getMember(1)`
a == b 는 false가 나온다.

이런 패러다임의 불일치를 해결하려고 같은 인스턴스가 리턴되게 만들면, 문제는 더 어렵다. - JPA는 같은 트랜잭션일 때 같은 객체가 조회되는 것을 보장한다.
즉, 같은 트랜잭션이라면
`var a= member.getMember(1)`
`var b= member.getMember(1)`
a == b 는 true가 나온다.


## 1.2.5 정리
패러다임의 불일치 해결

# 1.3 JPA란 무엇인가?

JPA(JAVA PERSISTENCE API) 는 자바 진영의 ORM 기술 표준이다. JPA는 어플리케이션과 JDBC 사이에서 동작한다.
ORM이란, Object-Relational Mapping이다. 객체와 관계형 데이터베이스를 매핑한다는 뜻이다.

자바 객체를 PERSIST하는 순간
- Entity 분석
- INSERT SQL 생성
- JDBC API 사용
- 패러다임 불일치 해결 ( 뭐 join할 key가 필요하면 select 해오는 둥)

자바 객체 조회
- SELECT SQL 생성
- JDBC API 사용
- ResultSet 매핑 (기존 JDBC에서 사용되던 result 받아오는 클래스)
- 패러다임 불일치 해결 (다른 객체의 참조 정보까지 필요하면 같이 가져오기. ex. primary key of foreign key 로 해당 객체 참조할 수 있게 (객체 그래프 탐색) )

Hibernate는 ORM 프레임워크로, 패러다임 불일치를 대부분 해결하는 성숙한 프레임워크이다.


## 1.3.1 JPA 소개

자바 진영에서 사용하던 EJB 기술표준안에 엔티티 빈이라는 ORM 기술도 있었다. 너부 복잡하고, 기술 성숙도도 떨어졌으며, 자바 엔터프라이즈 서버에서만 동작.
Hibernate를 기반으로 새로 자바 ORM 기술 표준이 만들어진 게 JPA.

JPA는 자바 ORM 기술에 대한 API 표준 명세
- 여러 인터페이스를 모아둔 것.

## 1.3.2 왜 JPA를 사용해야 하는가?
생산성
- SQL을 개발자가 직접 안 써도 된다.
- DDL문을 자동으로 생성해주는 기능 ( 테이블 자동 생성,제거,변경)
- 객체 중심 설계 가능 ( DB를 따라가는 객체 설계를 하지 않아도 됨)

유지보수
- 클래스 (객체)의 변경이 있다면 많은 부분의 수정이 필요했었음 -> 유지보수 좋음
- Entity가 어떤 것을 가져오는지 100% 확실함 -> DAO에서 리턴해주는 객체를 믿을 수 있음.

패러다임의 불일치 해결
- 테이블은 객체 참조나, 상속같은 게 없어서 비교, 객체 그래프 탐색이 문제임. 이걸 최대한 해결해준다.

성능
- 같은 객체에 대한 조회를 lazy loading으로 한번만에 처리할 수 있다.
- SQL 힌트를 넣을 수도 있다.

데이터 접근 추상화와 벤더 독립성
- 한 계층의 추상화가 더해졌으니 DB를 변경하기 쉽다. 
- 개발환경과 실제 환경의 DB를 다르게 할 수 있다. (? 무슨 문제를 일으키려고 ...)

표준
- 이를테면 mysql의 모든 칼럼 명이 snake_case라는 것을 알고 있기 때문에 우리가 모든 칼럼 명을 MyName 은 my_name 칼럼을 찾아본다 로 해석할 수 있는 것처럼,
표준 인터페이스를 따른다는 것은 나중에 더 나은 어플리케이션이 표준이 되어도 쉽게 변경할 수 있게 된다.

## 1.4 정리
JPA 패러다임 불일치, 객체와 테이블의 차이, 어떻게 해결하는지에 대한 설명이 있었다.

JPA를 사용해보자.
