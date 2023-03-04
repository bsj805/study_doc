# 9장

# 9.2 임베디드 타입

클래스를 값의 속성으로 하고싶다면, 칼럼에 `@embedded`하거나, 클래스에 `@embeddable` 둘중하나.

값 타입 == 우리가 말하는 값의 속성명, 필드명.  
엔티티 타입: 실제 클래스

## 9.2.3

근데 만약 임베디드 클래스를 속성으로 가지는 필드를 여러개 만들었어

```java

@Embedded Address myAddress;
@Embedded Address yourAddress;
```

그러면 Address라는 속성 밑에 zipcode, location 두개의 필드명이 있었다면

DB에 자동으로 myAddress_zipcode, myAddress_location 이런 칼럼으로 매핑이 될까? 안된다. zipcode, location 두개로 생성이 된다. 그러니
@AttributeOverride를 써줘야한다.

근데

# 9.3 값 타입과 불변 객체

```java
member1.setHomeAddress(new Address("OldCity"));
        Address address=member1.getHomeAddress();

        address.setCity("NewCity"); //회원1의 address를 받아서 member2에게 적절히 변형해서 넣는경우
        member2.setHomeAddress(address); 
```

이 경우 이미 영속성 컨텍스트의 address를 사용하는 것이라서, 회원 1, 회원 2가 둘다 "NewCity"로 업데이트된다. side effect가 생기는 것인데,

```java
Address address=member1.getHomeAddress();
        Address address2=address.clone();
```

이런식으로 복사하는 메서드를 만들어서 사용해야한다.
`return new address(this.zipcode, this.location);`

이런식으로 말이다.

근데 이걸 프로그래밍적으로 막을 수는 없을까? 사람은 항상 실수하는법. 객체의 값을 수정 못하게해. 그럼 clone을 무조건하게 된다.

## 9.3.3 불변 객체

`setter`를 안 만들면 불변객체가된다.

# 9.4 값 비교

equals() 메서드 재정의 할때 모든 필드값 비교하게 구현해야. HashCode()도 제정의 해야, HashSet, HashMap이 정상동작한다.

# 9.5 값 타입 컬렉션

R DB에서는 컬렉션으로 객체를 못가지니까, @CollectionTable 애노테이션으로 추가 테이블을 매핑해야 한다.

근데 일부만 변경했을때에는 바뀐값이 정확히 뭔지 감지 못해서 테이블을 죄다 지웠다가 죄다 INSERT하는 경우가 생긴다.

# 10장

# 10.1 객체지향 쿼리

JPA가 지원하는 기능

- JPQL: Java Persistence Query Language
- Criteria Query : JPQL을 편하게 작성하도록 도와주는 API. 빌더 클래스 모음
- Native SQL: 해당 DB의 SQL문을 직접 사용가능
- QueryDSL: Criteria 쿼리 처럼 JPQL 편하게 작성
- JDBC 직접 사용. MyBatis 같은 SQL 매퍼 프레임워크 사용.

## 10.1.2 Criteria Qeury

`query.select(m).where(..)` 같은 쿼리. where절에는 `.where(cb.equal(m.get("username","kim)))` 이런식으로 string이 들어가게 되는데,
메타 모델 API를 사용해서 annotation processor를 통해 `m.get(Member_.username)` 이런식의 코드가 만들어지게 할 수 있다. 특정 조건에 따라 where 절이
바뀌어야 하는 경우 등 `동적 쿼리`를 작성해야할 때 도움됨.

## 10.1.3 QueryDSL

표준은 아니고 오픈소스 프로젝트.

```java
List<Member> members=
        query.from(member)
        .where(member.username.eq("kim"))
        .list(member);
```

되게 편리한데?

## 10.1.4 native query

그냥 SQL 작성해서 쓰는거.

## 10.1.5 JDBC 직접사용.

영속성 컨텍스트를 셀프로 플러시 (JPA랑 같이 쓰면 entity Manager로부터 session가져와서 사용)

