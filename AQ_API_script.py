import requests
import json
import pandas as pd

#pd.set_option("display.max_colwidth", None)

url = "https://api.openaq.org/v2/latest/498?limit=100&page=1&offset=0&sort=asc"

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

results_df = pd.json_normalize(data['results'], record_path=['measurements'])
print(results_df)
# # if response.status_code == 200:
    
# print(f"Status Code: {response.status_code}")
# print(response.text)
# response.raise_for_status(HTTPError)



# response = requests.get(url, headers=headers)

# print(response.text)
