# 6장 웹플럭스 - 비동기 논블로킹 통신

# 리액티브 기반 서버 기술의 핵심: WebFlux
원래 스프링 프레임워크 web application은 자바 EE의 서블릿 API와 통합하기로 결정을 했었다. 그래서 spring web mvc는 서블릿 API와 강하게 결합되어 있다.

## 흐름
MVC: 요청 -> javax.servlet.Servlet 메서드로 들어옴, request 객체와 response 객체 생성
webflux: `ServerWebExchange` 메서드로 들어와 Request(Flux<DataBuffer>)와 response(Publisher<DataBuffer> 을 write하는 함수를 가진다. Mono<void>로 완료를 알린다) 생성
특이한점: response가 Mono<void>를 내보내기 때문에, 이걸 구독했을때만 수신 서버에 write가 시작된다는 것.

MVC: 요청 -> ServletAPI -> filterChain -> dispatcher handler -> RequestMappingHandler -> 적합한 @Controller 어노테이션 객체 - RequestMappingHandlerAdapter
webFlux: 요청 -> HttpHandler(`ServerWebExchange` 인스턴스로 request, response 변환) -> filterChain -> dispatcher handler -> RequestMappingHandler -> 적합한 @Controller 어노테이션 객체 - RequestMappingHandlerAdapter
dispatcher handler에서는 어떤 순서로 controller bean을 찾아야하는지 RequestMappingHandler를 찾는다.
이후, 어떤 @Controller 객체를 사용하는지 RequestMappingHandlerAdapter를 활용하고, 실제 응답을 만든다.

WebFlux에서는 routing을 하나의 모듈에서 모두 처리할 수 있다.


```java
	@Bean
	public RouterFunction<ServerResponse> routes(OrderHandler orderHandler) {
		return
			nest(path("/orders"),
				nest(accept(APPLICATION_JSON),
					route(GET("/{id}"), orderHandler::get)
					.andRoute(method(HttpMethod.GET), orderHandler::list)
				)
				.andNest(contentType(APPLICATION_JSON),
					route(POST("/"), orderHandler::create)
				)
				.andNest((serverRequest) -> serverRequest.cookies()
				                                         .containsKey("Redirect-Traffic"),
					route(all(), serverRedirectHandler)
				)
			);
	}
```

endpoint가 두개있다.
- /orders/
- /orders/id

이는 RouterFunction이라는 라우팅하는 방법을 기술하는 클래스와 , RequestPredicates 라는 어떤 입력을 받을지 정의하는 클래스를 사용한다.

함수형 프로그래밍방식으로 핸들러 선언을 하고, 모든 경로 매핑을 한군데에서 명시적으로 관리한다.


```java
    public Mono<ServerResponse> create(ServerRequest request) {
        return request
            .bodyToMono(Order.class)
            .flatMap(orderRepository::save)
            .flatMap(o ->
                ServerResponse.created(URI.create("/orders/" + o.getId()))
                              .build()
            );
    }
```
위에서는 이 메서드만 가져다 사용하면 된다. 응답을 내가 직접 만들어낼 수 도 있다.
이런 새로운 함수형 웹 프레임워크는 전체 스프링 인프라를 시작하지 않고도 웹 응용프로그램을 간단히 만들 수 있는 방법을 제공한다 (node처럼 간단한 서버 제작방법을 제공한다)


## WebClient : 논블로킹 지원 클라이언트

RestTemplate 대체하는 WebClient - 
```java
WebClient.create("http://localhost/api")
        .get()
        .uri("users/{id}",userId)
        .retrieve()
        .bodyToMono(User.class)
        .map(...)
        .subscribe()
```
retrieve()하면 session이 담겨져오는데 `WebClient.ResponseSpec` 이 반환된다.
- status
- header
- body
에 대해서 처리를 해주어야 한다.
 ```java
 Mono<ResponseEntity<Person>> entityMono = client.get()
     .uri("/persons/1")
     .accept(MediaType.APPLICATION_JSON)
     .retrieve()
     .toEntity(Person.class);
 
Or if interested only in the body:

 Mono<Person> entityMono = client.get()
     .uri("/persons/1")
     .accept(MediaType.APPLICATION_JSON)
     .retrieve()
     .bodyToMono(Person.class);
 
By default, 4xx and 5xx responses result in a WebClientResponseException. To customize error handling, use onStatus handlers.
```

```java
<T> reactor.core.publisher.Mono<T> bodyToMono(Class<T> elementClass) Decode the body to the given target type.
```

