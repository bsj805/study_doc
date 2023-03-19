# 리액터 프로젝트 
 
- 리액터 패턴
  - 모든 이벤트는 큐에 추가 되고, 이벤트는 별도의 스레드에 의해 처리됨. 
- 함수형 프로그래밍 
- 리액티브 프로그래밍

 reactor 1.x 버전에서는 , 직접 dispatcher를 지정해서 `reactor` 인스턴스를 생성한다.
 내부적으로 이벤트가 생성될때, 세팅한 디스패처에 의해서 처리가 된 후 목적지로 보내진다. 
 Dispatcher의 선택에 따라 동기 또는 비동기 처리가 된다.
 
리액터 1.x로도 네티와 결합해서 비동기 및 논블로킹 메시지 처리가 가능했다.
다만 `subscription. request` 등을 통한 배압 조절 기능이 없었다. 
아예 producer 스레드 차단 or 이벤트 받아서 생략 외에는 배압 제어 기능 x 
오류 처리 복잡


# 리액터 프로젝트 2.x

```java
stream
        .retry()
        .onOverflowBuffer()
        .onOverflowDrop()
        .dispatchOn(new RingBufferDispatcher("test")) 
```

1. 오류 발생시 retry() == 지금까지 위에있던 작업들 다시 실행하도록 한다.
2. onOverflowBuffer(), onOverflowDrop() 로 배압 관리 가능하다
3. dispatchOn 연산자로 새로운 Dispatcher를 이용해 해당 리액티브 스트림에서 작업할 수 있다 -> 메시지를 비동기적으로 처리할 수 있다.

`reactive-stream-commons` 라이브러리가 생겼다. 
RxJava 2.0과 reactor 3.x 버전이 비슷하다.

# 리액터 프로젝트 필수 요소

1. 콜백 지옥과 깊게 중첩된 코드를 생략하자
2. 가독성을 높이고, 리액터 라이브러리에 의해 정의된 워크플로우에 조합성을 추가하자
   - 연산자를 연결해서 사용하는 것을 권장한다.
   - 실제 구독이 일어날때만 데이터 플로가 기동된다.
3. 내부데이터, 외부 데이터와 관계없이 오류가 발생할 가능성이 있는 비동기 요청의 결과를 효율적으로 처리. (복원력 있는 코드 작성)
4. 배압 지원
   - 푸시 전용 (subscription.request(Long.MAX_VALUE))
   - 풀 전용 (subscription.request(1))
   - 풀-푸시(혼합형): 구독자가 수요를 실시간 제어할 수 있고, 게시자가 데이터 소비 속도에 적응할 수 있는 경우

 리액터 프로젝트는 실행 스레드를 다양하게 관리할 수 있는 스케줄러 세트를 제공하고, 개발자가 로우 레벨 제어 기능을 갖춘 자체 스케줄러도 만들 수 있다

# 리액티브 타입 - Flux와 Mono 

리액티브 스트림 스펙에는 네가지가 정의되어 있다. 
- Publisher
- Subscriber
- Subscription
- Processor

리액터 프로젝트는 Publisher<T> 의 구현체로 Flux<T> Mono<T> 가 존재한다.

Flux는 아래와 같이 끝 신호, 0,1 또는 여러 요소 생성가능하고 무한한 요소도 만들 수 있다. 
```java
onNext x 0..N [onError | onComplete]
```
```java
Flux.range(1,5).repeat()
```
이러면 12345 가 무한으로. 
전체 스트림 생성을 완료하지 않고도 각 요소 변형, 소비할 수 있으니 OOM 안나는데, 무한인 flux를 `.collectList().block()` 하면 OOM 날 수도 있다.
block은 구독을 시작시키고, 최종 결과가 도착할때까지 실행중인 스레드를 차단하기 때문에, collectList()에서 값이 나올때까지 기다린다.


# Mono

```java
onNext x 0..1 [onError | onComplete]
```
끝, 0 또는 1 개의 원소를 반환하다. 

