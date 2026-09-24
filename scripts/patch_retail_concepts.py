from pathlib import Path
import re

ROOT = Path("site")

TITLE = "Retail Concepts & Impulse Design"
TITLE_HTML = "Retail Concepts &amp; Impulse Design"
CARD_BODY_OLD = "A sharper position, a clearer story and a brand built to lead."
CARD_BODY_NEW = "Turn small products, smart displays and accessible price points into stronger museum-shop sales."
SEO_OLD = "Positioning, brand architecture, messaging and launch strategy for complex B2B companies."
SEO_NEW = "Museum retail concepts, impulse products, low-MOQ collections, smart pricing and shelf-ready display solutions."
HERO_OLD = "We find the strategic idea that makes a complex business easy to understand, hard to confuse and ready for its next stage of growth."
HERO_NEW = "Great museum retail is not only about what you sell. We design products, displays, pricing and opening quantities together to make impulse purchasing easier and shelf space work harder."
OVERVIEW_OLD = "The strongest brands begin with a decision. We combine research, leadership alignment and creative strategy to define what your company stands for, who it matters to and how it should show up everywhere."
OVERVIEW_NEW = "We design the product and its retail environment together — combining compact displays, coordinated collections, accessible price points and smaller opening quantities. From countertop units and rotating stands to checkout displays, every solution is built around available space, target retail prices, margins and purchasing budget."

def spans(value: str):
    out = []
    for i, ch in enumerate(value):
        if ch == " ":
            out.append(f'<span aria-hidden="true" style="--char-index:{i}" class="detail-title-space"> </span>')
        else:
            esc = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(ch, ch)
            out.append(f'<span aria-hidden="true" style="--char-index:{i}">{esc}</span>')
    return "".join(out)

# 01 capability card
path = ROOT / "capabilities.html"
text = path.read_text(encoding="utf-8", errors="ignore")
pat = re.compile(r'(<a[^>]+href="capabilities/brand-strategy\.html"[^>]*>)(.*?)(</a>)', re.S)
m = pat.search(text)
if not m:
    raise SystemExit("Brand Strategy card not found")

opening = m.group(1).replace(
    'aria-label="Brand Strategy: A sharper position, a clearer story and a brand built to lead."',
    'aria-label="Retail Concepts &amp; Impulse Design: Turn small products, smart displays and accessible price points into stronger museum-shop sales."'
)
card = m.group(2)
card = card.replace(
    'src="images/agency/work-brand-system.webp"',
    'src="images/agency/retail-concepts-hero.webp"'
)
card = card.replace(
    'alt="Minimal brand system arranged on a warm editorial surface"',
    'alt="Curated museum-shop impulse display with coordinated souvenirs and shelf-ready presentation"'
)
card = card.replace("01 - Strategy", "01 - Retail Concepts")
card = card.replace("Brand Strategy", TITLE_HTML)
card = card.replace(CARD_BODY_OLD, CARD_BODY_NEW)
text = text[:m.start()] + opening + card + m.group(3) + text[m.end():]
path.write_text(text, encoding="utf-8")

# Detail page
path = ROOT / "capabilities" / "brand-strategy.html"
text = path.read_text(encoding="utf-8", errors="ignore")

# SEO/social
text = text.replace("Brand Strategy - Axial", TITLE + " - Axial")
text = text.replace(SEO_OLD, SEO_NEW)
text = text.replace(
    "https://example.com/images/agency/work-brand-system.webp",
    "https://dragan-bg.github.io/artifacta-preview/images/agency/retail-concepts-hero.webp"
)

# Hero visual
text = text.replace(
    'src="../images/agency/work-brand-system.webp"',
    'src="../images/agency/retail-concepts-hero.webp"',
    1
)
text = text.replace(
    'alt="Minimal brand system arranged on a warm editorial surface"',
    'alt="Curated museum-shop display combining impulse products, compact merchandising and coordinated presentation"',
    1
)

# Animated title
pat = re.compile(
    r'<h1(?P<a1>[^>]*)aria-label="Brand Strategy"(?P<a2>[^>]*)data-character-reveal[^>]*>.*?</h1>',
    re.S
)
m = pat.search(text)
if not m:
    raise SystemExit("Animated Brand Strategy title not found")
attrs = (m.group("a1") + f'aria-label="{TITLE_HTML}"' + m.group("a2") + "data-character-reveal")
attrs = attrs.replace("w-[49%]", "w-[68%]").replace("text-[64px]", "text-[52px]")
new_title = f'<h1{attrs}>{spans(TITLE)}</h1>'
text = text[:m.start()] + new_title + text[m.end():]
text = text.replace(
    '<h1 class="capability-detail__title-mobile">Brand Strategy</h1>',
    f'<h1 class="capability-detail__title-mobile">{TITLE_HTML}</h1>'
)
text = text.replace(HERO_OLD, HERO_NEW)

# Overview
text = text.replace(OVERVIEW_OLD, OVERVIEW_NEW)
text = text.replace(
    'src="../images/agency/journal-clarity.webp"',
    'src="../images/agency/retail-concepts-overview.webp"',
    1
)
text = text.replace(
    'alt="Editorial composition exploring clarity and brand direction"',
    'alt="Museum-shop checkout and impulse merchandising display designed around accessible price points"',
    1
)

