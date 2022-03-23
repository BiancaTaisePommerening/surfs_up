# import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Add the SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#  import the Flask dependency
from flask import Flask, jsonify


# set up our database engine for the Flask application to access the SQLite database.
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

# reflect the database
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# create a Flask application called "app."
app = Flask(__name__)

# WELCOME ROUTE
# create Flask Route
@app.route("/")

# create a function welcome() with a return statement
# add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement.
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# PRECIPITATION ROUTE
# create a new route for Precipitation
@app.route("/api/v1.0/precipitation")

# create the precipitation() function
def precipitation():
    # add the line of code that calculates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   # write a query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # use jsonify() to format our results into a JSON structured file
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


# STATIONS ROUTE
# Define the Stations route.
@app.route("/api/v1.0/stations")

# create a new function called stations()
def stations():
    # create a query that will allow us to get all of the stations in our database
    results = session.query(Station.station).all()
    # use the function np.ravel(), with results as the parameter to start unraveling the results into a one-dimensional array.
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# MONTHLY TEMPERATURE ROUTE
# Define the monthly temperature route.
@app.route("/api/v1.0/tobs")

# create a function called temp_monthly()
def temp_monthly():
    # add the line of code that calculates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year.
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # unravel the results into a one-dimensional array and convert that array into a list
    temps = list(np.ravel(results))
    # use jsonify() to format our results into a JSON structured file
    return jsonify(temps=temps)

# STATISTICS ROUTE
# this route will be to report on the minimum, average, and maximum temperatures
# create starding and ending date routes.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create a function called stats()
# add a start parameter and an end parameter, and set them both to 'None'.
def stats(start=None, end=None):
    #create a query to select the minimum, average, and maximum temperatures from our SQLite database.
    # create a list called 'sel'
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]


    # add an if-not statement 
    # query our database using the list that we just made
    #unravel the results into a one-dimensional array and convert them to a list
    # jsonify our results and return them.
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)







