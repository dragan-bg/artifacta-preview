from pathlib import Path
import re

ROOT = Path("site")

CARD_BODY_OLD = "Distinctive ideas designed to travel without losing their edge."
CARD_BODY_NEW = "Upgrade proven products through design, finishes and packaging."
SEO_OLD = "Campaign platforms, creative direction and channel systems for B2B launches and growth moments."
SEO_NEW = "Product analysis, creative upgrades, materials, packaging, production technology and cost engineering for museum-shop products."
HERO_OLD = "We build campaign ideas that earn attention in one moment and stay coherent across every market, format and team."
HERO_NEW = "Give us a product that already sells — or one with untapped potential. We analyse it, improve it and build a stronger version around design, materials, packaging, production and price."
OVERVIEW_OLD = "A strong campaign is more than a headline. We connect the strategic proposition, creative platform, visual world and rollout system so the work can flex across channels without becoming generic."
OVERVIEW_NEW = "We keep what makes the product recognisable and improve what creates value: colour, materials, finish, dimensional detail, packaging and manufacturing method. Every option is tested against target cost, MOQ, retail price and margin, so the result is not only more distinctive — it is commercially stronger."

def spans(text):
    out = []
    for i, ch in enumerate(text):
        if ch == " ":
            out.append(f'<span aria-hidden="true" style="--char-index:{i}" class="detail-title-space"> </span>')
        else:
            esc = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(ch, ch)
            out.append(f'<span aria-hidden="true" style="--char-index:{i}">{esc}</span>')
    return "".join(out)

# Capabilities listing card
path = ROOT / "capabilities.html"
text = path.read_text(encoding="utf-8", errors="ignore")
card_pattern = re.compile(
    r'(<a[^>]+href="capabilities/integrated-campaigns\.html"[^>]*>)(.*?)(</a>)',
    re.S,
)
m = card_pattern.search(text)
if not m:
    raise SystemExit("Integrated Campaigns card not found")

opening = m.group(1).replace(
    'aria-label="Integrated Campaigns: Distinctive ideas designed to travel without losing their edge."',
    'aria-label="Product Evolution: Upgrade proven products through design, finishes and packaging."',
)
card = m.group(2)
card = card.replace(
    'src="images/agency/work-campaign.webp"',
    'src="images/agency/product-evolution-overview.webp"',
)
card = card.replace(
    'alt="Bold campaign typography installed in an urban environment"',
    'alt="Museum souvenir shown before and after a premium product evolution"',
)
card = card.replace("03 - Campaigns", "03 - Product Evolution")
card = card.replace("Integrated Campaigns", "Product Evolution")
card = card.replace(CARD_BODY_OLD, CARD_BODY_NEW)
text = text[:m.start()] + opening + card + m.group(3) + text[m.end():]
path.write_text(text, encoding="utf-8")

# Detail page
path = ROOT / "capabilities" / "integrated-campaigns.html"
text = path.read_text(encoding="utf-8", errors="ignore")

# SEO / social metadata
text = text.replace("Integrated Campaigns - Axial", "Product Evolution - Axial")
text = text.replace(SEO_OLD, SEO_NEW)
text = text.replace(
    "https://example.com/images/agency/work-campaign.webp",
    "https://dragan-bg.github.io/artifacta-preview/images/agency/product-evolution-hero.webp",
)

# Hero
text = text.replace(
    'src="../images/agency/work-campaign.webp"',
    'src="../images/agency/product-evolution-hero.webp"',
    1,
)
text = text.replace(
    'alt="Bold campaign typography installed in an urban environment"',
    'alt="Museum souvenir evolution from a simple keepsake to a premium gift-ready product"',
    1,
)

title_pattern = re.compile(
    r'<h1(?P<a1>[^>]*)aria-label="Integrated Campaigns"(?P<a2>[^>]*)data-character-reveal[^>]*>.*?</h1>',
    re.S,
)
m = title_pattern.search(text)
if not m:
    raise SystemExit("Animated Integrated Campaigns title not found")
new_title = (
    f'<h1{m.group("a1")}aria-label="Product Evolution"{m.group("a2")}data-character-reveal>'
    f'{spans("Product Evolution")}</h1>'
)
text = text[:m.start()] + new_title + text[m.end():]
text = text.replace(
    '<h1 class="capability-detail__title-mobile">Integrated Campaigns</h1>',
    '<h1 class="capability-detail__title-mobile">Product Evolution</h1>',
)
text = text.replace(HERO_OLD, HERO_NEW)

