from flask import Flask,request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://instabiker1:%40udacity@ds039135.mongolab.com:39135/instabike_credentials")
#client = MongoClient()
db = client.instabike_credentials
cust = db.customers

def verify(u_name,passw):
    print "hello"
    try:
        cursorObject = cust.find({"username": u_name,"password": passw})[0]
        print "Successful login"
        return True
    except IndexError:
        print "Wrong Credentials"
        return False

def registerTheUser(params):
    cust.insert_one(
        {
            "first": params[0],
            "last": params[1],
            "username": params[2],
            "email": params[3],
            "password": params[4],
        }
        )
    print "user registered"
    return "user registered"

def checkUniqueness(u_name,e_mail):
    try:
       username_c = cust.find({"username": u_name})[0]
       email_c = cust.find({"email": e_mail})[0]
       print 'user already exists'
       return False
    except Exception,e:
       print "unique credentials"
       return True



@app.route('/')
def help_message():
    return """ you can only see this message because the debug mode is on.
                    Please go to /login or /register."""

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        print "Entered"
        u_name = request.form['username']
        e_mail = request.form['email']
        passw = request.form['password']
        f_name = request.form['firstname']
        l_name = request.form['lastname']
        #f_name, l_name, u_name, e_mail, password
        #u_name and e_mail should be unique
        if len(u_name) == 0 or len(f_name) == 0 or len(l_name) == 0 or len(e_mail) == 0 or len(passw) == 0:
            print "incomplete variables"
            return "Please provide complete variables"
        if checkUniqueness(u_name,e_mail):
            return registerTheUser(params=[f_name,l_name,u_name,e_mail,passw])
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



if __name__ == "__main__":
    app.run(debug=True)