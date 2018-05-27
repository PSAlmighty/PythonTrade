import json

from kiteconnect.connect import KiteConnect
from credentials import API_KEY, API_SECRET_KEY
from ConnectKite import GetKiteToken

kite = KiteConnect(api_key=API_KEY)
session_token = GetKiteToken()
print session_token
data = kite.generate_session("%s"%session_token, api_secret=API_SECRET_KEY)
kite.set_access_token(data["access_token"])
BuySyms = {}
BuySyms['HCLTECH'] = 0
BuySyms['TCS'] = 0
SellSyms = {}
#SellSyms['INDIACEM'] = 0
#SellSyms['MCLEODRUSS'] = 0
syms = ['NSE:'+sym for sym in BuySyms.keys()] + ['NSE:'+sym for sym in SellSyms.keys()]
cmps = kite.ltp(syms)
print (cmps['NSE:HCLTECH'])['last_price']
exit(0)
for sym in BuySyms.keys():
    #sym_info = {}
    #sym_info = cmps['NSE:%s'%sym]
    print cmps['NSE:%s'%sym]['last_price']
