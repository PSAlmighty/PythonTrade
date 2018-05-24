#!/usr/bin/python -u

from __future__ import division

import json, os, sys, datetime, csv, urllib2
#import requests, io
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy

MasterData = {}
 
verbose=0
idx_close = 0
idx_high = 1
idx_low = 2
idx_open = 3
idx_vol = 4
one_day_scan=0
y = 2018
m = 4
d = 15
CAPITAL=100000
CPS=0
GROSS=CAPITAL
today=False
variance = "Both-Buy-And-Sell"
RsymsSell = []
RsymsSellDetail = []
RsymsBuy = []
RsymsBuyDetail = []
BackTesting = True
#Interval = 960
#Interval = 120
Interval = 60
TodayData = {}
OneYearData = {}
SixtyDaysData = {}
sl_count = 0
tgt_count = 0
sq_count = 0
ProfitPct = 1.1
SLPct = 1.1
Leverage=True
pcts = ""
LOCAL_CACHE=True

NDays = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
Months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

#SCRIPS=['YESBANK']
SCRIPS=['YESBANK', 'TATASTEEL', 'STAR', 'SBIN', 'RELIANCE', 'POWERGRID', 'PETRONET', 'ONGC', 'OIL', 'MARUTI', 'M&M', 'LT', 'KTKBANK', 'KOTAKBANK', 'JSWSTEEL', 'ITC', 'IOC', 'INDUSINDBK', 'IGL', 'ICICIBANK', 'HINDUNILVR', 'HEROMOTOCO', 'HDFCBANK', 'HDFC', 'GAIL', 'FEDERALBNK', 'DCBBANK', 'DABUR', 'COLPAL', 'COALINDIA', 'CIPLA', 'CEATLTD', 'CASTROLIND', 'CANBK', 'BPCL', 'BOSCHLTD', 'BHARTIARTL', 'BHARATFORG', 'BATAINDIA', 'BANKBARODA', 'BAJAJ-AUTO', 'AXISBANK', 'ASIANPAINT', 'ASHOKLEY', 'ARVIND', 'APOLLOTYRE', 'APOLLOHOSP', 'AMBUJACEM', 'AMARAJABAT', 'ACC', 'UNIONBANK', 'KSCL', 'ICIL', 'ZEEL', 'VEDL', 'UPL', 'ULTRACEMCO', 'UBL', 'TVSMOTOR', 'TITAN', 'TATAMTRDVR', 'TATAMOTORS', 'TATACHEM', 'SRTRANSFIN', 'SRF', 'RECLTD', 'PTC', 'PIDILITIND', 'NTPC', 'NMDC', 'NCC', 'MOTHERSUMI', 'MCLEODRUSS', 'MCDOWELL-N', 'MARICO', 'M&MFIN', 'LUPIN', 'LICHSGFIN', 'L&TFH', 'JUBLFOOD', 'JISLJALEQS', 'INDIACEM', 'HINDZINC', 'HINDPETRO', 'HINDALCO', 'HEXAWARE', 'GRASIM', 'GLENMARK', 'EXIDEIND', 'ENGINERSIN', 'BRITANNIA', 'BHEL', 'GRANULES', 'GOLDBEES', 'BANKBEES', 'WIPRO', 'VOLTAS', 'TECHM', 'TCS', 'TATAPOWER', 'TATAGLOBAL', 'TATAELXSI', 'TATACOMM', 'SIEMENS', 'RELINFRA', 'RELCAPITAL', 'PFC', 'PAGEIND', 'NIITTECH', 'MINDTREE', 'IRB', 'INFY', 'INFRATEL', 'IBULHSGFIN', 'HCLTECH', 'HAVELLS', 'DISHTV', 'CONCOR', 'CESC', 'CADILAHC', 'BIOCON', 'BEML', 'BEL', 'TORNTPOWER', 'OFSS', 'KPIT', 'JINDALSTEL', 'CGPOWER', 'CENTURYTEX', 'BHARATFIN', 'AJANTPHARM', 'WOCKPHARMA', 'TORNTPHARM', 'SUNPHARMA', 'ORIENTBANK', 'IDEA', 'GODREJIND', 'DRREDDY', 'DLF', 'DIVISLAB', 'DHFL', 'BANKINDIA', 'BAJFINANCE', 'AUROPHARMA']

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

def log(str):
    if verbose:
	print str

def GetHumanDate(utc, time=0):
    if time == 1:
	return datetime.datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d %H:%M:%S')
    else:
	return datetime.datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d')

