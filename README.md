# Deploy of a ML model as a web service on Cloud Run

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
```bash
$ poetry run uvicorn --app-dir ner_model app:app --host 0.0.0.0 --port 5000 --workers 2
```
The FastAPI docs can be accessed at web server at `http://0.0.0.0:5000/docs`

To test the model results, `test.py` script sends a POST request to the FastAPI exposed endpoint `http://0.0.0.0:5000/predict/`.
```bash
$ python test.py --text 'Stonehenge is a prehistoric monument on Salisbury Plain in Wiltshire, England, two miles (3 km) west of Amesbury.'

# Output
{
  "text": "Stonehenge is a prehistoric monument on Salisbury Plain in Wiltshire, England, two miles (3 km) west of Amesbury.",
  "entities": [
    {
      "text": "Stonehenge",
      "label": "GPE",
      "start_idx": 0,
      "end_idx": 10
    },
    {
      "text": "Salisbury Plain",
      "label": "FAC",
      "start_idx": 40,
      "end_idx": 55
    },
    {
      "text": "Wiltshire",
      "label": "GPE",
      "start_idx": 59,
      "end_idx": 68
    },
    {
      "text": "England",
      "label": "GPE",
      "start_idx": 70,
      "end_idx": 77
    },
    {
      "text": "two miles",
      "label": "QUANTITY",
      "start_idx": 79,
      "end_idx": 88
    },
    {
      "text": "3 km",
      "label": "QUANTITY",
      "start_idx": 90,
      "end_idx": 94
    },
    {
      "text": "Amesbury",
      "label": "GPE",
      "start_idx": 104,
      "end_idx": 112
    }
  ]
}
```

---
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
---
### Google Cloud Platform
You need to enable Cloud Build API and Cloud Run on your project before executing the commands below. 

#### Cloud Build
Cloud Build API will build your docker image and store it in GCR (Google Container Registry).
```bash
$ make run_grc_build
```
#### Cloud Run
Cloud Run will deploy the image saved on GCR as a service. 
```bash
$ make cloud_run_deploy
```
You can access FastAPI docs using the service url provided (`${SERVICE_URL}/docs`)

#### Testing the GCP hosted app
```bash
$ export SERVICE_URL='https://...' # your service url provided by Cloud Run
$ python test.py --server "${SERVICE_URL}" --text 'Stonehenge is a prehistoric monument on Salisbury Plain in Wiltshire, England, two miles (3 km) west of Amesbury.'
```