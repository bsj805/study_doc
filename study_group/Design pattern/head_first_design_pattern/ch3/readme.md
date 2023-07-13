1. A 클래스가 추상 구성 요소이고, B 클래스는 A를 상속하는 구상 구성 요소이다. C 클래스가 decorator 패턴을 써서 B 클래스를 decorate하기 위한 C클래스의 조건은?

<details>
<summary> 정답: </summary>
우선 C 클래스는 A클래스를 상속받아서 B클래스가 가지고 있는 모든 메서드를 오버라이드 해야 한다.  <br/>
하지만 decorator를 여러개 두기 위해서는 decorator 패턴을 추상클래스로 가지는 D 추상 데코레이터 클래스를 가지는 것이 좋다. <br/>

그렇기 때문에, A 추상 구성 요소를 상속받는 D 추상 데코레이터 클래스를 상속하는 C 클래스를 만들어, 구상 데코레이터 역할을 하게 해야 한다. <br/>

</details>


2. 구성으로 객체의 행동을 확장한다는 것의 예시가 어떤 것이 있을까요?

<details>
<summary> 정답: </summary>
- observer 패턴처럼 다른 객체를 인스턴스 변수로 들고 있을 수 있게 하는 것 <br/>
- strategy 패턴처럼 행동을 다른 객체에게 위임함으로써 동적으로 객체의 행동을 달리할 수 있는 것 <br/>
</details>


3. 다음중 decorator 패턴으로 구현하기 좋아보이는 task는 ? (정답 딱히 없음)

- 사용자 요청 중 악성 요청을 필터링 해야하는 rest api <br/>
- 하나의 DB에 json 타입의 데이터를 insert할 때 조건에 맞는지 파악해야 하는 경우 <br/>
- 오리 객체를 만들어서, 나는 행동을 구현해야 하는데, 날 때 나는 소리를 오리 종류에 따라 다르게 내야 하는 경우 <br/>

<details>
<summary> 정답: </summary>
- Rest API 의 웹 필터의 경우 결국 response를 대응하는 객체를 가진 여러개의 decorator가 있으면 도움이 된다. ip 기반 필터링, query 기반 필터링 등등 <br/>
- Insert 할때에, 여러 조건에 맞는지 판단하는 decorator를 insert 함수에 대해서 계속 구현 한다면 조건에 맞지 않으면 fail하는 것을 쉽게 구현할 수 있을 듯 하다 <br/> 
</details>


4. 책속의 커피예제를 똑같이 사용한다. 단, 가격을 올바르게 표시하는 것만이 관심사라고 할 때, int형으로 mocha , whip, soy, 각 옵션의 개수를 최상위 클래스인 beverage가 갖고있게 하고, cost는 클래스의 static 변수인 hashmap을 통해
매번 계산하게 한다면 decorator 패턴과 비교해서 어떤 장점과 단점이 있을까?

<details>
<summary> 정답: </summary>
- 우선 클래스 개수가 늘어나지 않는다는 장점이 존재 <br/>
- 메모리 절약, 실행시간의 장점
단점<br/>
- 매번 옵션이 추가될 때마다 변수가 하나씩 추가된다. OCP(open close ) 를 지키지 않는다. <br/> 
- cost 함수 내부도 굉장히 복잡해진다. <br/>
- description을 추가해야 하는 상황이 생기면 뜯어 고쳐야 할 것 <br/>
</details>


5. 데코레이터 패턴을 사용할 때, 내부에 자기가 래핑한 객체에 대한 instance_of 를 사용해서 객체 별로 다른 동작을 하게 해도 된다? O/ X    

<details>
<summary> 정답: </summary>
- 그런 상황이 생긴다면, 내부의 객체에 위임했던 메서드의 결과물을 다시 고치는 방식을 사용해서 내부 객체에 대한 접근을 없애는 것이 맞다. - 모카모카 -> double mocha <br/>
</details>