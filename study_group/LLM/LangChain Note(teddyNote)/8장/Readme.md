# vllm 으로 langchain embedding 사용하기

```
from langchain_openai import OpenAIEmbeddings
embedding_model = OpenAIEmbeddings(
    openai_api_base=os.environ.get("OPENAI_API_BASE"),  # OpenAI API URL
    model=os.environ.get("OPENAI_API_EMBEDDING_MODEL"),  # 임베딩 모델명
)
# 질의내용
text = "대한민국의 수도는 서울이고, 정자동이 서울이랑 가까워요"

embedding_result = embedding_model.embed_query(text)

```

llm에서는 파라미터가 model_name이더니 model로 바뀌었다.

원 문장과, 각 5개 문장을 비교시켰는데, 정자동과, 영등포가 높게 나오는걸 보면,

영등포가 서울에 있다는 것도 반영이 되는 듯하다.

qwen/qwen3-embedding-8b 사용결과다.

```
대한민국의 수도는 서울이고, 정자동이 서울이랑 가까워요
유사도: 0.4221 - 문장: 정자동의 집값이 많이 오르겠습니다
유사도: 0.4171 - 문장: 영등포의 집값이 많이 오르겠습니다
유사도: 0.4054 - 문장: 군포시의 집값이 많이 오르겠습니다
유사도: 0.3881 - 문장: 인계동의 집값이 많이 오르겠습니다
유사도: 0.3844 - 문장: 수영구의 집값이 많이 오르겠습니다

```



