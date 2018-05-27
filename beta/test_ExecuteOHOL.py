#!/usr/bin/env python2.7

from __future__ import division

import os, sys, datetime, time
import urllib2, csv, multiprocessing
from kiteconnect.connect import KiteConnect
import logging

OHOL_PATH="%s" % os.getcwd()
sys.path.append(OHOL_PATH)

from credentials import API_KEY, API_SECRET_KEY
from test_ohol import FindOHOLStocks, LoadPastData, MIS, PastData, TODAY, Vol5_buffer, Vol_buffer, VolInc
from ConnectKite import GetKiteToken

# Important parameters
CAPITAL=14000
#cap=CAPITAL*(80/100) # 80% of whole capital
cap=CAPITAL
SLPct=(1.2/100)
ProfitPct=(1.2/100)
TSLPct=(0.5/100)

DRY_RUN=False

def GetTicks(price):
    tgt=round(0.05 * round(float(price * ProfitPct)/0.05), 2)
    sl=round(0.05 * round(float(price * SLPct)/0.05), 2)
    tsl=round(0.05 * round(float(price * TSLPct)/0.05), 2)
    return (tgt, sl, tsl)

def GetAbsolutes(price):
    tgt=round(float(price * ProfitPct))
    sl=round(float(price * SLPct))
    tsl=round(float(price * TSLPct))
    if tsl == 0:
        tsl=1
    return (tgt, sl, tsl)

def PlaceOrder(call, sym, rprice, Orders):
    # Derive price to buy/sell from recommended price
    price = round(float(rprice), 2)

    numberOfStocks = int((cps*int(MIS[sym]))/price)

    # Get Ticks values for SqOff, SL, and Trailing SL used for BO
    (tgt, sl, tsl) = GetAbsolutes(price)

    # Place a BO order
    if (call == 'Buy'):
	if DRY_RUN:
	    print "Buy %d %s @ %d" % (numberOfStocks, sym, rprice)
	else:
	    try:
		order_id = kite.place_order(tradingsymbol=sym,
	                                exchange=kite.EXCHANGE_NSE,
	                                transaction_type=kite.TRANSACTION_TYPE_BUY,
	                                quantity=numberOfStocks,
	                                order_type=kite.ORDER_TYPE_LIMIT,
	                                product=kite.PRODUCT_MIS,
	                                variety=kite.VARIETY_BO,
	                                price=price,
	                                squareoff=tgt,
	                                stoploss=sl,
	                                trailing_stoploss=tsl
	                                )
		OrderDetails = [price, tgt, sl, tsl]
		Orders[order_id] = OrderDetails
		print >>fhandle, "Buy[%s]: OrderId=%s, Price=%.2f, TGTTick=%.2f, SLTick=%.2f, TSLTick=%.2f" % (sym, str(order_id), Orders[order_id][0], Orders[order_id][1], Orders[order_id][2], Orders[order_id][3])
	    except Exception as e:
		print >>fhandle, "Buy Order placement failed: {}".format(e)
		print >>fhandle, "Failed to place buy order for  %d %s @ %d" % (numberOfStocks, sym, rprice)
		logging.info("Buy Order placement failed: {}".format(e))
    elif (call == 'Sell'):
	if DRY_RUN:
	    print "Sell %d %s @ %d" % (numberOfStocks, sym, rprice)
	else:
	    try:
		order_id = kite.place_order(tradingsymbol=sym,
	                                exchange=kite.EXCHANGE_NSE,
	                                transaction_type=kite.TRANSACTION_TYPE_SELL,
	                                quantity=numberOfStocks,
	                                order_type=kite.ORDER_TYPE_LIMIT,
	                                product=kite.PRODUCT_MIS,
	                                variety=kite.VARIETY_BO,
	                                price=price,
	                                squareoff=tgt,
	                                stoploss=sl,
	                                trailing_stoploss=tsl
	                                )
		OrderDetails = [price, tgt, sl, tsl]
		Orders[order_id] = OrderDetails
		print >>fhandle, "Sell[%s]: OrderId=%s, Price=%.2f, TGTTick=%.2f, SLTick=%.2f, TSLTick=%.2f" % (sym, str(order_id), Orders[order_id][0], Orders[order_id][1], Orders[order_id][2], Orders[order_id][3])
	    except Exception as e:
		print >>fhandle, "Sell Order placement failed: {}".format(e)
		print >>fhandle, "Failed to place sell order for %d %s @ %d" % (numberOfStocks, sym, rprice)
		logging.info("Sell Order placement failed: {}".format(e))

