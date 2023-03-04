# 12장, 스프링 데이터 JPA

데이터 접근 계층은 CRUD operation 하는 함수를 계속 개발해야. 근데 대부분 동작방식이 비슷한걸.

# 12.1 스프링 데이터 JPA

CRUD를 처리하기 위한 공통 인터페이스 제공. 데이터 접근 계층을 개발할 때 인터페이스만 작성해도 CRUD 처리를 할 수 있게 된다.

CRUD 처리를 위한 공통 메서드는

```java
org.springframework.data.jpa.repository.JpaRepository
```

이 인터페이스에 존재한다.

어플리케이션 실행 시점에 스프링 데이터 JPA가 레포지터리 인터페이스의 구현체를 주입해준다.
`findByUsername(String id)` 이런것도 자동생성 해준다.

# 12.1.1 스프링 데이터 프로젝트

DB에 대한 접근 추상화.

# 12.2 스프링 데이터 JPA 설정

어떤 리포지토리에 적용할지 패키지 명을 적어야.

그럼 해당 패키지 내의 인터페이스들을 찾아서 impl 클래스를 동적으로 생성해 스프링 빈으로 등록한다.

# 12.3 공통 인터페이스 기능

JPARepository 인터페이스를 상속하는 방식이 이 자동으로 지원하는 CRUD기능 받는것.

```java
public interface MemberRepository extends JpaRepository<Member, Long> {
}
```

회원 엔티티를 쓰고, 식별자는 long. 주요 메서드는

- save -> persist랑 merge 알아서 분리해서 호출
- delete
- findOne
- getOne
- findAll

# 12.4 쿼리 메서드 기능

- 메서드 이름만으로 쿼리 생성하는 기능

## 12.4.1 메서드 이름으로 쿼리 생성

회원조회 하려면
`findByEmailAndName(String email, String name);`

정해진 규칙에 따라 이름을 지어야 한다.

## 12.4.2 JPANamedQuery

쿼리에 이름을 부여해서 사용하는 방식인데, XML에 쿼리를 미리 정의하거나 `@NamedQuery` 어노테이션으로 정의가능.

```java

@Entity
@NamedQuery(
        name = "Member.findByUsername",
        query = "select m from Member m where m.username = :username"
)
public class Member {

}
```

`em.createNamedQuery("member.findByUsername`,Member.class)`
이런식으로 사용한다. 메서드 이름만으로 NamedQuery 호출도 가능한데,

```java
public interface MemberRepository extends JpaRepository<Member, Long> {
    List<Member> findByUsername(@Param("username") String username);
}
```

선언한 도메인 클래스 . 메서드 이름으로 named query 찾아서 실행

## 12.4.3 @Query, 레포지토리 메서드에 쿼리 정의

가장 일반적인,

```java

@Query("select m from Member m where m.username = ?1")
Member findByUsername(String username);
```

네이티브 SQL 사용하려면 Query에 `nativeQuery = true` 설정.

네이티브 SQL의 파라미터 바인딩은 0부터고, JPQL은 1부터

## 12.4.5 벌크성 수정 처리

@Modifying 어노테이션을 붙여놓으면, 수정 벌크 쿼리를 할 때에 좋다.

> 3.1. Result of NOT Using the @Modifying Annotation Let's see what happens when we don't put the @Modifying annotation on the delete query. For this reason, we need to create yet another method:
>
> ```java
>@Query("delete User u where u.active = false")
>int deleteDeactivatedUsersWithNoModifyingAnnotation();
>```
>Notice the missing annotation.
> When we execute the above method, we get an InvalidDataAccessApiUsage exception:
> org.springframework.dao.InvalidDataAccessApiUsageException: org.hibernate.hql.internal.QueryExecutionRequestException:
> Not supported for DML operations [delete com.baeldung.boot.domain.User u where u.active = false]
(...)
The error message is pretty clear; the query is Not supported for DML operations.


https://www.baeldung.com/spring-data-jpa-modifying-annotation

이거 안붙이면 여러개 못바꾸게 한다.

## 12.4.6 반환 타입

반환 여러개 하면 컬렉션, 단건은 반환 타입지정.

## 12.4.7 페이징, 정렬

파라미터에 Pageable 사용하면 List나 Page 를 반환 타입으로 사용가능.

페이지당 10개면, page를 `getContent()`로 가져오고 다음 데이터가 존재하는 지 여부를 `result.hasNextPage()` 로 가져오고,

# 12.5 명세

AND나 OR 같은 술어를 명세. Specification.

`findAll(where(memberName(name)).and(isOrderStatus())`
이런식으로 쓰는게 명세이다.

# 12.6 사용자 정의 레포지토리 구현

IMPL을 JPA가 만들어버리니까, 내 구현체를 못만드네? 필요한 메서드만 구현해야 한다면? 레포지토리 인터페이스 이름 + Impl 클래스를 두면, 사용자 정의 인터페이스를 적용해서 새로운 메서드 도
Impl 하면서, 스프링 데이터 JPA도 사용할 수 있다.

# 12.7 web 확장

스프링 MVC에서 사용할수있는 편리한 기능을 제공한다.
`@EnableSpringDataWebSupport` 하면,

## 12.7.2 도메인 클래스 컨버터 기능

HTTP 파라미터로 넘어온 엔티티의 ID로 엔티티 객체를 바인딩. 회원정보수정기능할때 @RestObject 이런거 두면 막 알아서 커맨드 객체에 들어가듯이.

# 12.8 스프링 데이터 JPA가 사용하는 구현체

Impl 클래스의 실체는

@Repository == 스프링이 추상화한 예외로 JPA 예외를 변환한다. @Transactional == JPA 모든 변경은 트랜잭션 안. 서비스 계층에서 트랜잭션 시작안했으면, 리포지토리에서
시작하지만, 이미 시작했으면 새로 시작안함. transaction에 Readonly = true 하면 플러싱 안해. 성능향상 조금 save() 메서드 뭐 자연스럽게.

# 12.10 스프링 데이터 JPA와 QueryDSL 통합

- QueryDslPredicateExecutor 사용 - 리포지토리에서 이거 JPA데이터 + 상속받으면된다. 그럼 레포지토리에서 QueryDSL을 검색 조건으로 사용하고, 스프링 데이터 JPA의
  findAllBy ... 이런 기느옫 사용가느아핟.

## 12.10.2 QueryDslRepositorySupport

사실 QueryDSL의 모든 기능을 사용하긴 어렵다. join이나 fetch가어려운데, 커스텀 Impl 만들듯이 하고, 이걸 상속받으면, 사용가능하다.

