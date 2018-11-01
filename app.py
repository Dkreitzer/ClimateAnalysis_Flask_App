import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import MetaData
from sqlalchemy import Table
from flask import Flask, jsonify
import datetime as dt

import json
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"<strong>Welcome to Hawaii's Vacation Temp and Precipitation App!</strong><br/>"
        f"<br/>"
        f"A couple of quick notes:<br/>"
        f"The range of data in the avaiable dataset is from 2010-1-1 to 2017-8-23<br/>"
        f"Please note the syntax for dates, this app exclusively uses Year-Month-Date<br/>"
        f"The last two links below provide custom range returns of Minimum Temperature (F), Average Temperature, and High Temperature<br/>"
        f"For a custom range return, please enter in the start and end dates directly into the url in place of 'start' and 'end' <br/>"
        f"<br/>"
        f"<br/>"
        f"<strong>Available Routes:</strong><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start-end/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    """Dictionary with date and precipitation values"""
    # Query all dates and prcp values
    yearF_last_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    yearB_last_date = yearF_last_date + dt.timedelta(days = 365)
    yeardata = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= yearF_last_date).all()

    key=[yeardata[i][0] for i in range(len(yeardata))]
    values=[yeardata[i][1] for i in range(len(yeardata))]
    results=dict(zip(key,values))
    return jsonify(results)



@app.route("/api/v1.0/stations")
def stations():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    # Save reference to the table
    Station = Base.classes.station
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query all station names
    results = session.query(Station.station).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    # Save reference to the table
    Measurement = Base.classes.measurement
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates and prcp values
    yearF_last_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    yeardata = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= yearF_last_date).all()

    key=[yeardata[i][0] for i in range(len(yeardata))]
    values=[yeardata[i][1] for i in range(len(yeardata))]
    results=dict(zip(key,values))
    return jsonify(results)

@app.route("/api/v1.0/start/<start>")
def calc_temps(start):
# Engine
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    # Save reference to the table
    Measurement = Base.classes.measurement
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    canonicalized = start.replace(" ", " ")
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=start).all()

    return jsonify(results)


   
if __name__ == '__main__':
    app.run(debug=True)
