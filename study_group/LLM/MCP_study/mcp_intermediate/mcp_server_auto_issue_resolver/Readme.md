# 1. 목적

이슈를 자동으로 해결해서 PR을 제작해주는 MCP를 제작하고 싶었다
처음에는 단순하게 아래같은 프롬프트를 사용했는데, 너무 형편없는 PR을 생성했다. 이슈도 해결 못하고, project구조도 망가뜨렸다. 

```
            이슈 본문의 상황을 정리한다음 해당 이슈번호가 123이면 "feature/#123" 처럼 이슈번호를 붙인 이름의 브랜치를 생성해줘.   
            먼저 ddl.sql 등 sql들을 조회해서 테이블간의 관계를 파악해줘.  
            %s 페이지에 @issue-tracker 라고 쓰여진 커멘트들의 조건에 맞춰서 하나의 커밋마다 하나의 세부 이슈를 풀 수 있도록 해.
            %s 이슈 링크를 매 커밋의 prefix로 [https://...] xxxx 해결, xxxx 추가  등으로 붙여줘.
            만약, 특정 API의 결과값이 어떤 형식인지 알고 싶다거나, 요청해야할 API주소가 있다면 물어봐줘. 
            DB에 접근하는 repository는 storageService에서만 사용해야해.             
            PR 올리기 전에는 ./gradlew ktlintFormat ./gradlew ktlintCheck ./gradlew test 를 순차적으로 진행한 다음에 PR을 올려야 해. 
            %s 레포에 새로운 PR로 만들어줘. base branch는 develop이야 프로젝트에 PR 템플릿이 있다면 해당 템플릿 양식을 지켜줘
            PR 본문에서 %s 이슈를 멘션 걸도록 하고, 이슈의 제목 앞에는 [AI-AUTOFIX] prefix를 붙여줘.                      
```

# 2. 문제점

