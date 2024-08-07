# Parks API
Park API built with Flask that pulls nearby parks from Google Places API

## Features
- Docker-compose dev environment that updates upon changes
- Returns nearby parks data from a postal zipcode including:

  - Park name
  - Address
  - Rating
  - Picture
- Connected to [main app](https://github.com/Ramsey2022/day_planner) and database via Docker network

# Demo
<img src="img/planner_parks_demo.png" alt="parks api demo">
<img src="img/flask_parks_test.png" alt="parks pytest demo">