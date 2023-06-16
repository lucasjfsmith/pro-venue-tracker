# pro-venue-tracker
An application that displays and tracks your attendance at professional sports venue within the NFL, MLB, NBA, NHL, and MLS

### Goal
Create an interactive map that shows markers for each team’s venue in the MLB, NFL, NBA, NHL, and MLS (https://www.kaggle.com/datasets/logandonaldson/sports-stadium-locations). The map will allow users to filter by criteria such as:
*	Ever attended
*	League/sport
Additionally, users will be able to click on any stadium marker and see:
*	An image of the venue
*	When the next game will be played at the venue
*	If the user has attended
*	Venue capacity (?)

## Technical Roadmap

### Data wrangling and cleaning – Python
Use latitude and longitude from Kaggle sports stadium locations dataset (https://www.kaggle.com/datasets/logandonaldson/sports-stadium-locations) to pull information on the venue from Geoapify’s Places API. Between these two sources we will pull the following data:
*	Team name
*	Latitude/longitude
*	Venue address
*	Venue capacity
Kim/Luke are looking for APIs for the following information:
*	Next home game
*	Image of the venue
*	Combine all relevant data into a DataFrame

### Data storage – TBD
*	Still need to decide between Postgres and MongoDB

### Flask API – Python
*	Create a Flask API (see lesson plan 10-Advanced-SQL day 3)

### Map Build – JavaScript
*	Accept data using flask API
*	Use Leaflet/GeoJSON to generate map
*	Still need to determine a new JS library for the team to use
