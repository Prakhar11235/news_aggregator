from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import random

# Dictionary of categories and their URLs
categories = {
    "Business": "https://www.bbc.com/business",
    "Innovation": "https://www.bbc.com/innovation",
    "Culture": "https://www.bbc.com/culture",
    "Arts": "https://www.bbc.com/arts",
    "Travel": "https://www.bbc.com/travel",
}

# Set up Selenium options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# List to store scraped data
scraped_news = []

try:
    # Function to scrape articles from a given category
    def scrape_category(category_name, category_url):
        driver.get(category_url)
        time.sleep(5)  # Wait for the page to load

        article_links = []
        try:
            # Wait until links appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@data-testid="internal-link"]'))
            )

            a_elements = driver.find_elements(By.XPATH, '//a[@data-testid="internal-link"]')
            for a in a_elements:
                link = a.get_attribute("href")
                if link and link not in article_links:
                    article_links.append(link)
                if len(article_links) >= 20:  # Limit to 20 articles per category
                    break

        except Exception as e:
            print(f"Error finding articles in {category_name}: {e}")
            return

        print(f"Found {len(article_links)} articles in {category_name}.")

        # Visit each article and scrape data
        for index, article_url in enumerate(article_links):
            print(f"Scraping {category_name} article {index + 1}/{len(article_links)}: {article_url}")

            try:
                driver.get(article_url)
                time.sleep(random.uniform(5, 8))  # Random delay to avoid detection

                soup = BeautifulSoup(driver.page_source, "html.parser")

                headline = soup.find("h1").text.strip() if soup.find("h1") else "N/A"
                author = soup.find("span", class_="sc-b42e7a8f-7").text.strip() if soup.find("span", class_="sc-b42e7a8f-7") else "N/A"
                published_date = soup.find("time").text.strip() if soup.find("time") else "N/A"
                summary = soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else "N/A"
                content = " ".join([p.text.strip() for p in soup.find_all("p")])
                image_url = soup.find("img")["src"] if soup.find("img") else "N/A"

                # Include category field in the JSON data
                scraped_news.append({
                    "category": category_name,
                    "headline": headline,
                    "author": author,
                    "published_date": published_date,
                    "summary": summary,
                    "content": content,
                    "image_url": image_url,
                    "source_link": article_url
                })

            except Exception as e:
                print(f"Error scraping {article_url}: {e}")
                continue

    # Scrape all categories
    for category, url in categories.items():
        scrape_category(category, url)

finally:
    # Ensure browser closes properly
    driver.quit()

# Save data to JSON file with category field included
with open("scraped_news.json", "w", encoding="utf-8") as f:
    json.dump(scraped_news, f, ensure_ascii=False, indent=4)

print("Scraping complete! Data saved in scraped_news.json.")
