# 7장  리액티브 방식으로 DB 사용하기

# 최근 데이터 처리 패턴 

## 도메인 주도 설계
DDD관점에서 정의된 bounded context가 하나의 마이크로서비스로 매핑되야 한다. (구분된 서비스가 배달이면 배달서비스를 만들고, 회계면 회계 서비스를 만들어야)

- 엔티티
- 데이터 전달 객체
- 애그리게이트
- 리포지토리

이런 객체들은 서비스 영속 계층 (DB 계층)과 매핑해야 한다.

## 마이크로 서비스 시대의 데이터 저장소 (영속 계층)
각 서비스 사이에 DB 공유 하지 않는 것이 핵심이다.
다른 서비스의 데이터를 조회해야 한다면 해당 서비스 API를 통해 받아와야지 DB를 접근하면 안된다.

- DB 스키마와 강한 결합 없이 서비스 계속 진화시킬 수 있어야 함
- 더 섬세한 자원을 관리할 수 있어야 함
- 수평적으로 확장이 가능해야 함 (부하가는 서비스만 늘려도 되게 ex. 회원가입 등 )
- 가장 적합한 영속 계층 구현을 사용할 수 있어야 함. 

이런 원칙들을 지키기 위해 DB접근을 차단한다.

1. 하나의 DB 서버 , 서비스 별 스키마 하나씩

규칙이 무너지기 쉽다. 다른 서비스 DB접근이 쉽다.

2. 하나의 DB 서버, 다른 엑세스 권한, (즉 별개 계정)



3. 하나의 DB서버 여러개의 DB 구성
백업 작업이 복잡해진다

4. 여러 DB서버, 각서버별로 DB생성
DB별로 세부 설정 가능 - DB확장도 새로 서버에 구성하면 되는 수평, 서버 메모리 늘리는 등 수직 확장 쉬움

5. 혼합해서 사용 = polyglot persistence ( 여러 종류 DB + 여러 서버 사용) - 다중 저장소 영속화

## 다중 저장소 영속화

polyglot programming ( 다중 언어 프로그래밍 ) - 각 언어별로 잘하는게 있으니 여러 언어로 작성해서 소프트웨어를 만들자.

RDBMS는 ACID 지키지만, 그래프 저장, 인메모리 저장소, 분산 저장소 등에 대해 최상의 성능 및 관리 기능 제공 x
NOSQL는 범용 데이터 저장소지만 효율적 사용 불가. 

사용자 세션 : REDIS
상품 정보: MONGODB
사용자 활동 기록: Cassandra (event sourcing)
회계 정보 : PostgreSQL ( 어떤 장점이 있을까? )

다중 언어 영속성은 복잡성으로 인해 추가비용발생 
올바른 영속성 기술을 사용한다면 부담이 적어질 수 있다. 

스프링 프레임워크는 스프링 데이터라는 데이터 영속성 프로젝트를 가진다. 

## 서비스로서의 데이터베이스
잘 설계된 마이크로서비스는 모든 서비스가 상태 의존적이지 않다. (stateless)
즉 처리된 값은 input으로 들어온 데이터에만 연관이 되어 있다. 같은 input이면 같은 결과낼것.

클라우드 환경에서는 서비스가 상태가 없을때에 효율적 확장 가능하고, 높은 가용성을 가질 수 있다. 
대부분 클라우드 제공 업체는 DB를 서비스로 제공 (DBaaS)
클라우드 위 DB 알고리즘은
1. 클라우드가 DB, 파일 저장 영역에 대한 엑세스 요청
2. 클라우드 공급자는 데이터 영역에 접근할 수 있는 API 또는 서버 자원에 대한 권한 부여. 클라이언트는 제공되는 API 세부 구현에는 신경 x
3. 클라이언트는 엑세스 자격 증명 제공 API 또는 데이터베이스 드라이버를 사용
4. 과금

클라이언트, 즉 SW 개발자는 핵심 목표에만 집중. 관심사의 분리. (separation of concerns SOC)
AWS S3 , DynamoDB

# 마이크로 서비스 사이의 데이터 공유

두 개 이상의 서비스가 소유한 데이터 쿼리할때 join 쓰지 않는다. 
1. 주문 , 결제 서비스에 조회하는 어댑터 서비스를 구현한다
2. 너무 강결합 되어있다면 둘을 포함한 하나의 서비스로 병합

다만, 조회가 아닌 업데이트는 매우 복잡해진다. 모든 서비스에 동시에 데이터가 업뎅이트가 되야 한다면?

보통 분산 트랜잭션, 이벤트 기반 아키텍처로 풀어낸다.

