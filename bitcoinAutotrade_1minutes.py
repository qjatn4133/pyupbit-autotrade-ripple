import time
import pyupbit
import datetime

access = "BIN0ppsDkCMZ5jwjfyuJTvXSPzAw1rHWQXkKW9GS"
secret = "7SkrsigOsYbs8M3dAlEBdNHv2CmN2fcKaw8HsbbM"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_target_price_minute1(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_start_time_minute1(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


##!!! 현재 매매 코인명 : 비트코인ABC(BCHA)

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time_minute1("KRW-BCHA") #9:00
        end_time = start_time + datetime.timedelta(minutes=5) #9:00 + 1분

        # 9:00 < 현재 < # 9:00:55
        if start_time < now < end_time - datetime.timedelta(seconds=5):
            target_price = get_target_price_minute1("KRW-BCHA", 0.5)
            current_price = get_current_price("KRW-BCHA")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BCHA", krw*0.9995)
        else:
            BCHA = get_balance("BCHA")
            if BCHA > 0.00008:
                upbit.sell_market_order("KRW-BCHA", BCHA*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)