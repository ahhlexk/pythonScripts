import pandas as pd

#file = "C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Documents\\_Rights\\Episode_Segments_06162020.csv"
file = "C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Documents\\_Rights\\Season_Segments_06162020.csv"
df = pd.read_csv(file, encoding = "ISO-8859-1")

df = df.rename(columns={"ParentProdID (Series)":"SERIES_ID"})
df = df.drop(columns=["PRODUCTID","FULLTITLE","CONTRACT_NO","RIGHTSEGMENTID","RIGHTSEGMENTTYPEDESC"])
df2 = df.groupby(["SERIES_ID","MEDIALIST","TERRITORYLIST","TERMEXPIRATION"]).count()
df2 = df2.reset_index()
df3 = df2[df2['SERIES_ID'].duplicated()==True]
#df3.to_csv("C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Documents\\_Rights\\Episode_Segments_Grouped_06162020.csv",header=True)
df3.to_csv("C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Documents\\_Rights\\Season_Segments_Grouped_06162020.csv",header=True, index=False)
