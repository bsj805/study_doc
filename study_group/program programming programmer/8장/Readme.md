# 노하우

- 재계산을 피하기 위한 상태 저장
- 정보를 사전처리해서 데이터 저장해두기
- 나누어 푸는 알고리즘
- 스캐닝 알고리즘
- 누적
- 하한
  - lower boundary를 보이기


# 연습 문제


# 문제 1

알고리즘 3과 4는 틀리기 쉬운 미묘한 코드를 사용한다. [칼럼 4]의 프로그램 검증 기법을 사용해서 코드의 정확성을 증명하라.

특히 루프 불변식(invariant)를 신중하게 정하기 바란다. 


루프 불변식 - 이진탐색 루프를 돌 때마다 mustbe(l,u) 라고 해서, target이 a[l] a[u] 사이에 있음을 사용했었다.

루프의 처음부터 끝까지 사실인것을 의미한다.


```

float maxsum3(l, u)
    if (l > u) 
        return 0
    if (l == u)
        return max(0, x[l])
    m = (l + u) / 2 
    
    lmax = sum = 0
    for (i = m; i >=l ; i-- )
        sum += x[i]
        lmax = max(lmax, sum) 
    rmax = sum = 0
    for i = (m, u]
        sum += x[i]
        rmax = max(rmax, sum)
    return max(lmax+rmax, maxsum3(l, m) , maxsum3(m+1, u))

```


<details>

```

float maxsum3(l, u)
    if (l > u) 
        return 0
    if (l == u)
        return max(0, x[l])
    m = (l + u) / 2 
    
      
        
    lmax = sum = 0
    for (i = m; i >=l ; i-- )
        sum += x[i]
        lmax = max(lmax, sum)    
    LOOP_INVARIANT: maximum( [l,m] ) <= lmax 
     
    rmax = sum = 0
    for i = (m, u]
        sum += x[i]
        rmax = max(rmax, sum)
    LOOP_INVARIANT: maximum( [m,u] ) <= rmax
        
    LOOP_INVARIANT: maximum( [l,u] ) <= lmax+rmax
    
    return max(lmax+rmax, maxsum3(l, m) , maxsum3(m+1, u))

```

항상 l~u까지의 최대값보다 lmax+rmax값이 커야하는 loop invariant를 충족한다면, 범위 실수로 어떤 항목이 연산이 안되었다거나를 잡을 수도 있지 않을까?

확실한 invariant를 세팅하려면, l~u까지 maxsum1(l,u) (원시적인 방법) 을 사용했을 때 maxsum1(l,u) == maxsum3(l,u) 하면 되겠지만 그게 loop invariant는 아니겠지? 

(물론 범위 실수가 마침 최대값을 연산 안하는 경우이겠지만)

</details>


# 문제 1.2 


알고리즘 4

```
maxsofar = 0
maxendinghere = 0
for i = [0, n)
    invariant : maxendinghere and maxsofar are accurate for x[0..i-1] 
    maxendinghere = max(maxendinghere + x[i], 0)
    maxsofar = max(maxsofar, maxendinghere)
    
    # 실수하기 쉬운 부분이 무엇일까? 예전 항목보다 더 큰 항목만 나온다면 상관없다.  
    LOOP_INVARIANT: prev_maxsofar <= maxsofar 
    
   
```

해답: https://www.cs.cornell.edu/gries/TechReports/82-531.pdf


이론설명

```
최초에 true인 condition은 P 

loop 끝났을때 true여야 하는 condition이 R 

R의 조건을 약화시켜서, 첫 invariant를 만들어보라고 한다.
``` 

post condition은  max(arr[i],arr[j]) >= arr[i] >= arr[j] >= total_sum(i,j)

constant 시간내에 계산이 될만 한걸 loop invarant로 써야하고, 

total_sum(i,k-1) 까지의 최대값과, 그 i, k값을 안다고 치면, total_sum(i, k) 까지의 값도 constant 시간에 계산될 수 있다. 
 
