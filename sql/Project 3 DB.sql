/*DROP TABLE events;*/
DROP TABLE team CASCADE;
DROP TABLE league CASCADE;
DROP TABLE venue CASCADE;
DROP TABLE event CASCADE;



/*Create the tables*/
CREATE TABLE venue(
	venue_id INTEGER PRIMARY KEY,
	venue_name VARCHAR,
	venue_city VARCHAR,
	venue_state VARCHAR,
	venue_country VARCHAR,
	venue_address VARCHAR,
	venue_lat DECIMAL,
	venue_lon DECIMAL,
	venue_capacity DECIMAL,
	next_event_id INTEGER
);


CREATE TABLE league(
	league_id INTEGER PRIMARY KEY,
	league VARCHAR
);


CREATE TABLE team(
    team_id INTEGER PRIMARY KEY,
	team VARCHAR,
	venue_id INTEGER,
	FOREIGN KEY (venue_id) REFERENCES venue(venue_id),
    league_id INTEGER,
    FOREIGN KEY (league_id) REFERENCES league(league_id) 
);


CREATE TABLE event (
	event_id SERIAL PRIMARY KEY,
	home_id INTEGER,
	FOREIGN KEY (home_id) REFERENCES team(team_id),
	away_id INTEGER,
	FOREIGN KEY (away_id) REFERENCES team(team_id),
	venue_id INTEGER,
	FOREIGN KEY (venue_id) REFERENCES venue(venue_id),
	event_timestamp_cst TIMESTAMP
);