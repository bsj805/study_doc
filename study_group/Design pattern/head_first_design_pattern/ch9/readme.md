1. 다음 웨이트리스 클래스는 pancakeHouseMenu 와 dinerMenu를 받아서 iterator를 생성해 순회를 하고 있다. 여기서 문제점은?

```java
public class Waitress {
    PancakeHouseMenu pancakeHouseMenu;
    DinerMenu dinerMenu;
    
    
    Public Waitress(PancakeHouseMenu pancakeHouseMenu, DinerMenu dinerMenu){
        this.pancakeHouseMenu = pancakeHouseMenu;
        this.dinerMenu = dinerMenu;
        
    }
    
    public void printMenu() {
        pancakeHouseIterator = pancakeHouseMenu.createIterator();
        dinerMenuIterator = dinerMenu.createIterator();
        while(pancakeHouseIterator.hasNext()){
            MenuItem menuItem = pancakeHouseIterator.next();
            System.out.println(menuItem.getName());
        }
        while(dinerMenuIterator.hasNext()){
            MenuItem menuItem = pancakeHouseIterator.next();
            System.out.println(menuItem.getName());
        }
    }
}
```



<details>
<summary> 정답: </summary>
1. code duplication 존재한다. <br/>
2. pancakeHouseMenu와 dinerMenu에 createIteator()가 있음을 몰라서 구상클래스에 직접적인 의존성을 가진다. <br/>
</details>


2. 이 코드에서 문제점은?

```java
public class Waitress {
    PancakeHouseMenu pancakeHouseMenu;
    DinerMenu dinerMenu;
    
    Iterator pancakeHouseIterator;
    Iterator dinerMenuIterator;
    
    Public Waitress(PancakeHouseMenu pancakeHouseMenu, DinerMenu dinerMenu){
        this.pancakeHouseMenu = pancakeHouseMenu;
        this.dinerMenu = dinerMenu;
        this.pancakeHouseIterator = pancakeHouseMenu.createIterator();
        this.dinerMenuIterator = dinerMenu.createIterator();
    }
    public void printMenu(){
        printMenu(pancakeHouseIterator);
        printMenu(dinerMenuIterator);
    }
    public void printMenu(Iterator iterator) {
        while(pancakeHouseIterator.hasNext()){
            MenuItem menuItem = pancakeHouseIterator.next();
            System.out.println(menuItem.getName());
        }
        while(dinerMenuIterator.hasNext()){
            MenuItem menuItem = pancakeHouseIterator.next();
            System.out.println(menuItem.getName());
        }
    }
}
```

<details>
<summary> 2번 힌트: </summary>

```java
public interface Iterator {

    boolean hasNext();
    
    Object next();
    
    void remove();

}
```

</details>

<details>
<summary> 정답: </summary>
1. iterator은 hasNext()만 있다. 즉 처음으로 갈 수 없다. <br/>
</details>

3. 컴포지트 패턴은 단일 역할 원칙을 깨는 대신 투명성을 확보한다. 투명성은 뭘까?

<details>
<summary> 3정답: </summary>
- 투명성이란, 그것을 소유한 객체에서 봤을 때 구분이 되지 않는다는 것을 의미한다. 중간 노드와 leaf노드의 인터페이스를 같게하면서 클라이언트는 똑같은 방식으로 그들을 처리할 수 있다. <br/>
</details>


4. iterator클래스를 만들어서 has_next메서드를 구현하는 과정은 예전에 우리가 배운 패턴 같다. 어떤 패턴과 유사할까? (그냥 내 생각)

- 전략 패턴
- 옵저버 패턴
- 데코레이터 패턴
- 팩토리 패턴
- 싱글턴 패턴
- 커맨드 패턴
- 어댑터 패턴
- 파사드 패턴
- 템플릿 메서드 패턴


<details>
<summary> 4.정답: </summary>
- 내부 구현을 몰라도 하나의 메서드를 통해 상호작용 할 수 있게 한 것이 파사드 패턴같다고 느꼈음.   <br/>
</details>

5. 컴포지트 패턴에서, 복합 객체 내에 다른 일을 하는 객체도 노드로 딸려있으면, 해당 메서드는 어떻게 구현해야 하는가? (2가지)

<details>
<summary> 5.정답: </summary>
- 1. 노드마다 인터페이스를 달리해도 되는데 메서드를 호출할때마다 노드의 instance_of를 확인해주어야 한다.   <br/>
- 2. null객체, false 리턴 등 <br>
</details>
