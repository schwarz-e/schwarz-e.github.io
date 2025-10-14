from scholarly import scholarly
import time
from datetime import datetime
import re

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

def format_authors(authors_str, your_name="E. Schwab"):
    """
    Converts a raw author string from Google Scholar into:
    Initials LastName, Initials LastName, ...
    Bold your name if present.
    """
    if not authors_str:
        return ""
    
    authors = []
    for name in authors_str.split(","):
        name = name.strip()
        if not name:
            continue
        
        # Split into parts
        parts = name.split()
        last = parts[-1]  # last word is last name
        initials = " ".join([p[0] + "." for p in parts[:-1]]) if len(parts) > 1 else ""
        formatted = f"{initials} {last}".strip()
        
        # Bold your name
        if your_name and your_name in name:
            formatted = f"**{formatted}**"
        
        authors.append(formatted)
    
    return ", ".join(authors)


def title_case(title):
    """
    Converts a string to title case, ignoring small words like 'and', 'of', 'in', etc.
    """
    if not title:
        return ""
    
    small_words = {'and', 'or', 'the', 'of', 'in', 'on', 'for', 'a', 'an', 'with', 'to', 'by'}
    words = title.split()
    title_cased = [words[0].capitalize()]  # always capitalize first word
    
    for w in words[1:]:
        title_cased.append(w.capitalize() if w.lower() not in small_words else w.lower())
    
    return " ".join(title_cased)

header = f"""---
layout: default
title: Publications
---

# Publications

### Selected Works
> 📚 Automatically generated from Google Scholar
> Last updated: {datetime.now().strftime("%B %d, %Y")}

"""

md_lines = [header]

for pub in pubs:
    title = title_case(pub["title"])
    authors = format_authors(pub["authors"], YOUR_NAME)
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
