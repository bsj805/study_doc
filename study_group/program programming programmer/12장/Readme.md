# 표본 선정 문제 프로그래밍 프로세스 원리

1. 발견된 문제를 이해하라
2. 추상적인 문제를 구체화해라. 
3. 디자인 공간을 탐구하라
   -  100개중 99개의 랜덤한 숫자를 뽑아야 한다면 거꾸로 1개의 랜덤한 숫자를 제외시키는게 낫다
4. 한 솔루션을 구현하라 
   -  직관적인 코드를 구현해서 더 나은코드로 나아가자. 


# 연습문제 

# 1. 
rand함수가 15개의 랜덤 비트를 리턴 -> 30개의 랜덤 비트를 리턴하게해라

2번사용하고 concat? 

# 2.

12.1절에서는 m개의 요소를 가지는 부분집합들이 모두 같은 확률로 선택되야 한다고 정했는데, 이는 각 정수를 m/n의 확률로 선택하는 것보다 더 어려운 조건이다. 

각 요소는 같은 확률로 선택하지만, 어떤 부분집합을 다른 부분집합보다 더 높은 확률로 선택하는 알고리즘을 설명하라. 


<details>

m개를 고르고 싶고, n개의 요소가 있는 배열이 주어진다. 

각 요소가 같은 확률로 선택되야 한다면, n이나 m을 줄여나가지 않고, 각 요소를 m/n의 확률로 선택하면 된다.

다만, 이렇게 선택하면 m개를 넘을 수도 있으니까, 제외시키는 로직이 추가되야 한다. 

이 상태에서 앞에서부터 m개를 고르면 같은 확률로 선택했다고 볼 수 있나? 그렇진 않을거같은데 (앞에있는 요소가 더 높은 확률로 골라지니까 사실상 m/n * m/(뽑힌 C개))


### 연습문제 해답

0에서 n-1까지 m개의 정수를 선택하려면, 범위에서 i를 랜덤하게 고르고 (그러면 C개가 뽑히는데,) 특정 랜덤 정수 i를 골라서 i번째부터 m개를 고르면 된다. (최대범위 넘으면 0부터)

그러면 각 정수가 모두 m/n 확률로 선택된 셈이지만, 특정 부분집합이 더 많이 선택될 것이다.(이를테면 m이 크다면 항상 0번째랑 가까운게 더 많이 선택될 것이다.) 


</details>


# 5. 

이 칼럼에서는 한 가지 문제에 대한 여러 개의 솔루션을 설명했다. 각 프로그램의 퍼포먼스를 측정하고, 실행시간, 메모리 등을 고려할 때 각 솔루션이 언제 적당할지를 설명하라 

문제: 정렬된 m개를 랜덤하게 골라달라

1번: m개 고르기 위해서 remaining_select/remaining_elements 의 확률로 골라서 차례대로 배열에 넣기
  - 특징: input제외하고, 메모리가 O(m) 필요, O(n) 시간 걸림. 따라서 n이 커지면 느려질 것이다. 

2번: set에 1/n 확률로 선택해서 m개를 넣는다. 
  - 특징: Set operation 특성상 O(log m)이 삽입시간. 정렬해서 출력하는게 O(m). 따라서 O(mlogm) 시간 걸린다.
  - 메모리를 많이 먹는다고 한다. 해시테이블 등도 유지해야해서 그런듯 하다.? 

3번: 배열의 m번째 index까지 random한 index와 swap시킨다. 그런다음 0번째부터 m번째 index까지 정렬을 실행시킨다.
  - 특징: O(m) 메모리 필요, O(m) 시간 걸린다. m이 커지면 O(n)에 가까워지지만, O(max(m,n-m)) 100개중 99개 뽑아야 하는 경우 1개 뽑는걸로해서 조금 단축시킬 수 있다.

 
C++ set이 메모리를 더 많이 먹는이유?

<details>

 std::set이 메모리를 많이 먹는 이유

노드 기반 데이터 구조
  - std::set은 각 원소를 노드(Node) 단위로 저장하며, 각 노드는 추가적인 메타데이터(부가 정보)를 포함합니다.
  - 예를 들어, Red-Black Tree를 사용하면 색상 정보(1bit) 와 포인터(좌, 우, 부모 노드용 3개) 를 추가로 저장해야 합니다.
  - 즉, set<int>을 사용할 경우, int 하나만 저장하는 것이 아니라 추가적인 포인터 3개 + 색상 정보 등이 포함된 구조체(Node) 를 저장하는 방식입니다.

