# 1장

tomcat과 다른 네티

## tomcat
요청당 쓰레드를 만들어서,각 요청별로 쓰레드를 생성하는 작업을 진행하면 
요청 * 생성하는 쓰레드수 만큼 쓰레드가 늘어나고, thrashing이 발생
또한, 만들어진 쓰레드도 100% utilize 되지 않고, request를 보내는등 i/o 블로킹이 발생하면 논다.

-> servelet API 3.0 부터는, 서블릿을 실행한 스레드가 사라져도, 별도의 스레드로 응답할 수 있게 되었다. 
무작정 스레드가 늘어나는 일을 막을 수 있게 되었다. 

## 네티
몇개의 "요청을 받는 쓰레드" 가 존재하고, 이 쓰레드들은 callback을 register 하고, publisher와 함께 즉시 return된다.
이벤트 큐에는 저 callback들을 실행해줄 이벤트가 담겨있고,
이벤트 루프쓰레드에서는 큐에서 작업을 뽑아서 작업을 진행한다. 

## 스프링 클라우드
분산시스템 구축을 단순화하는 기반 프로젝트로, 리액티브 시스템을 구축하는데 적합할 수 있다.
자바에서는 보통 명령형 프로그래밍 기법(imperative programming)을 사용해서 코드를 작성한다.

하지만 `Output output = scService.calculate(input)`
이런식으로 받는 것은 리액티브 하지 않다. HTTP 요청이나 DB 요청같이 I/O 작업을 요청하면 쓰레드가 쉰다.

그래서 대신, 콜백 기법을 적용할 수 있다.

```java
interface ShoppingCardService {
    void calculate(Input value, Consumer<Output> c);
}
```
```java
class OrderService {
    private final ShoppingCardService scService;
    void process(){
                Input input =...;
                scService.calculate(input,output -> {...});
        }
}
```
이렇게 하면, callback을 register 해두고, scService 내부에서 callback 함수를 실행하면 실제 결과에 대한 처리를 게속할 수 있다.
그리고 process()다음에 오는 로직들을 쭉 실행하고, 이 결과값을 실제 가져다 쓰는 부분에서 사용할 수 있다.

### Consumer을 사용한 구현
scService에 뭐가 올 수 있냐면,

```java
class SyncShoppingCardService implements ShoppingCardService {
    public void calculate(Input value, Consumer<Output> c){
        Output result = new Output();
        c.accept(result);
    }
}
```
`Consumer`을 사용하면 이렇게 나중에 리턴시킬 수 있다.

### Future을 이용한 구현
```java
interface ShoppingCardService {
    Future<Output> calculate(Input value);
}
```
```java
class OrderService {
    private final ShoppingCardService scService;
    void process(){
                Input input =...;
                Future<Output> future = scService.calculate(input);
                ...
                Output output = future.get();
                ...
        }
}
```
Future은 사용가능한 결과가 있는지 확인한다. future.get()은 블로킹이 되지만, 다른 로직을 더 사용할 수 있다.

이를 개선한 CompletionStage는 `Promise` 처럼 실행할 수 있다.

```java
interface ShoppingCardService {
    CompletionStage<Output> calculate(Input value);
}
```
```java
class OrderService {
    private final ShoppingCardService scService;
    void process(){
                Input input =...;
                scService.calculate(input)
                        .thenApply(out1->{...})
                        .thenCombine(out2->{...})
                        .thenAccept(out3->{...})
                
        }
}
```
반환된 결과에 관한 로직을 모아서 선언가능하다 ( 기능적 선언 방식 : 반환되었을 떄 어떤일을 할지 다 기술)
Apply나 Combine 등을 통해 여러 결과처리가 가능하다. 


# 2장

RxJava에 대해 알아보자.

# 2.1 관찰자 패턴

subject 는 자손들의 리스트를 가진다. 
subject에 등록된 관찰자는 subject의 메서드에 의해 상태 변경을 알림 받는다.

subject -> notify -> 관찰자


```java
public interface Subject<T>{
    void registerObserver(Observer<T> observer);
    void unregisterObserver(Observer<T> observer);
    void notifyObservers(T event);
}
```
```java
public interface Observer<T>{
    void observe(T event);
}
```
subject가 notifyObservers 를 하면 `observer.observe(event);` 가 호출되는 방식.

- Observer가 구독 절차를 담당할 수도 있고, 
- Subject에 Observer 등록해주는 3rd 컴포넌트가 필요할 수도 있다 (DI컨테이너의 @EventListener 어노테이션 사용)