Mono<T>는 응용 프로그램 API가 최대 하나의 원소를 반환 . CompletableFuture처럼, Mono.get() 느낌으로 사용하게 된다. 다만 reactive stream형식으로 받을 수 있다.

또 Mono는 클라이언트에게 작업 완료 신호를 알리는데 사용할 수 있다. `Mono<Void> `를 하면, onComplete() 신호나 onError() 신호가
왔을 때, 이후 연산을 실행시킬 수 있다.

`Mono.from(Flux)` 로 간단히 상호 변환가능

# RxJava 2 의 리액티브 타입
RxJava2의 publisher는 형태가 다르다.
처음에는 Observable 하나만 존재했는데 2버전에 오면서 Single, Completable 타입이 추가되어서
- Obserbvable
  - 배압 지원 x, Publisher 인터페이스 구현x - `Flowable`로 변환해서 배압전략을 사용
- Flowable
  - Flux 타입과 동일. 리액티브 스트림의 `Publisher` 구현. Flux에서 publisher 유형의 인수 사용할 수 없으니 필요하면 Flowable을 사용해라.
- Single
  - 하나의 요소를 생성하는 스트림을 나타낸다.
  - Mono처럼 구독이 발생했을 때만 처리 시작
- Maybe (Maybe<T> == Mono<T>)
  - Mono타입과 동일한 의도를구현 but Publisher 인터페이스 구현 안해서 리액티브 스트림과 호환성 x
- Completable
  - RxJava 2.x엔 onNext 신호는 생성못하고 onError 또는 onComplete만 발생시키는 Completable.
  - Mono<Void> 와 같이 신호 제공용이다. 


# Flux와 Mono 시퀀스 만들기
Flux 및 Mono는 데이터를 기반으로 리액티브 스트림을 생성하는 많은 팩토리 메서드를 제공한다.
```java
        Flux<String> stream1 = Flux.just("Hello","world");
        Flux<Integer> stream2 = Flux.fromArray(new Integer[]{1,2,3});
        Flux<Integer> stream3 = Flux.fromIterable(Arrays.asList(9,8,7));

        stream1.subscribe(System.out::println);
        stream2.subscribe(System.out::println);
        stream3.subscribe(System.out::println);
```
ragne는 `Flux.range(2010,5);`

Mono는 주로 하나의 요소를 대상으로 한다. nullable이나 Optional 타입과 함께 사용한다.

Mono는 HTTP 요청이나 DB 쿼리와 같은 비동기 작업을 래핑하는데 매우 유용하다. 이를 위해 Mono는 
`fromCallable(Callable), fromRunnable(Runnable), fromSupplier(Supplier)`  등의 메서드를 제공한다.
오래 걸리는 HTTP요청을 다음과같이 작성한다.
```java
Mono<String> stream8 = Mono.fromCallabe(this::httpRequest);
```
일단 Mono자체는 바로 반환되기 때문에 비동기식으로 처리할 수 있다는점. onError 를 구현하면 전파되는 오류도 처리 가능.

```java
Flux.empty();
Flux.never();
Mono.error(new RuntimeException("Unknown id"));
```
이처럼, 
- 빈 인스턴스를 생성하거나
- 완료 메시지, 데이터, 오류에 대해서 신호를 안보내거나
- 항상 오류를 전파하는 시퀀스를 만들 수 있다.


`defer` 은 특이한 메서드인데, 구독하는 순간에 행동을 결정할 시퀀스를 만든다.

```java
Mono<User> requestUserData(string sessionId){
    return Mono.defer( () ->
        isValidSession(sessionId) ? Mono.fromCallable(() -> requestUser(sessionId))
        : Mono.error(new RuntimeException("Invalid user session")) );
        }
```
```java
Mono<User> requestUserData(string sessionId){
    return isValidSession(sessionId) ? Mono.fromCallable(() -> requestUser(sessionId))
        : Mono.error(new RuntimeException("Invalid user session"));
        }
```

위 아래는 Mono.defer()를 썼느냐 안썼느냐이다. 
위에는 .subscribe() 구독이 발생할 때까지 유효성 검사를 진행하지 않는데,
아래는 `requestUserData` 불리자마자 isValidSession, 인지 검사한다. 

