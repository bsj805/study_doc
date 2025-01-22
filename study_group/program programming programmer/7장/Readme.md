# 72의 법칙

y년 동안 매년 a% 증가한다면

y*a=72가 될 때 초기값이 약 두 배 가량 증가해 있다.

# Little의 법칙

시스템을 떠나는 평균비율 * 시스템에 머무는 시간 == 객체의 개수

클럽대기줄 떠나는 비율은 x명/1h * 3h = 60명 (클럽의 정원)

# 연습문제

## 1. mississippi강

Bell 연구소가 Mississippi 강으로부터 1천마일 떨어져있지만, Passaic 강은 단지 몇 마일 떨어져있다.

1992년 6월 10일, 일주일동안 폭우가 내린 후, Star-Ledger는 "그 강은 평균보다 5배나 빠른, 시간당 200마일의 속도로 흘러내려갔다" 고 한 엔지니어의 말을 인용했다.

이에대한 의견을 말해보라.


<details>

passaic 강의 흐름속도를 이용해 mississippi강의 유역속도가 200마일 / 1h 만큼 빨라졌음을 이야기하고 싶었던 것으로 보인다.

over estimate 해야 하는 요소들: (속도가 더 빨라질 것)

- mississippi강으로 흘러들어오는 모든 지류의 물양이 5배가 빨라졌음

under estimate 해야 하는 요소들: (속도가 더 느려질 것)

- mississippi강의 높이가 높아지면서, 동일시간에 더 많은 양의 물이 흘러야만 동일 속도를 유지할 수 있다.

over-estimate , under-estimate이 어느정도 상쇄되는 부분이 있어 시간당 200마일의 속도로 흘러간다는 예측이 맞게되지 않을까?

해답:

- 80피트의 비가 내린다고 해도, Passaic 강이 한 시간에 200mile을 절대 흘러갈 수 없다. 나는 그 엔지니어가 실제로는 불어난 그 강이 하루에 200마일을 흐른다고 말하려고 했던 것이
  아닌가 의심스럽다.

이는 평상시의 속도인 하루에 50마일 (50마일/day), 즉 시간당 2마일보다 5배 빠른 것

</details>

## 2. 달리기

어느정도의 거리라면 고속 데이터 전선으로 정보를 전달하는 것보다 배달원이 자전거를 타고 이동성 미디어를 운반하는 것이 더 빠르겠는가?

<details>

간단히 계산해보자. 요즘은 1Gb/s 인터넷을 사용한다. 1기가비트를 1초에 보낼 수 있다. 광케이블을 사용한다고 하면 1초에 30만킬로미터를 갈 수 있다.

즉, 1기가비트를 1초에 30만킬로미터까지 보낼 수 있다. 1초에 1킬로미터거리에 (1/30만)기가비트를 보낼 수 있게 된다. 1초에 0.0035킬로미터 거리에 (0.000000011666667)
기가비트를 보낼 수 있게 된다.

자전거는 13km/h 정도의 속도를 낼것이다. == 0.21km/m == 0.0035km/s 의 속도로 보낼 수 있다.

0.0035거리에서 초당 1.4mb 보다 많이 운반할 때에 자전거를 타는게 더 빠르다.


</details>

## 3. 타이핑으로 플로피 디스크 한 장을 채우는데 얼마나 오래걸릴까?

<details>

64MB 디스크라면, unicode는 2byte

32*10^6 글자를 타이핑해야한다. 프로그래머라면 필수로 분당 1000타정도 나올테니까, 32*10^3분이 필요하다. 32000분 == 22일


</details>

## 4. 세상이 지금보다 백만 배 느려진다고 생각해보라.

여러분의 컴퓨터가 명령을 하나 수행하는데 얼마나 오래 걸리겠는가? 1,000,000 10^6이구나

디스크가 한 바퀴 도는 데는?

디스크 암이 디스크를 가로지르는 데는 ?

여러분의 이름을 타이핑하는데는 얼마나 걸리겠는가?


<details>


Q1. CPU 명령어 처리 속도는 14gen intel cpu 기준으로 6.2Ghz

