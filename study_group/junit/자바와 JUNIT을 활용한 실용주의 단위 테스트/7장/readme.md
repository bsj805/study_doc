1. 다음 소스코드를 보고 문제를 푸시오
1.1 Rectangle 클래스의 존재 이유가 무엇일까요?<br/>
1.2 `RectangleTest`는 CORRECT 중 어떤 속성을 검증하고 싶은 것일까요? <br/>
1.3 이사람은 왜 A 와 같이 하지 않고, B와 같은 사용자 정의 매처를 사용했을까요? <br/>
   (각 test마다 생성된 직사각형의 각 변이 100보다 작은 크기라는 것을 테스트한다.) - FIRST, RIGHT-BICEP, correct <br/>

A. 직접 테스트 
```java
public class RectangleTest{
    private Rectangle rectangle;
    
    @After
    public void ensureInvariant() {
        assertEqual(Math.abs(rect.origin().x - react.opposite().x) <= 100 && 
                    Math.abs(rect.origin().y - rect.opposite().y) <= 100
        ,true);
    }
    @Test
    public void testCreateRectangle(){...}
    @Test(expected=RectangleOutOfRangeException.class)
    public void throwsOnZeroEdge(){
        new Rectangle(4,4,4,6);
    }
}
```
B. hamcrest matcher 제작
```java
public class ConstrainsSidesTo extends TypeSafeMatcher<Rectangle>{
    private int length;
    
    public ConstrainsSidesTo(int length){
        this.length = length;
    }
    @Override
    public void describeTo(Description description){
        description.appendText("both sides must be <=" + length);
    }
    @Override
    protected boolean matchesSafely(Rectangle rect){
        return(
                Math.abs(rect.origin().x - rect.opposite().x) <= length && 
                Math.abs(rect.origin().y - rect.opposite().y) <= length
                );
    }
    @Factory
   public static <T> Matcher<Rectangle>
                constrainsSidesTo(int length){
        return new ConstrainsSidesTo(length);
    }
}
```

<details>
<summary> 1.1정답: </summary>
Rectangle 클래스가 있어 Range를 잘 지키고 있는지 따로 검사하지 않아도 된다.<br/>
 <br/> 
</details>
<details>
<summary> 1.2정답: </summary>
값이 `Range` 안에 있는지를 체크하기 위함이다.  <br/>
 <br/> 
</details>
<details>
<summary> 1.3정답: </summary>
의미 있는 메시지를 담은 describe to 덕분에 어떤 부분이 틀렸는지 명확히 알 수 있다. self-validating<br/>
 <br/> 
</details>

2. 아래 자바 함수에서의 sideEffect는 무엇인가?
```java
    @Test
    public void allowsShiftToParkWhenNotMoving(){
    transmission.shift(Gear.DRIVE);
    car.accelerateTo(30);
    car.brakeToStop();
    transmission.shift(Gear.PARK)
    assertThat(transmission.getGear(), equalTo(Gear.PARK))
        }
```
<details>
<summary> 2정답: </summary>
Side Effect는 호출 행동의 결과로 발생하는 상태 변화들이다. <br/>
여기서는 transmission의 GEAR가 DRIVE로 바뀐것, PARK로 바뀐것<br/>
car의 속도가 30으로 올라가고 0으로 바뀐 것 이 모두 side effect에 포함된다.<br/>
이들중에 검사가 필요한 것이 있다면 검사를 해야 한다.
</details>

3. 사용자가 년도를 입력할때     "[0-9]{4}[ ]*년" 이란 Regex에 match하는지 여부를 검사했다.
이는 right BICEP, CORRECT 중 어떤 특징을 검사하기 위함인가?

<details>
<summary> 3정답: </summary>
Boundary Condition, Conformance이다.  <br/>
</details>
