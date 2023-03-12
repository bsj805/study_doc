# 3장 스트림의 새로운 표준 - 리액티브 스트림

# API 불일치 문제

- `CompletionStage, completableFuture` 사용하던 자바 코어 라이브러리
- RxJava 라이브러리
- 스프링4의 `ListenableFuture` 같은 프레임워크 특정 클래스

비동기 구현하려고 여러 선택 가능하다. 하지만, 여러 시스템 사이의 호환성을 위해 코드 고쳐야 하는 문제 존재.

이를테면

`ListenableFuture`은 .addCallback(onComplete, onEerror) 을 통해서 콜백을 등록하고,
`CompletionStage`는 `.thenApply().thenCombine().thenAccept()` 이런게 필요하다. 그래서 직접 생성자를 통해 변환시켜줘야 한다.
하지만, 이렇게 개발자가 직접 인터페이스와 클래스를 제작해 변환시켜주는 것은, 
- 버그 유입 가능성
- 추가 유지보수 필요
등의 이유로 좋지 않다.
하지만 라이브러리 공급자가 따를 표준 명세가 존재하지 않았다.


# 풀 방식과 푸시 방식

json 데이터가 DB에 string으로 박혀있고, 조건에 맞는 데이터를 10개 가져와야 한다고 해보자.
그러면 json데이터를 하나 달라고 한 뒤, string을 파싱해서, 만약 조건에 맞으면 10개 -> 9개. 
또, 10개보다 적으면 게속 DB에게 json데이터를 요청할 것이다.
이런 식으로 요청하는 방식이 PULL 방식이다.
하지만, DB가 쉬고 있는 시간들이 생기고, 비효율적이다 (대기시간)

그러면, DB에서는 stream으로 계속 쏴주고 클라이언트에서는 파싱을 해서 10개가 채워질때까지 스트림을 받는다면 어떨까? 
즉, 비록 과하게 쏴주더라도, 취소 신호가 올때까지 쏴주면 어떨까.
이게 바로 PUSH 방식이며, DB의 대기시간을 줄일 수 있다는 장점이 존재한다


# 흐름 제어
푸시 모델은 요청하는 횟수를 최소화 해서 전체 처리시간을 최적화하려고 한다. 하지만, 
- 무한한 메시지 스트림을 서비스가 수신할 수 있어야 하며
- 프로듀서는 항상 무리한 일을 하게 된다.

1. 느린 프로듀서와 빠른 컨슈머
   - 컨슈머가 너무 빨리 처리해서 프로듀서의 큐가 항상 빈다.
   - 순수 `푸시` 모델은 더 빠르게 달라 등의 요구를 조절할 수 없어서, 동적으로 시스템 처리량 증가는 어렵다.
2. 빠른 프로듀서와 느린 컨슈머가 존재한다면
   - 프로듀서가 컨슈머 처리 가능량보다 많이 보낸다. 그러면 큐를 사용해 초과량을 수집해둔다면?
     - 무제한 큐
       - 큐 사이즈 제한 x. 모든 메시지가 전달되지만, 메모리 한도 등에 도달하면 전체 시스템 손상
     - 크기가 제한된 드롭 큐
       - 메모리 오버플로 방지를 위해 큐가 가득차면 신규 유입된 메시지 무시.
         - 데이터 변경 `True,False`을 요청하는 이벤트라면 몇번이 오던 존재만 하면 상관이 없다. 이런 류에 쓴다.
     - 크기가 제한된 블로킹 큐
       - 유입 자체를 차단해서, 스트림에서 그만 보내도록 한다. 가장 느린 컨슈머때문에 모든 동작이 블로킹됨 (비동기가 아님) 

그래서 순수 푸시 모델은 다양한 부작용을 낳는다. 배압 제어 메커니즘이 필요하다.

RxJava 1.x 에서는 배압 제어 메커니즘이 존재하지 않으나, 2013, reactive 스트림의 초안이 발표됐다.


# 리액티브 스트림의 기본 스펙
- Publisher
- Subscriber
- Subscription
- Processor

