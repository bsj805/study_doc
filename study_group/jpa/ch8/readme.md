# 8장 프록시와 연관관계 관리
* 프록시와 즉시 로딩, 지연 로딩 - 객체는 객체 그래프로 연관된 객체들을 탐색.
  이때, 객체를 실제 사용하는 시점에 DB에서 조회가 가능.

* 영속성 전이와 고아 객체: JPA는 연관된 객체를 함께 저장하거나, 함께 삭제할 수 있는
  `영속성 전이` == cascade, `고아 객체` 라는 편의 기능 제공.


# 8.1 프록시
 
엔티티를 조회할 때 연관된 엔티티들이 항상 사용되는건 아니라서 지연로딩
얘 엑세스할 때 데이터베이스에서 가져와라 할 수 있는 `가짜 객체 == 프록시` 객체가 필요.
get() 함수 같은 것을 래핑해서, DB에 접근하는 코드로 바꾸는 것이겠지.

이제 이건 JPA 구현체 별로 다른 로직이 있어서, 아래서는 hibernate 구현체에 대한 설명을 할 것.

## 8.1.1 프록시 기초
JPA에 식별자로 엔티티를 조회할 때 `EntityManager.find()`를 사용한다.
이 메서드는 영속성 컨텍스트에 엔티티가 없을때 DB를 조회한다.
`Member member = em.find(Member.class, "member1`)`

이렇게 엔티티를 직접 조회하면, 엔티티를 실제로 사용하던 말던 실제 DB를 조회해서 값을 가져온다.
만약 실제 사용시점까지 조회를 미루고 싶으면, 
`EntityManager.getReference()` 메서드를 사용한다.

`Member member = em.getReference(Member.class, "member1")`
이 메서드를 호출할 때는 JPA는 DB를 조회하지 않고, 실제 엔티티 객체도 생성하지 않는다. 

*프록시의 특징*
프록시는 실제 클래스와 겉 모양이 같다. 프록시 객체는 실제 객체에 대한 참조(`Entity target`)를 보관.
그리고, 프록시 객체의 메서드를 호출하면 실제 객체의 메서드를 호출한다.

*프록시 객체의 초기화*
프록시 객체는 member.getName() 처럼 실제 사용될 때 DB를 조회해서 실제 엔티티 객체를 생성하는데,
이게 프록시 객체의 초기화. 

```java
Member member = em.getReference(Member.class, "id1");
member.getName(); 
```
이런식으로 하면, MemberProxy를 반환받고, 아래서 실제 DB접근이 일어난다.

```java
class MemberProxy extends Member {
    Member target = null; // 이게 실제 엔티티를 가리키는 참조값
    
    public String getName() {
        if(target == null) {
            //실제 참조값이 DB에서 읽어들여지지 않은 경우
            //1. 초기화 요청
            //2. DB 조회
            this.target = member;//3. 실제 엔티티 생성 및 참조 보관
        }
        return target.getName();//4. target.getName()을 실제로 리턴시켜줄수 있다.
        
    }
    
}
```

*프록시의 특징*

- 프록시 객체는 처음 사용할 때 한 번만 초기화된다.
- 프록시 객체를 초기화한다고 프록시 객체가 실제 엔티티로 바뀌는 것은 아니다. 
  프록시 객체가 초기화되면 실제 엔티티를 가진 프록시 객체일뿐. (비효율적인거 아닌가~ if문을 항상 더 거치는데)
- 프록시 객체는 원본 엔티티를 상속받은 객체니까 타입 체크 시에 주의해서 사용.
  `instanceof(Member.class)` 하면 true가 뜨지만, `getClass() == Member.class`하면 false가 뜬다.
- 영속성 컨텍스트에 찾는 엔티티가 이미 있으면, lazy loading할 필요가 없어서 
  `em.getReference()` 호출해도, 프록시가 아닌 실제 객체 반환.
- 초기화는 영속성 컨텍스트의 도움을 받아야 가능. - detach를 해버리는 문제가 발생한다. (em.getReference(), em.detach(member) 하고 member.find()해버리면?) (LazyInitializationException)
    ```java
      Member reference1 = em.getReference(Member.class, member1.getId());
      System.out.println(reference1.getClass());
      em.clear();
      System.out.println(reference1.getName());
    ```
## 8.1.3 프록시 확인
JPA가 제공하는 `PersistenceUnitUtil.isLoaded(Object entity)` 메서드를 사용하면 프록시 인스턴스의 초기화 여부 확인 가능.
아직 초기화 안한 프록시 인스턴스는 false 반환. 

```java
boolean isLoad = em.getEntityManagerFactory()
                    .getPersistenceUnitUtil().isLoaded(entity)
