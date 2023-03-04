```java
public class UrlResponseHandler {
    private Stream stream;
    private Logger logger;

    public Stream openStream(Url url, int option) throws Exception {
        if (option == 0) {
            logger.setMode(DEBUG);
        } else if (option == 1) {
            logger.setMode(ERROR);
        }
        if (!url.startsWith("www.")) {
            throw new Exception("Wrong URL");
        }
        return ByteInputStreamBuilder.url(url).build();
    }

    public String getBytes(int length) {
        return stream.getBytes(length);
    }

    public void closeStream() {
        stream.close();
    }
}

@Test
public class UrlResponseHandlerTest {
    @Test
    public void validURLSuccess() {
        UrlResponseHandler handler = new UrlResponseHandler();
        handler.openStream("www.abc.com", 1);
        String res = handler.getBytes(10);
        handler.closeStream();
        assertTrue(res != null);
        assertTrue(res.length() > 9);
    }

    @Test
    public void invalidURLFail() throws Exception {
        UrlResponseHandler handler = new UrlResponseHandler();
        handler.openStream("www.", 1);
        String res = handler.getBytes(10);
        handler.closeStream();

        assertTrue(res.length() == 0);
    }
}
```

1. 리팩토링할 방법들을 말해보시오

<details>
<summary> 1정답: </summary>
assertion을 length로 하지 말고 명확한 string이 될 수 있게 목업을 제공한다.  <br/>
closeStream() 같은 경우엔 두개 다 부르니까 After로 빼는것이 좋고  <br/>
AAA (arrange act assert) 를 \n으로 분리해주면 좋다  <br/>
assertion할때는 null check가 필요없다  <br/>
openStream의 뒤 숫자는 magic number라는것을 알릴 수 있게 (상수로 선언하지 않은 수를 magic number) ARBITRARY_NUMBER 따위로 선언한다 <br/>
</details>
