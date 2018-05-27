import os, json, datetime

Nsyms=['YESBANK', 'TATASTEEL', 'STAR', 'SBIN', 'RELIANCE', 'POWERGRID', 'PETRONET', 'ONGC', 'OIL', 'MARUTI', 'M&M', 'LT', 'KTKBANK', 'KOTAKBANK', 'JSWSTEEL', 'ITC', 'IOC', 'INDUSINDBK', 'IGL', 'ICICIBANK', 'HINDUNILVR', 'HEROMOTOCO', 'HDFCBANK', 'HDFC', 'GAIL', 'FEDERALBNK', 'DCBBANK', 'DABUR', 'COLPAL', 'COALINDIA', 'CIPLA', 'CEATLTD', 'CASTROLIND', 'CANBK', 'BPCL', 'BHARTIARTL', 'BHARATFORG', 'BATAINDIA', 'BANKBARODA', 'BAJAJ-AUTO', 'AXISBANK', 'ASIANPAINT', 'ASHOKLEY', 'ARVIND', 'APOLLOTYRE', 'APOLLOHOSP', 'AMBUJACEM', 'AMARAJABAT', 'ACC', 'UNIONBANK', 'KSCL', 'ICIL', 'ZEEL', 'VEDL', 'UPL', 'ULTRACEMCO', 'UBL', 'TVSMOTOR', 'TITAN', 'TATAMTRDVR', 'TATAMOTORS', 'TATACHEM', 'SRTRANSFIN', 'SRF', 'RECLTD', 'PTC', 'PIDILITIND', 'NTPC', 'NMDC', 'NCC', 'MOTHERSUMI', 'MCLEODRUSS', 'MCDOWELL-N', 'MARICO', 'M&MFIN', 'LUPIN', 'LICHSGFIN', 'L&TFH', 'JUBLFOOD', 'JISLJALEQS', 'INDIACEM', 'HINDZINC', 'HINDPETRO', 'HINDALCO', 'HEXAWARE', 'GRASIM', 'GLENMARK', 'EXIDEIND', 'ENGINERSIN', 'BRITANNIA', 'BHEL', 'GRANULES', 'GOLDBEES', 'BANKBEES', 'WIPRO', 'VOLTAS', 'TECHM', 'TCS', 'TATAPOWER', 'TATAGLOBAL', 'TATAELXSI', 'TATACOMM', 'SIEMENS', 'RELINFRA', 'RELCAPITAL', 'PFC', 'NIITTECH', 'MINDTREE', 'IRB', 'INFY', 'INFRATEL', 'IBULHSGFIN', 'HCLTECH', 'HAVELLS', 'DISHTV', 'CONCOR', 'CESC', 'CADILAHC', 'BIOCON', 'BEML', 'BEL', 'TORNTPOWER', 'OFSS', 'KPIT', 'JINDALSTEL', 'CGPOWER', 'CENTURYTEX', 'BHARATFIN', 'AJANTPHARM', 'WOCKPHARMA', 'TORNTPHARM', 'SUNPHARMA', 'ORIENTBANK', 'IDEA', 'GODREJIND', 'DRREDDY', 'DLF', 'DIVISLAB', 'DHFL', 'BANKINDIA', 'BAJFINANCE', 'AUROPHARMA', 'TV18BRDCST', 'SYNDIBANK', 'SOUTHBANK', 'SAIL', 'RPOWER', 'RAYMOND', 'PNB', 'NHPC', 'JSWENERGY', 'IFCI', 'IDFCBANK', 'IDFC', 'IDBI', 'GMRINFRA', 'ANDHRABANK', 'ALBK', 'ADANIPOWER']

# Return Human readable data for a givne UTC (in seconds)
def GetHumanDate(utc):
    return datetime.datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d %H:%M:%S')
    #return datetime.datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d')

def Read():
    #Nsyms = ['NIFTY']
    for sym in Nsyms:
        #for interval in ('60dCandles', '1Y'):
        for interval in (['1Y']):
            DATA = {}
            sym_file = "DATA/%s.%s.json" % (sym, interval)
            if os.path.exists(sym_file):
                with open(sym_file, "r") as sym_file_handle:
                    DATA = json.load(sym_file_handle)
                sym_file_handle.close()
                #print sym, GetHumanDate(list(sorted(DATA.keys()))[0]), GetHumanDate(list(sorted(DATA.keys()))[-1])
            print "%s [%s to %s]" % (sym, GetHumanDate(sorted(DATA.keys())[0]), GetHumanDate(sorted(DATA.keys())[-1]))

Read()
