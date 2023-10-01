# 2장 URL과 리소스

#  2.2 URL 문법

URL은 리소스에 접근하는 방법을 제공한다. 

`스킴://사용자이름:비밀번호@호스트:포트/경로;파라미터?질의#프래그먼트`

`http://www.naver.com/hammers;sale=false/index.html` 이 있다면,

경로 조각은 hammers, index.html 이 속한다.

프래그먼트는 서버에게 전달되지 않는다. (일반적으로 http 서버는 객체 일부가 아닌 전체를 처리한다.)

# 2.3 단축 URL

## 2.3.1 상대 URL

html에서
```html
<a href="./hammers.html">hammer</a>
```
어떻게 해석할까?

현재위치가 http://www.naver.com/tools.html 이라면, 이게 기저 URL이 되고,

`http://www.naver.com` 에서 스킴(http) 와 호스트 (www.naver.com) 을 알아내서, 상대URL인 hammers.html을 뒤에 붙인다.

RFC문서로 상대URL to 절대URL 하는 알고리즘이 정의되어있다. 

## 2.4 안전하지 않은 문자

이스케이프를 통해 US-ASCII가 아닌 문자도 전송할 수 있도록 했다. (%로 시작하고 두개의 16진수 숫자로 변경. `~` -> `0x7E` 등)

인코딩하는 위치는 브라우저처럼 요청을 보내는 어플리케이션단. 서버에서 요청을 받았을때 어떤 문자가 인코딩되야하는지 불분명하기 때문이다.


## 2.6.1 URN

URN은 리소스 이름과 다른 몇가지 정보만 있어도 알아낼 수 있도록 하는 URI규칙이다. 

PURL 방식은 DNS같은 애로, 자원의 위치를 물어보면 그 자원이랑 연결될 permanent URL을 제공해준다. 

