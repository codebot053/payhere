# payhere 

### 💻 과제 소개

    고객은 본인의 소비내역을 기록/관리 하고 싶다.
    아래의 요구사항을 만족하는 DB 테이블과 REST API를 설계하라.

**요구사항**
 - [x] 1. 고객은 email 비밀번호 입력을 통해서 회원 가입을 할 수 있다. 
 - [x] 2. 고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있다.
3. 고객은 로그인 이후 가계부 관련 안래 행돌을 할 수 있다.   
    - [x] a. 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있다.  
    - [x] b. 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있다.  
    - [x] c. 가계부에서 삭제를 원하는 내역은 삭제 할 수 있다.  
    - [x] d. 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있다.  
    - [x] e. 가계부에서 상세한 세부내역을 볼 수 있다.  
    - [ ] f. 가계부의 세부 내역을 복제할 수 있다.  
    - [ ] g. 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있다. (단축 URL은 특정 시간뒤에 만료되어야 한다.)  
- [x] 4. 로그인 하지 않은 고객은 가계부 내역에 대한 접근 제한 처리가 되어야 한다.  

### 📐 구현 및 설계

**사용 기술 및 프레임워크**
- **Language & Framework**: Python, Django
- **Database**: MySQL 5.7
- **Third party**: DRF, django-rest-framework-simplejwt, Black

**ERD**

<iframe width="560" height="315" src='https://dbdiagram.io/embed/63c3e664296d97641d79bb5e'> </iframe>


**API EndPoint**

|Index|URI|Method|Description|
|:---|:---|:---|:---|
|1|{ServiceRoot}/signup/|POST|회원가입|
|2|{ServiceRoot}/login/|POST|로그인|
|3|{ServiceRoot}/logout/|POST|로그아웃|
|4|{ServiceRoot}/moneybook/|POST|메모 생성|
|5|{ServiceRoot}/moneybook/|GET|메모 리스트 조회|
|6|{ServiceRoot}/moneybook/\<int:log_id>/|GET|메모 세부내역 조회|
|7|{ServiceRoot}/moneybook/\<int:log_id>/|PUT|메모 수정|
|8|{ServiceRoot}/moneybook/\<int:log_id>/|DELETE|메모 삭제|
|9|{ServiceRoot}/moneybook/\<int:log_id>/duplication/|POST|특정 메모 세부내역 복제|


**API document**
https://documenter.getpostman.com/view/21365815/2s8ZDU5j5Q#95f4e8f8-1eb0-4913-bc19-321eac40d052


**구현하며 든 생각들**

- 가계부의 상세 기록에 접근하는 URI의 `Path Variable`을 해당 콜렉션 자원의 id(PK)로 접근한다면 각 유저마다 작성한 가계부 기록이 예상가능할지 에 대한 고민이 들었습니다. 
- 위의 고민을 해결하기 위해 각 유저마다 카운트 되는 id(log_id)을 MoneyBookLog 테이블의 칼럼으로 두고 해당 id를 통해 자원에 접근할 수 있도록 구현하였습니다.