## 분산 트랜잭션
네트워크가 분리된 두 개 이상의 컴퓨터 시스템에 저장된 데이터 업데이트하는 트랜잭션
여러 서비스가 동시에 업데이트를 동의 해줘야 한다.

2-phase locking을 보통 사용한다. lock만 거는 단계가 있고, lock 풀기만 하는 단계가 있다. 즉 lock -> unlock -> lock 의 흐름으로 가지 않는다.
이럼 업데이트해야하는 모든 곳에 대한 lock을 가지고서야 진행되는 것.

하지만 분산 트랜잭션은 여러개로 구성된 마이크로서비스에서는 권장 안한다. 
- 마이크로서비스 사이의 강결합이 나타난다.
- 분산 트랜잭션은 확장되지 않는다.
  - 대역폭이 제한되고 시스템 확장성이 저하된다.

## 이벤트 기반 아키텍쳐
event-driven architecture.

1. 시스템 상태 변경시 첫번째 서비스가 DB 변경후 같은 트랜잭션 안에서 이벤트를 메시지 브로커로 전달
2. 이벤트 전달받은 두번째 서비스는 이벤트 수신해서 그 data변경 - 또 메시지 전달할수도 있음.
서비스는 동시에 블로킹 x , 상호 의존성도 x

첫번째만 작동하고 있더라도 요청에 대한 처리가 계속된다. ( 분산 트랜잭션의 경우 2가 실행될때까지 무한 블로킹 )
아니면 아예 이런 동시 업데이트만 처리하는 어댑터를 둘 수 도 있다. (업데이트 되는 상태값들을 모두 받는 어댑터)

## 궁극적 일관성 

불확실성을 도메인 모델에 포함시켜야 한다. 
시스템에는 inconsistency가 언제든 발생할 수 있다.
ex.) `결제 정보 확인 중` 이라는 상태를 도입해서 결제 정보 확인 없이 주문을 생성할 수도 있다. 
그러면 결제정보 확인이 끝난 상태를 추후에 확인해서 다음 progress를 진행할 수 있다.

## SAGA 패턴
마이크로서비스에서 분산 트랜잭션에 가장 널리 사용되는 패턴 

소수의 작은 트랜잭션으로 구성되고, 각 트랜잭션은 하나의 마이크로서비스에 국한
외부요청이 saga 시작, saga의 첫번째 작은 트랜잭션 시작. 성공시 두번째 트랜잭션 시작. 중간에 성공못하면 롤백처럼 이전 트랜잭션의 보상이 기동되는 방식이다.
- events-based choreography : 별도 중재 서비스 없이 서로 직접 상호작용
- orchestration via a coordinator service : 중재서비스 있다.

## 이벤트 소싱
각 비즈니스 엔티티 상태 변화 순서를 저장한다. - 이전의 스냅샷에서 추가된 이벤트들을 확인가능 - 일정 기간마다 스냅샷 제작
상태를 지속적으로 재계산해야 해서, 쿼리가 복잡할 떄 효율적인 쿼리 수행 불가!
CQRS ( 명령 및 쿼리 분리 )
- 쓰기는 상태 변경 명령을 수신해 기본 이벤트 저장소에 저장
- 상태의 snapshot을 내보냄. 갱신 이벤트가 수신되었을 때 비동기적으로 계산

이벤트 저장소 cassandra, 쿼리 저장소 ES (상태에 대한 view를 가지고 있음- 일종의 캐시 역할)

## 충돌 없는 복제 데이터 타입 (CRDT)
글로벌 락이나 트랜잭션 일관성 없이 여러 서비스에서 동시에 업데이트 할 수도 있다 - 낙관적 복제 : 불일치를 감수하며 데이터 복제본 사용
복제본끼리 병합될 떄 consistency가 지켜지게 된다. 병합 시점에서 충돌을 해결하는데, 병합 프로세스가 항상 성공하는 수학적 속성을 가진 데이터 구조도 있다
CRDT 라고 한다. Conflict-Free-Replicated Data Types

https://channel.io/ko/blog/crdt_vs_ot

이게 google docs의 코어 알고리즘이라고 한다. 이제 여기서 문제점을 보완하는 알고리즘들이 있는 것.

![img.png](img.png)

Redis DB도 CRDT지원

## 데이터 저장소로서의 메시징 시스템

메시지를 저장하는 곳이 있으니 DB자체가 필요없는거 아닌가? 그렇다. DB 중요도가 낮아진다. 아파치 카프카 같은거 사용.
polyglot persistence + 메시지 브로커 + 이벤트 중심 아키텍쳐

# 데이터 조회를 위한 동기식 모델  

