#This part of is mainly used to sell off all other crypto assets into USDT
from binance.spot import Spot as Client
import time

client = Client(base_url='https://testnet.binance.vision', api_key='FPH30yGmXVCmoun430ngOx14n2Gk0nkxcavsi55CRDrzO311cqeUCQmbbCA3CN8n', api_secret='N8rGeqsNjY6lkPZDZyzXUmNFDIlZTUuIJrgqaiP7cs6MaKs8mPObqa3vxDbIGFzO')
account_details=client.account()
account= (account_details['balances'])


for coin in account:
    try:
        symbol=coin['asset']+"USDT"
        quantity=coin['free']

        params = {
            'symbol': symbol,
            'side': 'sell',
            'type': 'MARKET',
            'quantity': quantity,
        }
        response = client.new_order(**params)
        print(response)
        if response:
            time.sleep(2)
    except:
        continue
