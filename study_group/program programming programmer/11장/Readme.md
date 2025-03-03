# 11장 sort 

swap(i, j) 는 arr[i], arr[j] 를 바꾸는 연산임


qsort1은 0번째를 t로 정하고, t보다 작은경우에 swap시키는 방법을 사용해서 n개의 요소가 모두 동일한 배열일 때 느려짐 (한번에 하나의 원소만 위치가 결정됨)

qsort3은 i,j가 왼쪽끝, 오른쪽끝에서 각각중앙으로가다가, t보다 작은 i 또는 t보다 큰 j를 만났을때 멈추는 방식



# 연습문제 

# 1
1. n개 부동소수점 수 배열에서 정렬 잘못 사용되는 케이스 

- 비교연산이 정확하지 않으니까 


```python

    a = 0.1 + 0.2
    b = 0.3

    print(a == b)  # False 출력
    print(a)  # 0.30000000000000004 출력
```

- 이런 경우에는 평균구하는것 같은게 잘못될 수 있음. 다만 정렬에서 문제가 아리송


# 2. x[l]을 센티널로 사용해서 Lomuto의 분할 기법의 속도를 개선해보라. 

이 기법이 어떻게 루프 다음의 swap 함수 호출을 제거할 수 있게 하는지 보여라. 


## 2 답

qsort1은 0번째를 t로 정하고, t보다 작은경우에 swap시키는 방법을 사용해서 n개의 요소가 모두 동일한 배열일 때 느려짐 (한번에 하나의 원소만 위치가 결정됨)

```c

void qsort1(l, u)
    if (l>=u) return;
    m = l; # 첫원소로 t를 정함 (x[l]==t 인셈)
    for i = [l+1, u]
        if (x[i] < x[l])   # t보다 작으면 아래쪽으로 내린다.           
            swap(++m, i)
    swap(l, m)
    # x[l]이었던 대상의 위치가 m으로 확정됨 
     
    qsort(l, m-1)
    qsort(m+1, u)
```

이를 센티널로 바꾸면, 종료조건 검사가 매 루프마다 이뤄질 필요가 없이, 통합된다. 

```c
void qsort1_sentinel(l, u)
    if (l>=u) return;
    m = l; # 첫원소로 t를 정함 (x[l]==t 인셈)
    swap(l, u) # 루프의 종료 조건이 t를 만났을때가 될 수 있게  
        
    for( i=l+1; ; i++)
       
```

### 2. 실제답안
알고보니까 센티넬이 조건 검사를 제외시킬 필요는 없고, 그냥 배열의 특정 값을 만났을 때 종료되면 된다. 


그래서 거꾸로 루프를 돌게하면, 이를 구현할 수 있다고 한다. 일단 센티널을 적용하기 전 코드는 이렇다.  

```c
    m = u+1 
    for (i = u; i>= l; i--)
        if x[i] >=t 
            swap(--m, i)
```
종료되었을때 x[m] == t 인게 보장되기 때문에, swap이 더 필요하지 않음.      


```c
void custom_sort(vector<int>& x, int l, int u) {
    int t = x[l];
    int m = u + 1;
    int i = m;

    do {
        while (x[--i] < t); // 조건 만족할 때까지 감소        
        swap(x[--m], x[i]); // 값 교환
    } while (i != l);
}    
```

``` 
[2,1,4] 배열이라고 하자.

l = 0
u = 0
m = 3 
i = 3에서 시작한다.

#-------------- 첫번째 loop

while( x[--i] < t) ; 

t보다 작은값이 나올때까지 i를 줄인다. 
x[2] < 2 인가? False라서 바로 루프 끝남. 

swap(2,2) 가 실행되서 자기자신이랑 교환됨 
아직 i != l  (2 != 0) 이라서 다음 loop
#------------------

while( x[--i] < t) ;

t보다 작은값이 나올때까지 i를 줄인다 
x[1] < 2 맞기 때문에 while( x[--i] < t) ; 한번더. 

x[0] < 2 가 무조건 False일 수밖에 없음. (sentinel로 작용)  x[l] == t 이기 때문에. 
그래서 
swap(m, i) == swap(1, 0) 이 실행되고, sentinel이었던 애는 무조건 i에 있고, m보다 작은 위치는 모두 t보다 작기 때문에 quicksort 작동  
  

```

# 5


