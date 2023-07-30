1. 우리 팀장님은 박스를 포장할 때만 빼면 꽤 괜찮은 분이죠. 박스를 포장해야 할 때면 꼭 어디론가 사라지더라구요.

이 말에 담긴 템플릿 메서드 패턴과의 유사성은?



<details>
<summary> 정답: </summary>
'박스를 포장한다' 라는 세부 작업을 할 때에는 직원(서브 클래스)에게 맡긴다 <br/>
</details>


2. 책에서는 템플릿 메서드 패턴을 이용해서 다음 boil 과 pourInCup() 메서드를 효율적인 구조로 변경한다. 우리가 배운 다른 패턴을 사용한다면?
```java
public class Tea {
    void prepare(){
        boil();
        steepTeaBag();
        pourInCup();
        addLemon();
    }
    
    public void boil(){...}
    public void steepTeaBag(){...}
    public void pourInCup(){...}
    public void addLemon(){...}
    
}
```
```java
public class Coffee {
    void prepare(){
        boil();
        brewCoffeeGrinds();
        pourInCup();
        addSugarAndMilk();
    }
    
    public void boil(){...}
    public void brewCoffeeGrinds(){...}
    public void pourInCup(){...}
    public void addSugarAndMilk(){...}
    
}
```


<details>
<summary> 정답: </summary>
- boil 과 pourInCup을 공통으로 사용하려면 데코레이터 패턴을 사용할 수 있겠다. 다만 순서는 팩토리패턴 등으로 보장해야 할것.<br/>

```java
BoilDecorator( 
    steepTeaBagDecorator(
        PourInCupDecorator(
            LemonDecorator(
            )
        )
    )
 )
```
그래서 prepare() 메서드를 여러번 데코레이트 함으로써 prepare() 메서드만 호출해도 Boil, SteepTeaBag, PourInCup, addLemon 할 수 있게 된다.<br/>

단점은? 클래스 개수가 너무 늘어나고, 순서 보장어렵고. <br/>

</details>

3. 카페인 음료에 "핫식스" 가 생기면서 물을 끓이는 과정이 원래 최상위 슈퍼클래스의 메서드였는데, 핫식스의 레시피는 물끓이기도 없고, 과정이 단순하다 각 솔루션 별 문제점은?

기존:
```java
public abstract class CaffeineBeverage() {
    void prepare() {
        boil();
        brew();
        pourInCup();
        addCondiment();
    }
    void boil();
    void pourInCup();
    abstract void brew();
    abstract void addCondiment();
}
```

핫식스의 prepare():
```java
    void prepare() {
        pourInCup();
    }
```

3.1  CaffeineBeverage와 공통점이 하나밖에 없으니 이 클래스를 상속받지 않는다.

<details>
<summary> 3.1정답: </summary>
- CaffeinBeverage와 같은 클래스가 아니라 prepare()메서드가 있음을 보장할 수 없다. 유지보수가 어려워진다. <br/>
</details>

3.2 CaffeineBeverage를 상속받되, brew()를 prepare에서 호출한 것이 아니라면 주문이 잘못들어온거니까, <br/>
(`StackTraceElement[] stackTraceElements = Thread.currentThread().getStackTrace()` 으로 호출메서드 파악) <br/>
Coffee 객체를 생성해서 Coffee.prepare()을 불러 커피를 반환해준다.

<details>
<summary> 3.2정답: </summary>
- 디미테르 법칙 위반한거 빼고는 문제가 있을까?  <br/>
</details>

3.3 prepare()메서드 자체를 오버라이드 해서 pourInCup() 만 사용하게 한다.

<details>
<summary> 3.3정답: </summary>
- pourInCup만 사용하게 오버라이드 한다면 템플릿 메서드를 위반하게 된다. 알고리즘의 각 단계를 정의할 수 있게 해주는게 템플릿 메서드라 오버라이드 하면 안된다. 모두 같은 prepare()메서드가 호출될 것을 알아야 한다. <br/>
</details>
