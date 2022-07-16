# Deploy of a ML model as a web service on Google Cloud Run

## Description
In this repo, we build a machine learning model as a web service and deploy this model to GCP's Cloud Run.

* We used [Poetry](https://python-poetry.org/) for python packaging and dependency management.
* [FastAPI](https://fastapi.tiangolo.com/) framework to expose and endpoint for predictions, and [uvicorn](https://www.uvicorn.org/) as our web server implementation.
* [Docker](https://www.docker.com/) to build a deployable container (dockerized service).
* Cloud Build API to build and push our docker image to GCR (Google Container Registry).
* Could Run to deploy the model.

This repo was based on a medium article [found here](https://towardsdatascience.com/deploy-your-ml-model-as-a-web-service-in-minutes-using-gcps-cloud-run-ee9d433d8787).

## Code Reproduction
After cloning this repo, [install Poetry](https://python-poetry.org/docs/#installation), [Docker](https://www.docker.com/get-started/) and [gcloud CLI](https://cloud.google.com/sdk/docs/install) - if you haven't already. The next sections assume you're already in the root directory of this repo.

### Install Poetry project
```bash
$ poetry install  # install all packages in toml
```

### Testing the web server locally with uvicorn
The FastAPI docs can be accessed at web server at `http://0.0.0.0:5000/docs`
```bash
$ poetry run uvicorn --app-dir ner_model app:app --host 0.0.0.0 --port 8080 --workers 2
```

### Build Docker locally 
```bash
$ make build_docker
# OR
$ docker build . -t ner_model:0.0.1
```

### Run Docker locally 
```bash
$ make run_docker
# OR
$ docker run -p 5000:5000 -i -t ner_model:0.0.1
```

### Google Cloud Platform
You need to enable Cloud Build API and Cloud Run on your project before executing the commands below. 

#### Cloud Build
Cloud Build API will build your docker image and store it in GCR (Google Container Registry).
```bash
$ make run_grc_build
```
#### Cloud Run
Cloud Run will deploy the image saved on GCR as a service. You can access FastAPI docs using the service url provided (`{service_url}/docs`)
```bash
$ make cloud_run_deploy
```
