import json
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://abisezerano.com"
MAX_PAGES = 2

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def fetch_article_content(url):
    try:
        print(f"   ↳ Fetching article: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        content_div = soup.find("div", class_="entry-content")
        if content_div:
            paragraphs = content_div.find_all("p")
            content_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            return content_text
        else:
            return "[No content found]"
    except Exception as e:
        print(f"   ❌ Error fetching article content: {e}")
        return "[Error fetching content]"

def fetch_titles_and_contents(page_num):
    url = f"{BASE_URL}/page/{page_num}/"
    try:
        print(f"\n📄 Scraping page {page_num}: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
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
                time.sleep(1)  # polite pause between articles

        return results
    except Exception as e:
        print(f"❌ Error scraping page {page_num}: {e}")
        return []

def main():
    all_articles = []
    for page in range(1, MAX_PAGES + 1):
        articles = fetch_titles_and_contents(page)
        all_articles.extend(articles)
        time.sleep(1)  # polite pause between pages

    if not all_articles:
        print("⚠️ No articles found.")
        return

    print(f"\n✅ Total articles collected: {len(all_articles)}")

    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print("📝 Articles saved to articles.json")

if __name__ == "__main__":
    main()
