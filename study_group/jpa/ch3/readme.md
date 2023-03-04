# 3 영속성 관리

JPA가 제공하는 기능은 엔티티와 테이블을 매핑하는 설계 부분이랑 매핑한 엔티티를 실제 사용하는 부분으로 나뉜다.

즉, 
* configuration 파트
* SQL을 사용해야 하는 비즈니스 로직 파트

매핑한 엔티티를 엔티티 매니저를 통해 사용하는데, 엔티티와 관련된 CRUD 기능을 처리할 수 있다.

## 3.1 엔티티 매니저 팩토리와 엔티티 매니저

DB를 하나만 사용하는 어플리케이션은 EMF ( 엔티티 매니저 팩토리 )를 하나만 생성한다. ( DB 여러개와 매핑하는 경우 EMF가 여러개, 각자 주입을 통해 사용 )

```java
EntityManagerFactory emf = Persistence.createEntityManagerFactory("jpabook");
```
이러면 persistence.xml (Datasource 정보 등) 에 있는 정보를 바탕으로 EMF를 생성하게 된다. 

이제 `emf.createEntityManager()` 을 통해 `EntityManager em`을 사용할 수 있다.

EMF 하나를 생성하는 비용이 커서, 어플리케이션 전체에서 공유가 된다.
다만, `EntityManager`은 thread가 동시에 접근할 수 없고, EMF는 여러 쓰레드가 동시에 접근해도 된다.

`EM`은 데이터베이스 연결이 꼭 필요한 시점까지 커넥션을 얻지 않는다.
JPA를 J2EE 환경(스프링 프레임워크 환경 포함)에서 사용하면 EMF는 데이터소스에 대한 커넥션 풀을 만드는 방식으로 사용한다.

## 3.2 영속성 컨텍스트란?

`persistence context`가 JPA를 이해하는데 가장 중요한 용어이다.
`엔티티를 영구 저장하는 환경` 으로 이해할 수 있고, `em.persist(member)` 처럼 객체를 저장하고, `find`로 찾는 것이 영속성 컨텍스트에 저장하고, 그로부터 찾는 것이다.
여러 `EM`이 같은 영속성 컨텍스트에 접근할 수도 있다. 일단은 나중에 생각하자.

## 3.3 엔티티의 생명 주기

엔티티에는 4가지 상태가 존재한다.
* 비영속(new/transient): 영속성 컨텍스트와 전혀 관계가 없는 상태
* 영속(managed): 영속성 컨텍스트에 저장된 상태
* 준영속(detached): 영속성 컨텍스트에 저장되었다가 분리된 상태
* 삭제 (removed): 삭제된 상태

<img width="940" alt="image" src="https://media.oss.navercorp.com/user/29140/files/64be9872-1b73-4eed-a1e9-d40463ac4bdc">

1. 비영속(new/transient)
엔티티 객체를 생성하고, 아직 영속성 컨텍스트에 저장하지 않았을 때.
```java
Member member = new Member();
```

2. 영속(Managed) 

`em.persist(member)`로 영속성 컨텍스트에 의해 관리되는 상태.
`em.find()` 나 JPQL을 사용해 조회된 엔티티도 이 상태.

3. 준영속(detached)

영속성 컨텍스트에 있던 엔티티를 관리하지 않으면. 
`em.detach(member)` 이런식으로 호출하거나
`em.close()` 로 영속성 컨텍스트를 닫거나 `em.clear()`로 초기화해도 `member`라는 객체는 준영속 상태가 된다.

4. 삭제 (removed)

엔티티를 영속성 컨텍스트와 데이터베이스에서 삭제한다. 
`em.remove(member)`

## 3.4 영속성 컨텍스트의 특징
 
* 영속성 컨텍스트와 식별자 값
영속성 컨텍스트는 엔티티를 식별자 값 (`@Id`로 테이블의 기본 키와 매핑한 값 )으로 구분한다.
즉, 영속 상태는 식별자 값이 반드시 있어야 한다. 
https://stackoverflow.com/questions/53817508/how-id-can-be-found-in-transaction-scoped-persistence-context-if-its-not-in-the

`persistence context` 에 영속상태가 될 때에 각 객체에 id 값을 배정하게 된다고 한다.

