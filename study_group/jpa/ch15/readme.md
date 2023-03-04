# 15장 고급 주제와 성능 최적화

- 예외 처리
- 엔티티 비교
- 프록시 심화 주제
- 성능 최적화
    - N+1 문제 :   
        >N+1문제가 있는데, select o from Order o 라고 해봐. 그리고 Member는 order하나를 가지고 있어. 그러면 Order의 o 하나마다 Member을 조회해야한다.
      Member를 먼저 조회했다면 상관없겠지만, order 번호 하나 가지고 Member를 찾아서 써야하니 최악의 경우에는 order 개수만큼 Member에 SQL 을 날린다.
    - 읽기 전용 쿼리 성능 최적화
    - 배치 처리
    - SQL 쿼리 힌트 사용
        >힌트는 엔티티 그래프 사용할때, 빈번히 조회되는건 같이 가져오라고 할 수 있는 것.
    - 트랜잭션 지원하는 쓰기 지연과 성능 최적화
    

## 15.1 예외처리

JPA 예외는 모두 unchcked Exception (runtime Exception) 
다만, 트랜잭션 롤백을 표시하는 예외, 롤백을 표시하지 않는 예외가 있어.
롤백을 표시하는 애들은 복구해서는 안돼. 이외엔 개발자가 커밋할지 롤백할지 판단.

롤백 표시하는 예외
- 이미 엔티티가 존재하는데 persist (중복 데이터 삽입)
- 락 충돌
- 트랜잭션 없이 엔티티 변경

롤백 표시하지 않는 예외
- Query.getSingleResult() 호출시 결과가 하나도 없을 때 발생
- 쿼리 실행 시간 초과 등

## 15.1.2 스프링 프레임워크의 JPA 예외 변환 
서비스 계층에서 데이터 접근 계층의 구현에 직접 의존은 안좋다. - > 예외를 추상화시켜서 개발자에게 제공.

## 15.1.3 스프링에서 JPA 예외 변환기 적용
JPA예외를 스프링 프레임워크의 예외로 변경하려면 `PersistenceExceptionTranslationPostProcessor` 빈 등록
그러면 이 빈이, `@Repository` 를 적용한 곳에 예외 변환 AOP를 적용해준다.
만약 예외를 변환하지 않고 그대로 받고 싶으면, JPA예외를 만드는 메서드에
`throws javax.persistence.NoResultException`
이런식으로 예외를 명시해서 직접 반환시킨다. `throws java.lang.Exception`만 해도 예외 변환 없이 내보낸다.

## 15.1.4 트랜잭션 롤백 시 주의사항
트랜잭션 롤백은 데이터베이스 반영사항만 롤백하고 수정한 자바 객체까지 원상태로 복구해주지 않는다.
즉, 객체가 수정된 채로 영속성 컨텍스트에 남아있기 때문에, 새로운 영속성 컨텍스트를 생성해서 사용하거나, 영속성 컨텍스트 초기화 한 다음에 사용해야 한다.
스프링에서는 트랜잭션당 연속성 컨텍스트 전략이 default니까, 트랜잭션을 종료시켜서 영속성 컨텍스트도 사라지게 한다.

OSIV같은 경우, 롤백을해도 다른 트랜잭션에서 해당 영속성 컨텍스트 그대로 사용할 수도 있다.
(view까지 세션 연장)

# 15.2 엔티티 비교
영속성 컨텍스트 내부에 엔티티 인스턴스 보관 위한 1차 캐시 - 영속성 컨텍스트와 생명주기 같이한다.
엔티티를 조회할때 항상 같은 엔티티 인스턴스 어떻게 받을까? 주소값이 같은 인스턴스를 반환해.

## 15.2.1 영속성 컨텍스트가 같을때의 엔티티 비교
identity: == 비교가 같다
equivalent: equals 비교가 같다.
DB 동등성: @Id == 즉 PK 값이 같다.

> 테스트할때 같은 트랜잭션이니까 어떤 SQL이 플러시에 일어나는지 알 수 없다. 고로 em.flush()해보면 알 수 있다.


## 15.2.2 영속성 컨텍스트 다를 때 엔티티 비교 
당연히 동일성 비교가 안돼. 다른 영속성 컨텍스트에 들어가는 걸.

# 15.3 프록시 심화 주제
프록시는 원본 엔티티를 상속받아 만들어진다.

