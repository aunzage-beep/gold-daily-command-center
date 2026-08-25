import numpy as np,pandas as pd
def ema(s,n):return s.ewm(span=n,adjust=False).mean()
def rsi(s,n=14):
 d=s.diff();u=d.clip(lower=0).ewm(alpha=1/n,adjust=False).mean();dn=(-d.clip(upper=0)).ewm(alpha=1/n,adjust=False).mean()
 return 100-100/(1+u/dn.replace(0,np.nan))
def atr(x,n=14):
 p=x.close.shift(1);tr=pd.concat([x.high-x.low,(x.high-p).abs(),(x.low-p).abs()],axis=1).max(axis=1)
 return tr.ewm(alpha=1/n,adjust=False).mean()
def tf(x):
 x=x.copy()
 for n in [20,50,200]:x[f"ema{n}"]=ema(x.close,n)
 x["rsi"]=rsi(x.close);x["atr"]=atr(x);x["ret20"]=x.close.pct_change(20);x["vol"]=x.close.pct_change().rolling(20).std()
 x["strength"]=((x.ema50-x.ema200).abs()/x.close*5000).clip(0,100)
 x["trend"]=np.where((x.ema20>x.ema50)&(x.ema50>x.ema200),"BULLISH",np.where((x.ema20<x.ema50)&(x.ema50<x.ema200),"BEARISH","MIXED"))
 return x.dropna()
def latest(x):
 x=tf(x);r=x.iloc[-1];mom=np.clip(50+220*r.ret20,0,100);ts=80 if r.trend=="BULLISH" else 20 if r.trend=="BEARISH" else 50
 return {"trend":r.trend,"score":float(np.clip(ts*.65+mom*.2+r.rsi*.15,0,100)),"rsi":float(r.rsi)}
def build(d,h,m15,macro):
 md=macro.copy();md["score"]=(50-md.real10*12).clip(0,100)*.4+(50-md.us10*8).clip(0,100)*.25+(50-md.usd.pct_change(20)*250).clip(0,100)*.25+(50+md.breakeven.pct_change(20)*150).clip(0,100)*.1
 day=latest(d);four=latest(h);one=latest(h);fif=latest(m15);r=tf(d).iloc[-1];ms=md.reindex(tf(d).index).ffill().iloc[-1]
 score=day["score"]*.30+four["score"]*.20+one["score"]*.15+fif["score"]*.10+ms.score*.20+r.rsi*.05
 sig="BUY" if score>=60 else "SELL" if score<=40 else "HOLD";atrv=float(r.atr);price=float(r.close);support=float(d.tail(60).low.min());resistance=float(d.tail(60).high.max())
 if sig=="BUY": el=max(support,price-atrv*.75);eh=price;sl=el-atrv*.5;tp1=price+2*atrv;tp2=price+3*atrv
 elif sig=="SELL": el=price;eh=min(resistance,price+atrv*.75);sl=eh+atrv*.5;tp1=price-2*atrv;tp2=price-3*atrv
 else: el=price-.5*atrv;eh=price+.5*atrv;sl=price-1.5*atrv;tp1=price+2*atrv;tp2=price-2*atrv
 return {"price":price,"signal":sig,"score":float(score),"confidence":float(min(95,50+abs(score-50))),
 "regime":"TRENDING" if r.strength>=55 else "RANGING" if r.strength<=20 else "TRANSITION",
 "daily":day,"4h":four,"1h":one,"15m":fif,"macro_score":float(ms.score),"us10":float(ms.us10),"real10":float(ms.real10),"usd":float(ms.usd),"breakeven":float(ms.breakeven),
 "support":support,"resistance":resistance,"entry_low":el,"entry_high":eh,"sl":sl,"tp1":tp1,"tp2":tp2,"updated":pd.Timestamp.utcnow().isoformat()}