# 10.2 JPQL

## 10.2.1 기본 문법, 쿼리 API

SELECT ,UPDATE, DELETE 지원. INSERT는 그냥 em.persist()하면 되어서, 없다.

### SELECT

```java
SELECT m.username FROM Member m
```

이렇게 테이블 이름의 별칭은 필수.

이런 쿼리 실행하려면 쿼리객체 생성해야.

- 반환 타입이 명확 = `TypeQuery` 객체 사용
- 반환 타입 지정불가 = `Query`객체 사용

```java
TypeQuery<Member> query=em.createQuery("select m From Member m",Member.class)
```

맨 뒤에 반환 클래스를 지정해서 TypeQuery를 반환한다.

파라미터 바인딩을 `where m.username = :username).setParameter("username",usernameParam).getResultList()`
이것처럼, 이름기준으로 할 수 있다. 원래는 positional parameter place holder라고 해서, `setParameter(1,usernameParam)`
이런식으로.

parameter binding을 사용하면 파라미터의 값이 달라도, 같은 쿼리로 인식해서 내부적으로 JPA to SQL 했던 쿼리를 재사용 가능. +로 연결하는 것을 지양하라.
> StringBuilder 이거 사용하는 것 지양하라. SQL injection 너무나 쉽다. by 리다

## 10.2.3 프로젝션

SELECT 절에 조회할 대상을 지정하는 것을 프로젝션이라고 한다.

```java
select{프로젝션 대상}FROM...
```

엔티티, 임데디드 타입, 스칼라 타입 이렇게 존재.

엔티티 조회하면 영속성 컨텍스트에서 관리되지만, 임베디드 타입 조회하면 영속성 컨텍스트에서 관리되지 않는다. (스칼라 타입으로 그냥 새로운 객체를 만들어 관리하는것.)

```java
new EmbeddedType(order.city,order.secret,order.zipcode)
```

이런식으로 리턴받은 스칼라 값을 embedded 타입의 클래스 하나로 바꾸는 것.

아, 프로젝션을 어디서 봤나 했더니, 만약 엔티티 전체를 받아올 필요가 없고, 일부만 조회하고 싶다면, 새로운 DTO를 하나 만들어. 해당 속성만 존재하는. 이를테면

```java
private String username;
private int age;
```

두개만 필요하다면 이 두개만 담은 `UserDTO`를 만들어서

```java
TypedQuery<UserDTO> query=em.createQuery("SELECT new jpabook.jpql.UserDTO(m.username, m.age) FROM Member m",UserDTO.class );
```

이런식으로 하면, 알아서 변환해서 객체로 넘겨준다.

## 10.2.5 집합과 정렬

- NULL값은 무시해서 COUNT같은데에 안잡힌다
- 값이 없는데 SUM, AVG, MAX, MIN 함수를 사용하면 NULL값이 된다. count는 0
- DISTINCT 집합함수에 사용해서 중복된 값을 제거하고 집합구하기.

```java
select COUNT(DISTINCT m.age)from Member m
```

페치 조인 : 미리 Member 받아올때 연관된 Team 객체도 받아오게 한다 -> team들 지연로딩 안시키는 성능 최적화.

# 10.3 Criteria

JPQL을 자바 코드로 작성할 수 있는 클래스 모음.

```java
// SELECT m FROM Member m
CriteriaBuilder cb=em.getCriteriaBuilder();
        CriteriaQuery<Member> cq=cb.createQuery(Member.class);
        Root<Member> m=cq.from(Member.class); //FROM 절을 생성한다. m이라는 별칭으로 사용한다랑 똑같다. m을 조회의 시작점이란 의미로 쿼리 ROOT라고 한다.
        cq.select(m);

        TypedQuery<Member> query=em.createQuery(cq);
        List<Member> members=query.getResultList();
```

```java
Predicate usernameEqual=cb.equal(m.get("username"),"회원1");

        javax.persistence.criteria.Order ageDesc=cb.desc(m.get("age"));
        cq.select(m)
        .where(usernameEqual)
        .orderBy(ageDesc);
```

