# Python-and-DB-Applications

### 기능
- 선수 검색 기능
    - 팀명, 포지션, 출신국
        - 팀명의경우, TEAM 테이블에 있는 팀명으로 나열되고, 사용자가 특정 팀을 선택할수있음.
        - 포지션과 출신국의 경우, PLAYER 테이블에 나오는 모든 값이 나열되고, 사용자가 특정 값을 선택할수있음.
        - 팀명, 포지션, 출신국에 “ALL“ 이라는 값이 있어야 함. 이 값을 선택하면, 메뉴의 모든 값에 대한 검색 결과가 출력됨. 이 값이 초기값, 즉 default value 로 세팅되어야 함.
        - 포지션의 경우, NULL은 메뉴와 출력에 모두 “미정“으로 나타냄.
        - 출신국의 경우, NULL은 메뉴와 출력에 모두 “대한민국”으로 나타냄.
    - 키, 몸무게
        - 사용자의 입력을 받음.(정수값으로 입력. 정수가 아니면 재입력 메시지 출력하고 재입력 받음)
        - 디폴트는 이 검색 조건은 사용하지 않는 것으로 함.
    - AND 기능
        - 팀명, 포지션, 출신국, 키, 몸무게에서 두 개 이상의 조건을 세팅하고 검색버튼을 누르면, 세팅된 조건들이 AND 연산으로 실행됨.
        
- 파일 출력 기능
    - CSV, JSON, XML 파일 중 선택된 파일을 출력하는 기능.
        - CSV의 경우, 테이블 컬럼명을 파일의 첫 줄에 먼저 기록함.
        - XML의 경우, 루트 엘리먼트는 “TABLE”,  레코들들은 “ROW”라는 엘리먼트로 함. 각각의 속성값은 ROW 엘리먼트의 attribute로 표현함.
    - 포지션, 출신국이 NULL인 경우, 파일에는 각각 “미정“, “대한민국”으로 출력함.
    - 생성된 파일은 프로그램이 실행되는 폴더에 저장함.
    
- UI의 기능
    - Main window에 layout 기능을 적용하여, 윈도우 크기가 변할때 내부의 widget 크기도 따라서 변할 수 있어야함.

### 구현 이미지
    
선수 검색 기능             |  파일 출력 기능
:-------------------------:|:-------------------------:
![AND연산](https://user-images.githubusercontent.com/55051191/148059107-139b39ce-f5a6-42d1-b437-329df83dc77e.png)  |  ![대표이미지](https://user-images.githubusercontent.com/55051191/148059091-1bf19b7d-4ad9-4f40-8692-67d66e9a8d17.png)
 
