# Abisezerano Article Scraper

A Python web scraper that extracts article titles, links, and full content from [Abisezerano.com](https://abisezerano.com), automatically navigating through all available pages.

---

## 🚀 Features

- 🔁 Scrapes **all pages** of articles dynamically (no fixed page limit)  
- 📰 Extracts article **title**, **URL**, and **full article content**  
- 🤖 Handles HTTP requests politely with **user-agent** and **time delays**  
- 💾 Saves scraped data as a clean, readable **JSON file**  
- 🛡️ Robust error handling for connection and parsing issues  

---

## ⚙️ How It Works

1. The script starts scraping from **page 1** and continues until no more article pages are found.
2. For each page, it fetches all article **titles** and **links**.
3. It visits each article link to extract the **full content**.
4. All collected data is stored in a list of dictionaries and written to a `JSON` file.

---

## 📄 License

This project is licensed under the **MIT License**.