ex. [1,4]까지의 최대값이 10인것을 알고있고 지금이 5번째라면 [1,5]까지의 최대값은 max(10 + arr[5], 0) 다. 이걸 전체 최대랑 비교해서 실제 부분합의 최대 이끌어낼 수 있다. 

![img_1.png](img_1.png)

![img_2.png](img_2.png)




# 문제 2. 앞 네가지 알고리즘에 대한 실행시간 측정


# 문제 3. 앞에서는 O 표기법만 사용. 각 알고리즘이 사용하는 max 함수의 횟수는? 각 알고리즘은 메모리를 얼마나 필요로 하는지?

# 문제 4. 

입력된 배열의 각 요소가 [-1, 1] 에서 균일하게 선택된 랜덤한 실수일 경우, 부분벡터의 최대합에 대한 기대값은 얼마일까? 

<details>

기댓값을 구하는 방법부터 찾아봄

기댓값은 각 사건이 벌어졌을 때의 이득과 그 사건이 벌어질 확률을 곱한 것을 전체 사건에 대해 합한 값

![img.png](img.png)

너무 어렵다 

단순하게 생각하면, f(x)는 실수 하나를 뽑는 일정한 확률이고, x는 해당 실수값이다. 

n이 5라면 실수하나를 균일하게 뽑을 확률 1/5라고 해보자. 아래가 a,b,c,d,e 로 이뤄진 배열을 만들게 되는 기대값이다. 

`a*1/5 + b*1/5 + c*1/5 + d*1/5 + e*1/5`

최대합에 대한 기대값은 각 요소가 1/2 확률로 최대합에 포함되느냐 안되느냐이지 않을까?  

`a*1/10 + b*1/10 + c*1/10 + d*1/10 + e*1/10`
 
단순하게 생각해봤을 때, [-1 ,0, 1] 같은 배열이 나올 수 있고, 기대값은 1에 수렴할 것 같긴 하다. [-1, 1, 0] 어찌됐던 음수는 무시할테고 [0,1] 사이의 값만 취하게 될테니까>? 이유를 모르겠네 근데. 

hint: random walk의 누적값을 그래프로 그려보라.

기대값은 평균이다. 1.07에 가깝다. 

1.0727177778110957


![img_3.png](img_3.png)


</details>

# 문제 7 스캐폴딩으로 답 찾았을 때 미묘한 오차

max sum 찾는 알고리즘 구현했을 때 스캐폴딩을 사용해서 알고리즘 4의 답과 나머지 알고리즘이 구한 답을 비교했다. 스캐폴딩이 알고리즘 2b와 3에 대해 에러를 출력했다. 

답으로 나온 수치는 동일하지는 않더라도 매우 가까운 값이었다. 무엇이 문제였을까?



알고리즘 4

```
maxsofar = 0
maxendinghere = 0
for i = [0, n)
    invariant : maxendinghere and maxsofar are accurate for x[0..i-1] 
    maxendinghere = max(maxendinghere + x[i], 0)
    maxsofar = max(maxsofar, maxendinghere)    
   
```

알고리즘 2b

```
cumarr[-1] = 0
for i = [0, n]
  cumarr[i] = cumarrr[i-1] + x[i]
maxsofar = 0
for i = [0, n)
  for j = [i, n)
    sum = cumarr[j] - cumarr[i-1]
    maxsofar = max (maxsofar, sum) 

```

알고리즘 3
```

float maxsum3(l, u)
    if (l > u) 
        return 0
    if (l == u)
        return max(0, x[l])
    m = (l + u) / 2 
    
      
        
    lmax = sum = 0
    for (i = m; i >=l ; i-- )
        sum += x[i]
        lmax = max(lmax, sum)    
    LOOP_INVARIANT: maximum( [l,m] ) <= lmax 
     
    rmax = sum = 0
    for i = (m, u]
        sum += x[i]
        rmax = max(rmax, sum)

```

