VERSION := 0.0.1
APP_NAME := ner_model

build_docker:
	docker build . -t ${APP_NAME}:latest -t ${APP_NAME}:${VERSION}

run_docker:
	docker run -p 5000:5000 -i -t ${APP_NAME}:${VERSION}

PROJECT_ID := $(shell gcloud config get-value project)
HOSTNAME := eu.gcr.io
GCR_TAG := ${HOSTNAME}/${PROJECT_ID}/${APP_NAME}:${VERSION}

run_grc_build:
	echo "${GCR_TAG}"
	gcloud builds submit --tag ${GCR_TAG} -q

cloud_run_deploy:
	gcloud run deploy ner-app --image=${GCR_TAG} --max-instances=2 --min-instances=0 --port=5000 \
	--allow-unauthenticated --region=europe-west1 --memory=2Gi --cpu=4 -q

cloud_run_delete:
	gcloud run services delete ner-app --region=europe-west1 -q