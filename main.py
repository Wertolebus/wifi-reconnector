#   РАБОТАЕТ ТОЛЬКО С WIFI
#
#   Программа запускает цикл который каждую секунду получает 1 пакет от google.com
#   Если пакет не был получен запускается функция перезапуска сети
#   Логи сохраняются в /logs/


import time
import os
from datetime import datetime

now = datetime.now()

start_time = now.strftime("%Y-%m-%d--%H-%M-%S")

run = True
DEV_MODE = False
SSID = "ASUS"       # Можно посмотреть на сайте роутера
INTERFACE = "WiFi"  # Можно посмотреть в настройках 

set_mode = int(input("1. DEBUG\n2. Standart\n==> ")) # Включение режима разработчика
if set_mode == 1:
    DEV_MODE = True
elif set_mode == 2:
    DEV_MOVE = False

def reconnect():    # функция перезапуска интернета
    if DEV_MOVE:
        os.system('cmd /c "netsh wlan show networks"')      # анализ всех сетей
        os.system("netsh interface show interface")         # анализ всех сетей со стороны интерфейса
    os.system(f'netsh wlan disconnect interface="WiFi"')    # отключение от интернета по названию интерфейса
    os.system(f'''cmd /c "netsh wlan connect name=ASUS"''') # подключение к интернету по ssid роутера
    
    # Создание логов #
    with open(f'logs/{start_time}.log', 'a') as logfile:
        logfile.write(f'{datetime.now().strftime("%H-%M-%S")} - Network Reloaded\n')
    logfile.close()
    ##################
    time.sleep(3)
def check_ping():           # проверка пинга
    hostname = "google.com" # Хост для проверки пинга
    response = os.system("ping -n 1 {}".format(hostname))

    if response == 0:       # если интернет есть:
        pingstatus = "\nNetwork Active"

        # Создание логов #
        with open(f'logs/{start_time}.log', 'a') as logfile:
            logfile.write(f'{datetime.now().strftime("%H-%M-%S")} - Network Active\n')
        logfile.close()
        ##################
        
    else:                # если интернета нету:
        pingstatus = "\nNetwork Error"
        
        # Создание логов #
        with open(f'logs/{start_time}.log', 'a') as logfile:
            logfile.write(f'{datetime.now().strftime("%H-%M-%S")} - Network Error\n')
        logfile.close()
        ##################
        
        reconnect()
        

    print(pingstatus)   # вывод
while run:              # Цикл
    os.system("cls")    # очистка консоли
    pingstatus = check_ping()
    if DEV_MODE:
        os.system('cmd /c "netsh wlan show networks"')  # анализ всех сетей
    time.sleep(1)