라는 기본 인터페이스가 정의되어 있다. 

## Publisher는

```java
public interface Publisher<T> {
    void subscribe(Subscriber<? super T> s);
}
```
subscribe 액션을 하는 subscriber는, Publisher가 내뿜는 T 클래스와 T 클래스의 부모들만 인자로 받는다.
즉, 이 원소를 받을 수 있는 클래스여야 한다.

## Subscriber
```java
public interface Subscriber<T>{
    void onSubscribe(Subscription s); // 새로 생김. subscription 변수를 넣으면 채워준다.
    void onNext(T t);
    void onError(Throwable t);
    void onComplete();
}
```

onSubscribe는 구독이 성공했음을 알리는 방식이다. Subscription 클래스는

## Subscription
```java
public interface Subscription{
    void request(long n);
    void cancel();
}
```
`request`로 Publisher가 보내줘야 하는 데이터의 크기를 알릴 수 있다. 2^61 -1 까지 가능하다.

하이브리드 Push-pull 모델을 사용할 수도 있다. 
```java
public Publisher<Item> list(int count){
    Publisher<Item> source = dbClient.getStreamOfItems(); // db에게서 stream얻어옴.
    TakeFilterOperator<Item> takeFilter = new TakeFilterOperator<>(
            source,
        count,
        item -> isValid(item);
        );    
    return takeFilter;
}
```
우리의 목적은 db로부터 valid한 item만 뽑기. 

이렇게 하고서, 
```java
public class TakeFilterOperator<T> implements Publisher<T> {

    private final Publisher<T> source;
    private final int          take;
    private final Predicate<T> predicate;

    public TakeFilterOperator(Publisher<T> source, int take, Predicate<T> predicate) {
        this.source = source;
        this.take = take;
        this.predicate = predicate;
    }

    public void subscribe(Subscriber s){ // publisher인 DB와의 stream에 대해서 구독을 시키는데, 구독자는 TakeFilterInner<>인것.
        source.subscribe(new TakeFilterInner<>(s, take, predicate)); //TakeFilterInner가 구독을 함으로써, TakeFilterInner에서 내보낸 값을 "s"가 받도록 구현함.
    }
    
    static final class TakeFilterInner<T> implements Subscriber<T>, Subscription {
        TakeFilterInner(Subscriber<T> actual, int take, Predicate<T> predicate){};
        // actual이 실제로 predicate에 의해 필터된 값을 받고 싶어하는 애. take는 Publisher 생성할때 지정한값. predicate은 DB에서 받는 값의 조건
        
        public void onSubscribe(Subscription current){
            ...
            current.request(take); // 이제 이 TakeFilterInner는 필터를 해야되니까 원본으로부터 값을 take개수만큼 받아와야 한다.
            ...
        }
        /*
        public void onSubscribe(Subscription current) {   // publisher에 subscribe할 때, publisher가 이 함수를 불러서 current를 채워줌.
			if (this.current == null) {
				this.current = current;

				this.actual.onSubscribe(this);  // 그리고 사실 actual도  실제 subscribe를 이 TakeFilterInner에 하는 셈이라서, actual도 취소할때, 이 TakeFilterInner에 취소 요청을 해야 한다.
				if (take > 0) {
					this.current.request(take);
				} else {
					onComplete();
				}
			}
			else {
				current.cancel();
			}
		}
         */
        
        public void onNext(T element){
            ...
            // 성공시
            if(isValid && requested > 0 && isQueueEmpty) {
                a.onNext(element); // 실제로 TakeFilterOperator라는 publisher에 subscribe한 "a" 라는 Subscriber에게 값 전달하는 로직.
            }
            ...
            if(remaining==0){
                s.cancel(); // OnSubscribe 에서 DB publisher가 등록하면서 내어준 subscription 객체의 cancel을 불러서, DB한테 나 그만 받을래 하는것.
                onComplete();  // 스트림이 끝났으니까, onComplete()를 자체적으로 부른다. - 구독 취소할때는 onComplete()가 불리지 않는다.
            }
            ...
        }
    }
}
```

