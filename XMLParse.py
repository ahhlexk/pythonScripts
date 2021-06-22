import xml.etree.ElementTree as et
import pandas as pd

xtree = et.parse("C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Desktop\\PRD_P_DAX_20201222_142919_1.xml")
xroot = xtree.getroot()
df = pd.DataFrame()


for node in xroot:
    dxno = node.find('DXNO').text
    df2 = pd.DataFrame()
    try:
        for genre in node.find('Dgtl/Genre_Dgtl'):
            genre_text = genre.text
            data = [[dxno, genre_text]]
            df2 = pd.DataFrame(data=data)
            df = df.append(df2,sort=False)
    except:
        data = [[dxno, " "]]
        df2 = pd.DataFrame(data=data)
        df = df.append(df2, sort=False)
        
df.rename(columns={0:'DXNO',1:'GENRE_DGTL'}, inplace=True)
df.to_csv('C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Desktop\\Genre_Dgtl.csv', index=False)
#print(df)


df_theme = pd.DataFrame()

for node in xroot:
    dxno = node.find('DXNO').text
    df2 = pd.DataFrame()
    try:
        for theme in node.find('Dgtl/Theme_Dgtl'):
            theme_text = theme.text
            data = [[dxno, theme_text]]
            df2 = pd.DataFrame(data=data)
            df_theme = df_theme.append(df2,sort=False)
    except:
        data = [[dxno, " "]]
        df2 = pd.DataFrame(data=data)
        df_theme = df_theme.append(df2, sort=False)

df_theme.rename(columns={0:'DXNO',1:'THEME_DGTL'}, inplace=True)
df_theme.to_csv('C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Desktop\\Theme_Dgtl.csv', index=False)
#print(df_theme)

df_tv_genre = pd.DataFrame()

for node in xroot:
    dxno = node.find('DXNO').text
    df2 = pd.DataFrame()
    try:
        for theme in node.find('TV/Genre_TV'):
            theme_text = theme.text
            data = [[dxno, theme_text]]
            df2 = pd.DataFrame(data=data)
            df_tv_genre = df_tv_genre.append(df2,sort=False)
    except:
        data = [[dxno, " "]]
        df2 = pd.DataFrame(data=data)
        df_tv_genre = df_tv_genre.append(df2, sort=False)
    
df_tv_genre.rename(columns={0:'DXNO',1:'GENRE_TV'}, inplace=True)
df_tv_genre.to_csv('C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Desktop\\Genre_TV.csv', index=False)

#print(df_tv_genre)

df_tv_theme = pd.DataFrame()

for node in xroot:
    dxno = node.find('DXNO').text
    df2 = pd.DataFrame()
    try:
        for theme in node.find('TV/Theme_TV'):
            theme_text = theme.text
            data = [[dxno, theme_text]]
            df2 = pd.DataFrame(data=data)
            df_tv_theme = df_tv_theme.append(df2,sort=False)
    except:
        data = [[dxno, " "]]
        df2 = pd.DataFrame(data=data)
        df_tv_theme = df_tv_theme.append(df2, sort=False)
    
df_tv_theme.rename(columns={0:'DXNO',1:'THEME_TV'}, inplace=True)
df_tv_theme.to_csv('C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Desktop\\Theme_TV.csv', index=False)
#print(df_tv_theme)


        
    
    