이런식으로. Projection으로 일부만 받아올 때 새로 클래스 생성했잖아?

```java
//JPQL: select new jpabook.domain.MemberDTO(m.username,m.age)

CriteriaQuery<MemberDTO> cq=cb.createQuery(MemberDTO.class)
        Root<Member> m=cq.from(Member.class);

        cq.select(db.construct(MemberDTO.class,m.get("username"),m.get("age")))

```

또, `tuple`을 사용하면 Object[] 배열로 받아와서 DTO를 생성하는일이 없다.

```java
TypedQuery<Tuple> query=em.createQuery(cq);
        List<Tuple> resultList=query.getResultList();
        for(Tuple tuple:resultList){
        String username=tuple.get("username",String.class);
        Integer age=tuple.get("age",Integer.class);
        }
```

이런식으로 Object[1] 을 쓰는 것보다 훨씬 가독성도 좋고, 실수의 여지도 없겠지.

## 10.3.12 동적쿼리

쿼리를 그때그때 바꿔야 할 일도 생긴다.

```java
List<String> li=new ArrayList<String>();
        if(age!=null)li.add("m.age = :age")
```

이런식으로해서 SQL string에 append해서 쓰게 된다.

하지만 이건 문제가 많고, Criteria식으로 하면,

```java
List<Predicate> criteria=new ArrayList<Predicate>();
        if(age!=null)criteria.add(cb.equal(m.<Integer>get("age"),cb.parameter(Integer.class,"age")))

        cq.where(cb.and(criteria.toArray(new Predicate[0]))) // 위에서 list로 생성한것을 predicate로 집어넣는다.

        if(age!=null)query.setParameter("age",age);
```

이런식으로 추가해서 코드가 읽기 복잡해지긴 해도, 에러 가능성 낮아짐.

## 10.3.14 Criteria 메타 모델 API

String이 아예 포함 안 되어있는 쿼리를 만드려고 하면, 메타 모델 API가 그 답이다. 메타 모델 적용 전 후를 비교해보면

```java
cq.select(m)
        .where(cb.gt(m.<Integer>get("username"),20)); //전

        cq.select(m)
        .where(cb.gt(m.<Integer>get(Member_.age),20))
```

이런게 가능한것은 annotation processor

```java

@Generated(value = "org.hibernate.jpamodelgen.JPAMetaModelEntityProcessor")
@StaticMetamodel(Member.class)
public abstract class Member_ {

}
```

이런식으로 메타 모델이 만들어진다. 코드 생성기가 모든 엔티티 클래스를 찾아서 엔티티명_.java 모양의 메타 모델 클래스를 생성한다. 컴파일 에러가 된다는 것이 큰 장점.

# 10.4 QueryDSL

JPA Criteria는 문자가 아닌 코드로 JPQL을 작성. but 너무 복잡 어렵. QueryDSL이 진짜 간결한 오픈소스.

```java
public void queryDSL(){
        JPAQuery query=new JPAQuery(em);
        Qmember qMember=new QMember("m"); //m이라는 별칭으로 만든다.
        List<Member> members=
        query.from(qMember)
        .where(qMember.name.eq("회원1"))
        .orderBy(qMember.name.desc())
        .list(qMember);
        }
```

```java
.where(item.name.eq("좋은상품"),item.price.gt(20000))
```

이런식으로 검색조건 사용가능.
`list(qMember)`
이게 결과 조회 메서드이다. 결과가 하나 이상일 때 사용

- uniqueResult(): 조회 결과가 한건일때 사용. 없으면 null, 하나 이상이면 exception
- singleResult(): 위와 같지만 결과가 하나 이상이면 첫 데이터 반환

## 10.4.9 프로젝션과 결과 반환

아까처럼
`List<Tuple> result` 로 받아도 되고, 빈 생성 기능을 사용가능.

