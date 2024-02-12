# 3장 설계 원칙

SOLID
- 함수와 데이터 구조를 클래스로 배치하는 방법
- 클래스를 서로 결합하는 방법을 설명해준다.
- GOAL: 변경에 유연하게
- GOAL: 이해하기 쉽게

SRP: 소프트웨어 모듈은 변경의 이유가 단 하나
OCP: 기존코드 수정 x 말고 새로운 코드 추가하는 방식으로 발전
LSP: 구성요소들은 서로 치환 가능해야한다. 상호 대체 가능한 구성요소로 소프트웨어 제작
ISP: 인터페이스 분리 원칙 - 사용하지 않은 것에 의존하지 않아야 한다.
DIP: 의존성 역전 원칙



# 4. SRP는 모든 모듈이 단 하나의 일만 해야 한다는 의미가 아니다. 그렇다면?


<details>

"함수"는 반드시 하나의, 단 하나의 일만 해야 한다는 원칙은 지켜야 하지만, SRP는 아니고 더 저수준이다.
- 응집성이 높아야 한다.
- 하나의 액터에 대해서만 책임져야 한다.
  - ex.) 다른 역할의 객체가 사용하는 다른 기능의 함수를 하나의 모듈이 다 들고 있으면 안된다.


</details>

# 5. 파사드 패턴을 사용해서 A가 사용하는 HourReporter 클래스와, B가 사용하는 EmployeeSaver의 파사드를 만들었다. SRP위반인가?

Employee
- reportHours
- saveEmployee

HourReporter
- reportHours

EmployeeSaver
- saveEmployee

<details>

Employee가 A, B 각 요청시에 HourReporter나 EmployeeSaver에게 적절하게 위임하는 형식의 파사드 패턴을 제작한다면, 

A나 B가 사용하는 유효범위 바깥의 클래스가 각 A나 B의 scope에 있는것이 아니기 때문에 SRP 위반이라고 보기는 어려울ㄹ듯하다

</details>