```java
public class ConcreteSubject implements Subject<String>{
    private final Set<Observer<String>> observers= new CopyOnWriteArraySet<>(); // 쓰레드 세이프한 set (list를 read할때 무조건 복사본을 read하게함.)
    public void registerObserver(Observer<String> observer){
        observers.add(observer);
    }
    public void notifyObservers(String event){
        observers.forEach(observer -> observer.observe(event));
    }
    
}
```
unittest는 Mockito의 spy를 사용해서 실제로 해당 함수가 호출되었는지 확인하는 방식으로 진행. 
```java
@Test
void whenSpyingOnList_thenCorrect() {
    List<String> list = new ArrayList<String>();
    List<String> spyList = spy(list);

    spyList.add("one");
    spyList.add("two");

    verify(spyList).add("one");
    verify(spyList).add("two");

    assertThat(spyList).hasSize(2);
}
```

observer가 많을 경우에는 아래 이벤트 전파가 병목이 될 수도 있다.
```java
public void notifyObservers(String event){
        observers.forEach(observer -> observer.observe(event));
    }
```
만약 호출했는데 응답을 늦게하는 observer라면 ( 60초 뒤에 응답 ) - 30초마다 들어오는 이벤트들이 전파가 안될 수도 있다.
그러면 무지성으로 쓰레드 만들어서하면?

```java
ExecutorService executorService = Executors.newCachedThreadPool();
public void notifyObservers(String event){
        observers.forEach(observer -> executorService.submit( ()->observer.observe(event));
    }
```

이러면 , 쓰레드 풀 크기 제한 안하면 OutOfMemory 발생한다.

# 2.2 EventListener와 ApplicationEventPublisher
발행 구독 패턴이다. 

게시자 -> 이벤트 채널 (구독자가 구독함) -> 구독자

게시자와 구독자가 연관이 덜 된다. 

서버에서 클라이언트로 비동기 메시지 전달을 할 수 있는 웹소켓, SSE(Server-Sent Events)를 사용하면 
비동기식으로 클라이언트가 데이터를 받는게 가능하다. 이는 브라우저가 html5를 지원하면서 EventSource라는 js API가 사용되는데,
EventSource는 특정 URL을 호출해 이벤트 스트림을 수신한다. 

```java
@RestController
public class TemperatureController {
   static final long SSE_SESSION_TIMEOUT = 30 * 60 * 1000L;
   private static final Logger log = LoggerFactory.getLogger(TemperatureController.class);

   private final Set<SseEmitter> clients = new CopyOnWriteArraySet<>();

   @RequestMapping(value = "/temperature-stream", method = RequestMethod.GET)
   public SseEmitter events(HttpServletRequest request) {
      SseEmitter emitter = new SseEmitter(SSE_SESSION_TIMEOUT);
      clients.add(emitter);

      // Remove SseEmitter from active clients on error or client disconnect
      emitter.onTimeout(() -> clients.remove(emitter));
      emitter.onCompletion(() -> clients.remove(emitter));

      return emitter;
   }

   @Async
   @EventListener
   public void handleMessage(Temperature temperature) {

      List<SseEmitter> deadEmitters = new ArrayList<>();
      clients.forEach(emitter -> {
         try {
            emitter.send(temperature, MediaType.APPLICATION_JSON);
         } catch (Exception ignore) {
            deadEmitters.add(emitter);
         }
      });
      clients.removeAll(deadEmitters);
   }

   @ExceptionHandler(value = AsyncRequestTimeoutException.class)
   public ModelAndView handleTimeout(HttpServletResponse rsp) throws IOException {
      if (!rsp.isCommitted()) {
         rsp.sendError(HttpServletResponse.SC_SERVICE_UNAVAILABLE);
      }
      return new ModelAndView();
   }
}
```

이제 sensor에서 아래처럼 처음에 1초후에 probe함수를 부르게 한 뒤부터는, 5초마다 publisher.publishEvent를 하는데, 
```java
   @PostConstruct
   public void startProcessing() {
      this.executor.schedule(this::probe, 1, SECONDS);
   }

   private void probe() {
      double temperature = 16 + rnd.nextGaussian() * 10;
      publisher.publishEvent(new Temperature(temperature));

      // schedule the next read after some random delay (0-5 seconds)
      executor.schedule(this::probe, rnd.nextInt(5000), MILLISECONDS);
   }
```
이 이벤트는
```java
   @Async
   @EventListener
   public void handleMessage(Temperature temperature) {
```
여기서 그대로 받아서 처리를 하게 된다. 
그럼 이 함수에서는 현재까지 등록된 sseEmitter들에게 온도를 전달하게 된다.
SseEmitter는 전송할때 오류가 나면 더이상 응답하지 않은 client인지 확인할 수 있다. 그래서 저부분에서 제거가 일어난다.
그럼 클라이언트에서는 EventSource API를 통해 온도값을 받게 된다. 

