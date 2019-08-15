# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# flask tools
from flask import Flask, jsonify, render_template, url_for, request

# datetime dependency
import datetime as dt

#################################################
#                Database Setup                 #
#################################################

# Create the connection engine
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
#                  Flask Setup                  #
#################################################

# Create ClimateApp and pass __name__
ClimateApp = Flask(__name__)

#################################################
#                  Flask Routes                 #
#################################################

# >>> ROUTE 1 <<< #
# Define actions for the index route
@ClimateApp.route("/")
def index():
    '''List all available api routes with hyperlinks or submission forms to designated module in this app.'''
    # Display index.html page
    return render_template('index.html')
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #

# >>> ROUTE 2 <<< #
# Define actions for "/api/precipitation" route
@ClimateApp.route("/api/precipitation")
def prcp():
    '''Return a JSON list of precipitation data with "date" set as key'''

    # Query for all precipitation data
    prcp_retrv = session.query(Station.station, Measurement.date, Measurement.prcp).\
        filter(Station.station == Measurement.station).order_by(Measurement.date).all()

    # Close session
    session.close()

    # Create list of dictionaries data type to store "prcp" data with "date" set as key
    all_prcp = []
    for sta, date, prcp in prcp_retrv:
        prcp_dict = {}
        prcp_dict['station'] = sta
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)
    
    #  Return JSON format of all_prcp
    return jsonify(all_prcp)
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #

# >>> ROUTE 3 <<< #
# Define actions for "/api/stations" route
@ClimateApp.route("/api/stations")
def sta():
    '''Return a JSON list of stations info'''

    # List to store the arguments of Station queries
    sel_sta = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]

    # Query for all station data
    sta_retrv = session.query(*sel_sta).order_by(Station.station).all()

    # Close session
    session.close()

    # Create list of dictionaries data type to store "station" data
    all_sta = []
    for sta, name, lat, lng, elv in sta_retrv:
        sta_dict = {}
        sta_dict['station'] = sta
        sta_dict['name'] = name
        sta_dict['latitude'] = lat
        sta_dict['longitude'] = lng
        sta_dict['elevation'] = elv
        all_sta.append(sta_dict)
    
    # Return JSON format of "all_sta"
    return jsonify(all_sta)
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #

# >>> ROUTE 4 <<< #
# Define actions for "/api/temperature" route
@ClimateApp.route("/api/temperature")
def tobs_1yr():
    '''Return a JSON list of Temperature Observations (tobs) within one-year interval from the latest documented date'''

    # Query for date of the latest documented data from "measurement" table
    date_latest = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    # Determine the threshold date (date_thold) that is exactly one year apart (inclusive) from "date_latest"
    # Note that "dt.timedelta" automatically takes leap year into consideration
    date_thold_1yr = str(dt.datetime.strptime(date_latest, "%Y-%m-%d") - dt.timedelta(days=365))[:10]
    
    # Query for ("date", "tobs") data within one-year interval from "date_latest"
    tobs_1yr_retrv = session.query(Station.station, Measurement.date, Measurement.tobs).\
        filter(Station.station == Measurement.station).filter(Measurement.date >= date_thold_1yr).\
        order_by(Measurement.date).all()
    
    # Close session
    session.close()

    # Create list of dictionaries data type to store "date" and "tobs" data within one year interval from the latest documented date
    all_tobs_1yr = []
    for sta, date, tobs in tobs_1yr_retrv:
        tobs_1yr_dict = {}
        tobs_1yr_dict['date'] = date
        tobs_1yr_dict['station'] = sta
        tobs_1yr_dict['tobs'] = tobs
        all_tobs_1yr.append(tobs_1yr_dict)
    
    # Return JSON format of all_tobs_1yr
    return jsonify(all_tobs_1yr)
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #

# >>> ROUTE 5 <<< #
# Define actions for "/api/<start>" route
@ClimateApp.route("/api/<start>", methods=['GET', 'POST'])
def tobs_start_ab(start):
    '''Return a JSON list of the min, avg, and max tobs data for all dates no earlier than the start date'''

    # List to store the arguments of Station queries
    sel_tobs_start = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Query for ("date", "tobs") data with date no earlier than "start" date
    tobs_start_retrv = session.query(*sel_tobs_start).filter(Measurement.date >= start).all()

    # Close session
    session.close()

    # Create list of dictionaries data type to store "date" and "tobs" data for all dates no earlier than the start date
    all_tobs_start = []
    for tmin, tavg, tmax in tobs_start_retrv:
        tobs_start_dict = {'start_date':start}
        tobs_start_dict['tmin'] = tmin
        tobs_start_dict['tavg'] = tavg
        tobs_start_dict['tmax'] = tmax
        all_tobs_start.append(tobs_start_dict)
    
    # Return JSON format of "all_tobs_start"
    return jsonify(all_tobs_start)
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #

# >>> ROUTE 6 <<< #
# Define actions for "/api/<start>/<end>" route
@ClimateApp.route("/api/<start>/<end>", methods=['GET', 'POST'])
def tobs_start_end_ab(start, end):
    '''Return a JSON list of the min, avg, and max tobs data for all dates between the start and end dates (inclusive)'''

    # List to store the arguments of Station queries
    sel_tobs_start_end = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Query for ("date", "tobs") data with date no earlier than "start" date
    tobs_start_end_retrv = session.query(*sel_tobs_start_end).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Close session
    session.close()

    # Create list of dictionaries data type to store "date" and "tobs" data for all dates no earlier than the start date
    all_tobs_start_end = []
    for tmin, tavg, tmax in tobs_start_end_retrv:
        tobs_start_end_dict = {'start_date':start, 'end_date':end}
        tobs_start_end_dict['tmin'] = tmin
        tobs_start_end_dict['tavg'] = tavg
        tobs_start_end_dict['tmax'] = tmax
        all_tobs_start_end.append(tobs_start_end_dict)

    # Check if end date is earlier than start date
    if dt.datetime.strptime(start, "%Y-%m-%d") <= dt.datetime.strptime(end, "%Y-%m-%d"):    
        # Return JSON format of "all_tobs_start"
        return jsonify(all_tobs_start_end)
    else:
        # Return message indicating query checkup
        return f'You serious? End date is earlier than start date. Please double-check your query input!'
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #

# Execute the script
if __name__ == '__main__':
    ClimateApp.run(debug=True)