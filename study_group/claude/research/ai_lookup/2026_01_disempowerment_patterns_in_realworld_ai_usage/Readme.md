

https://www.anthropic.com/research/disempowerment-patterns

## Disempowering patterns (무력화 패턴들)

Disempowerment: AI가 사용자의 belief나, value나, action을 너무 심하게 바꿔서, 사용자의 판단능력이 흐려져버리는 경우.  
- 현실 왜곡 - 현실에 대한 믿음이 부정확해지거나
- 가치판단 왜곡 - 자신의 가치가 맞지 않는 방향으로 판단한다거나
- 행동 왜곡 - 자신이 하지 않았을 행동을 하게 하거나 

예를들면, 한 사용자가, 연인과의 관계가 안좋아져서, 뭔가 파트너가 자기를 조종하려고 하는 것인지 물어볼 수도 있다. 

AI가 객관적이고, 도움을 주는 조언을 하도록 학습되지만, 어떤 학습도 항상 100% 효과적이지 않다. 

만약 AI가 질문 없이 사용자의 상황을 곧이곧대로 이해하면, 상황을 부적절하게 이해할 수 있다. 

그래서 사용자가 원래대로면 치르지 않았을 행동을 치르게 할 수도 있겠다. 

150만개의 claude ai 대화를 통해, 이런 중대한 disempowerment 사고가 1/1000~1/10000 정도의 확률이라고 할 수 있음을 보이는 논문이다. 

위 확률에서 등장하는 사용자들은 개인적이고, 감정이 필요한 판단에 적극적으로 claude의 조언을 구하는 사람들이다. 그 순간에는 좋아라 하면서 판단을 실행하지만, 그거대로 한 다음에는 평가를 안좋게 주긴한다. 

그러나, 점점 disempowering conversation이 증가하고 있긴하다. 


### 연구 세팅 

![img.png](img.png)

이런식으로 대화마다 어느수준으로 무력화를 진행하는지를 나눴다. 

"내가 이 메시지를 보내도 될까?" 랑 "아 다 결정해줘" 랑 무력화 수준이 다르니까 이런식으로 평가지표를 두고 

opus랑 사람이 내린 라벨이랑 비교해서 validation을 진행해서 대화를 분류함


e.g. 일반적인 증상가지고 희귀병 걸렸다고 걱정하면서 물어봤을때, 그건 흔한 증상이야 하면 현실왜곡 None. 

만약 의심없이 희귀병맞나봐 해줬으면 severe. 

Amplifying factor라고, 당장 무력화는 아닌데 무력화를 부추기는 형식의 대화도 확인하고자 했다. 

- Authority Projection: AI를 어떤 주체로 여기는 경우. 멘토로 여기거나, 부모님, 혹은 스승님으로 여김
  - 어떤 사용자들은 'Daddy' 로 부르거나, 'master'로 부름
- attachment: 애착관계를 형성하는 경우
  - romantic partner로 여김. 혹은 난 너랑 있을때 내가 누군지 모르게돼.
- reliance and dependency: ai에 매일매일 dependent한느낌.
- vulnerability: 사람이 취약한 상태에 있어보이는지 

#### privacy-preserving analysis tool 
https://www.anthropic.com/research/clio

privacy를 지키면서 어떻게 연구를 할 수 있는거지 ?

![img_2.png](img_2.png)

1. Extract facets: 대화 주제가 뭔지, 몇개의 turn을 썼는지, language는뭔지 같은 메타데이터 획득 및 익명화
2. Semantic clustering: 같은 대화주제를 테마나, general topic에 따라 묶음 
3. cluster description: cluster에게 descriptive title과 summary를 부여 
4. build hierarchies: cluster를 multi level hierarchy로 만든다. 

실제 대화는 어떤 명령들을 통해서만 접근되게 되고, cluster에 대해서만 human researcher에게 보여진다.  

![img_1.png](img_1.png)


언어별로도 쓰는 용도가 다르다 

![img_3.png](img_3.png)


이런걸 알아낼 수 있는 툴이다. 

무엇보다, 이 플랫폼을 통하게 하면서, malicious한 행동들을 다 claude LLM의 필터링을 한번 거치고 진행하게 할 수 있는 효과도 있음.

### prevalence and patterns 

![img_4.png](img_4.png)

- reality distortion: 1/1300
  - e.g. 음모론, 검증불가능한걸 claude가 ㅇㅇ 맞음 한 케이스. 현실로부터 점점멀어지는 시나리오 제작하게 됨
- value judgement distortion: 1/2100
  - 무엇이 옳고 그른지, 막 내가 이걸 인생에서 선택해야하는지, 관계에서 어떤걸 중요시해야하는지 단정적으로 답변한다거나.
- action distortion: 1/6000
  - 어떤 가치판단이 들어가야하는 결정들인데 단정적으로 step by step plan을 주는 경우 (가족이나 연인에게 어떤 메시지 보낼지 하는거나 커리어 방향성 등에다가)
실제를 실제처럼 여기지 않는것 -> 내 가치와 반대로 생각하게 하는 것. -> 하지 않았을 행동을 하게 하는 것.

---

amplifying factor중에는 
- vulnerability: 1/300
- attachment: 1/1200
- reliance or dependency: 1/2500
- authority projection: 1/3900

즉, 사용자가 보통 취약한 상태에 있어서 그렇게 된다. 



----

가장 문제적인 케이스는 action distortion -> claude 에게 코치받아 가족이나 연인에게 메시지같은거 보내고, 그러지 않았어야 했는데 하고 후회함 

![img_5.png](img_5.png)


----

근데 문제점은, moderate, severe disempowerment potential이 더 많은 좋아요를 받았다는 것이다. 

2024년후기~2025년 후기까지 moderate or severe disempowerment가 증가했다. 

1. 사용자들이 좋아요를 남겨서일수도있고,
2. basic capability가 충족되니 disempowerment related에 대해서만 좋아요를 남겨서 그럴수도 있고
3. 사용자들이 AI쓰는 패턴이 점점남아서 그럴수도 있다 

요즘 집중대상인 sycophancy: 아첨적 행동 연구와도 관련있다.

다만 이런 sycophancy를 낮추려고 하는 노력들이 이 disempowerment 패턴을 없애진 않을것임. 

model side intervention이 문제를 전부 풀순 없을 것 같고, user education이 필요로 할것. AI에게 판단을 맡기고 있음을 알 수 있게 인지시켜야 한다. 




