2장 JPA 시작

# 2.4 객체 매핑 시작

회원정보를 담는 클래스 `MEMBER`가 
`String id`
`String username`
`Integer age`

를 가지고 있어야 한다고 해보자.

* 이 클래스에 `@Entity` 애노테이션을 붙이면
테이블과 매핑할 클래스라고 JPA가 인식할 수 있다.

* `@Table` 애노테이션을 쓰면, 엔티티 클래스가 어떤 테이블 정보와 매핑되야 하는지 알려준다.
생략하면 Entity 이름이 곧 테이블 이름이 된다.

* `@Id` 애노테이션을 쓰면,
테이블의 기본 키(primary key) 에 매핑을 한다. 만약 복합키 (composite key) 라면 클래스를 만들어서 모든 key가 되는 속성을 때려박고
해당 클래스를 가진 필드를 선언, `@id` 어노테이션을 붙인다.

* `@Column` 애노테이션을 쓰면,
필드를 컬럼에 매핑한다.
```java
@Column(name = "name")
private String username; 
```
이렇게 하면 테이블 안에서 name 칼럼과 이 변수값이 매핑이 된다.

* 매핑정보가 없는 필드
이 경우에는 그냥 칼럼명을 변수이름으로 설정하게 되는데, 
만약 spring boot에서 제공하는 default entity manager를 사용하게 되면 CamelCase를 snake_case로 바꿔주는 옵션도 적용되어 있다.
- `String ageOverThree` -> age_over_three 칼럼에 저장
- age_over_three 칼럼값이 ageOverThree로 저장됨.

# 2.5 persistence.xml 설정
JPA의 설정 정보 관리. resources/META-INF/persistence.xml, 즉 클래스 패스의 /META-INF/persistence.xml에 있으면 별도의 설정 없이 JPA가 인식할 수 있다.

Spring boot 기준으로는 
`@Configuration` , `@EnableJpaRepostories` 를 붙인 클래스를 이용, 설정 클래스를 제작할 수 있다
javax.persistence로 시작하는 속성들은 JPA 표준 속성으로, 구현체에 종속되지 않는다.
hibernate.dialect 처럼 hibernate로 시작하는 속성은 JPA를 이용한 wrapping이라고 볼 수 있는 `hibernate`에서만 사용할 수 있다.

## 2.5.1 데이터베이스 방언
`hibernate.dialect` 
JPA는 특정 DB에 종속되지 않는 기술이다. 따라서 각 DB별로 다른 SQL문을 설정해야 하거나 특수 기능들을 사용할 수 있어야 한다. 
그것을 위해 Dialect를 설정하게 해둔다.
```
      hibernate:
        format_sql: true // hibernate가  실행한 SQL 보기 쉽게 정렬해서 출력
        dialect: org.hibernate.dialect.MySQL5Dialect
        show_sql: true // hibernate가 실행한 sql 출력
        use_sql_comments: true // query 출력할때 주석도 함께 출력
        id:
          new_generator_mappings: // JPA 표준에 맞춰 새로운 키 생성 전략을 사용
```
mysql v 5 는 이런 dialect를 쓴다.

어플리케이션 코드를 교체할 필요가 없는 상황인 것이다. 다만 JPA 표준으로 dialect를 설정하는 방법은 없다고 한다.


# 2.6 애플리케이션 개발


 코드는 3부분으로 나뉜다. (머리 가슴 배..)
 1. 엔티티 매니저 설정 (데이터 소스, 네이밍 컨벤션, dialect 등)
 2. 트랜잭션 관리 (`entityManager.getTransaction().begin() ~~ 로직실행 ~~ tx.commit() `)
 3. 비즈니스 로직

## 2.6.1 엔티티 매니저 설정

*엔티티 매니저 설정*
 먼저 persistence가 xml 파일을 보고 해당 설정들을 이용해 EntityManagerFactory를 생성하면, 여기서 `EntityManager`를 받게 된다.
JPA는 
`EntityManagerFactory emf = Persistence.createEntityManagerFactory("jpabook");`
과 같이 EMF를 생성할 수 있는데, 이러면 xml 파일에서 `jpabook`으로 된 영속성 유닛 (persistence-unit)을 찾아 EMF를 생성하게 된다.
EMF를 만드는 비용은 매우 커서, 어플리케이션 전체에서 딱 한번만 생성하고 공유해서 사용해야 한다. 

*엔티티 매니저 생성*

`EntityManager em = emf.createEntityManager();`
엔티티 매니저 팩토리에서 엔티티 매니저를 생성한다. EM을 활용해 엔티티를 데이터베이스에 CRUD할 수 있다.
매니저는 내부에 데이터 소스(DB 커넥션)을 유지하면서 데이터베이스와 통신한다. 하지만, thread 사이에 공유하거나 재사용하면 안된다.
각각이 EMF에서 EM하나씩을 생성하도록 로직을 구현해야 한다. EMF는 공유해도 된다.

*종료*
마지막 사용이 끝난 EM은 `em.close()` 로 종료해야 한다.
애플리케이션이 종료될 때에도 `emf.close()`를 호출해야 한다.

## 2.6.2 트랜잭션 관리
JPA를 이용할 때는 항상 트랜잭션 안에서 데이터를 변경해야 한다.
- 트랜잭션이 없을 때 변경하면 예외가 발생한다.


## 2.6.3 비즈니스 로직

등록은
```java
String id = "id1";
Memeber mem = new Member();
mem.setId(id);
mem.setNumber(2);

em.persist(mem);

```
이런식으로 진행한다. JPA는 entity정보를 분석해서 SQL문을 만들어 데이터베이스에 전달한다.

수정은 위에서 `mem.setId(id);` 이런식으로 하면 된다.JPA는 어떤 엔티티가 변경되었는지 추적하는 기능을 가진다.

삭제는 `em.remove(mem)` 와 같이 진행하면 delete SQL이 실행된다.\

한 건 조회: `Member findMember = em.find(Member.class, id);`


## 2.6.4 JPQL

하나 이상의목록을 조회하면, `em.createQuery("select m from Member m":,Member class)`
이런식으로 쓰게 되기도 하는데, 엔티티 객체를 대상으로 검사하려면 모든 테이블을 어플리케이션의 메모리에 올려서, 검색을 진행해야 한다.
이런 상황을 해결하기 위해 Java Persistence Query Language 라는 쿼리 언어로 이 문제를 해결할 수 있다.

* JPQL은 엔티티 객체를 대상으로 쿼리하는 것. (클래스와 필드 대상)
* SQL은 데이터베이스 테이블을 대상으로 쿼리한다.

JPQL은 데이터베이스 테이블을 전혀 알지 못한다.
이를 사용하려면 `em.createQuery(JPQL, 반환타입(Member.class))` 메서드를 실행해 `Query query` 쿼리 객체를 생성한 후,쿼리 객체의
`.getResultList()`
`.getResultStream()` 이런것을 호출하면 된다.





