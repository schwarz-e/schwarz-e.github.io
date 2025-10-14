from scholarly import scholarly
import time
from datetime import datetime

# === CONFIGURATION ===
SCHOLAR_ID = "s4mUv1AAAAAJ"   # Replace with your Google Scholar ID
YOUR_NAME = "E. Schwarz"       # Will be bolded in authors
OUTPUT_FILE = "../publications.md"
SLEEP_BETWEEN_REQUESTS = 0.1

# === FETCH AUTHOR DATA ===
print(f"Fetching publications for Scholar ID: {SCHOLAR_ID} ...")
author = scholarly.search_author_id(SCHOLAR_ID)
author = scholarly.fill(author, sections=["publications"])

pubs = []

for i, pub in enumerate(author["publications"], 1):
    try:
        pub_filled = scholarly.fill(pub)
        bib = pub_filled.get("bib", {})

        pubs.append({
            "title": bib.get("title", "").strip(),
            "authors": bib.get("author", "").strip(),
            "year": bib.get("pub_year", ""),
            "venue": bib.get("venue", bib.get("journal", "")).strip(),
            "url": pub_filled.get("pub_url", "").strip(),
        })
        print(f"✓ {i}. {bib.get('title', '')[:60]}")
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    except Exception as e:
        print(f"⚠️ Skipping one entry due to error: {e}")

# === CLEAN AND SORT ===
pubs = [p for p in pubs if p["title"]]
pubs.sort(key=lambda x: int(x["year"]) if str(x["year"]).isdigit() else 0, reverse=True)

# === GENERATE MARKDOWN ===
def bold_name(authors, name):
    if not authors:
        return ""
    return authors.replace(name, f"**{name}**")

header = f"""---
layout: default
title: Publications
---

# Publications

> 📚 Automatically generated from Google Scholar
> Last updated: {datetime.now().strftime("%B %d, %Y")}

"""

md_lines = [header]

for pub in pubs:
    title = pub["title"]
    authors = bold_name(pub["authors"], YOUR_NAME)
    year = pub["year"] or "n.d."
    venue = pub["venue"]
    url = pub["url"]

    entry = f"- **{title}**  \n  {authors} ({year})"
    if venue:
        entry += f"  \n  *{venue}*"
    if url:
        entry += f"  \n  [Link]({url})"
    md_lines.append(entry + "\n")

# === WRITE FILE ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"\n✅ Markdown file written to {OUTPUT_FILE}")
