import os, requests, json, datetime, time
from params import *

MarginData = None

# Bracket and cover order Margins calculation for Equity:
def DownloadMarginData():
    print 'Downloading Margin data from https://api.kite.trade/margins/equity'
    return requests.get('https://api.kite.trade/margins/equity').json()

def MarginCal(sym, cps, price, sl, transaction_type):
    global MarginData
    co_lower = 0
    co_upper = 0
    quantity = 1

    if 1 == 0:
	margin_cache_file = "DATA/margins.json"
	if not os.path.exists(margin_cache_file):
	    margin_data = requests.get('https://api.kite.trade/margins/equity')
	    data = margin_data.json()

	    for item in data:
		if item['tradingsymbol'] == sym:
		    co_lower = item['co_lower']
		    co_upper = item['co_upper']
		    break

	    with open(margin_cache_file, 'w') as margin_file_handle:
		json.dump(data, margin_file_handle)
		margin_file_handle.close()
	else:
	    with open(margin_cache_file, 'r') as margin_file_handle:
		data = json.load(margin_file_handle)
		margin_file_handle.close()

	    for item in data:
		if item['tradingsymbol'] == sym:
		    co_lower = item['co_lower']
		    co_upper = item['co_upper']
		    break
    elif MarginData is None:
	MarginData = DownloadMarginData()

    if MarginData:
	for item in MarginData:
	    if item['tradingsymbol'] == sym:
		co_lower = item['co_lower']
		co_upper = item['co_upper']
		break

    if co_lower == 0 or co_upper == 0:
	print '%s: Unable to find maximum margin, using regular Multiplier' % sym;
	qty = ((cps * MIS[sym]) / price)
	return qty

    co_lower = co_lower/100
    co_upper = co_upper/100

    trigger = price - (co_upper * price)

    if sl < trigger:
	sl = trigger
    else:
	trigger = sl

    x = 0
    if transaction_type == 'Buy':
	x = (price - trigger) * quantity
    else:
	x = (trigger - price) * quantity

    y = co_lower * price * quantity
    margin = x if x > y else y
    margin = margin + (margin * 0.2)

    return round(cps/margin)
