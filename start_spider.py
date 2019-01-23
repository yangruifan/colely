import requests
import json

datas = {
    "source_id": "2",
}

url = "http://10.125.0.8:12310/api/v1/genlist"
datas = json.dumps(datas)
response = requests.post(url=url,
                         data=datas,
                         )
print(response)
print(response.text)