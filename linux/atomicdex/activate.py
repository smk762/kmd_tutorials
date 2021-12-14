#!/usr/bin/env python3
from lib_atomicdex import *

if len(sys.argv) > 1:
	for i in range(1,len(sys.argv)-1):
		params = get_activate_command(sys.argv[i])
		if len(params) > 0:
			resp = mm2_proxy(params)
		else:
			print(f"{sys.argv[i]} is not a recognised coin!")
