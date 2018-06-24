#!/usr/bin/env python2.7

from __future__ import division

import os, sys, datetime, time
import urllib2, csv, multiprocessing
from kiteconnect.connect import KiteConnect
import pandas as pd
from StringIO import StringIO

MY_MOD_PATH="%s" % os.getcwd()
sys.path.append(MY_MOD_PATH)

from credentials import API_KEY, API_SECRET_KEY
from ohol import FindOHOLStocks, LoadPastData, MIS, PastData, TODAY, Vol5_buffer, Vol_buffer, VolInc
from ConnectKite import GetKiteToken
from params import *

Interval = 60
DRY_RUN=False

def log_it(log_str):
    print("%s: %s" % (datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), log_str))

Tick=(5/100)
def RoundToTick(price):
    return round(price/Tick)*Tick

def GetAbsolutes(price):
    tgt=RoundToTick((float(price) * ProfitPct))
    sl=RoundToTick((float(price) * SLPct))
    tsl=RoundToTick((float(price) * TSLPct))
    if tsl < 1:
        tsl=1
    return (tgt, sl, tsl)

def GetNiftyScrips(n):
    try:
	url='https://www.nseindia.com/content/indices/ind_nifty%dlist.csv' % n
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0')
	response = urllib2.urlopen(req)
	return pd.read_csv(StringIO(response.read()), usecols=[2]).values.flatten()
    except:
	return []

def PlaceOrder(call, sym, rprice, Orders):
    # Derive price to buy/sell from recommended price
    price = round(float(rprice), 2)

    numberOfStocks = int((cps*int(MIS[sym]))/price)

    # Get Ticks values for SqOff, SL, and Trailing SL used for BO
    (tgt, sl, tsl) = GetAbsolutes(price)

    # Place a BO order
    if (call == 'Buy'):
	if DRY_RUN:
	    log_it("Buy %d %s @ %d" % (numberOfStocks, sym, rprice))
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
		log_it("Buy[%s]: OrderId=%s, Price=%.2f, TGT=%.2f, SL=%.2f, TSL=%.2f" % (sym, str(order_id), Orders[order_id][0], Orders[order_id][1], Orders[order_id][2], Orders[order_id][3]))
	    except Exception as e:
		log_it("Buy Order placement failed: {}".format(e))
		log_it("Failed to place buy order for %d Qty of %s @ %d (Price=%.2f, TGT=%.2f, SL=%.2f, TSL=%.2f)" % (numberOfStocks, sym, rprice, Orders[order_id][0], Orders[order_id][1], Orders[order_id][2], Orders[order_id][3]))
    elif (call == 'Sell'):
	if DRY_RUN:
	    log_it("Sell %d %s @ %d" % (numberOfStocks, sym, rprice))
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
	                                trailing_stoploss=0
	                                )
		OrderDetails = [price, tgt, sl, tsl]
		Orders[order_id] = OrderDetails
		log_it("Sell[%s]: OrderId=%s, Price=%.2f, TGTPoints=%.2f, SLPoints=%.2f, TSLPoints=%.2f" % (sym, str(order_id), Orders[order_id][0], Orders[order_id][1], Orders[order_id][2], Orders[order_id][3]))
	    except Exception as e:
		log_it("Sell Order placement failed: {}".format(e))
		log_it("Failed to place sell order for %d Qty of %s @ %d (Price=%.2f, TGT=%.2f, SL=%.2f, TSL=%.2f)" % (numberOfStocks, sym, rprice, Orders[order_id][0], Orders[order_id][1], Orders[order_id][2], Orders[order_id][3]))

