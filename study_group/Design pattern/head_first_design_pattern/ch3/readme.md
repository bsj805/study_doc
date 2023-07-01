### 1. new를 쓰지 않고 팩토리 메서드를 사용하게 된 이유는?

<details>
<summary> 정답: </summary>
- new를 쓰면 구상클래스에 직접적으로 의존을 하게 되기 때문 <br/>
- 특정 type에 따라 다른 new를 쓰게 된다면 , 비슷한 코드가 우후죽순 생기게 된다. (피자를 사용하는 곳이 pizzastore 뿐만 아니라 PizzaDescription 등도 있는 경우 )<br/>
</details>

### 2. 문제 2

PizzaStore는 Pizza를 만드는 createPizza() 메서드를 만들었다. <br/>
createPizza() 메서드안에서는 매장별로 같은 주문에도 다른 스타일로 Pizza를 만들수도 있다. (NY지점은 NY Style로 CH지점은 CH style로)<br/>
PizzaFactory를 언제 initialize하게 짜야될까? <br/>


<details>
<summary> 정답: </summary>
- 특정 PizzaStore을 initialize할 때 PizzaFactory를 가지고 있으면 되겠다. <br/>
<br/>
</details>

### 3. 문제 3

왜 dependency inversion 이라고 할까요?

```java
public abstract class PizzaStore {
    public Pizza orderPizza(String type) {
        Pizza pizza;

        pizza = createPizza(type);

        pizza.prepare();
        pizza.bake();
        pizza.cut();
        pizza.box();

        return pizza;
    }

    protected abstract Pizza createPizza(String type);
} 
```

<details>
<summary> 정답: </summary>
- createPizza 대신에 type이 cheese 일때 pizza = new CheesePizza()를 일일이 하게 했다면 CheesePizza의 변화가 직접적으로 PizzaStore에 영향을 미친다. ex. 생성자 인자추가 <br/>
- 하지만 추상화를 해서, pizza라는 추상화 객체를 두어서 pizza를 뱉어내는 팩토리를 만들었다. 그러면 CheesePizza의 변화는 Pizza class에만 영향을 미친다. <br/>
- 또한, PizzaStore는 더이상 CheesePizza의 변화는 상관이 없고, Pizza class의 변화에만 상관이 있다. 즉 고수준 구성요소 pizzaStore가 저수준 구성요소인 pizza에만 의존한다.    <br/>
</details>

### 4. 문제 4

팩토리 패턴이 느슨한 결합을 하게 해주는 이유?

<details>
<summary> 정답: </summary>
- 클래스의 생성자부분만 신경쓰게 하고, 구상클래스는 어떤 메서드를 추가하던 상관없다. pizza.bake() 말고도 CheesePizza 자체 클래스만 수정해서 screma() 메서드를 만들어 피자가 소리지르게 만들어도 된다.<br/>
</details>

### 5. 문제 5.

팩토리를 써서 캡슐화 하는 것은 무엇일까요?


<details>
<summary> 정답: </summary>
객체의 생성 부분을 캡슐화. 로직에서 분리시킬 수 있다. <br/>
</details>