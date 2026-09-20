"""Generate the six case-study pages.

Copy is lifted verbatim from the Figma file (canvas.fig is zstd-compressed
kiwi; the text runs were read out of it). Layout is this site's, not Figma's —
the frames themselves were never exported.
"""
import html
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")

PROJECTS = [
    dict(
        slug="agri-tech", nav="Agri-Tech", hero="p-agritech",
        title="Application of earth observation data for food systems",
        meta="Service design | UI UX design", year="2026",
        alt="Gardening starter kit with seed packets and a printed grow guide",
        lede="The project explores how Earth Observation data can be made accessible "
             "and actionable to encourage everyday food growing and contribute to a "
             "more resilient food system.",
        sections=[
            ("Understanding the needs of stakeholders", [
                "I conducted structured interviews and open-ended conversations with both "
                "providers and users of Earth Observation data. Open-ended conversations "
                "with farmers, food community groups and researchers helped uncover "
                "experiences, needs and perceptions around using data for food growing.",
                "More structured interviews with industry experts and data-dashboard "
                "engineers helped me understand how EO data is collected, processed, "
                "translated and delivered to users. I then used insight clustering to "
                "group insights from these engagements, identifying recurring patterns, "
                "needs, barriers and opportunities.",
            ], None),
            ("From insights to emerging themes", [
                "I used thematic mapping to connect insights across the stakeholder "
                "ecosystem, uncovering user needs alongside the barriers providers face "
                "in making EO resources accessible and usable.",
            ], None),
            ("From evidence to designing a solution", [
                "Grove — a service ecosystem that helps people take their first step "
                "towards food resilience using Earth Observation data. The service "
                "addresses a key barrier to getting started: feeling overwhelmed by "
                "complex information and not knowing where to begin.",
                "Grove acts as an enabler, translating Earth Observation data into simple, "
                "relevant and actionable growing advice. Through a personalised and "
                "customisable starter kit, users are guided from understanding their local "
                "growing conditions to taking action, making food growing easier to start.",
            ], None),
            ("Building a community", [
                "Grove creates opportunities for growers to connect, share existing "
                "knowledge and grow together. As participation increases, users can form "
                "local groups, exchange growing insights and work collectively towards "
                "larger community initiatives.",
                "The service could support communities in identifying underutilised land "
                "that could be transformed into green spaces. It also helps gather "
                "ground-level observations and food-production data, creating evidence "
                "communities can use to support research or funding applications.",
            ], None),
            ("A connected ecosystem", [], [
                "Direct plant scanning for quick, actionable insights",
                "Simple, accessible navigation with minimal steps",
                "Watering reminders and fixed care schedules",
                "Weather alerts based on your plants",
                "Track watering streaks and growing progress",
                "My Grove Garden to manage all your plants",
                "Personalised tips and tricks for what you grow",
                "Community space to connect and share",
                "Impact tracking to see your contribution",
            ]),
        ],
    ),
    dict(
        slug="retrofit", nav="Retrofit", hero="p-retrofit",
        title="Rebuilding trust in retrofit",
        meta="Service design", year="2026",
        alt="A curved terrace of Victorian sandstone tenements",
        lede="The project aims to reframe how trust is built in the retrofit process — "
             "often technical and misunderstood — by proposing a low-barrier, "
             "conversation-based intervention that builds relationships and creates a "
             "repeatable framework for participation.",
        sections=[
            ("The current reality of retrofit", [
                "Insights from community engagement, stakeholder conversations, and expert "
                "interviews revealed that the biggest barriers to retrofit are relational, "
                "not technical.",
            ], [
                "Homeowners: perception gap, fear of disruption, hidden skills",
                "Policy: jargon, no visible pathway, voluntary, no accountability",
                "Delivery: fragmented schemes, no implementation plan, conflicting guidance",
            ]),
            ("Synergy Days", [
                "A low-pressure, facilitated conversation at a community hub that brings "
                "homeowners, contractors, and local stakeholders together to develop the "
                "relationships that lead to trust. Targeting events already happening in "
                "the neighbourhood — not to sell retrofit or services, but to have open "
                "conversation structured through dialogue cards.",
            ], None),
            ("Why it works", [], [
                "Supports net zero delivery",
                "Converts interest into action",
                "Simplifies complicated retrofit knowledge",
            ]),
            ("Scaling and sustainability model", [
                "Over 6–12 months, run Synergy Days across different postal codes. "
                "Aggregate learnings into a public knowledge hub — a library of trust "
                "solutions — then expand it to commercial scale. Capture insights on what "
                "breaks and repairs trust, and in future expand into a digital platform.",
            ], None),
        ],
    ),
    dict(
        slug="healthcare", nav="Healthcare", hero="p-healthcare",
        title="Reimagining care using the natural environment",
        meta="Space design | System design", year="2025",
        alt="A hospital waiting room before and after redesign, with planting and daylight",
        lede="The project aims to develop a meaningful relationship with nature and "
             "purposefully connect it with care in the NHS, by creating a nature-inspired "
             "toolkit that helps patients feel calm in GP clinic waiting rooms through "
             "playful design interventions.",
        sections=[
            ("Building on shared knowledge", [
                "Early research intentionally explored the broad context of NHS Scotland — "
                "ranging from care systems to GP burnout. This scoping helped bring into "
                "view systemic pressures, existing assets, and the burden of overlooked "
                "everyday experiences within healthcare environments.",
                "The research identified burnout as a cumulative, environmental and "
                "experiential challenge shaped by everyday interactions, spaces and routines.",
            ], None),
            ("Co-design and brainstorming", [
                "Using design instruments to facilitate stakeholder engagement: an "
                "interactive nature-based icebreaker to initiate open conversation, and "
                "conversation through collage, encouraging participants to express "
                "experiences they might not put into words.",
                "Exploring nature-based interventions to reduce friction between the "
                "general practice clinic, admin staff and patients.",
            ], None),
            ("What the research told us", [], [
                "The GP clinic waiting room is the first point of contact between staff and patients",
                "It is an overwhelming, noisy and cluttered space that increases stress levels",
                "A toolkit is easy to implement and low maintenance",
                "Stakeholders are encouraged to care for the plants; materials are sturdy and easy to maintain",
            ]),
            ("The outcome", [
                "A nature-inspired toolkit that helps patients feel calm in GP clinic "
                "waiting rooms, through playful design interventions. Patient and staff "
                "empathy maps were used to test their needs against the proposed solution.",
            ], None),
        ],
    ),
    dict(
        slug="gas-station", nav="Gas station", hero="p-gas",
        title="Redesigning the future of CNG gas stations",
        meta="Service design | Rebranding", year="2024",
        alt="Rebranded Indraprastha Gas filling station with a covered waiting area",
        lede="This project conducted research into the existing brand philosophy and "
             "perception of Indraprastha Gas Limited, and its existing gas station "
             "experience — in order to propose a redesign of the brand and service "
             "experience for over 150 stations.",
        sections=[
            ("Decoding the existing brand experience", [
                "Workshops, co-design sessions and field visits, observing the customer "
                "journey and mapping user behaviour.",
            ], [
                "Brand personality exploration",
                "Employee perspective",
                "Business future vision",
                "Perception mapping",
                "Validating the user journey",
                "Incorporating employee needs",
                "Business expectations and aspirations",
            ]),
            ("Insights to action", [
                "Turning the insights collected through research into operational "
                "improvements.",
            ], [
                "Signage and navigation system design — reduce confusion and improve confidence in movement",
                "Structured user journey design — improved user journey experience and operational flow",
                "EV infrastructure and information system — EV support as part of future-ready services",
                "Digital and service revamp — standardised digital service systems improve trust and experience",
                "Facilities and comfort infrastructure upgrade — increase customer satisfaction",
                "Office and employee space redesign — boost work efficiency and morale",
            ]),
            ("The future-ready service experience", [
                "Designed a safer, smarter and future-ready experience for customers and "
                "employees across every touchpoint.",
            ], [
                "Station design — improved station visibility by totem redesign, with a comfortable, inclusive waiting area",
                "Safety — protective barriers and lane identification to improve safety and visibility",
                "Information and sign boards — live waiting time on a digital board, key services on static display",
                "Branding — consistent and strategic brand presence, increasing recall value",
                "Office redesign — improved office space with lockers and better facilities for employees",
            ]),
            ("Business impact", [
                "Value delivered through enhanced customer experience, operational "
                "efficiency and a strong brand presence.",
            ], [
                "YoY profit after tax growth during FY25–26",
                "EBITDA growth supporting business expansion",
                "Stations aligned to a more consistent experience network",
            ]),
        ],
    ),
    dict(
        slug="aviation", nav="Aviation", hero="p-aviation",
        title="Reimagining aviation safety",
        meta="Experience design | Space design", year="2024",
        alt="An Air India aircraft above the clouds at sunset",
        lede="This project was developed as part of a safety training initiative within "
             "Air India’s training centre, aimed at reinforcing aviation safety. The work "
             "involved creating a safety walkthrough designed to translate procedural "
             "safety guidelines into an immersive, spatial journey.",
        sections=[
            ("A journey in three zones", [], [
                "A neutral zone at the entry, welcoming visitors into the space",
                "Risk and consequence highlighted through dark contrast material — a strain-driven space evoking safety awareness",
                "Transition into clarity and resolution gained from experience — a well-lit, calm environment strengthening behavioural recall",
            ]),
            ("Designing the experience", [
                "Worked with stakeholders to understand operational needs and translate "
                "those insights into experience. Interactive experience design for advanced "
                "technologies, including multi-touch tables and VR simulation.",
            ], None),
            ("Impact", [
                "Designed an immersive safety centre for 5,000+ aviation professionals "
                "expected to undergo training at the Air India training academy.",
            ], None),
        ],
    ),
    dict(
        slug="tourism", nav="Tourism", hero="p-tourism",
        title="Tackling the challenges of tourism",
        meta="System design | UI design", year="2023",
        alt="Visitors riding elephants up the ramp to Amber Fort",
        lede="The project aims to investigate the fragmented tourism ecosystem and develop "
             "a scalable systems framework that strengthens connections between people, "
             "places, services and local stakeholders — enabling seamless, sustainable and "
             "culturally meaningful travel experiences.",
        sections=[
            ("Understanding the existing system", [
                "Conducted field research to observe the current tourism ecosystem, uncover "
                "stakeholder needs, and identify key challenges shaping the visitor "
                "experience.",
            ], [
                "Tourists struggled to find attractions without clear signage",
                "Streets littered with waste diminished the city’s aesthetic charm",
                "Local craftsmen lacked platforms to connect with visitors",
            ]),
            ("Concept and prototype", [
                "The solution we envisioned was a holistic, integrated waste management "
                "system doubling as a travel guide and a platform for local artisans, "
                "welcoming tourists to experience Rajasthan.",
            ], [
                "Rotating lid to ease garbage removal",
                "Lid on top to avoid overflow and smell",
                "Gap in between to provide contactless access",
                "Distinct shape to easily identify waste segregation",
            ]),
            ("A digital platform for a connected ecosystem", [], [
                "Enhance visitor experience — built-in wayfinding, city maps and QR-enabled digital information create seamless, intuitive navigation",
                "Empower local artisans — a dedicated space for craftspeople to showcase products, increasing visibility and supporting cultural heritage",
                "Encourage responsible waste disposal — rewards visitors for using waste collection points, redeemable at local shops and artisan stores",
            ]),
        ],
    ),
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Nishita Gupta</title>
<meta name="description" content="{lede_short}">
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
    <a href="index.html">Home</a>
    <a href="index.html#projects">Projects</a>
    <a href="cv.html">Full CV</a>
  </nav>
</header>

<main class="case-body">
  <a class="back" href="index.html#projects">Back to the work</a>

  <header class="case-head">
    <p class="case-meta">{meta} · {year}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </header>

  <img class="case-hero" src="assets/{hero}.webp" alt="{alt}" width="1200" height="675" decoding="async">

{sections}

  <nav class="case-next">
    <a class="btn" href="{next_slug}.html">Next: {next_nav}</a>
    <a class="btn btn-ghost" href="index.html#contact">Get in touch</a>
  </nav>
</main>
<script type="module" src="cursor.js"></script>
</body>
</html>
"""


def section_html(heading, paras, bullets):
    out = [f'  <section class="case-section">', f"    <h2>{html.escape(heading)}</h2>"]
    for p in paras:
        out.append(f"    <p>{html.escape(p)}</p>")
    if bullets:
        out.append('    <ul class="case-list">')
        out += [f"      <li>{html.escape(b)}</li>" for b in bullets]
        out.append("    </ul>")
    out.append("  </section>")
    return "\n".join(out)


for i, p in enumerate(PROJECTS):
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    body = "\n\n".join(section_html(*s) for s in p["sections"])
    page = PAGE.format(
        title=html.escape(p["title"]),
        lede=html.escape(p["lede"]),
        lede_short=html.escape(p["lede"][:155]),
        meta=html.escape(p["meta"]),
        year=p["year"],
        hero=p["hero"],
        alt=html.escape(p["alt"]),
        sections=body,
        next_slug=nxt["slug"],
        next_nav=html.escape(nxt["nav"]),
    )
    with open(os.path.join(OUT, f"{p['slug']}.html"), "w") as f:
        f.write(page)
    print("wrote", p["slug"] + ".html")
