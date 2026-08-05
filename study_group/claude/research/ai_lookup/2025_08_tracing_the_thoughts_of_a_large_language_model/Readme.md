# AI는 어떻게 생각할까? 

2025년 3월

https://www.anthropic.com/research/tracing-thoughts-language-model

## 왜 수학 계산하는데 맨날 문제가 있었을까?

물론 계산기 역할로 만들어진건 아니라 text보고 훈련해서 그런거긴 한데, 가끔 정답도 내보낸다. 

1. rough approximation 하는 path (88에서 97쯤 사이인거같다)
2. last digit을 결정하는 path 

2개를 조합해서 95라는 정답을 낸다. 

![img.png](img.png)

근데 와중에 36+59 어떻게 풀었어 설명하라고 하면 (6+9=15 1의 자리수 덧셈하고, 3+5+1=9 2의 자리수 덧셈했다)

막 이렇게 한다. 설명하는 방법은 학습되어있기 때문이다. 

## claude의 설명이 항상 faithful한가? 

Claude 3.7 Sonnet 

답이 이미 있는 정답의 경우는 그냥 해당 답이 나올것이라고 유추하고 문제를 푸는 경향이 있음

![img_1.png](img_1.png)

AI system auditing을 통해서, reward model에 appeasing bias 가 있었음을 알 수 있었다.

그래서, 이런 methods로 thought process를 밝혀낼 수 있을것이라고 믿는다. 

이래서 요즘에 답을 확신하는것처럼 물어봐도 실제 정답을 잘 내주는것 같다. 

## anti-hallucination은 어떻게 시켰을까? 

LLM training 할때는 모델이 다음 word를 추론하도록 incentivize하기 때문에, 그렇게 훈련된게 당연한 것. 

이때의 anti-hallucination training을 시켰더니 모르는걸 모른다고 하도록 했는데, 이게 어떻게 작동하는걸까? 

refusal to answer이 default behavior이다. 근데 잘 아는 분야가 나오면 이 refuse default circuit이 억제된다. 

그래서 known answer feature을 작동시키면 모르는 정답도 뱉게 할 수 있다. 

근데 가끔 hallucination나는건, 이름 자체는 인식했는데 관련된 아무 정보도 없을때 known answer feature가 켜지게 되어있어서 그렇다. 

## 이런건 어떻게 리서치한걸까? 

LLM 내부를 뉴런 단위로 이해하고 싶은데, 뉴런은 polysemantic 즉 저장해야할 개념이 많아서, 개념이 여러 뉴런에 번져서 저장되는 superposition(중첩) 현상 때문이다.

관건은 해석 가능한 feautre 단위로 분해할 도구가 필요 한것. Cross-Layer Transcoder로 교체해서, 특정 feature가 활성화되는걸 볼 수 있도록 한다. 

MLP를 희소 feature 사전으로 교체 → 비선형성을 얼려서 feature 간 상호작용을 선형화 → 특정 프롬프트에서 선형 기여도 그래프를 그림 → pruning과 그룹핑으로 사람이 읽게 만듦 → 개입 실험으로 검증

https://transformer-circuits.pub/2025/attribution-graphs/methods.html


# 