```
아니면 클래스명을 `member.getClass().getName()` 으로 출력해봐도 돼.
proxy 생성 라이브러리에 따라, 출력되는 클래스명은 다르다.

hibernate는 프록시 개체를 강제 초기화할 수 있다. org.hibernate.Hibernate.initialize(order.getMember());
JPA 표준은 아니다.

# 8.2 즉시 로딩과 지연 로딩

프록시 객체는 주로 연관된 엔티티의 지연 로딩을 위해 사용된다.
```java
Member member = em.find(Member.class, "member1");
Team team = member.getTeam();//여기서!! 프록시 객체를 Team에 넣게 된다.
team.getName(); //여기서 Team이 실제로 로딩된다.
```
근데 사실 언제 어떤 엔티티가 로딩되는 것이 좋을지는 
* 즉시 로딩 : 엔티티 조회시 연관된 엔티티도 조회
  * @ManyTOOne(fetch = FetchType.EAGER)
* 지연 로딩 : 연관된 엔티티를 실제 사용할 때 조회
  * @ManyToOne(fetch = FetchType.LAZY)

## 8.2.1 즉시 로딩
즉시 로딩을 사용하려면 FetchTYpe.EAGER (연관된 엔티티 필드에다가 설정하는것.)

`em.find(Member.class, "member1")` 한번으로 팀을 조회할 수 있다.
보통의 JPA 구현체들은 Join 쿼리를 사용한다. 

Left Outer Join 보다 inner join이 성능과 최적화에 유리한데, 외래 키에 NOT NULL 제약조건이 있을때에만 INNER JOIN을 사용할 수 있다.
그래서 `@JoinColumn(name = "TEAM_ID" , nullable = false)` 이런식으로 조건을 걸어줘야 한다.
`@ManyToOne(optional = false)` 도 INNER JOIN을 사용하게 한다. 

## 8.2.2 지연 로딩

@ManyTOOne의 fetch 속성이 `FetchTYpe.LAZY`라면 지연 로딩을 사용하게 된다.
물론, 영속성 컨텍스트에 이미 존재하는 객체라면 프록시객체가 아닌 실제 객체를 사용한다.

## 8.2.3 즉시로딩, 지연 로딩 정리

모든 엔티티를 영속성 컨텍스트에 넣는것도, 모든 엔티티를 지연 로딩하는것도, 최적화에는 좋지 않다. 상황에 맞춰써야.


# 8.3 지연 로딩 활용

* `Member`와 연관된`Team`은 같이 잘 사용된다 -> 즉시로딩
* `Member`와 연관된 `Order`은 가끔 사용된다 -> 지연 로딩
* `Order`와 연관된 `Product`는 같이 잘 사용된다. -> 즉시로딩
## 8.3.1 프록시와 컬렉션 래퍼

엔티티를 영속 상태로 만들 떄, 엔티티에 컬렉션이 있으면 - 하이버네이트의 컬렉션으로 변환하는데 이를 컬렉션 래퍼라고 한다.
컬렉션은 컬렉션 래퍼가 지연 로딩을 처리한다. 프록시 객체같은 느낌이지만, 컬렉션 래핑 클래스가 그걸 맡고 있는 것이다.

```java
Member member = em.find(Member.class, "member1");
List<Order> orders = member.getOrders();//이때까지는 order객체로딩안되고, 프록시가 로딩
orders.get(0); //여기에서 로딩되는데, `product`도 즉시로딩되게 해놨으니, product도 로딩된다. 
```

## 8.3.2 JPA기본 페치 전략.
fetch 속성의 기본 설정값은
* @ManyTOOne, @OneToOne: 즉시로딩 (FetchType.EAGER)
* @OneTOMany, @ManyToMany: 지연로딩 (FetchType.LAZY)


JPA의 기본 페치 전략은 연관된 엔티티가 하나면 즉시 로딩을, 컬렉션이면 지연 로딩을 사용한다.
oneTOMany같은 경우를 생각해보면, Member하나가 VVIP라서 Order를 엄청나게 했어. 그러면 이거 즉시로딩한다고 했다가 
수십만개의 Order를 동시에 로딩하게 될 수도 있다.

## 8.3.3 컬렉션에 FetchType.EAGER 사용시 주의점

* 컬렉션을 하나 이상 즉시 로딩하는 것은 권장하지 않는다. 
이를테면 Member하나가 list of Order, list of Product를 즉시로딩한다고 하면,
Order개수 * Product 개수 만큼의 연산량이 생긴다. 아마도 cartesian product가 진행되니까 그렇다.

* 컬렉션 즉시 로딩은 항상 외부 조인( OUTER JOIN)을 사용한다. 

여러명의 멤버를 가지고 있는 팀을 생각해보자.
만약 팀에 사람이 한명도 없으면, 내부조인을 하는 것 때문에 팀 자체가 조회가 안될 수도 있다.
팀->멤버 조회시에는 내부조인을 사용하면 안되는 것이다.
1:N 

# 8.4 영속성 전이: CASCADE

특정 엔티티를 영속 상태로 할 때, 연관 엔티티도 영속 상태로 만들고 싶으면, 영속성 전이 (transitive persistence)를 사용할 수 있다.
JPA는 CASCADE 옵션으로 영속성 전이를 제공한다. 영속성 전이를 사용하면 부모 엔티티를 저장할 때, 자식 엔티티도 함께 저장할 수 있다.

원래는
```java
em.persist(parent);

