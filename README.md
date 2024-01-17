# llm-story-generator
LLM based app that generates brief stories


## Project Summary & Main Purpose
TODO


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

### Endpoints
TODO

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