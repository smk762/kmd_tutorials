#!/usr/bin/env python3
import json
from lib_atomicdex import *

# Documentation reference: https://developers.komodoplatform.com/basic-docs/atomicdex-api-20-dev/start_simple_market_maker_bot.html

resp = "N"
while resp not in ["Y", "y"]:
	sell_coins = input("Enter tickers of coins you want to sell, seperated by a space:\n")
	buy_coins = input("Enter tickers of coins you want to buy, seperated by a space:\n")
	min_usd =  input("Enter minimum trade value in USD (e.g. 10): ")
	max_usd =  input("Enter maximum trade value in USD (e.g. 100): ")
	spread =  input("Enter spread percentage (e.g. 5): ")
	refresh_rate =  input("How often to update prices in seconds (e.g. 180): ")

	makerbot_conf = {
		"sell_coins": sell_coins.split(" "),
		"buy_coins": buy_coins.split(" "),
		"min_usd": int(min_usd),
		"max_usd": int(max_usd),
		"spread": 1+(float(spread)/100),
		"refresh_rate": refresh_rate,
		"prices_api": PRICES_API,
		"prices_api_timeout": 180,
		"use_bidirectional_threshold": True,
	}

	print(json.dumps(makerbot_conf, indent=4))
	resp = input("Confirm configuration? [Y/N]: ")

with open("bot_settings.json", "w+") as f:
	json.dump(makerbot_conf, f, indent=4)

print("bot_settings.json file created.")
print("execute './run_makerbot.py' to start trading")
