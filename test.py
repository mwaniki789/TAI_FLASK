from flask import *

app=Flask(__name__)
@app.route("/api/home")
def home():
    return jsonify({"message":"Welcome to Home API"})
@app.route("/api/products")
def products():
    return jsonify({"message":"welcome to products API"})
@app.route("/api/calc",methods=["POST"])
def calc():
    num1=request.form("num1")
    num2=request.form("num2")
    sum=int(num1)+int(num2)
    return jsonify({"answer":sum})
if __name__=='__main__':
    app.run(debug=True)