그러나 여기서의 문제는 @async 함수로 실행이 되고 있어서, 아무 sseEmitter도 등록이 안되어 있어도 쓰레드가 계속 호출된다는 것이다.

이러면 비동기 실행을 위한 쓰레드 풀을 잡아주어야 한다.

쓰레드 풀을 잡을때, 큐 용량을 올바르게 구성하지 않으면 쓰레드 풀이 커질 수 없다고 한다.
SynchronousQueue가 사용되기 때문이라는데, 

뭔소리일까?

workQueue : 모든 쓰레드가 작업 중일때 task 를 보관할 큐.
corePoolSize :기본적으로 관리할 쓰레드 숫자
maximumPoolSize: corePoolSize 를 초과하여 최대로 만들 쓰레드 숫자

즉, task가 들어갈 Queue의 사이즈가 제대로 구성되지 않으면 SynchronousQueue, 즉 task를 보관할 버퍼 사이즈가 0이고,
thread들의 queue를 구성해서, thread가 하나씩 item을 빼가도록 하는 것이다.

https://multifrontgarden.tistory.com/276
단순히 생각하기로는 corePoolSize 만큼 쓰레드들에게 task 를 할당하고, 
이 이상 task 가 들어오면 maximumPoolSize 까지 쓰레드를 추가하며 task 를 실행시키다가 
maximumPoolSize 까지 쓰레드가 꽉 찼음에도 task 가 더 추가되면 그 때부턴 
workQueue 에 task 를 보관한다고 생각하기 쉽다. 아니다.

```java
A ThreadPoolExecutor will automatically adjust the pool size (see getPoolSize()) 
 according to the bounds set by corePoolSize (see getCorePoolSize()) and maximumPoolSize (see getMaximumPoolSize()). 
When a new task is submitted in method execute(java.lang.Runnable), 
and fewer than corePoolSize threads are running, a new thread is created to handle the request,
even if other worker threads are idle. 
If there are more than corePoolSize but less than maximumPoolSize threads running, 
a new thread will be created **only if the queue is full.** 
        
By setting corePoolSize and maximumPoolSize the same, 
you create a fixed-size thread pool. 
By setting maximumPoolSize to an essentially unbounded value such as Integer.MAX_VALUE, 
you allow the pool to accommodate an arbitrary number of concurrent tasks. 
Most typically, core and maximum pool sizes are set only upon construction, 
but they may also be changed dynamically using setCorePoolSize(int) and setMaximumPoolSize(int).
```
자 중간에 엔터된 부분을 보면, 
corePoolsize만큼 늘어난다음에, queue를 채우려고 한 다음에, maximumPoolSize만큼 늘어난다.
즉 쓰레드가 corePoolSize개수만큼 늘어난다음에, 그래도 job이 더 있으면, queue에 job을 쌓은다음에, 
queue도 꽉찼다 하면, maximumPoolSize만큼 쓰레드를 늘린다.

work queue는 각 쓰레드 별로 생성이 되기 때문에, job이 쌓일 수 있는데, 오히려 다른 쓰레드랑 간섭이 없으니 lock은없다. 
이게 synchronous queue가 되어버리면 blocking하면서 하나의 쓰레드마다 작업하나를 가져가게 하기 때문에, 동시성이 제한된다.

### 단점
1. 근데 만약 event 개수가 많아지면, 각 event 종류마다 ( 각 스트림마다) Async 메서드가 돌면서 스트림 개수에 비례해서 이벤트가 늘어난다.
2. EventListener은 스프링 내부라서, 스트림 종료시 어떻게, 오류시 어떻게 할지 구현을 추가하기 어려움. ( 스트림 종료나 오류에 대한 별도의 오브젝트 ,클래스 상속 구조 정의해야.)
3. 온도 이벤트를 비동기적 브로드 캐스팅하기 위한 스레드 풀 사용 -> 이벤트 쓰레드가 자신의 사이클 돌면서 계속 각기 다른 이벤트 처리하는게 바람직.
4. 클라이언트 하나도없는데 이벤트 발생

# RxJAVA

Observer는 subject에게 3가지 이벤트를 받을 수 있다. 다음 처리할 이벤트 콜백, 스트림 종료됐다 (onComplete), 스트림 에러났다 (onError)

