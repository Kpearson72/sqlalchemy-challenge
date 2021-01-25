# import Dependencies
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Home Page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/weatherstation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>" 
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    meas_data = []
    for date, prcp in results:
        meas_dict = {}
        meas_dict['date'] = date
        meas_dict['prcp'] = prcp
        meas_data.append(meas_dict)

    meas_data = [{date:prcp} for date, prcp in results]

    # Return the JSON representation of your dictionary.
   

    return jsonify(meas_data)

@app.route("/api/v1.0/weatherstation")
def weatherstation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results2 = session.query(Station.station).all()

    session.close()

    # Convert list 
    list_stations = list(np.ravel(results2))

    return jsonify(list_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    
    active = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date >= 2016-8-23).\
        order_by(Measurement.date).all()

    session.close()
  
    active_list = list(active)

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(active_list)




   

# main block, run the flask app
if __name__ == '__main__':
    app.run(debug=True)