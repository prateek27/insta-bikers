#TODO: implement security of user credentials and email verification
#TODO: verification of email id and phone no.
#TODO: verification of city,state and zipcode

from flask import Flask,request
from pymongo import MongoClient
from collections import OrderedDict
app = Flask(__name__)

"""
app = Flask(__name__)
client = MongoClient("mongodb://instabiker1:%40udacity@ds039135.mongolab.com:39135/instabike_credentials")
#client = MongoClient()
db = client.instabike_credentials
cust = db.customers
veh = db.vehicle
root_url = 'localhost:5000'
"""


def verify(u_name,passw):
    #TODO: hash the password here
    print "hello"
    try:
        cursorObject = cust.find({"username": u_name,"password": passw})[0]
        print "Successful login"
        return True
    except IndexError:
        print "Wrong Credentials"
        return False

def registerTheUser(params):
    #TODO: hash the password here
    passw = params['passw']

    cust.insert_one(
        {
            "first": params['f_name'],
            "last": params['l_name'],
            "gender": params['gender'],
            "username": params['u_name'],
            "email": params['e_mail'],
            "password": passw,
            "phone": params['phone'],
            "address": { "houseno": params['address']['houseno'],
            "street": params['address']['street'],
            "city": params['address']['city'],
            "state": params['address']['state'],
            "zipcode": long(params['address']['zipcode']),
            #"country": params['address']['country']
            },
            "coords":[ float(params['lati']), float(params['longi'])]
        }
        )
    print "user registered"
    return "user registered"

def checkUniqueness(u_name,e_mail,phone):
    try:
       username_c = cust.find({"username": u_name})[0]
       email_c = cust.find({"email": e_mail})[0]
       phone_c = cust.find({"phone": phone})[0]
       print 'user already exists'
       return False
    except Exception,e:
       if username_c or email_c or phone_c:
           return False
       print "unique Credentials"
       return True

@app.route('/')
def help_message():
    return """ you can only see this message because the debug mode is on.
                    Please go to /login or /register."""

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        print "Entered"
        userdata = OrderedDict((
        ('f_name' , request.form['firstname']),
        ('l_name' , request.form['lastname']),
        ('gender' , request.form['gender']),
        ('u_name' , request.form['username']),
        ('e_mail' , request.form['email']),
        ('passw' , request.form['password']),
        ('phone' , request.form['phone']),
        ('address' , OrderedDict((('houseno' , request.form['house']),('street' , request.form['street']),('city' , request.form['city']),('state' , request.form['state']),('zipcode' , request.form['zipcode']),'''('country' , request.form['country'])'''))),
        ('lati' , request.form['lat']),
        ('longi' , request.form['long']),
        ))
        #no field should be empty
        #furthur validation checks will be at the app end
        if len(u_name) == 0 or len(f_name) == 0 or len(l_name) == 0 or len(e_mail) == 0 or len(passw) == 0:
            print "incomplete variables"
            return "Please provide complete variables"
        #unique username, email and phone
        if checkUniqueness(u_name,e_mail,phone):
            return registerTheUser(params=userdata)
        else:
            return "user already exists"
    else:
        return "Use POST request to access this url"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print 'Entered'
        u_name = request.form['username']
        passw = request.form['password']
        #no field should be empty
        #furthur validation checks will be at the app end
        if len(u_name) == 0 or len(passw) == 0:
            return "Please provide complete variables"
        if verify(u_name,passw):
            print 'success'
            return 'success'
        else:
            print 'failed'
            return 'failed'
    else:
        return "Use POST request to access this url"

@app.route('/forgotPassword',methods=['GET','POST'])
def forgot(username=None,email=None):
    if not username and not email:
        print "field should not be empty"
        return True
    if username and e_mail:
        print "only one field allowed"
        return False
    else:
        u_name = cust.find({'username': username})
        e_mail = cust.find({'email': email})
        if u_name.alive:
            u_name = u_name[0]
            userid = str(u_name['_id'])
            #send userid to user's inbox
            return True
        elif e_mail.alive:
            e_mail = e_mail[0]
            userid = str(e_mail['_id'])
            #send userid to user's inbox
            return True
        else:
            print "user does not exist"
            return False
        #send change password link to email

@app.route('/changePassword/<userid>',methods=['GET','POST'])
def changeP(userid):
    print 'hello'
    passw = str(request.form['password'])
    coll.update({'_id':userid},{'$set':{'password':passw}})
