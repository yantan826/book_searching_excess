from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from read_csv_goodread import get_to_read_titles
import pandas as pd
import time
import random

titles_and_authors = get_to_read_titles('data/goodreads_library_export.csv')
random.shuffle(titles_and_authors)

def search_book():
    driver = webdriver.Chrome()
    results = []

    try:
        driver.get("https://www.bookxcess.com")
        # waiting for prompt to process any key
        driver.find_element(By.CSS_SELECTOR, ".user_labels").click()
        # <a href="/account/login" class="button">Sign In</a>
        driver.find_element(By.CSS_SELECTOR, ".h_accont_dropdown a.button").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys("tankarhau@gmail.com")
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("K@rhau5433")
        # send key enter
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(Keys.RETURN)
        time.sleep(2)

        for title, author in titles_and_authors:
            search_box = driver.find_element(By.CSS_SELECTOR, "input[name='q']")
            if len(title) < 15:
                title = f"{title} by {author}"
            search_box.send_keys(title)
            time.sleep(2)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
            tab_title = driver.title
            result = tab_title.split(" ")[1]
            if int(result) == 0:
                results.append({"Title": title, "Status": "Not found", "Books Found": ""})
            elif int(result) < 5:
                try:
                    status = driver.find_element(By.CSS_SELECTOR, ".search_main_block .container-fluid li .grid_stock").text
                    results.append({"Title": title, "Status": status, "Books Found": ""})
                    button = driver.find_element(By.CSS_SELECTOR, ".search_main_block .container-fluid li .button")
                    if button.text == "NOTIFY":
                        button.click()
                        time.sleep(2)
                        iframe = driver.find_element(By.ID, "SI_frame")
                        driver.switch_to.frame(iframe)
                        button = driver.find_element(By.CSS_SELECTOR, ".form-group button")
                        button.click()
                        time.sleep(0.4)
                        driver.switch_to.default_content()
                        driver.refresh()
                    time.sleep(1)
                except:
                    status = driver.find_element(By.CSS_SELECTOR, ".search_main_block .container-fluid li button").text
                    if "ADD TO CART" in status:
                        books_found = driver.find_element(By.CSS_SELECTOR, ".search_main_block .container-fluid li h5").text
                        status = "Available"
                    results.append({"Title": title, "Status": status, "Books Found": books_found})
            else:
                results.append({"Title": title, "Status": "Not found", "Books Found": ""})
            search_box = driver.find_element(By.CSS_SELECTOR, "input[name='q']")
            search_box.clear()
            
            # Save result to CSV after each search
            df = pd.DataFrame(results)
            df.to_csv('search_results.csv', mode='a', header=not pd.io.common.file_exists('search_results.csv'), index=False)
            results.clear()
            
    except Exception as e:
        print(f"Failed to search book: {e}")
    finally:
        driver.quit()
        
if __name__ == "__main__":
    search_book()