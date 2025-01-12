from binance.client import Client # pip install python-binance
from dotenv import load_dotenv
import os
import time
import asyncio
import logging

# Load the .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = Client(API_KEY,API_SECRET,testnet=True)

client.get_account()

symbol = 'BTCUSDT'
buy_price: float = 94900
sell_price: float = 95000
trade_quantity = 0.001

async def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

async def place_buy_order(symbol,quantity):
    try:
        order = client.order_market_buy(symbol=symbol,quantity=quantity)
        print(f"Buy order done: {order}")
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return None        

async def place_sell_order(symbol,quantity):

    try:
        order = client.order_market_sell(symbol=symbol,quantity=quantity)
        print(f"Sell order done: {order}")
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

async def trading_bot():
    
    positioned = True

    while True:
        currency = await get_current_price(symbol)
        
        if currency is None:
            await asyncio.sleep(5)  # Retry after 5 seconds if there was an error
            continue


        print(f" {symbol} current price is {currency}")

        if positioned:
            if currency > sell_price:
                print(f"Price is {currency} placing sell order")
                await place_sell_order(symbol,trade_quantity)
                positioned = False
        else:
            if currency < buy_price:
                print(f"Price is {currency} placing buy order")
                await place_buy_order(symbol,trade_quantity)
                positioned = True

        await asyncio.sleep(30)  # Poll every 30 seconds

async def main():
    try:
        await trading_bot()
    except Exception as e:
        logging.error(f"Unexpected error in trading bot: {e}")


if __name__ == "__main__":

    asyncio.run(main())