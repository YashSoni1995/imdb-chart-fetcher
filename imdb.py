from bs4 import BeautifulSoup
import requests
import json
import sys

#Checking arguments
if len(sys.argv) != 3: 
    sys.exit("2 arguments required: chart_url and items_count")

items_count = sys.argv[2]
try:
    items = int(items_count)
except ValueError:
    sys.exit("invalid argument items_count, must be an integer") 

#chart_url
url = sys.argv[1]

#Get movie list and associated movie_details page link and store it
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
movie_links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]

imdb = []

# Store each item into dictionary (data), then put those into a list (imdb)
for index in range(0,  items):

    #Extract movie title by removing html tags
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    title = movie[len(str(index))+1:-7]

    #Get movie_details (duration, rating, genre, release_year, summary) from movie details page url
    movieUrl = "https://www.imdb.com/" + movie_links[index]
    movie_response = requests.get(movieUrl)
    movie_details = BeautifulSoup(movie_response.text, 'lxml')
    
    #Extract movie_details by removing html tags
    duration = movie_details.select('div.title_wrapper time')[0].get_text().strip()
    rating = movie_details.select('div.ratingValue span')[0].get_text().strip()
    genre = movie_details.select('div.title_wrapper a')[1].get_text().strip()
    release_year = movie_details.select('div.title_wrapper a')[0].get_text().strip()
    summary = movie_details.select('div.summary_text')[0].get_text().strip()
    
    data = {"title": title,
            "movie_release_year": int(release_year),
            "summary": summary,
            "duration": duration,
            "imdb_rating": float(rating),
            "genre": genre}
    imdb.append(data)    

print(json.dumps(imdb))
