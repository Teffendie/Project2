import os

import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:CD!1234567a@localhost/realestate"
# engine = create_engine("mysql://root:CD!1234567a@localhost/realestate")
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Listing = Base.classes.newmonthlylistings_allhomes_2019
Price = Base.classes.city_medianlistingprice_allhomes_2019
Affordability = Base.classes.affordability_wide_2019q1_public_2019
States = Base.classes.statelist

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/usstates")
def usstates():
    """Return a list of US States."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(States).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.StateName))

@app.route("/listing")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Listing).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])


@app.route("/samples/<sample>")
def samples(sample):
    """Return `RegionName` and `May2019`."""
    stmt = db.session.query(Listing).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    sample_data = df.loc[df.StateName==sample , ["RegionName","May2019"]]

    # Sort by sample
    sample_data.sort_values(by="May2019", ascending=False, inplace=True)
    
    # Format the data to send as json
    data = {
        "RegionName": sample_data.RegionName.values.tolist(),
        #"StateName": sample_data[sample].values.tolist(),
        "May2019": sample_data.May2019.tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
