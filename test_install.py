import os
import sys

working_dir =os.getcwd()
name0='test0'
service_config = f"""[Unit]
Description= test

[Service]  
User=donga
WorkingDirectory={working_dir}
Environment="PATH={sys.prefix}/bin"
ExectStart={sys.executable} {working_dir}/{name0}.py
Restart=always

[Install] 
WantedBy=multi-user.target 
""".replace('\\', '/')

service_file = f"/etc/systemd/system/{name0}.service"
with open(service_file, "w") as f:
    f.write(service_config)

os.system("sudo systemctl daemon-reload")
os.system(f"sudo systemctl start {name0}.service")
os.system(f"sudo systemctl enable {name0}.service")