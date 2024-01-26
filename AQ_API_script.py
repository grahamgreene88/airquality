import requests
import json
import pandas as pd

url = "https://api.openaq.org/v2/measurements?location_id=498&parameter=o3&parameter=pm25&date_from=2023-12-23T01:20:56-05:00&date_to=2023-12-24T01:20:56-05:00&limit=1000"

headers = {
    "X-API-Key": "5eb79066433eb416b9a688101dfba9b40f44ffbbd58f913d2f8aafd4867395e5",
    "accept": "application/json"}

session = requests.Session()
session.headers.update(headers)

try:
    response = session.get(url, headers=headers)
    data = json.loads(response.text)
    print(data)
except(ConnectionError, TimeoutError, HTTPError) as e:
    print(e)

df = pd.json_normalize(data['results'])
pd.set_option('display.max_columns', None)
print(df)
# # if response.status_code == 200:
    
# print(f"Status Code: {response.status_code}")
# print(response.text)
# response.raise_for_status(HTTPError)