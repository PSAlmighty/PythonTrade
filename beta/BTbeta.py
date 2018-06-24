#!/usr/bin/python -u

from __future__ import division

import os, sys, datetime
import json, csv
import urllib2, socket, requests
import pandas as pd
from StringIO import StringIO
from termcolor import colored

socket.setdefaulttimeout(10) 
MasterData = {}

DefferredSL=False

# Buy Param
BuyParams = {}
BuyParams['VolCheck'] = float(1.9)
BuyParams['Vol5Check'] = float(5)
BuyParams['CptCheck'] = float(0.2)
BuyParams['P_Candle'] = int(4)
BuyParams['Vol5SLPct1Hr'] = float(5/100)
BuyParams['SLPct1Hr'] = float(5/100)
BuyParams['Vol5ProfitPct'] = float(1.4/100)
BuyParams['Vol5SLPct'] = float(1.1/100)
BuyParams['ProfitPct'] = float(1.1/100)
BuyParams['SLPct'] = float(1.0/100)
#BuyParams['VolBuffer'] = float(0.2/100)
#BuyParams['Vol5Buffer'] = float(0.3/100)
BuyParams['VolBuffer'] = float(0.0/100)
BuyParams['Vol5Buffer'] = float(0.0/100)

# Sell Param
SellParams = {}
SellParams['VolCheck'] = float(1.4)
SellParams['Vol5Check'] = float(5)
SellParams['CptCheck'] = float(0.2)
SellParams['P_Candle'] = int(4)
SellParams['Vol5SLPct1Hr'] = float(3/100)
SellParams['SLPct1Hr'] =float(3/100)
SellParams['Vol5ProfitPct'] = float(1.4/100)
SellParams['Vol5SLPct'] = float(1.1/100)
SellParams['ProfitPct'] = float(1.2/100)
SellParams['SLPct'] = float(1.0/100)
#SellParams['VolBuffer'] = float(0.2/100)
#SellParams['Vol5Buffer'] = float(0.3/100)
SellParams['VolBuffer'] = float(0.0/100)
SellParams['Vol5Buffer'] = float(0.0/100)
 
