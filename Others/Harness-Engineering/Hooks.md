Claude 의 Claude.md나 다른 세팅들은 “권고사항”이였다. 그 말은 즉, 가끔은 실행을 안할수도, 혹은 안했지만 했다고 판단을 내리는 경우가 생긴다. 이 오류는 치명적일 수 있다. 믿을 수 있는 정보를 가지고(규격) 작업이 실행, 검토, 재실행의 루프를 완성해야 하네스 엔지니어링의 의미가 있다고 보기 때문이다.
따라서, Claude에서는 Hooks라는 기능에 기반하여 작업이 수행되고 각각의 수행에 미리 정의된 hooks를 붙여 실행을 컨트롤 할 수 있어진다.

### 작동 방식
1. Claude code에서 이벤트 발생(파일수정, 명령어 실행, 세션 종료)
2. 설정된 Hook확인
3. 등록된 작업 자동 실행(shell script, http, mcp, prompt등등)
4. 결과에 따라 후속 처리(실행, 재실행, 기록, 승인등등)

핵심은 설정된 이벤트가 실행되면 그에 맞는 hooks가 실행된다는 점.


### 주요 hook event
	Hook event        실행 시점.       활용 예시
- SessionStart -               세션 시작.                Git 상태 불러오기(fetch, pull..)
- UserPromptSubmit.      프롬프트 제출.         요청 전 검증
- PreToolUse                      도구 실행 직전.       위험한 명령어 차단.                    
- PostToolUse.                  도구 실행 직후.         자동 포매팅
- PermissionRequest.       권한 요청 직전.       권한 처리
- Stop.                                Claude 응답종료.    테스트 및 완료 검증
- SubagentStop.              Subagent작업종료.  결과 검증
- PreCompact.                  컨텍스트 압축 직전.    중요 정보 백업



