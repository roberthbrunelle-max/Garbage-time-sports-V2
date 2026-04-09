import os
import re
import json
import random
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# ----------------- CONFIGURATION -----------------
RSS_URL = "http://www.espn.com/espn/rss/news"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_DIR = os.path.join(PROJECT_ROOT, "articles")
INDEX_PATH = os.path.join(PROJECT_ROOT, "index.html")
ARTICLES_PAGE_PATH = os.path.join(PROJECT_ROOT, "articles.html")

# Find a valid template. We will use whatever HTML file is in articles/
def get_template_path():
    files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f != "index.html"]
    if not files:
        raise Exception("No template HTML file found in articles/")
    return os.path.join(ARTICLES_DIR, files[0])

SYSTEM_PROMPT = """You are an edgy, stat-focused sports writer for 'Garbage Time Sports'.
Write a bold, analytical, yet casual sports article based on the provided news context.
Return ONLY valid JSON with no markdown wrapping. The JSON must exactly match these keys:
{
  "headline": "catchy and bold title",
  "preview": "2-3 sentence summary",
  "body": "The full article in HTML formatting. Use <p>, <h3>, <blockquote>, etc. Include stats! At least 200 words.",
  "category": "one of [nfl, nba, cfb, mlb, nhl, opinion, analytics]",
  "author": "Make up cool sports writer name",
  "emoji": "A single emoji representing the article's theme"
}
"""

GRADIENTS = [
    "linear-gradient(135deg, #1a0d00, #3d2400)",
    "linear-gradient(135deg, #1a0a0a, #3c0a0a)",
    "linear-gradient(135deg, #1a1a2e, #0f3460)",
    "linear-gradient(135deg, #0a1a0a, #0a2e0a)",
    "linear-gradient(135deg, #00101a, #001a30)",
    "linear-gradient(135deg, #1a1a00, #2e2e00)"
]

def clean_json(text):
    text = text.strip()
    if text.startswith("```json"):
        text = "\n".join(text.split("\n")[1:-1])
    elif text.startswith("```"):
        text = "\n".join(text.split("\n")[1:-1])
    return json.loads(text)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def fetch_top_news():
    print("Fetching top news from ESPN RSS...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(RSS_URL, headers=headers)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    items = root.findall(".//item")
    news_list = []
    
    seen = set()
    for item in items:
        if len(news_list) >= 10:
            break
        title = item.find("title").text if item.find("title") is not None else ""
        desc = item.find("description").text if item.find("description") is not None else ""
        if title and title not in seen:
            seen.add(title)
            news_list.append({"title": title, "desc": desc})
    return news_list

def generate_article_content(news, client):
    prompt = f"Title: {news['title']}\nSummary: {news['desc']}\n\nWrite the article!"
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=[prompt],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
        )
    )
    return clean_json(response.text)

