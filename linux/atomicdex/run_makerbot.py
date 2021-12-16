#!/usr/bin/env python3
from lib_atomicdex import *

# Documentation reference: https://developers.komodoplatform.com/basic-docs/atomicdex-api-20-dev/start_simple_market_maker_bot.html

if os.path.exists("MM2.json"):
	with open("MM2.json", "r") as f:
		conf = json.load(f)
else:
	print("MM2.json not present - run './gen_conf.py' to create")
	sys.exit()

if os.path.exists("bot_settings.json"):
	with open("bot_settings.json", "r") as f:
		bot_settings = json.load(f)
else:
	print("bot_settings.json not present - run './configure_makerbot.py' to create")
	sys.exit()

MM2_USERPASS = conf["rpc_password"]
MM2_IP = "http://127.0.0.1:7783"
BUY_COINS = bot_settings["buy_coins"]
SELL_COINS = bot_settings["sell_coins"]
MIN_USD = bot_settings["min_usd"]
MAX_USD = bot_settings["max_usd"]
SPREAD = bot_settings["spread"]
ORDER_REFRESH_RATE = bot_settings["refresh_rate"]
PRICES_API = bot_settings["prices_api"]
PRICES_API_TIMEOUT = bot_settings["prices_api_timeout"]
USE_BIDIRECTIONAL_THRESHOLD = bot_settings["use_bidirectional_threshold"]

ACTIVATE_COMMANDS = requests.get("http://stats.kmd.io/api/atomicdex/activation_commands/").json()["commands"]

PARAMS = {
    "price_url": PRICES_API,
    "bot_refresh_rate": int(ORDER_REFRESH_RATE)	
}

CFG_TEMPLATE = {
    "base": "base_coin",
    "rel": "rel_coin",
    "min_volume": {
    	"usd":MIN_USD
    },
    "max_volume":  {
    	"usd":MAX_USD
    },
    "spread": SPREAD,
    "base_confs": 3,
    "base_nota": True,
    "rel_confs": 3,
    "rel_nota": True,
    "enable": True,
    "price_elapsed_validity": int(PRICES_API_TIMEOUT),
    "check_last_bidirectional_trade_thresh_hold": USE_BIDIRECTIONAL_THRESHOLD
}

def get_cfg(base,rel):
	cfg = CFG_TEMPLATE.copy()
	cfg.update({
	    "base": base,
	    "rel": rel,	
	})
	return cfg


configs = {}
for base in SELL_COINS:
	for rel in BUY_COINS:
		if base != rel:
			configs.update({
				f"{base}/{rel}": get_cfg(base, rel)
			})
PARAMS.update({
	"cfg":configs
})
print(json.dumps(PARAMS, indent=4, sort_keys=True))

with open('makerbot_command_params.json', 'w', encoding='utf-8') as f:
	json.dump(PARAMS, f, ensure_ascii=False, indent=4)

# activate coins
for coin in list(set(BUY_COINS + SELL_COINS)):
	for protocol in ACTIVATE_COMMANDS:
		if coin in ACTIVATE_COMMANDS[protocol]:
			print(mm2_proxy(ACTIVATE_COMMANDS[protocol][coin]))

command = {
    "userpass": MM2_USERPASS,
    "mmrpc": "2.0",
    "method": "start_simple_market_maker_bot",
    "params":PARAMS
}
# start bot
resp = mm2_proxy(command)
if 'error' in resp:
	print("You need to use the latest dev branch version of the AtomicDEX-API")
	print("run ./get_latest_mm2_dev.py")
else:
	print(resp)


