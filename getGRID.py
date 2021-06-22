import json
import pandas as pd
import requests
import urllib3
from requests.auth import HTTPBasicAuth


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = "http://gmdm-ods-dev.spe.sony.com:8050/rest-api/data/getGridData.sjs"
headers={'Content-type':'application/json', 'Accept':'application/json'}
auth = HTTPBasicAuth('admin', '620pwmlA#DGMGM')
#response = urllib.urlopen(url)
r = requests.get(url,headers=headers, auth=auth,verify=False)
data = r.json()
with open('grid.json', 'w') as f:
    json.dump(data, f)