* 영속성 컨텍스트와 데이터베이스 저장

언제 DB에 저장될까? 트랜잭션을 커밋하는 순간 == `flush()`

* 영속성 컨텍스트가 엔티티 관리시 장점

- 1차 캐시
- 동일성 보장 (같은 transaction안에서 같은 id로 `find`하면 같은 객체 참조값을 가짐)
- 트랜잭션을 지원하는 쓰기 지연 
- 변경 감지
- 지연 로딩 ( 객체가 실제로 쓰일 때까지 load 안 해)

### 3.4.1 엔티티 조회

영속성 컨텍스트 내부의 캐시가 1차 캐시.
영속성 컨텍스트 내부에 Map이 하나 있는데, 키는 `@Id`로 매핑한 식별자고 값은 엔티티 인스턴스이다.
<img width="366" alt="image" src="https://media.oss.navercorp.com/user/29140/files/85fe273b-3342-4427-a14e-13fc0e8c898f">

```java
Member member = new Member()
member.setId("member1")
```
이런식으로 하면 PK가 `member1`로 세팅되고, 
`em.persist(member)`를 하면 영속성 컨텍스트의 1차 캐시 `MAP`에 `member1`을 key값으로 회원 엔티티를 저장한다.

1차 캐시의 키는 PK인 `member1`이 된다.
그래서 `em.find(Member.class, "member1")` 과 같이 PK를 이용해 조회한다.
만약 1차 캐시에 없으면 DB에서 가져와서 1차 캐시에 저장 후 리턴해준다.

* 영속 엔티티의 동일성 보장 * 

같은 트랜잭션안에서는 영속성 컨텍스트가 같은 1차 캐시를 사용하고, 따라서 `find`를 같은 `PK`값으로 한다면, `==` 동일성 비교가 성공한다.

### 3.4.2 엔티티 등록

엔티티 매니저는 `em.getTransaction().begin()` 하고  이 transaction.commit() 하기까지 내부 쿼리 저장소에 `INSERT SQL`을 차곡차곡 모아둔다.
이것을 `transactional write-behind` : 쓰기 지연 이라고 한다.

커밋하면, `persistence context`를 `flush`를 먼저 한다. `flush`는 영속성 컨텍스트의 변경 내용을 DB와 동기화 한다. 
이때 DB에 반영되는 것이다. (이 과정에서 실패하면 DB는 원래상태로 돌아감) 이제 DB의 `commit`이 실행되면 그대로 DB에 저장이 되는 것이다.


### 3.4.3 엔티티 수정

*SQL 수정 쿼리의 문제점*

SQL을 사용하면 수정 쿼리를 직접 작성해야 한다. 처음엔 `이름`만 바꿔야 할지도, 다음엔 `나이`까지 바뀌어야 할지도 모른다.

*변경 감지*
JPA는 엔티티를 수정할 때 단순히 엔티티를 조회해서 1차 캐시에 있는 데이터의 내용을 바꾸게 된다.
`member.setAge(15)`
`member.setAge(209)` 
이런식으로 바꾸더라도, 처음 persist 되었을 때 객체의 snapshot( 최초 상태를 복사해서 저장해둔 것 )과 엔티티를 비교해서 변경된 속성을 찾는다.
이 스냅샷과의 비교는 flush()가 호출되었을 때 일어난다. (DB에 보내지기 전 - 어떤 `update`문을 만들어야 할지 모르니까) 
비영속이나, 준영속처럼 영속성 컨텍스트의 관리를 받지 못하는 엔티티는 값을 변경해도 DB에 반영되지 않는다. 

하지만, JPA의 update문은 모든 필드를 `update`하도록 `SQL`문이 만들어진다.
이 경우, 수정 쿼리가 항상 동일하다는(데이터는 달라도) 장점이 있고 ( 쿼리문 재사용 ) DB는 한번 parsing 했던 쿼리를 재사용 한다.
하지만 데이터량이 늘어나긴 하니까, 이 경우에는 `@org.hibernate.annotations.DynamicUpdate`와 같은 하이버네이트 확장 기능을 사용해야 한다.
수정된 데이터에 대한 `UPDATE` SQL문을 생성한다.

