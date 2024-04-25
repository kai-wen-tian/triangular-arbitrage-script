#This part of code is to get all symbols of Bybit.
from pybit.unified_trading import HTTP

session = HTTP(
    testnet=True,
    demo=True,
    api_key="HUdme6LlSe7KfRDu2y",
    api_secret="LQUsN0y6j9e43GyOhk37ynHb2fCjgPayNfu0",
)

coinInfo = session.get_tickers(
    category="spot",
)

coinSpotInfo = coinInfo["result"]["list"]

symbols = [coin["symbol"] for coin in coinSpotInfo]

print(symbols)
print(len(symbols))
