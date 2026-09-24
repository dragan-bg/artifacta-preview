from pathlib import Path
import re

ROOT = Path('site')

CARD_BODY_OLD = 'Useful experiences that make sophisticated businesses feel simple.'
CARD_BODY_NEW = 'Test new products, categories and collections with lower inventory exposure before committing to scale.'
SEO_OLD = 'Digital products, websites and design systems that make complex B2B experiences clear, useful and easy to act on.'
SEO_NEW = 'Low-risk museum retail pilots using consignment, sale-or-return and hybrid stock models to test demand before scaling.'
HERO_OLD = 'We design digital products and websites that reduce friction, build confidence and make the next action feel obvious.'
HERO_NEW = 'Test real visitor demand through consignment, sale-or-return or hybrid stock models before committing to scale.'
OVERVIEW_OLD = 'Strategy, content, interface and technology are designed together. The result is not a polished screen on its own. It is a coherent experience that works for users, internal teams and the business behind it.'
OVERVIEW_NEW = 'A museum shop should not have to commit to a large quantity simply to discover whether a new product, category or collection will perform. We create controlled retail pilots designed to generate real selling data before a larger buying decision is made. Depending on the project, stock can be supplied through consignment, sale-or-return or a hybrid model combining purchased core items with lower-risk trial products. The objective is simple: reduce the cost of learning, identify the strongest products faster and scale only what earns its place on the shelf.'

def spans(value: str):
    out=[]
    for i,ch in enumerate(value):
        if ch == ' ':
            out.append(f'<span aria-hidden="true" style="--char-index:{i}" class="detail-title-space"> </span>')
        else:
            esc={'&':'&amp;','<':'&lt;','>':'&gt;'}.get(ch,ch)
            out.append(f'<span aria-hidden="true" style="--char-index:{i}">{esc}</span>')
    return ''.join(out)

path = ROOT / 'capabilities.html'
text = path.read_text(encoding='utf-8', errors='ignore')
card_pattern = re.compile(r'(<a[^>]+href="capabilities/digital-products\.html"[^>]*>)(.*?)(</a>)', re.S)
m=card_pattern.search(text)
if not m:
    raise SystemExit('Digital Products card not found')
opening=m.group(1).replace(
    'aria-label="Digital Products: Useful experiences that make sophisticated businesses feel simple."',
    'aria-label="Low-Risk Retail Pilot: Test new products, categories and collections with lower inventory exposure before committing to scale."'
)
card=m.group(2)
card=card.replace('src="images/agency/work-digital-product.webp"','src="images/agency/low-risk-retail-hero.webp"')
card=card.replace('alt="Premium editorial digital product shown across several devices"','alt="Curated museum-shop pilot assortment designed to test visitor demand with lower inventory risk"')
card=card.replace('02 - Digital','02 - Retail Pilot')
card=card.replace('Digital Products','Low-Risk Retail Pilot')
card=card.replace(CARD_BODY_OLD,CARD_BODY_NEW)
text=text[:m.start()]+opening+card+m.group(3)+text[m.end():]
path.write_text(text,encoding='utf-8')

path = ROOT / 'capabilities' / 'digital-products.html'
text = path.read_text(encoding='utf-8', errors='ignore')

text = text.replace('Digital Products - Axial', 'Low-Risk Retail Pilot - Axial')
text = text.replace(SEO_OLD, SEO_NEW)
text = text.replace('Digital products and websites that reduce friction, build confidence and make the next action feel obvious.', SEO_NEW)
text = text.replace('https://example.com/images/agency/work-digital-product.webp','https://dragan-bg.github.io/artifacta-preview/images/agency/low-risk-retail-hero.webp')

text = text.replace('src="../images/agency/work-digital-product.webp"','src="../images/agency/low-risk-retail-hero.webp"',1)
text = text.replace('alt="Premium editorial digital product shown across several devices"','alt="Curated museum-shop pilot assortment designed to test real visitor demand before scaling"',1)

pat = re.compile(r'<h1(?P<a1>[^>]*)aria-label="Digital Products"(?P<a2>[^>]*)data-character-reveal[^>]*>.*?</h1>', re.S)
m=pat.search(text)
if not m:
    raise SystemExit('Animated Digital Products title not found')
new_title=(f'<h1{m.group("a1")}aria-label="Low-Risk Retail Pilot"{m.group("a2")}data-character-reveal>'
           f'{spans("Low-Risk Retail Pilot")}</h1>')