리액티브 이전의 데이터 엑세스 구현을 보고, 쿼리 실행시 클라이언트와 DB 통신이 어떻게 되는지, 어떤 부분을 비동기식으로 할 수 있는지 보자.

## DB 엑세스를 위한 와이어 프로토콜

어플리케이션에서 DB 드라이버를 통해 DB 서버에 요청을 보내게 되는데, 기본적으로 DB 드라이버와 DB 서버 사이의 통신을 와이어 프로토콜이라고 한다.
클라이언트와 DB 사이 전송되는 메시지의 정렬 형식을 정의한다. DB가 C++로 짜였던, 아무 상관없는 이유는 와이어 프로토콜이 언어 독립적이기 때문.

와이어 프로토콜은 TCP/IP층이라서, 블로킹 방식으로 동작할 필요는 없다. 다만 지금까지 프로그래밍 된 것이, 요청 결과 올때까지 블로킹. 
또한 TCP는 슬라이딩 윈도우에 의해 구현된 흐름 제어로 배압을 지원할 수 있는 비동기 프로토콜이다. (흐름 제어가 가능하다 TCP는) - byte 더 많이 보내라, 적게 보내라 가능 ( buffer 채워지는 거 보고 )

다만 우리에게 필요한 배압조절은, DB에서 row를 받을 때 네트워크 버퍼와 상관없이 현재 받은 row의 개수를 보고 다음 row를 보내도록 해야 하는 것이다. 
HTTP2, 웹소켓, gRPC 등이 있다. 

클라이언트가 수백만개의 행을 검색한다면 검색결과 반환은 
1. 전체 결과를 DB에서 계산해서 넘겨주기 - 클라이언트와 DB 다 큰 버퍼 필요 + 전체 쿼리 이후에 결과 받을 수 있음
2. chunk 결과 받기 - 논리적 배압 전파 가능
3. 쿼리 중 결과 얻자마자 스트림으로 보내기 - 버퍼 안필요, 클라이언트 빠르게 수신가능. but 네트워크 cpu 과하게 사용가능하다

DB는 하나 이상의 접근 방법으로 와이어 프로토콜 (driver to db) 구현 ex. mysql은 전체 or stream으로 가능.

## 데이터베이스 드라이버
드라이버는 DB용 와이어 프로토콜을 각종 프로그래밍 언어로 구현한 라이브러리이다. 파이썬용 DB-API, 자바용 JDBC 등.

mongoDB, Cassandra, Couchbase는 드라이버 API를 비동기나 리액티브 스타일로 구현했다.

### JDBC ( JAVA Database Conncectivity)

JDBC의 결과는 java.sql.ResultSet이지만 모든 행을 로드한 뒤에야 처리가 가능하다. 
JDBC는 직접사용하기보다는 스프링 데이터 JDBC, JPA 사용한다.

요즘엔 JDBC에 직접 의존 안하고 커넥션 풀 사용한다 -  hikariCP

리액티브 방식으로 RDB접근하려면 JDBC가 아닌 다른 DB ACCESS API가 필요하다.

### 스프링 JDBC (동기식)

JdbcTemplate 클래스가 있어 쿼리를 실행시키고, 테이블의 각 행을 entity로 매핑해준다. (kafkaTemplate이 kafka로 메시지를 send하는 객체이듯 template이라는 이름을 많이 쓰나보다)
Mapper class를 직접만들수도있다. (ResultSet과 int rowNum 을 받는)

### 스프링 data JDBC (동기식)
@Query 어노테이션, 객체로 매핑된 결과를 List, Stream, CompletableFuture 등으로 받을 수 있다. 
CompletableFuture <Stream> 형태는 첫 row 받을 때까지 블로킹 되지 않는다.다만, 그 다음 요청을 해서 다음 chunk를 받아와야 한다면 
stream의 원소를 처리하다가 블로킹 된다. (stream에 다음 원소가 쌓일때까지)


### 스프링 데이터 JDBC를 리액티브하게 만들기. 

R2DBC를 개발중이다. 데이터베이스와 논블로킹 방식으로 리액티브하게 동작하는 드라이버를 통합하기 위함.

JPA는 자체 API와 JPQL (Java Persistence Query Language) 로 구성된다. JPA는 자체 API와 JPQL(Java Persistence Query Language)로 구성
순수 JDBC 아닌 JPA 구현체 사용시 캐싱의 장점. Hibernate같은.

### JPA를 리액티브하게 만들기는 불가능

### 스프링 데이터 JPA
@Entity를 붙여서 DB와 매핑되는 모델을 만든다.
메서드 이름기반 쿼리를 제작하는 `CrudRepository` 상속

