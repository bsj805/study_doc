# 11. Reranker 

- 후보 문서와 쿼리의 관련성을 평가해서 문서 순위 재조정.
  - 후보 문서는 retriever로 encoding 기반으로 빠르게 유사한걸 가져옴 
  - BERT, RoBERTa 같은 트랜스포머 기반 모델 
  - 대규모 검색시스템을 위한 것이라기 보다는, 소규모

# 11.1 Cross Encoder Reranker

RAG 성능 향상시키려고 한다. 
- reranker 사용시 상위 5~10 개 문서에 대한 리랭킹 수행

