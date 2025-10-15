# 데이터 색인과 검색

인덱스 작동 방식

데이터를 적정한 데이터 유형에 매핑하는 방법

엘라스틱서치에서 데이터를 쿼리하는 방법 



```

# Create an index
PUT /my-index


# Add a document to my-index
POST /my-index/_doc
{
    "id": "park_rocky-mountain",
    "title": "Rocky Mountain",
    "description": "Bisected north to south by the Continental Divide, this portion of the Rockies has ecosystems varying from over 150 riparian lakes to montane and subalpine forests to treeless alpine tundra."
}


# Perform a search in my-index
GET /my-index/_search?q="rocky mountain"
```

GET _cluster/health 를 하니

```
{
  "cluster_name": "docker-cluster",
  "status": "green",
  "timed_out": false,
  "number_of_nodes": 1,
  "number_of_data_nodes": 1,
  "active_primary_shards": 39,
  "active_shards": 39,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 0,
  "unassigned_primary_shards": 0,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 100
}
```

### 인덱스란?

인덱스가 일반 RDB에서 여러 테이블을 포함하는 데이터베이스 개념

인덱스 하나가 여러 개의 프라이머리 샤드(Read&Write)로 구성된다.

각 샤드 하나하나가 색인 및 검색 요청을 처리할 수 있는 루씬인덱스 인스턴스.

#### 색인(indexing)

문서를 엘라스틱서치 인덱스에 기록한다.

`GET _cat/indices` 하면

```
yellow open my-index
```

라고뜨는데, 아마 아무 문서도 없어서 그럴것.

인덱스에 저장되는 문서는 JSON 객체. JSON하나가 하나의 row. 

문서는 색인되면 _source 필드에 저장되고, _index필드와, _id 필드가 문서에 추가된다.

ex.) PUT my-index/_doc/2
```
{
    "year" : 2021,
    "city" : "Sydney",
    "country": "Australia",
    "population_M": 5.23
}
```


```
      {
        "_index": "my-index",
        "_id": "2",
        "_score": 1,
        "_source": {
          "year": 2021,
          "city": "Sydney",
          "country": "Australia",
          "population_M": 5.23
        }
      }
```

여기서 POST my-index/_doc/ 과 같이 날리면 id가 자동생성된다.

### 인덱스 매핑

문서의 모든 필드가 엘라스틱서치의 데이터 유형에 매핑되야 한다. 

검색을 위해 필드를 색인하고 분석하는 방법을 결정한다.

인덱스 매핑을 동적으로 생성할 수도 있다.

인덱스 매핑 생성후에는 그 타입에 맞지않는 필드값을 넣으려는 색인요청은 실패할수 있다.

객체형식도 indexing이 된다. 

properties로 나타낸다. 

```
POST my-index/_doc
{
    "year" : 2022,
    "city" : "Seoul",
    "country": "Korea",
    "population_M": 0.395,
    "customValue": {
        "key": "value"
    }

}
```

하니까 index는

```
"customValue": {
  "properties": {
    "key": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    }
  }
```

customvalue.key 에 대해서 index 매핑을 지정하는 방식이다.

### index template 
인덱스 설정 및 매핑을 위한 blueprint를 미리 작성해두는 것. 

데이터 소스를 여러 인덱스에 분산하는게 일반적이라서 그렇다. (12월 10일에 나온 로그가 한 인덱스, 12월 11일에 나온 로그가 한 인덱스)

로그스태시같은 ETL 클라이언트로 이벤트 날짜 기반 인덱스 자동생성이 가능하다. 

`GET _index_template/*` 하면 index template 목록 볼 수 있다.

index template 없이도 logstash에서 

```
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "project-abc-%{+YYYY.MM.dd}"  # 날짜별 인덱스 생성
  }
```

이런식으로 지정해두면, 날짜별로 project-abc-2025.01.12 같이 생성된다. 

다만 이때는 동적으로 첫번째 문서를 보고 데이터 타입을 추론한다는게 다를 뿐이다. 

### 노드 종류 

데이터 노드 - 데이터 담는곳 (hot, warm, cold) 

인제스트 노드 - 색인하고 데이터 노드에 저장하기 전에 변환하는 프로세서 

코디네이터 노드 - (모든 노드가 이거 지원) 검색 색인요청을 적절한 데이터 노드로 전달하기 및 검색결과 반환




