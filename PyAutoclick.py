from tkinter import *
import time
import pyautogui
import ntplib
from datetime import datetime
import os

tk = Tk()
tk.title("{PyAutoclick}")
tk.config(bg="#2c3e50")

TimeEntry = Entry(tk)
TimeEntry.bind("<Return>", lambda event: Run())

TimeLabel = Label(tk)
WaitLabel = Label(tk)
ResultLabel = Label(tk)

TimeLabel.config(text = "Current Time", fg="#2ecc71", bg="#2c3e50", font=("Times New Roman", 20))
WaitLabel.config(text = "Wait Time", fg="#2ecc71", bg="#2c3e50", font=("Times New Roman", 20))
ResultLabel.config(text = "", fg="#2ecc71", bg="#2c3e50", font=("Times New Roman", 20))

TimeLabel.pack(side = TOP)
TimeEntry.pack(side = TOP)
WaitLabel.pack(side = TOP)
ResultLabel.pack(side = TOP)

width = 450
height = 150

x = (tk.winfo_screenwidth() // 2) - (width // 2) - 35
y = (tk.winfo_screenheight() // 2) - (height // 2) - 35

tk.geometry("{}x{}+{}+{}".format(width, height, x, y))

def Run():
    InputTime = str(TimeEntry.get())
    hour = int(InputTime[0:2])
    minute = int(InputTime[2:])
    c = ntplib.NTPClient()
    response = c.request('time2.kriss.re.kr', version=3)
    t = datetime.fromtimestamp(response.orig_time)
    TimeLabel.config(text = t.strftime("Current Time %H:%M:%S.%f"))
    wait = (hour - int(t.strftime("%H")))*3600 + (minute- int(t.strftime("%M")))*60 - int(t.strftime("%S")) - float(t.strftime("%f"))/1000000
    WaitLabel.config(text = f"Wait Time {wait} sec")
    tk.update()
    time.sleep(wait-0.1)
    pyautogui.click()
    response = c.request('time2.kriss.re.kr', version=3)
    t = datetime.fromtimestamp(response.orig_time)
    ResultLabel.config(text = (t.strftime("%H:%M:%S.%f")+"에 클릭 완료."))

TimeEntry.focus()

tk.mainloop()
