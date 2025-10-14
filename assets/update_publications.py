from scholarly import scholarly
import yaml
import time

# === CONFIGURATION ===
SCHOLAR_ID = "s4mUv1AAAAAJ"   # Replace with your Google Scholar ID
YOUR_NAME = "E. Schwarz"        # Used to bold your name later if desired
OUTPUT_FILE = "_data/publications.yml"
SLEEP_BETWEEN_REQUESTS = 1     # seconds between requests (to avoid throttling)

# === FETCH AUTHOR DATA ===
print(f"Fetching publications for Scholar ID: {SCHOLAR_ID} ...")
author = scholarly.search_author_id(SCHOLAR_ID)
author = scholarly.fill(author, sections=["publications"])

pubs = []

for i, pub in enumerate(author["publications"], 1):
    try:
        # Get full details for each publication
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

# === SORT ===
def sort_year(entry):
    y = entry.get("year", "")
    return int(y) if str(y).isdigit() else 0

pubs = sorted(pubs, key=sort_year, reverse=True)

# === CLEAN ===
pubs = [p for p in pubs if p["title"]]

# === WRITE CLEAN YAML ===
# This formatting block makes it very readable for direct copy/paste
yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str
def str_presenter(dumper, data):
    """Keep long strings in quotes"""
    if len(data) > 60 or ":" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.org_represent_str(data)
yaml.add_representer(str, str_presenter, Dumper=yaml.SafeDumper)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.dump(pubs, f, allow_unicode=True, sort_keys=False, width=100)

print(f"\n✅ Saved {len(pubs)} publications to {OUTPUT_FILE}")