## 15.3.1 영속성 컨텍스트와 프록시
프록시로 조회한 엔티티도 동일성 보장? identity
같은 영속성 컨텍스트에서 "member1"로 조회했으면 두 프록시 개체 identical
영속성 컨텍스트가 처음 조회된 프록시를 그대로 반환

물론 이미 영속성 컨텍스트에 있으면 `getReference`로 호출해도 프록시가 아닌 실제 객체 반환

## 15.3.2 프록시 타입비교
프록시가 `Member` type인지는 Member.class == .getClass() 말고 instanceOf로 해야 한다. 상속때문에 올바르게 작동한다

## 15.3.3 프록시 동등성 (equivalent) 비교
equals()로 비교해야하는데, 프록시는 실제 데이터를 가지고 있지 않다. 
그래서 `Getter`을 사용해야 한다. 그러면 실제 객체를 가져와 비교를 하게 되기 때문이다.

## 15.3.4 상속관계와 프록시

프록시를 부모 타입으로 조회하면 문제가 생기는데, 즉 Book 클래스인 애를 
```java
Item proxyItem = em.getReference(Item.class, saveBook.getId());
```
처럼 해버렸다면 Item 엔티티를 프록시로 조회했다.
이 `proxyItem` 은 원본 엔티티로 Book 엔티티를 참조한다.
근데 `proxyItem instanceOf Book` 은 실패한다. 프록시 객체 자체는 Item 타입에 의해서 만들어져서.
Book book = (Book) proxyItem 처럼 강제 다운캐스팅도 실패한다. 
`ClassCastException`인데, 당연하다. Item 기반으로 만들어졌으니 Book으로는 못간다. 

그럼 Item 클래스로 general 하게 받는 것은 안될까?

### JPQL로 대상 직접 조회
자식 타입을 Book으로 지정한다.
```java
em.createQuery("Select b from Book b where b.id=:bookId"", Book.class)
```
이런식이다.

### 프록시 벗기기
hibernate에서는 unProxy 메서드를 제공해서, 원래의 엔티티가 무엇인지 찾아올 수 있다.
`Item unProxyItem = unProxy(item)`
그럼 `unProxyItem instanceof Book`에 성공한다.
단, 이렇게 꺼내온 unProxyItem과 `em.find("book1")`로 조회한 item은 `==` 비교에 실패한다. 
왜냐하면 강제로 꺼내왔고, 영속성 컨텍스트에 있는애니까, 

### 기능을 위한 별도의 인터페이스 제공
음~ 만약 Item.Class 로 받아서 각 아이템의 이름을 조회하고자 하는 task였다면
그냥 `TitleView`와 같은 공통 인터페이스를 만들고, 각 자식 엔티티들은 해당 인터페이스의 getTitle() 메서드를 구현하면
```java
Item item = em.find(Item, "item1")
item.getTitle()
```
이런식으로 할 수 있다. 다만, 이 경우 프록시의 대상이 되는 타입에서 인터페이스를 implement해야 한다.

### visitor 패턴 사용

Visitor가 있고 `visit(Book book)`, visitor를 `accept(visitor)` 하는 클래스들로 구성된다. 

1. Visitor 인터페이스를 두어서 각 엔티티에 visit하게 한다
2. visit마다
```java
public void visit(Book book)
        {
            println(book.getClass()+book.getName()+book.getAuthor());
        }
public void visit(Album album)
        {
        println(album.getClass());
        }
public void visit(Movie movie)
        {
        println(movie.getClass());
        }
        

```
Book, Album, Movie에 visit 메서드를 구현한다. 실행 로직은 visitor에 위임한다. 
```java
public void accept(Visitor visitor){
    visitor.visit(this)
        }
```
이런식으로 한다.

그럼 `item.accept(new PrintVisitor())//PrintVisitor가 visit 메서드 구현한것` 
visit()에 새로운 동작만 추가하면 되니 좋지만, 객체 구조 변경시 모든 visitor 수정, 위임이 많아져 복잡해지는 문제 등이 있다.

# 15.4 성능 최적화

## 15.4.1 N+1 문제

Member가 List<Order> orders 를 가지고 있다고 생각해보자. 그리고 이걸 FetchType=EAGER로 설정하면

em.find(Member.class, id);
할 때 자연스래 OuterJoin으로 SQL을  JPA가 만들어준다.