"구독하는 시점" 에 따라 user의 validity가 변경될 수 있는 환경이라면, 위와 같이 defer을 해야한다. 

ex.) 로그인할때 Mono.defer() 로 userData를 받아올 수 있는 Mono를 받아놓는다. (클라이언트나 html 페이지에서?) 
추후, 유저가 `내 상품정보 조회` 버튼을 눌렀을때, 그 유저의 세션이 (로그인 정보가) 살아있는지 체크해서 정보를 제공해야 한다면 defer().

rxjavascript
```javascript
async componentDidMount() {
    this.setState({isLoading: true});

    const request = interval(1000).pipe( 
      startWith(0), 
      switchMap(() => 
        fetch('http://localhost:3000/profiles')
          .then((response) => response.json())
      ));

    request.subscribe((data: any) => { 
      this.setState({profiles: data, isLoading: false});
    })
  }
```
아래는 websocket
```javascript
class ProfileList extends Component<ProfileListProps, ProfileListState> {

  // constructor()

  async componentDidMount() {
    this.setState({isLoading: true});

    const response = await fetch('http://localhost:3000/profiles');
    const data = await response.json();
    this.setState({profiles: data, isLoading: false});

    const socket = new WebSocket('ws://localhost:3000/ws/profiles'); 
    socket.addEventListener('message', async (event: any) => { 
      const profile = JSON.parse(event.data);
      this.state.profiles.push(profile);
      this.setState({profiles: this.state.profiles}); 
    });
  }

  // render()
}

export default ProfileList;
```


# 리액티브 스트림 구독하기

Flux나 Mono는 구독 루틴을 훨씬 단순화하는 subscribe() 메서드를 람다 기반으로 재정의한다.

subscribe의 모든 메서드는 Disposable 인터페이스의 인스턴스를 반환하는데, 이 disposable 인스턴스는 스트림 취소가 가능하다

```java
Disposable disposable = Flux.interval(Duration.ofMillis(50))
        .subscribe(
                data -> log.info("onNext:{}", data )
        );
Thread.sleep(200);
disposable.dispose();
```
구독을 호출해서 disposable 인스턴스를 반환받고, dispose()로 구독을 취소한다. 

subscribe의 프로토타입은
```java
subscribe(Consumer<T>, Consumer<Throwable> , Runnable, Consumer<subscription>);
subscribe(Subscriber<T>);
```
즉, onNext, onError, onComplete, subscription 사용자. 이거나, 이들 모두를 가지는 Subscriber<T> 클래스를 넣는 방식이다.

근데 subscription을 직접 인자로 받아서 사용할떄
```java
Subscriber<String> subscriber = new Subscriber<String>(){
    
    volatile Subscription subscription;
    public void onSubscribe(Subscription s){
            subscription=s;
            subscription.request(1);    
            }
}
```
이런식으로 사용해야 하는데, 변수가 독특하다.
### volatile 
구독 및 데이터 처리가 다른 스레드에서 발생할 수 있으니 모든 스레드가 Subscription 인스턴스에 대한 올바른 참조를 가질 수 있도록 volatile을 사용한다.

volatile 키워드는 쓰레드들에 대한 변수의 변경의 가시성을 보장한다 고 한다.
멀티쓰레드 어플리케이션에서의 non-volatile 변수에 대한 작업은 성능상의 이유로 CPU 캐시를 이용한다. 
둘 이상의 CPU가 탑제된 컴퓨터에서 어플리케이션을 실행한다면, 각 쓰레드는 변수를 각 CPU의 캐시로 복사하여 읽어들인다.

volatile 키워드를 선언한다면 이 변수에 대한 쓰기 작업은 즉각 메인 메모리로 이루어질 것이고, 읽기 작업 또한 메인 메모리로부터 다이렉트로 이루어질 것이다.

물론 volatile이 만병통치약은 아니다.
다수의 쓰레드가 같은 counter 값을 증가시키는 상황이 바로 volatile 변수가 불완전해지는 상황이다