`@DynamicInsert`도 있다. 30개 칼럼 이상일 때 이들을 사용하자.

### 3.4.4 엔티티 삭제

엔티티 삭제를 위해서는 삭제 대상 엔티티를 조회를 먼저 하고, `em.remove()`에 `find`한 엔티티를 넘겨준다. 
이것도 역시 `flush()` 때 DB에 삭제 쿼리를 전달하게 되는데, `em.remove(memberA)` 이런식으로 했을 때 이미 영속성 컨텍스트에서 제거되긴 한다.


## 3.5 플러시

플러시는 영속성 컨텍스트의 변경 내용을 데이터베이스에 반영한다. 
`flush()`실행시, 
1. 변경감지가 동작해서, 영속성 컨텍스트의 모든 엔티티를 스냅샷과 비교, 수정된 엔티티를 찾고 `update`쿼리를 '지연' SQL 저장소에 등록
2. 쓰기 지연 SQL 저장소의 쿼리를 데이터베이스에 전송

플러시하는 방법은 3가지
1. em.flush 
2. 트랜잭션 커밋시 
3. JPQL 쿼리 실행시 => JPQL을 만들기 전에 `persist` 해 놓았던 것들이 있으면 JPQL에 의해 조회되는 것들은 `persist`에 의해 반영된 정보가 들어있지 않을 것. 그래서 flush가 자동 호출되게 해 놓았다.

### 3.5.1 플러시 모드 옵션

엔티티 매니저에 플러시 모드를 직접 지정하려면 `javax.persistence.FlushModeType`
* FlushModeType.AUTO: 커밋이나 쿼리를 실행할 때 플러시 (기본값)
* FlushModeType.COMMIT: 커밋할 때만 플러시

플러시 모드를 별도로 설정하지 않으면 AUTO로 동작한다. 
`em.setFlushMode`

## 3.6 준영속

영속 -> 준영속? 
`detach`된 것을 준영속 상태라고 한다. flush 되지도 않고, 변경감지도 안돼.

### 3.6.1 엔티티를 준영속 상태로 전환 `detach()`

`em.detach()`는 특정 엔티티를 준영속 상태로 만든다. 
특정 엔티티 하나를 준영속 상태로 전환하는데,
'1차 캐시'부터 '쓰기 지연 SQL 저장소'까지, 해당 엔티티와 관련된 모든 정보가 제거 된다. 

### 3.6.2 영속성 컨텍스트 초기화 `clear()`

영속성 컨텍스트의 모든 엔티티를 준영속 상태로 만든다.

### 3.6.3 영속성 컨텍스트 종료 `close()`
영속성 컨텍스트의 모든 엔티티를 준영속 상태로 만든다.
보통은 `persistence context`, `entity manager`가 `commit`처럼 일을 마치고 종료되면서 종료되는 경우가 많다.

### 3.6.4 준영속 상태의 특징

*거의 비영속 상태에 가깝다*

*식별자 값을 가지고 있다.*
 한번 영속 상태였기 때문에
 
* 지연 로딩을 할 수 없다*
 실제 객체 대신 프록시 객체를 로딩해두고, 실제로 객체가 사용될 때 쿼리를 실행해서 데이터를 불러오는 방법을 못 쓴다. 

### 3.6.5 병합 merge()

준영속 상태의 엔티티를 다시 영속 상태로 변경할 수 있다. 기존 비영속 상태의 객체를 `em.merge(member)`와 같이 넣어서 새로운 영속 상태의 엔티티를 반환한다.

다만 `Member member2 = em.merge(member)`을 해서 받아온 `member2`는 member1과 같지 않다.
물론 내부 필드값들은 다 동일하겠지만. 새로운 영속 상태의 엔티티가 반환된다.

이것은, 
1. 이번에 들어온 entity인 `member`를 이용해 1차 캐시에서 entity를 찾아보고, 
2. 없어서 DB를 조회해서 1차 캐시를 채워넣고
3. merge로 들어온 `member`의 변화한 값을 1차 캐시에 저장해두고
4. 이 상태의 엔티티를 반환한 것이다.

`merge`는 비영속 엔티티도 영속 상태로 만들 수 있다.

















