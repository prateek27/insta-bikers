from flask import Flask,request
from pymongo import MongoClient
from webLogin import *
from vehiclePing import *


app = Flask(__name__)
#client = MongoClient("mongodb://instabiker1:%40udacity@ds039135.mongolab.com:39135/instabike_credentials")
client = MongoClient()
db = client.instabike_credentials
cust = db.customers
veh = db.vehicles
root_url = 'localhost:5000'

if __name__ == '__main__':
    app.run(debug=True)