from scholarly import scholarly
import time
from datetime import datetime
import re
import yaml

# === CONFIGURATION ===
SCHOLAR_ID = "s4mUv1AAAAAJ"   # Replace with your Google Scholar ID
YOUR_NAME = "Schwarz"         # Will be bolded in authors
OUTPUT_FILE = "../_data/publications.yml"
SLEEP_BETWEEN_REQUESTS = 0.1

# === FETCH AUTHOR DATA ===
print(f"Fetching publications for Scholar ID: {SCHOLAR_ID} ...")
author = scholarly.search_author_id(SCHOLAR_ID)
author = scholarly.fill(author, sections=["publications"])

pubs = []

def make_id(pub, your_name="Schwarz"):
    small_words = {'and', 'or', 'the', 'of', 'in', 'on', 'for', 'a', 'an', 'with', 'to', 'by'}
    """Generate a unique ID: year + first author's last name + first keyword of title"""
    year = str(pub.get("year") or "n.d.")
    first_author = pub.get("authors", "").split(",")[0].lower().replace(" ", "")
    if your_name.lower() in first_author.lower():
        first_author = your_name.lower()
    # Pick first non-small word from title
    title = pub.get("title", "").strip()
    keyword = ""
    for word in title.split():
        if word.lower() not in small_words:
            keyword = re.sub(r'\W+', '', word.lower())  # remove punctuation
            break
    if not keyword:
        keyword = "title"
    return f"{first_author}{year}{keyword}"

def format_authors(authors_str, your_name="Schwarz"):
    if not authors_str:
        return ""
    # Split by ' and ' or ',' (Google Scholar style)
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
        if your_name.lower() in name.lower():
            formatted = f"<strong>{formatted}</strong>"
        formatted_authors.append(formatted)
    if len(formatted_authors) > 1:
        return ", ".join(formatted_authors[:-1]) + ", & " + formatted_authors[-1]
    else:
        return formatted_authors[0]

def title_case(title):
    if not title:
        return ""
    small_words = {'and', 'or', 'the', 'of', 'in', 'on', 'for', 'a', 'an', 'with', 'to', 'by'}
    words = title.split()
    title_cased = [words[0].capitalize()]  # always capitalize first word
    for w in words[1:]:
        title_cased.append(w.capitalize() if w.lower() not in small_words else w.lower())
    return " ".join(title_cased)

for i, pub in enumerate(author["publications"], 1):
    try:
        pub_filled = scholarly.fill(pub)
        bib = pub_filled.get("bib", {})

        pub_dict = {
            "title": title_case(bib.get("title", "").strip()),
            "authors": format_authors(bib.get("author", "").strip(), YOUR_NAME),
            "year": bib.get("pub_year", ""),
            "journal": bib.get("venue", bib.get("journal", "")).strip(),
            "url": pub_filled.get("pub_url", "").strip(),
        }
        pub_dict["id"] = make_id(pub_dict, YOUR_NAME)

        pubs.append(pub_dict)
        print(f"✓ {i}. {pub_dict['id'][:60]}")
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    except Exception as e:
        print(f"⚠️ Skipping one entry due to error: {e}")

# Sort publications by year descending
pubs = [p for p in pubs if p["title"]]
pubs.sort(key=lambda x: int(x["year"]) if str(x["year"]).isdigit() else 0, reverse=True)

# === WRITE YAML FILE ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.dump(pubs, f, sort_keys=False, allow_unicode=True)

print(f"\n✅ YAML data file written to {OUTPUT_FILE}")