def create_article_html(article_data, date_str, slug, gradient, template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    if soup.title:
        soup.title.string = f"{article_data['headline']} — Garbage Time Sports"
    
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        meta_desc['content'] = article_data['preview']

    cat_tag = soup.find('span', class_=re.compile(r'tag \w+'))
    if cat_tag:
        cat_tag['class'] = f"tag {article_data['category']}"
        cat_tag.string = article_data['category'].upper()

    headline = soup.find('h1', class_='article-headline')
    if headline:
        headline.string = article_data['headline']

    author_name = soup.find('div', class_='byline-name')
    if author_name:
        author_name.string = article_data['author']

    byline_meta = soup.find('div', class_='byline-meta')
    if byline_meta:
        read_time = f"{random.randint(3, 8)} min read"
        byline_meta.string = f"{date_str} · {read_time} · {article_data['category'].upper()}"

    hero_img = soup.find('div', class_='article-hero-img-placeholder')
    if hero_img:
        hero_img['style'] = f"background:{gradient};"
        hero_img.string = article_data['emoji']

    body = soup.find('div', class_='article-body')
    if body:
        body.clear()
        body_html = BeautifulSoup(article_data['body'], 'html.parser')
        body.append(body_html)

    filepath = os.path.join(ARTICLES_DIR, f"{slug}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    return filepath

def update_articles_page(new_articles):
    with open(ARTICLES_PAGE_PATH, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    grid = soup.find('div', class_='articles-grid', id='articleGrid')
    if not grid:
        return

    for article in reversed(new_articles):
        card_html = f"""
        <article class="article-card fade-in" data-category="{article['category']}" data-title="{article['slug'].replace('-', ' ')} {article['headline'].lower()}">
          <a href="articles/{article['slug']}.html">
            <div class="card-img">
              <div class="card-img-placeholder" style="background:{article['gradient']};">{article['emoji']}</div>
            </div>
          </a>
          <div class="card-body">
            <div class="card-tag-row"><span class="tag {article['category']}">{article['category'].upper()}</span></div>
            <a href="articles/{article['slug']}.html"><h3 class="card-title">{article['headline']}</h3></a>
            <p class="card-preview">{article['preview']}</p>
            <div class="card-footer">
              <span class="card-author">{article['author']}</span>
              <span class="card-date">{article['date_str']}</span>
            </div>
          </div>
        </article>
        """
        new_card = BeautifulSoup(card_html, 'html.parser').article
        grid.insert(0, new_card)
        grid.insert(1, "\n        ")

    with open(ARTICLES_PAGE_PATH, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def update_index_page(new_articles):
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    ticker = soup.find('div', class_='ticker-track')
    if ticker:
        for article in reversed(new_articles[:5]):
            span = soup.new_tag('span')
            span.string = article['headline']
            ticker.insert(0, span)

    hero = soup.find('section', class_='hero')
    if hero and new_articles:
        top_art = new_articles[0]
        hero_tag = hero.find('span', class_='hero-tag')
        if hero_tag:
            hero_tag['class'] = f"tag {top_art['category']} hero-tag"
            hero_tag.string = top_art['category'].upper()
        
        hero_label = hero.find('span', class_='hero-label')
        if hero_label:
            hero_label.string = f"Feature Story · {top_art['date_str']}"

        hero_headline = hero.find('h1', class_='hero-headline')
        if hero_headline:
            hero_headline.string = top_art['headline']

        hero_desc = hero.find('p', class_='hero-description')
        if hero_desc:
            hero_desc.string = top_art['preview']

        hero_meta = hero.find('div', class_='hero-meta')
        if hero_meta:
            spans = hero_meta.find_all('span')
            if len(spans) >= 3:
                spans[0].string = f"by {top_art['author']}"
        
        hero_btn = hero.find('a', class_='btn-primary')
        if hero_btn:
            hero_btn['href'] = f"articles/{top_art['slug']}.html"

    featured_grid = soup.find('div', class_='featured-grid')
    if featured_grid:
        for article in reversed(new_articles[:3]):
            card_html = f"""
            <article class="article-card fade-in">
              <a href="articles/{article['slug']}.html">
                <div class="card-img">
                  <div class="card-img-placeholder" style="background:{article['gradient']}">{article['emoji']}</div>
                </div>
              </a>
              <div class="card-body">
                <div class="card-tag-row"><span class="tag {article['category']}">{article['category'].upper()}</span></div>
                <a href="articles/{article['slug']}.html"><h3 class="card-title">{article['headline']}</h3></a>
                <p class="card-preview">{article['preview']}</p>
                <div class="card-footer">
                  <span class="card-author">{article['author']}</span>
                  <span class="card-date">{article['date_str']}</span>
                </div>
              </div>
            </article>
            """
            new_card = BeautifulSoup(card_html, 'html.parser').article
            featured_grid.insert(0, new_card)
    
    latest_list = soup.find('div', class_='latest-list')
    if latest_list:
        for article in reversed(new_articles[3:7]):
            latest_html = f"""
            <a href="articles/{article['slug']}.html" style="text-decoration:none;">
              <div class="latest-item fade-in">
                <div class="latest-item-img"><div class="latest-item-img-placeholder" style="background:{article['gradient']};">{article['emoji']}</div></div>
                <div class="latest-info">
                  <div class="card-tag-row"><span class="tag {article['category']}">{article['category'].upper()}</span></div>
                  <div class="latest-title">{article['headline']}</div>
                  <div class="latest-meta">{article['author']} · {article['date_str']} · 5 min</div>
                </div>
              </div>
            </a>
            """
            new_item = BeautifulSoup(latest_html, 'html.parser').a
            latest_list.insert(0, new_item)

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in env.")
        return

    try:
        template_path = get_template_path()
        print(f"Using template: {template_path}")
    except Exception as e:
        print(f"Error: {e}")
        return

    client = genai.Client(api_key=api_key)
    date_str = datetime.now().strftime("%b %-d, %Y")

    news_list = fetch_top_news()
    print(f"Found {len(news_list)} news items.")

    new_articles = []
    
    for i, news in enumerate(news_list):
        print(f"Generating article {i+1}/10: {news['title']}")
        try:
            article_data = generate_article_content(news, client)
            slug = slugify(article_data['headline'])[:50]
            if slug.endswith('-'):
                slug = slug[:-1]
            gradient = random.choice(GRADIENTS)

            create_article_html(article_data, date_str, slug, gradient, template_path)
            
            article_data['slug'] = slug
            article_data['date_str'] = date_str
            article_data['gradient'] = gradient
            new_articles.append(article_data)
        except Exception as e:
            print(f"Failed to generate article: {e}")

    print("Updating pages...")
    update_articles_page(new_articles)
    update_index_page(new_articles)
    print("Done!")

if __name__ == "__main__":
    main()
