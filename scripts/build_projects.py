"""Generate the six case-study pages.

Each one is the project's own Figma page, exported as a single tall render,
with the site's chrome around it: a back link, and a link on to the next
project — except the last, which only goes back.
"""
import html
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")

# Order follows the storyboard.
PROJECTS = [
    dict(slug="gas-station", nav="Gas station", title="Redesigning the future of CNG gas stations",
         meta="Service design | Rebranding", year="2024", h=3015,
         alt="Case study: rebranding the Indraprastha Gas station experience"),
    dict(slug="aviation", nav="Aviation", title="Reimagining aviation safety",
         meta="Experience design | Space design", year="2024", h=1926,
         alt="Case study: an immersive safety walkthrough for Air India's training centre"),
    dict(slug="healthcare", nav="Healthcare", title="Reimagining care using the natural environment",
         meta="Space design | System design", year="2025", h=3575,
         alt="Case study: a nature-inspired toolkit for NHS GP waiting rooms"),
    dict(slug="agri-tech", nav="Agri-Tech", title="Earth observation data for food systems",
         meta="Service design | UI UX design", year="2026", h=3575,
         alt="Case study: Grove, a service turning Earth Observation data into growing advice"),
    dict(slug="retrofit", nav="Retrofit", title="Rebuilding trust in retrofit",
         meta="Service design", year="2026", h=2669,
         alt="Case study: Synergy Days, a conversation-led route into home retrofit"),
    dict(slug="tourism", nav="Tourism", title="Tackling the challenges of tourism",
         meta="System design | UI design", year="2023", h=3126,
         alt="Case study: an integrated waste, wayfinding and artisan platform for Rajasthan"),
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Nishita Gupta</title>
<meta name="description" content="{meta}, {year}. {title}.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏄</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Caveat:wght@600&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body class="case">
<div class="cursor" id="cursor" aria-hidden="true"></div>

<header class="nav">
  <a class="nav-name" href="index.html">Nishita Gupta</a>
  <nav>
    <a href="index.html#projects-list">Projects</a>
    <a href="index.html#contact">Contact</a>
    <a href="cv.html">CV</a>
  </nav>
</header>

<main class="case-body">
  <a class="back" href="index.html#projects-list">Back to the work</a>

  <!-- The sheet carries the project's own title, so ours is for screen
       readers and search results only. -->
  <h1 class="sr-only">{title}</h1>
  <p class="case-meta">{meta} · {year}</p>

  <img class="case-sheet" src="cases/{slug}.webp" alt="{alt}"
       width="1160" height="{h}" decoding="async">

  <nav class="case-next">
{next_links}
  </nav>
</main>
<script type="module" src="cursor.js"></script>
</body>
</html>
"""

for i, p in enumerate(PROJECTS):
    last = i == len(PROJECTS) - 1
    if last:
        links = '    <a class="btn" href="index.html#projects-list">Back</a>'
    else:
        nxt = PROJECTS[i + 1]
        links = (f'    <a class="btn" href="{nxt["slug"]}.html">Next: {html.escape(nxt["nav"])}</a>\n'
                 '    <a class="btn btn-ghost" href="index.html#contact">Get in touch</a>')
    page = PAGE.format(
        title=html.escape(p["title"]), meta=html.escape(p["meta"]), year=p["year"],
        slug=p["slug"], alt=html.escape(p["alt"]), h=p["h"], next_links=links,
    )
    open(os.path.join(OUT, f"{p['slug']}.html"), "w").write(page)
    print("wrote", p["slug"] + ".html")
