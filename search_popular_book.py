# https://www.popularonline.com.my/default/catalogsearch/result/index/?q=%20Hidden%20Potential&mode=grid&category_id=5897&language_code=&searchby=&customer_review=&fprice=&tprice=&order=&dir=&stock=1&did=5897

import cloudscraper

url = 'https://www.popularonline.com.my/default/catalogsearch/result/index/?q=%20Hidden%20Potential&mode=grid&category_id=5897&language_code=&searchby=&customer_review=&fprice=&tprice=&order=&dir=&stock=1&did=5897'

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

scraper.headers.update({
    'referer': 'https://www.popularonline.com.my/',
    'accept': 'application/json'
})

response = scraper.get(url)

print(response.status_code)
print(response.text)  # Print the response content