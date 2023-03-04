
# 4장 엔티티 매핑

JPA 사용시 엔티티와 테이블을 매핑하는 것이 중요하다.
4가지의 매핑 어노테이션

* 객체와 테이블 매핑: `@Entity`,`@Table`
* 기본 키 매핑: `@Id`
* 필드와 컬럼 매핑: `@Column`
* 연관관계 매핑: `@ManyToOne`, `@JoinColumn`

# 4.1 `@Entity`

JPA를 사용해서 테이블과 매핑할 클래스는 `@Entity`를 붙인다.
`@Entity`가 붙은 클래스는 JPA가 관리하게 된다.

다른패키지에 이름이 같은 엔티티 클래스가 있다면, 클래스 이름이 default로 `entity` 이름이 되는데, `name` 속성을 바꿔줘야 한다.


`@Entity`의 주의사항
- 기본 생성자는 필수 
- final 클래스, enum, interface, inner 클래스엔 사용불가
- 저장할 필드에 final 사용하면 안됨.

JPA가 엔티티 객체를 사용할 때 기본 생성자를 사용해서, 만약 엔티티 객체에 별도의 생성자를 인위적으로 만들었다면 기본 생성자 `()`<- 이렇게 아무 인자도 안받는 걸 만들어야.

# 4.2 `@Table`

`@Table`은 엔티티와 매핑할 테이블을 지정한다. 

# 4.3 다양한 매핑 사용

회원 테이블의 구조가 수정될 때 각 필드에 이런걸 붙인다. 
- 회원은 일반 회원과 관리자 2개 중 하나인 ENUM => `@Enumerated` 어노테이션
- 회원 가입일, 수정일 칼럼 추가 => `@Temporal`
- 회원 설명, 이라는 길이제한 없는 칼럼 추가 => `VARCHAR` 대신 `CLOB` 타입으로 지정해야. `@Lob`을 사용해서 CLOB, BLOB 타입으로 매핑

# 4.4 데이터베이스 스키마 자동 생성

JPA는 데이터베이스 스키마를 자동으로 생성하는 기능 지원
클래스의 매핑정보 (`@Column`, `@Enumerated` 등) 를 보고 어떤 테이블에 어떤 컬럼을 사용하는지 보고 데이터베이스 스키마 생성.
(DB Dialect가 영향미침)

이 경우 `persistence.xml` ( 데이터 소스 설정 등)에 추가해서 
`hibernate.hbm2ddl.auto` 값을 
- CREATE(테이블을 drop하고 다시 생성) 나 
- UPDATE 등으로 설정해야 한다. (DB 테이블과 엔티티 매핑정보 비교해서 변경 사항 수정)
- 이외에는 DB에 해당 테이블이 없으면 warning을 띄우는 validate (app 실행 안됨)
- Create와 같으나 종료시점에 테이블을 drop하는 테스트용 `create-drop`
이 있다.
  
운영할때는 물론 validate로 설정해두겠지.
- 실제 테이블이나 칼럼이 삭제 되어버릴 수 있다.

`hibernate.show_sql = true` 이걸 추가하면, 콘솔에 실행되는 DDL SQL문을 확인가능.

Enumerated.String 타입으로 지정했던 `회원 타입`은 그냥 VARCHAR로 생성되고 `@Temporal`은 timestamp 타입으로 생성된다.

스키마 자동생성 기능을 사용하면 어플리케이션 실행 시점에 테이블이 생기긴 하나, 개발환경정도에서 사용하자.

## TIP
`hibernate.ejb.naming_strategy`를 사용해서 이름 매핑 전략을 변경할 수 있다.
ex.) 디폴트로 `private String userName` 이라는 필드가 테이블에서는 `user_name`이라는 칼럼으로 저장되게 하려면 `org.hibernate.cfg.ImprovedNamingStrategy`

# 4.5 DDL 생성 기능

회원 이름은 필수로 생성되야 하고, 10자를 초과하면 안된다라는 조건을 걸어보자.
Domain Constraint가 생긴것.

```java
@Column(name = "NAME", nullable= false, length=10 )
private String userName;
```
이러면 not null, length로 `VARCHAR(10)` 인걸 만들 수 있다.

`@Table`의 uniqueConstraints 속성은 유니크 제약을 만들어줄 수 있다.

```java
@Entity
@Table(name="MEMBER", uniqueConstraints = {@UniqueConstaint(name= "name_age_unique",
                                                            columnNmaes={"NAME", "AGE"})}
)
public class Member {

}
```
이렇게 만들면, Name, Age 합쳤을때 unique해야 한다는 제약조건이 생성된다. 
근데 Column의 length나 nullable 을 포함해서 이런 제약조건 기능들은 DDL 자동 생성할때만 영향을 미친다.
그래도 개발자가 entity만 보고도 다양한 제약조건 파악 가능하다는 이점.

