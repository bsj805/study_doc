1. 원격 호출을 완전히 투명하게 처리할 수 있을지? 정말 좋을지? 어떤 문제가 생길지?

<details>
<summary> 정답: </summary>
가능성: 아예 투명성을 높인다면, 내부 코드는 모두 네트워크 통신이라는 가정하에 짜여질 것.  <br/>
장점: 클라우드로 올려서 MSA하기 좋을듯 <br/>
단점: 로컬에서만 돌아가도 되는 코드라면 복잡성 & 수행시간 늘어난다.  <br/>
</details>

2. 책에서는 여러개의 GunBallMachine에 접속해서 모니터링 정보 내보낼때 rmi registry를 세개 실행시켜서 각각 실제 구현체가 등록되어있게 했다. 왜 그럴까?
```java
String[] location = {"rmi://santafe.com/gumballmachine" , "rmi://boulder.com/gumballmachine", "rmi://austin.com/gumballmachine"}
```

<details>
<summary> 정답: </summary>
서버가 실행되는 곳에 rmi registry가 있는게 일반적. 결국 JVM heap에 있는 주소에 대한 stub을 만들어줘야 한다.  <br/>
또한, 같은 코드로 static 파일만 바꿔 여러개 등록시켜놓을 수 있다는 장점 <br/>
</details>

3. 직렬화해서 Serializable extends 할 때, SerivalVersionUID = 1L; 이거 왜만들까?

<details>
<summary> 정답: </summary>
직렬화 할 때와 역직렬화 하는 대상 클래스가 같은 버전의 클래스 코드인지 확인 할 수 있다 <br/>

```java
컴파일러가 자동으로 생성하는 방법은 클래스를 보고서 만드는데 참조하는 요소는 아래와 같다.

1. 클래스 이름 (fully qualified)
2. 클래스의 접근 제한자 (public, final, abstract, 또 interface 여부)
3. 각 멤버 필드의 시그너처 (이름과 접근 제한자, 타입)
4. 각 멤버 메소드의 시그너처 (이름과 접근 제한자, 각 인자별 정보, 리턴 타입)
4. 각 생성자의 시그너처 (접근 제한자, 각 인자별 정보)
5. static initializer block 존재 유무
```

다만, 컴파일러 자동생성에 맡기게 되면, 컴파일러버전에따라, 같은 코드라도 역직렬화 불가능하다는 에러 날 수 있다.

</details>

4. RMI 와 RPC의 차이는?

<details>
<summary> 정답: </summary>
주요 차이는, https://www.geeksforgeeks.org/difference-between-rpc-and-rmi/

* RPC:
  - library 와 OS dependent
  - procedural programming
  - 보안성 x

* RMI:
  - java만 실행한다면
  - objective oriented
  - 얘가 더 효율적
  - RPC 다음 버전으로 제작됨.
  - 클라이언트단 security

</details>

5. 원격 프록시를 접근을 제어하는 프록시라고 할 수 있는 이유는?

<details>
<summary> 정답: </summary>
원격 객체로의 접근을 제어 할 수 있기 때문이다. 원래는 원격 객체에 대한 접근이 안되는건데 원격 프록시를 통해 가능해진 것이기 때문에  <br/>
</details>
