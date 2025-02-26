from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time

# Set up Selenium options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# Get website URL from user
URL = "https://www.bbc.com/"
driver.get(URL)

# Wait for articles to load
time.sleep(5)

# Extract all links with data-testi="internal link"
article_links = []
try:
    # Wait until links with data-testi="internal link" appear
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@data-testid="internal-link"]')))

    a_elements = driver.find_elements(By.XPATH, '//a[@data-testid="internal-link"]')
    for a in a_elements:
        link = a.get_attribute("href")  # Extract link
        if link and link not in article_links:
            article_links.append(link)

except:
    print("No articles found.")
    driver.quit()
    exit()

print(f"Found {len(article_links)} articles.")

# List to store scraped data
scraped_data = []

# Visit each article and scrape data
for index, article_url in enumerate(article_links):
    print(f"Scraping article {index + 1}/{len(article_links)}: {article_url}")

    driver.get(article_url)
    time.sleep(5)  # Wait for page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract article details
    try:
        headline = soup.find("h1").text.strip() if soup.find("h1") else "N/A"
        author = soup.find("span", class_="sc-b42e7a8f-7").text.strip() if soup.find("span", class_="sc-b42e7a8f-7") else "N/A"
        published_date = soup.find("time").text.strip() if soup.find("time") else "N/A"
        summary = soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else "N/A"
        content = " ".join([p.text.strip() for p in soup.find_all("p")])  # Extracts all paragraph text
        image_url = soup.find("img")["src"] if soup.find("img") else "N/A"

        # Store the data
        scraped_data.append({
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

# Close browser
driver.quit()

# Save data to JSON file
with open("scraped_news.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, ensure_ascii=False, indent=4)

print("Scraping complete! Data saved in scraped_news.json.")
