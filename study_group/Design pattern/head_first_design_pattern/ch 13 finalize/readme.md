1. list를 소팅할때 compareTo(A, B) 를 가지는 Comparable을 구현한 인자를 필요로 한다. 이같은 방식은 어떤 패턴일까?

```java
public interface Comparable {
    public void compareTo(String a, String b);
}
```

<details>
<summary> 정답: </summary>
템플릿 메서드 패턴, 최상단 함수에서 서브클래스가 그 행위를 결정하게 한다. <br/>

</details>


2. 위키피디아 페이지를 파싱해서 "아이유의 나이 30살"과 같은 정보를 얻는 프로그램이 있다. 이 프로그램에서 파싱된 값이 다양한 조건에 맞는지 검증해야 하는 상황이고, 검증이 틀리면 값은 바로 ""로 반환해버리면 된다.
 
조건이 계속 추가될 수 있는 상황이고 순차적으로 적용이 되어서 어떤 결과에서 실패했는지 확인하고 싶다면 어떤 패턴이 걸맞을까?

조건:
- 길이가 몇 이하
- regex 에 맞는지 확인
- 지식백과를 파싱해서 나온 아이유의 나이 값과 일치하는 지 확인
- ...

<details>
<summary> 정답: </summary>
상태패턴: if문이 엄청 여러개 나올텐데 각각을 하나의 상태로 하고, 차례대로 검증을 수행하면 된다. (한 상태에서 다음 상태로 넘긴다. ex. nullState -> lengthConstraintPassState -> regexConstraintPassState ... <br/>
</details>

3. 위키피디아 페이지를 파싱해서 "아이유의 나이 30살"과 같은 정보를 얻는 프로그램이 있다. 이 프로그램에서 파싱된 값이 다양한 조건에 맞는지 검증해야 하는 상황이고, 검증이 틀리면 값은 바로 ""로 반환해버리면 된다.

조건이 계속 추가될 수 있는 상황이고, 조건의 검증 순서는 상관이 없다. 다른 쓸만한 패턴이 있을까? 

<details>
<summary> 정답: </summary>
데코레이터 패턴도 괜찮겠다. value를 가진 객체를 감싸는 validator을 계속 감싸서 결과값만 얻으면 된다.  <br/>

4. 만약 데코레이터 패턴으로 열심히 다 바꿔서 만들었는데 검증이 어디서 실패하는지 동적으로 확인할 수 있으면 좋겠다고 한다. 어떤 방식으로 해결할까? 

```java
public class WikipediaParseResult extends ParseResult{
    public String parsedValue; // "아이유 나이 30살" 따위가 들어있다. 
}
```

```java
public class LengthValidityConditionChecker extends ConditionDecorator{ // ConditionDecorator는 ParseResult를 extends
    public String parsedValue; // "아이유 나이 30살" 따위가 들어있다. 
    public LengthValidityConditionChecker(String parsedValue){
        this.parsedValue = parsedValue;
    }
    public getResult(){
        if (parsedValue.length() < 10) {
            return ""; // 통과못함
        }
        return parsedValue;
    }
}
```

<details>
<summary> 정답: </summary>
1. 로깅용 싱글톤 객체를 사용해서 남긴다. (hash map 형태로 해도 되고) <br/>
2. parsedValue 만 데코레이터 사이를 떠도는게 아니라, `String failureReason` 같은 변수를 같이 가지는 객체 하나를 생성해서 같이 데코레이터에 품을 수 있게 한다. <br>
</details>


</details>


5. 패턴 카테고리의 용도가 뭔가?

<details>
<summary> 정답: </summary>
1.언제, 어떤 경우에 패턴 사용하는지 알기 <br>
2 도입했을 때 장단점 알기 <br>
3. 패턴 도입시의 클래스 다이어그램. <br>

</details>


