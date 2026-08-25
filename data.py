import pandas as pd, numpy as np, requests, yfinance as yf
def yfdata(period, interval):
    x=yf.download("XAUUSD=X",period=period,interval=interval,auto_adjust=False,progress=False,threads=False)
    if isinstance(x.columns,pd.MultiIndex): x.columns=x.columns.get_level_values(0)
    x=x.rename(columns=str.lower); x.index=pd.to_datetime(x.index)
    if getattr(x.index,"tz",None) is not None: x.index=x.index.tz_convert(None)
    return x.dropna(subset=["close"])
def fred(s):
    r=requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}",timeout=30);r.raise_for_status()
    x=pd.read_csv(pd.io.common.BytesIO(r.content));x["DATE"]=pd.to_datetime(x.DATE);x[s]=pd.to_numeric(x[s],errors="coerce")
    return x.set_index("DATE")[s].dropna()
def load():
    return yfdata("10y","1d"),yfdata("2y","1h"),yfdata("60d","15m"),pd.concat({
      "us10":fred("DGS10"),"real10":fred("DFII10"),"usd":fred("DTWEXBGS"),"breakeven":fred("T10YIE")},axis=1).ffill()