# 4.6 기본 키 매핑 (PK mapping)

`@Id` 를 붙이면 PK가 되는 형식이었다. 
* sequence object
* AUTO_INCREMENT

이런 키들을 기본 키로 사용하려면 어떻게 할까?

* 직접 할당: 기본 키를 어플리케이션에서 직접 할당한다.
* 자동 생성: 
  * IDENTITY: 기본 키 생성을 DB에 위임
  * SEQUENCE: 데이터베이스 시퀀스를 이용해 키본 키를 할당한다.
  * TABLE: 키 생성 테이블을 사용한다.
    
데이터베이스 벤더마다 지원하는 방식이 달라서 자동 생성 전략이 다양하다. 
Oracle DB는 sequence를 제공하지만, MySQL은 sequence를 제공안하고, 이런식이니 `IDENTITY`나 `SEQUENCE`는 사용하는 DB에 따라 사용가능.
`TABLE`은 범용적인 솔루션. 
`@Id`에 `@GeneratedValue`를 같이 붙여서 원하는 키 생성 전략을 선택한다. 

## 4.6.1 기본 키 직접 할당 전략

`@Id`만 쓰는 형태.
* 자바 기본형
* String
* java.util.Date
등 어플리케이션에서 객체에 대해 PK를 set해서 저장하는 형태.
```java
Member member = new Member();
member.setId("id1");
em.persist(member);
```
*식별자 값 없이 저장하면 예외가 발생하는데, 어떤 예외가 발생하는지는 JPA 표준에 안 나타난다. JPA 최상위 예외인 javax.persistence.PersistenceException 은 hibernate에서 구현하면서 만들어내는 예외

## 4.6.2 IDENTITY 전략  :기본 키 생성을 DB에 위임

MYSQL의 AUTO_INCREMENT기능 수행하면, ID column 빈 채로 `INSERT`해도 데이터베이스가 순서대로 값을 채운다.
이 경우 값을 저장해야만 기본 키 값이 구해진다. 이 경우, 새로 INSERT 했을 때 기본키 값을 얻어오려고 DB를 추가 조회한다.

```java
Member member = new Member();
em.persist(member);
member.getId();
```
이렇게해도 getId()가 작동하는 것이 PK를 DB를 조회해서 얻어오기 때문.

근데 사실 영속상태가 되려면 식별자가 필요하다. 근데 식별자는 항상 PK를 기준으로하고, 따라서 `em.persist()`를 호출하자마자 DB에 접근해서 PK를 얻어온다.

## 4.6.3 SEQUENCE 전략: 데이터베이스 시퀀스를 이용해 키본 키를 할당한다

DB sequence는 유일한 값을 순서대로 생성하는 DB 오브젝트이다. 
먼저 DB에서 sequence생성이 필요하다.
`CREATE SEQUENCE BOARD_SEQ START WITH 1 INCREMENT BY 1;`

그러면 
```java
@Entity
@SequenceGenerator(
        name = "BOARD_SEQ_GENERATOR",
        sequenceName = "BOARD_SEQ", // 이게 위에서 생성한 SEQ이름
        initialValue = 1, allocationSize = 1) // DDL 생성시 SEQUENCE를 만들게 하기 위함. allocationSize는 시퀀스 한번 호출에 증가하는 수 (default == 50 )? 
// 하나의 memory chunk가 50개의 row인 경우가 많아서, parallel 접근을 하게 되면, 0~49, 50~99 이렇게 할당할 수 있게 된다. INSERT 성능 상의 이점이 있다. 
public class Board{
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE,
                    generator = "BOARD_SEQ_GENERATOR")
    private Long id;
}
```
이렇게하면, id 식별자 값은 DB에서 생성한 `sequence` 생성기를 사용하게 된다. 
내부 동작방식이, em.persist()를 호출할 때 먼저 DB `sequence`를 사용해서 식별자를 조회해서, 엔티티에 식별자를 할당하고,
엔티티를 영속성 컨텐스트를 저장하면, 이제야 트랜잭션을 `commit`해서 `flush`가 일어나면 엔티티를 DB에 저장한다.

`IDENTITY` 가 먼저 커밋해서 저장한다음, 조회를해서 식별자를 얻어오는 것과는 방식이 다르다.