```
1. Frequency (Clock Speed)
   Measured in gigahertz (GHz), it indicates how many clock cycles the CPU can execute per second.
   In this case, 6.2 GHz means the CPU executes 6.2 billion clock cycles per second.
2. Instructions Per Clock (IPC)
   A CPU doesn't execute one instruction per clock cycle. Modern CPUs are capable of executing multiple instructions in a single clock cycle, depending on their architecture and efficiency.
   For example, if a CPU can process 4 instructions per clock cycle, then at 6.2 GHz, it could potentially execute 4 × 6.2 billion = 24.8 billion instructions per second. 
   However, this depends on the workload and how efficiently the CPU can use its resources.
```

그러니까, clock이 6.2 billion clock이 1초마다 도는거고,

![img.png](img.png)

integer addition은 clock이 1씩 사용되니까, integer addition이 내 명령이라고 했을 때 6200 clock per second, 여전히 1초마다 처리될 수 있다.6200
clock이나 돌릴 수 있다.

Q2. 요즘 흔한 하드디스크는 7200RPM 이고, 10,000 RPM까지 존재한다고 한다.

1/100 RPM이 되니까 디스크 한바퀴 도는데 100분이 걸린다.

Q3 디스크 암 스피드는 가장 안쪽에서 가장 바깥쪽까지 15ms 걸린다고 한다. 10^-3*10^6 ==15000초가 걸린다.

Q4 우리 이름 타이핑하는데에도, 1000타/분 10^-3타 /분 1타를 치는데 1000분씩 걸리니까, 3000분이 걸리겠다. (영어이름이 아닌것에 감사)

의도는 인건데, 영리한 독자는 시계도 같이 느려지니까 소요되는 시간이 변함없다 ^&^

</details>

# 5. 9를 버리는 기법이 덧셈 테스트 어떻게 하는가? 72의 법칙은 어떻게 증명?

72의 법칙이 5%~10% 에 대해서는 오차범위 1%내에서 정확하다

# 6. UN은 1998년 인구가 59억, 인구 증가율이 1.33%

x * 1.33 = 72가될 때 59*2

54년 뒤.

72/1.33은 약 54이므로 2052년에 인구가 2배가 될 것.

# 7. [부록3] 시스템의 시간 및 공간 비용 모델을 생성

[부록3]은 여러분의 시스템에 대한 시간 및 공간 비용에 대한 모델을 생성하는 프로그램을 설명한다. 이 모델에 대해 읽은 다음, 여러분의 시스템에 대한 비용을 추정하여 기록해보라

이 책의 웹사이트에서 프로그램을 다운로드하여 시스템에서 실행시켜보고 결과를 여러분의 추정이랑 비교해보라 .



<details>


나눗셈은 일반 연산의 5배

제곱근은 나눗셈에 비해 두배 정도

(sin)삼각함수는 제곱근의 두배

복잡한 삼각함수는 (sinh) 3배~6배까지 올라간다.

</details>

# 8.

# 9.

하나의 트랜잭션 위해서 디스크에 100번 접근한다고 가정하자

한시간동안 얼마나 많은 트랜잭션 처리 가능한가?

<details>

디스크 access가 10ns 든다고 하면 100번접근할 때 10^-5 *10^2 == 10^-3 second.

1초에 1000개 처리가능하다.

</details>

# 10. 여러분이 사는 도시의 연간 사망률이 전체 인구의 몇%가 되는지 추정하라.

<details>

우리 도시가 10만명 정도 사는 것 같다.

0.5%정도 죽지 않을까?

10^5 * 10^-4*5 = 50명정도 죽을 것.

50명 / 5*10^8 = 1/10^7 의 사망률. %로 전환하면, 1/10^5 % = 0.00001%

</details>

# 11. little 법칙에 대한 증명을 스케치 해보라 .

<details>

어떻게 하는거지.

머무는 시간 * 들어가는 비율 = 총 개수다.



</details>

# 12.

미국 25센트 동전 평균 수명이 30년이다. 확인 방법은?

<details>

방구석에서 확인하는 방법은 없는것 같고, 수거되는 동전의 비율?

하루에 거래되는 동전의 비율 * x = 시중에 풀린 동전의 전체 수량

이것도 little의 법칙이었구나.

</details>