보통 처음 데이터베이스 연결되고, TakeFilterOperator 인스턴스가 Subscription을 받으면 (`OnSubscribe()` 가 불려서)
TakeFilterInner 가 subscription.request(10) 이런식으로 호출해서 데이터베이스에서 element 달라고 보낸다.
그러면 10개의 원소가 오게 된다. 데이터의 새 부분을 요청하더라도, 데이터를 프로세싱하는 도중에 요청하기 때문에, 
(받아야할게 많이 남았는데 queue에 쌓일만한게 너무적으면 subscription.request()를 더 부름)
기존보다 대기시간이 적다. 

순수 푸시 모델이 바람직한 경우도 있는데, 리액티브 스트림은 동적 푸시 풀 모델, 푸시 모델, 풀 모델도 지원.
순수 푸시 모델은 2^63 -1 개 요청하면 된다.

순수 pull 모델은 onNext() 마다 1개씩 요청하면된다

# 리액티브 스트림 동작해 보기.

뉴스 구독을 한다고 해보자.
그럼 뉴스 제작자가 있고, 구독자가 있으니, 각각 Publisher, Subscriber를 만들어보자.

```java
NewsServicePublisher newsService = new NewsServicePublisher();

NewsServiceSubscriber subscriber = new NewsServiceSubscriber(5);
newsService.subscribe(subscriber);
```
그럼, 구독을 진행한다음 subscriber가 subscription.request로 몇개를 달라고 하겠지. (리액티브 스트림 스펙을 따랐기 때문에 요청만큼 반환)

만약 이전 뉴스 요약본을 읽은 경우에만 새로운 뉴스 요약본을 보내는 서비스를 제공한다고 하면,

```java
public void onNext(newsLetter newsLetter){
    mailbox.offer(newsLetter);
} // mailbox라는 queue를 채운다.

public Optional<NewsLetter> eventuallyReadDigest(){
        NewsLetter letter = mailbox.poll();
        if (letter != null){
            
            if (remaining.decrementAndGet() ==0 ){
                subscription.request(take);
                
                remaining.set(take);
                
            return Optional.of(letter);
        }
        return Optional.empty();
    }
}
```

이렇게 하면, 뉴스가 다 떨어질 때 다시 채워달라는 요청을 보낸다. 스트림에 미리 요청을 보내는 방식인것이다. 
remaining은 결국 queue에 남은 메일 개수랑 일치할것. 또는 queue가 너무 작으면 스트림에 대기하고 있는 분량을 포함해서.

```java
    public void onError(Throwable t) {
        Objects.requireNonNull(t);

        if (t instanceof ResubscribableErrorLettter) {
            subscription = null;
            ((ResubscribableErrorLettter) t).resubscribe(this);
        }
    }
```
이런식으로 에러가났을 때, 다시 subscribe를 요청할 수도 있다. (DB에 에러가 생기는 정도?)


# processor 개념의 소개

Processor은 Publisher와 subscriber의 혼합형태이다.
```java
public interface Processor<T, R> extends Subscriber<T>, Publisher<R>{
    
}
```

고로 Subscriber의 함수랑 Publisher의 함수를 모두 가진다.
Publisher (시작부), Subscriber(최종부) 사이 몇가지 단계를 추가할 수 있다.
이를테면 아까의 복잡했던 필터로직을 다르게 표현할 방법이 생긴것.

그냥 다 Processor로 해도 되지만, 이를테면 A->B로 단순 변환이 필요한 경우 Publisher와 Subscriber를 동시에 노출하는 인터페이스는 필요 없다.
Subscriber 인터페이스의 존재는 Processor가 업스트림을 구독하면 스트림 요소가 `Subscriber#onNext` 메서드를 시작할 수 있음을 의미.

문제점.

1. 다운스트림 Subscriber가 없을 때에는 스트림 요소가 손실될 수도 있다는걸 생각해야한다. 

