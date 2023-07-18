1. 다음 코드가 가지고 있는 문제점들은 어떤게 있을까요? 개선법은?

```java
public class Car {
    Engine engine;
    
    public Car(Engine engine){
        this.engine = engine;
    }
    
    public void start_roll(Key key){
        
        if (key.getType() == Key.AVANTE_TYPE){
            Motor motor = engine.getMotor();
            motor.start();
            
        }
    }
}
```


<details>
<summary> 정답: </summary>
engine.getMotor().start() 하는 코드이다. 최소 지식의 원칙을 따르지 않았다. <br/>
engine.start() 코드 안에 스스로의 motor.start() 를 넣는 방법이 있겠다.

```java
public class Engine {
    Motor motor;
    
    //생략
    
    public start(){
        motor.start();
    }
    
} 
```

</details>


2. 커맨드 객체 파트에서 등장했던 파사드 패턴은?

<details>
<summary> 정답: </summary>
- 가장 먼저 생각나는건 매크로 객체 <br/>
- 리시버들의 execute()함수 자체가 파사드 패턴이 될 수 있지 않을까. 내부 구현 모른채로 해당 클래스에서 실행해야하는 기능들을 집합시키니까. 서브클래스를 일일이 조작해도 된다. <br/>
</details>

3. 다중상속으로 어댑터를 구현하는 경우, client가 호출하는 것은 Target Class, Adapter Class, Adaptee 클래스 중 무엇인가? 

<details>
<summary> 정답: </summary>
- client는 항상 Target Class만을 호출한다. <br/>
- 결과적으로 봤을 때에는, Adapter Class가 Target Class를 상속했기 때문에 Adapter Class도 호출할 수 있다. <br/>
</details>


4. "파사드 패턴은 간단한 인터페이스를 구현해서 서브시스템 클래스들을 캡슐화한다. 파사드 클래스에 들어간 서브시스템 클래스들을 모른채로 서브시스템 클래스들의 기능을 사용할 수 있게 한다."

이 문구에서 틀린말은?

<details>
<summary> 정답: </summary>
- 서브시스템 클래스들을 캡슐화하지 않는다. 캡슐화를 하면 내부 구현을 감춘다는 뜻이고, 이는 언제든 서브시스템 클래스들을 직접 조작할 수 있게 하는 파사드 패턴과는 다르다. <br/>
</details>

5. 최소 지식의 원칙의 단점은?

<details>
<summary> 정답: </summary>
- 메서드 호출을 대신 처리해주는 래퍼 객체가 너무 많이 생길 수 있다. 시스템이 복잡해지게 된다. <br/>
</details>
