"Test the web service sending a post request"
import argparse
import json

import requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", type=str, default="http://0.0.0.0:5000")
    parser.add_argument("--text", type=str)

    args = parser.parse_args()

    text = dict(text=args.text)
    url = f"{args.server}/predict/"

    response = requests.post(url, json=text)
    print(json.dumps(response.json(), indent=2))
