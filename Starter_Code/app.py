# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measure = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<center><h1><strong>Welcome to the App!<center><h1><strong></br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
           #10.3.10 activity
            #     all_passengers = []
            # for name, age, sex in results:
            #     passenger_dict = {}
            #     passenger_dict["name"] = name
            #     passenger_dict["age"] = age
            #     passenger_dict["sex"] = sex
            #     all_passengers.append(passenger_dict)

    return(f"Finish Precip")

@app.route("/api/v1.0/stations")
def station():
    #call the needed info and close the session afterwards
    station_count = session.query(Measure.station, func.count(Measure.station)).group_by(Measure.station).order_by(func.count(Measure.station).desc()).all()
    session.close()
    #get it into the right format
    station_stuff = list(np.ravel(station_count))
    return jsonify(station_stuff) 
    return(station_stuff)

@app.route("/api/v1.0/tobs")
def tobs():
    #call the needed info and close the session afterwards
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station_count = session.query(Measure.station, func.count(Measure.station)).group_by(Measure.station).order_by(func.count(Measure.station).desc()).all()
    tobby = session.query(Measure.tobs).filter(Measure.station == station_count[0][0]).filter(Measure.date >= query_date).all()
    session.close()
    #get it into the right format
    tobby_stuff = list(np.ravel(tobby))
    return jsonify(tobby_stuff) 

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp(start = None, end = None):
    #call the needed info
    stats = [func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)]
    #loop through if there is no end date provided and format
    if not end:
        result = session.query(*stats).filter(Measure.date >= start).all()
        session.close()
        results = list(np.ravel(result))
        return jsonify(results) 
    #provide range if end date is provided and format
    result = session.query(*stats).filter(Measure.date >= start).filter(Measure.date <= end).all()
    session.close()
    results = list(np.ravel(result))
    return jsonify(results) 


if __name__ == '__main__':
    app.run(debug=True)