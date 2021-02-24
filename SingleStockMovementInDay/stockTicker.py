import win32api
import yfinance as yf
import data as d
import time
import winsound
import random
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

price = 737
delta = 1
while current_time <= "15:30:00" and current_time >= "09:15:00":
    previousDayData = yf.download(
        "CIPLA.NS", start=d.previousDayDate, end=d.todaysDate)
    print(previousDayData['Close'][0])
    if previousDayData['Close'][0] <= price - delta:
        duration = 500  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)
        win32api.MessageBox(0, str(previousDayData['Close'][0]), 'title')
        price -= 0.5
    elif previousDayData['Close'][0] >= price + delta:
        duration = 500  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)
        win32api.MessageBox(0, str(previousDayData['Close'][0]), 'title')
        price += 0.5
    time.sleep(random.random() + 2)
if current_time > "15:30:00" or current_time < "09:15:00":
    print("Market is closed")
