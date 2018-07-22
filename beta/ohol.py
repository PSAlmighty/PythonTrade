#!/usr/bin/env python2.7

from __future__ import division

import os, sys, datetime, time
import urllib2, json, csv, multiprocessing
import socket, re

MY_MOD_PATH="%s" % os.getcwd()
sys.path.append(MY_MOD_PATH)

from params import Nsyms, MIS, BuyVolInc, SellVolInc, PriceInc, Vol_buffer, Vol5_buffer

socket.setdefaulttimeout(10)
os.environ['TZ'] = 'Asia/Calcutta'

manager = multiprocessing.Manager()
PastData = manager.dict()

# Important Parameters
TODAY = datetime.datetime.today().strftime("%Y-%m-%d")
Interval = 60

# Candle index
idx_close = 0
idx_high = 1
idx_low = 2
idx_open = 3
idx_vol = 4

# Variables
ndays = 1
utc = 0
utcl = 0
DailyData = {}
TodayCandleData = {}

def log_it(log_str):
    print("%s: %s" % (datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), log_str))

# Get data from finance.google.com
def GetURLData(p, sym, candle):
    if candle == False:
	url = 'https://finance.google.com/finance/getprices?x=NSE&q=%s&f=d,c,h,l,o,v&p=%sd' % (sym.replace('&','%26'), p)
    else:
	url = 'https://finance.google.com/finance/getprices?x=NSE&q=%s&f=d,c,h,l,o,v&p=%sd&i=%s' % (sym.replace('&','%26'), p, Interval)
    #log_it("Getting %s day(s) data for %s from %s" % (p, sym, url))
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = csv.reader(response.read().splitlines()[7:])
    return content

# Get 1 year data for a given symbol
def GetDailyData(sym):
    sym_cache_file = "DATA/%s.json" % sym
    if os.path.exists(sym_cache_file):
	with open(sym_cache_file, 'r') as sym_file_handle:
	    data_cache = json.load(sym_file_handle)
	    sym_file_handle.close()
	    if len(data_cache) > 0:
		#log_it("Getting data for %s from %s" % (sym, sym_cache_file))
		return data_cache
    data = {}
    content = GetURLData(ndays+8, sym, False)
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
    if days > 1:
	sym_cache_file = "DATA/%s.%sCandles.json" % (sym, days)
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
    if days > 1:
	if not os.path.exists(TODAY):
	    os.mkdir(TODAY)
	sym_file = "%s/%s.%sCandles.json" % (TODAY, sym, days)
	if os.path.exists(sym_file):
	    os.rename(sym_file, "%s.moved" % sym_file)
	with open(sym_file, 'w') as sym_file_handle:
	    json.dump(data, sym_file_handle)
    return data

# Return valid previous time/day for a given time/day
def GetPrevUTC(data, UTC):
    keys = data.keys()
    i=1
    while i < 6:
	pUTC = str(int(UTC) - (i*86400))
	if pUTC in keys:
	    return pUTC
	i+=1
    return None

# Return Human readable data for a givne UTC (in seconds)
def GetHumanDate(utc):
    return datetime.datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d %H:%M:%S')
    #return datetime.datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d')

def GetNSEPrice(sym):
    url = 'http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=%s&illiquid=0' % sym
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(req)
    nse_quote = response.read()
    m = re.search('.*,"lastPrice":"([^"]*)".*', nse_quote)
    return float(m.group(1).replace(",",""))

# Get previous day close price, and previous day traded vol for a given symbol
def GetPastData(sym, PastData):
    DailyData[sym] = GetDailyData(sym)
    prev_utcl = GetPrevUTC(DailyData[sym], utcl)
    if prev_utcl is None:
	return
    pclose = float(DailyData[sym][prev_utcl][0])
    pvol = int(DailyData[sym][prev_utcl][4])
    if pclose > 0 and pvol > 0:
	ValHash = {}
	ValHash['CLOSE'] = float(pclose)
	ValHash['VOL'] = int(pvol)
	PastData[sym] = ValHash

