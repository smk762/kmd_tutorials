#!/usr/bin/env python3
from lib_atomicdex import *

# Documentation: https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/my_balance.html

if len(sys.argv) > 1:
	for i in range(1,len(sys.argv)):
		coin = sys.argv[i]
		params = {"userpass":"$userpass","method":"my_balance","coin":coin}
		if len(params) > 0:
			resp = mm2_proxy(params)
			print(resp)
		else:
			print(f"{sys.argv[i]} is not a recognised coin!")
else:
	print(f"You need to add a coin (or series of coins) as a parameter")
	print(f"e.g. ./balance.py KMD BTC TKL")

