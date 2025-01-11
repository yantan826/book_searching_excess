from os import link
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re
from read_csv_goodread import get_to_read_titles
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
    query = re.sub(r'[\s-]+', '+', query)
    return query

def search_books(search_term):
    if len(search_term[0]) < 15:
        search_term = f"{search_term[0]} by {search_term[1]}"
    else:
        search_term = search_term[0]
    search_query = format_search_query(search_term)
    url = f"https://www.bookxcess.com/search?q={search_query}&options%5Bprefix%5D=last"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for item in soup.find_all('div', class_='product_grid'):
        title_tag = item.find('h5')
        title = title_tag.text.strip() if title_tag else 'Unknown title'
        link_tag = item.find('a')
        link_tag = link_tag.get('href') if link_tag else 'No link'
    
        
        price_box = item.find('div', class_='pro_grid_price')
        usual_price_tag = price_box.find('span', class_='bp_compare')
        usual_price = usual_price_tag.text.strip() if usual_price_tag else price_box.text.strip()
        now_price_tag = price_box.find('span', class_='bp_regular')
        now_price = now_price_tag.text.strip() if now_price_tag else 'No discounted price'

        books.append({
            'title': title,
            'link': link_tag,
            'usual_price': usual_price,
            'now_price': now_price,
            'extracted_at': current_datetime,
            'search_term': search_term
        })

    if books:
        # Save the results to a CSV file
        with open('data/books_excess.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=books[0].keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(books[:20])  # Limit to 20 books
        print(f"Books saved to books.csv for search term: {search_term}")
    else:
        print(f"No books found for search term: {search_term}")
            
    print(f"Search completed for: {search_term} with {len(books)} results")

def main():
    for i in range(0, len(titles_and_authors), 5):
        batch = titles_and_authors[i:i+5]
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(search_books, title_author) for title_author in batch]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

