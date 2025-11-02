# logstash 

- 비츠로 데이터를 수집해 ES 에 보내는것도 도움되지만, 검색과 분석에 유용하게 변환하는것도 중요하다. 
- Extract, Transform, Load (ETL) 도구이다. 
- push model (인제스트한 모든 데이터를 집계하는 지점) 또는 pull model (다른 소스 시스템에서 데이터 추출 및 HTTP API 폴링 가능) 으로 사용가능.
    - 하이브리드로도 사용가능


## Logstash 구성요소 

- 파이프라인
  -  워크로드를 처리하기 위해 구성된 플러그인 모음
  - 하나의 logstash 인스턴스가 여러 파이프라인을 (서로 독립적으로) 실행가능
- 입력 플러그인
  - pre-define 된 소스 시스템에서 데이터 추출하거나 수신 
- 필터 플러그인
  - 들어오는 이벤트 변환, 보강 
- 출력 플러그인
  - 특정 대상 시스템으로 데이터 로딩, 전송


클러스터로 동작하지 않아서, 각각의 로그스태시 인스턴스는 서로를 인식하지 못함. 다만 여러개 로그스태시 인스턴스 사용하면 인스턴스 사이에 로드 밸런싱 될것. 
  - 뭔소리냐면, filebeat쪽에서 여러개의 Logstash로 전송하게 세팅할 수 있다. 그러니까 로드 밸런싱이 된다는것. 


## logstash.yml 세팅값 

로그스태시 설정 및 구성 옵션중 중요시 봐야할 것 
- pipeline.batch.size
  - 필터 플러그인, 출력 플러그인 실행시마다 허용되는 최대 이벤트 개수 정의 (스레드당 125개 이벤트가 default) window 사이즈인셈
- pipeline.batch.delay 
  - batch.size 채워지지 않더라도 몇초까지 기다렸다 전송할지 정하는 값 (50ms) 
- queue.type
  - default로 메모리 기반 대기열 사용하는데, `persistd` 로 설정한다면 디스크 기반 대기열 


## 첫 파이프라인 실행 

[logstash-pipeline.conf](./logstash-pipeline.conf)
```
{
       "@version" => "1",
        "message" => "hello_world",
        "event" => {
              "original" => "hello_world"
        },
        "host" => {
              "hostname" => "abc-3.local"
        },
     "@timestamp" => 2025-11-02T03:40:27.137131Z,
    "description" => "First pipeline!"
}

```

이렇게 나오게 된다. 이건 근데 json형태가 아닌거같다. 

```
output {
    stdout {
        codec => json
     }
 }
```

이렇게 지정했어야한다.

```
{"message":" Hello world x2","@version":"1","@timestamp":"2025-11-02T03:52:48.464626Z","event":{"original":" Hello world x2"},"description":"First pipeline!","host":{"hostname":"abc-3.local"}}
{"message":"hello_world x1 ","@version":"1","@timestamp":"2025-11-02T03:52:48.464083Z","event":{"original":"hello_world x1 "},"description":"First pipeline!","host":{"hostname":"abc-3.local"}}
```

잘되는구만.



```json
{
  "u881001": {
    "name": "Jim Mar",
    "department": "Marketing",
    "email": "Jim.Mar@corp.com",
    "login_country": "Australia",
    "using_vpn": true
  }
  // ...
}
```

이런식의 dictionary 룩업도 가능하다. 


## 이벤트 스트림을 단일 이벤트로 집계하기. 

그냥 COUNT 이런 정보만 남기는게 좋을 수도 있다. 모든 단일 이벤트를 남기기 보다는. 

루비 코드로 aggregate 정의할 수 있음.


## 로그스태시를 사용해서 파일비트로 수집된 사용자 정의 로그 처리 


