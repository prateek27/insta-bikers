from flask import Flask,request
from pymongo import MongoClient
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
    coords:''
}
"""


app = Flask(__name__)
client = MongoClient("mongodb://instabiker1:%40udacity@ds039135.mongolab.com:39135/instabike_credentials")
#client = MongoClient()
db = client.instabike_credentials
cust = db.customers
veh = db.vehicles
root_url = 'localhost:5000'

def getVehicle(dis,latlon):
    """ returns vehicle ids within dis km of range """
    if dis > 1:
        ##get data from database
        vehs = []
        cursor = veh.find({})
        for value in cursor:
            make = value['make']
            tempColl = db[make]
            cursor2 = tempColl.find({})
            for vehicle in cursor2:
                if vehicle['state'] == 'free':
                    #not occupied
                    latlon2 = LatLon(Latitiude(vehicle['coords'][0]),Longitude(vehicle['coords'][1]))
                    if latlon.distance(latlon2) <= dis:
                        vehs += vehicle

    return vehicles


@app.route('/getVehicles/<dis>', methods=['POST'])
def getVehicles(dis):
    if request.method == 'POST':
        print "Entered"
        lati = request.form['lat']
        longi = request.form['long']
        return getVehicle(dis,LatLon(Latitiude(lati),Longitude(longi)))


if __name__ == "__main__":
    app.run(debug=False)



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