import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://abisezerano.com"

def get_article_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for a in soup.find_all('a', href=True):
        if '/202' in a['href']:  # Basic filter for articles with year in URL
            link = a['href']
            if not link.startswith("http"):
                link = BASE_URL + link
            if link not in links:
                links.append(link)
    return links

def scrape_articles():
    links = get_article_links()
    os.makedirs("articles", exist_ok=True)

    for i, url in enumerate(links):
        print(f"Scraping {url}")
        try:
            r = requests.get(url)
            s = BeautifulSoup(r.content, "html.parser")
            title = s.find("h1").text.strip()
            body = s.find("div", class_="entry-content").text.strip()

            with open(f"articles/article_{i+1}.txt", "w", encoding="utf-8") as f:
                f.write(f"Title: {title}\n\n{body}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    scrape_articles()
