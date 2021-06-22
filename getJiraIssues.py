import http.client
import json

conn = http.client.HTTPSConnection("sonypictures.atlassian.net")
headers = {
    'authorization': "2kFfYqoxdtFXXymSXaSQ6D36",
    'cache-control': "no-cache"
}
conn.request("GET", "/rest/api/2/search?jql=project%20%3D%20""IT_GMDM""%20AND%20status%20changed%20to%20Released&startAt=0&maxResults=1", headers=headers)
res = conn.getresponse()
data = res.read()
jsonstr = data.decode("utf-8")
jsondata = json.loads(jsonstr)
print(jsondata)
