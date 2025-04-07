import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import numpy as np
import time
import telegram
from datetime import datetime

# Define your Telegram Bot token and chat ID
TELEGRAM_TOKEN = "your-telegram-bot-token"
CHAT_ID = "your-chat-id"

# Function to send messages to Telegram
def send_telegram_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Function to fetch data and calculate indicators
def get_data(symbol, period="1d", interval="1m"):
    data = yf.download(symbol, period=period, interval=interval)
    data["RSI"] = ta.rsi(data["Close"], length=14)
    data["EMA"] = ta.ema(data["Close"], length=9)
    return data

# Function to calculate the signal
def generate_signal(data):
    if data["RSI"].iloc[-1] > 70 and data["Close"].iloc[-1] < data["EMA"].iloc[-1]:
        return "SELL"
    elif data["RSI"].iloc[-1] < 30 and data["Close"].iloc[-1] > data["EMA"].iloc[-1]:
        return "BUY"
    else:
        return "HOLD"

# Main Streamlit App
def app():
    st.title("Quotex Signal Bot")

    st.write("This is a simple Quotex Signal Bot that sends buy/sell signals based on technical analysis.")

    symbol = st.text_input("Enter asset symbol", "EURUSD=X")
    period = st.selectbox("Select Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])
    interval = st.selectbox("Select Interval", ["1m", "5m", "15m", "30m", "1h"])

    if st.button("Get Signal"):
        data = get_data(symbol, period, interval)
        signal = generate_signal(data)
        st.write(f"Generated Signal: {signal}")

        # Send signal to Telegram
        send_telegram_message(f"Signal for {symbol}: {signal}")

# Run the Streamlit app
if __name__ == "__main__":
    app()
