#!/usr/bin/env python3
"""
Pets of Perfection | static site builder
-----------------------------------------
Edit CONFIG, PRICES and copy below, then run from the repo root:

    python3 tools/build.py

It writes every .html page into the repo root (GitHub Pages serves it as is).
No dependencies beyond Python 3.
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =========================================================
# CONFIG: business facts (from petsofperfection.com)
# =========================================================
CONFIG = {
    "name": "Pets of Perfection",
    "sub": "Salon · Spa · Boutique",
    "phone": "561-369-0913",
    "phone_tel": "+15613690913",
    "email": "info@petsofperfection.com",
    "street": "11048 S. Military Trail",
    "city": "Boynton Beach",
    "state": "FL",
    "zip": "33436",
    "hours_short": "Tue to Sat · 8:30 AM to 4:00 PM",
    "hours_note": "Need a later pickup? Just ask. Hours can stretch on request.",
    "google_rating": "4.5",  # confirm current Google rating before launch
    "maps_link": "https://www.google.com/maps/search/?api=1&query=Pets+of+Perfection+11048+S+Military+Trail+Boynton+Beach+FL+33436",
    "maps_embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3570.186749778041!2d-80.12524828421265!3d26.514117683301052!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x88d9214032947675%3A0x7ca92e10969eb576!2sPets+of+Perfection!5e0!3m2!1sen!2sus!4v1478047633685",
    "instagram": "https://www.instagram.com/petsofperfection/",
    "instagram_handle": "@petsofperfection",
    "facebook": "https://www.facebook.com/petsofperfection/",
    "pinterest": "https://www.pinterest.com/petsofperfect/",
    "site_url": "https://petsofperfection.com",
}

# =========================================================
# PRICES: SAMPLE starting prices for the demo.
# Replace with the salon's real numbers before launch.
# =========================================================
SIZES = [
    ("s", "Small", "up to 20 lb", 34),
    ("m", "Medium", "21 to 40 lb", 42),
    ("l", "Large", "41 to 70 lb", 50),
    ("xl", "X-Large", "71 lb and up", 58),
]

DOG_SERVICES = [
    dict(id="full-groom", name="The Full Groom", nick="Head-to-tail glow up", color="mint", icon="scissors",
         desc="Bath, blow-dry, a breed-standard or custom haircut, nails, ears and a tidy of the sanitary areas.",
         incl=["Premium shampoo and conditioner", "Hand-finished haircut", "Nails, ears and paw pads"],
         prices=dict(s=65, m=80, l=95, xl=120)),
    dict(id="spa-bath", name="Spa Bath & Tidy", nick="The between-cuts refresh", color="bubble", icon="bubbles",
         desc="A luxurious bath, fluffy blow-dry and full brush-out, plus a face, feet and sanitary tidy.",
         incl=["Deep-clean bath and conditioner", "Fluff dry and brush-out", "Nails and ear cleaning"],
         prices=dict(s=45, m=55, l=70, xl=90)),
    dict(id="hand-strip", name="Hand-Stripping", nick="For terriers and wire coats", color="sun", icon="sparkle",
         desc="The traditional way to keep a wire coat crisp, colorful and true to breed standard. Slow, careful, worth it.",
         incl=["Coat pulled by hand, never clipped", "Bath and finish", "Breed-standard shaping"],
         prices=dict(s=90, m=110, l=130, xl=150)),
    dict(id="puppy", name="Puppy's First Groom", nick="Gentle intro, under 6 months", color="pink", icon="heart",
         desc="A short, happy first visit with a bath, face and feet trim, nails and plenty of praise so grooming feels fun for life.",
         incl=["Extra time to settle in", "Gentle bath and fluff", "Treats. Lots of treats."],
         prices=dict(s=40, m=45, l=50, xl=55)),
    dict(id="deshed", name="De-Shed Treatment", nick="Less fur on your couch", color="mint", icon="comb",
         desc="A deep conditioning treatment and high-velocity blow-out that pulls loose undercoat before it hits your floors.",
         incl=["Add to any bath or groom", "Great for Labs, Huskies, Goldens", "Leaves the coat soft and shiny"],
         prices=dict(s=25, m=35, l=45, xl=55)),
]

ADDONS = [
    ("Nail trim", "$15"),
    ("Nail grind (smooth finish)", "$20"),
    ("Teeth brushing", "$10"),
    ("Ear cleaning", "$10"),
    ("Blueberry facial", "$12"),
    ("Paw pad balm", "$8"),
    ("Bow or bandana", "Free"),
    ("De-matting", "from $15"),
]

CAT_SERVICES = [
    dict(id="cat-bath", name="Cat Bath & Fluff Dry", nick="Clean, calm, done", color="pink", icon="bubbles",
         desc="A gentle bath with cat-safe products, careful towel and low-heat dry, and a full comb-out.",
         price="$75"),
    dict(id="lion-cut", name="The Lion Cut", nick="Mane event", color="sun", icon="scissors",
         desc="Short body, fluffy mane, boots and a tail pom. Perfect for matted coats and Florida summers.",
         price="$90"),
    dict(id="cat-comb", name="Comb-Out & De-Mat", nick="No bath needed", color="mint", icon="comb",
         desc="Patient work through tangles and loose undercoat, ideal for long-haired breeds between full grooms.",
         price="from $50"),
    dict(id="cat-nails", name="Cat Nail Trim", nick="Save your sofa", color="bubble", icon="sparkle",
         desc="Quick, calm and over before they can file a complaint.",
         price="$20"),
]

REVIEWS = [
    dict(stars=5, text="They do a great job grooming our little dog, and are always available for nail trims for our bigger girl. The groomer is wonderful and we love supporting a small business!",
         who="Local customer", src="via BestProsInTown"),
    dict(stars=5, text="After several years in Florida, my furrbabies have finally found their forever salon! Pets of Perfection is by far the most professional, educated, and talented grooming staff...",
         who="Pet parent", src="via Yellow Pages"),
    dict(stars=5, text="I brought him to Pets of Perfection about 1 year ago and haven't left. I bring him every month and they do an amazing job.",
         who="Demi A., Pomeranian parent", src="via Yelp"),
]

NAV = [
    ("services.html", "Services"),
    ("cats.html", "Cats"),
    ("gallery.html", "Gallery"),
    ("reviews.html", "Reviews"),
    ("about.html", "About"),
    ("faq.html", "FAQ"),
]

INK = "#1F2A44"
PINK = "#FF8FA3"
MINT = "#BFEBD9"
SUN = "#FFD166"
CREAMY = "#FFF5E8"

# =========================================================
# ICONS (24px, stroke)
# =========================================================
_ICONS = {
    "phone": '<path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 6 6L15 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1.1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 12h.01M12 12h.01M15.5 12h.01"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M16 3v4M8 3v4M3 10h18"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/>',
    "bubbles": '<circle cx="9" cy="14" r="5"/><circle cx="17" cy="7" r="3"/><circle cx="18.5" cy="16" r="2"/><path d="M7 12.5a2 2 0 0 1 2-1.5"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.7 1.8L21.5 17.5l-1.8.7L19 20l-.7-1.8-1.8-.7 1.8-.7z"/>',
    "heart": '<path d="M12 20s-7-4.4-9.2-9A4.9 4.9 0 0 1 12 6.3 4.9 4.9 0 0 1 21.2 11C19 15.6 12 20 12 20z"/>',
    "comb": '<path d="M3 7h18v4H3z"/><path d="M5 11v6M8.5 11v7M12 11v6M15.5 11v7M19 11v6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3.5 7.5 12 13l8.5-5.5"/>',
    "check": '<path d="M5 12.5l4.2 4.2L19 7"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "alert": '<circle cx="12" cy="12" r="9"/><path d="M12 7.5V13M12 16.5v.01"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "leaf": '<path d="M5 19c0-8 6-14 15-14 0 9-6 15-14 15"/><path d="M5 19l7-7"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h7"/>',
    "cat": '<path d="M4 10V4l4.5 3h7L20 4v6c0 4.97-3.58 9-8 9s-8-4.03-8-9z"/><path d="M9 11.5h.01M15 11.5h.01M10.5 15c1 .8 2 .8 3 0"/>',
    "dog": '<path d="M7 5 3.5 7.5 5 13l2-1.5"/><path d="M17 5l3.5 2.5L19 13l-2-1.5"/><path d="M7 5h10v7a5 5 0 0 1-10 0z"/><path d="M10 9.5h.01M14 9.5h.01M11 13h2"/>',
    "bag": '<path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    "facebook": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/>',
    "pinterest": '<circle cx="12" cy="12" r="9"/><path d="M10.6 20l1.7-7.4"/><path d="M8 13.4c-.6-.6-1-1.5-1-2.5 0-2.7 2.3-5 5.4-5 3 0 5.1 2 5.1 4.8 0 2.8-1.5 5-3.8 5-1.2 0-2-.8-1.8-2"/>',
}
_FILLED = {
    "paw": '<ellipse cx="5.5" cy="10" rx="2.1" ry="2.7"/><ellipse cx="9.4" cy="5.6" rx="2.1" ry="2.8"/><ellipse cx="14.6" cy="5.6" rx="2.1" ry="2.8"/><ellipse cx="18.5" cy="10" rx="2.1" ry="2.7"/><path d="M12 11.2c-3.4 0-6.4 3.5-6.4 6.2 0 1.9 1.6 2.9 3.4 2.6 1.2-.2 1.9-.7 3-.7s1.8.5 3 .7c1.8.3 3.4-.7 3.4-2.6 0-2.7-3-6.2-6.4-6.2z"/>',
    "star": '<path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.3 6.4 20.2l1.1-6.3L2.9 9.5l6.3-.9z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    if name in _FILLED:
        return f'<svg{c} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">{_FILLED[name]}</svg>'
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_ICONS[name]}</svg>')


# =========================================================
# ILLUSTRATIONS
# =========================================================
def _star(cx, cy, r, fill=SUN):
    pts = []
    for i in range(8):
        a = math.pi / 4 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.38
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'


def pet_face(fur="#F4C89A", ear=None, messy=False, acc=None, kind="dog", ears="flop",
             width=None, label=None, sparkles=True, extra_cls=""):
    """Cartoon pet face, 200x200. messy=True draws the 'before' version."""
    ear = ear or fur
    s = []
    if messy:
        s.append('<g fill="none" stroke="#8A93A8" stroke-width="4" stroke-linecap="round" opacity=".85">'
                 '<path d="M66 30c-7 6 7 10 0 17"/><path d="M100 16c-7 6 7 10 0 17"/><path d="M134 30c-7 6 7 10 0 17"/></g>')
    # ears
    if kind == "cat" or ears == "point":
        s.append(f'<path d="M48 94 L54 24 L100 62 Z" fill="{ear}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        s.append(f'<path d="M152 94 L146 24 L100 62 Z" fill="{ear}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        s.append('<path d="M60 76 L62 44 L84 62Z" fill="#FFB3C1"/><path d="M140 76 L138 44 L116 62Z" fill="#FFB3C1"/>')
    else:
        s.append(f'<ellipse cx="52" cy="106" rx="24" ry="44" transform="rotate(18 52 106)" fill="{ear}" stroke="{INK}" stroke-width="5"/>')
        s.append(f'<ellipse cx="148" cy="106" rx="24" ry="44" transform="rotate(-18 148 106)" fill="{ear}" stroke="{INK}" stroke-width="5"/>')
    # head
    if messy:
        pts = []
        n = 34
        for i in range(n):
            a = 2 * math.pi * i / n
            r = (62 if i % 2 == 0 else 76) + ((i * 37) % 7) - 3
            pts.append(f"{100 + r * math.cos(a):.1f},{108 + r * math.sin(a):.1f}")
        s.append(f'<polygon points="{" ".join(pts)}" fill="{fur}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        s.append('<ellipse cx="68" cy="150" rx="9" ry="6" fill="#7A5A3A" opacity=".35"/><ellipse cx="134" cy="70" rx="7" ry="5" fill="#7A5A3A" opacity=".3"/>')
    else:
        s.append(f'<circle cx="100" cy="108" r="62" fill="{fur}" stroke="{INK}" stroke-width="5"/>')
    # eyes
    s.append(f'<g class="pet-eyes"><circle cx="78" cy="100" r="10.5" fill="#fff" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="122" cy="100" r="10.5" fill="#fff" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="79" cy="102" r="6.2" fill="{INK}"/><circle cx="123" cy="102" r="6.2" fill="{INK}"/>'
             '<circle cx="81.2" cy="99.6" r="2.1" fill="#fff"/><circle cx="125.2" cy="99.6" r="2.1" fill="#fff"/></g>')
    if messy:
        s.append(f'<path d="M42 102 L50 76 L60 98 L70 70 L80 100 L90 68 L100 98 L110 68 L120 100 L130 70 L140 98 L150 76 L158 102 Q100 112 42 102 Z" '
                 f'fill="{fur}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    if kind == "cat":
        s.append(f'<path d="M93 122 h14 l-7 8z" fill="{PINK}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
        s.append(f'<path d="M100 130 v6 M100 136 q-7 7 -13 2 M100 136 q7 7 13 2" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
        s.append(f'<g stroke="{INK}" stroke-width="3" stroke-linecap="round"><path d="M70 128 L34 120"/><path d="M70 136 L34 140"/><path d="M130 128 L166 120"/><path d="M130 136 L166 140"/></g>')
        if not messy:
            s.append(f'<ellipse cx="66" cy="124" rx="9" ry="5.5" fill="{PINK}" opacity=".5"/><ellipse cx="134" cy="124" rx="9" ry="5.5" fill="{PINK}" opacity=".5"/>')
    else:
        s.append(f'<ellipse cx="100" cy="134" rx="30" ry="22" fill="{CREAMY}" stroke="{INK}" stroke-width="4"/>')
        s.append(f'<ellipse cx="100" cy="124" rx="10.5" ry="7.5" fill="{INK}"/><ellipse cx="97" cy="121.5" rx="3" ry="1.8" fill="#fff" opacity=".7"/>')
        if messy:
            s.append(f'<path d="M86 144 q7 -5 14 0 q7 5 14 0" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
        else:
            s.append(f'<path d="M93 141 q7 18 14 0 z" fill="{PINK}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
            s.append(f'<path d="M100 131 v8 M100 139 q-8 9 -17 3 M100 139 q8 9 17 3" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
            s.append(f'<ellipse cx="62" cy="128" rx="10" ry="6" fill="{PINK}" opacity=".5"/><ellipse cx="138" cy="128" rx="10" ry="6" fill="{PINK}" opacity=".5"/>')
    # accessories (after only)
    if not messy:
        if acc == "bow":
            s.append(f'<g transform="translate(142 54) rotate(-16)"><path d="M0 0 L-24 -13 L-24 13 Z" fill="{PINK}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                     f'<path d="M0 0 L24 -13 L24 13 Z" fill="{PINK}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                     f'<circle r="7" fill="{PINK}" stroke="{INK}" stroke-width="4"/></g>')
        elif acc == "bandana":
            s.append(f'<path d="M56 160 Q100 180 144 160 L100 198 Z" fill="{MINT}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                     '<circle cx="86" cy="172" r="3.5" fill="#fff"/><circle cx="112" cy="174" r="3.5" fill="#fff"/><circle cx="100" cy="186" r="3.5" fill="#fff"/>')
        elif acc == "crown":
            s.append(f'<path d="M72 52 L78 24 L92 42 L100 18 L108 42 L122 24 L128 52 Z" fill="{SUN}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
        if sparkles:
            s.append(_star(28, 46, 13) + _star(176, 150, 11) + _star(174, 36, 8, "#fff"))
    w = f' width="{width}"' if width else ""
    a11y = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    cls = f' class="{extra_cls}"' if extra_cls else ""
    return f'<svg{cls} viewBox="0 0 200 200"{w} {a11y}>{"".join(s)}</svg>'


HERO_DOG = f'''<svg class="hero-dog" viewBox="0 0 420 380" role="img" aria-label="A happy golden pup in a bubble bath, tail wagging">
  <g class="bubbles">
    <circle class="b b1" cx="78" cy="196" r="11"/><circle class="b b2" cx="126" cy="186" r="7"/>
    <circle class="b b3" cx="300" cy="190" r="12"/><circle class="b b4" cx="350" cy="196" r="8"/>
    <circle class="b b5" cx="196" cy="200" r="6"/><circle class="b b6" cx="250" cy="194" r="9"/>
    <circle class="b b7" cx="60" cy="210" r="6"/><circle class="b b8" cx="330" cy="206" r="10"/>
  </g>
  <g class="tail">
    <path d="M318 236 C 352 222, 360 186, 384 160" fill="none" stroke="{INK}" stroke-width="23" stroke-linecap="round"/>
    <path d="M318 236 C 352 222, 360 186, 384 160" fill="none" stroke="#F4C89A" stroke-width="13" stroke-linecap="round"/>
  </g>
  <g class="dog">
    <ellipse cx="146" cy="160" rx="25" ry="47" transform="rotate(16 146 160)" fill="#C98B5B" stroke="{INK}" stroke-width="5"/>
    <ellipse cx="274" cy="160" rx="25" ry="47" transform="rotate(-16 274 160)" fill="#C98B5B" stroke="{INK}" stroke-width="5"/>
    <ellipse cx="210" cy="142" rx="72" ry="66" fill="#F4C89A" stroke="{INK}" stroke-width="5"/>
    <ellipse cx="160" cy="168" rx="12" ry="7" fill="{PINK}" opacity=".55"/>
    <ellipse cx="260" cy="168" rx="12" ry="7" fill="{PINK}" opacity=".55"/>
    <ellipse cx="210" cy="174" rx="40" ry="30" fill="{CREAMY}" stroke="{INK}" stroke-width="4"/>
    <g class="eyes">
      <circle cx="184" cy="134" r="11.5" fill="#fff" stroke="{INK}" stroke-width="3"/>
      <circle cx="236" cy="134" r="11.5" fill="#fff" stroke="{INK}" stroke-width="3"/>
      <circle cx="186" cy="136" r="7" fill="{INK}"/><circle cx="238" cy="136" r="7" fill="{INK}"/>
      <circle cx="188.6" cy="133.4" r="2.4" fill="#fff"/><circle cx="240.6" cy="133.4" r="2.4" fill="#fff"/>
    </g>
    <path d="M200 186 Q202 210 210 210 Q218 210 220 186 Z" fill="{PINK}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M197 158 Q210 150 223 158 Q223 168 210 171 Q197 168 197 158Z" fill="{INK}"/>
    <path d="M210 171 V180 M210 180 Q200 192 188 184 M210 180 Q220 192 232 184" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>
    <g fill="#fff" stroke="{INK}" stroke-width="4">
      <circle cx="156" cy="100" r="13"/><circle cx="178" cy="86" r="20"/><circle cx="206" cy="74" r="25"/>
      <circle cx="236" cy="82" r="21"/><circle cx="260" cy="98" r="14"/>
    </g>
    <circle cx="198" cy="64" r="4" fill="{MINT}"/><circle cx="230" cy="76" r="3" fill="{MINT}"/>
  </g>
  <path d="M62 226 H358 L340 318 Q336 336 316 336 H104 Q84 336 80 318 Z" fill="#fff" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  <path d="M74 264 H346" stroke="{PINK}" stroke-width="10"/>
  <path d="M77 282 H343" stroke="{PINK}" stroke-width="4" stroke-dasharray="2 12" stroke-linecap="round"/>
  <circle cx="112" cy="346" r="12" fill="{INK}"/><circle cx="308" cy="346" r="12" fill="{INK}"/>
  <rect x="46" y="208" width="328" height="30" rx="15" fill="#CDEBFA" stroke="{INK}" stroke-width="5"/>
  <g fill="#fff" stroke="{INK}" stroke-width="4">
    <circle cx="70" cy="207" r="16"/><circle cx="98" cy="200" r="20"/><circle cx="124" cy="208" r="12"/>
    <circle cx="294" cy="206" r="13"/><circle cx="320" cy="199" r="20"/><circle cx="350" cy="207" r="15"/>
  </g>
  <g fill="#F4C89A" stroke="{INK}" stroke-width="4">
    <ellipse cx="164" cy="212" rx="25" ry="15"/><ellipse cx="256" cy="212" rx="25" ry="15"/>
  </g>
  <path d="M156 206v9M166 205v10M174 207v8M248 207v8M256 205v10M266 206v9" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
  <g class="duck">
    <ellipse cx="96" cy="180" rx="22" ry="15" fill="{SUN}" stroke="{INK}" stroke-width="4"/>
    <circle cx="108" cy="162" r="12" fill="{SUN}" stroke="{INK}" stroke-width="4"/>
    <path d="M118 162 l12 3 -12 4z" fill="#FF9F43" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
    <circle cx="111" cy="159" r="2.6" fill="{INK}"/>
  </g>
</svg>'''

SQUIGGLE = '<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M4 14 Q 25 2 46 12 T 88 12 T 130 12 T 172 12 T 214 12 T 256 12 T 296 10" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>'


# =========================================================
# SHARED PARTS
# =========================================================
def addr_line():
    c = CONFIG
    return f'{c["street"]}, {c["city"]}, {c["state"]} {c["zip"]}'


def header(active):
    c = CONFIG
    cur = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{href}"{cur if href == active else ""}>{label}</a></li>'
        for href, label in NAV)
    book_cur = cur if active == "book.html" else ""
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="topbar"><div class="wrap">
    <div class="topbar-left">
      <span class="status" data-open-status><span class="status-dot"></span><span class="status-text">{c["hours_short"]}</span></span>
      <a class="topbar-hide-sm" href="{c["maps_link"]}" target="_blank" rel="noopener">{icon("pin")}{c["street"]}, {c["city"]}</a>
    </div>
    <a href="tel:{c["phone_tel"]}">{icon("phone")}{c["phone"]}</a>
  </div></div>
  <div class="wrap nav-row">
    <a class="brand" href="index.html" aria-label="{c["name"]} home">
      <span class="brand-mark"><img src="img/logo-mark.svg" alt="" width="76" height="76"></span>
      <span><span class="brand-name">{c["name"]}</span><span class="brand-sub">{c["sub"]}</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav">
      <span class="sr-only">Menu</span>{icon("menu", "icon-open")}{icon("close", "icon-close")}
    </button>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>{links}<li class="nav-cta"><a class="btn btn-pink btn-small" href="book.html"{book_cur}>{icon("paw")}Book a groom</a></li></ul>
    </nav>
  </div>
</header>'''


def footer():
    c = CONFIG
    explore = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html"><span class="brand-mark"><img src="img/logo-mark.svg" alt="" width="76" height="76"></span><span><span class="brand-name">{c["name"]}</span><span class="brand-sub">{c["sub"]}</span></span></a>
        <p class="foot-about">A luxury pet salon, spa and boutique in Boynton Beach. Every pet is family here, and every groom is done with love.</p>
        <div class="socials">
          <a href="{c["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a>
          <a href="{c["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook">{icon("facebook")}</a>
          <a href="{c["pinterest"]}" target="_blank" rel="noopener" aria-label="Pinterest">{icon("pinterest")}</a>
        </div>
      </div>
      <div>
        <h4>Visit</h4>
        <ul>
          <li><a href="{c["maps_link"]}" target="_blank" rel="noopener">{c["street"]}<br>{c["city"]}, {c["state"]} {c["zip"]}</a></li>
          <li>{c["hours_short"]}</li>
          <li>Closed Sunday and Monday</li>
        </ul>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>{explore}<li><a href="book.html">Book a groom</a></li></ul>
      </div>
      <div>
        <h4>Say hi</h4>
        <ul>
          <li><a href="tel:{c["phone_tel"]}">{c["phone"]}</a></li>
          <li><a href="sms:{c["phone_tel"]}">Text us</a></li>
          <li><a href="mailto:{c["email"]}">{c["email"]}</a></li>
          <li><a href="policies.html">Privacy &amp; SMS policy</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; <span data-year>2026</span> {c["name"]}. Made with treats in Boynton Beach.</span>
      <span>Website by <a href="https://tskaizen.com" target="_blank" rel="noopener">tsKaizen</a></span>
    </div>
  </div>
</footer>
<nav class="action-bar" aria-label="Quick actions">
  <a href="tel:{c["phone_tel"]}">{icon("phone")}Call</a>
  <a href="sms:{c["phone_tel"]}">{icon("chat")}Text</a>
  <a class="go" href="book.html">{icon("paw")}Book now</a>
</nav>'''


def page(slug, title, desc, body, active="", extra_head=""):
    c = CONFIG
    url = f'{c["site_url"]}/{"" if slug == "index.html" else slug}'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{c["name"]}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#FFF8EE">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Caveat:wght@600;700&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<script>document.documentElement.classList.add("js");</script>
{extra_head}
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="js/config.js"></script>
<script src="js/main.js" defer></script>
</body>
</html>
'''


def tag_dog(svc, show_book=True, static_size=None, delay=""):
    p = svc["prices"]
    start = p[static_size or "s"]
    incl = "".join(f'<li>{icon("check")}{i}</li>' for i in svc.get("incl", []))
    size_lbl = "small pups"
    btn = (f'<a class="btn btn-small" href="book.html?service={svc["id"]}" aria-label="Book {svc["name"]}">Book this {icon("arrow")}</a>'
           if show_book else "")
    return f'''<article class="tag {svc["color"]} reveal {delay}">
  <span class="tag-band" aria-hidden="true"></span>
  <div class="tag-icon">{icon(svc["icon"])}</div>
  <p class="nick">{svc["nick"]}</p>
  <h3>{svc["name"]}</h3>
  <p>{svc["desc"]}</p>
  <ul>{incl}</ul>
  <div class="tag-foot">
    <div class="price"><small>from</small><strong data-prices data-s="{p["s"]}" data-m="{p["m"]}" data-l="{p["l"]}" data-xl="{p["xl"]}">${start}</strong><span class="unit">for <span data-size-label>{size_lbl}</span></span></div>
    {btn}
  </div>
</article>'''


def tag_cat(svc, delay=""):
    return f'''<article class="tag {svc["color"]} reveal {delay}">
  <span class="tag-band" aria-hidden="true"></span>
  <div class="tag-icon">{icon(svc["icon"])}</div>
  <p class="nick">{svc["nick"]}</p>
  <h3>{svc["name"]}</h3>
  <p>{svc["desc"]}</p>
  <div class="tag-foot">
    <div class="price"><small>price</small><strong>{svc["price"]}</strong></div>
    <a class="btn btn-small" href="book.html?service={svc["id"]}" aria-label="Book {svc["name"]}">Book this {icon("arrow")}</a>
  </div>
</article>'''


def quotes_block():
    items = []
    for r in REVIEWS:
        items.append(f'''<figure class="quote reveal">
  <div class="stars" aria-label="{r["stars"]} out of 5 stars">{"&#9733;" * r["stars"]}</div>
  <blockquote><p>&ldquo;{r["text"]}&rdquo;</p></blockquote>
  <figcaption>{r["who"]} &middot; {r["src"]}</figcaption>
</figure>''')
    return f'<div class="quotes">{"".join(items)}</div>'


def visit_block(title="Come say hi"):
    c = CONFIG
    return f'''<section class="section" aria-labelledby="visit-title">
  <div class="wrap">
    <div class="visit reveal">
      <div class="visit-info">
        <p class="hand">we'll have the treats ready</p>
        <h2 id="visit-title">{title}</h2>
        <dl>
          <div><dt>Where</dt><dd><a href="{c["maps_link"]}" target="_blank" rel="noopener">{addr_line()}</a></dd></div>
          <div><dt>When</dt><dd>{c["hours_short"]}<br><span style="font-weight:600;color:var(--ink-soft)">{c["hours_note"]}</span></dd></div>
          <div><dt>Right now</dt><dd><span class="status" data-open-status><span class="status-dot"></span><span class="status-text">{c["hours_short"]}</span></span></dd></div>
          <div><dt>Call or text</dt><dd><a href="tel:{c["phone_tel"]}">{c["phone"]}</a></dd></div>
        </dl>
        <div class="btn-row">
          <a class="btn btn-pink" href="book.html">{icon("paw")}Book a groom</a>
          <a class="btn" href="{c["maps_link"]}" target="_blank" rel="noopener">{icon("pin")}Directions</a>
        </div>
      </div>
      <div class="visit-map">
        <iframe src="{c["maps_embed"]}" title="Map to Pets of Perfection on S. Military Trail" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </div>
</section>'''


def cta_band(title="Your dog called. They want a spa day.", text="Book online in about a minute. We'll text to confirm."):
    return f'''<section class="cta-band" aria-label="Book an appointment">
  <div class="wrap cta-inner">
    {pet_face("#F4C89A", "#C98B5B", acc="bandana", extra_cls="cta-face", sparkles=False)}
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="btn-row"><a class="btn" href="book.html">{icon("paw")}Fetch my appointment</a></div>
  </div>
</section>'''


def page_hero(title, lede, crumb, tone="mint", deco=""):
    return f'''<section class="page-hero {tone}">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / {crumb}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
  {deco}
</section>'''


# =========================================================
# PAGES
# =========================================================
def build_home():
    c = CONFIG
    paws = "".join(icon("paw") for _ in range(8))
    marquee_items = ["Spa baths", "Breed-standard cuts", "Hand-stripping", "Nail trims", "Teeth brushing", "De-shedding", "Cats welcome", "Puppy first grooms"]
    mq = "".join(f'<span>{icon("paw")}{m}</span>' for m in marquee_items)
    tags = "".join(tag_dog(s, delay=f"d{i}") for i, s in enumerate(DOG_SERVICES[:3]))
    steps = [
        ("calendar", "Book in a minute", "Pick a service and a day online, or give us a call. We'll text to confirm."),
        ("heart", "Drop off and say hi", "Tell us about coat, quirks and favorite treats. We take notes."),
        ("bubbles", "Spa time", "Bath, blow-dry, cut and the little extras, done calmly with no rushing."),
        ("chat", "\"I'm ready!\" text", "We text you the moment your pet is fresh, fluffy and ready to go home."),
    ]
    steps_html = "".join(
        f'<li class="step reveal d{i}"><span class="step-num">{i + 1}</span>{icon(ic, "step-ico")}<h3>{t}</h3><p>{d}</p></li>'
        for i, (ic, t, d) in enumerate(steps))
    perks = [
        ("scissors", "Breed standards, not guesswork", "From a Poodle's precise scissoring to a Terrier's hand-strip, every detail is done by eye and by hand."),
        ("leaf", "Calm, clean, no rush", "A relaxed, stress-free salon where pets get time to settle in. Kindness and respect, always."),
        ("book", "Always learning", "Ongoing education in pet styling keeps our safety and style standards high."),
        ("heart", "Regulars for years", "Many families have trusted us with their pets for years. That says more than we could."),
    ]
    perks_html = "".join(f'<li class="perk">{icon(ic)}<h3>{t}</h3><p>{d}</p></li>' for ic, t, d in perks)
    schema = {
        "@context": "https://schema.org", "@type": "LocalBusiness", "name": c["name"],
        "description": "Luxury pet salon, spa and boutique for dogs and cats in Boynton Beach, Florida.",
        "telephone": c["phone"], "email": c["email"], "url": c["site_url"],
        "address": {"@type": "PostalAddress", "streetAddress": c["street"], "addressLocality": c["city"],
                    "addressRegion": c["state"], "postalCode": c["zip"], "addressCountry": "US"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                       "opens": "08:30", "closes": "16:00"}],
        "sameAs": [c["instagram"], c["facebook"], c["pinterest"]],
    }
    extra = f'<script type="application/ld+json">{json.dumps(schema)}</script>'

    body = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="kicker">{icon("paw")}Boynton Beach pet salon &amp; spa</p>
      <h1>Fresh cuts. <span class="squiggle">Wagging tails.{SQUIGGLE}</span></h1>
      <p class="lede">A calm, clean salon where your dog or cat gets the full star treatment. Spa baths, breed-standard styling and a whole lot of patience, right on S. Military Trail.</p>
      <div class="btn-row">
        <a class="btn btn-pink" href="book.html">{icon("paw")}Fetch my appointment</a>
        <a class="btn" href="services.html">See services &amp; prices</a>
      </div>
      <div class="hero-meta">
        <span class="status" data-open-status><span class="status-dot"></span><span class="status-text">{c["hours_short"]}</span></span>
        <span><span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> {c["google_rating"]} on Google</span>
        <span>{icon("cat")}Dogs and cats</span>
      </div>
    </div>
    <div class="hero-art">
      <div class="hero-blob" aria-hidden="true"></div>
      <span class="hero-sticker s1" aria-hidden="true">spa day!</span>
      <span class="hero-sticker s2" aria-hidden="true">good boy approved</span>
      {HERO_DOG}
    </div>
  </div>
  <div class="paw-trail" aria-hidden="true">{paws}</div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}{mq}</div></div>

<section class="section" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="section-head center">
      <p class="hand">the menu</p>
      <h2 id="svc-title">Bath time, but make it fancy.</h2>
      <p class="lede">Clear starting prices right here, no phone tag required. Prices go by size, so pick yours on the services page.</p>
    </div>
    <div class="tags">{tags}</div>
    <div class="btn-row" style="justify-content:center;margin-top:40px">
      <a class="btn btn-mint" href="services.html">All services, add-ons and sizes {icon("arrow")}</a>
    </div>
  </div>
</section>

<section class="section" style="background:var(--bubble-2);border-block:var(--stroke) solid var(--line)" aria-labelledby="how-title">
  <div class="wrap">
    <div class="section-head center">
      <p class="hand">easy peasy</p>
      <h2 id="how-title">How a visit goes</h2>
    </div>
    <ol class="steps">{steps_html}</ol>
  </div>
</section>

<section class="section" aria-labelledby="why-title">
  <div class="wrap split">
    <div class="reveal">
      <div class="art-card mint">
        {pet_face("#FFFFFF", "#F2F2F2", acc="crown", label="A fluffy white dog wearing a little gold crown", extra_cls="face-float")}
        <p class="note">Treated like family. Spoiled like royalty.</p>
      </div>
    </div>
    <div>
      <p class="hand">why pets love us</p>
      <h2 id="why-title">Every pet is the star of the show</h2>
      <p class="lede">Our groomers take the time to learn each pet's needs, personality and preferences, so every visit feels personal and stress-free.</p>
      <ul class="perks">{perks_html}</ul>
    </div>
  </div>
</section>

<section class="section-tight" aria-labelledby="cats-title">
  <div class="wrap split flip">
    <div class="reveal">
      <div class="art-card pink">
        {pet_face("#D9D4CC", "#BDB5A8", kind="cat", acc="bow", label="A cat with a pink bow, looking pleased with itself", extra_cls="face-float")}
        <p class="note">Purr-fessionally groomed.</p>
      </div>
    </div>
    <div>
      <p class="hand">psst, cat people</p>
      <h2 id="cats-title">Cats too. Yes, really.</h2>
      <p class="lede">Baths, lion cuts, comb-outs and nail trims for cats, done gently and at their pace. Because your cat deserves a spa day too (even if they won't admit it).</p>
      <a class="btn btn-sun" href="cats.html">{icon("cat")}See cat grooming</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="rev-title">
  <div class="wrap">
    <div class="section-head center">
      <p class="hand">tail-wagging reviews</p>
      <h2 id="rev-title">Pet parents say it best</h2>
    </div>
    {quotes_block()}
    <div class="btn-row" style="justify-content:center;margin-top:24px"><a class="text-link" href="reviews.html">Read more reviews</a></div>
  </div>
</section>

{visit_block()}
{cta_band()}'''
    return page("index.html", "Dog & Cat Grooming in Boynton Beach, FL | Pets of Perfection",
                "Luxury dog and cat grooming in Boynton Beach. Spa baths, breed-standard cuts, hand-stripping and nail trims. See prices and book online.",
                body, active="", extra_head=extra)


def build_services():
    sizes = "".join(f'''<div class="size-opt">
  <input type="radio" name="dog-size" id="size-{k}" value="{k}"{" checked" if k == "s" else ""}>
  <label for="size-{k}"><span class="size-dog">{pet_face("#F4C89A", "#C98B5B", width=w, sparkles=False)}</span><strong>{name}</strong><span>{rng}</span></label>
</div>''' for k, name, rng, w in SIZES)
    tags = "".join(tag_dog(s, delay=f"d{i % 3}") for i, s in enumerate(DOG_SERVICES))
    addons = "".join(f'<li><span>{n}</span><span class="dots" aria-hidden="true"></span><b>{p}</b></li>' for n, p in ADDONS)
    deco = f'<div class="deco">{pet_face("#E8B77E", "#C98B5B", acc="bandana")}</div>'
    body = f'''{page_hero("Services &amp; prices, no phone tag.", "Pick your pup's size and every price on the page updates. Want something not listed? Ask us, we love a custom request.", "Services", "bubble", deco)}

<section class="section" aria-labelledby="dogs-title">
  <div class="wrap">
    <h2 id="dogs-title" class="sr-only">Dog grooming services</h2>
    <fieldset class="size-picker">
      <legend>Who's getting groomed?</legend>
      <div class="size-options">{sizes}</div>
    </fieldset>
    <div class="tags">{tags}</div>
    <div class="price-note">{icon("alert")}<span>These are starting prices. The final price depends on coat condition, matting and how wiggly things get. We'll always confirm with you before we start.</span></div>
  </div>
</section>

<section class="section-tight" aria-labelledby="addons-title">
  <div class="wrap">
    <div class="menu-board reveal">
      <p class="hand" style="color:var(--mint)">little extras</p>
      <h3 id="addons-title" style="font-size:clamp(1.6rem,3vw,2.2rem)">Add-ons for any visit</h3>
      <ul class="menu-list">{addons}</ul>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="cat-tease">
  <div class="wrap split">
    <div class="reveal"><div class="art-card sun">{pet_face("#F2A65A", "#E08A3C", kind="cat", acc="bow", label="An orange cat with a pink bow", extra_cls="face-float")}<p class="note">Cat grooming lives on its own page.</p></div></div>
    <div>
      <p class="hand">meow</p>
      <h2 id="cat-tease">Grooming a cat?</h2>
      <p class="lede">Cat baths, lion cuts and comb-outs have their own menu and their own (very calm) approach.</p>
      <a class="btn btn-sun" href="cats.html">{icon("cat")}Cat services</a>
    </div>
  </div>
</section>

{cta_band("Know what you want? Let's book it.", "Pick a day Tuesday to Saturday and we'll text to confirm.")}'''
    return page("services.html", "Dog Grooming Services & Prices | Pets of Perfection, Boynton Beach",
                "Full grooms, spa baths, hand-stripping, puppy grooms and de-shedding in Boynton Beach, with starting prices by dog size.",
                body, active="services.html")


def build_cats():
    tags = "".join(tag_cat(s, delay=f"d{i % 3}") for i, s in enumerate(CAT_SERVICES))
    perks = [
        ("leaf", "At their pace", "No rushing, no wrestling. Cats get an unhurried appointment with quiet breaks when they need them."),
        ("shield", "Gentle handling", "Soft hands, cat-safe products and low-heat drying keep things comfortable."),
        ("chat", "We'll check in", "If your cat tells us they're done for the day, we listen and call you before going further."),
        ("sparkle", "Matts, meet your match", "Long-haired and matted coats are our specialty. Lion cuts give a fresh start."),
    ]
    perks_html = "".join(f'<li class="perk">{icon(ic)}<h3>{t}</h3><p>{d}</p></li>' for ic, t, d in perks)
    deco = f'<div class="deco">{pet_face("#3A3A44", "#2A2A33", kind="cat", acc="bow")}</div>'
    body = f'''{page_hero("Cats welcome. We speak fluent hiss.", "Baths, lion cuts, comb-outs and nail trims for cats of every attitude. Calm, careful and never rushed.", "Cats", "pink", deco)}

<section class="section" aria-labelledby="cat-svc">
  <div class="wrap">
    <div class="section-head"><p class="hand">the cat menu</p><h2 id="cat-svc">Cat grooming services</h2></div>
    <div class="tags">{tags}</div>
    <div class="price-note">{icon("alert")}<span>Prices are a starting point. Heavily matted coats may need extra time, and we'll always talk to you first.</span></div>
  </div>
</section>

<section class="section" style="background:var(--mint-2);border-block:var(--stroke) solid var(--line)" aria-labelledby="calm-title">
  <div class="wrap split">
    <div>
      <p class="hand">keeping kitty calm</p>
      <h2 id="calm-title">A grooming visit your cat might (almost) enjoy</h2>
      <ul class="perks">{perks_html}</ul>
    </div>
    <div class="reveal"><div class="art-card">{pet_face("#D9D4CC", "#BDB5A8", kind="cat", acc="crown", label="A grey cat wearing a gold crown", extra_cls="face-float")}<p class="note">Royalty, obviously.</p></div></div>
  </div>
</section>

{cta_band("Book your cat's spa day.", "Pick a service and a day. We'll text to confirm.")}'''
    return page("cats.html", "Cat Grooming in Boynton Beach | Pets of Perfection",
                "Gentle cat grooming in Boynton Beach: cat baths, lion cuts, comb-outs, de-matting and nail trims.",
                body, active="cats.html")


def build_about():
    vals = [
        ("heart", "Kindness and respect", "Every pet is treated with patience and care, the way we'd want our own treated."),
        ("leaf", "Compassionate care", "Driven by a love for animals, we keep every visit positive and stress-free."),
        ("book", "Always learning", "Ongoing education in pet styling keeps us sharp on technique and safety."),
        ("shield", "Safety first", "Clean tools, a clean salon and high safety standards on every single groom."),
    ]
    vals_html = "".join(f'<li class="perk">{icon(ic)}<h3>{t}</h3><p>{d}</p></li>' for ic, t, d in vals)
    deco = f'<div class="deco">{pet_face("#FFFFFF", "#EDEDED", ears="point", acc="bandana")}</div>'
    body = f'''{page_hero("A luxury pet spa with a soft spot for every pet.", "Pets of Perfection is a pet salon, spa and boutique in Boynton Beach where the dogs (and cats) are the stars of the show.", "About", "mint", deco)}

<section class="section" aria-labelledby="story-title">
  <div class="wrap split">
    <div>
      <p class="hand">our story</p>
      <h2 id="story-title">A sanctuary for pets and the people who love them</h2>
      <p>The moment you step through our door, you'll feel it: a warm, welcoming salon built around one idea. Every pet owner deserves to know their pet is cared for with love.</p>
      <p>Our highly trained groomers have a meticulous eye for detail and a deep understanding of breed standards. From the precise scissoring of a Poodle to the intricate hand-stripping of a Terrier, no detail is overlooked.</p>
      <p>Beyond the cut, we offer luxurious baths with high-quality shampoos and conditioners, nail trims and teeth brushing, so your pet not only looks their best but feels their best too.</p>
      <p>Many of our clients have been bringing their pets to us for years. That trust is the part we're proudest of.</p>
    </div>
    <div class="reveal"><div class="art-card bubble">{pet_face("#3B3B3B", "#2A2A2A", ears="flop", acc="bow", label="A black dog with a pink bow", extra_cls="face-float")}<p class="note">Every pet is family here.</p></div></div>
  </div>
</section>

<section class="section" style="background:var(--sun-2);border-block:var(--stroke) solid var(--line)" aria-labelledby="values-title">
  <div class="wrap">
    <div class="section-head center"><p class="hand">what we believe</p><h2 id="values-title">The promise behind every groom</h2></div>
    <ul class="perks" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">{vals_html}</ul>
  </div>
</section>

<section class="section-tight" aria-labelledby="boutique-title">
  <div class="wrap split flip">
    <div class="reveal"><div class="art-card pink" style="aspect-ratio:4/3">{pet_face("#F4C89A", "#C98B5B", acc="crown", label="A golden pup in a crown")}</div></div>
    <div>
      <p class="hand">treat yourself (and them)</p>
      <h2 id="boutique-title">Stop by the boutique</h2>
      <p class="lede">Pick up quality shampoos, treats and accessories on your way out, hand-picked by the people who groom your pet.</p>
      <a class="btn" href="book.html">{icon("paw")}Book a visit</a>
    </div>
  </div>
</section>

{visit_block("Visit the salon")}'''
    return page("about.html", "About Pets of Perfection | Luxury Pet Spa in Boynton Beach",
                "A luxury pet salon, spa and boutique in Boynton Beach with skilled, caring groomers and breed-standard expertise.",
                body, active="about.html")


GALLERY = [
    dict(breed="Shih Tzu", svc="Teddy bear face and full groom", fur="#F3E3C8", ear="#D9B98C", acc="bow", ears="flop", kind="dog", cat="cuts"),
    dict(breed="Goldendoodle", svc="Full groom, fluffy finish", fur="#E8B77E", ear="#C98B5B", acc="bandana", ears="flop", kind="dog", cat="cuts"),
    dict(breed="West Highland Terrier", svc="Hand-strip and shaping", fur="#FFFFFF", ear="#F1F1F1", acc="bandana", ears="point", kind="dog", cat="cuts"),
    dict(breed="Pomeranian", svc="Spa bath and blow-out", fur="#F2A65A", ear="#E08A3C", acc="bow", ears="point", kind="dog", cat="spa"),
    dict(breed="Chocolate Lab", svc="De-shed treatment", fur="#8B5A3C", ear="#6E4329", acc="bandana", ears="flop", kind="dog", cat="spa"),
    dict(breed="Persian cat", svc="Lion cut and comb-out", fur="#D9D4CC", ear="#BDB5A8", acc="bow", ears="point", kind="cat", cat="cats"),
]


def build_gallery():
    cards = []
    for i, g in enumerate(GALLERY):
        before = pet_face(g["fur"], g["ear"], messy=True, kind=g["kind"], ears=g["ears"])
        after = pet_face(g["fur"], g["ear"], acc=g["acc"], kind=g["kind"], ears=g["ears"])
        cards.append(f'''<article class="ba-card reveal d{i % 3}" data-cat="{g["cat"]}">
  <div class="ba">
    <div class="ba-img ba-after" style="background:var(--mint-2)">{after}</div>
    <div class="ba-img ba-before" style="background:#ECE6DC">{before}</div>
    <span class="ba-label l">Before</span><span class="ba-label r">After</span>
    <input type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after: {g["breed"]}">
    <span class="ba-handle" aria-hidden="true"></span>
  </div>
  <div class="ba-meta"><h3>{g["breed"]}</h3><p>{g["svc"]}</p></div>
</article>''')
    c = CONFIG
    body = f'''{page_hero("Glow-ups, one wag at a time.", "Drag the slider on any card to see the before and after. Swipe on your phone, it works there too.", "Gallery", "sun")}

<section class="section" aria-labelledby="gal-title">
  <div class="wrap">
    <h2 id="gal-title" class="sr-only">Before and after grooms</h2>
    <div class="chips" role="group" aria-label="Filter grooms">
      <button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>
      <button class="chip" type="button" data-filter="cuts" aria-pressed="false">Haircuts</button>
      <button class="chip" type="button" data-filter="spa" aria-pressed="false">Spa &amp; de-shed</button>
      <button class="chip" type="button" data-filter="cats" aria-pressed="false">Cats</button>
    </div>
    <p id="gallery-live" class="sr-only" aria-live="polite"></p>
    <div class="gallery">{"".join(cards)}</div>
    <div class="insta-band reveal">
      <div><p class="hand">fresh from the salon</p><h3>Follow {c["instagram_handle"]} for daily glow-ups</h3></div>
      <a class="btn" href="{c["instagram"]}" target="_blank" rel="noopener">{icon("instagram")}Open Instagram</a>
    </div>
  </div>
</section>

{cta_band("Ready for your pet's glow-up?")}'''
    return page("gallery.html", "Grooming Gallery: Before & After | Pets of Perfection",
                "Before and after dog and cat grooms from Pets of Perfection in Boynton Beach.",
                body, active="gallery.html")


def build_reviews():
    c = CONFIG
    body = f'''{page_hero("The reviews are in. Tails are wagging.", "Real words from real pet parents around Boynton Beach.", "Reviews", "bubble")}

<section class="section" aria-labelledby="rv-title">
  <div class="wrap">
    <h2 id="rv-title" class="sr-only">Customer reviews</h2>
    <div class="rating-card reveal">
      <div class="rating-big">{c["google_rating"]}</div>
      <div>
        <div class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <strong>Rated {c["google_rating"]} out of 5 on Google</strong>
      </div>
      <div class="btn-row">
        <a class="btn btn-pink" href="{c["maps_link"]}" target="_blank" rel="noopener">{icon("star")}Read &amp; leave a review</a>
      </div>
    </div>
    {quotes_block()}
  </div>
</section>

{cta_band("Join the regulars.", "Book your first visit and see what the fuss is about.")}'''
    return page("reviews.html", "Reviews | Pets of Perfection, Boynton Beach Pet Grooming",
                "What pet parents say about Pets of Perfection, rated 4.5 on Google.",
                body, active="reviews.html")


FAQS = [
    ("How often should my dog be groomed?",
     "Most dogs do best with a full groom every 4 to 8 weeks, depending on coat type. Doodles, Poodles and long coats lean toward every 4 to 6 weeks. Short coats can stretch longer with a spa bath in between. We're happy to suggest a schedule for your pet."),
    ("How long does an appointment take?",
     "Plan on a few hours for a full groom. Timing depends on size, coat and how your pet is feeling that day. We'll text you as soon as they're ready, so you're never left guessing."),
    ("What do you need before the first visit?",
     "Please make sure vaccinations, including rabies, are current and bring proof on your first visit. Tell us about any health issues, allergies or sensitive spots so we can plan around them."),
    ("My dog is matted. Can you help?",
     "Yes. Light matting can often be brushed out. Heavy matting is kinder to shave down and start fresh, because brushing out tight mats can hurt. We'll always talk it through with you first."),
    ("Do you groom cats?",
     "We do! Cat baths, lion cuts, comb-outs and nail trims. See the <a class=\"text-link\" href=\"cats.html\">cat page</a> for details."),
    ("Do you do hand-stripping?",
     "Yes. Hand-stripping keeps wire coats like Terriers and Schnauzers crisp and true to breed standard. It takes longer than clipping, so let us know when you book."),
    ("What are your hours?",
     "Tuesday to Saturday, 8:30 AM to 4:00 PM. Closed Sunday and Monday. Need a later pickup? Just ask, hours can be extended on request."),
    ("Will you text me?",
     "If you opt in, we text appointment reminders and a heads-up when your pet is ready for pickup. Reply STOP anytime to opt out. Details are in our <a class=\"text-link\" href=\"policies.html\">privacy &amp; SMS policy</a>."),
]


def build_faq():
    items = "".join(f'''<details class="reveal">
  <summary>{q}<span class="plus" aria-hidden="true">{icon("plus")}</span></summary>
  <div class="answer"><p>{a}</p></div>
</details>''' for q, a in FAQS)
    body = f'''{page_hero("Questions? We've got answers (and treats).", "Everything pet parents usually ask before their first visit.", "FAQ", "sun")}
<section class="section" aria-label="Frequently asked questions">
  <div class="wrap"><div class="faq">{items}</div>
  <p style="margin-top:32px;font-weight:700">Still curious? Call or text <a class="text-link" href="tel:{CONFIG["phone_tel"]}">{CONFIG["phone"]}</a>.</p></div>
</section>
{cta_band()}'''
    return page("faq.html", "Grooming FAQ | Pets of Perfection, Boynton Beach",
                "Answers about grooming frequency, appointment times, vaccines, matting, cats and hours at Pets of Perfection.",
                body, active="faq.html")


def build_policies():
    c = CONFIG
    body = f'''{page_hero("Privacy &amp; SMS policy", "Plain-English answers about what we collect, why, and how texting works.", "Privacy &amp; SMS", "mint")}
<section class="section">
  <div class="wrap prose">
    <p class="callout">The short version: we use your info only to care for your pet and run your appointments. We never sell it, and we never share your phone number or text-message consent with anyone for their marketing.</p>
    <p><strong>Last updated:</strong> November 2026</p>

    <h2>1. Information we collect</h2>
    <p>We collect information you give us when you contact us, book an appointment or opt in to text messages:</p>
    <ul>
      <li><strong>Contact information:</strong> name, phone number, email address and physical address.</li>
      <li><strong>Pet information:</strong> your pet's name, breed, size, grooming history and any care notes you share.</li>
    </ul>

    <h2>2. How we use it</h2>
    <p>We use your information only to provide grooming and bathing services, manage your appointments and contact you about them, such as reminders and a note when your pet is ready for pickup.</p>

    <h2>3. How we share it</h2>
    <p>We do not sell, rent or trade your personal information. We use a small number of service providers, like our scheduling software and our text-message delivery provider, who process information only on our behalf and only to deliver our services to you.</p>

    <h2>4. Text messages (SMS)</h2>
    <p>By opting in to SMS on our website or in person, you agree to receive text messages from {c["name"]} about your appointments and conversations with us. Message frequency varies. Message and data rates may apply. Reply <strong>HELP</strong> for help and <strong>STOP</strong> to opt out at any time.</p>
    <p>Your mobile number and SMS opt-in consent are never shared with third parties or affiliates for marketing or promotional purposes. Our text-message delivery provider receives your number only to send the messages you asked for.</p>

    <h2>5. Your choices</h2>
    <p>You can opt out of texts at any time by replying STOP. To update or delete your information, email <a class="text-link" href="mailto:{c["email"]}">{c["email"]}</a> or call us.</p>

    <h2>6. Contact us</h2>
    <ul>
      <li>Email: <a class="text-link" href="mailto:{c["email"]}">{c["email"]}</a></li>
      <li>Phone: <a class="text-link" href="tel:{c["phone_tel"]}">{c["phone"]}</a></li>
      <li>Address: {addr_line()}</li>
    </ul>
  </div>
</section>'''
    return page("policies.html", "Privacy & SMS Policy | Pets of Perfection",
                "How Pets of Perfection collects, uses and protects your information, and how appointment text messages work.",
                body, active="")


def build_book():
    c = CONFIG
    dog_opts = [(s["id"], s["name"]) for s in DOG_SERVICES] + [("nails", "Nail trim only"), ("teeth", "Teeth brushing")]
    cat_opts = [(s["id"], s["name"]) for s in CAT_SERVICES]

    def picks(opts, prefix):
        return "".join(f'<div class="pick"><input type="checkbox" name="services" id="{prefix}-{v}" value="{v}" data-label="{lbl}"><label for="{prefix}-{v}">{lbl}</label></div>'
                       for v, lbl in opts)

    size_opts = "".join(f'<option value="{n} ({r})">{n} ({r})</option>' for _, n, r, _ in SIZES)
    err = lambda n: f'<p class="error-msg" data-error-for="{n}" id="err-{n}">{icon("alert")}<span></span></p>'
    deco = f'<div class="deco">{pet_face("#F4C89A", "#C98B5B", acc="bow")}</div>'
    body = f'''{page_hero("Let's get your pet on the books.", "Takes about a minute. Send a request and we'll text or call to lock in the exact time.", "Book", "pink", deco)}

<section class="section">
  <div class="wrap book-grid">
    <div>
      <form id="booking-form" class="form-card" novalidate action="#" method="post">
        <input type="hidden" name="_subject" value="New grooming request from the website">
        <div style="position:absolute;left:-9999px" aria-hidden="true"><label for="_gotcha">Leave this empty</label><input type="text" name="_gotcha" id="_gotcha" tabindex="-1" autocomplete="off"></div>
        <div class="form-alert" role="alert"></div>

        <fieldset class="form-step">
          <legend><span class="n">1</span>About you</legend>
          <div class="fields">
            <div class="field"><label for="owner_name">Your name</label><input type="text" id="owner_name" name="owner_name" autocomplete="name" aria-describedby="err-owner_name">{err("owner_name")}</div>
            <div class="field"><label for="phone">Mobile number</label><input type="tel" id="phone" name="phone" autocomplete="tel" inputmode="tel" placeholder="561-555-0123" aria-describedby="hint-phone err-phone"><p class="hint" id="hint-phone">We'll text your confirmation here.</p>{err("phone")}</div>
            <div class="field full"><label for="email">Email <span class="opt">(optional)</span></label><input type="email" id="email" name="email" autocomplete="email" aria-describedby="err-email">{err("email")}</div>
          </div>
        </fieldset>

        <fieldset class="form-step">
          <legend><span class="n">2</span>About your pet</legend>
          <div class="fields">
            <div class="field"><label for="pet_name">Pet's name</label><input type="text" id="pet_name" name="pet_name" aria-describedby="err-pet_name">{err("pet_name")}</div>
            <div class="field"><label for="breed">Breed <span class="opt">(optional)</span></label><input type="text" id="breed" name="breed" placeholder="Doodle, Shih Tzu, mystery mix..."></div>
            <div class="field full">
              <span class="label" id="pet-type-label">Dog or cat?</span>
              <div class="pick-grid" role="radiogroup" aria-labelledby="pet-type-label" aria-describedby="err-pet_type">
                <div class="pick"><input type="radio" name="pet_type" id="type-dog" value="Dog"><label for="type-dog">{icon("dog")}Dog</label></div>
                <div class="pick"><input type="radio" name="pet_type" id="type-cat" value="Cat"><label for="type-cat">{icon("cat")}Cat</label></div>
              </div>
              {err("pet_type")}
            </div>
            <div class="field full" id="field-size"><label for="size">Size</label><select id="size" name="size" aria-describedby="err-size"><option value="">Choose a size</option>{size_opts}</select>{err("size")}</div>
          </div>
        </fieldset>

        <fieldset class="form-step">
          <legend><span class="n">3</span>Pick the pampering</legend>
          <p class="hint" style="margin:-8px 0 14px">Choose as many as you like.</p>
          <div class="pick-grid" id="dog-services" role="group" aria-label="Dog services" aria-describedby="err-services">{picks(dog_opts, "svc")}</div>
          <div class="pick-grid" id="cat-services" role="group" aria-label="Cat services" aria-describedby="err-services" hidden>{picks(cat_opts, "svc")}</div>
          {err("services")}
        </fieldset>

        <fieldset class="form-step">
          <legend><span class="n">4</span>Pick a time</legend>
          <div class="fields">
            <div class="field"><label for="date">Preferred day</label><input type="date" id="date" name="date" aria-describedby="hint-date err-date"><p class="hint" id="hint-date">We groom Tuesday to Saturday.</p>{err("date")}</div>
            <div class="field"><label for="time">Drop-off window</label><select id="time" name="time">
              <option>Morning, 8:30 to 10:00</option><option>Late morning, 10:00 to 12:00</option><option>Early afternoon, 12:00 to 2:00</option><option>No preference</option>
            </select></div>
            <div class="field full"><label for="notes">Anything we should know? <span class="opt">(optional)</span></label><textarea id="notes" name="notes" placeholder="Matting, nerves, a favorite treat, the haircut you have in mind..."></textarea></div>
          </div>
        </fieldset>

        <fieldset class="form-step">
          <legend><span class="n">5</span>Last bits</legend>
          <div style="display:grid;gap:16px">
            <div>
              <label class="check"><input type="checkbox" name="vaccines" id="vaccines" value="yes" aria-describedby="err-vaccines"><span>My pet's vaccinations, including rabies, are current.<small>Please bring proof on your first visit.</small></span></label>
              {err("vaccines")}
            </div>
            <label class="check"><input type="checkbox" name="sms_consent" value="yes"><span>Text me appointment reminders and a "ready for pickup" heads-up from {c["name"]}. <span class="opt">(optional)</span><small>Message frequency varies. Msg &amp; data rates may apply. Reply STOP to opt out, HELP for help. See our <a href="policies.html">privacy &amp; SMS policy</a>.</small></span></label>
          </div>
        </fieldset>

        <div class="submit-row">
          <button type="submit" class="btn btn-pink"><span class="spinner" aria-hidden="true"></span>{icon("paw", "paw-ico")}<span class="btn-label">Fetch my appointment</span></button>
          <p class="fine">This sends a request. We'll text or call to confirm the exact time.</p>
        </div>
      </form>

      <div id="booking-success" class="form-card success" aria-live="polite">
        {pet_face("#F4C89A", "#C98B5B", acc="crown", extra_cls="face")}
        <h2>Pawsome! We'll text you to confirm.</h2>
        <p class="lede" style="margin-inline:auto">Your request is in. Expect a text or call from us soon, usually the same day during business hours.</p>
        <div class="summary">
          <div>Pet: <span data-s-pet></span></div>
          <div>When: <span data-s-date></span></div>
          <div>Services: <span data-s-services></span></div>
        </div>
        <div class="btn-row" style="justify-content:center">
          <button type="button" class="btn btn-mint" id="book-another">{icon("plus")}Book another pet</button>
          <a class="btn" href="index.html">Back to home</a>
        </div>
      </div>
    </div>

    <aside class="side-card" aria-label="Salon info">
      <h3>Prefer to talk?</h3>
      <ul>
        <li>{icon("phone")}<span><a href="tel:{c["phone_tel"]}">{c["phone"]}</a><br>Call or text</span></li>
        <li>{icon("clock")}<span>{c["hours_short"]}<br><span style="opacity:.8">{c["hours_note"]}</span></span></li>
        <li>{icon("pin")}<span><a href="{c["maps_link"]}" target="_blank" rel="noopener">{addr_line()}</a></span></li>
        <li>{icon("mail")}<span><a href="mailto:{c["email"]}">{c["email"]}</a></span></li>
      </ul>
      <a class="btn btn-sun" href="tel:{c["phone_tel"]}">{icon("phone")}Call the salon</a>
    </aside>
  </div>
</section>'''
    return page("book.html", "Book a Grooming Appointment | Pets of Perfection, Boynton Beach",
                "Request a dog or cat grooming appointment at Pets of Perfection in Boynton Beach. Takes about a minute.",
                body, active="book.html")


def build_404():
    body = f'''<section class="lost"><div class="wrap">
  {pet_face("#F4C89A", "#C98B5B", messy=True, extra_cls="face")}
  <p class="hand">uh oh</p>
  <h1>This page ran off to chase a squirrel.</h1>
  <p class="lede" style="margin-inline:auto">Let's get you back on the leash.</p>
  <div class="btn-row" style="justify-content:center"><a class="btn btn-pink" href="index.html">{icon("paw")}Back to home</a><a class="btn" href="services.html">See services</a></div>
</div></section>'''
    return page("404.html", "Page not found | Pets of Perfection", "This page ran off to chase a squirrel.", body)


FAVICON = open(os.path.join(ROOT, "img", "logo-mark.svg"), encoding="utf-8").read()


def main():
    pages = {
        "index.html": build_home(),
        "services.html": build_services(),
        "cats.html": build_cats(),
        "about.html": build_about(),
        "gallery.html": build_gallery(),
        "reviews.html": build_reviews(),
        "faq.html": build_faq(),
        "policies.html": build_policies(),
        "book.html": build_book(),
        "404.html": build_404(),
    }
    os.makedirs(os.path.join(ROOT, "img"), exist_ok=True)
    for name, html_out in pages.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(html_out)
    with open(os.path.join(ROOT, "img", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON)
    print(f"Built {len(pages)} pages into {ROOT}")


if __name__ == "__main__":
    main()
