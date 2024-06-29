# 24. partial boundary

- 아키텍쳐 경계를 완벽히 만드는 것은 어렵다.
  - Input Ouput을 위한 데이터 구조, boundary interface 다 만들 수가 없다. 
  - 필요한 작업만 해야하는데! 



# 1. 파사드로 모든 서비스 클래스를 메서드 형태로 정의해 두고 클라이언트가 서비스 클래스에 접근할 수 없게 막는다면 단점은?


<details>
<summary> 정답 </summary>

Client가 모든 서비스 클래스에 대해 transitive dependency를 가져서, Client가 재컴파일 되야 한다. 
- 쌍방향 인터페이스를 만들어서 모든 서비스 클래스로 들어가는 interface, 나가는 interface를 활용할 수 없다면 결국 겪는 문제중 하나이다.

</details>


