# Colono Trader bot

This is a simple python bot with a logic to buy and sell crypto using Binance API.

## Usage

First step you need to create an API key on Binance, following the [documentation](https://www.binance.com/en/support/faq/how-to-create-api-keys-on-binance-360002502072)

The, create a .env file and fill with your API_KEY and API_SECRET

```
API_KEY='YOUR KEY'
API_SECRET = 'YOUR SECRET'
```

Install required libraries

```
pip install apscheduler python-binance python-dotenv
```

Configure the requested crypto, buy and sell price on the code.

```python
symbol = 'BTCUSDT'
buy_price: float = 94900
sell_price: float = 95000
trade_quantity = 0.001
```

And run

```
$ python colonotrader.py 
Starting bot...
Scheduler started. Press Ctrl+C to exit.
```

Modify to fill your needs