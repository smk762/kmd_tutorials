#!/usr/bin/env python3
from lib_atomicdex import *

# Documentation: https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/my_balance.html

if os.path.exists("bot_settings.json"):
	with open("bot_settings.json", "r") as f:
		bot_settings = json.load(f)
else:
	print(f"No bot_settings.json file found!")
	print(f"Run './configure_makerbot.py' to create one.")

coins = list(set(bot_settings["buy_coins"] + bot_settings["sell_coins"]))

if len(coins) > 0:
	for coin in coins:
		params = {"userpass":"$userpass","method":"my_balance","coin":coin}
		if len(params) > 0:
			resp = mm2_proxy(params)
			print(resp)
		else:
			print(f"{coin} is not a recognised coin!")