if __name__ == '__main__':
    if len(sys.argv) > 1 and '--test' in sys.argv:
	DRY_RUN=True

    if not DRY_RUN:
	order_info_file = "/home/somasm/GITRepo/PythonTrade/beta/Orders/%s.orders" % TODAY
	fhandle = open(order_info_file, 'w')
	kite = KiteConnect(api_key=API_KEY)

	session_token = ''
	AutoFetch=True
	if AutoFetch == True:
	    try_count=1
	    while try_count < 6:
		try:
		    print >>fhandle, "GetKiteToken(): Attempt %d" % try_count
		    session_token = GetKiteToken()
		    if session_token is None or session_token == '':
			try_count+=1
		    else:
			break;
		except:
		    try_count+=1
	else:
	    raw_input('Add token to token file')
	    token_file = "/Users/somasm/Pangu/ZD-Auto/PythonTrade/beta/token"
	    with open(token_file, 'r') as token_file_handle:
		session_token = token_file_handle.readlines()[0].strip()
		token_file_handle.close()

	print >>fhandle, "RequestToken=%s" % session_token

	# Redirect the user to the login url obtained
	# from kite.login_url(), and receive the request_token
	# from the registered redirect url after the login flow.
	# Once you have the request_token, obtain the access_token as follows.
	data = kite.generate_session("%s"%session_token, api_secret=API_SECRET_KEY)
	kite.set_access_token(data["access_token"])

	if len(sys.argv) > 1 and '--test' not in sys.argv:
	    while True:
		tdt = datetime.datetime.today()
		min = int(tdt.strftime("%M"))
		if min > 1:
		    break
		time.sleep(2)

    (BuySyms, SellSyms) = FindOHOLStocks()
    
    if (len(BuySyms.keys())+len(SellSyms.keys())) > 0:
        jobs1 = []
        manager = multiprocessing.Manager()

        cps = int(cap/(len(BuySyms.keys())+len(SellSyms.keys())))

	PARALLEL=False
	if PARALLEL:
	    if(len(BuySyms.keys())>0):
		BuyOrders = manager.dict()
		for bsym in BuySyms.keys():
		    p = multiprocessing.Process(target=PlaceOrder, args=('Buy', bsym, BuySyms[bsym], BuyOrders))
		    jobs1.append(p)
		    p.start()

	    if(len(SellSyms.keys())>0):
		SellOrders = manager.dict()
		for ssym in SellSyms.keys():
		    p = multiprocessing.Process(target=PlaceOrder, args=('Sell', ssym, SellSyms[ssym], SellOrders))
		    jobs1.append(p)
		    p.start()

	    for proc in jobs1:
		proc.join()
	else:
	    syms = ['NSE:'+sym for sym in BuySyms.keys()] + ['NSE:'+sym for sym in SellSyms.keys()]
	    cmps = kite.ltp(syms)
	    if(len(BuySyms.keys())>0):
		BuyOrders = {}
		for bsym in BuySyms.keys():
		    c1 = float(BuySyms[bsym][0])
		    vcpt = int(BuySyms[bsym][1])
		    cmp = float((cmps['NSE:%s'%bsym])['last_price'])
		    if (vcpt > 5 and (cmp+(cmp*Vol5_buffer)) > c1) or (vcpt > VolInc and (cmp+(cmp*Vol_buffer)) > c1):
			bprice = cmp+(cmp*(0.1/100))
			PlaceOrder('Buy', bsym, bprice, BuyOrders)

	    if(len(SellSyms.keys())>0):
		SellOrders = {}
		for ssym in SellSyms.keys():
		    c1 = float(SellSyms[ssym][0])
		    vcpt = int(SellSyms[ssym][1])
		    cmp = float((cmps['NSE:%s'%ssym])['last_price'])
		    if (vcpt > 5 and (cmp-(cmp*Vol5_buffer)) < c1) or (vcpt > VolInc and (cmp-(cmp*Vol_buffer)) < c1):
			sprice = cmp-(cmp*(0.1/100))
			PlaceOrder('Sell', ssym, sprice, SellOrders)

