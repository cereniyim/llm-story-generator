# LLM Story Generator
LLM based app that generates brief stories using Strava activity data.

## Project Summary & Main Purpose
FastAPI based web service designed to run on local machines that creates stories using Strava data.

Users are authenticated through Strava. Web service allows users to get their last 3 activities. 

Then, an LLM model generates a story around 50 words for a given activity (might be a ride) based on the 
speed (as max_speed), distance, time (as moving_time) and the elevation (as total_elevation_gain) of each activity.

Moreover, users can list their processed activities.

The service has 3 endpoints in `activities` namespace:

![img.png](images/swagger.png)

**POST /activities/**: Creates activities from Strava.
![img.png](images/post_endpoint.png)

**PUT /activities/**: Takes activity_id as a parameter and returns the activity details, generated title and story. If 
activity is not present in the database then gets the activity from Strava.
![img.png](images/put_endpoint.png)

**GET /activities/processed/**: Lists all the activities the system has ever processed. A processed activity has a 
story and title assigned. By default, it gets last 3 activities.
![img.png](images/get_endpoint.png)


## How to Install and Use

**Pull Mongo Docker image**: It will pull the image from Docker Hub.
```shell script
docker pull mongo:latest
```

**Create local DB**
```shell script
docker run --name mongo -p 27017:27017 -d mongo:latest
```

**Start the service**
```shell script
uvicorn app.main:app 
```

You can access it and its documentation on Swagger http://0.0.0.0:8000/docs

## My Approach on Solving the Challenge and Key Architectural Decisions
TODO

## Further System Improvements
TODO

## For Developers
### Project organization
TODO
### Setup local environment & run unit tests
Change directory to your local repository
```shell script
cd <path-to-your-local-repository>
```

Create conda environment
```shell script
conda create --name llm-story-generator python=3.9.18
```

Activate environment
```shell script
conda activate llm-story-generator
```

Install requirements
```shell script
pip install -r requirements.txt
```

Add repository path to PYTHONPATH 
```shell script
export PYTHONPATH=<path-to-your-repo-root>
```

Change to project root directory and run unit tests
```shell script
py.test tests