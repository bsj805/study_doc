# 코드 튜닝

- 코드 튜닝 규칙들
    - Exploit Common Cases : 가장 많이 사용되는 타입의 레코드를 캐싱한다.
    - Exploit an Algebraic Identity : 비용이 많이 드는 나머지 연산을 값싼 비교연산으로 대체
    - Collapsing a Procedure Hierarchy: 함수를 매크로로 대체해 2배의 속도개선
    - Loop unrolling
    - Data structure Augmentation: 위도, 경도를 카테시안 좌표로 저장
    - Combining Tests: 루프 비교횟수를 줄인다. increment만 있게해서 (매번 종료조건 검사를 target 값을 찾는것과 동일하게)

# 1. 자신이 직접 작성한 프로그램을 프로파일링해보고, 이 칼럼에서 설명한 접근방법을 이용해서 핫스팟에서의 실행시간을 단축시켜보라

```
         88353 function calls (88134 primitive calls) in 0.067 seconds

   Ordered by: internal time
   List reduced from 92 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     9630    0.019    0.000    0.019    0.000 {method 'translate' of 'str' objects}
     2234    0.007    0.000    0.042    0.000 short_id2uri.py:55(is_object_type)
     9630    0.004    0.000    0.024    0.000 /envs/entity_ranking/lib/python3.9/re.py:270(escape)
      694    0.003    0.000    0.021    0.000 short_id2uri.py:99(escape_object_type)
      183    0.003    0.000    0.003    0.000 {method 'write' of '_io.TextIOWrapper' objects}
     2234    0.003    0.000    0.026    0.000 short_id2uri.py:66(<listcomp>)
      695    0.002    0.000    0.005    0.000 short_id2uri.py:167(convert_object_type)
     3695    0.002    0.000    0.006    0.000 /envs/entity_ranking/lib/python3.9/re.py:289(_compile)
    10901    0.002    0.000    0.002    0.000 {method 'startswith' of 'str' objects}
     4651    0.002    0.000    0.002    0.000 {method 'join' of 'str' objects}

```

<details>

translate는 f'{} 같은걸 많이 사용하기 때문이고, is_object_type이라는 함수를 최적화해야한다.

AS_IS

```
if re.search("<.+?wikipedia:", token):
    # wikipedia
    re_obj = re.search("<(.+?)wikipedia:", token)
    wikipedia_lang = re_obj.group(1)



```

re.search가 두번 호출되고 있다. conditional 을 줄이기.

TO_BE

```

if (re_obj := re.search(r"<(.+?)wikipedia:", val)):
    wikipedia_lang= re_obj.group(1)

```

AS_IS

```
3695    0.002    0.000    0.006    0.000 /envs/entity_ranking/lib/python3.9/re.py:289(_compile)

TO_BE
3569    0.002    0.000    0.007    0.000 envs/entity_ranking/lib/python3.9/re.py:289(_compile)
```

실제로 줄어들었다!

```
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
9630    0.021    0.000    0.021    0.000 {method 'translate' of 'str' objects}
2234    0.007    0.000    0.046    0.000 short_id2uri.py:55(is_object_type)
9630    0.005    0.000    0.027    0.000 envs/entity_ranking/lib/python3.9/re.py:270(escape)
183    0.004    0.000    0.004    0.000 {method 'write' of '_io.TextIOWrapper' objects}
694    0.003    0.000    0.023    0.000 /short_id2uri.py:99(escape_object_type)
2234    0.003    0.000    0.029    0.000 short_id2uri.py:66(<listcomp>)
695    0.002    0.000    0.005    0.000 short_id2uri.py:167(convert_object_type)
3569    0.002    0.000    0.007    0.000 envs/entity_ranking/lib/python3.9/re.py:289(_compile)
10901    0.002    0.000    0.002    0.000 {method 'startswith' of 'str' objects}
4651    0.002    0.000    0.002    0.000 {method 'join' of 'str' objects}
```

</details>

4. 양의 정수 n의 최대값은 배열의 크기라고 할 때, 다음 재귀적 C 함수는 배열 x[1..n-1]의 최대값을 리턴한다.

```c
float arrmax(int n)
{
  if (n==1)
     return x[0];
  else
     return max(x[n-1], arrmax(n-1));
}

```

max를 함수로 구현했을 때 n=10,000인 벡터에서 최대값을 구하는데는 2~3ms가 걸린다. max가 다음과 같은 C 매크로라면

`# define max(a,b) ( (a) > (b) ? (a) : (b))`

이 알고리즘은 최대값을 찾는데 n=27일 때 6초가 걸리고, n=28일 때에는 12초가 걸린다. 이런 엄청난 동작이 나타나도록 입력을 주고, 실행시간을 수학적으로 분석해보라


<details>

우선, max함수를 매크로로 사용하는 이유는

일반 함수로 max를 만들면, 호출할 때마다 스택에 인자(push) -> 함수 호출 -> 리턴값 반환 과정이 필요해서 성능이 저하

반면, 매크로 함수는 단순히 코드 치환이기 때문에 함수 호출 오버헤드가 없다

그런데 이게 재귀함수가 된다면,

`return ((x[n-1]) > (arrmax(n-1)) ? (x[n-1]) : (arrmax(n-1)));`

이렇게 치환되면서, arrmax(n-1)이 앞에서도 함수값이 계산되야 하고, 뒤에서도 함수값이 계산되야 하기 때문이다.

그래서 2^n번의 operation이 진행되게 된다고 한다 (해답)

처음에는 2군데만 생기고, 그다음엔 4군데에서 계산되야하고 ...

</details>