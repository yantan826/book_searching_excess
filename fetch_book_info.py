import requests

def fetch_book_info(book_id, api_key):
    url = f"https://www.goodreads.com/book/show/{book_id}.xml?key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        print(response.text)  # Print the XML response
    else:
        print(f"Failed to fetch book info: {response.status_code}")

if __name__ == "__main__":
    book_id = "2657"  # Example book ID for "To Kill a Mockingbird"
    api_key = "YOUR_GOODREADS_API_KEY"  # Replace with your Goodreads API key
    fetch_book_info(book_id, api_key)
