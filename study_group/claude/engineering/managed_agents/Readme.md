> 원문: https://www.anthropic.com/engineering/managed-agents

기존의 흐름 

Claude(모델) -> tool call 출력 -> harness가 그 tool call을 받아서 실제 인프라로 라우팅 -> 컨테이너에서 실행 -> 결과 문자열을 다시 Claude context로 반환 

harness: claude 호출하고 claude의 tool call을 관련 인프라로 라우팅하는 루프이다. 


## harness


Claude Sonnet 4.5 would wrap up tasks prematurely as it sensed its context limit approaching

라는 context anxiety 현상 발견. 이래서 harness를 둬서, context reset을 하게 했다. 

그런데 Opus4.5에서는 그런 행동이 없어져서, 그냥 harness 없애버렸다. 

harness가 계속 바뀌니까, evolve하기를 바란다. 

Managed Agents:a hosted service in the Claude Platform that runs long-horizon agents on your behalf through a small set of interfaces meant to outlast any particular implementation


OS는 file, process 처럼 hardware를 virtualize해서, 아직 존재하지 않는 system이 들어올 공간을 남겨뒀다. 

read() 커맨드만 실행하면 1970년의 disk나 ssd를 읽을 수 있게 해뒀다. 

managed agent도 이런 abstraction을 하고 싶은거다 

agent의 component를 session(append only log of what happened) , harness (the loop that calls Claude and routes Claude's tool calls to the relevant architecture),

and a sandbox(execution environment)

각각은 다른 이들에 대한 침해없이 swap 될 수 있다. 





---

### Don't adopt a pet

- 모든 agnet component를 single container로 밀어넣었다.
  - 근데 이러면 pet vs cattle anaology에서 pet을 adopt 한셈이 된다.
    - pet은 아주 고정된 객체이고, cattle은 언제든지 바꿀 수 있는것. 
    - pet을 입양 한 셈. 
      - container가 fail하면 session이 lost. 
      - container가 unresponsive하면 다시 살려야해. 
        - unresponsive한 session을 debug해야 한다. 너무 디버깅이 어렵다. (shell을 컨테이너에다 띄우면 되지만, user 정보에 엑세스가 가능한 shell을 띄우는건 우리가 디버깅 능력 없음을 실토하는 셈)
    - 또한, 이렇게 하니까 harness가 claude가 무조건 container 안에만 영향을 준다고 추정했다. (막 private cloud 접속해서 그거 수정하게 하기도 하는데.)

### Decouple the brain from the hands 

아래 두개로 나누자. Decoupling이 된 것.  
- 'brain' : Claude와 harness
- 'hand' : sandboxes와 tools (action할 tool들), session 

#### harness가 container 바깥으로 

harness가 container 바깥으로 빠지게 하고, 다른 tool calling처럼 container를 호출했다. 

container는 cattle처럼 언제든 죽어도, tool call error인 셈으로 여기고 claude에게 돌려놓는다. 

claude가 retry 결정하면, 새 container는 provision({resources}) 라는 표준 recipe(init 스크립트) 따라서 생성되고, 기존 container를 살리려고 노력하지 않아도 돼.


#### harness failure에서 복구하기 

session log가 harness 바깥에 있으니, 그냥 harness 있는 컨테이너 crash나도, log기반으로 reboot 시켜도된다.

- `wake(sessionId)`
  - container reboot
- `getSession(id)`
  - event log 다시 붙여넣기 
- agent 실행하면서 harness는 session에 `emitEvent(id, event)` 로 로그남김 


#### 또다른 좋은점 - security boundary

coupled design에서는 claude가 같은 container에 credentials을 갖고 실행되었기 때문에, prompt injection은 claude가 그 key를 읽어오게 하기만 하면 되었다. 

이때 "narrow scoping"이라는 대응책은 예를 들어:
- 토큰에 repo 전체 write 권한 대신 특정 repo read-only 권한만 부여
- 새 세션을 생성할 수 없는 토큰 발급
- 만료 시간이 짧은 토큰 사용

이런 대응만 할 수 있었다. 

Claude가 generate 한 코드를 실행시켰을때 sandbox에서 token이 never reachable 하게 하는 구조적 변경이 필요하다고 생각했다. 

git 같은건 credential이 필요하긴 한데, sandbox 초기화할때 sandbox환경에 박아두면 claude한테 아무리 닦달해도 git pull같은건 되지만 claude가 credential을 읽어올 순 없다. 

MCP같은 경우에도 proxy를 둬서 proxy가 갖고있게 하고, claude 자체는 모르게 


### session이 claude의 context window가 아님

long-horizon task는 claude context window 넘을 때가 있음. 

- compaction ? memory tool(file에 context 저장) ? contex trimming (old tool results, thinking blocks 제거)
  - 미래에 필요한 토큰을 지워버리면 어떡하지? context를 context window 바깥의 object로 저장해두자. 


Managed agents 에서는 context가 session log에 남아서 저장된다. harness가 계속 적도록 해. 

그리고 session에서 retrieve 할때도 harness가 자유자재로 변형해서 context에 넣을 수 있게 해.

## 결과

이제 container는 고객 on-premise 에서, 명령만 Anthropic cloud에서 하는 구조가 가능해졌다. 

또 anthropic cloud에서 container를 coupled system으로 제공하면, 추론을 시작하기도 전에 컨테이너 프로비저닝 비용을 선불로 냈다. 

brains can pass hands to one another

한 claude가 하던거 다른 claude로 넘길수도있고, hand도 여러개 사용가능. 














