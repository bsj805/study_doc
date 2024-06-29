# 26. 메인 컴포넌트

메인 컴포넌트는 가장 낮은 수준의 정책
- main함수 같은걸 의미하나보다.
- 의존성 주입, 팩토리, 전략패턴 등 모두 생성


# 1. 메인함수에서 Factory.retrieveClass('htw.game.seoul2021.FacadeClass'); 처럼 string으로 클래스를 로드한다. 이런 함수를 컴포넌트화 했을 때의 장점은

<details>
<summary> 정답 </summary>

- 일반적으로 이러면 안된다.
- 다만, 메인함수랑 소스코드 의존성을 없애서 메인함수를 재배포하거나 재컴파일 할 필요를 없앨 수 있다. 

</details>
