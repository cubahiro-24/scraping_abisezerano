import json
import requests
from bs4 import BeautifulSoup
import time
import random
import os

BASE_URL = "https://abisezerano.com"
OUTPUT_FILE = "articles.json"
ERROR_LOG = "errors.log"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

session = requests.Session()

def retry_request(url, retries=3, delay=2, backoff=2):
    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"⚠️ Retry {attempt+1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= backoff
            else:
                with open(ERROR_LOG, "a") as log_file:
                    log_file.write(f"{url} - {e}\n")
    return None

def fetch_article_content(url):
    print(f"   ↳ Fetching article: {url}")
    response = retry_request(url)
    if not response:
        return "[Error fetching content]"
    
    soup = BeautifulSoup(response.content, "html.parser")
    content_div = soup.find("div", class_="entry-content")
    if content_div:
        paragraphs = content_div.find_all("p")
        content_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return content_text
    else:
        return "[No content found]"

def fetch_titles_and_contents(page_num):
    url = f"{BASE_URL}/page/{page_num}/"
    print(f"\n📄 Scraping page {page_num}: {url}")
    response = retry_request(url)
    if not response:
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    results = []
    for h1_tag in soup.select("h1.entry-title"):
        a_tag = h1_tag.find("a")
        if a_tag:
            title = a_tag.get_text(strip=True)
            link = a_tag.get("href")
            content = fetch_article_content(link)
            results.append({
                "title": title,
                "link": link,
                "content": content
            })
            time.sleep(random.uniform(1, 2.5))  # respectful pause
    return results

def load_existing_articles():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def main():
    all_articles = load_existing_articles()
    page = (len(all_articles) // 10) + 1  # resume from last checkpoint

    while True:
        articles = fetch_titles_and_contents(page)
        if not articles:
            print(f"🚫 No more articles found at page {page}. Stopping.")
            break
        all_articles.extend(articles)

        # Save after each page
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=4)
        print(f"💾 Saved {len(all_articles)} articles so far.")

        page += 1
        time.sleep(random.uniform(1, 2.5))

    print(f"\n✅ Finished scraping. Total articles: {len(all_articles)}")
    print(f"📝 Articles saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
