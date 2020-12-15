import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app = Flask(__name__)

lastYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"These are all the routes that are available:<br/>"
        f"/api/v1.0/precipitation<br/>/api/v1.0/stations<br/>/api/v1.0/tobs<br/>/api/v1.0/temp/start/end"
      
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
  
    

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= lastYear).all()

    precip = []

    for p in precipitation:
        day = {p.date: p.prcp for date, 'Station' : p.station}
        precip.append(day)    
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    
    names = session.query(Station.station).all()
    stations_names = list(np.ravel(names))
    return jsonify(stations=station_names)


@app.route("/api/v1.0/tobs")
def temp():
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= lastYear).\
        filter(Measurement.station =='USC00519281').all()

    temprature = list(np.ravel(results))

    return jsonify(temps=temprature)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats():
    #didnt figure out. 

if __name__ == '__main__':
    app.run()
