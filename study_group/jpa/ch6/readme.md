6장 다양한 연관관계 매핑

엔티티의 연관관계를 매핑할 땐 
- 다중성 (N:1)
- 단방향, 양방향
  - 객체 관계에서 양쪽이 서로 참조하면 양방향
- 연관관계의 주인
  - 외래키의 관리자! (테이블에서 갖고 있는 객체를 지정) 

을 신경써야 한다.

# 6.1 다대일
N:1 관계. 회원 여러명이 한 팀에 속하는 구조
회원이 N 팀이 1.

## 6.1.1 N:1 다대일 단방향

```java
@Entity
public class Team {
    @Id
    @Column(name = "TEAM_ID")
    private String id;
    
    private String name;
    
 //   @OneToMany(mappedBy = "team")
  //  private List<Member> members = new ArrayList<Member>();
}
```
```java
@Entity
public class Member {
  @ManyToOne // (다 : 1 ) 
  @JoinColumn(name = "TEAM_ID")
  private Team team;
}
```
이것처럼,회원은 member.team으로 참조가 가능한데, 팀은 회원을 못보는 경우 N:1 단방향 연관관계이다.

## 6.1.2 N:1 양방향

```java
@Entity
public class Team {
    @Id
    @Column(name = "TEAM_ID")
    private String id;
    
    private String name;
    
    @OneToMany(mappedBy = "team")
    private List<Member> members = new ArrayList<Member>();
}
```
이렇게 양방향 연관관계를 가지게 하면, 연관관계 편의 메서드를 작성해서 빠뜨릴 가능성을 최소화한다.

## 6.2.1 1:N 단방향

이경우, 
```diff
@Entity
public class Team {
    @Id
    @Column(name = "TEAM_ID")
    private String id;
    
    private String name;
    
-   @OneToMany(mappedBy = "team")
+   @OneToMany
+   @JoinColumn(name = "TEAM_ID") // Member Table의 TEAM_ID FK를 가리키기 위함
    private List<Member> members = new ArrayList<Member>();
}
```
```diff
@Entity
public class Member {
  
-  @ManyToOne // (다 : 1 ) 
-  @JoinColumn(name = "TEAM_ID")
-  private Team team;
    
    @Id @GeneratedValue
    @Column(name = "MEMBER_ID")
    private Long id;
}
```

@JoinColumn 애노테이션을 안쓰면, JPA는 joinTable을 두어서 연결 테이블을 하나 만드는 것을 default로 삼는다.

이 방식의 단점은 `TEAM` 객체를 넣는 SQL도 실행시키고, 외래키가 반대쪽 `MEMBER`객체에 있으니, 그쪽의 UPDATE문도 실행시켜야 한다.

`member1`, `member2`가 새로 생성되어 team1을 배정받는 상황이라면

```java
team1.getMembers().add(member1);
team1.getMembers().add(member2);
em.persist(member1); //INSERT - MEMBER1
em.persist(member2); // INSERT - MEMBER2
em.persist(team1); // INSERT TEAM1, UPDATE MEMBER1, UPDATE MEMBER2
```

성능 bad, 관리 bad

## 6.2.2 1:N 양방향 연관관계 매핑
@ManyToOne은 `MappedBy` 속성이 없대. - 비정상적인 관계니까.

`@JoinColumn(name="TEAM_ID", insertable = false, updatable = false)`
이렇게 하면 read only 니까 이렇게 참조할 수 있게 한다.

# 6.3 1:1 연관관계
- 아무쪽에서나 외래 키를 가질 수 있다.

## 6.3.1 주 테이블에 외래 키
- 일대일 관계를 구성할 때 JPA도 주 테이블에 외래키가 있으면 좀 더 편리하게 매핑이 가능하다.

```java
@Entity
public class Member {
    
    @Id @GeneratedValue
    @Column(name = "MEMBER_ID")
    private Long id;
    
    @OneToone
    @JoinColumn(name = "LOCKER_ID")
    private Locker locker;
}

@Entity
public class Locker {
    
    @Id @GeneratedValue
    @Column(name = "LOCKER_ID")
    private Long id;
    private String name;
}
```
이걸 양방향 연관관계로 만드려면, 반대방향에서도 

```diff
@Entity
public class Locker {
    
    @Id @GeneratedValue
    @Column(name = "LOCKER_ID")
    private Long id;
    private String name;
    
+   @OneToOne(mappedBy = "locker")
+   private Member member;
}
```
이렇게 하면 된다.

 DB위의 어떤 테이블( `Member` or `Locker`) 에 FK를 둘지에 따라 연관관계의 주인을 정하면 된다.
 
# 6.4 다대다 (N:N)

관계형 데이터베이스는 정규화된 테이블 2개로 다대다 관계를 표현할 수 없다.
member1 - team1,team2,team3 
member1 - team4,team5 
이렇게 할 수가 없으니 (PK == 'member1')
그래서 보통은 다대다를 일대다, 다대일로 풀어내는 연결 테이블을 사용한다. 

## 6.4.1 다대다: 단방향
```java
@Entity
public class Member {
    
    @Id
    @Column(name = "MEMBER_ID")
    private String id;
    
    @ManyToMany
    @JoinTable(name = "MEMBER_PRODUCT", 
               joinColumns = @JoinColumn(name= "MEMBER_ID"),
               inverseJoinColumns = @JoinColumn (name = 
                                                 "PRODUCT_ID"))
    private List<Product> products = new ArrayList<Product>();
}

@Entity
public class Product {
    @Id @Column(name = "PRODUCT_ID")
    private String id;
    
    private String name;
}
```

