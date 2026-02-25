# import flask
from flask import *
import pymysql
import os

# create an insatance/create/initialize flask app
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='static/images'

@app.route("/api/signup",methods=["POST"])
def signup():
    username=request.form["username"]
    email=request.form["email"]
    password=request.form["password"]
    phone=request.form["phone"]

    # print(username,email,password,phone)
    # connecting DB
    connection=pymysql.Connect(host="localhost",user="root",password="",database="taisokogarden")
    # creating a cursor 
    cursor=connection.cursor()
    # sql querry
    sql="insert into users (username,email,password,phone) values(%s,%s,%s,%s)"
    
    data=(username,email,password,phone)
    # we start with a query which is a string then data which is a tuple
    cursor.execute(sql,data)
    connection.commit()

    return jsonify({"message":"Thank you for joining"})





@app.route("/api/signin",methods=["POST"])
def signin():
    email=request.form["email"]
    password=request.form["password"]

    connection=pymysql.connect(host="localhost",user="root",password="",database="taisokogarden")
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    sql="select * from users where email=%s and password=%s"
    data=(email,password)

    cursor.execute(sql,data)
    count=cursor.rowcount
    if count==0:
        return jsonify({"message":"Invalid credentials"})
    else:
        user=cursor.fetchone()
        return jsonify({"message":"Login successful","user":user})


# add product function
@app.route("/api/add_product",methods=["Post"])
def add_product():
    product_name=request.form["product_name"]
    product_description=request.form["product_description"]
    product_cost=request.form["product_cost"]
    # extract image data
    product_photo=request.files["product_photo"]

    # extract filename
    filename=product_photo.filename

    print(product_name,product_description,product_cost,filename)

    # specifies where the image will be saved (in static folder-image path)
    photo_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    product_photo.save(photo_path)

    # db connection
    connection=pymysql.connect(host="localhost",user="root",password="",database="taisokogarden")
    cursor=connection.cursor()

    # sql statement
    sql="insert into product_details (product_name,product_description,product_cost,product_photo) values(%s,%s,%s,%s)"
    data=(product_name,product_description,product_cost,filename)
    cursor.execute(sql,data)
    connection.commit()

    return jsonify({"message":"Product details added successfully"})



# Get products
@app.route("/api/get_product_details")
def get_product_details():
    connection=pymysql.connect(host="localhost",user="root",password="",database="taisokogarden")
    cursor=connection.cursor(pymysql.cursors.DictCursor)

    sql="select * from product_details"
    cursor.execute(sql)
    product_details=cursor.fetchall()
    return jsonify(product_details)


    


# Mpesa Payment Route 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
 
@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"
 
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
 
        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
 
        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
 
        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }
 
        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
 
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL
 
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})




if __name__=='__main__':
    app.run(debug=True)