from scholarly import scholarly
import yaml

scholar_id = "s4mUv1AAAAAJ"
author = scholarly.search_author_id(scholar_id)
author = scholarly.fill(author, sections=["publications"])

pubs = []
for p in author["publications"]:
    pubs.append({
        "title": p["bib"]["title"],
        "authors": p["bib"].get("author", ""),
        "year": p["bib"].get("pub_year", ""),
        "venue": p["bib"].get("venue", ""),
        "url": p.get("pub_url", ""),
    })

with open("_data/publications.yml", "w") as f:
    yaml.dump(pubs, f, allow_unicode=True)