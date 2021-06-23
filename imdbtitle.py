import requests
from bs4 import BeautifulSoup as bs
import json
import re
import csv

user = 'ajkim'
data = []
exceptions = []

with open('C:\\Users\\'+user+'\\Downloads\\ttcodes.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i in csv_reader:
                try:
                        url = 'http://www.imdb.com/title/'+str(i[0])
                        source_code = requests.get(url)
                        plain_text = source_code.text
                        soup = bs(plain_text, 'html.parser')
                        js = soup.find("script",type="application/ld+json")
                        clean_js = re.sub('<[^<]+?>', '', str(js))
                        final_js = json.loads(clean_js)
                        title = final_js['name']
                        raw_year = soup.find("span", {"id": "titleYear"}).text
                        year = re.sub(r'\(|\)', '', raw_year)
                        mpaa = final_js['contentRating']
                        genre1 = final_js['genre'][0]
                        genre2 = final_js['genre'][1]
                        rating = final_js['aggregateRating']['ratingValue']
                        ratingcount = final_js['aggregateRating']['ratingCount']
                        director = final_js['director']['name']
                        metacriticscore = soup.find('div', {'class': 'metacriticScore'}).text.strip()
                        raw_reviewcount = soup.find_all('span', {'class': 'subText'})[1].text.strip()
                        reviewcount = re.sub(r'\n', '', raw_reviewcount)
                        raw_pop = soup.find_all('span', {'class': 'subText'})[2].text.strip()
                        pop = re.sub(r'\n', '', raw_pop)
                        row = [title, year, mpaa, genre1, genre2, rating, ratingcount, director, metacriticscore, reviewcount, pop]
                        data.append(row)
                except Exception as e:
                        exceptions.append(str(e)+str(i))


file = open('C:\\Users\\'+user+'\\Downloads\\IMDBdata.csv', 'w', newline ='')
headers = ['TITLE', 'YEAR', 'MPAA', 'GENRE1', 'GENRE2', 'RATING', 'RATINGCOUNT', 'DIRECTOR', 'METACRITICSCORE', 'REVIEWCOUNT', 'POP']
with file:
        write = csv.writer(file, delimiter=',')
        write.writerow(i for i in headers)
        write.writerows(data)

file = open('C:\\Users\\'+user+'\\Downloads\\IMDB_Errors.csv', 'w', newline ='')
with file:
        write = csv.writer(file, delimiter=',')
        for i in exceptions:
                data = [str(i)]
                write.writerow(data)
