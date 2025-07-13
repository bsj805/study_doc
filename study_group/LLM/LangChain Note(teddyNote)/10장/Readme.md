# 다양한 retriever

- 벡터스토어 기반 검색기
- 문맥 압축 검색기
  - basic retriever 로 받아오고 그걸 압축기에 돌려서 핵심만 가지고있게 한다. (문서 전체를 없애던가, 일부만 떼온다던가)
  - LLMChainFilter: 문서 필터링만 할거라면
  - EmbeddingsFilter: LLM은 임베딩할때만 쓰이고 쿼리에 대한 필터링할때에는 임베딩으로만 필터
  - DocumentCompressorPipeline: 여러 compressor를 순차적 결합하는 용도로 사용해.  



## 4. 긴 문맥 재정렬

- 모델이 긴 컨텍스트 중간의 정보에 접근할 때 제공된 문서를 무시하는 경향이 있음.
  - attention 모델 자체에 input으로 긴 문서가 들어가는것도 흔하지 않고, 처음과 끝의 신호가 더 강해지는 특성이 있음. 
- LongContextReorder 클래스를 생성하면, 문서 목록을 재정렬해서, 덜 관련된 문서가 목록의 중간에 있도록 한다. 


## 5. ParentDocumentRetriever

작은 조각의 임베딩은 더 정확하니까, 작은 조각의 임베딩을 먼저 검색한다음, 해당 조각이 포함된 문서(부모 문서)를 가져온다.

## 6. MultiQueryRetriever

하나의 쿼리를 입력하면 LLM으로 여러 query를 생산해낸다

## 7. MultiVectorStoreRetriever

같은 문서를 여러개의 벡터를 생성해서 저장해둔다. 

- 작은 청크 생성
- 요약 임베딩
- 특정 가상 질문을 만들고 이 질문에 기반한 임베딩을 생성해둔다. 
- 수동 추가 방식 ( 특정 질문을 타겟팅 하고 싶을 때 특정 쿼리를 만들어서, 해당 내용에 대응되는 임베딩을 생성 )

