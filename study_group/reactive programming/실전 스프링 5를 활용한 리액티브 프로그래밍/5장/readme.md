# 5장, 스프링부트 2와 함께하는 리액티브

# 스프링 부트의 특징

스프링 프레임워크의 장점
- IoC 
  - 모든 객체를 new로 만드는게 아니라, application context 라는 저장소에 처음 부팅할때 만들어 넣어놓고 가져와서 사용한다. 코드가 덜복잡하다.

다만 이 방식을 사용할 때, 빈을 등록하기 위한 세가지 이상의 방법이 존재
- XML : 디버깅 어려움
- Groovy
- Properties

하지만 이런 설정들을 셋업하는데 매번 같은 코드가 반복되었음.

Spring ROO는 프로그램이 복잡해지면 사용 못함.

Spring boot의 특징
- 2013년, 사용자가 추가적인 인프라 설정 없이 새 프로젝트 시작할 수 있게 했다.
- IoC 컨테이너 실행 가능한 @SpringBootApplication 어노테이션 사용
  - spring-boot 모듈 (IoC 컨테이너관련 모든 기본 구성)
  - spring-boot-autoconfigure (스프링 데이터, 스프링 mvc 등 모든 설정 제공)이 모든 "starter" 모듈의 설정을 가지고 있다.
- gradle이나 maven과 같은 빌드 툴과 모듈들의 묶음이다

# 스프링 부트 2.0에서 리액티브

Spring Core 는 스프링 생태계 핵심 모듈로, 스프링 프레임워크 5.x에서 리액터 프로젝트 3과 같은 리액티브 스트림 및 리액티브 라이브러리 지원이 나옴

## 리액티브 타입으로 형 변환을 지원 
- ReactiveAdapter
  - 임의의 타입을 Publisher로, 임의의 Publisher를 Object로 변환하는 클래스. 이걸 extend해서 어떻게 publisher로 만들수있는지 제공한다.
- ReactiveAdapterRegistry
  - 모든 ReactiveAdapter 클래스를 여기에 등록해놓고, 특정 클래스에 대한 변환 어댑터를 얻어올 수 있다.

## Reactive I/O

### DataBuffer 클래스
네트워크로 통신할때 반드시 필요한 byte 인스턴스의 버퍼. 스프링 코어 모듈은 DataBuffer 클래스를 가지고 있다.
java.nio.ByteBuffer따위를 사용하면 io.netty.buffer.ByteBuf를 사용할 때에 여기의 힙 메모리를 복사하는 과정을 거쳐야 하지만,
DataBuffer 클래스는 추상화를 잘해서, io.netty.buffer.ByteBuf 에 이미 구현된 내부함수를 사용하도록 되어 있다.

DataBufferUtils 클래스에서 Flux로 읽을 수 있게 함수를 제공한다.

`리액티브 코덱`을 이용하면 논 블로킹 방식으로 직렬화된 데이터를 자바 객체로, 또는 vice versa.
DataBuffer 인스턴스의 스트림을 객체의 스트림으로 변환해 돌려주는 작업을 간편하게 할 수 있다. 
Encoder, Decoder 인터페이스가 있어서 어떻게 encode나 decode하면 되는지 정의해주면 된다.
모든 데이터가 decode되기를 기다리지 않아도 되어 전체 기다리는 시간을 줄인다.


### Reactive Web

Spring webflux 라는 새로운 웹 스타터 그룹. 리액터 3를 일급객체로 광범위하게 사용 (flux , mono를 리턴하고 인자로 받고)
클라이언트로 사용될 때에도 논 블로킹 통신할 수 있게 `WebClient` 클래스 제공
https://thalals.tistory.com/379 RestTemplate의 대체라고 보면 된다.

네티같은게 아니라, servlet 3.1 api를 활용한 경우 webclient로 비동기 요청을 보내더라도 webclient에서 하나의 응답씩 읽어와야 하기 때문에 (서블릿 api는 읽기 쓰기가 블로킹 방식으로 처리됨) 
request(1) 같은 pull model이 되어버리지만, netty를 사용하면 비동기로 몇개씩의 요청을 보내도 몇개의 요청을 동시에 처리할 수 있다.

# 스프링 데이터에서의 리액티브
# 스프링 세션에서의 리액티브
# 스프링 시큐리티에서의 리액티브
ThreadLocal를 사용해서 SecurityContext 인스턴스를 저장해두었다. 하나의 스레드가 하나의 요청을 처리할 때에는 이상이 없었기 때문.
이제 flux나 mono에서 전달하기 위해서는 reactor의 Context에 정보를 담아야 한다

# 스프링 클라우드에서의 네이티브

스프링 클라우드 넷플릭스 Zuul
```yaml
zuul:
  host: 
    connect-timeout-millis: 3000
    socket-timeout-millis: 3000
  routes: 
    order: 
      path: /order/** 
      url: http://order:9001  
    address: 
      path: /address/**
      service-id: address
  retryable: true 
```

이런식으로 설정해놓으면 특정경로로 포워딩해주는 일종의 게이트웨이. 하지만 블로킹 방식으로 라우팅하는 서블릿 API 기반.
Spring Webflux 이용한 스프링 클라우드 게이트웨이 등장. (비동기 논블로킹 라우팅 제공)

# 스프링 테스트에서의 리액티브
spring test는 웹 플럭스 기반 웹 앱 테스트를 위한 `WebTestClient`를 제공한다. 
reactor는 Publisher를 테스트하기 위해 리액터 테스트 모듈을 제공한다. 
# 리액티브 모니터링하기
Flux#metrics() 를 사용해서 특정 endpoint를 노출해 모니터링을 할 수 있게 하지만, 충분치 않다. spring cloud sleuth 모듈이 있다.
모든 리액티브 워크플로를 추적가능하다


