# 윈티드 프리온보딩 2차 5주차 개인과제

<div style="display: flex; align-items: flex-start; justify-content: center;">
    <img style="padding-right: 5px" align=top src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=green"/>
    <img style="padding-right: 5px" align=top src="https://img.shields.io/badge/bcrypt-4C4A73?style=flat-square"/>
    <img style="padding-right: 5px" align=top src="https://img.shields.io/badge/MySQL-005C84?style=flat-square&logo=mysql&logoColor=white"/>
    <img style="padding-right: 5px" align=top src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=flat-square&logo=redis&logoColor=white"/>
    <img align="top" src="https://img.shields.io/badge/JWT-000000?style=flat-square&logo=JSON%20web%20tokens&logoColor=white"/>
</div>

> ⚠️ 현재 프로젝트는  DJango와 자체 설계된 Architecture 위에 구현이 진행되고 있습니다. 아직 구현 초기에 Architecture 마저 
> 리펙토링을 수행하지 않았으므로 코드 컨벤션이 심각하게 난잡한 상태 입니다.

**상태: 진행중 (30%)**
  * **사용자 CRUD (40%)**
    * 사용자 인증 및 생성 (100%)
    * 사용자 RUD (0%)
  * **회사 데이터 CRUD (20%)**
    * Model 설계 (100%)
    * View Interface 구현 (90%)
    * 인증 추가 (10%)
    * 실구현 (0%)
  * Dockerizing (0%, 선택)

아래 노션 버튼을 클릭하면 프로젝트에 대한 자세한 내용을 볼 수 있습니다. (작성중)

[![](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)](https://plum-bearberry-96a.notion.site/2-5-Wanted-b2e5b68dbf354f6cb604ce6d966c5e4b)


## 개요

회사 데이터를 생성하고 언어에 따른 회사 검색을 수행합니다.

## 요구 사항
### 기존 요구 사항
#### 필수
* 회사명 자동완성
  * 회사명의 일부만 들어가도 검색이 되어야 합니다.
* 회사 이름으로 회사 검색
* 새로운 회사 추가
* 이때 검색 결과는 언어에 따라 달라야 합니다.
#### 선택
* Dockerising 및 배포
### 자체 설정된 요구 사항
* 계정 시스템 추가
  * 회사 데이터를 관리하려면 로그인을 해야 합니다.
  * 로그인 여부는 jwt로 구분합니다.
  * 회원 가입을 할 때, 이메일과 6자리 인증 코드로 인증을 한 다음 계정을 생성합니다.
  * 계정 타입은 다음과 같습니다.
    * Client: 회사 정보 검색만 가능합니다.
    * CompanyClient: 회사를 추가/수정 또는 제거할 수 있습니다. 단 이는 자신이 만든 회사 데이터에 한합니다.
    * Admin: 모든 권한을 가지고 있습니다.
* 회사 검색 기능 추가
  * 복수개의 Tag 단위로 검색해야 합니다.


## 개인 목표

#### 최대한 기술을 긁어모아서 제대로 된 서버 구현하기
* 단순 구현이 아닌 사용자 인증, 캐싱 같은 될 수 있는 기술들을 최대한 모아서
* 안전하고 견고한 어플리케이션 구현하기

#### Frontend(ReactJS) 까지 추가해서 완벽한 Web Applicaion 배포
* Frontend까지 구현해서 완전한 Web개발

#### DJango 기반의 자체 Architecture/Framework 설계 및 구현과 그 위에서 구현하기
* 객체지향적인 설계가 목표
* 개인 프로젝트로 Flask/FastAPI 기반의 아키텍쳐 솔루션 패키지인 flanaria가 진행 중이며 해당 프로젝트는 flanaria 프로젝트의 초석이 될 예정

## Directory Structure
```tree
├─access
│  ├─tests
│  └─utils
├─company
│  ├─tests
│  └─utils
├─user
│  ├─tests
│  └─utils
├─core
│  └─miniframework_on_django        
└─config
```
* access: 사용자 인증과 관련된 app 입니다.
  * 기능
    * 회원 가입
    * 로그인
* company: 회사 CRUD 관련 기능을 가지는 app 입니다.
  * 기능
    * 기본 CRUD
    * 회사 검색 (연관 검색, 태그 등..)
* user: 사용자 관련 app 입니다.
  * 기능
    * 사용자 프로필 수정
    * 탈퇴
    * 사용자 프로필 검색
* config: 
* core/miniframework_on_django
  * DJango위에 설계된 자체 Architecture 입니다. 범용성을 목표로 하고 있기 때문에 해당 프로젝트에만 국한되는 것이 아닌 다른 프로젝트에서도 적용이 되게 설게/구현하고 있습니다.


## 사용된 기술

### bcypt
패스워드를 저장할 때 해당 라이브러리르 사용해 패스워드를 암호화 해서 저장합니다.

### Redis

In-Memory Database, 즉 캐시 시스템 입니다. 해당 시스템의 사용 용도는 처음 사용자가 회원 가입 또는 패스워드를 찾을 때 이메일 인증 코드를 요청하는데,
이에 대한 정보를 RDB가 아닌 캐시에 저장합니다. 해당 데이터를 저장할 때 TTL을 저장하여 일정 시간이 지나면 캐시에서 자동으로 코드가 사라지게 되므로
자동으로 만료가 됩니다.




## DB Models
![](readme-assets/DatabaseDiagram.png)


## 자체 Architecture
(작성중)

## UML

> 일부분은 구현이 안되어 있거나 개발이 중단되었습니다.

> 설명은 자체 Architecture에 대한 설명과 Document가 완성되면 추가로 작성할 예정입니다.

<details>
<summary>UML 보기</summary>
<div>

![](readme-assets/uml.png)

</div>
</details>