이를테면 두개의 쓰레드가 기존counter+1 을 volatile 변수에 저장하려는 상황. 에는 lock을 이용해야 하지, volatile로 해결불가능.



다시 본론으로 돌아와서,

subscription을 직접 사용하는건 1차원적 코드 흐름이 꺠지고, 오류 발생이 쉽다.
대신, BaseSubscriber를 상속하는게 낫다. 그러면 hookOnSubscribe 와 같이 특정 함수들에 대한 오버라이딩을 하면 된다.

# 연산자를 이용해 리액티브 시퀀스 변환

## Map 

index() 메서드나 timestamp() 메서드 같은건 map의 일종이다.

```java
Flux.range(2018,5)
        .timestamp()
        .index()
        .subscribe(e-> log.info("Index: {}, ts: {}, value: {}"), e.getT1(), e.getT2().getT1() , e.getT2().getT2());
```

## 필터링하기

- filter
- ignoreElements (다 통과 안시킴)
- take(n) 처음 n개 제외
- takeLast 마지막
- takeUntil(predicate) 조건true때까지
- elementAt(n) n번째
- single - 소스가 하나만 있어야함 (0개 x , N개 x )
- skip, take 로 특정시간까지 원소 건너뛰기

```java
Mono<?> startCommand= ...
Mono<?> stopCommand=..
Flux<UserEvent> streamOfData = ...

streamOfData
        .skipUntilOther(startCommand)
        .takeUntilOther(stopCommand)
        .subscribe(system.out::println);
```
streamOfData 에서 startcommand 들어온때부터 stopCommand 들어온때까지 받기.


## 수집하기
collectList()
collectSortedList()
하면 Mono 타입 스트림이 나온다. Mono<List<T>> 이런느낌.

.subscribe로 받아서 쓰면된다.

collectMap 은 Map<K, T>
collectMultimap Map<K, Collection<T>> 
등.
Flux.distinct()는 모든 원소를 추적한다. 그러니 스트림 원소 많으면 distinct 중복체크 함수 셀프 최적화 권장
Flux.distinctUntilChanged() 는 무한 스트림에 중단 없는 행에 나타나는 중복 제거.
(111 22 33 2 11) -> 1 2 3 2 1

## 스트림 원소 줄이기
hasElement 연산자 : 찾는 원소 발견되면 즉시 true 반환

`stream3.hasElement(9).subscribe(System.out::println); // true`

Mono<> 가 반환된다.

any 연산자는 다양하게 검사가능하다 

`stream3.any(val -> val%2 ==0).subscribe(System.out::println); // true`
다만, true or false만 나온다. 스트림에 뭐가 있냐~ 이런거

reduce는 아는 대로의 행동이지만, scan은 reduce되는 중간값을 알 수 있다.
scan은 초기값출력이후 매 stream event마다 acc의 값을 출력해준다.

```java
Flux.range(1,5)
        .scan(0, (acc,elem) -> acc +elem)
        .subscribe(result -> log.info("Result:{}",result));
```

```java
stream3.any(val -> val <0).thenMany(Flux.just(4,5)).subscribe(System.out::println); //4, 5만 나온다.
```
thenMany, then, thenEmpty 이런게 있는데, 상위 스트림에서 들어오는 원소 무시하고 완료 또는 오류 신호를 내보내거나, 자기자신에게 배정된 새 스트림 기동.

concat
merge
zip
combineLatest ( zip이랑 같지만, 하나의 원소 없어도 먼저 들어온거부터 값 생성)


## 스트림 내 원소 일괄처리

Buffering : 스트림 타입이 FLux<List<T>>
windowing : 스트림 타입이 Flux<Flux<T>> (5분동안 쌓인 스트림을 처리하겠다 이런느낌)
Flux<GroupedFlux<K,T>> : 그룹이 된다.

`Flux.range(1,7).groupBy(e -> e %2 ==0 ? "Even" :  "odd");`
식으로 하면 이걸 subscribe할때 각 subcribe 별로 다른 stream이 구독된다.

scan을 사용하면 new List<>() 로 초기화 하면 Even끼리만 쌓여서 Even: [4,  6] 다음번에 Odd: [5,7] 이런식으로 되는것을 볼 수 있다.

