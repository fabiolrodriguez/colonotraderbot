from binance.client import Client # pip install python-binance

import time

API_KEY = 'GmsOPS1Yla8MwwjZocqBDHx0mpGM0D7OvwNIE6piVE5Zd3M7nCQby5GJWjOQMPvU'
API_SECRET = '6cky0lImAuEsWDilUBevcRCBOjW9tBSuHRMbS53Z04t7noPGCORAgo8PHfBVjXU1'

client = Client(API_KEY,API_SECRET,testnet=True)

client.get_account()

symbol = 'BTCUSDT'
buy_price: float = 93000
sell_price: float = 100000
trade_quantity = 0.001

def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def place_buy_order(symbol,quantity):

    order = client.order_market_buy(symbol=symbol,quantity=quantity)
    print(f"Buy order done: {order}")

def place_sell_order(symbol,quantity):

    order = client.order_market_sell(symbol=symbol,quantity=quantity)
    print(f"Sell order done: {order}")    


def trading_bot():
    
    positioned = False

    while True:
        currency = get_current_price(symbol)

        print(f" {symbol} current price is {currency}")

        if positioned:
            if currency > sell_price:
                print(f"Price is {currency} placing sell order")
                print(place_sell_order(symbol,trade_quantity))
                positioned = False
        else:
            if currency < buy_price:
                print(f"Price is {currency} placing buy order")
                print(place_buy_order(symbol,trade_quantity))
                positioned = True

        time.sleep(30)

if __name__ == "__main__":

    trading_bot()   