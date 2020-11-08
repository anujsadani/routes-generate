# routes-generate

The Routes generate application helps the user to create a unique endpoint and show the data dumped into it in a user-friendly manner. Every hit on the created endpoint is recorded and displayed for the user to inspect the data.
The endpoint and its relevant data are destroyed exactly an hour from when it is created, the reason being these are short-lived endpoints purely used for testing purposes.

## Description
The application consist of 3 major pieces
- Backend: Python, Postgres
Python(flask) provides the REST APIs for the the application and data is stored in Postgres DB (for simplicity, consider to run db in container)
- Frontend: Node, Knockout.js, Bootstrap 4
Node provide a light-weight server to host the html pages. Whereas, knockout along with jquery provides the data binding and api consumtion.
- Scheduler: crontab 
A cron job that runs every 1 minute to remove the expired routes.

## Setup

Install Docker Engine on Ubuntu (refer: https://docs.docker.com/engine/install/)
```
# Check if docker is available
> docker --version
Docker version 19.03.13
```

Install python3 (refer: https://www.python.org/downloads)
```
> python3 --version
Python 3.7.6
```

Install npm (refer: https://www.npmjs.com/get-npm)
Check that you have node and npm installed (npm is installed with Node.js)
```
> node -v
v8.0.0
> npm -v
5.0.0
```

### Backend
Start with project directory. 

1. Setup the database
Note: You can have postgres db installed on the system, for simplicity, plan to use docker image.
```
# Docker run the postgres image
docker run --name route_db -d -e POSTGRES_PASSWORD=root -e POSTGRES_USER=root -p 5432:5432 -d postgres:12-alpine
# Create the database in the image
> docker exec -it route_db bash
> PGPASSWORD=root psql -h localhost -U root -c "create database routesdb"
# exit the bash session
```
Note: You may need to run the commands with sudo.

2. Setup the flask application
```
# Go into the backend directory
> cd backend 
# Create a virtual environment 
> python3 -m venv rapp
# Activate the environment
> source rapp/bin/activate
# Install the required packages
> pip install --no-cache-dir -r requirements.txt
```

Run the flask application
```
> export FLASK_APP=app.py; flask run
```
The application will be up and running on port `5000`.

3. Setup the node application
```
# install the npm packages to server the static html pages
> npm install connect serve-static
# Run the node application
> node server.js
```
The application will be up and running on port `8080`

## Usage
- Go to browser `http://localhost:8080/`
- Click on "Create URL" button to get the unique url (active for 1 hour).
- Use `curl` or `postman` (or tool of your choice, to make api call).
hit the POST endpoint `http://localhost:5000/api/v1/hits/<unique id>`
```
curl -d '{"key1":"value1", "key2":"value2"}' \
     -H "Content-Type: application/json" \
     -X POST http://localhost:5000/api/v1/hits/006a47f3-1a65-4764-8d88-a64ee9dc309a
```

