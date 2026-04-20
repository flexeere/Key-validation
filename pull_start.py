import paramiko
import sys

host = '103.124.208.21'
user = 'advps'
password = '93jVJS7l1k6g'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=password, timeout=10)
    
    cmd = "cd ~/Key-validation && git pull && echo '93jVJS7l1k6g' | sudo -S docker-compose up -d --build"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out: print("STDOUT:\n", out)
    if err: print("STDERR:\n", err)
    
except Exception as e:
    pass
finally:
    ssh.close()