회원 엔티티와 상품 엔티티를 `@ManyToMany`, `@JoinTable`로 연결 테이블로 바로 매핑을 했다.
별도로 `MEMBER_PRODUCT` 라는 테이블에 상응하는 객체를 따로 만들지 않아도 매핑을 완료할 수있다.

* @JoinTable.name : 연결할 테이블 지정
* @JoinTable.joinColumns : 현재객체의 어떤 칼럼을 매핑시킬지.
* @JoinTable.inverseJoinColumns : 상대 객체의 어떤 칼럼으로 조인시킬지. `"PRODUCT_ID"`

이러면,
```java
member1.getProducts().add(productA)
em.persist(member1)
```
이렇게 하면 `MEMBER`테이블 에 insert되고, `MEMBER_PRODUCT` 에도 insert가 된다.
```java
member = entityManager.find(Member.class , "member1");
member.getProducts();
```
이렇게 찾을 때에도 `MEMBER` 테이블과 `MEMBER_PRODUCT` 테이블을 `JOIN` 해서 가져온다.

## 6.4.2 다대다 : 양방향

역방향도 @ManyToMany를 쓰면 되는데, 연관관계의 주인이 아닌 쪽에 `mappedBy`를 쓰면 된다.
```java
@Entity
public class Product {
    @Id @Column(name = "PRODUCT_ID")
    private String id;
    
    @ManyToMany(mappedBy="products")
    private List<Member> members;
    private String name;
} 
```

N:1처럼, 연관관계 편의 메서드를 설정해서
```java
product.add(member); 
```
이거만 해도,
`member.getProducts().add(product);`
`product.getMembers().add(member);`
두개가 실행되게 해야 한다. 

## 6.4.3 다대다 매핑의 한계와 극복, 연결 엔티티 사용

연결 테이블을 자동으로 처리해주니 편리하지만, 실무에서 사용되기에는 불편하다. 
왜냐하면, `Member_Product` 같은 테이블을 설정해두면, 이게 `주문`을 나타내는 테이블이 되는 셈인데,

`주문날짜`
`주문수량`
이런 칼럼을 `Member_Product`에 담으면, 클래스로 매핑되어 있는 테이블이 아니니까 불러올 방법이 없다.

그러니까, `MemberProduct` 클래스를 만들어서
`Member`, `Product`와 각각 1:N , N:1로 매핑을 시켜야 한다. 

`MemberProduct` 클래스가 연관관계의 주인이 된다. 
`Member` 쪽이랑 `Product` 쪽이 `mappedBy`를 써주어야 한다. 


```java
@Entity
@IdClass (MemberProductId.class)
public class MemberProduct{
    
    @Id
    @ManyToOne
    @JoinColumn ( name = "MEMBER_ID")
    private Member member; //MemberProductId.member와 연결되게 
  
    @Id
    @ManyToOne
    @JoinColumn(name = "PRODUCT_ID")
    private Product product; // MemberProductId.product와 연결
  
    private int orderAmount;
}
```

우리의 `MemberProduct`는 `composite key` 를 사용한다. (두 개 이상의 키를 합쳐서 PK로 사용)
이런 경우 클래스를 별도로 만들어 `@IdClass` annotation으로 지정해주어야 한다.

```java
public class MemberProductId implements Serializable {
    private String member;
    private String product;
}
```
이를 `식별자 클래스`라고 부르며
- Serializable을 구현하고
- equals, hashCode 메소드를 구현하고
- 기본 생성자가 있어야 하고
- 식별자 클래스는 public이어야 하고
- @EmbeddedId를 @IdClass 대신 사용할 수 있다.

* 식별 관계 ?

`MemberProduct`는 `Member`, `Product`의 기본키를 받아서 자신의 기본 키로 사용하는데, 
이렇게 부모 테이블의 기본 키를 받아서 기본키랑 외래키로 사용하는 경우를 DB 용어로 식별 관계 (`Identifying Relationship`)

물론 이렇게 새로 객체를 만드는 경우에는

```java
Memberproduct memberProduct = new MemberProduct();
memberProduct.setMember(member1);
memberProduct.setProduct(productA);
memberProduct.setOrderAmount(2);
em.persist(memberProduct);
```
이런식으로, 직접 모든 값에 대한 setting을 해야한다.

> Lombok Chain Accessor
>   ```java
> User user = new User(); //@NoArgsConstructor
>    user.setAccount(account); //@Setter
>    user.setPassword(password);
> ```
> ```java
>User user = new User() //chaining
>                    .setAccount(account)
>                    .setPassword(password);
>```
>@Accessors(chain=true)
>public class User 이런식으로 선언

이렇게 `composite key`를 만들어 조회하는 경우에는 
```java
MemberProductId memberProductId= new MemberProductId();
memberProductId.setMember()
memberProductId.setProduct()

MemberProduct memberProduct = em.find(MemberProduct.class, memberProductId);
```

이런식으로 조회를 하게 된다. 너무 복잡하다

## 6.4.4 다대다 : 새로운 기본 키 사용 

그럼 PK를 다른 것으로 만들자.
`ORDER` 라는 테이블로 만들어서 `ORDER_ID`라는 자동생성 키를 사용하고, `MEMBER_ID`, `PRODUCT_ID`를 FK로 사용하는 것이다.
매핑이 훨씬 단순해진다. 

## 6.4.5 다대다 연관관계 정리

다대다 관계를 일대다 다대일 관계로 풀어내기 위해 연결 테이블을 만들 때 식별자를 어떻게 구성할 지 선택해야 한다.

* 식별 관계: 받아온 식별자를 기본 키 + 외래 키로 사용한다.
* 비식별 관계: 받아온 식별자는 외래 키로만 사용하고, 새로운 식별자를 추가한다. (`ORDER_ID` 추가하는 것처럼)





