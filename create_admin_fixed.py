import paramiko
import sys

host = '103.124.208.21'
user = 'advps'
password = '93jVJS7l1k6g'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=password, timeout=10)
    
    cmd_django = 'from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username="admin").delete(); User.objects.create_superuser("admin", "admin@flexeere.net", "FlexeereAdmin@2026")'
    
    cmd = f"cd ~/Key-validation && echo '93jVJS7l1k6g' | sudo -S docker-compose exec -T web python manage.py shell -c '{cmd_django}'"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    exit_status = stdout.channel.recv_exit_status()
    print("STDOUT:", stdout.read().decode('utf-8', errors='replace'))
    print("STDERR:", stderr.read().decode('utf-8', errors='replace'))
    print("EXIT STATUS:", exit_status)
    
except Exception as e:
    pass
finally:
    ssh.close()