동적 할당 (Heap 메모리 사용)
  - std::set은 원소를 동적으로 할당하며, 각 원소가 힙(heap) 메모리에 개별적으로 저장됩니다.
  - 동적 할당 시에는 할당 오버헤드(extra metadata)도 추가되므로, 연속적인 메모리를 사용하는 vector보다 비효율적입니다.

포인터로 인한 캐시 비효율성
  - std::vector는 내부적으로 연속적인 메모리 블록을 사용하므로, CPU 캐시 친화적인 구조입니다.
  - 반면, std::set은 노드들이 서로 흩어져 있는 포인터 기반 구조이므로, 캐시 효율성이 떨어지고 더 많은 메모리를 요구합니다.

🔹 대안: std::unordered_set
만약 정렬이 필요하지 않고, 단순히 중복을 허용하지 않는 컨테이너가 필요하다면,
👉 std::unordered_set (해시 기반 컨테이너) 를 사용하면 메모리 사용량을 줄일 수도 있습니다.
단, std::unordered_set은 내부적으로 해시 테이블을 사용하므로, 해시 충돌이 많아지면 메모리 사용량이 증가할 수도 있습니다.

</details>



# 8

0부터 n-1에서 m개의 정수를 랜덤하게 선택해서 출력하는 프로그램을 어떻게 만들 수 있겠는가? (정수의 출력도 랜덤해야 한다)

리스트에서 정수의 중복이 허용된다면, 정렬된 리스트를 어떻게 생성할 수 있겠는가? 

또, 중복도 허용되고, 랜덤한 순서로 출력해야 한다면 어떻겠는가? 

<details>

1. m개의 정수를 랜덤하게 선택해서 출력한다면 m번째 index까지 무작위 index와 swap시켜서 그걸 m번째까지 출력할것. 

2. 리스트에서 정수의 중복이 허용된다면, 정렬된 리스트는 1/n 확률로 선택해서 list에 넣어서 차례대로 출력하면될 것.

3. 중복도 허용되고, 랜덤한 순서로 출력해야 한다면?  1/n 확률로 m번째 index까지 swap하고 m번째 index까지 출력한다? 이건 뜻을 잘 모르겠다. 


### 연습문제 해답

1. stdin으로 받을 때, 파일에서 읽어올 때 그냥 m개까지 출력해라. 

2. 중복이 허용된다면 set가 아니라 그냥 list에 넣어서 정렬해서 출력하면 된다 

3. 중복 허용, 랜덤 순서 출력하려면 가장 간단한 함수가 된다. 

```python

for i in range(0,m):
    print(random.randint(0,n-1))

```

# 11. 

한 광고용 게임에 16개의 점이 그려진 카드가 있고, 각 점에는 1 ... 16까지의 숫자가 적혀있다. 

게임 참가자는 스크래치를 긁어서 이 숫자를 드러나게 할건데, 만약 3이 나타나면 게임에서 지고 그 전에 1,2가 모두 나타나면 이긴다. (순서 상관 없이)

일련의 점을 선택했을 때 게임에서 이길 확률을 계산하기 위해 우리가 취할 단계를 설명하라

<details>

일단 가장 trivial 한 솔루션

1. 1에서 시작할때, 2에서 시작할때, 그리고 1,2가 아닌 특정 숫자에서 시작할때의 확률을 쭉 계산시킨다. 1에서 시작할땐 1/15 * 1/14 * 1/13 * ... 이런식으로 계산할 수 있을 것이다.

그럼 첫 카드를 고름에 따라서 게임의 확률이 테이블로 설정될거고, 각 카드를 고를 확률은 1/16 이므로, 이를 곱하면 될 것이다.


### 연습문제 해답 

어차피 다른 숫자들은 확률에 아무 상관도 없고, 그냥 한 라운드 스킵한거나 마찬가지다

1,2,3 의 순서 문제이다 

경우의 수 목록

```
1, 2, 3 
1, 3, 2
2, 1, 3
2, 3, 1
3, 1, 2
3, 2, 1
```

이렇게 6가지 경우의 수가 있을 것이다. 3이 마지막에 나오지 않는 이상 진다. 1/3 확률로 이긴다.

</details>

</details>

11
