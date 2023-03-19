#### readme #####

#설치방법
-JAVA 설치 후 JAVA_HOME 경로 등록
-python3.11 설치
-redis 서버 설치
-아래의 파이썬 라이브러리 설치
requests numpy fastapi uvicorn gensim konlpy redis mysql-connector-python

-폴더에 venv 설치 후 venv 활성화.
-mysqld 는 systemctl에서 stop 및 disable 실행.
-활성화한 채로 install_in_ubuntu.py 파일 실행

#### 구성

# API 서버는 FastAPI 프레임워크를 사용함. API 부분은 main.py에 담김.
-DB는 redis 와 mysql 을 사용함.
# redis DB는 0~3으로 구성되며 각각 역할은 다음과 같음.
db0 : 기사 일련번호(gid)와 그에 상응하는 벡터가 키-벨류 페어로 담겨있음.
db1 : 사용자 식별번호(ga)와 그에 상응하는 벡터가 키-벨류 페어로 담겨있음. 저장된 키값은 30일 후 자동 expire됨.
db2 : 추천목록 값들이 저장됨.	
	'mat' : 2000*50 매트릭스가 byte 형태로 저장됨. np.frombuffer() 을 통해 디코드. 2000개 기사의 50차원 행렬을 합친 것.
	'gid2' : mat 의 2000개 기사에 상응하는 gid 번호 리스트가 byte 형태로 저장.
	'title' :  mat 기사의 제목
	'url', 'thumurl' : mat 기사의 url과 썸네일 url.
	'temp : 사용자가 송신한 ga, gid에 해당하는 벡터가 없을 때, 아무 정보가 없는 상태에서 추천을 하기 위해 임의로 부여한 벡터. 현재 무작위 벡터를 부여하고 있으나 향후 QE 모델 등을 도입할 예정
db3 : 사용자 로그기록이 저장됨. 60분 뒤 자동 expire됨. 

# mysql DB 는 news_recommend.news_ago 테이블 한 개만 쓰임.
 약 1달치 기사를 저장하는 역할을 함. 이 데이터는 향후 모델 업데이트 트레이닝에 쓰임.
 테이블의 칼럼은 다음과 같음.
gid, createtime, title, content, url, thumburl, source : 기사 목록 API 와 같음
length : content 의 글자 수
vec : doc2vec 모델을 통해 변환한 벡터를 blob 형태로 보관.
konlpy : content에 대해 konlpy의 Okt 페키지를 통해 형태소 분석한 리스트를 blob 형태로 보관.

##### 구조
-main.py 가 API 역할을 함.
**mysql과 redis 에 대한 업데이트는 다음 파일들이 수행함
-db0_realtime_update : db0 을 업데이트. 동아닷컴API에서 2분에 한 번 기사를 받아와 새 기사를 벡터로 변환. 수정삭제를 mysql과 redis에 반영.
-db2_realtime_update : db2와 db3를 업데이트. 4분에 한번씩 db2의 추천목록(mat, title...) 데이터들이 업데이트됨. db3는 10분에 한번씩 1시간 이전 로그를 지우도록 함.
-db_mysql_daily_update : 매일 새벽 한번씩 mysql를 업데이트함. 1달이 지난 기사를 지움. 다만 동아일보를 소스로 하면서 글자 수가 1000자가 넘는 기사는 2달이 지나야 지움(모델 트레이닝에 쓰기 위함)

