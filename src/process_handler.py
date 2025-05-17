from time import sleep
import psutil
while True:
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            print(f"Name: {proc.info['name']}, Path: {proc.info['exe']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    sleep(10)