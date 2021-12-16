#!/usr/bin/env python3
from lib_atomicdex import *

if len(sys.argv) > 1:
	for i in range(1,len(sys.argv)):
		params = get_activate_command(sys.argv[i])
		if len(params) > 0:
			resp = mm2_proxy(params)
			print(resp)
		else:
			print(f"{sys.argv[i]} is not a recognised coin!")
else:
	print(f"You need to add a coin (or series of coins) as a parameter")
	print(f"e.g. ./activate.py KMD BTC TKL")
