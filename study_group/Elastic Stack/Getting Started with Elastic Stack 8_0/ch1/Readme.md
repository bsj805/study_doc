# 1. 핵심 컴포넌트 소개

## 1.1 엘라스틱 서치

- 색인
- 텍스트 검색
- 집계

### 엘라스틱 서치 특징 

- 수평적 확장성 (horizontal scalability)
  - 읽기 쓰기 처리량, 저장 용량을 선형으로 증가시키기. 

- 고가용성
- 스냅샷 복원 
- 클러스터간 검색도 가능 
  - 네이버 통합검색도 이런느낌일것 같음.


## 1.2 키바나 

엘라스틱 서치의 데이터를 위한 시각화 도구 

엘라스틱 서치의 데이터를 탐색하고 사용하게 도와주는건 인제스트 (ingest)

Elastic사가 라이선스를 바꾸면서, AWS가 중심이 되어 Elasticsearch 7.10 버전을 포크해서 OpenSearch라는 오픈소스 프로젝트를 만들었습니다.

그리고 Kibana도 7.10 시점에서 포크해서, 이름을 OpenSearch Dashboards라고 바꿨습니다.

Opensearch Dashboard에서 검색을 하면 DQL로 바뀌어서 Opensearch로 검색이 된다. 

## 1.3 인제스트

비츠를 활용해 환경 전반에서 데이터 수집하기 

- Filebeat: log data
- Metricbeat: 메트릭 데이터 

Libbeat라는 오픈소스 라이브러리로 범용 API 제공 (입력 데이터와 출력 데이터의 목적지 구성하기 위함)

통합 데이터모델 (Unified Data Model: UDM)을 준수하게 한다.

로그스태시같은 ETL(Extract Transform Load) 도구로 데이터 필드명을 변환하고 이름을 변경한다. 또는 어플 자체에서 UDM에 맞게 로그를 출력하게 한다. 

ECS는 엘라스틱 공통 스키마 - 대시보드, 시각화, 머신러닝 작업, alert 같은 컨텐츠를 활용할 수 있다. 