child.setParent(parent);
em.persist(child);

child2.setParent(parent);
em.persist(child2);
```
이렇게 해야지 된다.

즉, 자식도 영속성 컨텍스트에 영속상태로 존재하게 해야지 부모에 저장이 되는 것이다.

## 8.4.1 영속성 전이: 저장

이제 부모만 영속 상태로 만들면 자식도 영속상태로 만들 수 있다.

```java
@Entity
public class Parent {

@OneToMany(mappedBy = "parent", cascade = CascadeType.PERSIST)
private List<Child> children = new ArrayList<Child>();
```

흠?
이렇게 하면,
```java

Child child1 = new Child();
Child child2 = new Child();

Parent parent = new Parent();
child1.setParent(parent);
child2.setParent(parent);
parent.getChildren().add(child1);
parent.getChildren().add(child2);

em.persist(parent);

```
이렇게 해서, 자식 엔티티까지 한번에 영속상태로 만들 수 있다.


## 8.4.2 영속성 전이 : 삭제

원래는, 저장한 부모와 자식 엔티티를 모두 제거하려면, 각 parent를 em.find로 받아오고, 각 child list를 em.find로 가져오든 해서 em.remove를 모든 child, parent에 대해 호출한다.

영속성 전이를 사용하면
`CascadeType.REMOVE`를 설정해서, 부모 엔티티만 삭제해도, 다 삭제할 수 있다.

## 8.4.3 CASCADE 종류

* 영속
* 병합
* 삭제
* REFRESH
* DETACH
* 위 모두 

# 8.5 고아 객체

JPA는 부모 엔티티와 연관관계가 끊어진 자식 엔티티를 자동으로 삭제하는 기능을 제공하는데, 고아 객체 제거라고 한다.

그래서 부모 엔티티의 컬렉션에서 자식 엔티티의 참조를 제거하면 (영속상태의 부모 엔티티라면) 
자식 엔티티가 자동으로 삭제되게 할 수 있다.

```java
@Entity
public class Parent{

  @OneToMany(mappedBy = "parent", orphanRemoval = true)
  private List<Child> children = new ArrayList<Child>();

}
```

고아 객체를 제거하기 위해, 이렇게 설정하면, 엔티티는 자동으로 삭제된다.

```java
Parent parent1 = em.find(Parent.class, id);
parent1.getChildren().remove(0); //이러면 부모 컬렉션에서 자식 엔티티의 참조가 제거되는데
```
이럼 `DELETE FROM CHILD WHERE ID=?` 가 실행된다. 

`parent1.getChildren().clear()` 하면 컬렉션이 비워지고.

다 삭제될거야.

근데, 고아 객체 제거는 고아객체 제거 기능으로 지정된 엔티티가 한곳에서만 참조된다는 전제하에 쓰인다.

member -> product
team -> product 
이렇게 참조하고 있는 경우에는, member에서 고아객체 제거기능을 사용해버리면, team은 자기도 모르는 새에 product하나가 없어져버린다.
특정엔티티가 개인 소유하는 경우에만 사용해야 한다.

# 8.6 영속성 전이 + 고아 객체, 생명주기

CascadeType.ALL + orphanRemoval = true를 동시에 사용하면?
엔티티는 EntityManager.persist()를 통해 영속화되고,
EntityManager.remove ()를 통해 제거된다. 엔티티 스스로 생명주기를 관리한다는 뜻이다.

```java
Parent parent = em.find(Parent.class, parentId);
parent.addChild(child1);
```

자식을 삭제하려면 부모에서 제거하면 된다. (orphanRemoval)

자식 저장할때에는 부모에 등록만 하면 된다. (cascade)
이렇게 기억하자.



















































