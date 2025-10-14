from scholarly import scholarly
import time
from datetime import datetime
import re

# === CONFIGURATION ===
SCHOLAR_ID = "s4mUv1AAAAAJ"   # Replace with your Google Scholar ID
YOUR_NAME = "Schwarz"       # Will be bolded in authors
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

def format_authors(authors_str, your_name="Schwab"):
    """
    Converts a raw author string into:
    Initials LastName, Initials LastName, ..., & LastAuthor
    Bold your name if present.
    """
    if not authors_str:
        return ""
    
    # Split by ' and ' or ',' (Google Scholar style)
    import re
    names = re.split(r'\s+and\s+|,', authors_str)
    names = [n.strip() for n in names if n.strip()]
    
    formatted_authors = []
    for name in names:
        parts = name.split()
        if not parts:
            continue
        last = parts[-1]
        initials = " ".join([p[0] + "." for p in parts[:-1]]) if len(parts) > 1 else ""
        formatted = f"{last}, {initials}".strip() if initials else last
        
        # Bold your name if it matches (match on last name + initials)
        if your_name and your_name.lower() in name.lower():
            formatted = f"**{formatted}**"
        
        formatted_authors.append(formatted)
    
    # APA-style: add & before the last author if more than one
    if len(formatted_authors) > 1:
        return ", ".join(formatted_authors[:-1]) + ", & " + formatted_authors[-1]
    else:
        return formatted_authors[0]


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