# This is the core function
# Shortlist each symbol based on the startegy
def OHOLStrategy(sym, PastData, BuySyms, SellSyms, SkipSyms):
    # Collect today's Candle data for each symbol
    TodayCandleData[sym] = GetScripCandleData(ndays, sym)
    if utc not in TodayCandleData[sym].keys():
	while True:
	    tdt = datetime.datetime.today()
	    min = int(tdt.strftime("%M"))
	    if min > 16:
		break
	    time.sleep(10)
        TodayCandleData[sym] = GetScripCandleData(ndays, sym)
	if utc not in TodayCandleData[sym].keys():
	    log_it("Not able to get candle data for %s" % sym)
	    return

    cdata = TodayCandleData[sym][utc]

    h1 = float(cdata[0][idx_high])
    l1 = float(cdata[0][idx_low])
    o1 = float(cdata[0][idx_open])
    c1 = float(cdata[0][idx_close])

    v1 = c_candle_vol=int(cdata[0][idx_vol])
    if sym not in PastData.keys():
	return

    if o1 == l1 and o1 == h1:
	SkipSyms.append(sym)

    if o1 == l1 or o1 == h1:
	pclose = PastData[sym]['CLOSE']
	pcpt = abs((o1-pclose)/pclose)*100

	call=''
	if o1 == l1 and pclose <= o1:
	    call='Buy'

	if o1 == h1 and pclose >= o1:
	    call='Sell'

	if call != 'Buy' and call != 'Sell':
	    return

	if pcpt < PriceInc:
	    log_it("Rejecting a '%s' call on %s as pcpt < PriceInc (%.2f%%, %.2f%%)" % (call, sym, pcpt, PriceInc))
	    return

	pvol = PastData[sym]['VOL']
	vcpt = (c_candle_vol/pvol)*100

	values = [o1, vcpt]
	if call == 'Buy':
	    if vcpt < BuyVolInc:
		log_it("Rejecting a 'Buy' call on %s as vcpt < BuyVolInc (%.2f%%, %.2f%%)" % (sym, vcpt, BuyVolInc))
		return

	    c2 = float(cdata[1][idx_close])
	    if c2+(c2*(0.1/100)) < c1:
		log_it("Rejecting a 'Buy' call on %s as c2+(c2*(0.2/100)) < c1 (%.2f, %.2f)" % (sym, c2+((0.2/100)*c2), c1))
		return

	    v2cpt = (int(cdata[1][idx_vol])/pvol)*100
	    if v2cpt < 0.8:
		log_it("Rejecting a 'Buy' call on %s as v2cpt < 0.8 (%.2f%% < 0.8%%)" % (sym, v2cpt))
		return

	    log_it("Considering a Buy on %s (o=%.2f, l=%.2f, c=%.2f, v=%d, pclose=%.2f, vcpt=%.2f%%, pcpt=%.2f%%)" % (sym, o1, l1,c1, v1, pclose, vcpt, pcpt))
	    BuySyms[sym] = values
	elif call == 'Sell':
	    if vcpt < SellVolInc:
		log_it("Rejecting a 'Sell' call on %s as vcpt < SellVolInc (%.2f%%, %.2f%%)" % (sym, vcpt, SellVolInc))
		return

	    v2cpt = (int(cdata[1][idx_vol])/pvol)*100
	    if v2cpt < 0.5:
		log_it("Rejecting a 'Sell' call on %s as v2cpt < 0.5 (%.2f%% < 0.5%%)" % (sym, v2cpt))
		return

	    c2 = float(cdata[1][idx_close])
	    if c2-(c2*(0.1/100)) > c1:
		log_it("Rejecting a 'Sell' call on %s as c2-(c2*(0.1/100)) < c1 (%.2f, %.2f)" % (sym, c2-((0.1/100)*c2), c1))
		return
	    log_it("Considering a Sell on %s (o=%.2f, h=%.2f, c=%.2f, v=%d, pclose=%.2f, vcpt=%.2f%%, pcpt=%.2f%%)" % (sym, o1, h1, c1, pclose, v1, vcpt, pcpt))
	    SellSyms[sym] = values

def LoadPastData():
    global utc
    global utcl

    if len(sys.argv) > 1 and '--yesterday' in sys.argv:
	ndays=6
	dt = datetime.datetime.today() - datetime.timedelta(3);
    else:
	dt = datetime.datetime.today();
    y = int(dt.strftime("%Y"))
    m = int(dt.strftime("%m"))
    d = int(dt.strftime("%d"))

    dt = datetime.datetime(y, m, d, 0, 0, 0)
    utc = dt.strftime("%s")
    dtl = datetime.datetime(y, m, d, 15, 30, 0)
    utcl = dtl.strftime("%s")

    jobs = []
    for sym in Nsyms:
	p = multiprocessing.Process(target=GetPastData, args=(sym, PastData))
	jobs.append(p)
	p.start()

    for proc in jobs:
	proc.join()


def FindOHOLStocks():
    global utc
    global utcl
    global ndays

    if len(sys.argv) > 1 and '--yesterday' in sys.argv[1]:
	ndays=6
	dt = datetime.datetime.today() - datetime.timedelta(2);
    else:
	dt = datetime.datetime.today();
    y = int(dt.strftime("%Y"))
    m = int(dt.strftime("%m"))
    d = int(dt.strftime("%d"))

    dt = datetime.datetime(y, m, d, 0, 0, 0)
    utc = dt.strftime("%s")
    dtl = datetime.datetime(y, m, d, 15, 30, 0)
    utcl = dtl.strftime("%s")

    # Collect Nifty Candle data for 1 year and today
    NiftyIndexDailyData = GetDailyData('NIFTY')
    NiftyIndexCandle = GetScripCandleData(ndays, 'NIFTY')

    pnifty = GetPrevUTC(NiftyIndexDailyData, utcl)
    if pnifty is None:
	print "Could not find previous Nifty for %s" % GetHumanDate(utcl)
	return ({},{})
    pnifty = NiftyIndexDailyData[pnifty][0]
    if utc in NiftyIndexCandle.keys():
	cnifty = NiftyIndexCandle[utc][0][0]
    else:
	print "Could not find Nifty for %s" % GetHumanDate(utc)
	return ({},{})
    Ncpt = ((float(cnifty)-float(pnifty))/float(pnifty))*100
    if Ncpt <= -2:
	print "CAUTION: Better dont trade today as Nifty is down by %.2f%% :)" % Ncpt
	return ({},{})

    jobs = []
    GetOfflineData = False
    if GetOfflineData == False:
	for sym in Nsyms:
	    p = multiprocessing.Process(target=GetPastData, args=(sym, PastData))
	    jobs.append(p)
	    p.start()

	for proc in jobs:
	    proc.join()

    jobs = []
    BuySyms = manager.dict()
    SellSyms = manager.dict()
    SkipSyms = manager.list()

    count=1
    for sym in Nsyms:
	p = multiprocessing.Process(target=OHOLStrategy, args=(sym, PastData, BuySyms, SellSyms, SkipSyms))
	jobs.append(p)
	p.start()
	if count == 50:
	    time.sleep(2)
	    count=1

    for proc in jobs:
	proc.join()

    return (BuySyms, SellSyms, SkipSyms)