길이가 변하는 여러 개의 비트 열을 그 길이의 합에 비례하는 시간 내에 정렬하는데 Lomuto의 분할 기법을 어떻게 사용할 수 있는지 보여라. 


### 5 답안

가변길이의 비트 배열이 있다. 

이건 3N 안에 정렬되고
```
111
101
100
```

이건 4N 안에 정렬되고 ?? 
```
1111
1011
1001
```

이것도 비슷하게 분할정복을 할 수 있지 않나? 아래처럼 호출되도록 유도해서? 그러면 항상 길이의 합에 비례하는 시간내에 정렬될 것임. (bit_sort 2개씩이 길이 LENGTH만큼 호출될것. O(2*LENGTH)) 

bit_sort([D])

bit_sort([A,B,C])

```
A: 111
B: 101
C: 100
D: 000
```

### 5. 실제답안 
```c
void bsort(l, u, depth)
    if l >= u
        return 
    for i = [l, u]
        if x[i].length < depth
            swap(i, l++)
    m = l
    for i = [l, u]
        if x[i].bit[depth] == 0
            swap(i, m++)
    bsort(l, m-1, depth+1)
    bsort(m, u, depth+1)
    
```
ㅇㅇ 맞는듯하다. depth별로 sort



# 8 

여러분의 시스템 사용자가 정렬을 어떻게 선택해야 하는지를 보여주는 한 페이지짜리 가이드를 스케치해보라.

여러분이 제시한 방법은 실행시간, 공간, 유지보수 시간, 일반성(로마 숫자 문자열 정렬도), 안정성(key가 같을때 순서 유지되야함), 입력 데이터의 특성 등의 중요성을 고려해야 한다.


### 8. 답안 

`quicksort + insertionsort` 

- 실행시간: O(nlogn)
- 공간: O(N)
- 유지보수시간: quicksort가 chunk까지만 sort하기 때문에 상당히 복잡해진다. 
- 일반성: ...


![img.png](img.png)

# 11 

postcondition이 다음과 같은 두꺼운 피봇 분할 함수를 작성하라. 

func([values_less_than_t])

func([values_same_as_t])

func([values_larger_than_t])

어떻게 이 함수를 퀵 정렬 프로그램에 이용할 것인가? 


# 답안

아 뭔소린가 했더니..

```python

def three_way_partition(arr, t):
    less, equal, greater = [], [], []
    
    for num in arr:
        if num < t:
            less.append(num)
        elif num > t:
            greater.append(num)
        else:
            equal.append(num)
    
    return less, equal, greater

# 예제 테스트
arr = [3, 7, 2, 2, 5, 5, 5, 8, 1]
pivot = 5
less, equal, greater = three_way_partition(arr, pivot)

print("Less than t:", less)      # [3, 2, 2, 1]
print("Equal to t:", equal)      # [5, 5, 5]
print("Greater than t:", greater) # [7, 8]

```

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]  # 중앙값을 피벗으로 선택
    less, equal, greater = three_way_partition(arr, pivot)

    return quicksort(less) + equal + quicksort(greater)

# 예제 테스트
arr = [3, 7, 2, 2, 5, 5, 5, 8, 1]
sorted_arr = quicksort(arr)
print("Sorted array:", sorted_arr)
```

quicksort의 특징은, 같은값이 많을때 정렬이 너무 오래걸리는 문제. 그걸 해결할 수 있다. 

# 14 

이 칼럼의 퀵 정렬은 부분배열을 두 개의 정수 인덱스로 표현했는데, 이는 Java와 같이 포인터를 지원하지 않는 언어에서 필요하다. 

그러나 C나, C++에서는 정수 배열을 정렬하는 데 원래의 함수 호출과 모든 재귀적 호출에 대해 다음과 같은 함수를 사용할 수 있다. 

```c
void qsort(int x[], int n) 
```

이 인터페이스를 사용하도록 이 칼럼에서 사용한 알고리즘을 수정하라. 

### 14 답안

l=*x

u=*x+n

식으로 포인터를 담아두고 

for (i=l,i<u ; i+=(int*)1 ) 

이렇게해야하나?

```c
for (int *ptr = arr_low; ptr < arr_low + n; ptr++) {
    printf("%d ", *ptr); // 예시: 현재 값 출력
}

```

이렇게 순회하면 된다고 한다. 
