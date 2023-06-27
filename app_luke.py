import psycopg2
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
from api_key import postgres_pw

engine = create_engine(f'postgresql+psycopg2://postgres:{postgres_pw}@localhost:5432/project_3')

Base = automap_base()

Base.prepare(autoload_with=engine)

Venue = Base.classes.venue
Team = Base.classes.team
League = Base.classes.league

# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/venues")
def venue():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all venues"""
    # Query all venues
    results = session.query(Venue.venue_id, Venue.venue_name, Venue.venue_state, Venue.venue_address, Venue.venue_lat, Venue.venue_lon).all()

    session.close()

    all_venues = []
    for result in results:
        venue_dict = {}
        venue_dict["venue_id"] = result[0]
        venue_dict["venue_name"] = result[1]
        venue_dict["venue_state"] = result[2]
        venue_dict["venue_address"] = result[3]
        venue_dict["venue_lat"] = float(result[4])
        venue_dict["venue_lon"] = float(result[5])
        all_venues.append(venue_dict)

    return jsonify(all_venues)


@app.route("/api/teams")
def team():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all teams"""
    # Query all teams with league joined
    results = session.query(Team.team, Team.venue_id, League.league).filter(Team.league_id == League.league_id).all()

    session.close()

    all_teams = []
    for result in results:
        team_dict = {}
        team_dict["team_id"] = result[0]
        team_dict["venue_id"] = result[1]
        team_dict["league"] = result[2]

        all_teams.append(team_dict)

    return jsonify(all_teams)


if __name__ == '__main__':
    app.run(debug=True)

