# Gold Daily Command Center V2
Deployable XAU/USD web dashboard. Uses Yahoo Finance XAUUSD=X for market data and FRED DGS10, DFII10, DTWEXBGS, T10YIE for macro inputs. Includes Daily/4H/1H/15M alignment, Gold score, macro score, regime, support/resistance, entry/SL/TP and Refresh API.

Local: `pip install -r requirements.txt` then `python -m flask --app app.main run --host 0.0.0.0 --port 8501`.
Deploy with the included Dockerfile/render.yaml. Research only; not financial advice.
