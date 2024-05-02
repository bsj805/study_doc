1. 싱글턴 패턴의 유즈케이스에는 어떤 것이 있을까?


<details>
<summary> 정답: </summary>
- 쓰레드 풀 <br/>
- http 커넥션 풀 <br/>
- 스케줄러 (crontab을 등록한다던지)  <br/>
</details>


2. 직렬화/역직렬화 할때 singleton이 안되는 이유는? 

<details>
<summary> 정답: </summary>
- singleton을 직렬화 시키고, 다시 역직렬화 할 때, 다른 메모리 공간에 쓰이기 때문이다. <br/>

</details>

3. 같은 클래스 타입으로 여러개의 레지스트리를 생성하고 싶을 때 어떻게 해야 하는가? 

<details>
<summary> 정답: </summary>
- 2가지 방법이 있을 수 있겠다. <br/>
- 1. 각 레지스트리를 다른 클래스로더에서 부를수 있게 한다.  <br/>
- 2. 하나의 싱글턴 클래스 안에 여러개의 레지스트리를 두게 하고, 각 레지스트리를 반환하는 함수를 다르게 한다 - getInstanceOf123 <br/>
</details>


4. 싱글턴 패턴으로 제작된 클래스를 상속받아 서브클래스를 만들고 싶을 때 문제점?

<details>
<summary> 정답: </summary>
- 생성자가 private - protected나 public이 되는순간 싱글턴이 깨짐 <br/>
- 모든 서브클래스가 똑같은 인스턴스 변수를 공유하기 때문에 베이스 클래스에서 레지스트리 같은걸 구현해야 한다. <br/>
</details>

5. 전역변수로 안하는 이유는?

<details>
<summary> 정답: </summary>
- 게으른 인스턴스 생성이 불가능 <br/>
- 클래스가 하나의 인스턴스만 생성되도록 강제하지 못한다. <br/>
- 전역 레퍼런스가 너무 여러개 생기면 네임스페이스가 지저분하다.  <br/>
</details>
