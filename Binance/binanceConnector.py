#How to do buy and sell using binance api
from binance.spot import Spot as Client

client = Client(base_url='https://testnet.binance.vision', api_key='FPH30yGmXVCmoun430ngOx14n2Gk0nkxcavsi55CRDrzO311cqeUCQmbbCA3CN8n', api_secret='N8rGeqsNjY6lkPZDZyzXUmNFDIlZTUuIJrgqaiP7cs6MaKs8mPObqa3vxDbIGFzO')

#print(client.time())


print(client.account())


params = {
    'symbol': 'BTCUSDT',
    'side': 'sell',
    'type': 'MARKET',
    'quantity': 0.1,
}

response = client.new_order(**params)
print(response)