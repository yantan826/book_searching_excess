import cloudscraper
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re

from matplotlib.pylab import f
from read_csv_goodread import get_to_read_titles
import time
import random
import concurrent.futures

titles_and_authors = get_to_read_titles('data/goodreads_library_export.csv')
random.shuffle(titles_and_authors)

def format_search_query(query):
    # Limit to 10 words
    query = ' '.join(query.split()[:10])
    # Convert to lowercase
    query = query.lower()
    # Remove non-alphanumeric characters and replace spaces with hyphens
    query = re.sub(r'[^a-z0-9\s-]', '', query)
    query = re.sub(r'[\s-]+', '%20', query)
    return query

def search_books(search_term):
    search_query = format_search_query(search_term)
    url = f"https://www.popularonline.com.my/default/catalogsearch/result/index/?q={search_query}&mode=grid&category_id=5897&language_code=&searchby=&customer_review=&fprice=&tprice=&order=&dir=&stock=&did="
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # save the original HTML to a file
    with open('popularonline.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    books = []

    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for item in soup.find_all('div', class_='product--item'):
        title = item.find('a', class_='product-image').get('title')
        link = item.find('a', class_='product-image').get('href')
        
        author_tag = item.find('a', class_='blue')
        author = author_tag.text.strip() if author_tag else 'Unknown author'
        
        price_box = item.find('div', class_='price-box')
        usual_price = price_box.find('span', class_='regular-price').find('span', class_='price').text.strip()
        now_price = price_box.find('p', class_='member-price').find('span', 'price').text.replace('RM', '').replace('\n','').strip()
        member_price = price_box.find_all('p', class_='member-price')[1].find('span', 'price').text.replace('RM', '').replace('\n','').strip()

        books.append({
            'title': title,
            'link': link,
            'author': author,
            'usual_price': usual_price,
            'now_price': now_price,
            'member_price': member_price,
            'extracted_at': current_datetime,
            'search_term': search_term
        })

    if books:
        # Save the results to a CSV file
        with open('data/books.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=books[0].keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(books[:20])  # Limit to 20 books
        print(f"Books saved to books.csv for search term: {search_term}")
    else:
        print(f"No books found for search term: {search_term}")
            
    print(f"Search completed for: {search_term} with {len(books)} results") 

def main():
    for i in range(0, len(titles_and_authors), 10):
        batch = titles_and_authors[i:i+10]
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(search_books, title) for title, author in batch]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()