text=text[:m.start()]+new_title+text[m.end():]
text=text.replace('<h1 class="capability-detail__title-mobile">Digital Products</h1>','<h1 class="capability-detail__title-mobile">Low-Risk Retail Pilot</h1>')
text=text.replace(HERO_OLD,HERO_NEW)

text=text.replace(OVERVIEW_OLD,OVERVIEW_NEW)
text=text.replace('src="../images/agency/process-optics.webp"','src="../images/agency/low-risk-retail-overview.webp"',1)
text=text.replace('alt="An exploded optical system standing in for the layers of a digital product"','alt="Museum retail pilot showing trial stock, approved products and performance insights"',1)

repl={
    'From first journey to a system teams can ship':'Flexible ways to test before you scale',
    'Experience strategy':'Consignment',
    'Business goals and user needs translated into a focused product direction.':'Selected products remain ARTIFACTA inventory until sold. The museum settles only sold units under the agreed cycle.',
    'Information architecture':'Sale or Return',
    'Content and functionality organized around how people actually make decisions.':'Purchase stock under agreed terms with a defined return mechanism for eligible unsold items.',
    'Product design':'Hybrid Pilot',
    'Interfaces that balance clarity, character and the realities of daily use.':'Combine a purchased core assortment with lower-risk trial SKUs to share the commitment.',
    'Design systems':'Lower Initial Commitment',
    'Reusable foundations that keep the experience consistent as products and teams grow.':'Test new ideas without allocating the full inventory budget upfront.',
    'Prototyping':'Real-World Validation',
    'High-fidelity experiences that make ideas tangible before major investment.':'Use actual visitor purchases to learn which products, designs and price points perform.',
    'Engineering handoff':'Flexible Replenishment',
    'Specs, states and collaboration that preserve intent all the way through build.':'Reorder winning SKUs and adjust, replace or discontinue slower items faster.',
}
for old,new in repl.items():
    text=text.replace(old,new)

pat = re.compile(
    r'<section(?P<s1>[^>]*)aria-label="One product\. Four layers\."(?P<s2>[^>]*)>\s*'
    r'<h2(?P<h1>[^>]*)aria-label="Inside\. One product\. Four layers\."(?P<h2>[^>]*)data-character-reveal[^>]*>.*?</h2>\s*</section>',
    re.S,
)
m=pat.search(text)
if not m:
    raise SystemExit('Digital product statement not found')
statement='One shelf. Four moves.'
new_statement=(f'<section{m.group("s1")}aria-label="{statement}"{m.group("s2")}>'
               f'<h2{m.group("h1")}aria-label="Inside. {statement}"{m.group("h2")}data-character-reveal>'
               f'<b aria-hidden="true" class="mr-[.13em] font-[450]">↓</b>{spans(statement)}</h2></section>')
text=text[:m.start()]+new_statement+text[m.end():]

moves={
    'Journey':'Select',
    'The sequence of decisions and moments that defines the experience.':'Choose a focused assortment, category or exhibition capsule with clear commercial potential.',
    'Interface':'Place',
    'The visual and interaction language customers see and feel.':'Introduce products through the agreed pilot structure and give them real museum-shop shelf space.',
    'System':'Measure',
    'The components and rules that keep every surface connected.':'Track sell-through, product mix, price-point response and replenishment behaviour.',
    'Delivery':'Scale',
    'The working rhythm that turns a product vision into a shipped experience.':'Reorder winning products and adjust, replace or discontinue slower items.',
}
for old,new in moves.items():
    text=text.replace(old,new)

text=text.replace('Make it matter.','Give us one shelf.')
text=text.replace('Start a project','Start a Retail Pilot')

path.write_text(text,encoding='utf-8')

listing=(ROOT/'capabilities.html').read_text(encoding='utf-8')
detail=path.read_text(encoding='utf-8')
checks=[
    ('listing title','Low-Risk Retail Pilot' in listing),
    ('detail title','aria-label="Low-Risk Retail Pilot"' in detail),
    ('hero image','low-risk-retail-hero.webp' in detail),
    ('overview image','low-risk-retail-overview.webp' in detail),
    ('Consignment','Consignment' in detail),
    ('Sale or Return','Sale or Return' in detail),
    ('Hybrid Pilot','Hybrid Pilot' in detail),
    ('One shelf. Four moves.','One shelf. Four moves.' in detail),
    ('Scale','Reorder winning products' in detail),
]
failed=[n for n,ok in checks if not ok]
if failed:
    raise SystemExit('Validation failed: '+', '.join(failed))
print('Low-Risk Retail Pilot patch applied successfully')
