## Step 4 - Climate App
# `/api/v1.0/precipitation`
# `/api/v1.0/stations`
# `/api/v1.0/tobs`
# `/api/v1.0/<start>` 
#`/api/v1.0/<start>/<end>`


from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Hawaii_vacation.sqlite")
print("Connected to DB")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print("Reflected tables")

# Save reference to the table

Stations = Base.classes.station
Measurment = Base.classes.measurment   

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
# create an app, being sure to pass __name__
app = Flask(__name__)

#define what to do when user hit the index route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Beheshteh's weather channel: <br/>"
        f"<br/>"
        f"Available Routes:<br/>" 
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>    (Please provide your starting date in the format of 2016-08-23)<br/>"
        f"/api/v1.0/<start>/<end>     (Please provide your starting date and ending date in the format of 2016-08-23)"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the dates and temperature observations from the last year.
    # Convert the query results to a Dictionary using `date` as the key and
    # `tobs` as the value.
    # Return the json representation of your dictionary.

    results = session.query(Measurment.date, Measurment.tobs).filter(Measurment.date.between('2016-08-23', '2017-08-23'))
            
    # Convert list of tuples into dic
    precipitation_dic = []
    for result in results:
        result_dict = {}
        result_dict["key"] = result.date
        result_dict["value"] = result.tobs
        precipitation_dic.append(result_dict)

    return jsonify(f"The date and the tempeature of this period (2016-08-23, 2017-08-23):",precipitation_dic)


@app.route("/api/v1.0/stations")
def stations():
    # Return a json list of stations from the dataset.
    results = session.query(Stations.station)
    all_station = [record.station for record in results]
    return jsonify(f"The list of all stations:",all_station)


@app.route("/api/v1.0/tobs")
def temp_obs():
    # Return a json list of Temperature Observations (tobs) for the previous year
    results = session.query(Measurment.tobs).filter(Measurment.date.between('2016-08-23', '2017-08-23'))
    all_tobs = [record.tobs for record in results]
    return jsonify(f"The list of Temperature Observations (tobs) for the previous year (2016-08-23, 2017-08-23):",all_tobs)    


@app.route("/api/v1.0/<start>")
def calc_temp1(start):
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all 
    #dates greater than and equal to the start date.

    TMIN = session.query(func.min(Measurment.tobs)).filter(Measurment.date >= start)[0][0]
        
    TAVG = session.query(func.avg(Measurment.tobs)).filter(Measurment.date >= start)[0][0]
        
    TMAX = session.query(func.max(Measurment.tobs)).filter(Measurment.date >= start)[0][0] 

    return jsonify([TMIN, TAVG, TMAX])

    #return jsonify({"error": f"tempture with the start date {start} not found."}), 404

@app.route("/api/v1.0/<start>/<end>")
def calc_temp2(start, end):
    # When given the start and the end date, calculate the `TMIN`, `TAVG`, and 
    #`TMAX` for dates between the start and end date inclusive.

    TMIN = session.query(func.min(Measurment.tobs)).filter(Measurment.date.between(start, end))[0][0]
        
    TAVG = session.query(func.avg(Measurment.tobs)).filter(Measurment.date.between(start, end))[0][0]
        
    TMAX = session.query(func.max(Measurment.tobs)).filter(Measurment.date.between(start, end))[0][0] 

    return jsonify([TMIN, TAVG, TMAX])

    #return jsonify({"error": f"tempture with the start date {start} not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)

