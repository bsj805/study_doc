# 설치방법
https://orangecake.tistory.com/37
먼저 clause-desktop을 설치한다.
https://claude.ai/download



https://github.com/makenotion/notion-mcp-server

일단 여기를 따라하면서 using docker 부분을 참조했다.

~/Library/Application\ Support/Claude/claude_desktop_config.json

```
{
  "mcpServers": {
    "notionApi": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e", "OPENAPI_MCP_HEADERS",
        "mcp/notion"
      ],
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\":\"Bearer ntn_****\",\"Notion-Version\":\"2022-06-28\"}"
      }
    }
  }
}
```

이걸 추가하면, claude desktop app을 껐다켰을때부터 integration이 활성화된다.

notion의 integration key를 계속 저 docker에게 보내게된다. 지금 아래같은 docker가 떠있다.

```
CONTAINER ID   IMAGE                                 COMMAND                   CREATED              STATUS              PORTS                                                                 
3c53bfee6b9a   mcp/notion                            "notion-mcp-server"       About a minute ago   Up About a minute
```


![img.png](img.png)

나는 아래같은 링글 복습페이지를 만들어서, 피드백 받은 내용을 정리했는데, 이에 대한 액세스 권한을 얻고자한다.

![img_1.png](img_1.png)


![img_2.png](img_2.png)

근데 이런 똥.. length limit에 걸려서 큰 작업은 못하나보다. 
그냥 한 페이지만 읽어와서 요약해달라고 해야겠다.

![img_4.png](img_4.png)

최상단에 써달라구 했는데, 최하위에 써줬다. 아휴.. 

![img_3.png](img_3.png)


대충 느낌은 알겠다. ai가 api를 통해 notion에 접근해서, 페이지를 읽어오고, 그 내용을 요약해달라고 요청하는 것이다.

근데 length limit에 걸리는걸 생각해보면, multi turn으로 접근해야 하는데, 이런건 langchain같은걸로 풀어서 진행되도록 하면 좋겠다. 

일단 claude desktop app을 통해서 notion과 연결하는건 성공했다. 다만 claude llm model을 써야하니까 이게 별로다.

그리고 공식 mcp 깃허브는 https://github.com/modelcontextprotocol/servers 여기다. 