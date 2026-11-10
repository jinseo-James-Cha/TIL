
지침은 매번 따라오고, 요청서(prompt)는 이번 한번만 보내짐


## 요청서 작성 형식 Prompt-template.md
#요청서
##대상 - 어느 파일이나 어느 부분을 건드리는지
##내용 - 무엇을 하는지
##하지 않을 것 - 건드리면 안되는 부분
##애매한 경우 - 판단이 안 서면 진행할지 물어보기

현재 실행을 요청하면 바로 판단->계획->실행으로 이어진다..
이걸 좀 더 체계화해서 작업하자. 어떻게?
=> 계획모드를 추가해보자.



## 계획모드
Claude —permission-mode plan

공통규칙(CLAUDE.md)에도 **여러파일을 고치거나 파일 구조를 바꾸는 작업은 계획모드로 계획을 먼저 받고 승인한 다음에 진행한다** 를 추가해준다.




## 작업 단위를 나누어 실패 위험 줄이기
한번의 프롬프트로 수많은 작업을 한번에 시킨다? 앞의 요청들은 가중치가 높기때문에 그거는 이행할 지라도 뒷쪽 업무들은 묵살되거나 대충 할 확률이 높다. 

따라서, 우리는 업무를 잘라서 요청한다. 무슨 기준으로? 아래 기준으로!

- 되돌리기: 되돌려도 손해가 적은가?
- 확인: 결과가 바로 확인되는가?
- 겹침: 겹치는 데가 없는가?

But, 점점 모델들이 좋아지고 있어서, 사실 여러개를 던져도 잘한다!

Task-list.md를 요청하여 작업목록을 체크박스로하여 진행상황과 결과를 반환받는 리스트도 같이 관리



Quiz
- What is the main purpose of the request form pattern? -> to clearly limit the scope of the changes
- Why specify what will not be done in the request? -> to prevent unnecessary modifications
- what are the three stages divided using ‘plan mode’ ? -> Judgement, Approval, Work
- What is the biggest advantage of breaking work into small units? -> to coordinate the risk of the failure scope
- What is the primary purpose of checkbox-based task list management? -> to visually manage the progress of the work

