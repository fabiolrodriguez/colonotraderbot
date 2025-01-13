from apscheduler.schedulers.asyncio import AsyncIOScheduler # pip install apscheduler
from binance.client import Client # pip install python-binance
from dotenv import load_dotenv # pip install python-dotenv
import os
import time
import asyncio
import logging
import json


# Load the .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

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
buy_price: float = 94900
sell_price: float = 95000
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
    
    positioned = load_state()  # Load the state from the JSON file
    print(f"Loaded positioned: {positioned}")

    currency = await get_current_price(symbol)
    
    if currency is None:
        await asyncio.sleep(5)  # Retry after 5 seconds if there was an error
        
    print(f"{symbol} current price is {currency}")

    if positioned:
        if currency > sell_price:
            print(f"Price is {currency} placing sell order")
            await place_sell_order(symbol,trade_quantity)
            positioned = False
            save_state(positioned)            
    else:
        if currency < buy_price:
            print(f"Price is {currency} placing buy order")
            await place_buy_order(symbol,trade_quantity)
            positioned = True
            save_state(positioned)

async def main():

    # Initialize the scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(trading_bot, 'interval', seconds=30)
    print("Starting bot...")
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to exit.")
    
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":

    asyncio.run(main())
