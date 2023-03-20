import os

service_name = ['db0_realtime_update', 'db2_realtime_update', 'db_mysql_daily_update', 'news_recommend']

what0 = input('어떤 작업을 하시겠습니까 (start/stop/enable/disable) ?')

os.system("sudo systemctl daemon-reload")
for name0 in service_name:
    os.system(f"sudo systemctl {what0} {name0}.service")
print(f"{what0} 완료")