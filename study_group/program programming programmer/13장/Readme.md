# 탐색문제 

문제: 관련된 다른 데이터가 없는 정수의 집합을 어떻게 저장할 것인가? 

집합을 표현할 다섯가지 데이터 구조
- 배열
- 연결리스트
- 트리
- 비트 벡터
- 해시 테이블


# 문제 

# 1. 

연습문제 12.9의 해답은 랜덤한 정수의 정렬된 집합을 생성하기 위한 Bob Floyd의 알고리즘을 설명한다. 

이 칼럼의 IntSet들을 이용하여 그 알고리즘을 구현할 수 있겠는가? Floyd 알고리즘에 의해 생성된 랜덤이 아닌 분포에 대해 이들 구조는 어떻게 작동하는가? 


<details>

Robert W. Floyd 가 bob Floyd 씨라고 한다. 

Set 기반의 알고리즘으로 m개의 정수를 1,2,3,...n개의 배열에서 랜덤하게 추출하는 방법을 뽑는다. 

random한 정수를 generate하고, 중복을 찾으면 n이 클때 느려질 수 있다. Floyd 알고리즘은 메모리를 최소화 하면서, unique함을 보장하는 정수를 뽑는다. 


1. 랜덤 숫자를 저장하기 위한 empty set을 초기화한다.
2. `n-m+1` 부터 `n`까지 순회하면서 각 iteration마다 하나의 random한 숫자를 뽑는다.
   - 각 iteration j 마다, [1,j] 사이에 있는 t 하나를 뽑을 것이다. 

3. 만약 t가 set에 있다면 j를 넣고, 아니면 t를 넣어라. t는 [1,n-m+1] 까지일 수밖에 없고 j는 `[n-m+1,n]` 이고. 따라서 unique한 숫자가 선택됨
4. m iteration을 진행하면 m개의 unique한 숫자가 선택된다. 


```python
import random

def floyd_random_selection(n, m):
    selected = set()
    for j in range(n - m + 1, n + 1):
        t = random.randint(1, j)  # Pick a random number in the range [1, j]
        if t in selected:
            selected.add(j)  # If t is taken, use j instead
        else:
            selected.add(t)
    return selected

# Example usage
n = 100  # Range [1, 100]
m = 10   # Select 10 unique numbers
print(floyd_random_selection(n, m))
```

이 칼럼의 IntSet을 이용해서 알고리즘을 구현하려고 하면, 삽입정렬 사용하는 배열기반 정렬이 빨라질 수 있겠다. 

add할때 왼쪽 절반에 넣는지, 오른쪽 절반에 넣는지를 미리 알 수 있으니까. 나머지 링크드 리스트 기반, 트리 기반, 비트 벡터 기반, 해시 기반은 비슷하지 않을까? 

### 연습문제 해답

그냥 진짜 IntSet.insert(), IntSet.size() 인터페이스만 이용해서 구현할 수 있는지 묻는 것이었고, 

add 대신 IntSet.insert()를 사용하고, 우리의 insert문은 중복검사를 하기 때문에, insert(j) 한 다음에도 이전size와 size()가 동일하다면 t를 넣는 방식


한계점은 m과 maxval이 동일할 때 원소들을 오름차순으로 차례차례 삽입하기 때문에 최악의 경우가 생긴다. 

</details>



# 4. 

리스트, 빈, 이진 탐색 트리에 대한 재귀적 삽입 함수를 반복 사용하도록 재작성하고, 실행시간의 차이를 측정해보라 


<details>

리스트 

```
void insert(t):
    head = rinsert(head, t)

node* rinsert(p,t):
   if p->val < t
      p->next = rinsert(p->next, t)
   else if p->val > t
      p = newnode(t, p)
      n++
   return p  
```

트리
```

void insert(t):
    root = rinsert(root, t)

node* rinsert(p, t):
   if p == 0
        p = newnode(t, 0, 0)
        n++
   else if p->val < t
        p->right = rinsert(p->right, t)
   else if p->val > t
        p->left = rinsert(p->left, t)
    return p

```


빈

bins는 bin 최대 개수 - bin이 있고, 각 bin마다 연결리스트를 둔것. 
```
void insert(t):
    i = t / (1+maxval/bins)
    bin[i] = rinsert(bin[i], t)
node* rinsert(p,t):
   if p->val < t
      p->next = rinsert(p->next, t)
   else if p->val > t
      p = newnode(t, p)
      n++
   return p
```


n=1000 기준으로 역시 메모리 할당이 많이 필요한 링크드 리스트가 제일 많이먹고, 속도가 빠르긴 한 binary tree, 그다음이 해시 + linked list네. (bin이 100개라서 하나당 10개 이하로 떨어져서 그럴것.) 

{'Linked List': 0.0301, 
'Binary Tree': 0.0017, 
'Bins': 0.0009}


</details>

# 7. 우리의 배열, 연결 리스트, 빈은 모두 센티널을 이용한다. 이진 탐색 트리에 어떻게 같은 기법을 적용할 수 있는지 보여라 

<details>

이진 탐색 트리를 배열로 구현한다면 센티널을 사용할 수 있다?  

traverse가 종료됨을 센티널로 꺠달아야 하는데, 이진 탐색 트리는 루트에서 시작해서 끝까지 가는데, 이때 끝을 어떻게 알 수 있을까?

leaf 노드가 양쪽다 센티널이면 되는건 아닐까?

### 해답

이전 버전에서는 NULL이었던 포인터들이 모두 센티널 노드를 가리키도록 초기화 한다. 

root = sentinel = new node() 할때 , left, right 모두 sentinel을 가리키도록 한다.

삽입코드할 때에, 자기가 현재 센티넬 노드에 와있으면 그 자리에 삽입하는 방식이다. 


</details>


# 11. 

중복되지 않는 랜덤한 정수가 정렬된 배열을 생성하는 가장 빠르게 동장하는 완전한 함수를 작성하라. 

일단 중복되지 않는 랜덤한 정수를 뽑으려면 아래같은 selection을 사용해야 한다. 가장 빠르려면, bin을 두고 해싱기반의 정렬을 사용해야한다. 

비트벡터를 이용해서 j나 t번째 비트를 색칠해두고, traverse하면서 1인 비트를 차례대로 출력하면 O(n/8)로 끝날 수 있지 않을까?  

```python
import random

def floyd_random_selection(n, m):
    selected = set()
    for j in range(n - m + 1, n + 1):
        t = random.randint(1, j)  # Pick a random number in the range [1, j]
        if t in selected:
            selected.add(j)  # If t is taken, use j instead
        else:
            selected.add(t)
    return selected

# Example usage
n = 100  # Range [1, 100]
m = 10   # Select 10 unique numbers
print(floyd_random_selection(n, m))
```

<details>

GPT의 답안은 기가막히다

random.sample()은 내부적으로 Fisher-Yates Shuffle을 사용해 O(n) 에 동작.

sorted() 함수를 사용하면 O(nlogn)에 끝난다고 한다.

Knuth Shuffle, 즉 우리 지난 정렬할때 0...m번째 index까지 순회하면서 다른 원소랑 swap해서, m번째 index까지만 sort하는 방식이 제일 빠르다고 한다.  O(m) O(mlogm) 에 끝날테니까. 배열도 이미 정의되어있고. (공간할당 x)

</details>


