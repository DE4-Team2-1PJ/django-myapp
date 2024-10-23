[프로그래머스 데이터 엔지니어링 데브코스 4기] 과정에서 진행한 프로젝트입니다.
크롤한 웹데이터로 만들어보는 시각화 웹 서비스를 구현하였습니다.


# 👨‍🏫 프로젝트 소개
---
Web Scraping 을 활용하여 "데이터 직무 채용공고 통합 서비스"를 주제로 한 웹서비스입니다. 데이터 직무로 취업을 희망하는 구직자를 위한 취업공고 통합플랫폼을 제작해보았습니다.

# ⏲️ 개발 기간
---
2024.10.14(월) ~ 2024.10.17(목)

# 🧑‍🤝‍🧑 개발자 소개
---
강혜진 : 크롤링, 프론트엔드
김신웅 : 크롤링, 백엔드
김정희 : 크롤링, 보고서 작성
김태현 : 크롤링, 데이터 전처리
박진경 : 크롤링, 프론트엔드
이민지 : 크롤링, 결과물 소개서 작성
유영천 : 크롤링, 데이터 시각화
추민재 : 크롤링, 데이터 시각화

# 📝 프로젝트 아키텍처
---
![1](https://github.com/user-attachments/assets/e689ecac-2b5f-4dfe-b569-c28b85227235)


# 📌 주요 기능
---
![2](https://github.com/user-attachments/assets/970fc596-c4e3-41c8-8be9-65cd114f6836)

![3](https://github.com/user-attachments/assets/965b4e73-bc59-4ad9-9de9-b6e670169484)

![4](https://github.com/user-attachments/assets/060ae000-5f0a-44a0-8d0f-a60e64127787)


# django-myapp 프로젝트 환경 설정
---
### 1. 프로젝트 클론하기
```
$ git clone https://github.com/DE4-Team2-1PJ/django-myapp.git
$ cd django-myapp
```
### 2. 가상 환경 설정
가상 환경을 설정하려면, 아래 명령어를 사용하여 가상 환경을 생성하고 활성화하세요.
#### Windows (cmd) 의 경우
```
$ python -m venv venv
$ venv\Scripts\activate
```
#### Windows (PowerShell) 의 경우
```
$ python -m venv venv
$ .\venv\Scripts\Activate
```
#### Mac/Linux 의 경우
```
$ python3 -m venv venv
$ source venv/bin/activate
```

### 3. 필수 패키지 설치
requirements.txt에 명시된 모든 패키지를 설치하려면, 아래 명령어를 입력하세요 (가상환경에 설치하세요):
```
$ pip install -r requirements.txt
```

### 4. 데이터베이스 마이그레이션
데이터베이스 테이블을 생성하려면 다음 명령어를 실행하세요 (가상환경에서 하세요):
```
$ python manage.py migrate
```
### 5. 서버 실행
프로젝트 서버를 실행하려면, 아래 명령어를 입력하세요 (가상환경에서 하세요):
```
$ python manage.py runserver --noreload
```

### 6. 브라우저에서 페이지 확인
브라우저에서 http://127.0.0.1:8000/recruits 접속
![image](https://github.com/user-attachments/assets/e2c132de-a736-4622-add3-7a9c2bc5c073)


# 최종 결과물 링크
---
[결과물 소개 문서] : https://xn--2--i41iy10c9op.my.canva.site/
[프로젝트 보고서] : https://www.notion.so/11d6e9180a968129aebee7f824959f69
