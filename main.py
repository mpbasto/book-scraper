from requests import get
from bs4 import BeautifulSoup

url = 'https://blackwells.co.uk/bookshop/collection/Trending/-186140'
response = get(url)
soup = BeautifulSoup(response.text, 'html.parser')



trending_cat = soup.find('div', class_= 'search-result')
trending_list = trending_cat.find('ul', class_='search-result__list')
items = trending_list.find_all('a', itemprop='url')

# Grab titles of the books
book_titles = []

for link in items:  
    for title in link.contents:
        book_titles.append(title)

print(book_titles)



