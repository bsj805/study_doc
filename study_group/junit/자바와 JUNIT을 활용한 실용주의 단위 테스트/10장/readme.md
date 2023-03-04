https://www.baeldung.com/spring-boot-testing
1. `@SpringBootTest` 어노테이션은 `@Mock`과 일반적으로 같이 쓰지 않는다. 이유는?(3가지)

<details>
<summary> 정답: </summary>
1. 일단 Mock 객체는 작은 함수단위를 테스트하고자하는 unittest의 목적이 강하다.Integration test때에 보통 @SpringBootTest<br/>
2. unittest가 길어지면 안좋다 (FIRST - FAST) <br/>
3. SpringBootTest 어노테이션을 이용해 전체 컨테이너를 세팅하면 시간적 비용이 너무 커진다. <br/>
</details>

2. 
```java

public class urlRequester{
    private OkHttpClient client;
    private String url;
    UrlRequester(OkHttpClient client,String url,String port){
        this.client =client;
        ...//생략
    }
    String request(String contentId){
        HttpUrl httpUrl = new HttpUrl.Builder().scheme("http")
                .scheme("http")
                .host(url)
                .addQueryParameter("contentId",contentId).build();
        Request request = new Request.Builder().url(httpUrl).get().build();
        Call call = client.newCall(request);
        return call.execute().body().string();
    }
}

----

public class urlRequesterTest{
    @Mock private ClientImpl clientImpl; // 
    @InjectMocks UrlRequester urlRequester; // <-? 
    
}
```
문제2. urlRequester는 두개 이상의 인자가 필요한 상황이다. 어떻게 하지?<br/>
문제3. ClientImpl은 어떤 interface를 implement하고 있어야할까?<br/>

<details>
<summary> 2,3정답: </summary>
2.1 urlRequester처럼 두 개 이상의 인자를 필요로 하는 상황이면 인자를 하나로 줄이거나, `@Before` 같은걸로, new UrlRequester해라.<br/>
3.1 inject되는 mock 객체는 안에서 불릴 수 있는 모든 함수에 대해서 implement해야한다. 따라서, newCall, execute()  <br/>
</details>

불펌<br/>
### 3.1 생성 타임스탬프(변동하는 시간)를 검증하고자 하는데, 반복 가능하게 테스트 코드를 구현하려면 어떤 방법을 사용해야 하나?

<details>
<summary>정답</summary>
  <div markdown="1">
  목 객체를 사용하여 시간 변화에 독립성을 유지시킨다.
  </div>
</details>
</br>
