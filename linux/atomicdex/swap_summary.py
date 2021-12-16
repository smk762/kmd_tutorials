#!/usr/bin/env python3
from lib_atomicdex import *

# Documentation reference: https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/my_recent_swaps.html

# parameters: 
#	Limit (integer)
# Usage: 
#	./swap_summary.py 200 (shows summary of last 200 swaps)

# For each pair:
# PAIR | Base sent | Base recieved | Base USD | Rel sent | Rel Recieved | Rel USD | Delta



limit = 200
if len(sys.argv) > 1:
	limit = sys.argv[1]

resp = mm2_proxy({"userpass":"$userpass","method":"my_recent_swaps","limit":limit})
get_swaps_sumarised(resp)
