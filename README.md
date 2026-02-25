# GitHub Pages Website with Jekyll

This guide walks through creating a GitHub Pages website powered by Jekyll and running it locally so changes can be previewed before publishing.

---

# Step 1 — Create the GitHub Repository
1. Go to GitHub → **New Repository**
2. Name it:
   - `username.github.io`
3. Set it to **Public**
4. Click **Create Repository**

---

# Step 2 — Install Local Dependencies

Jekyll is Ruby-based. You need:

- Ruby
- Bundler
- Jekyll
- GitHub Pages gem (recommended for compatibility)

---

# Step 3 — Create a New Jekyll Site Locally

Open a terminal and run:

```bash
jekyll new username
cd username
```

---

# Step 4 — Choose a Jekyll Setup Strategy

Find a Jekyll theme repository (https://github.com/pages-themes/) and follow the directions, specifically about modifying the `_config.yml` in your repository.


# Step 8 — Configure for Deployment

Edit ```_config.yml```.
 
 ``` YAML
url: "https://username.github.io"
baseurl: ""
```

This ensures links and assets resolve properly.

# Step 9 — Push to GitHub
Initialize Git

```bash
git init
git add .
git commit -m "Initial Jekyll site"
```

```bash
Add Remote and Push
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

# Step 10 — Enable GitHub Pages

In your GitHub repository:

1. Go to Settings
2. Click Pages
3. Under Build and deployment
* Source: Deploy from a branch
* Branch: main
* Folder: /

GitHub will display the published site URL once deployed!


# Step 5 — Make It GitHub Pages Compatible

GitHub Pages runs specific gem versions. To match them locally:

## 5.1 Edit the Gemfile

In file named `Gemfile` replace the contents with:

```ruby
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins
```

## 5.2 Install Dependencies
In your terminal:

```bash
bundle install
```

# Step 6 — Launch the Site Locally

Start the local server:

```bash
bundle exec jekyll serve
```

Then open:

```bash
http://127.0.0.1:4000
```

## Useful Options

Auto rebuild + live reload:

```bash
bundle exec jekyll serve --livereload
```

Serve drafts:

```bash
bundle exec jekyll serve --drafts
```

Stop server with:

```bash
Ctrl + C
```

# Step 7 — Jekyll Structure

Common files and folders:

```_config.yml        # Site configuration
_layouts/          # Page templates
_includes/         # Reusable components
_posts/            # Blog posts
assets/            # CSS, images, JS
index.md           # Homepage
```

