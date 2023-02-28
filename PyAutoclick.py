import time
import pyautogui
import ntplib
from datetime import datetime
import os


def left_click_at_time(hour, minute, delay):
    
    c = ntplib.NTPClient()
    response = c.request('time2.kriss.re.kr', version=3)

    t = datetime.fromtimestamp(response.orig_time)
    print(t.strftime("%a %b %d %H:%M:%S.%f"))
    wait = (hour - int(t.strftime("%H")))*3600 + (minute- int(t.strftime("%M")))*60 - int(t.strftime("%S")) - float(t.strftime("%f"))/1000000
    print("%.3f sec" %wait)
    time.sleep(wait+delay)
    
    c = ntplib.NTPClient()
    response = c.request('time2.kriss.re.kr', version=3)

    t = datetime.fromtimestamp(response.orig_time)
    print(t.strftime("%a %b %d %H:%M:%S.%f"))
    pyautogui.click()
    print("클릭 완료")
    print(t.strftime("%a %b %d %H:%M:%S.%f"))

    input("Press enter to Continue")

while True:
    hour = int(input("시: "))
    minute = int(input("분: "))
    delay = float(input("ms: "))/1000
    left_click_at_time(hour, minute, delay)
    os.system("cls")