알고리즘 3은 명확하게 float을 반환했기 때문에 미묘한 차이가 발생할 것 같은데, 2b는 왜일까? 

floating point로 정수를 정확히 표현할 수 없기 때문. 2b도 같은문제라고 한다. 


# 10 최대합 대신 0에 가까운 합을 가지는 부분벡터를 찾는 것이 목적이라면? 

여러분이 이 문제를 풀기 위해 디자인할 수 있는 가장 효율적인 알고리즘은 무엇인가? 

어떤 알고리즘 디자인 기법을 적용할 수 있는가? (DP?, divide and conquer? scanning?) 

또, 주어진 실수 t에 가장 가까운 합을 가지는 부분벡터를 찾는다고 하면 어떻겠는가? 

 

```
maxsofar = 0
maxendinghere = 0
for i = [0, n)
    invariant : maxendinghere and maxsofar are accurate for x[0..i-1] 
    maxendinghere = max(maxendinghere + x[i], 0)
    maxsofar = max(maxsofar, maxendinghere)    
   
```

scanning해서 max함수 대신에 0에 가까운지를 측정하는 애로 바꾸면 안되나? 

그렇게 하면 [1,-4,-2,5]  하면 바로 안된다. [0]번째 index를 저장해놓고 그게 계속 정답이기 때문이다.

idx0 - idx3 까지의 경우의 수를 다 구하는것이 기본적인 알고리즘 

divide and conquer 하면 절반씩 나눈다고 했을 때, 

1. 왼쪽 절반에서 0에 가까운 부분합이 나오거나

2. 오른쪽 절반에서 0에 가까운 부분합이 나오거나

3. 왼쪽 절반과 오른쪽 절반의 각 일부를 합쳤을때 0에 가까운 부분합이 나오거나.
  - 이게 문제인 상황인것 같은데, 모두를 포함한 total sum을 센 다음에  
    - element를 왼쪽에서부터 하나씩 제거하면서 부분합중 0에 제일 가까운거 찾기 
    - element를 오른쪽에서부터 하나씩 제거하면서 부분합중 0에 제일 가까운거 찾기 


아하 


1. 왼쪽 끝을 포함해서 0에 가까운 부분합이 나오거나 
  - 왼쪽 끝에서부터 오른쪽 끝까지 total sum을 구하고, 오른쪽 끝에서부터 원소를 하나씩 제거하면서 부분합중 0에 제일 가까운 거 찾기 

2. 오른쪽 끝을 포함해서 0에 가까운 부분합이 나오거나 
  - 오른쪽 끝에서부터 왼쪽 끝까지 total sum을 구하고, 왼쪽 끝에서부터 원소를 하나씩 제거하면서 부분합중 0에 제일 가까운 거 찾기 

3. 왼쪽 또는 오른쪽 끝을 포함하지 않은 대상에서 0에 가까운 부분합이 나온다. 아래처럼 recursive하게 실행시키면 되지 않을까 생각
  - close_to_zero( left_part_sum, right_part_sum, func(middle_start, middle_end) )


해답은 누적 배열을 사용하라는 것이다. 

cum[i]=x[0]+...+x[i] 가 성립하도록 누적배열 cum을 초기화하라. cum[l-1]=cum[u]라면, 부분벡터 x[l..u] 의 합이 0이다. 

왜냐하면? [1,-4,-2,5] 라고 했을 때  

```

cum[0] = 1

cum[1] = -3

cum[2] = -5

cum[3] = 0
 
```

같은 지점이 없으면 가장 차이가 적은지점. cum[3] = 0 , cum[0] = 1 이니까 (0,3)

[1,-4,-2] 라고 하면 같은 지점이없는데?  이경우도 cum arr를 정렬해서 가장 차이가 적은 지점을 찾으면 된다. 


