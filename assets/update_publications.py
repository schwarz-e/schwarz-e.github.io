from scholarly import scholarly
import yaml
import time

scholar_id = "s4mUv1AAAAAJ"
author = scholarly.search_author_id(scholar_id)
author = scholarly.fill(author, sections=["publications"])

pubs = []
for p in author["publications"]:
    # Fill each publication to get full metadata
    pub_filled = scholarly.fill(p)
    bib = pub_filled.get("bib", {})
    
    pubs.append({
        "title": bib.get("title", ""),
        "authors": bib.get("author", ""),   # now populated
        "year": bib.get("pub_year", ""),
        "venue": bib.get("venue", bib.get("journal", "")),
        "url": pub_filled.get("pub_url", ""),
    })
    
    time.sleep(1)  # small delay to avoid Google blocking requests

# Save to YAML
with open("_data/publications.yml", "w", encoding="utf-8") as f:
    yaml.dump(pubs, f, allow_unicode=True, sort_keys=False)

print(f"✅ Saved {len(pubs)} publications to _data/publications.yml")
