from flask import Flask,render_template,jsonify
from .data import load
from .engine import build
app=Flask(__name__);CACHE={}
@app.get("/")
def home():return render_template("index.html")
@app.get("/health")
def health():return {"status":"ok"}
@app.get("/api/dashboard")
def dashboard():
 try:
  if "d" not in CACHE:CACHE["d"]=build(*load())
  return jsonify(CACHE["d"])
 except Exception as e:return jsonify({"error":str(e)}),500
@app.post("/api/refresh")
def refresh():
 try:CACHE["d"]=build(*load());return jsonify(CACHE["d"])
 except Exception as e:return jsonify({"error":str(e)}),500
if __name__=="__main__":app.run(host="0.0.0.0",port=8501)
