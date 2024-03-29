# git clone
# venv 설치.
# database.py 만들기
# pip install requests numpy fastapi uvicorn gensim konlpy redis mysql-connector-python
# venv activate 후 install_in_ubuntu.py 실행

sure = input("###  news_recommend를 설치하시겠습니까? (y/n) :")
if sure == 'n':
    exit()
sure = input("git cone, venv 설치, pip install 완료 후 venv activate 했습니까? (y/n) :")
if sure == 'y':
    import os
    import sys
    import subprocess

    ### 자바 설치
    
    os.system("pip3.11 install requests numpy fastapi uvicorn gensim konlpy redis mysql-connector-python")
    os.system("sudo apt install openjdk-8-jdk")
    output = subprocess.run(['which','java'], stdout=subprocess.PIPE).stdout.decode().strip()
    os.system(f"export JAVA_HOME={output}")

    ### database.py 작성
    working_dir = os.getcwd()
    text0 = """
import mysql.connector

config = {
'user' : 'root',
'password': 'dlftks44#',
'host' : 'dongailboars-rds.cluster-cr2zqjzbyiqo.ap-northeast-2.rds.amazonaws.com',
'port' : '3306'
}
    """
    sure = input(f"{text0} \n=========\n이 내용이 맞습니까? 아니라면 인스톨 파일을 수정하세요. (y/n)")
    with open(working_dir + '/database.py', "w") as f:
        f.write(text0)
    print('database.py 생성 완료')

    #### redis DB 초기화
    import redis
    from redis import ConnectionPool

    for i in range(6):
        pool = ConnectionPool(host='localhost', port=6379, db=i)
        r = redis.Redis(connection_pool=pool)
        r.flushdb()
    print("redis db 초기화 완료")

    ####### 모델, DB 생성
    import create_db_and_table
    import crawl_30
    import model_build
    import make_proto_redis

    print('### 모델 및 데이터베이스 생성 완료. systemctl 스크립트 설치 ###')

    import time

    service_name = ['db0_realtime_update', 'db2_realtime_update', 'db_mysql_daily_update', 'main']

    for name0 in service_name:
        name0 = 'news_recommend' if name0 == 'main' else name0
        service_config = f"""[Unit]
Description= {name0}

[Service]  
User=donga
WorkingDirectory={working_dir}
Environment="PATH={sys.prefix}/bin"
ExecStart={sys.executable} {working_dir}/{name0}.py
Restart=always

[Install] 
WantedBy=multi-user.target 
""".replace('\\', '/')

        service_file = f"/etc/systemd/system/{name0}.service"
        with open(service_file, "w") as f:
            f.write(service_config)
        time.sleep(1)
        os.system("sudo systemctl daemon-reload")
        os.system(f"sudo systemctl start {name0}.service")
        os.system(f"sudo systemctl enable {name0}.service")
        print(f"{name0} systemctl 작성, start, enable 완료")
        #####
print("news_recommend 설치완료")