CptCheck_Values = [0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
CPT_check_list = ['Open > (Buy) or < (Sell) 0.1% of PrevClose', 'Open > (Buy) or < (Sell) 0.2% of PrevClose', 'Open > (Buy) or < (Sell) 0.25% of PrevClose', 'Open > (Buy) or < (Sell) 0.3% of PrevClose', 'Open > (Buy) or < (Sell) 0.35% of PrevClose', 'Open > (Buy) or < (Sell) 0.4% of PrevClose', 'Open > (Buy) or < (Sell) 0.45% of PrevClose', 'Open > (Buy) or < (Sell) 0.5% of PrevClose']

PriceFixing=2
PriceFixing_list = ['(l+h+c)/3', '(h+c)/2', 'c']

verbose=0
idx_close = 0
idx_high = 1
idx_low = 2
idx_open = 3
idx_vol = 4
fromdt=None
todt=None
one_day_scan=0
Y = 2018
M = 4
D = 10
Tick=(5/100)
CAPITAL=100000
CPS=0
GROSS=CAPITAL
today=False
variance = "Both-Buy-And-Sell"
RsymsSell = []
RsymsSellDetail = []
RsymsBuy = []
RsymsData = {}
RsymsBuyDetail = []
BackTesting = True
#Interval = 960
#Interval = 120
Interval = 60
TodayData = {}
OneYearData = {}
DailyData = {}
sl_count = 0
tgt_count = 0
sq_count = 0
Leverage=True
pcts = ""
LOCAL_CACHE=True

NDays = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
Months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

#SCRIPS=['VEDL']
SCRIPS=['YESBANK', 'TATASTEEL', 'STAR', 'SBIN', 'RELIANCE', 'POWERGRID', 'PETRONET', 'ONGC', 'OIL', 'MARUTI', 'M&M', 'LT', 'KTKBANK', 'KOTAKBANK', 'JSWSTEEL', 'ITC', 'IOC', 'INDUSINDBK', 'IGL', 'ICICIBANK', 'HINDUNILVR', 'HEROMOTOCO', 'HDFCBANK', 'HDFC', 'GAIL', 'FEDERALBNK', 'DCBBANK', 'DABUR', 'COLPAL', 'COALINDIA', 'CIPLA', 'CEATLTD', 'CASTROLIND', 'CANBK', 'BPCL', 'BOSCHLTD', 'BHARTIARTL', 'BHARATFORG', 'BATAINDIA', 'BANKBARODA', 'BAJAJ-AUTO', 'AXISBANK', 'ASIANPAINT', 'ASHOKLEY', 'ARVIND', 'APOLLOTYRE', 'APOLLOHOSP', 'AMBUJACEM', 'AMARAJABAT', 'ACC', 'UNIONBANK', 'KSCL', 'ICIL', 'ZEEL', 'VEDL', 'UPL', 'ULTRACEMCO', 'UBL', 'TVSMOTOR', 'TITAN', 'TATAMTRDVR', 'TATAMOTORS', 'TATACHEM', 'SRTRANSFIN', 'SRF', 'RECLTD', 'PTC', 'PIDILITIND', 'NTPC', 'NMDC', 'NCC', 'MOTHERSUMI', 'MCDOWELL-N', 'MARICO', 'M&MFIN', 'LUPIN', 'LICHSGFIN', 'L&TFH', 'JUBLFOOD', 'JISLJALEQS', 'INDIACEM', 'HINDZINC', 'HINDPETRO', 'HINDALCO', 'HEXAWARE', 'GRASIM', 'GLENMARK', 'EXIDEIND', 'ENGINERSIN', 'BRITANNIA', 'BHEL', 'GRANULES', 'GOLDBEES', 'WIPRO', 'VOLTAS', 'TECHM', 'TCS', 'TATAPOWER', 'TATAGLOBAL', 'TATAELXSI', 'TATACOMM', 'SIEMENS', 'RELINFRA', 'RELCAPITAL', 'PFC', 'PAGEIND', 'NIITTECH', 'MINDTREE', 'IRB', 'INFY', 'INFRATEL', 'IBULHSGFIN', 'HCLTECH', 'HAVELLS', 'DISHTV', 'CONCOR', 'CESC', 'CADILAHC', 'BIOCON', 'BEML', 'BEL', 'TORNTPOWER', 'OFSS', 'KPIT', 'JINDALSTEL', 'CGPOWER', 'CENTURYTEX', 'BHARATFIN', 'AJANTPHARM', 'WOCKPHARMA', 'TORNTPHARM', 'SUNPHARMA', 'ORIENTBANK', 'IDEA', 'GODREJIND', 'DRREDDY', 'DLF', 'DIVISLAB', 'DHFL', 'BANKINDIA', 'BAJFINANCE', 'AUROPHARMA']

#SCRIPS=['ABB', 'ACC', 'ADANIPORTS', 'ABCAPITAL', 'AMBUJACEM', 'ASHOKLEY', 'ASIANPAINT', 'AUROPHARMA', 'DMART', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BANKBARODA', 'BEL', 'BHEL', 'BPCL', 'BHARTIARTL', 'INFRATEL', 'BOSCHLTD', 'BRITANNIA', 'CADILAHC', 'CIPLA', 'COALINDIA', 'COLPAL', 'CONCOR', 'CUMMINSIND', 'DLF', 'DABUR', 'DRREDDY', 'EICHERMOT', 'EMAMILTD', 'GAIL', 'GICRE', 'GODREJCP', 'GRASIM', 'HCLTECH', 'HDFCBANK', 'HAVELLS', 'HEROMOTOCO', 'HINDALCO', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'HDFC', 'ITC', 'ICICIBANK', 'ICICIPRULI', 'IDEA', 'IBULHSGFIN', 'IOC', 'INDUSINDBK', 'INFY', 'INDIGO', 'JSWSTEEL', 'KOTAKBANK', 'L&TFH', 'LICHSGFIN', 'LT', 'LUPIN', 'MRF', 'M&M', 'MARICO', 'MARUTI', 'MOTHERSUMI', 'NHPC', 'NMDC', 'NTPC', 'ONGC', 'OIL', 'OFSS', 'PETRONET', 'PIDILITIND', 'PEL', 'PFC', 'POWERGRID', 'PGHH', 'PNB', 'RELIANCE', 'RECLTD', 'SBILIFE', 'SHREECEM', 'SRTRANSFIN', 'SIEMENS', 'SBIN', 'SAIL', 'SUNPHARMA', 'SUNTV', 'TCS', 'TATAMTRDVR', 'TATAMOTORS', 'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'MCDOWELL-N', 'VEDL', 'WIPRO', 'YESBANK', 'ZEEL']

IgnoreSyms = ['BOSCHLTD', 'MRF', 'PAGEIND', 'EICHERMOT', 'ABCAPITAL', 'MCLEODRUSS']

MIS={'BANKBEES':'10',
'GOLDBEES':'10',
'GRANULES':'10',
'LIQUIDBEES':'10',
'NIFTYBEES':'10',
'BHEL':'11',
'BRITANNIA':'11',
'EICHERMOT':'11',
'ENGINERSIN':'11',
'EXIDEIND':'11',
'GLENMARK':'11',
'GRASIM':'11',
'HEXAWARE':'11',
'HINDALCO':'11',
'HINDPETRO':'11',
'HINDZINC':'11',
'INDIACEM':'11',
'JISLJALEQS':'11',
'JUBLFOOD':'11',
'L&TFH':'11',
'LICHSGFIN':'11',
'LUPIN':'11',
'M&MFIN':'11',
'MARICO':'11',
'MCDOWELL-N':'11',
'MCLEODRUSS':'11',
'MOTHERSUMI':'11',
'MRF':'11',
'NCC':'11',
'NMDC':'11',
'NTPC':'11',
'PIDILITIND':'11',
'PTC':'11',
'RECLTD':'11',
'SRF':'11',
'SRTRANSFIN':'11',
'TATACHEM':'11',
'TATAMOTORS':'11',
'TATAMTRDVR':'11',
'TITAN':'11',
'TVSMOTOR':'11',
'UBL':'11',
'ULTRACEMCO':'11',
'UPL':'11',
'VEDL':'11',
'ZEEL':'11',
'ICIL':'13',
'KSCL':'13',
'UNIONBANK':'13',
'ACC':'14',
'AMARAJABAT':'14',
'AMBUJACEM':'14',
'APOLLOHOSP':'14',
'APOLLOTYRE':'14',
'ARVIND':'14',
'ASHOKLEY':'14',
'ASIANPAINT':'14',
'AXISBANK':'14',
'BAJAJ-AUTO':'14',
'BANKBARODA':'14',
'BATAINDIA':'14',
'BHARATFORG':'14',
'BHARTIARTL':'14',
'BOSCHLTD':'14',
'BPCL':'14',
'CANBK':'14',
'CASTROLIND':'14',
'CEATLTD':'14',
'CIPLA':'14',
'COALINDIA':'14',
'COLPAL':'14',
'DABUR':'14',
'DCBBANK':'14',
'FEDERALBNK':'14',
'GAIL':'14',
'HDFC':'14',
'HDFCBANK':'14',
'HEROMOTOCO':'14',
'HINDUNILVR':'14',
'ICICIBANK':'14',
'IGL':'14',
'INDUSINDBK':'14',
'IOC':'14',
'ITC':'14',
'JSWSTEEL':'14',
'KOTAKBANK':'14',
'KTKBANK':'14',
'LT':'14',
'M&M':'14',
'MARUTI':'14',
'OIL':'14',
'ONGC':'14',
'PETRONET':'14',
'POWERGRID':'14',
'RELIANCE':'14',
'SBIN':'14',
'STAR':'14',
'TATASTEEL':'14',
'YESBANK':'14',
'3MINDIA':'3',
'AARTIIND':'3',
'ABAN':'3',
'ABB':'3',
'ABFRL':'3',
'ADANIENT':'3',
'ADANIPORTS':'3',
'AKZOINDIA':'3',
'ALKEM':'3',
'ALLCARGO':'3',
'APLLTD':'3',
'ASAHIINDIA':'3',
'ASTRAZEN':'3',
'ATFL':'3',
'ATUL':'3',
'AUBANK':'3',
'AUTOAXLES':'3',
'BAJAJCORP':'3',
'BAJAJELEC':'3',
'BAJAJFINSV':'3',
'BAJAJHIND':'3',
'BAJAJHLDNG':'3',
'BALKRISIND':'3',
'BALRAMCHIN':'3',
'BANCOINDIA':'3',
'BERGEPAINT':'3',
'BGRENERGY':'3',
'BLUEDART':'3',
'BRNL':'3',
'BSE':'3',
'CANFINHOME':'3',
'CAPACITE':'3',
'CAPF':'3',
'CDSL':'3',
'CENTRALBK':'3',
'CENTURYPLY':'3',
'CHENNPETRO':'3',
'CHOLAFIN':'3',
'COCHINSHIP':'3',
'COROMANDEL':'3',
'COX&KINGS':'3',
'CRISIL':'3',
'CROMPTON':'3',
'CUB':'3',
'CUMMINSIND':'3',
'CYIENT':'3',
'DALMIABHA':'3',
'DBCORP':'3',
'DCMSHRIRAM':'3',
'DIAMONDYD':'3',
'DIXON':'3',
'DMART':'3',
'ECLERX':'3',
'EDELWEISS':'3',
'EIDPARRY':'3',
'EMAMILTD':'3',
'ENDURANCE':'3',
'EQUITAS':'3',
'ERIS':'3',
'ESCORTS':'3',
'EVEREADY':'3',
'FEL':'3',
'FINCABLES':'3',
'FORTIS':'3',
'FRETAIL':'3',
'GANECOS':'3',
'GATI':'3',
'GDL':'3',
'GEPIL':'3',
'GESHIP':'3',
'GICHSGFIN':'3',
'GICRE':'3',
'GILLETTE':'3',
'GLAXO':'3',
'GNA':'3',
'GNFC':'3',
'GODREJCP':'3',
'GODREJPROP':'3',
'GPPL':'3',
'GREAVESCOT':'3',
'GRUH':'3',
'GSFC':'3',
'GSKCONS':'3',
'GSPL':'3',
'GTPL':'3',
'GUJALKALI':'3',
'GUJFLUORO':'3',
'GUJGASLTD':'3',
'HCC':'3',
'HDIL':'3',
'HEIDELBERG':'3',
'HGS':'3',
'HIKAL':'3',
'HONAUT':'3',
'HSCL':'3',
'HSIL':'3',
'HUDCO':'3',
'IBREALEST':'3',
'ICICIGI':'3',
'ICICIPRULI':'3',
'IEX':'3',
'IGPL':'3',
'IIFL':'3',
'IL&FSTRANS':'3',
'INDHOTEL':'3',
'INDIANB':'3',
'INDIGO':'3',
'INFIBEAM':'3',
'INOXLEISUR':'3',
'INOXWIND':'3',
'INTELLECT':'3',
'IOB':'3',
'IPCALAB':'3',
'JAGRAN':'3',
'JAMNAAUTO':'3',
'JETAIRWAYS':'3',
'JINDALPOLY':'3',
'JKCEMENT':'3',
'JKPAPER':'3',
'JKTYRE':'3',
'JPASSOCIAT':'3',
'JSL':'3',
'JSLHISAR':'3',
'JUBILANT':'3',
'JUSTDIAL':'3',
'JYOTHYLAB':'3',
'KAJARIACER':'3',
'KALPATPOWR':'3',
'KANSAINER':'3',
'KARURVYSYA':'3',
'KEC':'3',
'KEI':'3',
'KESORAMIND':'3',
'KHADIM':'3',
'KIRLOSENG':'3',
'KOTAKNIFTY':'3',
'KRBL':'3',
'LALPATHLAB':'3',
'LEEL':'3',
'LGBBROSLTD':'3',
'LINDEINDIA':'3',
'LOVABLE':'3',
'M100':'3',
'M50':'3',
'MAGMA':'3',
'MAHINDCIE':'3',
'MAHLOG':'3',
'MAJESCO':'3',
'MANALIPETC':'3',
'MANAPPURAM':'3',
'MANGALAM':'3',
'MANINFRA':'3',
'MANPASAND':'3',
'MARKSANS':'3',
'MASFIN':'3',
'MATRIMONY':'3',
'MCX':'3',
'MEGH':'3',
'MERCATOR':'3',
'MFSL':'3',
'MGL':'3',
'MINDAIND':'3',
'MOIL':'3',
'MOLDTKPAC':'3',
'MPHASIS':'3',
'MRPL':'3',
'MUKANDLTD':'3',
'MUTHOOTFIN':'3',
'NATIONALUM':'3',
'NAUKRI':'3',
'NBCC':'3',
'NESTLEIND':'3',
'NETWORK18':'3',
'NFL':'3',
'NH':'3',
'NIACL':'3',
'NIF100IWIN':'3',
'NIFTYIWIN':'3',
'NIITLTD':'3',
'NLCINDIA':'3',
'NOCIL':'3',
'NRBBEARING':'3',
'OBEROIRLTY':'3',
'OMAXE':'3',
'ORIENTCEM':'3',
'PARAGMILK':'3',
'PCJEWELLER':'3',
'PEL':'3',
'PERSISTENT':'3',
'PFIZER':'3',
'PGHH':'3',
'PHOENIXLTD':'3',
'PIIND':'3',
'PNBHOUSING':'3',
'POLYPLEX':'3',
'PRAKASH':'3',
'PRESTIGE':'3',
'PVR':'3',
'QUICKHEAL':'3',
'RADICO':'3',
'RADIOCITY':'3',
'RAJESHEXPO':'3',
'RALLIS':'3',
'RAMCOCEM':'3',
'RAMCOIND':'3',
'RBLBANK':'3',
'RCF':'3',
'RCOM':'3',
'RELAXO':'3',
'REPCOHOME':'3',
'RICOAUTO':'3',
'RKFORGE':'3',
'RNAM':'3',
'RNAVAL':'3',
'ROLTA':'3',
'SADBHAV':'3',
'SALASAR':'3',
'SANGHIIND':'3',
'SANOFI':'3',
'SAREGAMA':'3',
'SBILIFE':'3',
'SCHAND':'3',
'SCI':'3',
'SHANKARA':'3',
'SHARDAMOTR':'3',
'SHRIRAMCIT':'3',
'SICAL':'3',
'SINTEX':'3',
'SIS':'3',
'SJVN':'3',
'SKFINDIA':'3',
'SNOWMAN':'3',
'SOBHA':'3',
'SOLARINDS':'3',
'SPARC':'3',
'SPTL':'3',
'SREINFRA':'3',
'SUNDARMFIN':'3',
'SUNDRMFAST':'3',
'SUNTECK':'3',
'SUNTV':'3',
'SUPREMEIND':'3',
'SUZLON':'3',
'SYMPHONY':'3',
'SYNGENE':'3',
'TATACOFFEE':'3',
'TATAINVEST':'3',
'TATASPONGE':'3',
'TBZ':'3',
'TCI':'3',
'TEJASNET':'3',
'THERMAX':'3',
'THOMASCOOK':'3',
'THYROCARE':'3',
'TIFIN':'3',
'TIRUMALCHM':'3',
'TNPETRO':'3',
'TNPL':'3',
'TRENT':'3',
'TRIDENT':'3',
'TTKPRESTIG':'3',
'TWL':'3',
'UCOBANK':'3',
'UJJIVAN':'3',
'VGUARD':'3',
'VIJAYABANK':'3',
'VISHNU':'3',
'VTL':'3',
'WABCOINDIA':'3',
'WELENT':'3',
'WHIRLPOOL':'3',
'WONDERLA':'3',
'ADANIPOWER':'5',
'ALBK':'5',
'ANDHRABANK':'5',
'GMRINFRA':'5',
'IDBI':'5',
'IDFC':'5',
'IDFCBANK':'5',
'IFCI':'5',
'JSWENERGY':'5',
'NHPC':'5',
'PNB':'5',
'RAYMOND':'5',
'RPOWER':'5',
'SAIL':'5',
'SOUTHBANK':'5',
'SYNDIBANK':'5',
'TV18BRDCST':'5',
'AUROPHARMA':'7',
'BAJFINANCE':'7',
'BANKINDIA':'7',
'DHFL':'7',
'DIVISLAB':'7',
'DLF':'7',
'DRREDDY':'7',
'GODREJIND':'7',
'IDEA':'7',
'ORIENTBANK':'7',
'SUNPHARMA':'7',
'TORNTPHARM':'7',
'WOCKPHARMA':'7',
'AJANTPHARM':'8',
'BHARATFIN':'8',
'CENTURYTEX':'8',
'CGPOWER':'8',
'JINDALSTEL':'8',
'KPIT':'8',
'OFSS':'8',
'TORNTPOWER':'8',
'BEL':'9',
'BEML':'9',
'BIOCON':'9',
'CADILAHC':'9',
'CESC':'9',
'CONCOR':'9',
'DISHTV':'9',
'HAVELLS':'9',
'HCLTECH':'9',
'IBULHSGFIN':'9',
'INFRATEL':'9',
'INFY':'9',
'IRB':'9',
'MINDTREE':'9',
'NIITTECH':'9',
'PAGEIND':'9',
'PFC':'9',
'RELCAPITAL':'9',
'RELINFRA':'9',
'SIEMENS':'9',
'TATACOMM':'9',
'TATAELXSI':'9',
'TATAGLOBAL':'9',
'TATAPOWER':'9',
'TCS':'9',
'TECHM':'9',
'VOLTAS':'9',
'WIPRO':'9'
}

def reject(reason, sym, vcpt, pcpt, v2cpt, p2cpt, gap):
    return
    log_it("Rejecting %s as %s (vcpt=%.2f%%, pcpt=%.2f%%, v2cpt=%.2f%%, p2cpt=%.2f%%, gap=%.2f%%)" % (sym, reason, vcpt, pcpt, v2cpt, p2cpt, gap))

def log_it(str):
    if verbose:
	print str

def GetHumanDate(utc, time=0):
    if time == 1:
	return datetime.datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d %H:%M:%S')
    else:
	return datetime.datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d')

def GetNiftyScrips(n):
    url='https://www.nseindia.com/content/indices/ind_nifty%dlist.csv' % n
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(req)
    return pd.read_csv(StringIO(response.read()), usecols=[2]).values.flatten()

def RoundToTick(price):
    return round(price/Tick)*Tick

def GetAbsolutes(price, tgt_pct, sl_pct):
    tgt=RoundToTick((float(price) * tgt_pct))
    sl=RoundToTick((float(price) * sl_pct))
    #tsl=RoundToTick((float(price) * TSLPct))
    #if tsl < 1:
        #tsl=1
    #return (tgt, sl, tsl)
    return (tgt, sl)

# Bracket and cover order Margins calculation for Equity:
def MarginCal(sym, cps, price, sl, transaction_type):
    co_lower = 0
    co_upper = 0
    quantity = 1

    margin_data = requests.get('https://api.kite.trade/margins/equity')
    data = margin_data.json()

    for item in data:
	if item['tradingsymbol'] == sym:
	    co_lower = item['co_lower']
	    co_upper = item['co_upper']
	    break

    if co_lower == 0 or co_upper == 0:
	log_it('%s: Unable to find maximum margin, using regular Multiplier', sym);
	qty = ((cps*MIS[sym])/price)
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
    elif transaction_type == 'Sell':
        x = (trigger - price) * quantity

    y = co_lower * price * quantity
    margin = x if x > y else y
    margin = margin + (margin * 0.2)

    return round(cps/margin)

def MarketHours():
    tdt = datetime.datetime.today();
    th = int(tdt.strftime("%H"))
    tm = int(tdt.strftime("%M"))
    mins = th*60+tm
    if (mins > 555 and mins < 931):
	return True
    return False

# Get data from finance.google.com
def GetURLData(p, sym, candle):
    try:
	if candle == False:
	    url = 'https://finance.google.com/finance/getprices?x=NSE&q=%s&f=d,c,h,l,o,v&p=%sd' % (sym.replace('&','%26'), p)
	else:
	    url = 'https://finance.google.com/finance/getprices?x=NSE&q=%s&f=d,c,h,l,o,v&p=%sd&i=%s' % (sym.replace('&','%26'), p, Interval)
	#log_it("Getting %s day(s) data for %s from %s" % (p, sym, url))
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	content = csv.reader(response.read().splitlines()[7:])
	return content
    except:
	return None

def GetURLData_Old(p, sym):
    if p == '1Y':
	url = 'https://finance.google.com/finance/getprices?x=NSE&q=%s&f=d,c,h,l,o,v&p=%s' % (sym.replace('&','%26'), p)
    else:
	url = 'https://finance.google.com/finance/getprices?x=NSE&q=%s&f=d,c,h,l,o,v&p=%s&i=%s' % (sym.replace('&','%26'), p, Interval)
    response = urllib2.urlopen(url)
    content = csv.reader(response.read().splitlines()[7:])
    return content

def Get_1Y_Data(sym):
    if today and os.path.isdir(TODAY):
	sym_cache_file = "%s/%s.json" % (TODAY, sym)
	if os.path.exists(sym_cache_file):
	    with open(sym_cache_file, 'r') as sym_file_handle:
		data_cache = json.load(sym_file_handle)
		sym_file_handle.close()
		if len(data_cache) > 0:
		    #log_it("Getting data for %s from %s" % (sym, sym_cache_file))
		    return data_cache
    if today == False and BackTesting:
	sym_cache_file = "ACCUMULATED_DATA/%s.json" % sym
	if os.path.exists(sym_cache_file):
	    with open(sym_cache_file, 'r') as sym_file_handle:
		data_cache = json.load(sym_file_handle)
		sym_file_handle.close()
		if len(data_cache) > 0:
		    #log_it("Getting data for %s from %s" % (sym, sym_cache_file))
		    return data_cache
    data = {}
    content = GetURLData(ndays+20, sym, False)
    if content is None:
	return data
    for d in content:
	if d[0][0] == 'a':
	    lutc = d[0].replace('a','');
	    data[lutc] = d[1:]
	else:
	    llutc = str(int(lutc)+(int(d[0])*86400))
	    data[llutc] = d[1:]
    if not os.path.exists(TODAY):
	os.mkdir(TODAY)
    sym_file = "%s/%s.json" % (TODAY, sym)
    with open(sym_file, 'w') as sym_file_handle:
	json.dump(data, sym_file_handle)
	sym_file_handle.close()
    return data

# Get candle data for a given symbol for given days
def GetScripCandleData(days, sym):
    if today and os.path.isdir(TODAY):
	sym_cache_file = "%s/%s.candles.json" % (TODAY, sym)
	if os.path.exists(sym_cache_file):
	    with open(sym_cache_file, 'r') as sym_file_handle:
		data_cache = json.load(sym_file_handle)
		sym_file_handle.close()
		if len(data_cache) > 0:
		    #log_it("Getting data for %s from %s" % (sym, sym_cache_file))
		    return data_cache
    if today == False and BackTesting:
	sym_cache_file = "ACCUMULATED_DATA/%s.candles.json" % sym
	if os.path.exists(sym_cache_file):
	    with open(sym_cache_file, 'r') as sym_file_handle:
		data_cache = json.load(sym_file_handle)
		sym_file_handle.close()
		if len(data_cache) > 0:
		    #log_it("Getting data for %s from %s" % (sym, sym_cache_file))
		    return data_cache
    data = {}
    content = GetURLData(days, sym, True)
    if content is None:
	return {}
    lutc = 0
    for d in content:
	if d[0][0] == 'a':
	    utc = d[0].replace('a', '')
	    rutc = int(utc)
	else:
	    utc = rutc + (int(d[0]) * Interval)
	hr = int(datetime.datetime.fromtimestamp(int(utc)).strftime("%H"))
	utc_key = (datetime.datetime.fromtimestamp(int(utc)).date()).strftime("%s")
	if hr == 9 and utc_key not in data.keys():
	    #print 'Making new entry for', GetHumanDate(utc), GetHumanDate(utc_key)
	    data[utc_key] = [d[1:]]
	    lutc = utc_key
	else:
	    if lutc == 0:
		return {}
	    #print 'Appending to', GetHumanDate(lutc)
	    data[lutc].append(d[1:])
    if days > 0:
	if not os.path.exists(TODAY):
	    os.mkdir(TODAY)
	sym_file = "%s/%s.candles.json" % (TODAY, sym)
	if os.path.exists(sym_file):
	    os.rename(sym_file, "%s.moved" % sym_file)
	with open(sym_file, 'w') as sym_file_handle:
	    json.dump(data, sym_file_handle)
    return data

def GetPrevUTCNifty(UTC):
    keys = NiftyIndex1YCandle.keys()
    i=1
    while i < 6:
	pUTC = str(int(UTC) - (i*86400))
	if pUTC in keys:
	    return pUTC
	i+=1
    return None

def GetPrevUTC(data, UTC):
    keys = data.keys()
    i=1
    while i < 6:
	pUTC = str(int(UTC) - (i*86400))
	if pUTC in keys:
	    return pUTC
	i+=1
    return None

def Initialize():
    global sl_count
    global tgt_count
    global sq_count
    global y
    global m
    global d
    global CAPITAL
    global GROSS
    global RsymsData

    sl_count = 0
    tgt_count = 0
    sq_count = 0

    RsymsData = {}
    if today == True:
	y = int(dt.strftime("%Y"))
	m = int(dt.strftime("%m"))
	d = int(dt.strftime("%d"))
    elif fromdt:
	y = fromy
	m = fromm
	d = fromd
    else:
	y = Y
	m = M
	d = D
    GROSS=CAPITAL

def MainLoop(s):
    global tgt_count
    global sl_count
    global sq_count
    global y
    global m
    global d
    global RsymsBuy
    global RsymsSell
    global GROSS
    global CPS
    tdays=0
    mdays=0
    t_count=0
    t_tgt_count=0
    t_sl_count=0
    t_sq_count=0

    Initialize()

    tdt = datetime.datetime.today();
    tm = int(tdt.strftime("%m"))
    td = int(tdt.strftime("%d"))

    while True:
	if (todt and m == tom and d > tod) or (m == tm and ((today and d > td) or (not today and d >= td))):
	    break
	if d > NDays[m-1]:
	    d=1
	    m+=1
	    if m > 12:
		m=1
		y+=1
	    continue
	dt = datetime.datetime(y, m, d, 0, 0, 0)
	utc = dt.strftime("%s")
	dtl = datetime.datetime(y, m, d, 15, 30, 0)
	utcl = dtl.strftime("%s")

	pnifty = GetPrevUTCNifty(utcl)
	if pnifty is None:
	    d+=1
	    log_it("Could not find Nifty value for %s (3:30)" % GetHumanDate(utcl))
	    continue
	pnifty = NiftyIndex1YCandle[pnifty][0]
	if today == True:
	    cnifty = NiftyIndexTodayCandle[utc][0][0]
	elif utc in NiftyIndex60DCandle.keys():
	    cnifty = NiftyIndex60DCandle[utc][0][0]
	else:
	    d+=1
	    log_it("Could not find Current Nifty value for %s, %s" % (utc, GetHumanDate(utc, 1)))
	    continue
	Ncpt = ((float(cnifty)-float(pnifty))/float(pnifty))*100
	if Ncpt <= -2:
	    d+=1
	    log_it("Skipping trade on %s" % (GetHumanDate(utc)))
	    continue
	if s == 'Nifty':
	    strategy = "Both"
	    if Ncpt <= -1:
		strategy = "Sell"
	else:
	    strategy = s

	RsymsBuy = []
	RsymsSell = []

	mdays+=1
	# Shortlist complete list of stocks in one iteration
	for sym in Nsyms:
	    if today:
		utcs = TodayData[sym].keys()
		prev_utcl = GetPrevUTC(OneYearData[sym], utcl)
		if prev_utcl is None:
		    log_it("Previous data is not available for %s(%s:%s)" % (sym, utcl, GetHumanDate(utcl)))
		    continue
		OHOLStrategy(strategy, sym, utc, utcl)
	    else:
		utcs = DailyData[sym].keys()
		prev_utcl = GetPrevUTC(OneYearData[sym], utcl)
		if prev_utcl is None:
		    log_it("Could not find Previous Nifty for %s, %s" % (utcl, GetHumanDate(utcl, 1)))
		    continue
		if utc in utcs:
		    if prev_utcl is not None:
			#log_it("Iteration for %s, %s,%s" % (sym, GetHumanDate(prev_utcl), GetHumanDate(utc)))
			OHOLStrategy(strategy, sym, utc, prev_utcl)
		    else:
			log_it("Data is not available for %s(%s)" % (sym, GetHumanDate(prev_utcl)))
		else:
		    log_it("Data is not available for %s(%s,%s)" % (sym, utc, GetHumanDate(utc)))

	if today and BackTesting == False and (len(RsymsBuy) > 0 or len(RsymsSell) > 0):
	    CPS = CAPITAL/(len(RsymsBuy)+len(RsymsSell))
	    for sym in RsymsBuy:
		qty = MarginCal(sym, CPS, RsymsData[sym]['PRICE'], RsymsData[sym]['SL'], 'Buy')
		print colored('Buy %d %s @ %.2f with Target=%.2f, SL=%.2f' % (qty, sym, RsymsData[sym]['PRICE'], RsymsData[sym]['TGT'], RsymsData[sym]['SL']), 'green')
	    for sym in RsymsSell:
		qty = MarginCal(sym, CPS, RsymsData[sym]['PRICE'], RsymsData[sym]['SL'], 'Buy')
		print colored('Sell %d %s @ %.2f with Target=%.2f, SL=%.2f' % (qty, sym, RsymsData[sym]['PRICE'], RsymsData[sym]['TGT'], RsymsData[sym]['SL']), 'red')

	if BackTesting and (len(RsymsBuy) > 0 or len(RsymsSell) > 0):
	    total_count=len(RsymsBuy)+len(RsymsSell)

	    sl_count=0
	    tgt_count=0
	    sq_count=0

	    if GROSS <= 0:
		break

	    if strategy == "Buy" and len(RsymsBuy) > 0:
		CPS=GROSS/len(RsymsBuy)
	    elif strategy == "Sell" and len(RsymsSell) > 0:
		CPS=GROSS/len(RsymsSell)
	    elif len(RsymsBuy) > 0 or len(RsymsSell) > 0:
		CPS=GROSS/(len(RsymsBuy)+len(RsymsSell))

	    if CPS <= 0:
		break

	    if strategy == "Buy" or strategy == "Both":
		if len(RsymsBuy) > 0:
		    BackTest('Buy', utc, prev_utcl, CPS)
		else:
		    print 'No buy stocks picked on', GetHumanDate(utc)

	    if strategy == "Sell" or strategy == "Both":
		if len(RsymsSell) > 0:
		    BackTest('Sell', utc, prev_utcl, CPS)
		else:
		    print 'No sell stocks picked on ', GetHumanDate(utc)

	    if total_count > 0:
		#for key in MasterData[utc].keys():
		    #print "%s,%s,PPRICE=%.2f,SL=%.2f,ASLPCT=%.2f%%,ATGT=%.2f,BuyTGTPCT=%.2f%%,SellTGTPCT=%.2f%%,SQO=%.2f,SQOPCT=%.2f%%,CHLO1=%s,CHLO2=%s,SL_PCT=%.2f%%,ProfitPct=%.2f%%,VolCheck=%s,PriceInc=%s,VCPT=%.2f,PCPT=%.2f,PriceFixing=%s" % (GetHumanDate(utc), key, MasterData[utc][key]['PPRICE'], MasterData[utc][key]['SL'], MasterData[utc][key]['ASLPCT'], MasterData[utc][key]['ATGT'], MasterData[utc][key]['BuyTGTPCT'], MasterData[utc][key]['SellTGTPCT'], MasterData[utc][key]['SQO'], MasterData[utc][key]['SQOPCT'], MasterData[utc][key]['CHLO1'], MasterData[utc][key]['CHLO2'], MasterData[utc][key]['SL_PCT'], MasterData[utc][key]['ProfitPct'], MasterData[utc][key]['VolCheck'], MasterData[utc][key]['CptCheck'], MasterData[utc][key]['VCPT'], MasterData[utc][key]['PCPT'], MasterData[utc][key]['PriceChoice'])
		print("%s %d: Total Count=%d, SL Count=%d (%d%%), Tgt Count=%d (%d%%), SQO Count = %d (%d%%)" % (Months[m-1], d, total_count, sl_count, (sl_count/total_count*100), tgt_count, (tgt_count/total_count*100), sq_count, (sq_count/total_count*100)))
		t_count+=total_count
		t_tgt_count+=tgt_count
		t_sl_count+=sl_count
		t_sq_count+=sq_count
		tdays+=1
		#print("Nifty%d[%s]: Ncpt=%f, Capital=%d, Gross=%d, Pct=%.2f%% (ProfitPct=%s,SLPct=%s,VolumeCondition=%s,CptCheck=%d,TotalStocks=%d,Tgt-Hit=%d,SL-Hit=%d,SQ-Hit=%d,TradedDays=%d)" % (len(Nsyms), s, Ncpt, CAPITAL, GROSS, float((GROSS-CAPITAL)/CAPITAL)*100, tpct, slpct, 'CandleVolume > %.2f% of YesterdaysVolume' % VolCheck, BuyParams['CptCheck'], t_count, t_tgt_count, t_sl_count, t_sq_count, tdays, mdays))

	if one_day_scan == 1:
	    break

	d+=1

    if BackTesting:
	#if float((GROSS-CAPITAL)/CAPITAL)*100 > 0 and t_count > 0:
	    print("CSV,%s,%.2f,%s%%,%s%%,%s%%,%s%%,%s%%,%s%%,%s%%,%s%%,%s,%s,%s,%s,%s,%s,%d,%d,%d,%d,%d" % (s, float((GROSS-CAPITAL)/CAPITAL)*100, BuyParams['SLPct']*100, SellParams['SLPct']*100, BuyParams['ProfitPct']*100, SellParams['ProfitPct']*100, BuyParams['Vol5SLPct']*100, SellParams['Vol5SLPct']*100, BuyParams['Vol5ProfitPct']*100, SellParams['Vol5ProfitPct']*100, 'CandleVolume > Buy(%.2f%%)/Sell(%.2f%%) of YesterdaysVolume' % (BuyParams['VolCheck'], SellParams['VolCheck']), 'Open > Buy(%.2f%%) or < Sell(%.2f%%) of PrevClose' % (BuyParams['CptCheck'], SellParams['CptCheck']), 'Buy: c2+(%.2f%% or %.2f%%)ofc2 > o1' % (BuyParams['VolBuffer']*100, BuyParams['Vol5Buffer']*100), 'Sell: c2-(%.2f%% or %.2f%%)ofc2 < o1' % (SellParams['VolBuffer']*100, SellParams['Vol5Buffer']*100), PriceFixing_list[PriceFixing], 'Buy(%dCandle)/Sell(%dCandle)' % (BuyParams['P_Candle'], SellParams['P_Candle']), t_tgt_count, t_sl_count, t_sq_count, tdays, mdays))

def BackTest(call, UTC, prev_utcl, cpshare):
    global sl_count
    global tgt_count
    global sq_count
    global GROSS

    if call == 'Buy':
	pcandle = BuyParams['P_Candle']-1
    else:
	pcandle = SellParams['P_Candle']-1

    if call == 'Buy':
	syms = RsymsBuy
    else:
	syms = RsymsSell

    for sym in syms:
	cps = cpshare

	sq_off=1
	pft_list = []
	sl_list = []

	if today:
	    cdata = TodayData[sym][UTC]
	else:
	    cdata = DailyData[sym][UTC]

	o1 = float(cdata[0][idx_open])
	c_candle_vol=int(cdata[0][idx_vol])
	pclose = float(OneYearData[sym][prev_utcl][idx_close])
	pcpt = ((o1-pclose)/pclose)*100
	vcpt = (c_candle_vol/int(OneYearData[sym][prev_utcl][idx_vol]))*100
	v2cpt = (int(cdata[4][idx_vol])/int(OneYearData[sym][prev_utcl][idx_vol]))*100
	p2cpt = ((float(cdata[4][idx_open])-pclose)/pclose)*100

	if 1 == 1:
	    if vcpt > 5:
		if call == 'Buy':
		    tpct = BuyParams['Vol5ProfitPct']
		    slpct = BuyParams['Vol5SLPct']
		    slpct1hr = BuyParams['Vol5SLPct1Hr']
		elif call == 'Sell':
		    tpct = SellParams['Vol5ProfitPct']
		    slpct = SellParams['Vol5SLPct']
		    slpct1hr = SellParams['Vol5SLPct1Hr']
	    else:
		if call == 'Buy':
		    tpct = BuyParams['ProfitPct']
		    slpct = BuyParams['SLPct']
		    slpct1hr = BuyParams['SLPct1Hr']
		elif call == 'Sell':
		    tpct = SellParams['ProfitPct']
		    slpct = SellParams['SLPct']
		    slpct1hr = SellParams['SLPct1Hr']

	c = float(cdata[pcandle][idx_close])
	h = float(cdata[pcandle][idx_high])
	low = float(cdata[pcandle][idx_low])
	o = float(cdata[pcandle][idx_open])
	if PriceFixing == 0:
	    pprice = float(c+h+low)/3
	elif PriceFixing == 1:
	    pprice = float(c+h)/2
	elif PriceFixing == 2:
	    pprice = float(c)

	if Leverage:
	    if 1 == 0:
		cps *= int(MIS[sym])
	    else:
		if call == 'Buy':
		    sl_price = pprice - (pprice * slpct)
	        else:
		   sl_price = pprice + (pprice * slpct)
	        cps = int(pprice * MarginCal(sym, cps, pprice, sl_price, call))

	bought=False
	j=pcandle+1;
	#print sym, j, pcandle, len(cdata)
	while (j<(pcandle+120)):
	    if call == 'Buy':
		if pprice >= float(cdata[j][idx_low]):
		    bought=True
		    print "%s: Found buy price @ %d candle and bought it @ %d candle (%.2f,%s)" % (sym, pcandle+1, j+1, pprice, cdata[j][idx_low])
		    RsymsData[sym]['PCANDLE'] = j
		    break
	    elif call == 'Sell':
		if pprice <= float(cdata[j][idx_high]):
		    bought=True
		    print "%s: Found sell price @ %d candle and sold it @ %d candle (%.2f,%s)" % (sym, pcandle+1, j+1, pprice, cdata[j][idx_high])
		    RsymsData[sym]['PCANDLE'] = j
		    break
	    j+=1
	if bought == False:
	    if UTC not in MasterData.keys():
		MasterData[UTC] = {}
	    if call == 'Buy':
		print "%s: %s: Not able to buy %s" % (GetHumanDate(UTC), call, sym)
	    elif call == 'Sell':
		print "%s: %s: Not able to sell %s" % (GetHumanDate(UTC), call, sym)
	    continue
	#print "%s: Purchase Price=%s" % (sym, pprice)
	if call == 'Buy':
	    tgt_price = pprice + (pprice * tpct)
	    sl_price_rest = pprice - (pprice * slpct)
	    sl_price_1hr = pprice - (pprice * slpct1hr)
	else:
	    tgt_price = pprice - (pprice * tpct)
	    sl_price_rest = pprice + (pprice * slpct)
	    sl_price_1hr = pprice + (pprice * slpct1hr)
	#log_it("Sym=%s, ProfitPct=%.2f, Tgt Price = %.2f, SLPct=%.2f, SL Pric = %.2f" % (sym, ProfitPct, tgt_price, SLPct, sl_price))
	i=j+1
	for each_candle in cdata[j+1:]:
	    if DefferredSL:
		if i < 120:
		    sl_price = sl_price_1hr
		else:
		    sl_price = sl_price_rest
	    else:
		sl_price = sl_price_rest
	    cj = float(each_candle[idx_close])
	    hj = float(each_candle[idx_high])
	    lj = float(each_candle[idx_low])
	    # c h l o format, retrive the low and high
	    for idx in (3, 2, 1, 0):
		if sq_off == 0:
		    break
		if ((call == 'Buy' and float(each_candle[idx]) <= sl_price) or (call == 'Sell' and float(each_candle[idx]) >= sl_price)):
		    sl_count+=1
		    if i == 1:
			sl_price1 = float(each_candle[idx])
		    else:
			sl_price1 = sl_price
		    loss = (cps*abs((sl_price1-pprice)/pprice))
		    GROSS -= loss
		    log_it("%s: SL Hit: %s: Candle %d, GROSS=%.2f, SLPct=%.2f%%, PurchasePrice=%.2f, SL=%.2f, ActualSLPct=%.2f%%, ActualLoss=%.2f, G-LOSS=%.2f" % (sym, GetHumanDate(UTC), i, GROSS, slpct*100, pprice, sl_price, ((float(each_candle[idx])-pprice)/pprice)*100, loss, GROSS-loss))
		    #log_it("%s: %s => PossibleTgtHits = %s" % (sym, GetHumanDate(UTC), ','.join(pft_list)))
		    sq_off=0
		    SYM_DATA = {'PPRICE': pprice, 'SL': sl_price1, 'ASLPCT': abs((sl_price1-pprice)/pprice)*100, 'ATGT': 0, 'BuyTGTPCT': BuyParams['ProfitPct'], 'SellTGTPCT': SellParams['ProfitPct'], 'SQO': 0, 'SQOPCT': 0, 'CHLO1': cdata[0], 'CHLO2': cdata[1], 'SL_PCT': slpct*100, 'ProfitPct': tpct*100, 'VolCheck': 'CandleVolume > Buy(%.2f%%)/Sell(%.2f%%) of YesterdaysVolume' % (BuyParams['VolCheck'], SellParams['VolCheck']), 'CptCheck': 'Open > Buy(%.2f%%) or < Sell(%.2f%%) of PrevClose' % (BuyParams['CptCheck'], SellParams['CptCheck']), 'PriceChoice': PriceFixing_list[PriceFixing], 'VCPT': vcpt, 'PCPT': pcpt}
		    break
		if ((call == 'Buy' and float(each_candle[idx]) >= tgt_price) or (call == 'Sell' and float(each_candle[idx]) <= tgt_price)):
		    tgt_count+=1
		    log_it("%s: TGT Hit: %s: GROSS=%.2f, ProfitPct=%.2f%%, PurchasePrice=%.2f, TGT=%.2f, G+Earning=%.2f" % (sym, GetHumanDate(UTC), GROSS, tpct*100, pprice, tgt_price, GROSS+(cps*tpct)))
		    #log_it("%s: %s => PossibleSLHits = %s" % (sym, GetHumanDate(UTC), ','.join(sl_list)))
		    GROSS += (cps*tpct)
		    sq_off=0
		    SYM_DATA = {'PPRICE': pprice, 'SL': 0, 'ASLPCT': 0, 'ATGT': tgt_price, 'BuyTGTPCT': BuyParams['ProfitPct'], 'SellTGTPCT': SellParams['ProfitPct'], 'SQO': 0, 'SQOPCT': 0, 'CHLO1': cdata[0], 'CHLO2': cdata[1], 'SL_PCT': slpct*100, 'ProfitPct': tpct*100, 'VolCheck': 'CandleVolume > Buy(%.2f%%)/Sell(%.2f%%) of YesterdaysVolume' % (BuyParams['VolCheck'], SellParams['CptCheck']), 'CptCheck': 'Open > Buy (%.2f%%) or < Sell(%.2f%%) of PrevClose' % (BuyParams['CptCheck'], SellParams['CptCheck']), 'PriceChoice': PriceFixing_list[PriceFixing], 'VCPT': vcpt, 'PCPT': pcpt}
		    break
		if call == 'Buy':
		    if float(each_candle[idx]) < pprice:
			sl_list.append("%.2f%%" % (((float(each_candle[idx])-pprice)/pprice)*100))
		    if float(each_candle[idx]) > pprice:
			pft_list.append("%.2f%%" % (((float(each_candle[idx])-pprice)/pprice)*100))
		elif call == 'Sell':
		    if float(each_candle[idx]) < pprice:
			pft_list.append("%.2f%%" % ((((pprice-float(each_candle[idx]))/pprice))*100))
		    if float(each_candle[idx]) > pprice:
			sl_list.append("%.2f%%" % ((((pprice-float(each_candle[idx]))/pprice))*100))
	    if sq_off == 0:
		break
	    i+=1
	if sq_off == 1:
	    sq_off_change = (cps*(((lj+cj)/2)-pprice)/pprice)
	    log_it("%s: SquareOff Hit: %d: %s: Purchase Price=%.2f, Low=%.2f, High=%.2f, Close=%.2f, CutOffPrice=%.2f, GROSS=%.2f, CPCT=%.2f, G+Earning=%.2f" % (sym, i, GetHumanDate(UTC), pprice, lj, hj, cj, (lj+cj)/2, GROSS, sq_off_change, GROSS + sq_off_change))
	    sq_count+=1
	    GROSS += sq_off_change
	    SYM_DATA = {'PPRICE': pprice, 'SL': 0, 'ASLPCT': 0, 'ATGT': 0, 'BuyTGTPCT': BuyParams['ProfitPct'], 'SellTGTPCT': SellParams['ProfitPct'], 'SQO': sq_off_change, 'SQOPCT': (((lj+cj)/2)-pprice)/pprice, 'CHLO1': cdata[0], 'CHLO2': cdata[1], 'SL_PCT': slpct*100, 'ProfitPct': tpct*100, 'VolCheck': 'CandleVolume > Buy(%.2f%%)/Sell(%.2f%%) of YesterdaysVolume' % (BuyParams['VolCheck'], SellParams['VolCheck']), 'CptCheck': 'Open > Buy(%.2f%%) or < Sell(%.2f%%) of PrevClose' % (BuyParams['CptCheck'], SellParams['CptCheck']), 'PriceChoice': PriceFixing_list[PriceFixing], 'VCPT': vcpt, 'PCPT': pcpt}
	    #log_it("%s: %s => PossibleSLHits = %s" % (sym, GetHumanDate(UTC), ','.join(sl_list)))

	n50=''
	n100=''
	n200=''
	if sym in Nifty50:
	    n50="True"
	if sym in Nifty100:
	    n100="True"
	if sym in Nifty200:
	    n200="True"
	gap_up_down = ""
	if (float(cdata[0][idx_open]) > float(OneYearData[sym][prev_utcl][idx_high])):
	    gap_up_down = "UP"
	elif (float(cdata[0][idx_open]) < float(OneYearData[sym][prev_utcl][idx_low])):
	    gap_up_down = "DOWN"
	if call == 'Buy':
	    gap = ((float(cdata[0][idx_open])-float(OneYearData[sym][prev_utcl][idx_high]))/float(OneYearData[sym][prev_utcl][idx_high]))*100
	elif call == 'Sell':
	    gap = ((float(cdata[0][idx_open])-float(OneYearData[sym][prev_utcl][idx_low]))/float(OneYearData[sym][prev_utcl][idx_low]))*100

	if SYM_DATA['SL'] != 0:
	    #log_it("SL, %s, %s[%s], GAP=%s[%.2f%%], PCLOSE=%.2f, PurchasePrice=%.2f, VCPT=%s, PCPT=%s, PossibleTgtHits = %s, PDAY_CHLO=%s, CHLO1=%s, CHLO2=%s, CandleVCPT=%.2f, CandlePCPT=%.2f" % (GetHumanDate(UTC), call, sym, gap_up_down, gap, pclose, pprice, vcpt, pcpt, ':'.join(pft_list), ':'.join(OneYearData[sym][prev_utcl]), ':'.join(cdata[0]), ':'.join(cdata[1]), (float(cdata[1][idx_vol])/float(cdata[0][idx_vol]))*100, ((float(cdata[1][idx_close])-float(cdata[1][idx_open]))/float(cdata[1][idx_open]))*100))
	    log_it("SL, %s, Buy/Sell Candle=%d, Sell/Buy Candle=%d, %s, %s, %s, %.2f%%, %.2f, %.2f, %s, %s, %s, %s, %s, %s, %.2f, %.2f, %s, %s, %s, %s, %.2f%%, %.2f%%" % (GetHumanDate(UTC), j, i, call, sym, gap_up_down, gap, pclose, pprice, vcpt, pcpt, ':'.join(pft_list), ':'.join(OneYearData[sym][prev_utcl]), ':'.join(cdata[0]), ':'.join(cdata[1]), (float(cdata[1][idx_vol])/float(cdata[0][idx_vol]))*100, ((float(cdata[1][idx_close])-float(cdata[1][idx_open]))/float(cdata[1][idx_open]))*100, n50, n100, n200, MIS[sym], v2cpt, p2cpt))

	if SYM_DATA['ATGT'] != 0:
	    log_it("TGT, %s, Buy/Sell Candle=%d, Sell/Buy Candle=%d, %s, %s, %s, %.2f%%, %.2f, %.2f, %s, %s, %s, %s, %s, %s, %.2f, %.2f, %s, %s, %s, %s, %.2f%%, %.2f%%" % (GetHumanDate(UTC), j, i, call, sym, gap_up_down, gap, pclose, pprice, vcpt, pcpt, "", ':'.join(OneYearData[sym][prev_utcl]), ':'.join(cdata[0]), ':'.join(cdata[1]), (float(cdata[1][idx_vol])/float(cdata[0][idx_vol]))*100, ((float(cdata[1][idx_close])-float(cdata[1][idx_open]))/float(cdata[1][idx_open]))*100, n50, n100, n200, MIS[sym], v2cpt, p2cpt))
	    #log_it("TGT, %s, %s[%s], GAP=%s[%.2f%%], PCLOSE=%.2f, PurchasePrice=%.2f, VCPT=%s, PCPT=%s, PossibleTgtHits = %s, PDAY_CHLO=%s, CHLO1=%s, CHLO2=%s, CandleVCPT=%.2f, CandlePCPT=%.2f" % (GetHumanDate(UTC), call, sym, gap_up_down, gap, pclose, pprice, vcpt, pcpt, "", ':'.join(OneYearData[sym][prev_utcl]), ':'.join(cdata[0]), ':'.join(cdata[1]), (float(cdata[1][idx_vol])/float(cdata[0][idx_vol]))*100, ((float(cdata[1][idx_close])-float(cdata[1][idx_open]))/float(cdata[1][idx_open]))*100))


	if UTC not in MasterData.keys():
	    MasterData[UTC] = {}
	MasterData[UTC][sym] = SYM_DATA

def OHOLStrategy(strategy, sym, UTC, pUTC):
    global RsymsBuy
    global RsymsSell

    if sym in IgnoreSyms:
	return

    if today:
	if UTC not in TodayData[sym].keys():
	    return
	cdata = TodayData[sym][UTC]
    else:
	cdata = DailyData[sym][UTC]
	prev_utc = GetPrevUTC(DailyData[sym], UTC)
	if prev_utc is None:
	    log_it("Could not find previous Nifty for %s" % GetHumanDate(UTC))
	    return

    c1 = float(cdata[0][idx_close])
    h1 = float(cdata[0][idx_high])
    l1 = float(cdata[0][idx_low])
    o1 = float(cdata[0][idx_open])

    if o1 != l1 and o1 != h1:
	return

    if (1 == 0 and o1 == l1 and o1 == h1):
	return

    if len(cdata) < 4:
	return

    c2 = float(cdata[1][idx_close])
    h2 = float(cdata[1][idx_high])
    l2 = float(cdata[1][idx_low])
    o2 = float(cdata[1][idx_open])

    c3 = float(cdata[2][idx_close])
    h3 = float(cdata[2][idx_high])
    l3 = float(cdata[2][idx_low])
    o3 = float(cdata[2][idx_open])

    c4 = float(cdata[3][idx_close])
    h4 = float(cdata[3][idx_high])
    l4 = float(cdata[3][idx_low])
    o4 = float(cdata[3][idx_open])

    if today:
	OneYearData[sym] = Get_1Y_Data(sym)
	pUTC = GetPrevUTC(OneYearData[sym], pUTC)

    pclose = float(OneYearData[sym][pUTC][0])
    pcpt = ((o1-pclose)/pclose)*100
    vcpt = (int(cdata[0][idx_vol])/int(OneYearData[sym][pUTC][4]))*100
    v2cpt = (int(cdata[1][idx_vol])/int(OneYearData[sym][pUTC][idx_vol]))*100
    p2cpt = ((float(cdata[1][idx_open])-pclose)/pclose)*100

    if 1 == 1:
	# Buy
	if o1 == l1 and pclose < o1:
	    gap = ((float(cdata[0][idx_open])-float(OneYearData[sym][pUTC][idx_high]))/float(OneYearData[sym][pUTC][idx_high]))*100
	    if 1 == 0 and abs(gap) > 2.5 and vcpt < 2:
		reject("abs(gap) > 3 and vcpt < 3", sym, vcpt, pcpt, v2cpt, p2cpt, gap)
		return

	    if 1 == 1 and c2 < c1:
	    #if 1 == 1 and c2 < c1:
		log_it("c2+(0.1 of c2) < c1 (%s, c2=%.2f, 0.1c2=%.2f, c1=%.2f)" % (sym, c2, (c2+(c2*(0.1/100))), c1))
		return

	    if 1 == 0 and pcpt > 3 and vcpt < 2.5:
		reject("p2cpt < 0.8", sym, vcpt, pcpt, v2cpt, p2cpt, gap)
		return

	    #if vcpt > 5.5 and pcpt <= 2:
		#return

	    #if vcpt > 8 and pcpt < 2.3:
		#return

	# Sell
	if o1 == h1 and pclose > o1:
	    gap = ((float(cdata[0][idx_open])-float(OneYearData[sym][pUTC][idx_low]))/float(OneYearData[sym][pUTC][idx_low]))*100
	    if 1 == 0 and abs(gap) > 3 and vcpt < 3:
		return

	    if 1 == 0 and c2 > c1:
	    #if 1 == 1 and (abs(p2cpt) < 1):
		reject("v2cpt < 1.1", sym, vcpt, pcpt, v2cpt, p2cpt, gap)
		return

	    if 1 == 0 and abs(v2cpt) < 0.7:
		reject("v2cpt < 1.1", sym, vcpt, pcpt, v2cpt, p2cpt, gap)
		return

	    if 1 == 0 and v2cpt < 0.8 and abs(p2cpt) > 1:
		#print "SOMA_DEBUG: 1: Rejecting", sym, vcpt, pcpt, "V2CPT:", v2cpt, p2cpt, gap
		return

	    #if vcpt > 12 and abs(pcpt) > 4:
		#print "SOMA_DEBUG:", sym, GetHumanDate(UTC), vcpt, pcpt
		#return

    if strategy == 'Buy' or strategy == 'Both':
	if o1 == l1 and pclose < o1 and abs(pcpt) > BuyParams['CptCheck']:
	    volc2 = c2+(c2*BuyParams['VolBuffer'])
	    vol5c2 = c2+(c2*BuyParams['Vol5Buffer'])
	    if (vcpt >= BuyParams['Vol5Check'] and vol5c2 >= o1) or (vcpt >= BuyParams['VolCheck'] and vcpt <= BuyParams['Vol5Check'] and volc2 >= o1):
		log_it("%s: Buy %s @ %.2f (o1=%.2f, l1=%.2f, pclose=%.2f, vcpt=%.2f, pcpt=%.2f%%, v2cpt=%.2f%%, p2cpt=%.2f%%, volc2=%.2f%%, vol5c2=%.2f%%, c2=%.2f%%)" % (GetHumanDate(UTC), sym, c4, o1, l1, pclose, vcpt, pcpt, v2cpt, p2cpt, volc2, vol5c2, c2))
		RsymsBuy.append(sym)
		RsymsData[sym] = {}
		RsymsData[sym]['PRICE'] = c4
		if vcpt >= BuyParams['Vol5Check']:
		    (RsymsData[sym]['TGT'], RsymsData[sym]['SL']) = GetAbsolutes(c4, BuyParams['Vol5ProfitPct'], BuyParams['Vol5SLPct'])
		else:
		    (RsymsData[sym]['TGT'], RsymsData[sym]['SL']) = GetAbsolutes(c4, BuyParams['ProfitPct'], BuyParams['SLPct'])
	    #else:
		#print "SOMA_DEBUG: 2", sym, vcpt, vol5c2, o1, c1, volc2, (vcpt >= 5 and vol5c2 >= o1), (vcpt >= VolCheck and vcpt <= 5 and volc2 >= o1)

    if strategy == 'Sell' or strategy == 'Both':
	if o1 == h1 and pclose > o1 and abs(pcpt) > SellParams['CptCheck']:
	    volc2 = c2-(c2*SellParams['VolBuffer'])
	    vol5c2 = c2-(c2*SellParams['Vol5Buffer'])
	    if (vcpt >= SellParams['Vol5Check'] and vol5c2 <= o1) or (vcpt >= SellParams['VolCheck'] and vcpt <= SellParams['Vol5Check'] and volc2 <= o1):
		log_it("%s: Sell %s @ %.2f (o1=%.2f, h1=%.2f, pclose=%.2f, vcpt=%.2f, pcpt=%.2f%%, v2cpt=%.2f%%, p2cpt=%.2f%%, volc2=%.2f%%, vol5c2=%.2f%%, c2=%.2f%%)" % (GetHumanDate(UTC), sym, c4, o1, h1, pclose, vcpt, pcpt, v2cpt, p2cpt, volc2, vol5c2, c2))
		RsymsSell.append(sym)
		RsymsData[sym] = {}
		RsymsData[sym]['PRICE'] = c4
		if vcpt >= SellParams['Vol5Check']:
		    (RsymsData[sym]['TGT'], RsymsData[sym]['SL']) = GetAbsolutes(c4, SellParams['Vol5ProfitPct'], SellParams['Vol5SLPct'])
		else:
		    (RsymsData[sym]['TGT'], RsymsData[sym]['SL']) = GetAbsolutes(c4, SellParams['ProfitPct'], SellParams['SLPct'])

ndays = 1

if __name__=="__main__":
    Nsyms = []
    # Get Nifty symbols
    if len(sys.argv) > 0:
	i=1
	while i <= len(sys.argv[1:]):
	    if sys.argv[i] == "--verbose":
		verbose=1
	    elif sys.argv[i] == "--scrips":
		Nsyms.extend(sys.argv[i+1].split(','))
	    elif sys.argv[i] == "--profit-sl-combo":
		pcts = sys.argv[i+1]
		i+=1
	    elif sys.argv[i] == "--profit":
		ProfitPct = float(sys.argv[i+1])/100;
		i+=1
	    elif sys.argv[i] == "--sl":
		SLPct = float(sys.argv[i+1])/100;
		i+=1
	    elif sys.argv[i] == "--no-cache":
		LOCAL_CACHE=False
		i+=1
	    elif sys.argv[i] == '--today':
		dt = datetime.datetime.today();
		y = int(dt.strftime("%Y"))
		m = int(dt.strftime("%m"))
		d = int(dt.strftime("%d"))
		if not LOCAL_CACHE and MarketHours() == True:
		    LOCAL_CACHE=False
		one_day_scan=1
		today=1
	    elif sys.argv[i] == '--from':
		fromdt = datetime.datetime.strptime(sys.argv[i+1], '%d/%m/%Y')
		fromy = int(fromdt.strftime("%Y"))
		fromm = int(fromdt.strftime("%m"))
		fromd = int(fromdt.strftime("%d"))
		i+=1
	    elif sys.argv[i] == '--to':
		todt = datetime.datetime.strptime(sys.argv[i+1], '%d/%m/%Y')
		toy = int(todt.strftime("%Y"))
		tom = int(todt.strftime("%m"))
		tod = int(todt.strftime("%d"))
		i+=1
	    elif sys.argv[i] == '--yesterday':
		ndays=6
		dt = datetime.datetime.today() - datetime.timedelta(1);
		y = int(dt.strftime("%Y"))
		m = int(dt.strftime("%m"))
		d = int(dt.strftime("%d"))
		one_day_scan=1
	    elif sys.argv[i] == '--Both-Buy-And-Sell':
		variance = "Both-Buy-And-Sell"
	    elif sys.argv[i] == '--Go_with_Nifty':
		variance = "Go_with_Nifty"
	    elif sys.argv[i] == '--Always-Buy':
		variance = "Always-Buy"
	    elif sys.argv[i] == '--all':
		variance = "ALL"
	    elif sys.argv[i] == '--no-leverage':
		Leverage=False
	    elif sys.argv[i] == '--no-back-testing':
		BackTesting=False
	    i+=1

    if len(Nsyms) == 0:
	Nsyms.extend(SCRIPS)
	#Nsyms.extend(Nifty100)

    TODAY = datetime.datetime.today().strftime("%Y-%m-%d")
    for sym in Nsyms:
	# Collect Candle data for the each symbol for last 2 months and 1 year
	OneYearData[sym] = Get_1Y_Data(sym)
	if today == True:
	    TodayData[sym] = GetScripCandleData('1d', sym)
	else:
	    DailyData[sym] = GetScripCandleData('60d', sym)

    # Collect Nifty Candle data for the same period and interval as symbols.
    NiftyIndex1YCandle = Get_1Y_Data('NIFTY')
    NiftyIndex60DCandle = GetScripCandleData('60d', 'NIFTY')
    if today:
	NiftyIndexTodayCandle = GetScripCandleData('1d', 'NIFTY')

    Nifty50 = GetNiftyScrips(50)
    Nifty100 = GetNiftyScrips(100)
    Nifty200 = GetNiftyScrips(200)

    if today == False:
	log_it("Trade, Candle, Date, Call, Scrip, GAP UP/DOWN, GAP, PCLOSE, PurchasePrice, VCPT, PCPT, PossibleTgtHits, PDAY_CHLO, CHLO1, CHLO2, CandleVCPT, CandlePCPT, N50, N100, N200")
    MainLoop('Both')

