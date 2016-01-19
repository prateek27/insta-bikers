from flask import Flask,request
from pymongo import MongoClient
import json
from bson import ObjectId
import LatLon
from LatLon import *

"""
vehicles collection
{
    make:'',
    model:'',
    fare:'',
}

each vehicle has its own collection
e.g db.bajaj etc
{
    make:'',
    model:'',
    fare:'',
    state:'',
    coords:[,]
}



app = Flask(__name__)
#client = MongoClient("mongodb://instabiker1:%40udacity@ds039135.mongolab.com:39135/instabike_credentials")
client = MongoClient()
db = client.instabike_credentials
cust = db.customers
veh = db.vehicles
root_url = 'localhost:5000'

"""
app = Flask(__name__)
##encoding into json
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def getVehicle(dis,latlon):
    """ returns vehicle ids within dis km of range """
    vehs = []
    selected = []
    if dis > 1:
        print dis
        ##get data from database
        cursor = veh.find()
        for value in cursor:
            make = value['make']
            if make not in selected:
                tempColl = db[make]
                cursor2 = tempColl.find()
                for vehicle in cursor2:
                    if vehicle['state'] == 'free':
                        #not occupied
                        print "*************************************"
                        latlon2 = LatLon(Latitude(vehicle['coords'][0]),Longitude(vehicle['coords'][1]))
                        print latlon, latlon2
                        if latlon.distance(latlon2) <= dis:
                            vehs.append(vehicle)

            selected.append(make)

    print vehs
    vehs = JSONEncoder().encode(vehs)
    return vehs


@app.route('/getVehicles/<dis>', methods=['POST'])
def getVehicles(dis):
    if request.method == 'POST':
        print "Entered"
        lati = request.form['lat']
        longi = request.form['long']
        coords = LatLon(Latitude(lati),Longitude(longi))
        print dis,coords
        return getVehicle(dis,coords)




"""
Bajaj
    CT 100
    Platina
    Pulsar RS 200
    Discover 125M
    Avenger 150 Street
Hero
    HF Dawn
    MotoCorp Karizma
    MotoCorp Splendor Plus(ISmart,Pro,Pro Classic,Super Splendor,Passion Pro TR, Xtreme Sports, HF Deluxe Echo, Maestro Edge,Duet)
Honda
    CD 110 Dream
    Livo
    CB Shine
    Dream Yuga
Yamaha
    Crux
    YZF-R15
    FZ-16
    Alpha
    Saluto
Mahindra
    Pantero
    Centuro
Royal Enfield(expensive as fuck)
Piaggio( '' )
Suzuki
    Gixxer SF
    Hayate
    Slingshot Plus
Truimph(fuck)
TVS
    Sport
    XL Super HD(why does it even exist)
    Star City
    Phoenix
    MAX4R
Ducati(gand mara)
DSK(exp)
Harley-Davidson(exp)
"""