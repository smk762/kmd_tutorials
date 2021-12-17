#!/usr/bin/env python3
from lib_atomicdex import *

# Documentation: https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/my_balance.html


if os.path.exists("bot_settings.json"):
	with open("bot_settings.json", "r") as f:
		bot_settings = json.load(f)
else:
	print(f"No bot_settings.json file found!")
	print(f"Run './configure_makerbot.py' to create one.")

current_prices = requests.get(PRICES_API).json()
coins = list(set(bot_settings["buy_coins"] + bot_settings["sell_coins"]))

if len(coins) > 0:
	print("-"*169)
	print('|{:^16s}|{:^24s}|{:^24s}|{:^24s}|{:^58s}|{:^16s}|'.format(
			"Coin",
			"Unspendable balance",
			"Spendable balance",
			"Total balance",
			"Address",
			"USD Value"
		)
	)

	print("-"*169)
	total_value = 0
	for coin in coins:
		params = {"userpass":"$userpass","method":"my_balance","coin":coin}
		if len(params) > 0:
			resp = mm2_proxy(params)
			price = get_price(coin, current_prices)
			total_balance = float(resp['balance'])+float(resp['unspendable_balance'])
			value = round(total_balance * price, 2)
			total_value += value
			print('|{:^16s}|{:^24f}|{:^24f}|{:^24f}|{:^58s}|{:^16s}|'.format(
					coin,
					float(resp['balance']),
					float(resp['unspendable_balance']),
					total_balance,
					resp['address'],
					f"${value}"
				)
			)
		else:
			print(f"{coin} is not a recognised coin!")
	print("-"*169)
	print('{:>151s}|{:^16s}|'.format(
			"Total USD ",
			f"${round(total_value,2)}"
		)
	)
	print('{:>151s}{:^16s}'.format(
			"",
			"-"*18		)
	)

