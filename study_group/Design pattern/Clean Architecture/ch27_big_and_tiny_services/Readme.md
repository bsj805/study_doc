# 27. 크고 작은 모든 서비스들


# 1. 기능단위로 분할한 마이크로서비스 기반 택시 서비스가 야옹이 운반서비스를 하려니 모든 서비스를 바꿔야 했던 이유는?

택시 UI, TaxiFinder, Taxi Supplier, Taxi Selector, Taxi Dispatcher

<details>
<summary> 정답 </summary>

- 모든 마이크로 서비스를 기능적으로 분할했기 때문
- 새로운 기능이 기능적 행위를 횡단하는 상황이었기 때문
- 다형적으로 확장할 수 있는 클래스 집합을 생성해서, 한쪽의 기능만 변경할것.  

</details>
