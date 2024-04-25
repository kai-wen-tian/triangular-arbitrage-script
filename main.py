import json
import ccxt
import schedule
import time

exchange = ccxt.binance({})

def calculate_buy_or_sell(pair1, pair2, coin1, pair2_sell_price, pair2_buy_price, fee_percentage_pair):
        coin_pair1=pair1.split("/")
        coin_pair2=pair2.split("/")
        if coin_pair1[0] == coin_pair2[0]:
            coin2 = (coin1 * pair2_sell_price) * (100 - fee_percentage_pair) / 100
        elif coin_pair1[0] == coin_pair2[1]:
            coin2 = (coin1 / pair2_buy_price) * (100 - fee_percentage_pair) / 100
        return coin2

def calculate_profit(pair1, pair2, pair3):
        
        ticker1 = exchange.fetch_ticker(pair1)
        ticker2 = exchange.fetch_ticker(pair2)
        ticker3 = exchange.fetch_ticker(pair3)

        pair1_sell_price = ticker1['bid']
        pair1_buy_price = ticker1['ask']

        pair2_sell_price = ticker2['bid']
        pair2_buy_price = ticker2['ask']

        pair3_sell_price = ticker3['bid']
        pair3_buy_price = ticker3['ask']

        fee_percentage_pair = 0.075

        quoteCurrency = pair1.split("/")[1]

        if 'ETH' in quoteCurrency or 'BTC' in quoteCurrency:
            pair0 = quoteCurrency + '/USDT'

            ticker0 = exchange.fetch_ticker(pair0)

            pair0_sell_price = ticker0['bid']
            pair0_buy_price = ticker0['ask']

            coin0 = (1000 / pair0_buy_price) * (100 - fee_percentage_pair) / 100

            coin1 = calculate_buy_or_sell(pair0, pair1, coin0, pair1_sell_price, pair1_buy_price,
                                           fee_percentage_pair)

            coin2 = calculate_buy_or_sell(pair1, pair2, coin1, pair2_sell_price, pair2_buy_price,
                                          fee_percentage_pair)
            coin3 = (coin2 * pair3_sell_price) * (100 - fee_percentage_pair) / 100

            coin4 = (coin3 * pair0_sell_price) * (100 - fee_percentage_pair) / 100

            return coin4
        else:
            coin1 = (1000 / pair1_buy_price) * (100 - fee_percentage_pair) / 100

            coin2 = calculate_buy_or_sell(pair1, pair2, coin1, pair2_sell_price, pair2_buy_price,
                                          fee_percentage_pair)

            coin3 = (coin2 * pair3_sell_price) * (100 - fee_percentage_pair) / 100

            return coin3


def trade_execution(symbol,side,quantity):
    from pybit.unified_trading import HTTP
    session = HTTP(
        testnet=True,
        demo=True,
        api_key="HUdme6LlSe7KfRDu2y",
        api_secret="LQUsN0y6j9e43GyOhk37ynHb2fCjgPayNfu0",
    )

    order=(session.place_order(
        category="spot",
        symbol=symbol,
        side=side,
        orderType="Market",
        qty=quantity,
    ))
    if order:
         return (session.get_executions(
              category="spot",
              limit=1,
              orderId=order["orderID"],
))
    


def trade_preprocessing(pair1,pair2,pair3):
    coin_pair1=pair1.split("/")
    coin_pair2=pair2.split("/")
    coin_pair3=pair3.split("/")

    coin1=trade_execution(coin_pair1[0]+coin_pair1[1],"Buy",1000)
    if coin_pair1[0] == coin_pair2[0]:
         coin2=trade_execution(coin_pair2[0]+coin_pair2[1],"Buy",coin1["execQty"])
    elif coin_pair1[0] == coin_pair2[1]:
         coin2=trade_execution(coin_pair2[0]+coin_pair2[1],"Sell",coin1["execQty"])
    coin3=trade_execution(coin_pair3[0]+coin_pair3[1],"Sell",coin2["execQty"])

    print(coin3)
    
def main():
    print("Running script...")

    with open('triangular_relationships.json', 'r') as file:
        data = json.load(file)

    counter=0
    for relationship in data['triangular_relationships']:
        try:
            counter=counter+1
            pair1 = relationship[0]
            pair2 = relationship[1]
            pair3 = relationship[2]
            coin = calculate_profit(pair1, pair2, pair3)
            if coin > 1000:
                print("Trade Found")
                print(f"Triangular relationship: {pair1} -> {pair2} -> {pair3}")
                print(coin)
                #break
            else:
                print("Trade Not Found")
                print(f"Triangular relationship: {pair1} -> {pair2}-> {pair3}")
                print(coin)
                #break
        except:
            continue

    print(counter)
    print("Script finished.")

main()

"""
schedule.every(2).minutes.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
"""