# 8장 스프링 클라우드 스트림

# 메시지 브로커, 메시지 기반 시스템의 핵심

리액티브는 I/O 작업이 많은 시스템에 적합하다. 메시지 중심의 통신에도 적합하다는 뜻.

마이크로서비스로 분할해서 위치 투명성(어디에서 실행되던 동일한 경험) 을 보장하는 탄력적인 시스템을 만들어야 한다.

## 서버사이드 로드 밸런싱
분산 시스템을 만들 때 그냥 서버 여러개 있으면 로드 밸런서 Nginx 하나 둬서 
- 외부 -> 서비스
- 서비스A -> 서비스B
- 서비스B -> 서비스A

다 처리하면 로드밸런서가 시스템의 병목이 될 수 있다. 
물론, 각 서비스에 얼마나 요청되는지 알 수 있으니까 pod autoscaling 등의 편의도 있다. 

## 스프링 cloud와 Ribbon을 이용해 클라이언트 사이드 로드 밸런싱

기존 문제는 외부요청 뿐만 아니라 각 서비스 사이의 요청조차 로드밸런서를 통해야 한다는 것.

따라서 서비스 A -> 서비스 B(인스턴스 4개) 의 경우를 생각할 때, 
서비스 A가 4개중 어떤 인스턴스로 보낼지 결정해서 호출한다. 

Ribbon은 서비스 A를 시작시킬 때부터 인스턴스 4개의 주소를 써준다.
- 192.168.0.2
- 192.168.0.3
- 192.168.0.4
- 192.168.0.5

서비스 A는 일정 주기로 각 인스턴스의 load가 얼마나 되는지 pull을 해오게 된다. 

단점: 
- 모든 서비스 A가 동시에 pull을 하게 된다면 서비스 B - 인스턴스 1 이 동시에 최저 사용량으로 보이게 된다
- 모든 서비스 A가 인스턴스 1에 보내게 되면서 인스턴스 1이 과부하 발생해버린다.
- 새로 서비스 B 인스턴스 추가하려면 A를 다시 켜야 한다.

### 유레카 등장!

유레카는 서비스 레지스트리 서비스로, 서비스 목록을 계속 업데이트해서 가용량 등의 상태정보를 가진다. 
- heart beat를 계속 서비스와 주고받는다
- single point failure 이 될 가능성 높다. heartbeat방식의 고전적 문제점인데, 다운된 인스턴스에 계속 메시지를 보내고 있을 수 있다.
  - 다만 서버 단위 로드밸런싱을 할 때는 요청 하나 보냈는데 timeout나면 거기로 안보낼 수 있지만, clientside는 계속 같은 client를 받아오는 유레카 때문에 망할수도 있다.

## 탄련적, 신뢰성 있는 메시지 전달 계층 역할의 메시지 브로커

메시지 큐는 워커 하나가 메시지 요청할 때까지 기다린다
- 워커는 내부적으로 배압 관리 ( 메시지 안 원하면 안 받는다 ) 가능
- 메시지 큐는 병목이 되지 않는다. 
- 비동기적 논블로킹으로 메시지 큐에 넣을 수 있다.

메시지 브로커는 
- RabbitMQ
- Apache Kafka

# 스프링 클라우드 stream

스프링 Integration 모듈 + 스프링 메시지 모듈

비동기 메시지 서비스와 쉽게 통합 가능하다. 

- `@Output(Source.OUTPUT)` 은 메시지를 전달할 큐 이름을 정의한다.
- `@Input(Processor.INPUT)` 은 메시지를 받아올 queue 이름을 정의한다.

@EnableBinding(Processor.class)
뭐하는 애들이냐?

Message queue로 넣기만 하는 애들은
- @EnableBinding(Source.class)

Message queue에서 받아서 다시 넣는 애들은
- @EnableBinding(Processor.class)

받기만하는애들은
- @EnableBinding(Sink.class)

그래서 어떤 메서드가 실제로 큐를 받느냐 할때
@Input(Processor.INPUT) 이런식으로 명시해야줘야 한다.

