from apscheduler.schedulers.asyncio import AsyncIOScheduler # pip install apscheduler
from binance.client import Client # pip install python-binance
from dotenv import load_dotenv # pip install python-dotenv
from telegram import Bot
import os
import time
import asyncio
import logging
import json


# Load the .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MESSAGE = ''
# Set safe checks count
checks = 0
checks_treshold = 3

## Save the position on json file
STATE_FILE = "state.json"

def save_state(positioned):
    """Save the positioned value to a JSON file."""
    state = {"positioned": positioned}
    with open(STATE_FILE, "w") as file:
        json.dump(state, file)

def load_state():
    """Load the positioned value from a JSON file."""
    try:
        with open(STATE_FILE, "r") as file:
            state = json.load(file)
            return state.get("positioned", False)  # Default to False if key doesn't exist
    except FileNotFoundError:
        return False  # Default if file doesn't exist
###
        

client = Client(API_KEY,API_SECRET,testnet=True)

client.get_account()

symbol = 'BTCUSDT'
buy_price: float = 103000
sell_price: float = 104000
trade_quantity = 0.001

async def get_current_price(symbol):
    ticker = await asyncio.to_thread(client.get_symbol_ticker, symbol=symbol)
    return float(ticker['price'])

async def place_buy_order(symbol,quantity):
    try:
        order = await asyncio.to_thread(client.order_market_buy, symbol=symbol, quantity=quantity)
        print(f"Buy order done: {order}")
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return None        

async def place_sell_order(symbol,quantity):

    try:
        order = await asyncio.to_thread(client.order_market_sell, symbol=symbol, quantity=quantity)
        print(f"Sell order done: {order}")
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

async def trading_bot():

    global MESSAGE
    global checks
    global checks_treshold
    
    positioned = load_state()  # Load the state from the JSON file
    print(f"Loaded positioned: {positioned}")

    currency = await get_current_price(symbol)

    if currency is None:
        await asyncio.sleep(5)  # Retry after 5 seconds if there was an error
        
    print(f"{symbol} current price is {currency}")

    if positioned:
        if currency > sell_price:
            if checks < checks_treshold:
                print(f"Price is {currency} setting checks: {checks}")
                checks = checks + 1
                MESSAGE = f"Price is {currency} setting checks: {checks}"
                await send_telegram_message(TOKEN, CHAT_ID, MESSAGE)
            else:
                print(f"Price is {currency} placing sell order")
                await place_sell_order(symbol,trade_quantity)
                positioned = False
                checks = 0
                save_state(positioned)
                MESSAGE = f"Price is {currency} placing sell order"
                await send_telegram_message(TOKEN, CHAT_ID, MESSAGE)
    else:
        if currency < buy_price:
            if checks < checks_treshold:
                print(f"Price is {currency} setting checks: {checks}")
                checks = checks + 1
                MESSAGE = f"Price is {currency} setting checks: {checks}"
                await send_telegram_message(TOKEN, CHAT_ID, MESSAGE)
            else:                        
                print(f"Price is {currency} placing buy order")
                await place_buy_order(symbol,trade_quantity)
                positioned = True
                checks = 0
                save_state(positioned)
                MESSAGE = f"Price is {currency} placing buy order"
                await send_telegram_message(TOKEN, CHAT_ID, MESSAGE)

# Telegram notifcations

async def send_telegram_message(token, chat_id, message):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)

# End of telegram notifications

async def main():

    # Initialize the scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(trading_bot, 'interval', seconds=30)
    print("Starting bot...")
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to exit.")
    MESSAGE = "Bot iniciado"
    await send_telegram_message(TOKEN, CHAT_ID, MESSAGE)    
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":

    asyncio.run(main())
