import pandas as pd

df = pd.read_csv('C:\\Users\\ajkim\\Downloads\\210512_ADAdminGroups.csv')
df2 = df.Members.str.split(',').apply(pd.Series)
df2.index = df.set_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged']).index

def chunks(series, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(series), n):
        yield series[i:i + n]

chunk = chunks(df2, 1000)
batch1 = next(chunk)
batch2 = next(chunk)
'''
batch3 = next(chunk)
batch4 = next(chunk)
batch5 = next(chunk)
batch6 = next(chunk)
batch7 = next(chunk)
batch8 = next(chunk)
batch9 = next(chunk)
batch10 = next(chunk)
'''

df3 = batch1.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
df4 = batch2.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
'''
df5 = batch3.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
df6 = batch4.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
df7 = batch5.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
df8 = batch6.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
df9 = batch7.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
df10 = batch8.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
df11 = batch9.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
df12 = batch10.stack().reset_index(['SamAccountName', 'DistinguishedName','Description','WhenCreated','WhenChanged'])
'''
#for admins
final_df = pd.concat([df3,df4])

#for standard
#final_df = pd.concat([df3,df4,df5,df6,df7,df8,df9,df10,df11,df12])

final_df.to_csv('C:\\Users\\ajkim\\Downloads\\SingleAdminUser_ADGroup.csv')
