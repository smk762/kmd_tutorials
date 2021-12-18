#!/usr/bin/env python3
import os
import sys
import json
import time
import requests

if os.path.exists("MM2.json"):
  with open("MM2.json", "r") as f:
    conf = json.load(f)
    MM2_USERPASS = conf["rpc_password"]

MM2_IP = "http://127.0.0.1:7783"

PRICES_API = "https://prices.cipig.net:1717/api/v2/tickers?expire_at=600"

ERROR_EVENTS = [
  "StartFailed", "NegotiateFailed", "TakerFeeValidateFailed", "MakerPaymentTransactionFailed",
  "MakerPaymentDataSendFailed", "MakerPaymentWaitConfirmFailed", "TakerPaymentValidateFailed",
  "TakerPaymentWaitConfirmFailed", "TakerPaymentSpendFailed", "TakerPaymentSpendConfirmFailed",
  "MakerPaymentWaitRefundStarted", "MakerPaymentRefunded", "MakerPaymentRefundFailed"
  ]

def mm2_proxy(params):
  params.update({"userpass": MM2_USERPASS})
  #print(json.dumps(params))
  try:
    r = requests.post(MM2_IP, json.dumps(params))
  except requests.exceptions.RequestException as e:
    print("mm2 is not running!")
    raise SystemExit(e)
  return r.json()

def get_activate_command(coin):
  return requests.get(f"https://stats.kmd.io/api/atomicdex/activation_commands/?coin={coin}").json()


def get_swaps_sumarised(my_recent_swaps):
  swaps_summary = {
    'pairs':{},
    'totals_sent':{},
    'totals_received':{},
    'totals_delta':{}
  }

  for swap in my_recent_swaps["result"]["swaps"]:
    include_swap = True
    for event in swap["events"]:
      if event["event"]["type"] in ERROR_EVENTS:
        include_swap = False
        #print(event["event"]["type"])
        break
    if include_swap:
      my_coin = swap["my_info"]["my_coin"]
      my_amount = float(swap["my_info"]["my_amount"])
      other_coin = swap["my_info"]["other_coin"]
      other_amount = float(swap["my_info"]["other_amount"])

      if f"{my_coin}/{other_coin}" not in swaps_summary['pairs']:
        swaps_summary['pairs'].update({f"{my_coin}/{other_coin}":{
          f"{my_coin} sent":0,
          f"{other_coin} received":0
        }})
      swaps_summary['pairs'][f"{my_coin}/{other_coin}"][f"{my_coin} sent"] += my_amount
      swaps_summary['pairs'][f"{my_coin}/{other_coin}"][f"{other_coin} received"] += other_amount

      if f"{my_coin}" not in swaps_summary['totals_sent']:
        swaps_summary['totals_sent'].update({
          f"{my_coin}": 0
        })
        if f"{my_coin}" not in swaps_summary['totals_delta']:
          swaps_summary['totals_delta'].update({
            f"{my_coin}": 0
          })

      if f"{other_coin}" not in swaps_summary['totals_received']:
        swaps_summary['totals_received'].update({
          f"{other_coin}": 0
        })
        if f"{other_coin}" not in swaps_summary['totals_delta']:
          swaps_summary['totals_delta'].update({
            f"{other_coin}": 0
          })

      swaps_summary['totals_sent'][f"{my_coin}"] += my_amount
      swaps_summary['totals_received'][f"{other_coin}"] += other_amount

      swaps_summary['totals_delta'][my_coin] -= my_amount
      swaps_summary['totals_delta'][other_coin] += other_amount

    else:
      #print("skipping, swap failed")
      pass

  current_prices = requests.get(PRICES_API).json()
  print("-------------------------------------------")
  for pair in swaps_summary['pairs']:
    print(f"{pair}: {swaps_summary['pairs'][pair]}")
  print("-------------------------------------------")
  for coin in swaps_summary['totals_sent']:
    print(f"{coin} sent: {swaps_summary['totals_sent'][coin]}")
  print("-------------------------------------------")
  for coin in swaps_summary['totals_received']:
    print(f"{coin} recieved: {swaps_summary['totals_received'][coin]}")
  print("-------------------------------------------")
  total_delta = 0
  for coin in swaps_summary['totals_delta']:
    price = get_price(coin, current_prices)
    value = round(swaps_summary['totals_delta'][coin] * price, 2)
    total_delta += value
    print(f"{coin} delta: {swaps_summary['totals_delta'][coin]} (USD${value})")
  print("-------------------------------------------")
  print(f"Total Delta: USD${total_delta}")
  print("-------------------------------------------")


def get_price(coin, current_prices=None):
  if not current_prices:
    current_prices = requests.get(PRICES_API).json()
  if coin in current_prices:
    return float(current_prices[coin]["last_price"])
  else:
    return 0


def output_order_lines(ordertype, orders, current_prices=None):
  if not current_prices:
    current_prices = requests.get(PRICES_API).json()
  for uuid in orders:
    sell_coin = orders[uuid]['base']
    buy_coin = orders[uuid]['rel']
    sell_amount = float(orders[uuid]['max_base_vol'])
    sell_price_wrt_rel = float(orders[uuid]['price'])
    buy_amount = sell_amount*sell_price_wrt_rel

    sell_price_cex = get_price(sell_coin, current_prices)
    buy_price_cex = get_price(buy_coin, current_prices)

    cex_price_ratio = sell_price_cex/buy_price_cex
    pct_vs_cex = round((sell_price_wrt_rel/cex_price_ratio-1)*100,3)
    sell_price_usd = sell_price_cex*(1+pct_vs_cex/100)
    updated = orders[uuid]['updated_at']
    since = sec_to_hms(int(time.time()) - int(updated)/1000) 
    print('|{:^7}|{:^38}|{:^12}|{:^12}|{:^16}|{:^16}|{:^16}|{:^16}|{:^10}|{:^15}|'.format(
        ordertype,
        uuid,
        sell_coin,
        buy_coin,
        '{:16.8f}'.format(sell_amount),
        '{:16.8f}'.format(buy_amount),
        '{:10.2f}'.format(sell_price_usd),
        '{:10.2f}'.format(sell_price_cex),
        '{:6.2f}%'.format(pct_vs_cex),
        since
      )
    )

def sec_to_hms(sec):
  minutes, seconds = divmod(sec, 60)
  hours, minutes = divmod(minutes, 60)
  periods = [('h', hours), ('m', minutes), ('s', seconds)]
  return ' '.join('{}{}'.format(int(val), name) for name, val in periods if val)

  