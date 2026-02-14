import time
import requests
import pandas as pd
import numpy as np
from telegram import Bot

TOKEN = "8286509718:AAEKAEd-hzc9U14fCkzTDtQRrqwZH1n_-r8"
CHAT_ID = "PUT_YOUR_CHAT_ID"

bot = Bot(TOKEN)

def get_price():
    # Simulated OTC feed (we replace later with real feed)
    return np.random.normal(1.2000, 0.0005)

prices = []

def rsi(data, period=14):
    delta = np.diff(data)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(period).mean()
    avg_loss = pd.Series(loss).rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

while True:
    price = get_price()
    prices.append(price)

    if len(prices) > 50:
        prices = prices[-50:]

        rsi_val = rsi(np.array(prices))[-1]

        if rsi_val < 30:
            bot.send_message(chat_id=CHAT_ID, text="📈 BUY Signal")
        if rsi_val > 70:
            bot.send_message(chat_id=CHAT_ID, text="📉 SELL Signal")

    time.sleep(60)
