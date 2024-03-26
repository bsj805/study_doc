ISP: 다수의 사용자가 같은 인터페이스를 사용할 때에는, 각 사용자의 변경이 공통 인터페이스에 영향을 미치지 않도록 해라.

# 다음 함수가 있다. ISP를 지킨 것일까? ()

```java

interface Movable{
    void printWalk(){};
    void printFly(){};
}

class SoundEffect {
    void echoWalk(Animal animal){
        animal.printWalk();
    }
    
}

class Animal implements Movable{
    void printWalk(){ // 걸을 때 이펙트
        println("또각또각");
    }
    void printFly(){
        throw Exception;
    }
    
}
class Bird extends Animal implements Movable{
   void printWalk(){
      throw Exception;
   }
    void printFly(){  
        println("푸드드덕");
    }
}

class Cow extends Animal implements Movable{
    void printWalk(){ // 걸을 때 이펙트 ?? 
        println("쿵...쿵...");
    }
   void printFly(){
      throw Exception;
   }
}



```

<details>

1. 헬륨풍선에 대해서도 효과음이 동일했으면 좋겠어서 printFly가 아니라 printAviation으로 이름을 바꾼다고 해보자.
- 그럼 interface를 변경하면서 모든 클래스가 바뀐다. 

</details>


## 부가 문제: 어떻게 해결 할 수 있을까?


<details>

- movable 하위에 Walkable, Aviationable 인터페이스를 둬서 분리한다? 
  - 핵심은 Aviationable 의 변경은 Walkable에는 전혀 영향을 주지 않게 하는 것.
- 결국, 필요 이상으로 많은 모듈에 의존하지 말라.

</details>