https://www.msaschool.io/operation/implementation/implementation-three/


```java
    @StreamEmitter
    @Output(Source.OUTPUT)
    public Flux<MessageResponse> getMessagesStream() {
        return webClient.get()
                        .uri(GitterUriBuilder.from(gitterProperties.getStream())
                                             .build()
                                             .toUri())
                        .retrieve()
                        .bodyToFlux(MessageResponse.class)
                        .retryBackoff(Long.MAX_VALUE, Duration.ofMillis(500));
    }
```

application.yml에 spring.cloud.stream.bindings.output.destination 으로 지정해주면 된다. (https://docs.spring.io/spring-cloud-stream/docs/Elmhurst.SR1/reference/htmlsingle/)
- 위 코드는 Source.OUTPUT이라는 메시지 queue로 내보내는 것이다.


# 클라우드 환경에서의 리액티브 프로그래밍

AWS 람다 :이벤트에 대한 응답으로 코드를 실행하고, 자동으로 컴퓨팅 자원을 관리
- 작고, 독립적이며, 확장 가능한 서비스 개발 가능


## 스프링 cloud data flow

기능적 비즈니스 로직 개발과 개발된 컴포넌트 사이 실제 연계 및 통합을 분리한다.

데이터 소스(DB, 메시지 큐, 파일) 의 데이터 변환을 위한 다양한 내장 프로세서랑, 결과 저장 방법을 나타내는 sink를 지원하기 위해 다양한 기본 커넥터를 제공한다.

spring cloud data flow는 스트림 프로세싱이라는 개념을 사용한다. 

### spring cloud function으로 잘게 쪼개진 어플리케이션

메시지를 받았을 때 수신 메시지 유효성 검사 같은건 우리의 커스텀 로직이 들어간다.  이런데는 spring cloud stream application 사용하자.

문제점
1. 설정파일
2. 모든 의존성 포함된 jar 파일 (uber-jar)
3. app 배포 (클라우드 스트림이 실행되는 컨테이너에 어떻게 올리지?)

그래서 spring cloud function에는 AWS 람다, Azure 펑션 등에 사용할 수 있는 함수 배포용 어댑터가 존재한다.
`java.utils.function.Function`
`java.utils.function.Supplier`
`java.utils.function.Consume`
과 같은 자바 클래스 중 하나 정의하면 올릴 수 있다. 심지어 스프링 부트로 제작해도 된다.

```java
@Bean
public Funciton<Flux<Payment>, Flux<Payment>> validate(){ return flux.just()}
```
이런거 올릴 수 있다.

또한, spring 설정 파일에 문자열로 함수를 선언할 수도 있다.
그래서 이를테면 현재 실행 url의 정보가 application.yaml에 들어있어야 한다면
```java
spring.cloud.function:
    compile:
        payments:
            type: supplier/function/consumer 중 택 1 
            lambda: ()->Flux.just(new URL(...))
```
이런식으로 application.yml 에 넣어도 된다. 스프링 IoC 컨테이너에 "payments" 라는 함수로 등장한다.

함수가 동적으로 변경될 수 있다. 
 
spring-cloud-function-compiler 모듈이 이런 application.yml 파일 다 컴파일 한다. 심지어는 실시간으로 함수를 배포할 수 있는 endpoint도 제공한다.


### spring cloud function deployer

그래 그러면 순수함수들은 올릴 수 있는데, 만약 스프링 프레임워크의 일부 기능이 필요하다 또는 스프링 데이터 또는 웹 의존성이 있는 기능이 필요하다.

이 경우 thin-jar이라고, 어플리케이션이 직접 엑세스하는 의존성만 포함된 날씬한 jar이 있다.

Spring cloud function deployer는 Spring Deployer 어플리케이션으로 각각의 jar파일을 실행시킬 수 있는데, 완벽히 격리된 환경에서만 실행하도록 해준다.

매우 가벼운 함수들의 집합으로 Faas (서비스로서의 함수)를 구축할 수 있다.

그럼 spring cloud data flow (메시지 큐에서 받는) 와 spring cloud function (FaaS처럼 함수각각이 특정 엔드포인트에 떠있는) 이 어떻게 결합할까?

## spring cloud 

spring cloud data flow 에서 spring cloud function의 기능을 사용하게 하는 `spring cloud starter stream app function`
순수 jar파일을 사용하고, 해당 jar파일도 쉽게 배포할 수 있다. 

```java
public class PaymentValidator implements Function<Payment,Payment> {
    public Payment apply(Payment payment){...}
}
```
이렇게 함수정의하고, jar로 만들어 어디 페이지에 업로드한다음에,
```java
SendPaymentEndpoint=Endpoint: http --path-pattern=/payment --port=8080 |
Validator: function --class-name=com.example.PaymentValidator --location=https://github.com/.../payments-validation.jar?raw=true
```
이런식으로 하면, 우리의 `Spring Cloud Function Bridge` 에 쉽게 연결 할 수 있다.

### spring cloud data flow # Router Sink
근데 이런 순수함수 내에서 redirect는 어떻게할까? validate 해서 아니면 실패로 이동시켜야할텐데.

`| router --expression="payload.isValid() ? 'Accepted' : 'Rejected'"`
또는, 메시지 큐 이름을 직접 지정해 메시지를 보낼 수 있다.
```java
Accepted=Accepted: rabbit --queues=Accepted
```
validator에서 Accepted가 나왔으면 Accepted queue에 메시지를 넣는 방식으로 진행

### 데이터는 어떻게 DB에 넣을까? MongoDB sink

sink는 데이터를 넣어주는 역할을 일컫는다. (data inputter)
수신 메시지를 mongoDB로 쉽게 저장할 수 있게 한다. 



# 리액티브 메시지 전달을 위한 낮은 지연 시간의 Rsocket

이렇게 하면 메시지 전달에 지연시간때문에 오래 걸릴 수도 있다.

서비스 사이에 지속적이고 직접적인 통신 연결이 빠를 수 있다. 웹소켓은 ReactorNettyWebSocketClient도 이용할 수 있어 좋다.

다만, 서비스 사이의 강한 결합이나 웹소켓의 사용은 리액티브 시스템 요구 사항에 적합하지 않다. 프로토콜이 배압제어를 지원하지 않기 때문.


## Rsocket vs 리액터 -네티
리액터 네티의 문제점은 배압지원이 한 프로그램 내부에서만 동작한다는 것. 

컴포넌트와 네트워크까지 다 배압지원이 가능해야 한다.
리액터 네티를 사용하면 

빠른 프로듀서, 느린 컨슈머가 있다고 할때, 느린 컨슈머쪽 소켓 버퍼에 패킷이 쌓이다가 유실되어버린다. 

정말 배압지원이 된다면, 컨슈머 소켓 버퍼에 일정개수까지만 쌓이도록 요청을 해서 이런일이 발생하지 않아야 한다.

그냥 TCP의 네트워크 flow control 때문에 배압이 컨트롤 된다.

Rsocket의 강력한 기능 중 하나는 동일한 서버와 클라이언트 사이 여러 스트림에 대해 동일한 소켓 커넥션을 재사용한다.

한번 커넥션을 맺고나면 클라이언트 서버 구분이 사라지고, 같은 창구로 전송하고 수신할 수 있다. 

## 자바에서 RScoket의 사용

리액터3를 기반으로 구현됐다. Rsocket-Java.

## grpc 말고 왜 Rsocket쓰냐?

GRPC
protocol buffer 를 써서 처리. 
- 버전 변경 장점
- 직렬화로 매우 작아진 메시지. 등( 서로 format이 뭔지 알고있어서 format 정보 복원은 상대측에 받아서. )
- 비동기식

but
- 배압제어는 HTTP/2 흐름 제어
  - 슬라이딩 윈도우 크기에 의존 (바이트 단위)
- GRPC는 RPC 프레임워크 , RSocket은 프로토콜
  - GRPC 형태로 어플리케이션을 제작해야 함 .

Rsocket-RPC를 사용하자 (protobuf 기반)


