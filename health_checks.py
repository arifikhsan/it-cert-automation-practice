import os
import shutil
import psutil
import socket
from emails import generate_error_report, send_email

def check_cpu_usage():
    usage = psutil.cpu_percent(1)
    return usage < 80

def check_disk_usage(disk):
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20

def check_available_memory():
    available_memory = psutil.virtual_memory().available/(1024*1024)
    return available_memory > 500

def check_localhost():
    localhost = socket.gethostbyname('localhost')
    return localhost == '127.0.0.1'

to_be_checked = {
    check_cpu_usage(): "CPU usage is over 80%",
    check_disk_usage("/"): "Available disk space is less than 20%",
    check_available_memory(): "Available memory is less than 500MB",
    check_localhost(): "localhost cannot be resolved to 127.0.0.1"
}

error = False
for action, message in to_be_checked.items():
    if not action:
        error_message = message
        error = True

if error:
    try:
        sender = "automation@example.com"
        receiver = "{}@example.com".format(os.environ.get('USER'))
        subject = "Error - {}".format(error_message)
        body = "Please check your system and resolve the issue as soon as possible"
        message = generate_error_report(sender, receiver, subject, body)
        send_email(message)
        print('test')
    except NameError:
        pass
