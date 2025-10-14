# Publications

### Selected Works


> 📚 Automatically generated from Google Scholar

{% for pub in site.data.publications %}
- **{{ pub.title }}**  <br>
  {{ pub.authors }} ({{ pub.year }})  <br>
  *{{ pub.venue }}*  <br>
  {% if pub.url %}[Link]({{ pub.url }}){% endif %}  

{% endfor %}


[View all on Google Scholar →](https://scholar.google.com/citations?user=s4mUv1AAAAAJ)