## 4.6.4 TABLE 전략 : 키 생성 테이블을 사용한다.
TABLE 전략은 키 생성 전용 테이블을 하나 만들어서, 이름과 값으로 사용할 칼럼을 만들어 DB 시퀀스를 흉내내는 전략이다.
키 생성용도로 사용할 테이블을 하나 만들어놓고, 위 `@SequenceGenerator`처럼 `@TableGenerator`을 사용한다. 
그럼 얘네가 SEQUENCE같은 거야. `sequence_name`을 찾아서 다음 value를 식별자로 사용할 수 있는 것.
JPA가 `@TableGenerator`로 정한 `pkColumnValue`를 sequence_name으로 INSERT하면서 initial Value가 생긴다.


|sequence_name|next_val|
|------|---|
|BOARD_SEQ|2|
|MEMBER_SEQ|10|

Table을 `UPDATE`하는 쿼리가 추가된다. 기존 SEQUENCE 사용하는 방법보다 sql이 하나 더 있는셈.

## 4.6.5 AUTO전략

AUTO를 하면, DB에 따라서 알아서 세팅한다. 
* IDENTITY, SEQUENCE, TABLE

## 4.6.6 기본 키 매핑

- 엔티티를 영속 상태로 만들 때 식별자 값이 있어야 한다. 

#### 직접 할당 : em.persist() 호출하기 전에 setId() 해주는 것.
#### SEQUENCE: DB SEQUENCE에서 식별자값 획득해 와서 엔티티에 할당, 저장
#### TABLE: DB 테이블에서 식별자 값을 획득한 후 영속성 컨텍스트에 저장.
#### IDENTITY: DB에 entity 저장해서 식별자 값 획득해서, 영속성 컨텍스트에 저장. (저장 후 PK 조회해서 가져오는 방식.)

# 4.7 필드와 컬럼 매핑 : 레퍼런스

* `@Column` : 컬럼 매핑
* `@Enumerated`: 자바의 enum타입
* `@Temporal` : 날짜 타입 매핑
* `@Lob` : BLOB, CLOB(길이제한없는)
* `@Transient`: 특정 필드를 DB에 매핑안함.
* `@Access`: JPA가 엔티티에 접근하는 방식 지정

## 4.7.1 @Column
`@Column`은 객체필드를 테이블 칼럼에 매핑. 
`name`, `nullable`이 주로 사용되고, 나머지는 잘 사용 안됨.
`insertable`, `updatable` : 기본값들이 true라서, false로 해두면 readonly.
`unique`: 유니크 제약조건 쓰기. 두 컬럼 합쳐서 unique하려면 `@Table.uniqueConstraints`

이 `@Column` 생략하면, `private int number` 이런데에서는 null값을 입력할 수 없어. 따라서 int형이면 not null 제약을 붙이거나,
`Integer`로 받아야 한다. 

## 4.7.2 @Enumerated
자바의 enum타입 매핑할 때 사용
* enum 클래스를 직접 만들어서,
  ```java
    enum RoleType{
        ADMIN, USER
    }
  ```
  ```java
    @Enumerated(EnumType.STRING)
    private RoleType roleType;
  ```  
* `EnumType.ORDINAL`: enum 순서를 DB에 저장 -> ADMIN이면 0값, USER면 1값 저장 
* `EnumType.STRING`: enum 이름, ADMIN이면 ADMIN이 ,USER면 USER이라는 문자열이 저장된다. 데이터크기 차이.

## 4.7.3 @Temporal

날짜 타입 매핑할 때 사용된다. 
JAVA의 `Date`타입에는 연월일, 시분초가 있지만, DB는 날짜, 시간, 날짜와 시간 타입 세가지가 있다.
* `TemporalType.Date` -> Date
* `TemporalType.Time` -> Time
* `TemporalType.TIMESTAMP` ->TIMESTAMP 타입
@Temporal 생략하면 그냥 디폴트가 .TIMESTAMP가 된다.
  datetime으로 변경되는 것은 MYSQL. DB Dialect가 알아서 바꿔준다.
  
## 4.7.4 @Lob

데이터베이스의 BLOB, CLOB

### 속성 정리
* 문자만 CLOB으로 매핑
* byte[] 같은건 BLOB으로 매핑

## 4.7.5 @Transient: 매핑 안하고, 엔티티에 임시로 어떤 값 보관하려고 할때. DB에 저장하지 않고 조회하지않는.

## 4.7.6 @Access: JPA가 엔티티 데이터에 접근하는 방식 지정

* AccessType.FIELD : 필드에 직접 접근. 필드 접근 권한이 private이어도 접근 가능
* AccessType.PROPERTY: 접근자 Getter를 사용.
```java
@Entity
@Access(AcessType.FIELD)
public class Member
```

@Access 설정 안하면 @Id의 위치를 기준으로 접근 방식이 설정된다.
`@Id` 를 `getId()`에도 붙일 수가 있는데, 이 경우엔 알아서 `PROPERTY`타입이 뙤는거다. 

