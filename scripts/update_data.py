import yaml
import requests

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

url = config["api"]["base_url"]
api_key = config["api"]["service_key"]

params = {
    'serviceKey': api_key,
    'pageNo': '1',
    'numOfRows': '10',
    'period': '5',
    'zcode': '11'
}

response = requests.get(url, params=params)
print(response.content)