# Overview
text = text.replace(OVERVIEW_OLD, OVERVIEW_NEW)
text = text.replace(
    'src="../images/agency/work-climate-launch.webp"',
    'src="../images/agency/product-evolution-overview.webp"',
    1,
)
text = text.replace(
    'alt="Climate campaign assets staged across a warm architectural landscape"',
    'alt="Museum souvenir product evolution showing an original item, upgraded design and premium packaging"',
    1,
)

# Six capability areas
replacements = {
    "One idea with enough range to keep moving": "Improve what already works",
    "Campaign platform": "Product Audit",
    "A strategic territory built around the audience, moment and business objective.": "Review the existing item, price point, construction, presentation and improvement potential.",
    "Creative concept": "Creative Upgrade",
    "A memorable organizing idea with a clear verbal and visual expression.": "Refine artwork, colour, form and detail while keeping the product recognisable.",
    "Channel design": "Materials &amp; Finishes",
    "The idea adapted to paid, owned, social, environmental and sales contexts.": "Add value through metal, epoxy, glitter, foil, embossing, 3D and layered effects.",
    "Content production": "Packaging",
    "Photography, film, motion and copy art-directed as one connected body of work.": "Create gift-ready cards, blisters, sleeves, boxes, stickers and holograms.",
    "Launch toolkits": "Cost Engineering",
    "Flexible templates and guidance that help local teams execute with confidence.": "Balance quality, MOQ, target retail price and margin to keep the offer competitive.",
    "Optimization": "Sampling &amp; Production",
    "Performance signals used to sharpen the work without flattening the idea.": "Prototype, refine, quality-check and scale the approved version into production.",
}
for old, new in replacements.items():
    text = text.replace(old, new)

# Four-step statement
statement_pattern = re.compile(
    r'<section(?P<s1>[^>]*)aria-label="One campaign\. Four moves\."(?P<s2>[^>]*)>\s*'
    r'<h2(?P<h1>[^>]*)aria-label="Inside\. One campaign\. Four moves\."(?P<h2>[^>]*)'
    r'data-character-reveal[^>]*>.*?</h2>\s*</section>',
    re.S,
)
m = statement_pattern.search(text)
if not m:
    raise SystemExit("Campaign statement not found")
statement = "One product. Four moves."
new_statement = (
    f'<section{m.group("s1")}aria-label="{statement}"{m.group("s2")}>'
    f'<h2{m.group("h1")}aria-label="Inside. {statement}"{m.group("h2")}data-character-reveal>'
    f'<b aria-hidden="true" class="mr-[.13em] font-[450]">↓</b>{spans(statement)}</h2></section>'
)
text = text[:m.start()] + new_statement + text[m.end():]

# Four-step system
systems = {
    "Idea": "Analyse",
    "The memorable thought that connects audience tension to brand value.": "Understand what works, what limits performance and where value can be added.",
    "Toolkit": "Reimagine",
    "The verbal, visual and motion assets that make the idea recognizable.": "Develop stronger design, materials, finishes, technology and presentation.",
    "Rollout": "Prototype",
    "The sequence of channels and moments that builds cumulative impact.": "Turn selected ideas into samples that can be evaluated before volume production.",
    "Measurement": "Optimise &amp; Scale",
    "The signals that show what is moving and where the work should evolve.": "Refine cost and quality, then prepare the product for repeatable manufacturing.",
}
for old, new in systems.items():
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")

# Validation
listing = (ROOT / "capabilities.html").read_text(encoding="utf-8")
detail = path.read_text(encoding="utf-8")
checks = [
    ("Product Evolution listing title", "Product Evolution" in listing),
    ("Product Evolution detail title", 'aria-label="Product Evolution"' in detail),
    ("Hero image", "product-evolution-hero.webp" in detail),
    ("Overview image", "product-evolution-overview.webp" in detail),
    ("Product Audit", "Product Audit" in detail),
    ("One product. Four moves.", "One product. Four moves." in detail),
    ("Optimise &amp; Scale", "Optimise &amp; Scale" in detail),
]
failed = [name for name, ok in checks if not ok]
if failed:
    raise SystemExit("Validation failed: " + ", ".join(failed))
print("Product Evolution v2 patch applied successfully")
