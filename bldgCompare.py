import pyodbc
import fuzzywuzzy
import cx_Oracle
import pandas as pd
from requests.auth import HTTPBasicAuth
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


#Oracle SQL Connection
user='DBO'
password='d3vcidh#d80'
host='usdl676.spe.sony.com'
port=30751
service_name = 'COSDIDH'
dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
gpmsdb = cx_Oracle.connect(user,password,dsn)


idhArchibus = gpmsdb.cursor()
idhArchibus.execute('select distinct(archibus_building) from idh_location_compare_vw')
idhArchibus = [list(x) for x in idhArchibus]
idhArchibusDf = pd.DataFrame(idhArchibus)
archibusOptions = idhArchibusDf[0].astype(str).values.tolist()

idhWorkday = gpmsdb.cursor()
idhWorkday.execute('select distinct(wd_building) from idh_location_compare_vw')
idhWorkday = [list(x) for x in idhWorkday]
idhWorkdayDf = pd.DataFrame(idhWorkday)
wdOptions = idhWorkdayDf[0].astype(str).values.tolist()

def bldgCompare(firstList, checkList):
    df = pd.DataFrame(columns=['value1', 'value2', 'score'])
    
    for i in firstList:
        extract = process.extract(str(i), checkList, limit=5)
        n=0
        for x in extract:
            s = pd.Series([str(i), str(extract[n][0]), str(extract[n][1])],index=['value1','value2','score'])
            df = df.append(s, ignore_index = True)
            n=n+1
            
        #df=df.append({'value1':str(i),
        #              'value2':str(highest[0]),
        #             'score':str(highest[1])})
        #value = str(i)+', '+str(highest[0])+', '+str(highest[1])
        #compare.append(value)
    return(df)
