REP : 재사용/릴리스 등가 원칙 (Reuse/Release Equivalence Principle) - 릴리즈 단위로 컴포넌트 묶어라
CCP: 공통 폐쇄 원칙 (Common Closure Principle) - 컴포넌트 안에 모아라
CRP: 공통 재사용 원칙 (Common Reuse Principle) - 불필요한거까지 의존하지 않게 컴포넌트 나눠라

# 문제 1. 아래 중 필수적으로 같은 컴포넌트에 속해야 하는 클래스는 어떤 것일까?

```java
class Book extends Object {
    String title;
    String author;
    String coordinate;
}

class BookShelf extends Object {
    Book[] books;

    String printBookStatus() {
        for (Book book : this.books) {
            // book의 모든 원소를 출력
            sys.Out.println(book.title);
            sys.Out.println(book.author);
            sys.Out.println(book.coordinate);
        }
    }
}

class Librarian extends Person {
    // 책을 컨트롤하는 클래스
    String name;
    String phoneNumber;
    Queue<Book> taskList;

    String changeBookCoordinate(Book book, String coordinate) {
        book.setCoordinate(coordinate);
    }
}

class Library extends Building {
    BookShelf[] bookShelves;
    Librarian[] librarianList;

    String addLibrarian(Librarain librarian) {
        librarianList.pushBack(librarian);
    }

    Boolean addTaskToRandomLibrarian(Book book) {
        random.Choice(this.librarianList).addTask(book);
    }
}

class LibraryNetwork {
    Library library;

    Boolean addBookToLibrary(Book book) {
        library.addTaskToRandomLibrarian(book); // 아무튼 queue에 book 밀어넣으면 librarian이 갖다놓는다.
    }
}
```

<details>
<summary> 내가 생각하는 정답 </summary>

경우의 수 너무 많으니 대충 보이는 것만.

1. CCP는 변경될 가능성이 있는 클래스는 모두 한곳으로 묶을 것을 권한다. 항상 함께 변화되는 클래스라면 같은 컴포넌트에 있어야 한다.

- 따라서 Book과 BookShelf는 같은 컴포넌트여야 할것.
- Library는 book에도 의존성을 갖고 있긴 하지만, Book이라는 클래스가 없어지지 않는 이상은 동일한 로직을 사용할 수 있다.

2. CRP는 같이 재사용되는 경향이 있는 클래스와 모듈들이 같은 컴포넌트에 위치해야 한다고 한다.

- 강하게 결합되지 않았다면 동일 컴포넌트에 위치시키지 말라. 쓸데없이 의존성 생긴다.
- LibraryNetwork와 Library 도 같이 재사용될 것이 확실해 보인다.
    - 이들은 같은 컴포턴트에 있을 때 좋을 듯 하다.
- Librarian의 경우 Book 하나만을 사용하는데 Book쪽 컴포넌트에 의존성을 갖게 되었다.
    - 하지만 Librarian도 Book 클래스가 사라지지 않는 이상은 독립적이다. (Book은 String클래스와 같은 존재)

따라서 {Book, BookShelf} {LibraryNetwork, Library} {Librarian} 할 수 있지 않을까?

매번 최소한의 컴포넌트만 재배포 가능

</details>

# 2. 일반적으로 CCP, REP 중 개발 초기에 고려되는 것과 후기에 고려되는 것은?

<details>
<summary> 정답 </summary>

개발 초기에는 CCP를 해서, 컴포넌트 안에 몽땅 넣어놓는 것이 developability에 좋다.

이후에 재사용성을 높여서 추가적인 컴포넌트 추가가 쉽게 하자.

</details>