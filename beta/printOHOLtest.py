#!/usr/bin/env python2.7

from __future__ import division

import os, sys
import datetime, urllib2, csv, multiprocessing
import time

OHOL_PATH="%s" % os.getcwd()
sys.path.append(OHOL_PATH)

from test_ohol import FindOHOLStocks, MIS

# Important parameters
CAPITAL=50000
cap=CAPITAL*(80/100)
SLPct=(1.25/100)
ProfitPct=(1.25/100)

def GetTicks(price):
    tgt=round(0.05 * round(float(price * ProfitPct)/0.05), 2)
    sl=round(0.05 * round(float(price * SLPct)/0.05), 2)
    tsl=round(0.05 * round(float(price * 0.005)/0.05), 2)
    return (tgt, sl, tsl)

(BuySyms, SellSyms) = FindOHOLStocks()

if (len(BuySyms.keys())+len(SellSyms.keys())) > 0:
    cps = int(cap/(len(BuySyms.keys())+len(SellSyms.keys())))
    for bsym,value in BuySyms.items():
        n = int((cps*int(MIS[bsym]))/value)
        (tgt, sl, tsl) = GetTicks(value)
        print('Buy %d %s @ %.2f SL=%.2f Tgt=%.2f TSL=%.2f' % (n, bsym, value, tgt, sl, tsl))

    manager = multiprocessing.Manager()
    for ssym,value in SellSyms.items():
        n = int((cps*int(MIS[ssym]))/value)
        (tgt, sl, tsl) = GetTicks(value)
        print('Sell %d %s @ %.2f SL=%.2f Tgt=%.2f TSL=%.2f' % (n, ssym, value, tgt, sl, tsl))
else:
    print('No stocks shortlisted')
