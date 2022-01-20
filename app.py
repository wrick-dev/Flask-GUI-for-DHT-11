from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
import pymongo
app = Flask(__name__)

pycon = pymongo.MongoClient("mongodb://70.70.1.104:27017")
tempdb = pycon["tempdb"]
roomcol = tempdb["roomtemp"]
humidity = pycon["humidity"]
humcol = humidity["reading"]
#x = roomcol.find_one(sort=[('TimeStamp', pymongo.DESCENDING)])
x = roomcol.find().sort("TimeStamp",-1)
y = humcol.find().sort("TimeStamp",-1)
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
	temp = x.next()
	Temperature = float(temp["Temperature(Celsius)"].strip('Temperature: '))
	hum = y.next()
	Humidity = float(hum["Humidity"].strip('Humidity: '))
	print(Humidity)
	data = [time() * 1000, Temperature, Humidity]
	response = make_response(json.dumps(data))
	response.content_type = 'application/json'
	return response


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
