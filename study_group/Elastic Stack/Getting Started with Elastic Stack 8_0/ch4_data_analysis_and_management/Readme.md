# 엘라스틱 서치 집계

- 메트릭 집계 
  - 합계, 최솟값, 최댓값, 평균
- 버킷 집계
  - 필드의 값에 따라 그룹화. 검색결과 내 텀의 빈도수, 범위, 날짜 등으로 버킷 제작 가능. 

```
GET web-logs/_search?size=0
{
    "query":{
        "range":{
            "@timestamp":{
                "gte":"2019-01-23T00:00:00.000Z",
                "lt": "2019-01-24T00:00:00.000Z"
            }
        }
    }
}

```

?size=0 을 query param으로 붙이면 개별문서 반환 x 

```
GET web-logs/_search?size=0
{
    "query":{
        "range":{
            "@timestamp":{
                "gte":"2019-01-23T00:00:00.000Z",
                "lt": "2019-01-24T00:00:00.000Z"
            }
        }
    },    
    "aggs":{
        
        "hourly":{
            "date_histogram": {
              "field": "@timestamp",
              "calendar_interval": "hour"
            }
        },
        
            "bytes_served":{
                "sum": {"field": "http.response.body.bytes"}
            }
        
    }
}
```

시간별로 결과값을 얻으려면, hourly

<details>

```
{
  "took": 12,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4654,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "hourly": {
      "buckets": [
        {
          "key_as_string": "2019-01-23T00:00:00.000Z",
          "key": 1548201600000,
          "doc_count": 36
        },
        {
          "key_as_string": "2019-01-23T01:00:00.000Z",
          "key": 1548205200000,
          "doc_count": 33
        },
        {
          "key_as_string": "2019-01-23T02:00:00.000Z",
          "key": 1548208800000,
          "doc_count": 34
        },
        {
          "key_as_string": "2019-01-23T03:00:00.000Z",
          "key": 1548212400000,
          "doc_count": 60
        },
        {
          "key_as_string": "2019-01-23T04:00:00.000Z",
          "key": 1548216000000,
          "doc_count": 124
        },
        {
          "key_as_string": "2019-01-23T05:00:00.000Z",
          "key": 1548219600000,
          "doc_count": 212
        },
        {
          "key_as_string": "2019-01-23T06:00:00.000Z",
          "key": 1548223200000,
          "doc_count": 290
        },
        {
          "key_as_string": "2019-01-23T07:00:00.000Z",
          "key": 1548226800000,
          "doc_count": 326
        },
        {
          "key_as_string": "2019-01-23T08:00:00.000Z",
          "key": 1548230400000,
          "doc_count": 332
        },
        {
          "key_as_string": "2019-01-23T09:00:00.000Z",
          "key": 1548234000000,
          "doc_count": 307
        },
        {
          "key_as_string": "2019-01-23T10:00:00.000Z",
          "key": 1548237600000,
          "doc_count": 299
        },
        {
          "key_as_string": "2019-01-23T11:00:00.000Z",
          "key": 1548241200000,
          "doc_count": 290
        },
        {
          "key_as_string": "2019-01-23T12:00:00.000Z",
          "key": 1548244800000,
          "doc_count": 268
        },
        {
          "key_as_string": "2019-01-23T13:00:00.000Z",
          "key": 1548248400000,
          "doc_count": 253
        },
        {
          "key_as_string": "2019-01-23T14:00:00.000Z",
          "key": 1548252000000,
          "doc_count": 240
        },
        {
          "key_as_string": "2019-01-23T15:00:00.000Z",
          "key": 1548255600000,
          "doc_count": 216
        },
        {
          "key_as_string": "2019-01-23T16:00:00.000Z",
          "key": 1548259200000,
          "doc_count": 214
        },
        {
          "key_as_string": "2019-01-23T17:00:00.000Z",
          "key": 1548262800000,
          "doc_count": 216
        },
        {
          "key_as_string": "2019-01-23T18:00:00.000Z",
          "key": 1548266400000,
          "doc_count": 229
        },
        {
          "key_as_string": "2019-01-23T19:00:00.000Z",
          "key": 1548270000000,
          "doc_count": 229
        },
        {
          "key_as_string": "2019-01-23T20:00:00.000Z",
          "key": 1548273600000,
          "doc_count": 186
        },
        {
          "key_as_string": "2019-01-23T21:00:00.000Z",
          "key": 1548277200000,
          "doc_count": 131
        },
        {
          "key_as_string": "2019-01-23T22:00:00.000Z",
          "key": 1548280800000,
          "doc_count": 83
        },
        {
          "key_as_string": "2019-01-23T23:00:00.000Z",
          "key": 1548284400000,
          "doc_count": 46
        }
      ]
    },
    "bytes_served": {
      "value": 58785836
    }
  }
}
```

