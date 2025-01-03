# 5장 프로그래밍에서 사소한 문제 

스캐폴딩을 통해서 오류를 찾아내자. 

# 1. 이 칼럼과 이 책에서 사용된 프로그래밍 스타일에 대한 의견을 말해보라.


변수 이름, 이진 탐색 함수의 형태와 명세, 코드 레이아웃 등의 문제에 대해서 말해보라. 


```c++

int badsearch(DataType t)
{
  int l, u, m;
  l = 0;
  u = n-1;
  while (l <= u) {
    m = (l + u) / 2;
    printf(" %d %d %d\n" , l, m, u);
    if (x[m] < t)
        l = m;
    else if (x[m] > t)
        u = m;
    else
        return m;
  }
  
  return -1;
}

```


<details>

x[m] < t 라면, 타겟보다 현재 영역이 작은 영역을 가리키고 있다는 뜻 ,l = m+1 이 되야하고, 

x[m] > t 라면, 타겟보다 현재 영역이 큰 영역을 가리키고 있다는 뜻, u = m-1이 되야한다 .


변수 이름이 직관적이니 좋은 것 같지만, l , m, u, t 변수가 하나만 더 많았어도 헷갈리기 시작했을 듯 하다. 


#### 정답에 써있는것

전역 변수는 10자~20자 정도의 긴이름을 사용한다. 이 칼럼에서 짧은 이름을 사용하면 스캐폴딩을 만드는데 편리하고, 4.3절처럼 수학적 증명을 할 때도 유리하다.

다만, 짧은 이름은 대형 프로젝트에는 적합하지 않다.

리턴문에 대해서도 Steve McConnell은 2개의 값을 리턴하는 게 더 바람직하다고 했다. (값 존재 여부, 인덱스)

에러 검출이 없기 때문에, scanf를 호출하는 코드같은 데에서 버퍼에 대한 오버플로우를 만들기 쉽다. 배열이 인자가 아니라 전역변수로 사용되었다. 



</details>


# 2. 이진탐색 테스트, 디버그할 스캐폴딩 작성하기 


전채 배열원소수가 홀수개, 짝수개일때 각각 0번째, mid번째, 맨 끝번째 원소 찾아지는지 확인할 것 같음


# 3. 이진탐색 함수에 에러를 포함시켜보고, 테스트가 어떻게 에러를 찾는지, 스캐폴딩이 어떻게 버그를 추적하는데 도움주는지 확인하라


위와 같은 badSearch 같은 경우는 n-1번째를 찾을 때 범위가 줄어들지 않는게 보일 것. 

# 4. 이진 탐색 코드를 그대로 두고, 이진 탐색을 호출하는 부분에 에러를 포함시켜서 버그 추적에 도움되는지 확인하라

```python
x=[1,3,2,5,4]

print("bad_result",goodsearch(1), goodsearch(3), goodsearch(5))

# bad_result 0 -1 3
```

이렇게 해보니까 goodsearch(3)의 원소가 있는데 결과값이 안나오는 걸 확인가능하다. 로직문제인지 input 요소문제인지는 어떻게구분할까?  

mutuation testing이라고, 적은 변화를 만들어놓고 test_case가 실제로 이걸 잡아내는지 확인하는 것.


<details>

로직 문제인지 input 요소 문제인지 구분하는 scaffolding은 정렬된 원소를 넣었을 때 잘 찾아주는 것에서 판단가능하겠다.

</details>

# 5. 정렬되지 않은 배열에 이진 탐색 적용은 흔한 버그

배열 정렬을 확인하려면 n-1번 추가 비교가 필요하다. 훨씬 적은 비용으로 partial checking을 하려면 어떻게 할까?

내생각에는, 맨 처음에 l, m, u 원소들이 정렬되어있는 상태인지 x[l] <x[m] < x[u] 인지 확인.  


# 6. 이진탐색 연구를 위한 GUI -> 디버깅 효율성이 투자한 시간보다 늘어나는가? 

정말 복잡한 알고리즘을 만든다고 할 때는 디버깅 효율성이 더 좋을 수 있다. (또, 계속 변화할 수도 있다면)

예를들면 b-tree https://www.cs.usfca.edu/~galles/visualization/BTree.html 이거 없이는 절대 못만들었다.  

# 7. 5.5절의 시간 측정 스캐폴딩은 잠재적인 버그를 갖고 있다.

```

while read(algnum, n, numtests)
    for i = [0,n)
        x[i] = i
    starttime = clock()
    for testnum = [0, numtests]
        for i = [0, n)
            switch (algnum)
                case 1: assert(binarysearch1(i) == i)
                case 2: assert(binarysearch1(i) == i)
    clicks = clock() - starttime
    print algnum, n, numtests, clicks

```


각각의 요소를 순서대로 탐색해서 캐시 이익이 있다.

Q1. 사용될 어플리케이션도 locality따른다면 좋은 테스트 프레임워크가 될 것이다. 다만, 이 경우 이진탐색은 아마 적절한 도구가 아닐 것이다. 

Q2. 그러나 탐색이 배열을 랜덤하게 찾는다고 생각하면, 우리는 벡터를 초기화한 다음 뒤섞어 놓고 그 다음에 랜덤한 순서로 탐색을 실행해야 한다. 

두가지 버전에 대해 시간을 측정해서 차이가 있는지 보라.


A1. 어떤 어플리케이션이 binarysearch(1), binarysearch(2), binarysearch(3) ... 호출하겠는가? 이진탐색을 사용할게 아니라 for문을 써라 

A2. 


```
random 안하고 캐시타게 한거
Algorithm: 2, Array size: 100000, Number of tests: 10, Time taken: 2.715887 seconds
Algorithm: 2, Array size: 100000, Number of tests: 10, Time taken: 2.643491 seconds
-------------------------
random 하게 해서 캐시 못타게 한거
Algorithm: 2, Array size: 100000, Number of tests: 10, Time taken: 3.208772 seconds
Algorithm: 2, Array size: 100000, Number of tests: 10, Time taken: 3.230644 seconds
-------------------------


random 안하고 캐시타게 한거
Algorithm: 2, Array size: 1000000, Number of tests: 10, Time taken: 30.476969 seconds
Algorithm: 2, Array size: 1000000, Number of tests: 10, Time taken: 30.287387 seconds
-------------------------
random 하게 해서 캐시 못타게 한거
Algorithm: 2, Array size: 1000000, Number of tests: 10, Time taken: 44.226329 seconds
Algorithm: 2, Array size: 1000000, Number of tests: 10, Time taken: 41.561534 seconds
-------------------------

```

배열을 정렬된 순서로 탐색하는 것에 비해 랜덤한 순서가 20% 느려진다고 한다. 

8.3절의 이진 탐색은 튜닝이 잘 되어서 정렬된 순서로 탐색하면 125ns가 든다.  