## flatMap, concatMap, flatMapSequential
한개의 원소가 여러개의 flux가 될 수 있다.
그래서 flatMap()의 결과로 생성되는 flux는 Flux<integer> 이런식으로 나온다.
다만 flatMap은 순서를 보장하지 않는다

concatMap, flatMapSequential은 각각 순서가 유지된다.

## sample(DUration.ofMillis(20)) 으로 샘플링 ( 특정기간 내 최근값)

## 리액티브 시퀀스를 블로킹 구조로 변경가능
toIterable 등. 
blockFirst ( 업스트림이 첫번째 값을 보내거나 완료될때까지 현재 스레드 차단)
## 시퀀스 처리하는 동안 처리내역 확인 

doOnNext(Consumer <T>) Flux나 Mono의 각 원소에 대해 뭐 해라. (subscriber에 의존적이지 않게 할 수 있는거 .뭐 로그를 찍는다거나)
doOnComplete() 
doOnSubscribe()
doOnTerminate
doOnEach (어떤 경우에도 처리됨 onSubscribe, onNext, onError, onComplete)
즉, 발행자 주체적인 뭔가 가능

## 데이터와 시그널 변환하기
signal이란 onNext(1) 이런걸 말한다. 
data는 1 이런걸 말하고.
이벤트를 Signal 클래스로 래핑해서 보내준다.
materialize() 가 signal로 변환
dematerialize() 가 data로 변환


## 적합한 연산자 찾기
https://projectreactor.io/docs/core/release/reference/#which-operator

## 코드를 통해 스트림 만들기
push, create
```java
Flux.push(emitter -> IntStream)
        .range(2000, 3000)
        .forEach(emitter::next))  # emitter.next(2001); 이런식으로 flux에게 다음 원소가 뭔지 알려주는 방식인듯하다.
        
        .delayElements(Duration.ofMillis(1))
        .subscribe(e -> logl.info("onNext: {}", e));
```
push를 사용해서 기존 API인 자바 stream api를 이용해 1000개 정수를 만들어서 배압 상황처럼  

generate 메서드로 "초기값", "(accumulated, 다음에넘길값) -> { return ... }" 두개를 선언하면, 
accumulated 값이 다음 값으로 나타난다.

## 일회성 리소스를 리액티브 스트림 라이프 사이클에 래핑시키기

이를테면 httpConnection을 만들기 위해서 `Connection`이란 객체를 만들어야 한다고 생각해보자.
그러면, flux 내부에서 connection을 생성하고 닫아줘야할텐데 닫는걸 어떻게 구현하지? 

```java
Flux<String> ioRequestResults = Flux.using(
        Connection::newConnection,
        connection -> Flux.fromIOterable(connection.getData()),
        Connection::close
        );
```
이런식으로 하면, using이 어떤 객체가 만들어져야 하고, onComplete에 사라져야 하는지 알게 된다. 

근데 using 연산자는 Callable (Connection::newConnection 과 같은) 을 사용해 관리 자원을 동기적으로 검색한다.
usingWhen 연산자를 사용하면, Publisher의 인스턴스에 해당 인스턴스를 가입시켜서 리액티브 타입으로 검색할 수 있다.
메인스트림의 성공이나 실패에 대해 각각 다른 핸들러를 사용할 수 있다 ( 멀티 스레드에 대응가능한가보다 )

둘다, 각 subscriber 하나당 하나의 resource를 만드는 것은 똑같은데, 책에서처럼 Flux.defer() 메서드를 통해
onComplete 나 onError() flux를 제공하게 되면 - 모든 쓰레드가 같은 flux를 들고 있을수 있다. (close 핸들러를 가지고 있는 flux를 나누어 가질 수 있다.)
https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#usingWhen-org.reactivestreams.Publisher-java.util.function.Function-java.util.function.Function-

그니까 실제로 onNext()를 해서 원소를 subscriber에게 건네주는 쓰레드랑, 리소스를 초기화 해주는 스레드가 다를수 있다는 장점인것 같다.