if __name__ == '__main__':
    log_it("--------------------------------START---------------------------------")
    if len(sys.argv) > 1 and '--test' in sys.argv:
	DRY_RUN=True

    # Get Nifty100
    Nifty100 = GetNiftyScrips(100)
    if Nifty100 is None or len(Nifty100) == 0:
	log_it("Using static Nifty100 list")
	Nifty100.extend(Nifty100Static)

    kite = KiteConnect(api_key=API_KEY)
    session_token = ''
    AutoFetch=True
    if AutoFetch == True:
	try_count=1
	while try_count < 6:
	    try:
		log_it("GetKiteToken(): Attempt %d" % try_count)
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

    log_it("Got the RequestToken, %s" % session_token)

    # Redirect the user to the login url obtained
    # from kite.login_url(), and receive the request_token
    # from the registered redirect url after the login flow.
    # Once you have the request_token, obtain the access_token as follows.
    data = kite.generate_session("%s"%session_token, api_secret=API_SECRET_KEY)
    kite.set_access_token(data["access_token"])

    if len(sys.argv) == 1 or '--test' not in sys.argv:
	log_it("Waiting until 9:18")
	while True:
	    tdt = datetime.datetime.today()
	    hr = int(tdt.strftime("%H"))
	    min = int(tdt.strftime("%M"))
	    if hr == 9:
		if min > 17:
		    break
		else:
		    time.sleep(8)
	    else:
		break # You could be running after market hours

    log_it("Calling FindOHOLStocks()")
    (BuySyms, SellSyms, SkipSyms) = FindOHOLStocks()
    
    if (len(BuySyms.keys())+len(SellSyms.keys())) > 0:
        jobs1 = []
        manager = multiprocessing.Manager()

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
		    o1 = float(BuySyms[bsym][0])
		    vcpt = float(BuySyms[bsym][1])
		    cmp = float((cmps['NSE:%s'%bsym])['last_price'])
		    if (vcpt >= 5 and (cmp+(cmp*Vol5_buffer)) > o1) or (vcpt >= VolInc and vcpt < 5 and (cmp+(cmp*Vol_buffer)) > o1):
			bprice = RoundToTick((cmp+(cmp*(0.1/100))))
			if bsym in SkipSyms:
			    #BuySyms.pop(bsym, None)
			    log_it("Buy %s - Open is equal to low as well as high" % bsym)
			if OnlyNifty == False or bsym in Nifty100:
			    BuySyms[bsym] = bprice
			else:
			    BuySyms.pop(bsym, None)
			    log_it("Buy %s @ %.2f - Selected but skipping as it is not part of Nifty100" % (bsym, bprice))
		    else:
			BuySyms.pop(bsym, None)
			log_it("Buy: %s failed to meet cmp > o1 condition (vcpt=%.2f, cmp=%.2f, o1=%.2f, Vol5_buffer=%.3f, VolInc=%.2f, Vol_buffer=%.3f)" % (bsym, vcpt, cmp, o1,  Vol5_buffer, VolInc, Vol_buffer))

	    if(len(SellSyms.keys())>0):
		SellOrders = {}
		for ssym in SellSyms.keys():
		    o1 = float(SellSyms[ssym][0])
		    vcpt = float(SellSyms[ssym][1])
		    cmp = float((cmps['NSE:%s'%ssym])['last_price'])
		    if (vcpt >= 5 and (cmp-(cmp*Vol5_buffer)) < o1) or (vcpt >= VolInc and vcpt < 5 and (cmp-(cmp*Vol_buffer)) < o1):
			sprice = RoundToTick((cmp-(cmp*(0.1/100))))
			if ssym in SkipSyms:
			    #SellSyms.pop(ssym, None)
			    log_it("Sell %s - Open is equal to low as well as high" % ssym)
			if OnlyNifty == False or ssym in Nifty100:
			    SellSyms[ssym] = sprice
			else:
			    SellSyms.pop(ssym, None)
			    log_it("Sell %s @ %.2f - Selected but skipping as it is not part of Nifty100" % (ssym, sprice))
		    else:
			SellSyms.pop(ssym, None)
			log_it("Sell: %s failed to meet cmp < o1 condition (vcpt=%.2f, cmp=%.2f, o1=%.2f, Vol5_buffer=%.2f, VolInc=%.2f, Vol_buffer=%.2f)" % (ssym, vcpt, cmp, o1, Vol5_buffer, VolInc, Vol_buffer))

	    if (len(BuySyms.keys())+len(SellSyms.keys())) > 0:
		cps = int(cap)/(len(BuySyms.keys())+len(SellSyms.keys()))

		if(len(BuySyms.keys())>0):
		    for sym,price in BuySyms.items():
			#print 'Placing Buy order for %s @ %.2f' % (sym, price)
			PlaceOrder('Buy', sym, price, BuyOrders)

		if(len(SellSyms.keys())>0):
		    for sym,price in SellSyms.items():
			#print 'Placing Sell order for %s @ %.2f' % (sym, price)
			PlaceOrder('Sell', sym, price, SellOrders)
	    else:
		log_it("Nothing to Buy/Sell")

    log_it("--------------------------------END---------------------------------")