```
cum[0] = 1

cum[1] = -3

cum[2] = -5
```

-3, -5이 가장 적으니 (1,2)가 답이다. 0에 가장 가깝다라는 것은, a-b = 0 이어야 된다는 뜻이니까, a랑 b 사이의 차이가 가장 작은 값이 답이기 때문이다.   

```python
def close_to_zero(a,b):
   if abs(a) >= abs(b):
      return b
   else:
      return a
```

따라서 cum에서 `값이 가장 가까운 요소 두 개의 위치` == `(1,2)` 를 알면 합이 0에 가장 가까운 부분벡터를 찾을 수 있고, 이는 배열을 정렬하면 O(nlogn)에 가능하다.

```
# cum[i]의 값과 그 인덱스를 함께 저장한 후 정렬
cum_indices = sorted((value, index) for index, value in enumerate(cum))

# 최소 차이 찾기
min_diff = float('inf')
best_l, best_u = -1, -1
for i in range(1, len(cum_indices)):
    diff = abs(cum_indices[i][0] - cum_indices[i - 1][0])
    if diff < min_diff:
        min_diff = diff
        best_l, best_u = sorted([cum_indices[i][1], cum_indices[i - 1][1]])

# 최적 부분 벡터 출력
print(f"0에 가까운 합을 가지는 부분 벡터: x[{best_l}:{best_u}]")
```


13. 최대합 부분벡터 찾는 문제 - 실수로 이뤄진 n*n 배열이 주어졌고, 직사각형 모양의 부분배열에 대한 최대합을 구해야 한다. 이 문제의 복잡성은 어느정도인가? 

- 우리는 O(N) solution을 갖고있으니까 O(N^2)이 되는게 아닌가? 

- 직사각형모양으로 부분배열을 잡았을 때 최대값을 구하래.

누적합을 못만들것 같은데, 각 지점마다 N^2번 해봐야하니까 O(N^4) 아닐까? 


m*n 배열의 최대합 부분배열은 길이가 m인 방향으로는 알고리즘 2의 기법 (DP로 cumarr를 미리 구해두는것 )

길이가 n인 방향으로는 알고리즘 4의 기법을 사용해서 O(m^2n) 시간 내에 풀 수 있었다고 한다. 

Tamaki와 Tokuyama는 O(N^3[log(log n)/(log n)]^(1/2)) 에 작동하는 알고리즘 발표. 최상의 하한은 n^2에 비례할 정도라고 한다.

https://chatgpt.com/share/67a0d8f1-3090-8012-a58e-077b76f56e92

📌 알고리즘 개요
모든 가능한 행 구간을 선택

[r1,r2]
해당 행 구간을 압축하여 1D 배열을 만듦
1D 배열에서 Kadane’s Algorithm(최대 연속 부분 배열 알고리즘) 적용
최대 합을 갱신


```
def max_sum_submatrix(matrix):
    if not matrix or not matrix[0]:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    max_sum = float('-inf')

    # Step 1: Iterate over all possible row start points (r1)
    for r1 in range(rows):
        # Create a 1D array to store column sums for row range [r1, r2]
        col_sums = [0] * cols
        
        # Step 2: Expand to row r2 and calculate column sums
        for r2 in range(r1, rows):
            for c in range(cols):
                col_sums[c] += matrix[r2][c]

            # Step 3: Apply Kadane's Algorithm on col_sums
            max_sum = max(max_sum, kadane(col_sums))
    
    return max_sum

# Standard Kadane's Algorithm to find max subarray sum in 1D array
def kadane(arr):
    max_sum = float('-inf')
    current_sum = 0
    
    for num in arr:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
matrix = [
    [1,  -2, -1, 4],
    [-8,  3,  4, 2],
    [3,   8, 10, 1],
    [-4, -1,  1, 7]
]

print(max_sum_submatrix(matrix))  # 출력: 최대 합 부분 배열의 합
```
