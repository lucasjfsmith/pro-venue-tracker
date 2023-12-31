# # Sport-Venue-Tracker
Our goal is to create an interactive map that showcases the venues of teams in all sports leagues, allowing you to track and explore their locations. We also aim to add a feature that will focus on Baseball and create a model that will predict home run percentage based on the batting and pitching data obtained from Baseball Reference.

### Technical Roadmap:
Data Wrangling and Cleaning - Python:
We begin by leveraging the extensive Kaggle Sports Stadium Locations dataset, extracting latitude and longitude information. We then utilize Geoapify's Places API to fetch detailed venue data, including team name, latitude/longitude, and venue address. By combining all the relevant data, we will create a comprehensive and structured data frame for processing.

### MLB Batting and Pitching Data:
To enhance the application's functionality, we incorporate MLB batting and pitching data. This rich dataset, sourced from Baseball Reference, allows us to analyze and derive valuable insights.  By utilizing this dataset, we can provide users with additional information about the performance of teams and players during specific games or seasons.

### Map Build - JavaScript:
With the Flask API set up, we proceed to build an interactive map using JavaScript. By leveraging Leaflet and GeoJSON technologies, we can seamlessly integrate the relevant data provided by the Flask API. Users can now explore the map, filter by specific criteria, and view information about any stadium they click on. By implementing a Flask API in Python, we create a user-friendly application interface that presents a map, indicating each team's venue with distinguishable sports icons.

### Machine Learning Model:
As an added feature, we incorporate a machine learning model to predict home run percentage based on the batting and pitching data obtained from Baseball Reference. By analyzing historical data and training the model, users can obtain insights into the potential home run percentages based on the teams and venues.
