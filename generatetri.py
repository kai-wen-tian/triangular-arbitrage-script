import ccxt
import json
import time
exchange = ccxt.binance()

markets = exchange.load_markets()

ticker_data = {}
for pair in markets:
    filterPair = pair.split(":")
    try:
        ticker = exchange.fetch_ticker(filterPair[0])
        pair_bid = ticker['bid']
        pair_ask = ticker['ask']
        #print(pair_bid)
        if pair_bid is not None and pair_ask is not None:
            #print("STH"+str(pair_bid))
            print(filterPair[0])
            ticker_data[filterPair[0]] = ticker
    except ccxt.BadSymbol:
        #print(f"Symbol {filterPair[0]} is not supported on {exchange.id}. Skipping...")
        continue

with open("filename.txt", "w") as file:
    for key in markets.keys():
        file.write(key + "\n")


with open("filename2.txt", "w") as file:
    for key in ticker_data.keys():
        file.write(key + "\n")

print(len(markets))
print(len(ticker_data))

triangular_relationships = set()

exclude_currencies=['FDUSD','BRL','USDT','DAI','USDC','TUSD','BUSD','AUD','EUR','GBP','PLN','RON','TRY','UAH','VND','ZAR','BULL','BEAR','JPY',"INR"]
for pair1 in ticker_data:
    currencies1 = pair1.split('/')
    if currencies1[1] in ['FDUSD', 'BTC', 'ETH', 'USDT', 'USDC']:
        #print(currencies1[1])
        for pair2 in ticker_data:    
            currencies2 = pair2.split('/')
            if pair1 != pair2 and all(currency not in currencies2 for currency in exclude_currencies) and currencies1[0] in currencies2:
                for pair3 in ticker_data:
                    currencies3 = pair3.split('/')
                    if (pair3 != pair1 and pair3 != pair2 and currencies3[1] == currencies1[1]) \
                        and (currencies3[0] in {currencies2[0], currencies2[1]}):
                               triangular_relationships.add((pair1,pair2,pair3))

output_data = {"triangular_relationships": list(triangular_relationships)}

if triangular_relationships:
    #print("Triangular relationships found:")
    with open('triangular_relationships.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=4)
else:
    print("No triangular relationships found.")