하지만, JPQL을 쓸 때에
`SELECT M FROM MEBMBER M`을 하면, SELECT * FROM ORDERS WHERE MEMBER_ID="?" 하면서 찾는다.

지연로딩이면 JQPQL에서는 문제가 생기지 않는데,List<Order>을 순회하며 어떤 행동을 한다면 결국 N+1 문제가 생긴다.

### 페치 조인 사용
`SELECT M FROM MEMBER M JOIN FETCH M.orders`
이경우 INNER JOIN.

### Hibernate의 @BatchSize
지정한 size만큼 SQL의 IN 절을 사용해서 조회한다.
```java
SELECT * FROM ORDERS
WHERE MEMBER_ID IN (
        ? , ? , ? , ? , ?
        )
```

### Hibernate @Fetch
FetchMode.SUBSELECT
IN 서브 쿼리를 사용해서 N+1 문제 해결.
`select m from Member m where m.id > 10` 이런 JPQL이면 
`SELECT O FROM ORDERS O WHERE O.MEMBER_ID IN ( ... m.id>10 )`
이렇게돼.

## 15.4.2 읽기 전용 쿼리 성능 최적화
읽어오면 무조건 다 영속성 컨텍스트에의해 관리되니 메모리 사용 많아져.

- 스칼라 타입으로 조회 (select o.id,o.name)
- 읽기 전용 쿼리 힌트 사용 (setHint(readOnly)
---------------------------- 여기까지 메모리 절약
  
-----------------------아래부터는 속도 최적화
- 읽기 전용 트랜잭션 사용 ( 스프링에서 @Transactional(readOnly = true))
    - 영속성 컨텍스트 안에 있지만 플러시 안함. 고로 스냅샷 비교 등 연산 사라져
    
## 트랜잭션 밖에서 읽기
트랜잭션 없이 엔티티를 조회한다는 뜻.
조회할때만 사용해야해.

## 15.4.3 배치 처리
수백만건의 데이터 배치처리 - > 영속성 컨텍스트에 너무 많은 엔티티가 쌓여서 메모리 부족오류.
적절한 단위로 영속성 컨텍스트를 초기화 하는 것이 바람직 하다.

그래서 데이터를 `em.persist()` 할 때에도 적당히 몇건마다 플러시를 호출하도록 처리해야 한다.

데이터 처리할때에는? (수정할 때에는?)
- 페이징 처리 : DB 페이징 기능
- 커서 처리 : cursor 기능 사용

### JPA 페이징 배치 처리
.setFirstResult(i*pageSize)
.setMaxResults(pageSize)

이런식으로 해두면, 한 페이지씩 갖고오게 돼.

### 하이버네이트 scroll 사용 (cursor 느낌)

.scroll(ScrollMode.FORWARD_ONLY) 를 한다.

while(scroll.next()) 이런식으로 해서 scroll.get(0); 이런식으로 Product product를 가져올 수 있다.
엔티티를 .next() 할때마다 하나씩 조회할 수 있다.

### 하이버네이트 무상태 세션 사용 

영속성 컨텍스트가 없다. 엔티티 수정은 `update()`메서드를 직접 호출해야 반영된다. 
(영속성 컨텍스트가 없으니 flush()도 안해)

## 15.4.4 SQL 쿼리 힌트 사용
엔티티그래프 할때처럼 특정 경우에 같이 가져오기, 어떤 속성을 더 가져오기 이런게 해당한다.
`SELECT /*+ FULL (MEMBER) */ m.id, m.name from MEMBER m;`
이게 뭘까

## 15.4.5 트랜잭션을 지원하는 쓰기 지연과 성능 최적화

네트워크 호출 비용이 크니까 쓰기 지연을 했었다. 배치사이즈를 정하면 그 배치사이즈만큼의 SQL이 쌓일때마다 실행시킨다.
다만, 같은 SQL문 (value만 다른) 을 실행할때만 묶여서 보내진다.

### 트랜잭션을 지원하는 쓰기 지연과 어플리케이션 확장성.
- DB의 row에 락이 걸리는 시간 최소화가 장점이다.
트랜잭션을 커밋 해서 영속성 컨텍스트를 플러시하기 전까지는 DB에 데이터를 등록, 수정 ,삭제하지 않으니 커밋 직전까지는 row에 락이 걸려있지 않다.
  