bodyToMono는 mono를 반환하니 처리하는 함수를 지정하면 된다.
subscribe()가 불려야지만 커넥션이 생긴다.

반대로 WebClient로 Post 요청을 한다면 .body(Flux<>) 혹은 .body(Mono<>) 가 가능하다. exchange는
```java
exchange() 메소드는 retrieve() 메소드보다 더 많은 컨트롤을 제공합니다.
retrieve()와 동일한 역할을 하면서 ClientRespone 객체의 접근을 가능하게 해 response 처리를 커스터마이징하기 보다 용이합니다.

    Mono<Person> result = client.get()
            .uri("/persons/{id}", id).accept(MediaType.APPLICATION_JSON)
            .exchange()
            .flatMap(response -> response.bodyToMono(Person.class));
        https://dreamchaser3.tistory.com/11
```
retrieve()는 4xx 5xx response는 예외를 던지지만 exchange는 그렇지 않다. 직접 확인해야한다.
DefaultWebClient는 reactor-netty HttpClient로 적용되어 있는데, 
jettyClientHttpConnector 사용하려면 WebClient Builder사용해서 바꿀 수 있다. 


## 리액티브 웹소켓 API

기존에 사용되던 방식 - websocket에도 webflux가 도입됨.
웹소켓 연결을 하기 위해서 WebSocketHandler를 제공함 - WebSocketSession을 받아서 조작가능한 handle 메서드를 사용함.

session은 메시지 body 있고, session에 요청을 보낸 ip 정보도 존재한다.

WebSocketHandlerAdapter 빈을 제공하면 이 adapter에 존재하는 HandlerMapping을 이용해 WebsocketHandler의 Handle 메서드를 호출한다. 


클라이언트에서는 `WebSocketClient#execute` 메서드를 제공하는데, url, header, handler등을 인자로 받는다. 

## 웹플럭스 웹소켓과 스프링 웹소켓

서블릿 기반 웹소켓
- I/O가 블로킹
- 한번에 하나의 메시지만 처리하는 handler
- sendMessage가 동기식 메시지
- GETMAPPING, POSTMAPPING 등 어노테이션 사용가능했음.

스프링 웹플럭스 + 웹소켓 
- 완전한 논블로킹 쓰기 읽기.
- 어노테이션 기반 핸들링 불가 


## 웹소켓 경량화를 위한 reactive SSE
HTML5는 SSE로 서버가 이벤트를 푸시하는 연결만들 수 있다.

Flux<ServerSentEvent<?>> 를 반환받게 하면, 아니면 아래코드처럼 하면 webflux framework가 스트림에서 각 원소가 갈때마다 SSE로 래핑해준다.  
```java
@GetMapping(produces = "text/event-stream")
public Flux<StockItem> streamStocks(){
    
}
```

SSE의 특징은, 
- @RestController, @XXXMapping으로 설정이 가능하다는 점.
- 일반적인 rest 컨트롤러처럼 메시지 컨버터 설정을 제공한다 (SSE 내보낼때 message handle하는 방법을 따로 안써도 된다.)
- 바이너리 인코딩은 지원 x UTF-8만 지원
- HTTP 프로토콜의 추상화라서 일반적인 REST Controller와 동일한 선언적/기능적 엔드포인트 구성과 메시지 변환 지원
웹소켓의 특징은
- 세션을 직접 고쳐서 메시지를 변환하게 하는 등 추가적인 설정이 필요하다
- 메시지 크기가 작고, 트래픽이 적어서 대기 시간이 짧을 때 유용하다.



## 리액티브 템플릿 엔진

UI 중에서는 webflux 모듈을 활용한 뷰 렌더링 기술이 이식 안된 곳들이 많다. 뷰 렌더링 기술 자체는 이전처럼 Mono<String>
을 반환해 비동기적으로 뷰 이름을 리턴시켜줄 수 있다. 근데 프리마커 같은데에서는 리액티브 렌더링이나 논블로킹 렌더링 지원 x


타임리프는 view이름을 String으로 반환해서 리액티브 스트림이 model에 들어있는 형태가 가능하다.
(model에는 `ReactiveDataDriverContextVariable` 라는 데이터 타입으로 들어가게 되고, publisher, flux, mono, observable 등 리액티브 타입을 받는다)

템플릿에서는 자연스럽게 지원한다 (기존과 사용방법은 동일, 다만 렌더링 엔진이 list의 마지막 요소가 나오기를 기다리지 않고 클라이언트에 데이터 렌더링 시작)

## 리액티브 웹 보안

