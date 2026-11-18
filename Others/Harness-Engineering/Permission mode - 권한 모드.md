
# mode
- Manual - 바뀌는것, 필요한것 하나하나 물어봄
- AcceptEdits - 파일 여러 개를 고치는 반복 작업, 명령만
- Plan - 범위가 큰 작업. 전체를 보고 승인
- Auto - 물어보지않고 AI의 판단으로 자동 선택

### Sandbox
- 프로젝트 내에서만 작업이 이루어지고, 그 외 폴더나 파일은 못건드리게 범위를 제안함
- 터미널 명령어에 대한 범위를 격리 시킨다.


프로젝트 전체 세팅 settings.json
나만의 세팅 settings.local.json


### 클로드가 사용하는 input
1. 사용자가 요청하는 채널
2. 클로드가 읽어오는 웹서치, 서류등등 데이터 채널 - 프롬프트 인젝션 문제가 발생할 수 있다.


Quiz
1. What is the primary purpose of blocking irreversible commands through a hook?
- preventing unpredictable risks
2. What are the main configuration items typically addressed in allowlist-and denylist-based access control?
- Blocking bash commands and protecting secrets
3. What criteria does the sandbox use to restrict the scope of terminal command access?
- path






