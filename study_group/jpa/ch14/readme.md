# 14장 컬렉션과 부가 기능

## 14.1 컬렉션

JPA는 Collection, List, Set, Map 을 지원하고 @oneToMany, @ManyToMany, @ElementCollection 사용해서 값 타입을 하나 이상 보관할때 사용됨.

private Collection<Member> members = new ArrayList<Member>();
이런식으로 하고 영속상태로 만들면?
원본 컬렉션 감싸는 hibernate 클래스로 나온다. 래퍼 컬렉션이라고도 한다. 

## 14.1.2 Collection, List

중복허용 컬렉션. ArrayList로 초기화.
엔티티 추가만으로는 지연 로딩된 컬렉션을 초기화하지 않는다.
arrayList를 불러와서 거기에 추가하는 방식이 아니라서 .

## 14.1.3 Set
HashSet() -> add() 할때 중복 검사 해야되서 지연로딩할때에는 체크한다.

## 14.1.4 List+@OrderColumn
이러면 순서있는 컬렉션. 순서 값도 같이 보관된다. - 근데 별로 사용안한다.
댓글 1 ~ 4 저장되어있으면 1 삭제되었을때 2,3,4 변경일어남.
또 1을 지우면 null값이 보관되어있어.
NPE 생긴다.

# 14.2 @Converter
엔티티의 데이터를 변환해서 데이터베이스에 저장.

"Y", "N" 쓰는데 boolean타입으로 저장하려면? 컨버터.

VIP VARCHAR(1) 이러면

```
@Convert(converter=BooleanToYNConverter.class)
private boolean vip;
```

이런 컨버터를 붙여서 데이터베이스에 저장되기 직전에 컨버터가 동작한다.

이런 컨버터는

```java
@Override
public String convertToDatabaseColumn(Boolean attr){
    return (attr !=null && attr) ? "Y" : "N";
        }
        
@Override
public Boolean convertToEntityAttr(String dbData){
    return "Y".equals(dbData)
        }
```
이렇게 `AttributeConverter` 인터페이스를 구현해야한다. <Boolean, String> 이런식으로 어디서 어떤걸로 바꿀지.


# 14.3 리스너

모든 엔티티를 대상으로 언제 어떤 사용자가 삭제를 요청했는지 확인하고 싶어.
그럼 
1. PostLoad(find())
2. PrePersist ( persist())
3. PreUpdate (flush())
4. PreRemove ( remove() )

이런식으로 이벤트가 일어나기 전 후에 대해서 로깅을 할 수 있게 리스너를 붙일 수 있다.
- 엔티티에서 이벤트를 직접받거나 (@Prepersist 같은 어노테이션을 메서드에 붙인다.)
- 리스너를 등록하거나 (엔티티로 지정한 클래스 위에 @EntityListener(DuckListener.class))
- 기본리스너를 사용 == 모든 이벤트를 처리 (META-INF/orm.xml)

# 14.4 엔티티 그래프

엔티티를 조회할 때 연관된 엔티티를 함께 조회하려면 fetch 옵션을 fetchtype.EAGER로 설정한다. 
@NamedEntityGraph 어노테이션을 써서
`@NamedAttributeNode("member")` 이런식으로 Order엔티티에 특정 속성을 지정하면 이 order를 조회할 때 같이 조회되는 속성이 된다.
lazy load로 지정되어 있어도!

근데 member이 가리키는 뭐 Team도 같이 조회되었으면 좋겠어. 그러면 근데 이건 Order에 안 속해있잖아. 그러면 `subgraph`라고 속성을 지정해

JPQL에서는 setHint를 통해서 이런 엔티티그래프 사용가능.

hints.put("javax.persistence.fetchgraph",graph) 함수를 통하면 동적으로 엔티티그래프도 사용가능.
이미 초기화 되어있으면 새로 로딩해오지는 않는다.








