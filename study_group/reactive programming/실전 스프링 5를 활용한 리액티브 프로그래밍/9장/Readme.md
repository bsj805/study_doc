# 9장 리액티브 어플리케이션 테스트하기

# 리액티브 스트림 테스트하기 어려운 이유

리액티브 스트림 장점
- 비동기 통신 활성화 -> 리소스 사용 최적화
  - 논블로킹 I/O 통신 구축에 적합
- 비동기 구현을 깔끔한 코드로 가능하다.

다만, 테스트가 문제이다.

# StepVerifier를 통해 리액티브 스트림 테스트

리액터는 StepVerifier 포함된 reactor-test 모듈 제공한다. 
StepVerifier가 제공하는 연쇄형 API를 이용하면 스트림 검증이 가능함.

## StepVerifier의 핵심 요소

### Publisher 검증 핵심 메서드 1. `StepVerifier <T> create(Publisher<T> src)`
publisher를 받아서 StepVerifier를 만드는 것처럼 보이지 않는가? 맞다.
 
```java
StepVerifier
        .create(Flux.just("foo", "bar"))
        .expectSubscription() // subscription 신호가 왔는지 검증
        .expectNext("foo") // "foo" 이벤트가 발생해야 한다.
        .expectNext("bar")  // 그다음으로 "bar" 이벤트가 발생
        .expectComplete() // publisher가 끝나야 하며
        .verify() // 위 플로우를 구독해야 한다. verify는 blocking 호출이라서 실행을 차단시킨다.
```

몇개의 이벤트가 나오는지가 더 중요하면 .expectNextCount() 메서드.

```java
StepVerifier
        .create(Flux.range(0,100))
        .expectSubscription()
        .expectNext(0) // 0이 나오고
        .expectNextCount(98) // 98개의 이벤트가 있은 뒤,
        .expectNext(99) 
        .expectComplete()
        .verify();
```

Flux.range(0,100) 은 0부터 99까지의 원소를 만들어낸다.

다만, 매 이벤트마다 조건에 맞는지도 봤으면 좋겠다면 Hamcrest 조건사용하자. 


`.recordWith(ArrayList::new)` 를 expectSubscription() 뒤에 붙이면, 모든 이벤트가 저 arrayList에 저장된다.

다만, 멀티 스레드 퍼블리셔라면 기록이 저장될 때 ConcurrentLinkedQueue를 사용해 스레드 세이프한 자료구조를 사용해야 할 것.

`expectNextMatches(e->e.startsWith("some-prefix"))` 이런식으로 mather를 직접 정의해도 된다.  (`expectNext(0)` 이렇게 말고)

.assertNext() 및 .consumeNextWith() 을 사용하면 assertion을 직접 작성할 수 있다.

```java
.assertNext( event -> assertEqual(event, "hello_world"))
```
이런식으로 assertion을 일으키는 람다식을 넣어라.


## StepVerifier를 이용한 고급 테스트

Publisher 스트림이 무한한 경우에는 어떡할까? .verify()가 무한히 기다릴텐데.
그래서 일정 기대값 이후에 구독취소하는 `.thenCancel()` 을 제공한다.

배압확인도 .thenRequest()를 사용하면 가능하다. 

이런 `then`문을 사용하면 이벤트가 한번만 사용되지 않고 한번더 쓸 수 있다. `.expectNext(0).then(System.out::println)` 이렇게.

TestPublisher는 Publisher의 구현체인데, 테스트용으로 onNext(), onComplete(), onError() 이벤트를 public으로 노출시켜서 우리가 직접 작동시킬 수 있게 해놨다.

```java
TestPublisher<String> idsPublisher = TestPublisher.create();

StepVerifier
        .create(walletsRepository.findAllById(idsPublisher)) //testPublisher flux를 받는 findAllById함수
        .expectSubscription()
        .then( () -> idsPublisher.next("1") ) //subscription 신호가 온 다음, testPublisher flux가 onNext로 1 이라는 이벤트를 만들게 한다. 
        .assertNext(w -> assertThat(w, hasProperty("id", equalTo("1"))))  // 1이란 신호를 받아서 findAllById(1)을 했기 때문에 wallet클래스가 생겼다. 
        .then( () -> idsPublisher.next("2") )
        .assertNext(w -> assertThat(w, hasProperty("id", equalTo("2"))))  // 2이란 신호를 받아서 findAllById(2)을 했기 때문에 wallet클래스가 생겼다.
        .then(idsPublisher::complete)  // flux가 끝난 상황을 가정한다
        .expectComplete(); // 그럼 walletsRepository에서 나오는 stream도 끝나기를 기대한다.
        .verify();
        

```

## 가상 시간 다루기

```java
public Flux<String> sendWithInterval() {
    return Flux.interval(Duration.ofMinutes(1))
        .zipWith(Flux.just("a", "b", "c"))
        .map(Tuple2::getT2);
}
```

이걸 검증하고 싶어서

```java
StepVerifier
        .create(sendWithInterval())
        .expectSubscription()
        .expectNext("a", "b", "c")
        .expectComplete()
        .verify();
```
를 두면, "c"는 3분뒤에나 onNext()되니까 이 테스트가 3분이 걸린다는 것이다.

그래서 가상 시간으로 바꿀 수있는 기능이 있다.

`StepVerifier.withVirtualTime(() -> sendWithInterval())`

이 경우 리액터의 모든 스케줄러를 명시적으로 대체한다. 즉, FLux.interval은 우리의 가상 시간 스케줄러에서의 interval을 의미하고, 
우리 마음대로 시간을 조정할 수 있다.

https://projectreactor.io/docs/core/release/reference/

그런데 시간을 마음대로 조정하는 만큼, flux의 원소가 나오기 전의 시간으로 가게 되면, 시간이 흐르는게 아니기 때문에 거기서 영원히 wait한다. 
그래서 검증에 소요되는 시간을 제한할 수 있다. `.verify(Duration t)`


## 리액티브 컨텍스트 검증
컨텍스트에도 엑세스 할 수 있다. .expectAccessibleContext()를 사용하면된다. 
하지만 이 메서드 호출을 통해 컨텍스트 객체를 받으면 event랑 달리 일회성으로 사용하는 경우가 흔치 않다.
그래서 .then()이 나타날때까지는 계속 context 객체 하나에 대한 assertion인줄 안다.

```java
        .expectSubscription()
        .expectAccessibleContext()
        .hasKey("security") //then 나오기 전까지는 어떤 verification이던 context 객체와 연관됨.
        .then() // 
        .expectComplete()
        .verify()
```


# 웹플럭스 테스트 

## WebTestClient 로 컨트롤러 테스트

- WebTestClient는 servlet.MockMvc 와 유사한데, webflux endpoint  테스트하기 위함. 
- 특정 controller에 binding해서, webClient마냥 `.get().uri("/payments/").exchange()` 를 호출하면 header, status, body 등을 확인 가능하다.
- WebTestClient는 직접 메서드에 접근해서 HTTP 서버를 띄우지 않아도 되는 장점이 존재한다.

만약 외부 API를 호출해야 한다면, 모킹이 필요한데, 아예 발신하는 HTTP client 메서드 요청을 모킹하거나, WireMock같은 라이브러리를 사용해야 한다. 

이 경우 HTTP client 종속적인 테스트가 제작된 것이라서, HTTP client library 바꿀떄 바뀌어야 한다는 단점이 존재한다. 