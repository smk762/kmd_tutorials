#!/usr/bin/env python3
from lib_atomicdex import *

# Documentation: https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/my_orders.html

current_prices = requests.get(PRICES_API).json()
params = {"userpass":"$userpass","method":"my_orders"}
resp = mm2_proxy(params)
if 'result' in resp:
	if 'maker_orders' in resp['result']:
		maker_orders = resp['result']['maker_orders']
	if 'taker_orders' in resp['result']:
		taker_orders = resp['result']['taker_orders']
else:
	print(f"Error: {resp}")
	sys.exit()

print("-"*169)
print('|{:^7}|{:^38}|{:^12}|{:^12}|{:^16}|{:^16}|{:^16}|{:^16}|{:^10}|{:^15}|'.format(
		"Type",
		"UUID",
		"Sell Coin",
		"Buy Coin",
		"Sell Amount",
		"Buy Amount",
		"DEX Price USD",
		"CEX Price USD",
		"% vs CEX",
		"Updated"
	)
)

print("-"*169)
output_order_lines("Maker", maker_orders, current_prices)
output_order_lines("Taker", taker_orders, current_prices)

print("-"*169)
print('{:>152}|{:^15}|'.format(
		"Order count ",
		f"{len(maker_orders)+len(taker_orders)}"
	)
)
print('{:>152}{:^16}'.format(
		"",
		"-"*17)
)

