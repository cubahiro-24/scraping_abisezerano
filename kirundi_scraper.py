import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time

BASE_URL = "https://abisezerano.com"
MAX_PAGES = 20  # Limit to avoid hitting server too hard
MAX_WORKERS = 5  # Number of concurrent threads

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def fetch_article_links(page_num):
    url = f"{BASE_URL}/page/{page_num}/"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return [a['href'] for a in soup.select('h2.entry-title a')]
    except Exception as e:
        print(f"Error fetching page {page_num}: {e}")
        return []

def scrape_article(url):
    try:
        print(f"Scraping {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("h1", class_="entry-title").text.strip()
        content = soup.find("div", class_="entry-content").text.strip()
        return {"url": url, "title": title, "content": content}
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    all_article_links = []
    for page in range(1, MAX_PAGES + 1):
        print(f"Fetching article links from: {BASE_URL}/page/{page}/")
        links = fetch_article_links(page)
        all_article_links.extend(links)
        time.sleep(1)  # polite delay between pages

    # Scrape all articles concurrently
    print(f"\nScraping {len(all_article_links)} articles...\n")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(scrape_article, all_article_links))

    # Filter out failed scrapes
    articles = [r for r in results if r]
    print(f"\n✅ Successfully scraped {len(articles)} articles")

if __name__ == "__main__":
    main()
