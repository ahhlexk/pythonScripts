import json
import pandas as pd
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
QA = 'https://gmdm-ods-qa.spe.sony.com:8055' #/ mlapp pa$$4mlA99
Prod = 'http://uspl746.spe.sony.com:8055'
date = "2021-03-01"
url = Prod+"/api/getUserClicks.sjs?since="+date+"T23:59:00.000"
#response = urllib.urlopen(url)
r = requests.get(url, auth=('SDash','SDash'),verify=False)
data = r.json()

df = pd.DataFrame.from_dict(data, orient='columns')
df = df.drop(columns=['Comments'])
df_time = df["TimeStamp"].str.split("T", n=1,expand=True)
df["Date"]=df_time[0]
df["Time"]=df_time[1]
df.drop(columns=["TimeStamp"], inplace=True)
#df2 = df.query('UserId == "PLuri"')
#tabcounts = df2.groupby('TabName').count().UserId

#print(tabcounts)
df.to_csv('C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Desktop\\user_click.csv', index=False)


