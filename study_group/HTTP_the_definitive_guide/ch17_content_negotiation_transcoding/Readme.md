# 17장 내용 협상과 트랜스 코딩
하나의 URL이 여러 리소스에 대응할 필요가 있는 경우가 있음.

- 클라이언트 주도 협상
  - 클라이언트에게 서버가 선택지 줌
- 서버 주도 협상
  - 서버가 클라이언트 요청 헤더 검증해서 버전 선택
- 투명한 협상
  - 프락시 캐시가 서버 대신해 협상


# 17.2 클라이언트 주도 협상
- 각 페이지에 두번 요청 필요
- 여러개 URL 필요 (언어별)

# 17.3 서버 주도 협상
클라이언트가 아래 헤더들로 선호 정보 보내준다.
- Accept
- Accept-Language
- Accept-Charset
- Accept-Encoding

서버한테 quality value를 붙여서 전달하면 여러 언어중에 뭘로 보내줄 지 결정한다. 

User Agent를 보고 판단할 수 도 있다.

캐시는 서버의 특정 헤더 선호도를 Vary 헤더라는 것을 통해 받는다.

## 17.3.4 아파치의 내용 협상

type map파일을 만들어서 특정 파일에 대해서 특정 파일 응답할 수 있게 해준다.


# 17.4 투명 협상
서버가 Vary 헤더로 중개자(프락시)에게 내용협상할 때 어떤 헤더 사용하는 지 알려준다. 

캐시는 서버의 의사결정 로직을 가급적 많이 사용해야 하는데, 결국 클라이언트의 Accept 헤더에 매핑되는 서버의 파일을 저장하면 되는 문제
- 여러 variant , alternate가 생긴다 (같은 URL이지만 client header에 따라 여러 문서 캐싱)

그렇기 때문에 vary 헤더에 있는 클라이언트 헤더를 체크해서 variant를 만들면 된다.

Vary: User-Agent, Cookie

# 17.5 트랜스코딩

서버가 클라이언트 요구에 맞는 문서가 없다면 

- 포맷 변환
  - html을 WML로 변환하기도
    - 이런걸 정적으로 생성해둔다면, 서버측은 작은 변화에 대해서도 여러 파일을 만들고, 페이지 관리하기도 어렵다. 
- 정보 합성
  - 문서에서 정보의 요점을 추출
- 콘텐츠 주입
  - 자동 광고 생성
  - 사용자 추적 시스템