```java
List<ItemDTO> result=query.from(item).list(Projections.bean(ItemDTO.class,item.name.as("username"),item.price))
```

이 방식은 setter를 이용해서 값을 채운다. item.name.as 를 통해서 ItemDTO의 필드명을 맞춘다. Projections.constructor(ItemDTO.class,
item.name, item.price)
이런식으로 생성자를 채워도 된다.

UPDATE 나 DELETE도 영속성 컨텍스트를 안 거치고 한다. 한 후에 영속성 컨텍스트를 초기화 해야할듯.

## 10.4.11 동적 쿼리

com.mysema.query.BooleanBuilder: 특정 조건에 따른 동적 쿼리를 편리하게 생성가능.

```java
BooleanBuilder builder=new BooleanBuilder();
        if(StringUtils.hasText(param.getName())){
        builder.and(item.name.contains(param.getName()));
        }
        List<Item> result=query.from(item)
        .where(builder)
        .list(item)
```

이런식으로.

## 10.4.12 메서드 위임

.gt(10) 같이 함수를 만들고 싶다면? 메서드 위임 기능을 사용하면 된다.

# 10.5 네이티브 SQL

- 특정 DB만 사용하는 함수
- 특정 DB만 지원하는 SQL 쿼리 힌트
- 인라인 뷰, UNION, INTERSECT
- 스토어드 프로시저 -> 임의 함수 등, 원하는거 하고 싶을때.

조회한 엔티티도 영속성 컨텍스트에서 관리된다.

```java

@Entity
@SqlResultSetMapping(name = "memberWithOrderCount", //sql 실행할때 설정한 SQL 실행 이름
                     entities = { @EntityResult(entityClass = Member.class) },
                     columns = { @ColumnResult(name = "ORDER_COUNT") })
public class Member {...
}
```

이런식으로 선언해두면,

```java
// SELECT M.ID, AGE, NAME, TEAM_ID, I.ORDER_COUNT 
for(Object[]row:resultList){
        Member member=(Member)row[0];
        BigInteger orderCount=(BigInteger)row[1];
        }
```

이런식으로 받아올 수 있다. Member의 각 칼럼을 굳이 `String name =row[0]` 이런식으로 할 필요가 없다.

# 10.6 객체지향 쿼리 심화

벌크연산. 다량의 데이터를 동시 update, delete, 이 경우, 영속성 컨텍스트를 무시하고 DB에 직접 쿼리를 한다. 고로, DB에 직접 쿼리하고서, 영속성 컨텍스트에 반영해두지 않으면, DB에
직접 쿼리한 후에 영속성 컨텍스트의 값을 가져다 쓰는 일이 생긴다.

뭐 방법이야 많은데,

- em.refresh()
- 벌크연산 먼저 실행
- 벌크 연산 수행 후 영속성 컨텍스트 초기화

그리고 중요한게, Projection으로 DTO에 값을 받아오는 경우에 DTO는 엔티티가 아닐테고, 영속성 관리가 안된다.

또, JPQL로 조회하면 영속된 객체가 리턴되는데, SQL로 변환되어 DB를 무조건 조회하고, 그 조회한걸 영속성 컨텍스트의 캐시와 비교해서 없으면 새로 저장하고 리턴 ,있던거면 있던걸 리턴 하는
방식. `em.find()`랑 달리 무조건 DB를 조회한다.

## 10.6.3 JPQL과 플러시 모드

em.flush()메서드가 JPQL에서 커밋이나 쿼리 실행시, 커밋시에 자동 플러시되게 할 수 있다.

> ## 플러시 실행 시
>- 영속성 컨텍스트에 있는 모든 엩티티를 스냅샷과 비교. 수정된 엔티티를 찾는다.
>- 수정된 것이 있으면 수정 쿼리를 만들어 지연 SQL 저장소에 등록한다.
>- 쓰기 지연 SQL 저장소의 쿼리를 DB에 전송한다.

JPQL실행전에 영속성컨텍스트의 모든 값을 DB에 반영시켜놔야 한다. 



