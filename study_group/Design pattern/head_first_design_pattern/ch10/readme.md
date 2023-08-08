1. 상태 패턴을 사용하는 것으로 바꾸게 된다면, 상태는 어떤 구조로 사용되고, 어떻게 바뀌는가





<details>
<summary> 정답: </summary>
1. context 객체를 만들어서, state를 담고 있을 수 있게 한다. 각 상태객체가 context객체의 상태를 변경할 수 있다. <br/>
</details>


2. 기존 상태에서는 하나의 클래스 안에 state를 바꾸는 행동 4가지가 모두 들어있었고, 상태패턴으로 바꾸면서 상태를 바꾸는 행동 4가지가 각 클래스로 분산되었다. 응집도의 관점에서 어떤 변화가 일어난 것인가?

```java
final static int SOLD_OUT = 0;
final static int NO_QUARTER = 1;
final static int HAS_QUARTER = 2;
final static int SOLD = 3;
```


<details>
<summary> 정답: </summary>
1. 기존에는 서로 다른 기능을 하는 코드가 하나의 클래스 안에 들어있었다. 즉 응집도가 낮다고 볼 수 있다. (연관된 기능이 모여있어야 응집도 높음) <br/>
2. 하나의 기능을 맡는 코드만 존재하는 상태 클래스의 응집도가 높다.<br/>
</details>

3. 상태 패턴의 주요 구성요소 - 클라이언트, context, state가 존재한다. 각 구성요소의 관계는?

<details>
<summary> 3정답: </summary>
- 클라이언트는 context를 호출. context는 state를 가지고 있고, state는 context의 state를 변경하는 함수를 갖는다. <br/>
</details>


4. state들인 `ConcreteStateA` `ConcreateStateB` 클래스는 상태를 바꾸는 함수로 handle()을 갖고있다. handle()함수를 알고 있는 (호출할 수 있는) 범위는 어떤 대상까지일까? (클라이언트, context, state, ConcreteStateA, ConcreteStateB) -

<details>
<summary> 4.정답: </summary>
- 클라이언트는 state가 관리되는지 모른다. context는 State 라는 인터페이스를 통해 state객체에게 위임할 수 있으며, ConcreteStateA와 ConcreteStateB도 서로 호출 가능하다. <br/>
</details>

5. 상태 전환정보가 state 클래스에만 존재하는데 어떤 문제가 생길 수 있을까요, Context객체에서 진행하도록 한다면 어떤 장단점이 있을까요? (책 문제)

<details>
<summary> 5.정답: </summary>
- 장점: 상태 전환정보가 Context객체에서 진행된다면 특정 함수가 불렸을때 상태를 전환한 다음, 해당 상태의 동작만을 호출하는 방식이 될 것임. == 어떤 상태에서 어떤 상태로 변화가 일어나는지 알 수 있음 <br/>
- 단점: 상태 전환정보가 Context객체에서 진행된다면, Context객체는 변화에 닫혀있다. 새로운 상태 추가할 때 state의 sub클래스만 추가하고 sub크래스들만 고치는게 아니라, Context객체의 if문도 다 바꿔줘야 할것. <br/>
</details>

6. 왜 GumballMachine 객체의 인스턴스를 여러개 만들면, 상태 인스턴스를 정적 인스턴스 변수로 만들어 공유하라고 하는가? 각자 갖고있어야 하는거 아닌가?