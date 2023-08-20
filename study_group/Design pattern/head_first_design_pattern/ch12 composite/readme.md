1. quack() 메서드를 갖는 Quackable 인터페이스를 구현한 5마리의 duck이 있다. 이런 duck 인스턴스 하나가 생성될 때마다 count+=1 을 해서 duck 인스턴스의 수를 세고 싶다.

이때,  DuckObservable 로 구현을 해서 duck 인스턴스 생성시마다 observer에 등록한 뒤, observer에서 notifyObservers()로 신호를 받을 때마다 길이를 업데이트하는 방식으로 숫자를 세면 어떤 장단점이 있을까?
```java
public interface DuckObservable {
    public void registerObserver(Observer observer);
    public void notifyObservers();
    public void unregisterObserver(Observer observer);
}
```
```java
public interface Quackable {
    public void quack();
}
```

```java
public class RubberDuck implements Quackable, DuckObservable {
}
```
<details>
<summary> 정답: </summary>
장점: 추가적으로 duck이생길때마다 UI에 변화를 줘야 하는 등, 다른 observer로 확장성이 좋다. <br/>
단점: 실수하기 쉽다. duck자체가 Quack만 구현해야 하는 것으로 알 수도 있다. duck 클래스를 늘릴 때 실수로 DuckObservable을 추가 안 할 수도 있다.  <br/>

꼬리문제 2. 옵저버 패턴을 사용하는 상태에서 어떻게 개선할 수 있을까요?

<details>
<summary> 정답: </summary>

quack을 쓰는 duck들이 구현하도록 강제하면 된다. 

```java
public interface Quackable extends QuackObservable {
    public void quack();
}

```


</details>

</details>


3. quack() 메서드를 갖는 Quackable 인터페이스를 구현한 5마리의 duck이 있다. 이런 duck 인스턴스 하나가 생성될 때마다 count+=1 을 해서 duck 인스턴스의 수를 세고 싶다.

모든 Duck에게 아래 클래스를 상속받게 해서 count를 늘리는 것이 위 observable를 활용한 방법에 비해 어떤 장단점이 있을까요?

```java
public abstract class Duck implements Quackable{
    public static int count = 0;
    public void addDuckCount(){
        this.count+=1;
    }
}
```

<details>
<summary> 정답: </summary>
장점: Duck의 count를 얻어오는게 명확하다.  <br/>
단점: OCP. 확장에 닫혀있다. 만약 Duck에 대해서 숫자를 세는게 아니라, 가짜 DUCK에 대해서만 세고싶다고 하면? static 변수가 계속 늘어날것이다.  <br/>
</details>

4. quack() 메서드를 갖는 Quackable 인터페이스를 구현한 5마리의 duck이 있다. 이런 duck 인스턴스 하나가 생성될 때마다 count+=1 을 해서 duck 인스턴스의 수를 세고 싶다.

이번엔 책처럼 데코레이터를 사용해서 Duck의 수를 셀 것이다.

```java
public class QuackCounter implements Quackable{
    Quackable duck;
    static int numberOfDucks;
    
    public QuackCounter (Quackable duck) {
        this.duck = duck;
        numberOfDucks+=1;
    }
}
```

그래서 `Quackable mallardDuck = new QuackCounter(new MalardDuck());` 이런식으로 호출하게 된다. 

그런데, 오리 연구소중 A 오리 연구소에서는 , 50마리 이상일 때에는 duck이 생성안되고 exception이 나면 좋겠다고 한다. 어떻게 구현할 수 있을까?

<details>
<summary> 정답: </summary>
팩토리 메서드를 만들어서 A 오리 연구소 전용 팩토리를 제공한 뒤, 팩토리에서 생성해보고 난 뒤 51개라면 지금 생성한 객체를 지우고 exception을 일으킬 수 있겠다. <br/>

5. 꼬리문제: 다른 TooManyDuckCounter(Quackable duck) 데코레이터를 만들어서, QuackCounter의 numberOfDucks를 확인해서 사용하는 방식은 어떤 문제가 있을까?


<details>
<summary> 정답: </summary>
Decorator 패턴은 자기가 어떤 데코레이터를 갖고있는지 모르는 방식이 좋은 방식이다. QuackCounter을 안 씌운 Duck이 들어오면 어떡하는가? <br/>

</details>

</details>
