# 🗑️ Garbage Time Sports

A fully functional dark-themed sports blog website. No frameworks, no build tools. Just HTML, CSS, and vanilla JS — open in VS Code and go.

---

## File Structure

```
GarbageTimeSports/
│
├── index.html           — Homepage (hero, featured grid, latest takes, sidebar)
├── articles.html        — Article listing page with filter buttons + load more
├── article.html         — Article detail TEMPLATE (reuse for every new post)
├── infographics.html    — Infographics gallery page
├── about.html           — About / team / mission page
│
├── css/
│   └── styles.css       — All styles (CSS variables, components, responsive)
│
├── js/
│   └── script.js        — All interactivity (dropdown, filters, animations, etc.)
│
├── images/              — Put all article images here
│   └── (your images)
│
└── articles/            — Put individual article HTML files here (optional)
    └── (your articles)
```

---

## How to Add a New Article

1. **Duplicate `article.html`** and rename it (e.g., `articles/mahomes-greatness.html`)
2. Update the `<title>` and `<meta name="description">` tags at the top
3. Edit the article content inside `<article class="article-main">`:
   - Change the `.tag` category (nfl / nba / cfb / mlb / nhl / opinion / analytics)
   - Update the `<h1 class="article-headline">`
   - Update the `<p class="article-dek">`
   - Update the `.article-byline` with author name, date, read time
   - Replace the hero image placeholder (or add `<img>` tag)
   - Replace the `.article-body` content with your article text
4. **Add the article card to `articles.html`** — copy an existing `<article class="article-card">` block, update the text, and set `data-category="nfl"` (or whichever applies)
5. **Add a card to `index.html`** in the featured grid or latest takes section if it's a featured piece

---

## Content Components Reference

### Tags / Categories
```html
<span class="tag">Default (yellow)</span>
<span class="tag nfl">NFL</span>
<span class="tag nba">NBA</span>
<span class="tag cfb">CFB</span>
<span class="tag nhl">NHL</span>
<span class="tag mlb">MLB</span>
<span class="tag opinion">Opinion</span>
<span class="tag analytics">Analytics</span>
```

### Pull Quote
```html
<div class="pull-quote">
  <p>"Your memorable quote goes here."</p>
</div>
```

### Stat Highlight Block
```html
<div class="stat-highlight">
  <div class="stat-number">42%</div>
  <div class="stat-context">
    <strong>Stat Label Here</strong>
    <p>Short explanation of what this stat means.</p>
  </div>
</div>
```

### Article Card (for articles.html)
```html
<article class="article-card fade-in" data-category="nfl">
  <a href="articles/your-article.html">
    <div class="card-img">
      <img src="images/your-image.jpg" alt="Description" />
    </div>
  </a>
  <div class="card-body">
    <div class="card-tag-row"><span class="tag nfl">NFL</span></div>
    <a href="articles/your-article.html"><h3 class="card-title">Your Title</h3></a>
    <p class="card-preview">Short preview text.</p>
    <div class="card-footer">
      <span class="card-author">Author Name</span>
      <span class="card-date">Jun 14, 2025</span>
    </div>
  </div>
</article>
```

---

## Customization

- **Colors**: Edit CSS variables at top of `css/styles.css` (`:root { ... }`)
- **Accent color**: `--accent: #e8ff00;` — change to any color
- **Fonts**: Edit the Google Fonts import URL in `styles.css`
- **Ticker headlines**: Edit the `<div class="ticker-track">` in `index.html`
- **Hero article**: Update the `.hero` section in `index.html`

---

## Tips

- All images should go in `/images/` folder
- Use `aspect-ratio: 16/9` images for best card display
- The `data-category` attribute on `.article-card` powers the filter buttons on `articles.html`
- Cards marked `data-hidden="true"` are hidden behind the "Load More" button
- The `.fade-in` class on any element will animate it in when scrolled into view

---

## No Setup Required

Open `index.html` directly in a browser — or use VS Code's Live Server extension for hot-reloading during development.

**Recommended VS Code Extensions:**
- Live Server (ritwickdey.LiveServer)
- Prettier - Code formatter
- HTML CSS Support
