#!/usr/bin/env python2.7

from __future__ import division

import os, sys, datetime, time
import urllib2, csv, multiprocessing
from kiteconnect.connect import KiteConnect

OHOL_PATH="%s" % os.getcwd()
sys.path.append(OHOL_PATH)

from ohol import FindOHOLStocks, LoadPastData, MIS, PastData

# Important parameters
CAPITAL=10000
cap=CAPITAL*(80/100)
SLPct=(1.2/100)
ProfitPct=(1.2/100)

def GetTicks(price):
    tgt=round(0.05 * round(float(price * ProfitPct)/0.05), 2)
    sl=round(0.05 * round(float(price * SLPct)/0.05), 2)
    tsl=round(0.05 * round(float(price * 0.005)/0.05), 2)
    return (tgt, sl, tsl)

def PlaceOrder(call, sym, rprice, Orders):
    # Derive price to buy/sell from recommended price
    price = round(float(rprice), 2)

    numberOfStocks = int((cps*int(MIS[sym]))/price)
    #print "%s %d %s @ %.2f (Leverage=%s applied)" % (call, numberOfStocks, sym, price, MIS[sym])

    # Get Ticks values for SqOff, SL, and Trailing SL used for BO
    (tgt, sl, tsl) = GetTicks(price)

    # Place a BO order
    if (call == 'Buy'):
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
	    print Orders[str(1)]
	    print("Buy Order Id: " + str(order_id) + ", Price: " + str(Orders[order_id][0])  + ", SQTick: " + str(Orders[order_id][1]) + ", SLTick: " + str(Orders[order_id][2]) + ", TSLTick: " + str(Orders[order_id][3]))
	except Exception as e:
	    logging.info("Order placement failed: {}".format(e))
    elif (call == 'Sell'):
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
	    print Orders[str(1)]
	    print("Sell Order Id: " + str(order_id) + ", Price: " + str(Orders[order_id][0])  + ", SQTick: " + str(Orders[order_id][1]) + ", SLTick: " + str(Orders[order_id][2]) + ", TSLTick: " + str(Orders[order_id][3]))
	except Exception as e:
	    logging.info("Order placement failed: {}".format(e))

if __name__ == '__main__':
    #BuySyms = {'IDEA': 154.4}
    #SellSyms = {'HCLTECH': 930.1}

    LoadPastData()
    for sym in PastData.keys():
	print sym
    exit(0)

    kite = KiteConnect(api_key="xh7iuhiwsnjwo0mi")

    print(kite.login_url())

    AutoFetch=True
    if AutoFetch == True:
	response = urllib2.urlopen('http://tinyurl.com/5b2su2')
	session_token = response.geturl() # 'http://stackoverflow.com/'
    else:
	raw_input('Add token to token file')
	token_file = "/home/somasm/GITRepo/PythonTrade/token"
	with open(token_file, 'r') as token_file_handle:
	    session_token = token_file_handle.readlines()[0].strip()
	    token_file_handle.close()

    print session_token
    exit(0)

    # Redirect the user to the login url obtained
    # from kite.login_url(), and receive the request_token
    # from the registered redirect url after the login flow.
    # Once you have the request_token, obtain the access_token as follows.
    # data = kite.generate_session("lUSpKOEe1iJJb210R5ndM8vVkg8hLgyb", "5ik99ozioowfajcfgesno4omm6h5cma8")
    data = kite.generate_session("%s"%session_token, api_secret="5ik99ozioowfajcfgesno4omm6h5cma8")
    print(kite.login_url())

    kite.set_access_token(data["access_token"])

    while True:
	tdt = datetime.datetime.today()
	min = int(tdt.strftime("%M"))
	print min
	if min >= 35:
	    break
	time.sleep(10)
    exit(0)
    (BuySyms, SellSyms) = FindOHOLStocks()
    order_id = kite.place_order(tradingsymbol="CGPOWER",
	                                exchange=kite.EXCHANGE_NSE,
	                                transaction_type=kite.TRANSACTION_TYPE_SELL,
	                                quantity=1,
	                                order_type=kite.ORDER_TYPE_LIMIT,
	                                product=kite.PRODUCT_MIS,
	                                variety=kite.VARIETY_BO,
	                                price=71,
	                                squareoff=75,
	                                stoploss=10,
	                                trailing_stoploss=1
	                                )

    print(order_id)
    
    if (len(BuySyms.keys())+len(SellSyms.keys())) > 0:
        jobs1 = []
        manager = multiprocessing.Manager()

        cps = int(cap/(len(BuySyms.keys())+len(SellSyms.keys())))

        kite = KiteConnect(api_key="xh7iuhiwsnjwo0mi")
        # Redirect the user to the login url obtained
        # from kite.login_url(), and receive the request_token
        # from the registered redirect url after the login flow.
        # Once you have the request_token, obtain the access_token as follows.
        data = kite.generate_session("Z6LTOwl2VTyDPkyxJ366Wz6uNDpqh21U", "5ik99ozioowfajcfgesno4omm6h5cma8")
        kite.set_access_token(data["access_token"])

        if(len(BuySyms.keys()>0)):
            BuyOrders = manager.dict()
            for bsym in BuySyms.keys():
                p = multiprocessing.Process(target=PlaceOrder, args=('Buy', bsym, BuySyms[bsym], BuyOrders))
                jobs1.append(p)
                p.start()

        if(len(SellSyms.keys()>0)):
            SellOrders = manager.dict()
            for ssym in SellSyms.keys():
                p = multiprocessing.Process(target=PlaceOrder, args=('Sell', ssym, SellSyms[ssym], SellOrders))
                jobs1.append(p)
                p.start()

        for proc in jobs1:
            proc.join()
