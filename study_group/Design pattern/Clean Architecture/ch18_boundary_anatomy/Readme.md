소스코드의 의존성 관리
- 소스 코드 모듈 하나 변경시 의존하는 다른 모듈도 변경하게 되는데, 이런 변경이 전파되는 정도를 막는 것이 이 경계선이다.

# 1. 가장 단순한 형태의 경계 횡단은 저수준 클라이언트에서 고수준 서비스로 향하는 함수 호출이다. 저수준 클라이언트? 고수준 서비스는 어떻게 나뉠까?

<details>

고수준은 저수준보다 더 높은 추상화 수준을 제공하며, 개발자가 하드웨어나 시스템 리소스에 대한 세부 사항을 신경 쓰지 않고 작업하게 한다. 

저수준은 직접적으로 코드를 호출하는 부분이다. DB를 다루는 sql이 있다던가 등. (구체적인 기술에 종속적임) 입출력과 가까울수록 저수준인것.

저수준 클라이언트에서 고수준 서비스로 향하는 함수 호출이라면, mysql의 sql문을 보내서 mysql측의 INSERT 서비스를 작동시키는 예시?

고수준 클라이언트가 저수준 서비스를 호출한다는 것은, 자바 SERVICE에서 REPOSITORY IMPLEMENTATION 클래스의 함수 호출하는 셈 (인터페이스를 거쳐서 통신할것.)

</details>



# 2. 회원가입하면 카프카를 통해서 회원정보를 보내고, 다른 컨슈머가 카프카를 통해 들어온 회원정보를 DB에 넣는 유즈 케이스가 존재한다. 
추상화 아이디어: RegisterService가 userRepository의 createNewUser를 부르도록 하자. 

UserRepository는 뒤의 DB가 mysql이어도 되고, 아무튼 유저 정보만 넣고, 반환받을 수 있으면 된다.

근데 위의 유즈케이스를 Kafka로 구현하려니, Kafka에 Repository가 종속적이라는 문제가 있다. 어떻게 풀 수 있을까?

```java
public class RegisterService{
    private UserRepository userRepository;
    
    public boolean registerNewUser(String Id, String password);
}

public class RegisterServiceImpl extends RegisterService{

    public boolean registerNewUser(String id, String password){
        this.userRepository.createNewUser(id, password);
    }
}

public interface UserRepository {
    boolean createNewUser(String id, String password);
}
public class KafkaUserRepository implements UserRepository{
    private KafkaStream kafkaStream; // 대충 kafkaStream 
    boolean createNewUser(String id, String password){
        // ?????????
    }
}

```


<details>

```java
public abstract class MessageStreamUserRepository implements UserRepository{
    
    private MessageStream messageStream; // kafkaStream, rabbitMQ 등 암튼 다른 메시지 큐 활용할 수 있는 클래스 
    public boolean createNewUser(String id, String password){}
} 

public class KafkaStreamUserRepository extends MessageStreamUserRepository {
    public boolean createNewUser(String id, String password){
        this.messageStream.sendUserInfo(id, password);
    }
}

```

UserRepository 밑에서 messageStream 용으로 하나를 팔수도 있지만, 사실 이 어플리케이션의 정체성은 메시지 큐로 메시지를 보내는 것이다.

고로, UserRepository를 만드는게 아니라  sendCreateNewUserMessage 이런 함수를 만드는게 낫겠다는 생각이 들었다.

```java
public interface MessageStreamUserRepository {
    private MessageStream messageStream;
    boolean sendCreateNewUserMessage(String id, String password);
}
```


</details>