기존엔 ThreadLocal을 사용해서 security Context가 전달되었다. 이제는 reactive stream의 context를 사용해야 한다.
```java
ReactiveSecurityContextHolder.getContext()
        .getContext()
        .map(Mono<SecurityContext> 를 사용하는 함수)
```

내부적으로 getContext()는 

```java
return Mono.subscriberContext()
        .filter(c -> c.hasKey(SECURITY_CONTEXT_KEY))
        .flatMap(c -> c.<Mono<SecurityContext>>get(SECURITY_CONTEXT_KEY))
```
즉, Context에서 SECURITY KEY , value 로 들어있는 Mono<SecurityContext>를 반환시킨다.  
주의할점은 block()를 부르면 subscriberContext가 사라진다. 왜냐하면 context는 Reactor operator chain 바깥에서는 scope를 벗어나기 때문이다.
https://github.com/reactor/reactor-core/issues/1667

`ReactorContextWebFilter`를 사용하면 보다 context 설정과 엑세스가 쉽다. 
이 filter안에서는 subscriberContext로 securityContext를 제공한다. 이 securityContext는 ServerSecurityContextRepository에서 얻어온다.

ServerSecurityContextRepository이게 바로, 아래에 등장하는 ReactiveSecurityContextHolder를 initialize하는데에 쓰인다. 즉 context가 세팅된다. 
```java
ReactiveSecurityContextHolder.getContext()
        .getContext()
        .map(Mono<SecurityContext> 를 사용하는 함수)
```

repository는 `Mono<Void> save(ServerWebExchange exchange, SecurityContext context)` , load가 존재한다.

## 리액티브 방식으로 스프링 시큐리티 사용하기

```java
    @Bean
    public SecurityWebFilterChain securityFilterChainConfigurer(ServerHttpSecurity httpSecurity) {
        return httpSecurity

            .authorizeExchange()
                .anyExchange().permitAll()
            .and()

            .httpBasic()
            .and()

            .formLogin()
            .and()

            .build();
    }

```
이런식으로 webFilterChain을 구성할 수 있다. .and()로 구분이 되어있다.

MapReactiveUserDetailsService는 USER랑 PW를 설정하는 등을 하는데, 스프링 시큐리티에 로그인할 수 있고 없는 유저같은걸 세팅할 수 있다.
spring security라는 것과 연관된 빈으로 보임. 
스프링 시큐리티도 배워야할 듯.

## Observable과의 호환성

## 웹플럭스 vs 웹 MVC

webFlux 왜 써야 하나?

### 1. little의 법칙 (little's law)
지정한 대기시간 만족하려면 동시에 처리해야 하는 요청수가 얼만지 알 수 있는 법칙

요청 쌓이는 수 = 사용자수 * 응답 평균 대기 시간

근데 이건 cpu나 메모리 같은 공유 리소스때문에 느려지는걸 고려하지 않았다.

그래서 암달의 법칙과 보편적 확장성의 법칙이 적용된다. 

암달의 법칙은 직렬화되는 부분 (병렬화 x) 이 계산에 포함되어있다. 

USL은 Universal Scalability Law. 이건 쓰레드 사이의 공유 메모리 접근까지 계산에 들어가있다. 
프로세스보다 많은 쓰레드의 수가 계산에 고려되었다.


MVC의 경우 블로킹 I/O가 기반이 된다. 요청당 스레드가 생겨서 I/O가 블로킹 된 동안 해당 스레드는 아무일도 하지 않는다.
또한 요청당 스레드 생기면 1스레드당 1mb인데, 메모리 OOM되기 쉽다. (stack size와 연관)
WebFlux의 경우 이벤트는 계속 들어오고 워커 스레드가 큐에 쌓인 각 이벤트를 처리하게 된다. 

문제는 CPU intensive work가 많은 경우 = web mvc가 더 적절하다. 아니면 별도의 프로세서 풀로 위임을 하게 해야 한다.

또한 webflux의 경우 안에서 사용하는 함수들이 동기적인 지 아닌지 잘 판단해야 한다. 대다수의 라이브러리는 동기적으로 만들어졌다 *(JDK 자체가)

# 요청 처리 모델과 사용성 사이의 관계

- 학습 시간이 오래걸린다 
- webflux는 많은 버그와 취약점이 존재한다.
- non blocking code를 debug하는게 어렵다

- 마이크로서비스는 I/O 통신이 많고 비동기 시스템이 적합하다.
- 모바일 시스템은 클라이언트가 느리기 때문에 서버당 스레드를 사용하면 너무 많은 스레드가 만들어져있을 수 있다 (접속자가 많은 경우 )

