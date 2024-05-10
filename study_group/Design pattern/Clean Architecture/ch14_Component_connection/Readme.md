ADP: 의존성 비순환 원칙
SDP: 안정된 의존성 원칙 - 더 안정된 쪽에 의존하라.


# 문제 1. 컴포넌트 단위 릴리즈가 가능한 전제조건은?


<details>
<summary> 내가 생각하는 정답 </summary>

- 릴리즈 단위로 배포해도 컴포넌트가 동작 가능하도록 컴포넌트 사이의 의존성 순환이 없어야 한다. 
  - 의존성 그래프가 DAG로 만들어져야 한다. (Directed Acyclic Graph, DAG)
- 매번 내 프로젝트에 의존하는 대상들이 릴리즈 적용을 해줘야 한다.   

</details>

# 2. A->B->C 형태로 의존하는 컴포넌트들이 있다면 어디부터 시스템 전체 릴리즈 테스트가 이뤄져야 하는가?

<details>
<summary> 정답 </summary>

C가 가장 작은 형태의 컴포넌트라는 것이기 때문에, C에 대한 테스트부터 이뤄져야 한다.

</details>

3. 다음을 DAG로 만드는 법은?

```java

// Entities 컴포넌트

class User {
    String id;
    String pw;
    Int score;
    Boolean addScore(String pw, int score){
        if (AuthClass.isValidId(newId, this.pw)){
            this.score += score;
      }
    }
}
// Auth 컴포넌트
class AuthClass {
    UserDataStorage userDataStorage;
    
    Boolean isValidId(String id, String pw){
      userDataStorage.validityCheck(id, pw); //user정보를 조회해서 일치하는 지 확인
    }
    Boolean addNewUser(User user){
        userDataStorage.save(user.id, user.pw);
    }
}


```

<details>
<summary> 정답 </summary>

User 클래스에서 AuthClass에 대한 의존성이 역전되게 만들어야 한다.

기존 문제점: 

- 현재 User 클래스에서 전화번호가 추가된다고 했을 때, 
- AuthClass 버전이 바뀔때 isValidId 인자로 전화번호도 받기로 했다면
  - Authclass의 isValidId에 전화번호를 추가하려면 User에 이미 전화번호가 있어야 하는데 (addNewUser로 user.telephone 을 더해야함)
  - User에서도 isValidId를 사용하고 있기 때문에 Authclass.isValid(id, pw, 전화번호) 로 변경해야 하는 문제.
  - 동시에 컴포넌트가 업데이트되지 않으면 한쪽에러나서 실행안되고 있음.

```java
class User {
    String id;
    String pw;
    Int score;
    AuthenticateService authenticateService;
    Boolean addScore(String pw, int score){
        if (authenticateService.isValidId(newId, this.pw)){
            this.score += score;
      }
    }
}

interface AuthenticateService {
    
    Boolean isValidId(String newId, String pw);
}

// Authentication 컴포넌트
class AuthClass implements Entities.AuthenticateService{
  UserDataStorage userDataStorage;
  Boolean isValidId(String newId, String pw){
      //~~
  }
  Boolean addNewUser(User user){
    userDataStorage.save(user.id, user.pw);
  }
}

```

이러고 user 생성자에다가 AuthClass를 넣어주면 되겠다.

만약 isValidId의 인자가 바뀐다고 하면, User쪽이 먼저 업데이트 해서 버전을 내놓으면, 해당 버전에 맞춰서 개발.

 

</details>


# 4. 안정성을 표현하는 지표와, 안정적인 컴포넌트의 특징은? 
# 5. 정책결정을 해야 되는 소프트웨어는 어떤 컴포넌트에 위치해야 하는가?

<details> 
<summary> 정답 </summary>

FAN-IN이 많을 수록 안정적인 컴포넌트이다. ( 잘 안 바뀔 것 )

FAN-OUT이 많을 수록 불안정한 컴포넌트이다 ( 잘 바뀔 것 )
 - 의존하는게 많다. 

FAN_OUT / (FAN_IN + FAN_OUT) 이 0에 가까울수록 안정적인 컴포넌트인것.

FAN_OUT이 적은 안정된 컴포넌트에 고수준 정책이 위치해야 하는데, 그럼 정책 바꾸기가 어렵다. 그러면 OCP를 통해서 유동적으로 바꿀 수 있게 하면 된다. (추상 클래스) 

불안정한 컴포넌트는 구체 컴포넌트여야 한다. (쉽게 변경이 가능한)

</details>

A는 추상화정도 1에가까울수록 추상클래스 