</details>



# 인덱스 수명 주기 관리 (ILM) 

Index Lifecycle Management 

- 각 단계(frozen, cold, warm, hot)마다 데이터 전환으로 수행할 작업을 정의하기 위해 설정한다. 
- 다시 불러오자면, 인덱스는 한 테이블을 의미한다. 

인덱스 특성들
- 부트스트랩 인덱스: 연속적인 데이터 스트림을 색인하고 관리하기 위해 수동으로 초기 생성해야함 (데이터스트림 지원 인덱스는 알아서 함)
- Write Alias : 현재 활성화된 인덱스를 가리키는 역할 
- Index rollover: 새인덱스가 생성되고, Write Alias는 새 인덱스를 가리키게 한다. (로그 롤링이랑 똑같음)
  - 롤오버 하기 위한 조건을 인덱스 크기, 최대 문서수, 최대 인덱스 사용기간에 따라 명시할 수 있다. 

Write Alias

```
PUT ilm-web-logs-000001
{
    "aliases": {
        "ilm-web-logs": {
            "is_write_index": true
        }
    }
}
```

롤오버
```
POST ilm-web-logs/_rollover
```

# 데이터 스트림을 사용해 시계열 데이터 관리

시계열 데이터 소스를 관리할 때 데이터 스트림을 사용해서 단일한/고유한 리소스 이름으로 데이터를 쉽게 작성하고 사용한다. 

데이터 스트림 생성
```
1. ILM 정책 생성
2. 데이터 스트림 활성화된 인덱스 템플릿 생성
3. 데이터 스트림 생성
```

```
PUT /_index_template/logs-datastream
{
    "priority": 200,
    "index_patterns": ["logs-datastream*"],
    "data_stream": {
    },
    "template": {
        "settings": {
            "index.lifecycle.name": "logs-policy"
        }
    }
}
```

구체적인 인덱스 위치를 알필요 없이 검색 등이 가능하다는 장점.

# 인제스트 파이프라인으로 데이터 가공

쿼리할 때 필드 값을 평가하고 싶으면 runtime field - 임시/일회성 변경 사항을 확인할 수 있다. 
  - (해당 로그의 데이터를 이용해 평가식을 써두면 runtime field에 평가 값이 들어가있음.)

```
PUT _ingest/pipeline/logs-add-tag
{
    "description": "Add a static tag for the environment the log originates from",
    "processors": [
      {
        "set": {
          "field": "environment",
          "value": "production"
        }
      }
    ]
}

POST _ingest/pipeline/logs-add-tag/_simulate
{
    "docs": [
        {
            "_source": {
                "host.os": "macOS",
                "source.ip": "10.22.11.89"
            }
        }
    ]
}
```

이렇게하면 

```
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_version": "-3",
        "_id": "_id",
        "_source": {
          "source.ip": "10.22.11.89",
          "environment": "production",
          "host.os": "macOS"
        },
        "_ingest": {
          "timestamp": "2025-10-20T22:35:40.395177716Z"
        }
      }
    }
  ]
}
```

이렇게 _source에 environment가 붙는다. 

#### 인제스트 파이프라인 processor 종류

1. set: 새로운 필드 계산해서 넣기
  - set에서 _index에 대해 value를 지정하면, 해당 index에 저장하게 한다.
2. dissect: 하나의 메세지 필드에서 여러개 추출 `"%{time}" HTTP Monitor %{monitor.name}"`

3. drop: 수집 대상에서 특정 조건 이벤트 제외

4. gsub: 정규표현식으로 변환 

5. mappings를 정의해놓고, enrich_fields 에 해당 mapping의 key값이 올 필드를 적어두면 map으로 커



# 워처로 데이터 변경에 대응하기 

경보 메세지를 주는 방법임

- 특정 값에서 발생하는 단일 이벤트에 대한 경보 (event.severity == 'critical' , disk_free < 1GB)
- 필터 조건과 일치하는 이벤트가 임계치 초과
- 메트릭 집계 값이 특정 임계치 초과

Kibana Alerting이랑 워쳐는다른데, 워쳐는 elastic Search 쪽에 붙어있는거다. 


 
