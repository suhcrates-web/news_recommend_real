import sys
import os

print(sys.executable)   # 파이썬 파일
print(sys.prefix)

cwd = os.getcwd()
print(cwd)   # working directory

print(os.path.abspath(__file__))  # running file


#
# service_name = ['db0_realtime_update', 'db2_realtime_update', 'db_mysql_daily_update', 'news_recommend']
#
# working_dir =os.getcwd()
# for name0 in service_name:
#     service_config =f"""
# [Unit]
# Description= {name0}
#
# [Service]
# User=donga
# WorkingDirectory={working_dir}
# Environment="PATH={sys.prefix}"
# ExectStart={sys.executable} {working_dir}/{name0}.py
# Restart=always
#
# [Install]
# WantedBy=multi-user.target
# """
#
#     service_file = f"/etc/systemd/systme/{name0}.service"
#     with open(service_file, "w") as f:
#         f.write(service_config)
#
#     os.system("sudo systemctl daemon-reload")
#     os.system(f"sudo systemctl start {name0}.service")
#     os.system(f"sudo systemctl enable {name0}.service")
