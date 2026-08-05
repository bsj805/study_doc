https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html

## 요약

induction head가 대형 트랜스포머에서 일어나는 in-context learning의 대부분을 담당하는 메커니즘일 수 있다.

## in context learning?

가중치를 전혀 바꾸지 않고, 프롬프트 안에 들어 있는 정보만으로 모델이 그 자리에서 적응하는 현상입니다. 학습(training)은 이미 끝났고 파라미터는 고정되어 있는데, 순전파 한 번 안에서 뭔가를 "배운" 것처럼 행동하는 거죠.

```
sea otter => loutre de mer
peppermint => menthe poivrée
cheese =>
```

프랑스어 번역하라고 명시적이지 않지만, 아무튼 영어->불어 번역 상황인지를 컨텍스트에서 파악한다. 

## induction head?

2 layer model에서 
- 이전까지 들어온 토큰까지의 sequence(A)를보고, A 다음에 온 토큰(B)를 봐서, 같은 completion이 다시 occur할지 예측하는 함수이다.


문제점
- frontier 모델들은 2 layer attention model이 아니라 엄청 많은 레이어가 존재한다. 
- 수학적으로 분해하지말고, empirical 하게 검증하므로써, 무슨일이 일어나는지 추정하자. (신경학자들처럼)


## 실험적 결과로 주장된 내용

### 주장 1  (co-occurrence)

25억토큰~50억 토큰 구간에서, 갑자기 in-context learning 벤치마크 점수가 상승, induction-head 형성관측됨
- 1층 모델은 영원히 안생김. 
- 이 논문에서는 ICL이 일정하다.
- 이후 논문에서는 ICL이 나타났다 사라졌다 하기도 하는것 같다는 말이 나옴


### 주장 2 co-perturbation

아키텍쳐를 바꿔서 induction head 형성 조건을 바꾸면 ICL 상승 시점도 따라 움직인다. 

e.g. 앞 토큰 정보가 담긴 key를 1층 모델에 제공하니까 1층 모델에서도 ICL이 생긴다. 

- 후속 연구에서 transformer를 한 층만 쌓았다면, attention head 수,차원을 '지수적으로' 늘려야하는데, 2층이면 모델 크기의 로그 증가로도 충분하다고 한다. 

### 주장 3 ablation

테스트 시점에 induction head를 제거하면 ICL이 크게 줄어든다. 
- induction head circuit에 관여되지 않은 head를 끄면 (ICL이 설명하는 몫이 커지니까) ICL점수가 올라가고, induction head circuit의 head를 하나라도 끄면 ICL이 거의 다 사라진다. 


>그런데 "대부분"은 뒤집혔습니다. Yin & Steinhardt의 ICML 2025 논문이 결정적입니다. 
12개 언어모델에서 induction head와 function vector(FV) head — 활성값이 ICL 태스크의 잠재 인코딩을 계산하는 head — 를 비교한 결과,
 few-shot ICL 성능은 주로 FV head에 의존하며 특히 큰 모델일수록 그렇습니다. 
 FV head를 끄면 few-shot 정확도가 크게 떨어지는 반면, induction head를 끄는 건 무작위 head를 끄는 것보다 별로 나을 게 없었습니다. 

그럼 ①과 ②는 왜 다른 결론일까요? 교란변수 때문입니다. 
두 head 집합이 서로 상관되어 있는데 선행 ablation 연구들은 이를 통제하지 않았고, 
FV 점수가 낮은 induction head만 골라 ablate하면 효과가 무작위 ablation 수준으로 떨어집니다. 
즉 기존 ablation이 잡아낸 효과의 상당 부분은 "induction head이면서 동시에 FV head인" 것들이 만든 거였습니다. 


### 주장 4 

특정 head가 모든 번역(영프독) 수행할때 작동하는걸 발견했다. 번역에 대한 head가 있는건가? 

- 후속논문에 대해서 밝혀지기를 언어 독립적인 '어휘' 단위에 대한 표현을 담고 있다. 

### 주장 5 

소형 모델에 이 induction head circuit을 그대로 넣으면 ICL이 생기는것. 
- 후속 논문에서 알고보니 FV 점수를 높이는 발판이더라



### fv head

function vector: 지금 시연되고 있는 태스크의 압축된 표현을 하는 head들. 