### Spring Data Nosql
spring data mongo 는 @Entity 대신 @Document를 사용해 특정 DB 컬렉션을 참조가능하다 ( DB > 컬렉션 > 문서)
mongoDB는 object-Document mapping에 사용되는 자바 클래스를 설명하는 _class 필드를 추가한다.

Nosql 데이터베이스는 RDB와 다르게 동기식 블로킹 API에 크게 의존적이지 않다. (최근에 나왔고 빠르게 발전중)

## 동기 모델의 한계
1. 네트워크 호출 + 외부 서비스에 데이터 검색용도로 사용하지만 논블로킹 안한다. 자원이 낭비된다.
2. JDBC는 커넥션풀로 병렬로 쿼리를 요청하는데, 그러면 HTTP2 커넥션 개수도 쿼리 개수만큼 늘어난다. HTTP2를 이용해서 동일한 TCP로 여러 리소스 동시에 보내고 받을 수 있다. 고로 논블로킹으로 전환해서 점유할 TCP 소켓 수를 줄인다.

## 동기 모델의 장점
블로킹 웹 응용 프로그램 구축에 유용하다. - 디버그, 테스트하기 쉽다.

# 스프링 데이터로 리액티브하게 데이터 접근하기
스프링 데이터 commons의 ReactiveCrudRepository를 구현하면 된다.

- 효과적 쓰레드 관리 (I/O 작업 블로킹 x)
- 첫번째 쿼리 대기시간 짧음
- 낮은 메모리 사용
- 배압 전파 - 클라이언트 처리 속도를 알려서 더 받아올 수도, 적게 받아올 수도 있다.
- 하나의 커넥션 공유 (하나의 네트워크 연결로 쿼리와 데이터 처리작업을 보낼 수 있다. 어떤 쓰레드던 쿼리 객체에 대해 권한을 가지고 있다 stateless하다.)

# 리포지토리 동작 조합하기

책의 제목만 알고 있는 상태에서, 책의 출판연도 업데이트 해야 하는 상황
1. 책 인스턴스 DB에서 얻어오기
2. 책 출판연도 바꾸기
3. 책 DB에 저장하기

책 title이 1초 뒤에 반환되는 Mono<String> title
출판연도가 2초 뒤에 반환되는 Mono<Integer> year

```java
public Mono<Book> updatedBookYearByTitle(
        Mono<String> title,
        Mono<Integer> newPublishingYear
        )
```

mono를 subscribe해야지 title과 newPublishingYear를 얻어온다

### 1번방법
title을 이용해 book을 찾은다음,  Mono<book>.flatMap으로 book 인스턴스를 접근이 가능하게 한뒤, 
새 Mono<Integer> year를 그 내부에서 구독해 Book과 year에 대한 접근이 다 가능하게 해서 
해당 flatmap안에서 book의 year수정 후 DB에저장

```java
public Mono<Book> updatedBookYearByTitle(
        Mono<String> title,
        Mono<Integer> newPublishingYear
        ){
    
    return rxBookRepository.findOneByTitle(title)
        .flatMap(book -> newPublishingYear
                        .flatMap(year -> {
                            book.setPublishingYear(year);
                            return rxBookRepository.save(book);
        }))       
}
```

다만, 책을 받아온 뒤에나 year에 대한 구독을 시작하니까, year구독 시작한지 2초 뒤에 year이 나오는 이런 경우에는 구독을 빨리시작시켜주는게 좋다.

```java
public Mono<Book> updatedBookYearByTitle(
        Mono<String> title,
        Mono<Integer> newPublishingYear
        ){
    
    return Mono.zip(title, newPublishingYear).flatMap((Tuple2<String, Integer> data) ->{
            String titleVal = data.getT1();
            Integer yearVal = data.getT2();

            return rxBookRepository.findOneByTitle(titleVal)
            .flatMap(book -> {
                book.setPublishingYear(yearVal);
                return rxBookRepository.save(book);
            })
        })       
}
```
TupleUtils를 사용하면 더 깔끔하게 변환이 가능하다. + 책 엔티티 받는건 title만 수신했을때에도 가능한데 이 경우 계속 기다린다.

```java
public Mono<Book> updatedBookYearByTitle(
        Mono<String> title,
        Mono<Integer> newPublishingYear
        ){

        return Mono.zip( newPublishingYear, rxBookRepository.findOneByTitle(title))
                .flatMap(function( (yearValue, bookValue)  ->{
        bookValue.setPublishingYear(yearVal);
        return rxBookRepository.save(book);
        })
        }))
        }
```

비즈니스 요청에 가장 적합한 옵션을 선택해야 한다. 최적화!