# Six capability areas
replacements = {
    "From open questions to one useful direction": "Small products. Bigger retail potential.",
    "Research &amp; insight": "Display Concepts",
    "Customer, category and culture signals distilled into decisions the team can use.": "Countertop displays, rotating stands, hanging systems, trays and compact shelf solutions designed around the assortment.",
    "Positioning": "Impulse Products",
    "A differentiated place in the market, grounded in what the business can credibly own.": "Magnets, pins, keychains, bookmarks, charms and mini gifts designed for quick, low-friction purchase decisions.",
    "Brand architecture": "Low MOQ Collections",
    "Offers, products and audiences organized into a system that can grow without confusion.": "More designs with practical opening quantities and scalable reorders instead of overcommitting to every SKU.",
    "Messaging": "Smart Price Architecture",
    "A clear narrative, value proposition and language hierarchy for every important audience.": "A balanced assortment across entry, impulse, gift and premium price points.",
    "Naming": "Commercial Engineering",
    "Memorable names and verbal territories designed for strategic fit and long-term flexibility.": "Materials, packaging and production methods selected around target cost, retail price and required margin.",
    "Launch planning": "Ready-to-Merchandise",
    "A practical sequence for bringing the new story to teams, customers and the market.": "Header cards, boxes, hooks, trays, labels and display units developed with the product so it arrives closer to shelf-ready.",
}
for old, new in replacements.items():
    text = text.replace(old, new)

# Statement
pat = re.compile(
    r'<section(?P<s1>[^>]*)aria-label="One brand\. Four decisions\."(?P<s2>[^>]*)>\s*'
    r'<h2(?P<h1>[^>]*)aria-label="Inside\. One brand\. Four decisions\."(?P<h2>[^>]*)data-character-reveal[^>]*>.*?</h2>\s*</section>',
    re.S
)
m = pat.search(text)
if not m:
    raise SystemExit("Brand statement not found")
statement = "One collection. Four moves."
new_statement = (
    f'<section{m.group("s1")}aria-label="{statement}"{m.group("s2")}>'
    f'<h2{m.group("h1")}aria-label="Inside. {statement}"{m.group("h2")}data-character-reveal>'
    f'<b class="mr-[.13em] font-[450]" aria-hidden="true">↓</b>{spans(statement)}</h2></section>'
)
text = text[:m.start()] + new_statement + text[m.end():]

# Four moves
moves = {
    "Market": "Plan",
    "The change happening around the business and the opportunity it creates.": "Define the space, visitor profile, target price points and commercial objectives.",
    "Audience": "Curate",
    "The people we need to move, what they value and what stands in their way.": "Build a coordinated product mix across categories, designs and price levels.",
    "Proposition": "Display",
    "The distinctive value only this company is equipped to offer.": "Create the right presentation — from checkout impulse units to rotating stands and compact shelf concepts.",
    "Narrative": "Replenish",
    "The story and language that make the strategy memorable and repeatable.": "Track what sells, reorder winning SKUs and expand successful designs without rebuilding the entire range.",
}
for old, new in moves.items():
    text = text.replace(old, new)

# CTA
cta_pat = re.compile(
    r'<h2 class="final-cta__heading final-cta__heading--animated" aria-label="Make it matter\.">.*?</h2>',
    re.S
)
m = cta_pat.search(text)
if not m:
    raise SystemExit("Final CTA title not found")
cta = "Give us the space."
new_cta = (
    f'<h2 class="final-cta__heading final-cta__heading--animated" aria-label="{cta}">'
    f'{spans(cta)}</h2>'
)
text = text[:m.start()] + new_cta + text[m.end():]
text = text.replace(
    '<h2 class="final-cta__heading final-cta__heading--mobile">Make it matter.</h2>',
    '<h2 class="final-cta__heading final-cta__heading--mobile">Give us the space.</h2>'
)
text = text.replace('<span>Start a project</span>', '<span>Build a Retail Concept</span>', 1)

path.write_text(text, encoding="utf-8")

# Validation
listing = (ROOT / "capabilities.html").read_text(encoding="utf-8")
detail = path.read_text(encoding="utf-8")
checks = [
    ("listing title", "Retail Concepts &amp; Impulse Design" in listing),
    ("detail title", 'aria-label="Retail Concepts &amp; Impulse Design"' in detail),
    ("hero asset", "retail-concepts-hero.webp" in detail),
    ("overview asset", "retail-concepts-overview.webp" in detail),
    ("Display Concepts", "Display Concepts" in detail),
    ("Low MOQ Collections", "Low MOQ Collections" in detail),
    ("Smart Price Architecture", "Smart Price Architecture" in detail),
    ("One collection. Four moves.", "One collection. Four moves." in detail),
    ("Replenish", ">Replenish<" in detail),
    ("CTA", "Build a Retail Concept" in detail),
]
failed = [name for name, ok in checks if not ok]
if failed:
    raise SystemExit("Validation failed: " + ", ".join(failed))
print("Retail Concepts & Impulse Design patch applied successfully")