즉, A -> B ->C 의 흐름으로 간다면, C를 B에 꼭 먼저 연결해야한다. (데이터 손실가능성)
즉 processor에게 subscriber를 먼저 연결한뒤, processor를 A에 구독시켜야 한다.

2. Processor를 구성하면 별도의 subscriber 관리가 필요 (메인 Publisher에 구독되지 않게 ) // onSubscribe함수를 조정하나??
3. 적절한 배압 구현 (큐 사용 등) 이 필요하다.

이런게 복잡하니까, 사실 Processor는 구독자의 존재 여부와 관계없이 멀티 캐스팅해야 할 때 그 진가를 알 수 있다.
멀티캐스트는 one to many or many to many
broadcast는 one to all

# TCK
리액티브 스트림 기술 호환성 키트 (Reactive Streams Technology Compatibility Kit) 
reactive stream spec을 모두 지키는지 + 라이브러리 호환에 대한 테스트 묶음

# 리액티브 스트림을 활용한 비동기 및 병렬 처리

리액티브 스트림 API는 Publisher가 생성하고, Subscriber가 소비한 모든 신호는 처리 중에 논 블로킹이어야 하며, 방해받지 않아야 한다는 명시가 있다.
리액티브 스트림 스펙에서의 병렬화 개념은 `Subscriber#onNext` 메서드를 병렬로 호출하는 것을 뜻한다. 
다만, onNext 시에 스레드 안정성을 보장하는 방식으로 신호를 보내야 하고, 다중 스레드에서는 외부적인 동기화를 사용해야 한다고 써있다.
즉, 직렬화되거나, 순차적으로 onNext가 불리는것을 보장하라는 것이다. 그래서 ParallelPublisher는 불가능, 스트림 요소처리도 병렬처리가 불가능하다.

자원을 효율적으로 처리하려면 어떻게 할것인가.?

publish -> 필터 -> 맵 -> subscriber -> output 

이런흐름 이라고 생각해보자.

각 단계에 메세지가 비동기적 전달을 해결책으로 둘 수 있다.
    - subscriber쪽만 별도의 스레드를 둔다.
    - 앞부분의 작업들이 쭉 처리되는 동안, subscriber은 자체적으로 실행되면서, publisher가 subscriber의 속도에 딜레이가 없다
    - 이런 작업을 비동기 경계를 설정한다고 하는데, 어떤 부분끼리 연결될지는 선택지가 있다.

1. publish쪽과 연결되어있다.
2. subscriber쪽과 연결되어있다. 
3. publish, 중간처리, subscriber 다 제각각 큐에서 사용되는 방식.

각각 CPU 집약적인 작업이 어디서 일어나는지에 달려있다.

이런식으로 분할하는 것은 자유롭지 않고, 균형을 유지하는 게 어렵다. 구현 및 관리도 어렵고,
리액터 프로젝트나 Rxjava에서 이런 API를 제공한다.

```java
public class DBPublisher implements Publisher<News> {
    private final MongoCollection<News> collection;
    private final String category;

    public DBPublisher(MongoCollection<News> collection, String category) {
        this.collection = collection;
	    this.category = category;
    }

    @Override
    public void subscribe(Subscriber<? super News> s) {
	    FindPublisher<News> findPublisher = collection.find(News.class);
	    findPublisher.sort(Sorts.descending("publishedOn"))
			     .filter(Filters.and(
		            Filters.eq("category", category),
			        Filters.gt("publishedOn", today())
			     ))
	             .subscribe(s);
    }
```
이런 몽고 DB 드라이버는 리액티브 스트림 기반의 드라이버를 사용할 수 있다.
이런 push 방식의 드라이버는 장점이, 100개를 한번에 내보내면 100개를 찾는시간동안 기다려야하지만,
1개씩 내보내면서 필터링을 하기 때문에 순차적으로 결과값을 100개까지 볼수있다. 즉 첫번째 element를 볼 수 있는시간까지 걸리는 시간이 짧다. 

# 다음시간에

스프링 프레임워크에서는 리액터 프로젝트가 있는데, 이 리액티브 라이브러리 도입이 큰 변화이다.
