1. 중복된 코드 조각을 함수로 빼내는 것의 이점 (2가지)

<details>
<summary> 정답: </summary>
1. 코드 이해하는 비용을 줄인다. 이를테면 함수 이름만 보고도 어떤 역할을 할 것이라는 짐작이 가능하다면 굳이 그 함수의 내부를 보지 않는다 <br/>
2. 유지보수 비용을 줄인다. 특정 코드가 고장났으면 비슷한 코드를 다 보면서 고쳐야 한다. <br/> 
</details>

2. 리팩토링에서 테스트를 만들어두는 것의 이점 

<details>
<summary> 정답: </summary>
1. 리팩토링 이후에 테스트 코드를 돌려봤을 때 문제가 없으면 그냥 잘 변경되었다고 믿고 진행할 수 있다. <br/>
</details>

3. 디미테르의 법칙을 지키기 위해서 해주어야 하는것은?
```java
Answer answer = answers.get(criterion.getAnswer().getQuestionText());
```

<details>
<summary> 정답: </summary>
다른 객체의 코드를 이 코드에서 부르는 일이 없도록 해야한다. criterion의 함수를 불러서<br/>
```<br/>
Answer answer = answerMatching(criterion)<br/>
```<br/>
이런식으로 아예 위임을 시키도록 한다.
</details>

4. A씨는 열심히 리팩토링에 신경을 쓰다가 다음과 같은 의문을 품게 되었습니다 
"
어라 성능상으로 따지면 하나의 for문안에서 다 처리하면 
해시맵에 접근해서 객체를 assign 하는게 한번뿐이니까 더 좋은데, 메서드 각각이 for문을 갖게하면
for문이 3번 더 실행되어서 해시맵에 접근해서 하는 객체 assign이 3번이나 있으니 성능상 더 안좋아지는데?
"
A씨에게 조언을 한다면 어떤 조언들을 해줄 수 있을까요?

<details>
<summary> 정답: </summary>
1. 정말 성능에 문제가 크다면 고칠 방법을 찾을 때에 각각 메서드의 성능향상 방법을 쉽게 찾을 수 있으니 괜찮다 <br/>
2. 일반적으로 코드의 성능이 그렇게까지 나빠지지 않는다. <br/>

</details>


문제 낼거 없어서 냅다 4장문제 리뷰

# 4장

1. 다음 테스트 수도코드에서 4장과 관련되어 논의될만한 사항을 짚어보시오 (4개)

```java
public class BankOperationTest {
    
    @Test
    public void getHashTest(){
        Json content = GET("http://localhost:8080/get/json").getbody(); //대충 GET
        String importantContent = content["secure_content"];
        String sha256Content = content["SHA256"]; //sha256
        assertEquals(sha256Content, generateHash(importantContent,"SHA256"));
    }
    @Test
    public void getHash2Test(){
        Json content = GET("http://localhost:8080/get/json").getbody(); //대충 GET
        String importantContent = content["secure_content"];
        String sha256Content = generateHash(importantContent,"SHA256");
        assertNotEquals(sha256Content,importantContent);

    }
}
```

<details>
<summary> 정답: </summary>
* 비용이 비싼 sha256 해시값 계산, API요청을 매번 하는 대신 한번에 모든 비싼 operation을 진행하는 것이 좋겠다.<br/> 
    - Junit4의 `@BeforeClass`와 동일하게, Junit5에서 `@BeforeAll`을 사용해서 초기화를하는 것이 좋겠다 <br/>
* 메서드 이름을 given, when, then 형식으로 바꾸는 것이 좋겠다. <br/>
    * 보통 when, then <br/>
* Arrange와 Act와 Assert를 각각 \n으로 분리시켜두는 것이 좋겠다. <br/>
* generateHash같은 private 메서드까지 테스트가 되어야 하는지 잘 생각해보는 것이 좋겠다. <br/>
    * 내부의 세부 사항을 테스트 하는 것은, 깨진 테스트를 변경할 때마다 복구해야 함을 의미하는데, 리팩토링을 줄이게 하는 이유가 된다. <br/>
    * private 메서드를 테스트하고 싶다면 새로 `HashClass`를 제작해서 해당 클래스의 public 메서드로 `generateHash`를 제작하는 것이 좋겠다. <br/>
    * private 메서드가 테스트할만큼 중요하거나 복잡해졌다면 SRP(single responsibility principle)을 위반한 경우가 많을 것. <br/>
</details>

