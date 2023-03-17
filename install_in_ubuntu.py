
# git clone
# venv 설치
# venv activate 후 install_in_ubuntu.py 실행


#######
# import create_db_and_table
# import crawl_30
# import model_build
# import make_proto_redis

print('### 모델 및 데이터베이스 생성 완료. systemctl 스크립트 설치 ###')

import os
import sys
service_name = ['db0_realtime_update', 'db2_realtime_update', 'db_mysql_daily_update', 'news_recommend']

working_dir =os.getcwd()
for name0 in service_name:
    service_config =f"""[Unit]
Description= {name0}

[Service]  
User=donga
WorkingDirectory={working_dir}
Environment="PATH={sys.prefix}"
ExectStart={sys.executable} {working_dir}/{name0}.py
Restart=always

[Install] 
WantedBy=multi-user.target 
""".replace('\\','/')

    service_file = f"/etc/systemd/systme/{name0}.service"
    service_file = f"/home/donga/projects/{name0}.service"
    with open(service_file, "w") as f:
        f.write(service_config)

    # os.system("sudo systemctl daemon-reload")
    # os.system(f"sudo systemctl start {name0}.service")
    # os.system(f"sudo systemctl enable {name0}.service")