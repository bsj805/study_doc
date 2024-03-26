LSP: 간단히 말하자면 o1 객체를 이용해 만들어진 함수에 o2 객체를 넣어도 해당 함수의 기능이 일정해야

# 다음 함수가 있다. LSP를 지킨 것일까?

```java

class SoundEffect {
    void echoWalk(Animal animal){
        animal.printWalk();
    }
    
}

class Animal {
    void printWalk(){ // 걸을 때 이펙트
        println("또각또각");
    }
    
}
class Bird extends Animal {
    void printWalk(){ // 걸을 때 이펙트 ?? 
        println("푸드드덕");
    }
}

class Cow extends Animal {
    void printWalk(){ // 걸을 때 이펙트 ?? 
        println("쿵...쿵...");
    }
}



```

<details>

1. SoundEffect의 echoWalk 함수가 어떤 Animal type을 사용하던 신경쓰지 않는다 
2. 다만, 언젠가 문제가 발생할듯? 나는 새에 printWalk를 호출하다니. 디자인 principle에선 안걸리는듯?
   - SRP
   - OCP
   - LSP
   - ISP
   - DIP


</details>


# 아래는 LSP를 위반하는가

```java

class SoundEffect {
    void echoWalk(Animal animal){
        if instanceOf(animal, Bird) {
            animal.printFly();
        } else{
            animal.printWalk();
        }
    }
    
}

class Animal {
    void printWalk(){ // 걸을 때 이펙트
        println("또각또각");
    }
    
}
class Bird extends Animal {
    void printFly(){ // 날 때 이펙트 ?? 
        println("푸드드덕");
    }
}

class Cow extends Animal {
    void printWalk(){ // 걸을 때 이펙트 ?? 
        println("쿵...쿵...");
    }
}



```



<details>

이 경우 LSP를 위반한다. 타입에 의존성이 생겨버린다. 
- 하지만, Bird를 extend 하는 경우가 더 있었다면 나는 LSP 라고 할래? 
- 생성자에 if 문 쓰는것을 지양하는 게 클린 코드, 그게 다 LSP 때문이었나봄. 
```java
class ChamSay extends Bird {
    void printFly(){ // 날 때 이펙트 ?? 
        println("포도도독");
    }
}

class Dakk extends Bird {
    void printFly(){ // 날 때 이펙트 ?? 
        println("파다다닥");
    }
}

```


</details>


## 부가문제: 위의 경우처럼 Bird 클래스의 경우 특별한 실행을 하게 했으면 좋겠다면, 어떻게 처리해야 할까?

<details>

- 책에서 나온 바로는 Dispatch Format을 적어서, 클래스 정보가 특정 expression에 맞다면(ex. regex) 특정 포맷을 사용하도록 한다.
  - 코드는 항상 가만히 있고, 들어오는 클래스 정보가 하드코딩되는 것은 모두 static 파일로 막을 수 있다.


</details>