```java
Observable.create(
        sub -> {
            sub.onNext("helloworld");
            sub.onCompleted();
        }
        ).subscribe(
                System.out::println, //onNext
        System.err::println, // onError
        () -> System.out.println("Done!");
        )
```
이런식으로 간편히 등록가능.

Observable 객체는 아래처럼, 다양한 방식으로 만들 수 있고,
```java
Observable.just("1","2","3","4");
Observable.from(new String[]{"1","2","3","4"});
```
callable이나 Future을 활용할 수도 있다.
```java
//future활용하면
Future<String> future = Executors.newCachedThreadPool().submit(()->"world");
Observable<String> world = Observable.from(future);
```
나중에 future.get()을 해서 받을 수 있는데,  (.get은 블로킹 콜)
이런 future을 나눠가질 수 있다.

이런 하나의 이벤트만 발생시키는 것 외에도 비동기 시퀀스 생성이 가능하다.

### 비동기 시퀀스 생성하기

```java
Observable.interval(1, TimeUnit.SECONDS)
        .subscribe(e -> System.out.println("Received: " + e));
Thread.sleep(5000);
```

이런식으로 주기적으로 이벤트시퀀스를 비동기적으로 생성하는 애도 있다.
Thread.sleep()을 안부르면 바로 프로세스가 종료된다. 별개의 쓰레드에서 observable이 만들고 있다.
메인쓰레드는 그냥 종료해버린다.

가입 취소기능도 만들수 있다.

### 페이징 기능

일반적으로는 URL에 query랑 몇개의 검색결과를 원하는지 보낸다.
`List<URL>` 을 클라이언트가 리턴받는다.
커서 방식으로 전환해서, 클라이언트는 현재 검색결과를 표시하고, 서버는 다음 검색결과를 미리 반환받아놓는다.
`Iterable<URL>` 을 클라이언트가 리턴받아보자.

서버는 검색결과를 보낼때마다 다음 페이지 검색결과를 로드해놓고, Iterable.next()가 불릴때까지 대기한다.
클라이언트는 다음 페이지 검색결과를 원하면 해당 Iterable.next()를 호출한다.

아니면 아예 `CompletableFuture<List<URL>>`을 반환할 수 있다.
근데 이건 그냥 클라이언트가 api 호출하자마자 바로 리턴받는다 외에는, URL list 받기까지 똑같이 기다려야한다.
RxJava로 솔루션을 개선해보면, 아예 observable을 리턴시켜버려서, 클라이언트가 직접 이벤트를 받아 처리하게 한다.
이러면 observable에 subscribe를 할 수 있게 되고, 프로그램의 응답성을 높여준다. 

만약 Observable에 처리속도가 느린 함수를 배정할때에는 별도의 스레드를 사용해서
```java
Observable.subscribeOn(Schedulers.io()) 
```
이 함수로 별도의 쓰레드에서 스케줄링이 가능하나, 스레드 관리가 어렵다.
불변 객체를 사용하는 것이 좋다. 
함수형 프로그래밍에서 필수. 

```java
  private final Observable<Temperature> dataStream =
      Observable
         .range(0, Integer.MAX_VALUE)
         .concatMap(ignore -> Observable
            .just(1)
            .delay(rnd.nextInt(5000), MILLISECONDS)
            .map(ignore2 -> this.probe()))
         .publish()
         .refCount();
```

publish 이후 refCount()를 붙이면 매 이벤트마다 구독자가 있는지 확인해서 이벤트를 발생시키지 않는다.
concatMap을 이용해서 
- `0 probe()의리턴값`
- `1 probe()의리턴값`
- `2 probe()의리턴값`
식으로 이벤트를 발생시키게 된다.

publish()를 안붙이면, 각 구독자는 모두 개별적인 observable을 가진다. 
publish 하면 모든 대상스트림으로 브로드캐스팅을 할 수 있다.
이제는 RxSeeEmitter은 subscriber을 내부적으로 가지면서, onNext(event) 마다 send함수를 호출한다.
```java
this.subscriber = new Subscriber<Temperature>() {
            @Override
            public void onNext(Temperature temperature) {
               try {
                  RxSeeEmitter.this.send(temperature);
               } catch (IOException e) {
                  log.warn("[{}] Can not send event to SSE, closing subscription, message: {}",
                     sessionId, e.getMessage());
                  unsubscribe();
               }
            }
```

전체 리액티브 환경을 아우르며 호환성을 보장하는 표준 API는 "리액티브 스트림"으로 정의가 되어있다.

