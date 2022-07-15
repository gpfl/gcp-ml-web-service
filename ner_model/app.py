"FastAPI Prediction App"
from dataclasses import dataclass
from typing import List

from fastapi import FastAPI

from model import predict_entities


@dataclass
class Query:
    "Stores input text for prediction."
    text: str


@dataclass
class Entity:
    "Stores entity information."
    text: str
    label: str
    start_idx: int
    end_idx: int


@dataclass
class Response:
    "Response from model api."
    text: str
    entities: List[Entity]


app = FastAPI()


@app.post("/predict/", response_model=Response)
def predict(in_query: Query):
    entities = predict_entities(in_query.text)

    return Response(text=in_query.text, entities=[Entity(**x) for x in entities])
