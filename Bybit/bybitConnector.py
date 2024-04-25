#How to do buy and sell in Bybit
from pybit.unified_trading import HTTP


session = HTTP(
    testnet=True,
    demo=True,
    api_key="HUdme6LlSe7KfRDu2y",
    api_secret="LQUsN0y6j9e43GyOhk37ynHb2fCjgPayNfu0",
)
"""
print(session.get_coin_info(
    coin="ETH",
))
"""
print(session.place_order(
    category="spot",
    symbol="LTCETH",
    side="sell",
    orderType="Market",
    qty="50",
))

"""
print(session.get_executions(
    category="spot",
    limit=1,
    orderId="1670419312944614656",
)) 
"""