import psycopg2
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
# from api_key import postgres_pw
import datetime as dt
import pandas as pd
# import pickle
# import re
import os

# engine = create_engine(f'postgresql+psycopg2://postgres:{postgres_pw}@localhost:5432/project_3')
postgres_pw = os.environ.get('postgres_pw')
engine = create_engine(f'postgresql+psycopg2://lucasjfsmith:{postgres_pw}@dpg-cjn76gsdfrcc73d02qag-a/venue_tracker')

Base = automap_base()

Base.prepare(autoload_with=engine)

Venue = Base.classes.venue
Team = Base.classes.team
League = Base.classes.league
Event = Base.classes.event

# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/chart")
# def chart():
#     return render_template("chart.html")

@app.route("/api/venues")
def venue():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all teams"""
    # Query all teams with league joined
    results = session.query(Team.team, League.league,
                            Venue.venue_name, Venue.venue_state,
                            Venue.venue_address, Team.team_id,
                            Venue.venue_lat, Venue.venue_lon).\
                                filter(Team.league_id == League.league_id).\
                                filter(Team.venue_id == Venue.venue_id).all()

    venues_dict = {}

    for result in results:
        team_dict = {}
        team_dict["team"] = result[0]
        team_dict["league"] = result[1]
        team_dict["venue_name"] = result[2]
        team_dict["venue_state"] = result[3]
        team_dict["venue_address"] = result[4]
        team_dict["team_id"] = int(result[5])
        team_dict["venue_lat"] = float(result[6])
        team_dict["venue_lon"] = float(result[7])

        venue_name = result[2]

        if venue_name not in venues_dict.keys():
            venues_dict[venue_name] = [team_dict]
        else:
            venues_dict[venue_name].append(team_dict)

    today = dt.date.today()

    for venue in venues_dict:
        for team in venues_dict[venue]:
            # if team["league"] != "NBA":
            home_id = team["team_id"]

            next_event = session.query(Event.timestamp, Event.away_id).\
                                        filter(Event.home_id == home_id).\
                                        filter(Event.timestamp > today).\
                                        order_by(Event.timestamp).limit(1).all()
            
            event_time = next_event[0][0].strftime("%Y-%m-%d %I:%M %p") + " EST"


            team["next_event"] = [event_time]
            away_id = next_event[0][1]

            away_team = session.query(Team.team).filter(Team.team_id == away_id)[0][0]
            team["next_event"].append(away_team)

            # else:
            #     team["next_event"] = "NBA Schedule not yet released."

    session.close()

    return jsonify(venues_dict)

# @app.route("/api/predictions")
# def predictions():

#     # Bring in todays game from Baseball Reference
#     todays_game_dfs = pd.read_html('https://www.baseball-reference.com/previews/')

#     # Remove unwanted dfs from list
#     postponed_list = []
#     incomplete_list = []

#     for i in range(len(todays_game_dfs)):
#         if len(todays_game_dfs[i].columns) == 3:
#             if todays_game_dfs[i].iloc[0,2] == 'Postponed':
#                 postponed_list.append(i)
#     for i in postponed_list:
#         todays_game_dfs.pop(i)

#     for i in range(len(todays_game_dfs)):
#         if len(todays_game_dfs[i]) == 1:
#             incomplete_list.append(i)
#     for i in incomplete_list:
#         todays_game_dfs.pop(i)
    
#     # Loop through every other df to create dfs to build off for each game

#     game_dfs_clean = []

#     for i in range(1,len(todays_game_dfs),2):
        
#         # Create a df for the specific game
#         game_df = todays_game_dfs[i]
        
#         # Rename columns
#         game_df = game_df.rename(columns={0:'Team',1:'Pitcher'})
        
#         #Add the time from previous df
#         time_string = todays_game_dfs[i-1].iloc[1,2]
#         date_string = dt.date.today().strftime("%Y-%m-%d")
#         datetime_string = date_string+" "+time_string+' EST'
#         game_df["Datetime"] = datetime_string

#         for i in range(len(game_df)):
#             # Create 'Next Opp Arm_R' column
#             pitcher = game_df.loc[i,'Pitcher']
#             throws = re.findall("[LR]HP", pitcher)[0]
#             if throws == 'RHP':
#                 throws_binary = 1
#             else:
#                 throws_binary = 0

#             game_df.loc[i,'Next Opp Arm_R'] = throws_binary

#             # Create 'Next H/A_H' 
#             if i == 0:
#                 game_df.loc[i,'Next H/A_H'] = 0
#             elif i == 1:
#                 game_df.loc[i,'Next H/A_H'] = 1

#         game_df=game_df.drop(columns='Pitcher')

#         game_dfs_clean.append(game_df)
    
#     # Loop through each df and add remaing features to the df
#     mlb_teams = list(pd.read_csv('Home Run Classification/mlb_teams.csv')['Abbreviation'])

#     for df in game_dfs_clean:

#         # BATTING
#         for i in range(len(df)):
#             url_1 = "https://www.baseball-reference.com/teams/tgl.cgi?team="
#             url_b = "&t=b&year=2023"
#             url = f"{url_1}{df.loc[i,'Team']}{url_b}"
#             team_df = pd.read_html(url)[0]
#             team_batting = team_df.iloc[-1:]

#             # Extract team batting data
#             batting_cols = ['HR','BA','OBP','SLG','OPS']
#             team_batting_features = team_batting[batting_cols].reset_index(drop=True)

#             df.loc[i,'HRs Hit'] = team_batting_features.loc[0,'HR']
#             df.loc[i,'BA'] = team_batting_features.loc[0,'BA']
#             df.loc[i,'OBP'] = team_batting_features.loc[0,'OBP']
#             df.loc[i,'SLG'] = team_batting_features.loc[0,'SLG']
#             df.loc[i,'OPS'] = team_batting_features.loc[0,'OPS']


#             # PITCHING
#             url_p = "&t=p&year=2023"

#             if i == 0:
#                 opp_team = df.loc[1,'Team']
#             if i == 1:
#                 opp_team = df.loc[0,'Team']

#             url = f"{url_1}{opp_team}{url_p}"
#             opp_team_df = pd.read_html(url)[1]
#             opp_team_pitching = opp_team_df.iloc[-1:]

#             pitching_cols = ['ERA','Pitchers Used (Rest-GameScore-Dec)']
#             opp_team_pitching_features = opp_team_pitching[pitching_cols].reset_index(drop=True)

#             df.loc[i, 'Opp ERA'] = opp_team_pitching_features.loc[0,'ERA']
#             opp_pitchers_used = opp_team_pitching_features.loc[0,'Pitchers Used (Rest-GameScore-Dec)'].split(',')
#             df.loc[i, 'Num Pitchers Used'] = len(opp_pitchers_used)

        
#         df['Next Opp Arm_R']=df['Next Opp Arm_R'].astype(int)
#         df['Next H/A_H']=df['Next H/A_H'].astype(int)
#         df['Num Pitchers Used']=df['Num Pitchers Used'].astype(int)
#         df['HRs Hit']=df['HRs Hit'].astype(int)
#         df['BA']=df['BA'].astype(float)
#         df['OBP']=df['OBP'].astype(float)
#         df['SLG']=df['SLG'].astype(float)
#         df['OPS']=df['OPS'].astype(float)
#         df['Opp ERA']=df['Opp ERA'].astype(float)
        
#         for team in mlb_teams:
#             col_name = "Next Venue_"+team
#             df[col_name] = 0
#         home_team = df.loc[1,'Team']
#         venue = "Next Venue_"+home_team
#         df[venue] = 1

#     # Bring in model with pickle
#     model = pickle.load(open('Home Run Classification/model-all.pkl', 'rb'))

#     # Arrange features for model
#     features = "HRs Hit,BA,OBP,SLG,OPS,Opp ERA,Num Pitchers Used,Next H/A_H,Next Venue_ARI,Next Venue_ATL,Next Venue_BAL,Next Venue_BOS,Next Venue_CHC,Next Venue_CHW,Next Venue_CIN,Next Venue_CLE,Next Venue_COL,Next Venue_DET,Next Venue_HOU,Next Venue_KCR,Next Venue_LAA,Next Venue_LAD,Next Venue_MIA,Next Venue_MIL,Next Venue_MIN,Next Venue_NYM,Next Venue_NYY,Next Venue_OAK,Next Venue_PHI,Next Venue_PIT,Next Venue_SDP,Next Venue_SEA,Next Venue_SFG,Next Venue_STL,Next Venue_TBR,Next Venue_TEX,Next Venue_TOR,Next Venue_WSN,Next Opp Arm_R"
#     features_order = features.split(',')

#     model_game_output = []

#     for game in game_dfs_clean:
#         X = game[features_order]
#         game_prediction = model.predict(X)
        
#         game_dict = {
#             "home_team" : game.iloc[1,0],
#             "away_team" : game.iloc[0,0],
#             "datetime" : game.iloc[0,1],
#             "home_hr": game_prediction[1],
#             "away_hr": game_prediction[0]
#         }
        
#         model_game_output.append(game_dict)
        
#     return jsonify(model_game_output)
    
if __name__ == '__main__':
    app.run(debug=True)