def CalculateSMA(sym, prev_utc):
    sma5=0
    sma10=0
    sma20=0
    sma30=0
    i=1
    keys = OneYearData[sym].keys()
    while i <= 20:
	if prev_utc not in keys:
	    prev_utc = GetPrevUTC(OneYearData[sym], prev_utc)
	    if prev_utc is None:
		return [0, 0, 0, 0]
	close = float(OneYearData[sym][prev_utc][0])
	if i <= 5:
	    sma5+=close
	if i <= 10:
	    sma10+=close
	if i <= 20:
	    sma20+=close
	#if i <= 30:
	    #sma30+=close
	prev_utc = GetPrevUTC(OneYearData[sym], prev_utc)
	i+=1
    #log("%s[5,10,20,30] = [%d, %d, %d, %d]" % (sym, sma5/5, sma10/10, sma20/20, sma30/30))
    return [sma5/5, sma10/10, sma20/20, sma30/30]

VOL_Check=1
VOL_Check_Values=[1, 1.5, 2, 2.5, 3, 3.5, 4]
CPT_Check=4
CPT_Check_Values = [0, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
C_Check=2
P_Choice=2

VOL_check_list = ['CandleVolume > 1% of YesterdaysVolume', 'CandleVolume > 1.5% of YesterdaysVolume', 'CandleVolume > 2% of YesterdayLastCandleVolume', 'CandleVolume > 2.5% of YesterdaysVolume', 'CandleVolume > 3% of YesterdaysVolume', 'CandleVolume > 3.5% of YesterdaysVolume']
def VolCheck(c, sym, pUTC, prev_utc, c_candle_vol):
    # prev_utc will refer to previous day 3:30 UTC
    # pUTC will refer to previous day 9:15
    #print GetHumanDate(prev_utc), GetHumanDate(pUTC)
    pvol = int(OneYearData[sym][pUTC][4])
    p_candle_vol = int(SixtyDaysData[sym][prev_utc][-1][4])
    if c == 0 and (c_candle_vol/pvol)*100 > 2:
	#log("%s: PreviousDayVolume=%d, CurrentCandleVolume=%d" % (sym, pvol, c_candle_vol))
	return True
    if c == 1 and (c_candle_vol/pvol)*100 > 1:
	#log("%s: PreviousDayVolume=%d, CurrentCandleVolume=%d" % (sym, pvol, c_candle_vol))
	return True
    if c == 2 and c_candle_vol > p_candle_vol:
	#log("%s: PreviousDayLastCandleVolume=%d, CurrentCandleVolume=%d" % (sym, p_candle_vol, c_candle_vol))
	return True
    if c == 3 and (c_candle_vol/p_candle_vol)*100 > 1.5:
	#log("%s: PreviousDayLastCandleVolume=%d, CurrentCandleVolume=%d" % (sym, p_candle_vol, c_candle_vol))
	return True
    if c == 4 or c == 5:
	i=1
	vol5=0
	while i < 5:
	    vol5 += int(SixtyDaysData[sym][prev_utc][-i][4])
	    i+=1
	avg_vol5 = vol5/(i-1)
	if c == 4 and c_candle_vol > avg_vol5:
	    #log("%s: PreviousDayLast5CandleVolumeAvg=%d, CurrentCandleVolume=%d" % (sym, avg_vol5, c_candle_vol))
	    return True
	if c == 5 and (c_candle_vol/avg_vol5)*100 > 1.5:
	    #log("%s: PreviousDayLast5CandleVolumeAvg=%d, CurrentCandleVolume=%d" % (sym, avg_vol5, c_candle_vol))
	    return True
    if c == 6 and (c_candle_vol/pvol)*100 > 1.5:
	#log("%s: PreviousDayVolume=%d, CurrentCandleVolume=%d" % (sym, pvol, c_candle_vol))
	return True
    if c == 7 and (c_candle_vol/pvol)*100 > 3:
	#log("%s: PreviousDayVolume=%d, CurrentCandleVolume=%d" % (sym, pvol, c_candle_vol))
	return True
    if c == 8 and (c_candle_vol/pvol)*100 > 3.5:
	#log("%s: PreviousDayVolume=%d, CurrentCandleVolume=%d" % (sym, pvol, c_candle_vol))
	return True
    return False

CPT_check_list = ['Open > (Buy) or < (Sell) 0% of PrevClose', 'Open > (Buy) or < (Sell) 0.25% of PrevClose', 'Open > (Buy) or < (Sell) 0.1% of PrevClose', 'Open > (Buy) or < (Sell) 0.2% of PrevClose', 'Open > (Buy) or < (Sell) 0.3% of PrevClose', 'Open > (Buy) or < (Sell) 0.4% of PrevClose', 'Open > (Buy) or < (Sell) 0.5% of PrevClose']
def CPTCheck(cpt):
    if CPT_Check == 0:
	return 0
    elif CPT_Check == 1:
	return abs(cpt) > 0.25
    elif CPT_Check == 2:
	return abs(cpt) > 0.1
    elif CPT_Check == 3:
	return abs(cpt) > 0.2
    elif CPT_Check == 4:
	return abs(cpt) > 0.3
    elif CPT_Check == 5:
	return abs(cpt) > 0.4
    elif CPT_Check == 6:
	return abs(cpt) > 0.5

P_Check_list = ['None', '9:17th Candle', '9:18th Candle']
F_Check = 0
#F_Check_list = ['Regular', 'Toggle']
P_Choice_list = ['(l+h+c)/3', '(h+c)/2', 'c']
CCheck_list = ['Echeck Disabled', '(Buy)c2 > c1 or (Sell)c2 < c1', '(Buy)c2+0.1%ofc1 > c1 or (Sell)c1+0.1%ofc1 > c2', '(Buy)h2 > h1 or (Sell) l2 < l1', '(Buy)l2 < l1 and h2 > h1 and o2 > o1 or (Sell)l2 > l1 and h2 < h and o2 < o1)']
def CCheck(call, c1, c2):
    o1 = float(c1[idx_open])
    l1 = float(c1[idx_low])
    h1 = float(c1[idx_high])
    c1 = float(c1[idx_close])
    o2 = float(c2[idx_open])
    l2 = float(c2[idx_low])
    h2 = float(c2[idx_high])
    c2 = float(c2[idx_close])
    if C_Check == 0:
	return True
    elif C_Check == 1:
	if call == 'Buy':
	    return (c2 > c1)
	else:
	    return (c2 < c1)
    elif C_Check == 2:
	if call == 'Buy':
	    return ((c2+(c1*(0.1/100))) > c1)
	else:
	    return (c2 < c1+(c1*(0.1/100)))
    elif C_Check == 3:
	if call == 'Buy':
	    return (h2 > h1)
	else:
	    return (l2 < l1)
    elif C_Check == 4:
	if call == 'Buy':
	    return (l2 < l1 and h2 > h1 and o2 > o1)
	else:
	    return (l2 > l1 and h2 < h and o2 < o1)

def IntradayStrategy(strategy, sym, UTC, pUTC):
    global RsymsBuy
    global RsymsSell

    if today:
	cdata = TodayData[sym][UTC]
    else:
	cdata = SixtyDaysData[sym][UTC]
    c1 = float(cdata[0][idx_close])
    h1 = float(cdata[0][idx_high])
    l1 = float(cdata[0][idx_low])
    o1 = float(cdata[0][idx_open])
    c_candle_vol=int(cdata[0][idx_vol])
    prev_utc = GetPrevUTC(SixtyDaysData[sym], UTC)
    if prev_utc is None:
	#log("IntradayStrategy: Previous utc is not available for %s(%s)" % (sym, GetHumanDate(UTC)))
	return

    pclose = float(OneYearData[sym][pUTC][0])
    cpt = ((o1-pclose)/pclose)*100
    pvol = int(OneYearData[sym][pUTC][4])
    c2 = float(cdata[1][idx_close])

    if F_Check == 0:
	if strategy == 'Buy' or strategy == 'Both':
	    if o1 == l1 and pclose < o1 and (c_candle_vol/pvol)*100 > VOL_Check_Values[VOL_Check] and abs(cpt) > CPT_Check_Values[CPT_Check] and CCheck('Buy', cdata[0], cdata[1]):
		RsymsBuy.append(sym)

	if strategy == 'Sell' or strategy == 'Both':
	    if o1 == h1 and pclose > o1 and (c_candle_vol/pvol)*100 > VOL_Check_Values[VOL_Check] and abs(cpt) > CPT_Check_Values[CPT_Check] and CCheck('Sell', cdata[0], cdata[1]):
		RsymsSell.append(sym)
    else:
	if strategy == 'Buy' or strategy == 'Both':
	    if o1 == l1 and (c_candle_vol/pvol)*100 > VOL_Check_Values[VOL_Check] and abs(cpt) > CPT_Check_Values[CPT_Check] and CCheck('Buy', cdata[0], cdata[1]):
		if pclose < o1:
		    RsymsBuy.append(sym)
		else:
		    RsymsSell.append(sym)

	if strategy == 'Sell' or strategy == 'Both':
	    if o1 == h1 and (c_candle_vol/pvol)*100 > VOL_Check_Values[VOL_Check] and abs(cpt) > CPT_Check_Values[CPT_Check] and CCheck('Sell', cdata[0], cdata[1]):
		if pclose < o1:
		    RsymsBuy.append(sym)
		else:
		    RsymsSell.append(sym)

def BackTest(call, UTC, prev_utc, cpshare):
    global sl_count
    global tgt_count
    global sq_count
    global GROSS

    if C_Check == 0:
	pcandle = 1
    else:
	pcandle = P_Candle

    if call == 'Buy':
	syms = RsymsBuy
    else:
	syms = RsymsSell

    for sym in syms:
	cps = cpshare
	if Leverage:
	    if sym in MIS.keys():
		cps *= int(MIS[sym])

	sq_off=1
	pft_list = []
	sl_list = []
	if today:
	    cdata = TodayData[sym][UTC]
	else:
	    cdata = SixtyDaysData[sym][UTC]
	c = float(cdata[pcandle][idx_close])
	h = float(cdata[pcandle][idx_high])
	low = float(cdata[pcandle][idx_low])
	o = float(cdata[pcandle][idx_open])
	if P_Choice == 0:
	    pprice = float(c+h+low)/3
	elif P_Choice == 1:
	    pprice = float(c+h)/2
	elif P_Choice == 2:
	    pprice = c
	bought=False
	j=pcandle+1;
	while (j<(pcandle+30)):
	    if call == 'Buy':
		if (pprice >= cdata[j][idx_low]):
		    #or pprice == cdata[j][idx_open] or pprice == cdata[j][idx_close]:
		    bought=True
		    print "Decided the price @ %d candle and bought it @ %d candle" % (pcandle, j)
		    break
	    elif call == 'Sell':
		if pprice <= cdata[j][idx_high]:
		    #or pprice <= cdata[j][idx_high] or pprice == cdata[j][idx_open] or pprice == cdata[j][idx_close]:
		    bought=True
		    print "Decided the price @ %d candle and sold it @ %d candle" % (pcandle, j)
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
	    #pprice = h
	    tgt_price = pprice + (pprice * ProfitPct)
	    sl_price = pprice - (pprice * SLPct)
	else:
	    #pprice = low
	    tgt_price = pprice - (pprice * ProfitPct)
	    sl_price = pprice + (pprice * SLPct)
	#log("Sym=%s, ProfitPct=%.2f, Tgt Price = %.2f, SLPct=%.2f, SL Pric = %.2f" % (sym, ProfitPct, tgt_price, SLPct, sl_price))
	i=1
	for each_candle in cdata[j+1:]:
	    c1 = float(each_candle[idx_close])
	    h1 = float(each_candle[idx_high])
	    l1 = float(each_candle[idx_low])
	    o1 = float(each_candle[idx_open])
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
		    log("SL Hit: %s: %s => GROSS=%.2f, SLPct=%.2f%%, PurchasePrice=%.2f, SL=%.2f, ActualSLPct=%.2f%%, ActualLoss=%.2f, G-LOSS=%.2f" % (GetHumanDate(UTC), sym, GROSS, SLPct*100, pprice, sl_price, ((float(each_candle[idx])-pprice)/pprice)*100, loss, GROSS-loss))
		    #log("%s: %s => PossibleTgtHits = %s" % (sym, GetHumanDate(UTC), ','.join(pft_list)))
		    sq_off=0
		    SYM_DATA = {'PPRICE': pprice, 'SL': sl_price1, 'SLPCT': abs((sl_price1-pprice)/pprice), 'TGT': 0, 'TGTPCT': 0, 'SQO': 0, 'SQOPCT': 0, 'CHLO1': cdata[0], 'CHLO2': cdata[1], 'SL_PCT': SLPct, 'ProfitPct': ProfitPct, 'VolCheck': VOL_check_list[VOL_Check], 'CptCheck': CPT_check_list[CPT_Check], 'PriceChoice': P_Choice_list[P_Choice]}
		    break
		if ((call == 'Buy' and float(each_candle[idx]) >= tgt_price) or (call == 'Sell' and float(each_candle[idx]) <= tgt_price)):
		    tgt_count+=1
		    log("TGT Hit: %s: %s => GROSS=%.2f, ProfitPct=%.2f%%, PurchasePrice=%.2f, TGT=%.2f, G+Earning=%.2f" % (GetHumanDate(UTC), sym, GROSS, ProfitPct*100, pprice, tgt_price, GROSS+(cps*ProfitPct)))
		    #log("%s: %s => PossibleSLHits = %s" % (sym, GetHumanDate(UTC), ','.join(sl_list)))
		    GROSS += (cps*ProfitPct)
		    sq_off=0
		    SYM_DATA = {'PPRICE': pprice, 'SL': 0, 'SLPCT': 0, 'TGT': tgt_price, 'TGTPCT': ProfitPct, 'SQO': 0, 'SQOPCT': 0, 'CHLO1': cdata[0], 'CHLO2': cdata[1], 'SL_PCT': SLPct, 'ProfitPct': ProfitPct, 'VolCheck': VOL_check_list[VOL_Check], 'CptCheck': CPT_check_list[CPT_Check], 'PriceChoice': P_Choice_list[P_Choice]}
		    break
		#if call == 'Buy':
		    #if float(each_candle[idx]) < pprice:
			#sl_list.append("%s(%.2f%%)" % (each_candle[idx],((float(each_candle[idx])-pprice)/pprice)*100))
			##sl_list.append("%s" % each_candle[idx])
			#break
		    #if float(each_candle[idx]) > pprice:
			#pft_list.append("%s(%.2f%%)" % (each_candle[idx],((float(each_candle[idx])-pprice)/pprice)*100))
			##pft_list.append("%s" % float(each_candle[idx]))
			#break
		#elif call == 'Sell':
		    #if float(each_candle[idx]) > pprice:
			#sl_list.append("%s(%.2f%%)" % (each_candle[idx],(((pprice-float(each_candle[idx]))/pprice))*100));
			##sl_list.append("%s" % each_candle[idx])
			#break
	    #if float(each_candle[idx]) < pprice:
		#pft_list.append("%s(%.2f%%)" % (each_candle[idx],(((pprice-float(each_candle[idx]))/pprice))*100));
		##pft_list.append("%s" % each_candle[idx])
		#break
	    # 182th Candle is 3:20PM Candle
		#if i == 182:
		#log("%s: CandleTime is %s" % (sym, GetHumanDate(str(int(UTC)+((pcandle-1+i)*Interval)))))
		#break
	    if sq_off == 0:
		break
	    i+=1
	if sq_off == 1:
	    sq_off_change = (cps*(((l1+c1)/2)-pprice)/pprice)
	    log("SquareOff Hit: %d: %s: %s => Purchase Price=%.2f, Low=%.2f, High=%.2f, Close=%.2f, CutOffPrice=%.2f, GROSS=%.2f, CPCT=%.2f, G+Earning=%.2f" % (i, GetHumanDate(UTC), sym, pprice, l1, h1, c1, (l1+c1)/2, GROSS, sq_off_change, GROSS + sq_off_change))
	    sq_count+=1
	    GROSS += sq_off_change
	    SYM_DATA = {'PPRICE': pprice, 'SL': 0, 'SLPCT': 0, 'TGT': 0, 'TGTPCT': 0, 'SQO': sq_off_change, 'SQOPCT': (((l1+c1)/2)-pprice)/pprice, 'CHLO1': cdata[0], 'CHLO2': cdata[1], 'SL_PCT': SLPct, 'ProfitPct': ProfitPct, 'VolCheck': VOL_check_list[VOL_Check], 'CptCheck': CPT_check_list[CPT_Check], 'PriceChoice': P_Choice_list[P_Choice]}
	    #log("%s: %s => PossibleTgtHits = %s" % (sym, GetHumanDate(UTC), ','.join(pft_list)))
	    #log("%s: %s => PossibleSLHits = %s" % (sym, GetHumanDate(UTC), ','.join(sl_list)))
	if UTC not in MasterData.keys():
	    MasterData[UTC] = {}
	MasterData[UTC][sym] = SYM_DATA

def MarketHours():
    tdt = datetime.datetime.today();
    th = int(tdt.strftime("%H"))
    tm = int(tdt.strftime("%M"))
    mins = th*60+tm
    if (mins > 555 and mins < 931):
        return True
    return False

def GetURLData(p, sym):
    if p == '1Y':
	url = 'https://finance.google.com/finance/getprices?x=NSE&q=%s&f=d,c,h,l,o,v&p=%s' % (sym.replace('&','%26'), p)
    else:
	url = 'https://finance.google.com/finance/getprices?x=NSE&q=%s&f=d,c,h,l,o,v&p=%s&i=%s' % (sym.replace('&','%26'), p, Interval)
    response = urllib2.urlopen(url)
    content = csv.reader(response.read().splitlines()[7:])
    return content

def Get_1Y_Data(sym):
    data = {}
    data_cache = {}
    sym_file = "MERGED_DATA/%s.1Y.json" % sym
    #sym_file = "DATA/%s.1Y.json" % sym
    if (today == 0 or LOCAL_CACHE == True) and os.path.exists(sym_file):
	with open(sym_file, 'r') as sym_file_handle:
	    data_cache = json.load(sym_file_handle)
    if LOCAL_CACHE ==  True and len(data_cache) > 0:
	return data_cache
    content = GetURLData('1Y', sym)
    for d in content:
	if d[0][0] == 'a':
	    lutc = d[0].replace('a','');
	    data[lutc] = d[1:]
	else:
	    llutc = str(int(lutc)+(int(d[0])*86400))
	    data[llutc] = d[1:]
    data_new = {key: value for (key, value) in (data_cache.items() + data.items())}
    sym_file = "NEW/%s.1Y.json" % sym
    if os.path.exists(sym_file):
	os.rename(sym_file, "%s.moved" % sym_file)
    with open(sym_file, "w") as sym_file_handle:
	json.dump(data_new, sym_file_handle)
    if data is None:
	exit(0)
    return data

def GetScripCandleData(days, sym):
    data_cache = {}
    sym_cache_file = "MERGED_DATA/%s.%sCandles.json" % (sym, days)
    #sym_cache_file = "DATA/%s.%sCandles.json" % (sym, days)
    if (today == 0 or LOCAL_CACHE == True) and os.path.exists(sym_cache_file):
	with open(sym_cache_file, 'r') as sym_file_handle:
	    data_cache = json.load(sym_file_handle)
	sym_file_handle.close()
    if LOCAL_CACHE ==  True and len(data_cache) > 0:
	#print sym, sorted(data_cache.keys())
	return data_cache
    data = {}
    content = GetURLData(days, sym)
    lutc = 0
    for d in content:
	#print d
	if d[0][0] == 'a':
	    utc = d[0].replace('a', '')
	    rutc = int(utc)
	else:
	    utc = rutc + (int(d[0]) * Interval)
	hr = int(datetime.datetime.fromtimestamp(int(utc)).strftime("%H"))
	min = int(datetime.datetime.fromtimestamp(int(utc)).strftime("%M"))
	if hr == 9 and min == 16:
	    #print "%s: Making new entry for %s" % (sym, GetHumanDate(utc, 1))
	    data[str(utc)] = [d[1:]]
	    lutc = utc
	elif (hr == 9 and min > 16) or (hr > 9 and hr < 15) or (hr == 15 and min <= 30):
	    #print sym, ": Appending %s to %s" % (GetHumanDate(utc, 1), GetHumanDate(lutc, 1))
	    if lutc == 0:
		return {}
	    data[str(lutc)].append(d[1:])
	#else:
	    #log("Dropping candle %s" % GetHumanDate(utc, 1))
    data_new = {key: value for (key, value) in (data_cache.items() + data.items())}
    sym_file = "NEW/%s.%sCandles.json" % (sym, days)
    if os.path.exists(sym_file):
	os.rename(sym_file, "%s.moved" % sym_file)
    with open(sym_file, "w") as sym_file_handle:
	json.dump(data_new, sym_file_handle)
    sym_file_handle.close()
    #print sym, sorted(data.keys())
    return data

def GetPrevUTCNifty(pUTC):
    keys = NiftyIndex1YCandle.keys()
    i=1
    while i < 6:
	pUTC = str(int(pUTC) - (i*86400))
	if pUTC in keys:
	    return pUTC
	i+=1
    return None

def GetPrevUTC(data, pUTC):
    keys = data.keys()
    i=1
    while i < 6:
	pUTC = str(int(pUTC) - (i*86400))
	if pUTC in keys:
	    return pUTC
	i+=1
    return None

def GetNifty50Symbols():
    Nifty50 = []
    syms = []
    with open('ind_niftynext50list.csv', 'rb') as f:
	reader = csv.reader(f)
	Nifty50.extend(list(reader))
    f.close()
    for sym in Nifty50[1:]:
	syms.append(sym[2])
    return syms

def GetNifty100Symbols():
    Nifty100 = []
    syms = []
    with open('ind_nifty100list.csv', 'rb') as f:
	reader = csv.reader(f)
	Nifty100.extend(list(reader))
    f.close()
    for sym in Nifty100[1:]:
	syms.append(sym[2])
    return syms

def GetNifty200Symbols():
    Nifty200 = []
    syms = []
    with open('ind_nifty200list.csv', 'rb') as f:
	reader = csv.reader(f)
	Nifty200.extend(list(reader))
    f.close()
    for sym in Nifty200[1:]:
	syms.append(sym[2])
    return syms

def Initialize():
    global sl_count
    global tgt_count
    global sq_count
    global y
    global m
    global d
    global CAPITAL
    global GROSS

    sl_count = 0
    tgt_count = 0
    sq_count = 0

    if today == 1:
	y = int(dt.strftime("%Y"))
	m = int(dt.strftime("%m"))
	d = int(dt.strftime("%d"))
    else:
	y = 2018
	m = 4
	d = 15
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
    t_count=0
    t_tgt_count=0
    t_sl_count=0
    t_sq_count=0

    tdt = datetime.datetime.today();
    tm = int(tdt.strftime("%m"))
    td = int(tdt.strftime("%d"))


    while True:
	if m == tm and d > td:
	    break
	if d > NDays[m-1]:
	    d=1
	    m+=1
	    if m > 12:
		m=1
		y+=1
	    #log('Continuing 1')
	    continue
	dt = datetime.datetime(y, m, d, 9, 16, 0)
	utc = dt.strftime("%s")
	dtl = datetime.datetime(y, m, d, 15, 30, 0)
	utcl = dtl.strftime("%s")

	pnifty = GetPrevUTCNifty(utcl)
	if pnifty is None:
	    d+=1
	    #log("Could not find Nifty value for %s (3:30)" % GetHumanDate(utcl))
	    #log('Continuing 2')
	    continue
	pnifty = NiftyIndex1YCandle[pnifty][0]
	if today == 1:
	    cnifty = NiftyIndexTodayCandle[utc][0][0]
	elif utc in NiftyIndex60DCandle.keys():
	    cnifty = NiftyIndex60DCandle[utc][0][0]
	else:
	    d+=1
	    #log("Could not find Nifty value for %s (9:15)" % GetHumanDate(utc))
	    continue
	#Ncpt = ((float(NiftyIndex60DCandle[utc][0][0])-float(NiftyIndex1YCandle[prev_utc][0]))/float(NiftyIndex1YCandle[prev_utc][0]))*100
	Ncpt = ((float(cnifty)-float(pnifty))/float(pnifty))*100
	#log("[%s]: Ncpt = %.2f" % (GetHumanDate(utc), Ncpt))
	if Ncpt <= -2:
	    d+=1
	    #log("Skipping trade on %s" % (GetHumanDate(utc)))
	    #log('Continuing 4')
	    continue
	if s == 'Nifty':
	    strategy = "Both"
	    if Ncpt <= -1:
		strategy = "Sell"
	else:
	    strategy = s

	RsymsBuy = []
	RsymsSell = []

	# Shortlist complete list of stocks in one iteration
	for sym in Nsyms:
	    prev_utc = GetPrevUTC(OneYearData[sym], utcl)
	    if prev_utc is None:
		#log('Continuing 5')
		continue
	    if today:
		utcs = TodayData[sym].keys()
	    else:
		utcs = SixtyDaysData[sym].keys()

	    if utc in utcs:
		if prev_utc is not None:
		    #log("Iteration for %s, %s,%s" % (sym, GetHumanDate(prev_utc), GetHumanDate(utc)))
		    IntradayStrategy(strategy, sym, utc, prev_utc)
		#else:
		    #log("Data is not available for %s(%s)" % (sym, GetHumanDate(prev_utc)))
	    #else:
		#log("Data is not available for %s(%s)" % (sym, GetHumanDate(utc)))


	if BackTesting is True and (len(RsymsBuy) > 0 or len(RsymsSell) > 0):
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

	    if (strategy == "Buy" or strategy == "Both") and len(RsymsBuy) > 0:
		print 'Buy Stocks:', ','.join(RsymsBuy)
		BackTest('Buy', utc, prev_utc, CPS)

	    if (strategy == "Sell" or strategy == "Both") and len(RsymsSell) > 0:
		print 'Sell Stocks:', ','.join(RsymsSell)
		BackTest('Sell', utc, prev_utc, CPS)

	    if total_count > 0:
		for key in MasterData[utc].keys():
		    print "%s,%s,%.2f,%.2f,%.2f%%,%.2f,%.2f%%,%.2f,%.2f%%,%s,%s,%.2f%%,%.2f%%,%s,%s,%s" % (GetHumanDate(utc), key, MasterData[utc][key]['PPRICE'], MasterData[utc][key]['SL'], MasterData[utc][key]['SLPCT'], MasterData[utc][key]['TGT'], MasterData[utc][key]['TGTPCT'], MasterData[utc][key]['SQO'], MasterData[utc][key]['SQOPCT'], MasterData[utc][key]['CHLO1'], MasterData[utc][key]['CHLO2'], MasterData[utc][key]['SL_PCT'], MasterData[utc][key]['ProfitPct'], MasterData[utc][key]['VolCheck'], MasterData[utc][key]['CptCheck'], MasterData[utc][key]['PriceChoice'])
		cdate = GetHumanDate(utc)
		print("%s %d: Total Count=%d, SL Count=%d (%d%%), Tgt Count=%d (%d%%), SQO Count = %d (%d%%)" % (Months[m-1], d, total_count, sl_count, (sl_count/total_count*100), tgt_count, (tgt_count/total_count*100), sq_count, (sq_count/total_count*100)))
		t_count+=total_count
		t_tgt_count+=tgt_count
		t_sl_count+=sl_count
		t_sq_count+=sq_count
		tdays+=1
		#print("Nifty%d[%s]: Ncpt=%f, Capital=%d, Gross=%d, Pct=%.2f%% (ProfitPct=%s,SLPct=%s,VolumeCondition=%s,CptCheck=%d,TotalStocks=%d,Tgt-Hit=%d,SL-Hit=%d,SQ-Hit=%d,TradedDays=%d)" % (len(Nsyms), s, Ncpt, CAPITAL, GROSS, float((GROSS-CAPITAL)/CAPITAL)*100, ProfitPct, SLPct, VOL_check_list[VOL_Check], CPT_Check, t_count, t_tgt_count, t_sl_count, t_sq_count, tdays))

	if one_day_scan == 1:
	    break
	d+=1

    if BackTesting == True:
	#if float((GROSS-CAPITAL)/CAPITAL)*100 > 0 and t_count > 0:
	    #print("Nifty%d[%s]: Capital=%d, Gross=%d, Pct=%.2f%% (ProfitPct=%s,SLPct=%s,VolumeCondition=%s,CptCheck=%d,TotalStocks=%d,Tgt-Hit=%d,SL-Hit=%d,SQ-Hit=%d,TradedDays=%d)" % (len(Nsyms), s, CAPITAL, GROSS, float((GROSS-CAPITAL)/CAPITAL)*100, ProfitPct, SLPct, VOL_check_list[VOL_Check], CPT_Check, t_count, t_tgt_count, t_sl_count, t_sq_count, tdays))
	print("CSV,%s,%.2f,%s,%s,%s,%s,%s,%s,%s,%d,%d,%d,%d" % (s, float((GROSS-CAPITAL)/CAPITAL)*100, ProfitPct, SLPct, VOL_check_list[VOL_Check], CPT_check_list[CPT_Check], CCheck_list[C_Check], P_Choice_list[P_Choice], P_Check_list[P_Candle], t_tgt_count, t_sl_count, t_sq_count, tdays))

if __name__=="__main__":
    Nsyms = []
    # Get Nifty symbols
    if len(sys.argv) > 0:
	i=1
	while i <= len(sys.argv[1:]):
	    if sys.argv[i] == "--verbose":
		verbose=1
	    if sys.argv[i] == "--nifty50":
		Nsyms.extend(GetNifty50Symbols())
	    elif sys.argv[i] == "--nifty100":
		Nsyms.extend(GetNifty100Symbols())
	    elif sys.argv[i] == "--nifty200":
		Nsyms.extend(GetNifty200Symbols())
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
	    elif sys.argv[i] == '--yesterday':
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
	#Nsyms.extend(GetNifty100Symbols())
	Nsyms.extend(SCRIPS)

    for sym in Nsyms:
	# Collect Candle data for the each symbol for last 2 months and 1 year
	OneYearData[sym] = Get_1Y_Data(sym)
	SixtyDaysData[sym] = GetScripCandleData('60d', sym)
	if today == True:
	    TodayData[sym] = GetScripCandleData('1d', sym)

    # Collect Nifty Candle data for the same period and interval as symbols.
    NiftyIndex1YCandle = Get_1Y_Data('NIFTY')
    NiftyIndex60DCandle = GetScripCandleData('60d', 'NIFTY')
    if today:
	NiftyIndexTodayCandle = GetScripCandleData('1d', 'NIFTY')

    if len(pcts) == 0:
	pcts="%s:%s" % (ProfitPct,SLPct)

    for pcand in (1, 2):
	P_Candle = pcand
	for pchoice in (0, 1, 2):
	    P_Choice=pchoice
	    for pft_sl in pcts.split(','):
		pft_sl_list = pft_sl.split(':')
		ProfitPct = float(pft_sl_list[0])/100
		SLPct = float(pft_sl_list[1])/100
		MainLoop('Both')
		Initialize()
