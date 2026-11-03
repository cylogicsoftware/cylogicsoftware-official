#!/usr/bin/env python3
"""Static site generator for the CYLOGIC SOFTWARE digital identity hub.

Reads locales/*.json and data/social-links.json and writes one fully
pre-rendered HTML page per language (index.html, en/, ru/, fa/) plus
sitemap.xml. No third-party dependencies (Python 3.8+).

Usage:  python3 scripts/build.py [output_dir]   (default: repository root)
"""
import html
import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ROOT

BASE_URL = "https://cylogicsoftware.github.io/cylogicsoftware-official/"
REPO_URL = "https://github.com/cylogicsoftware/cylogicsoftware-official"
LOGO = "https://www.cylogicsoftware.com/brand/logo-192.png"
LOGO_LARGE = "https://www.cylogicsoftware.com/brand/logo-512.png"
LANGS = ["tr", "en", "ru", "fa"]
CONTACT_PATH = {"tr": "/iletisim", "en": "/contact", "ru": "/contact", "fa": "/contact"}

TECH = {
    "frontend": ["React", "TypeScript", "Vite", "Tailwind CSS", "Three.js", "TanStack Query", "Zod", "PWA"],
    "data": ["PostgreSQL", "Supabase", "pgvector", "Local LLM", "RAG"],
    "infra": ["Docker", "Nginx", "Linux"],
}

# Generic line icons (original artwork, stroke-based)
ICONS = {
    "ai": '<path d="M9 3v2M15 3v2M9 19v2M15 19v2M3 9h2M3 15h2M19 9h2M19 15h2"/><rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9.5 15l1.6-6h1.8l1.6 6M10 13h4"/>',
    "erp": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 9v11M12 13h5M12 16h3"/>',
    "software": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
    "automation": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
    "it": '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01M11 6.5h6M11 17.5h6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0119 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "form": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.4-8 9-4.6-.6-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
}
POINT_ICONS = ["target", "shield", "layers"]


def icon(name, cls="ic"):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>'
            % (cls, ICONS[name]))


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return json.load(fh)


def brand_svg(rel_path):
    """Inline a Simple Icons SVG path (CC0) for performance and theming."""
    with open(os.path.join(ROOT, rel_path), encoding="utf-8") as fh:
        raw = fh.read()
    start = raw.index("<path")
    end = raw.index("</svg>")
    return ('<svg class="brand" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">%s</svg>'
            % raw[start:end])


e = html.escape


def page_url(loc):
    return BASE_URL + loc["path"]


def render(loc, locales, social):
    L = loc
    prefix = "../" if L["path"] else ""
    profiles = [p for p in social["profiles"] if p.get("verified")]
    main_site = L["mainSite"]
    contact_url = main_site + CONTACT_PATH[L["lang"]]
    nt = e(L["ui"]["newTab"])

    # --- head -----------------------------------------------------------
    alternates = "\n".join(
        '  <link rel="alternate" hreflang="%s" href="%s">' % (x["lang"], page_url(x)) for x in locales
    ) + '\n  <link rel="alternate" hreflang="x-default" href="%s">' % BASE_URL
    og_alt = "\n".join(
        '  <meta property="og:locale:alternate" content="%s">' % x["locale"] for x in locales if x is not L
    )
    org_ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": "https://www.cylogicsoftware.com/#organization",
        "name": "Cy Logic Software",
        "alternateName": "CYLOGIC SOFTWARE",
        "url": "https://www.cylogicsoftware.com/",
        "logo": LOGO_LARGE,
        "email": social["email"],
        "description": L["meta"]["description"],
        "address": {"@type": "PostalAddress", "addressLocality": "Gazimağusa (Famagusta)", "addressRegion": "Northern Cyprus"},
        "areaServed": ["Northern Cyprus", "Türkiye"],
        "knowsAbout": ["Artificial intelligence", "Enterprise resource planning", "Custom software development",
                       "Business process automation", "IT infrastructure", "Digital transformation"],
        "sameAs": [p["url"] for p in profiles],
    }
    page_ld = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "url": page_url(L),
        "name": L["meta"]["title"],
        "inLanguage": L["lang"],
        "about": {"@id": "https://www.cylogicsoftware.com/#organization"},
        "mainEntity": {"@id": "https://www.cylogicsoftware.com/#organization"},
    }
    ld = json.dumps([org_ld, page_ld], ensure_ascii=False, indent=2).replace("</", "<\\/")

    fonts = ("family=Inter:wght@400;500;600;700;800"
             + ("&family=Vazirmatn:wght@400;500;700;800" if L["dir"] == "rtl" else ""))

    # --- language switcher ------------------------------------------------
    lang_items = "\n".join(
        '          <li><a role="menuitem" href="%s%s" hreflang="%s" lang="%s"%s>'
        '<span class="lang-code">%s</span><span>%s</span></a></li>'
        % (prefix, x["path"] or "./", x["lang"], x["lang"],
           ' aria-current="page"' if x is L else "", x["short"], e(x["name"]))
        for x in locales
    ).replace('href=".././"', 'href="../"')

    nav = L["nav"]
    nav_links = "".join(
        '<li><a href="#%s">%s</a></li>' % (k, e(nav[k])) for k in ["about", "services", "tech", "social", "contact"]
    )

    # --- sections ----------------------------------------------------------
    badges = "".join('<li>%s</li>' % e(b) for b in L["hero"]["badges"])
    points = "".join(
        '<li class="point reveal">%s<div><h3>%s</h3><p>%s</p></div></li>'
        % (icon(POINT_ICONS[i]), e(p["title"]), e(p["text"])) for i, p in enumerate(L["about"]["points"])
    )
    services = "".join(
        '<article class="card service reveal" id="svc-%s"><div class="card-icon">%s</div><h3>%s</h3><p>%s</p><ul>%s</ul></article>'
        % (s["id"], icon(s["id"]), e(s["title"]), e(s["desc"]),
           "".join('<li>%s<span>%s</span></li>' % (icon("check", "ic-sm"), e(i)) for i in s["list"]))
        for s in L["services"]["items"]
    )
    tech = "".join(
        '<div class="tech-group reveal"><h3>%s</h3><ul class="chips">%s</ul></div>'
        % (e(L["tech"]["groups"][g]), "".join('<li translate="no">%s</li>' % e(t) for t in TECH[g]))
        for g in ["frontend", "data", "infra"]
    )
    socials = "".join(
        '<li><a class="card social-card reveal" href="%s" target="_blank" rel="noopener noreferrer me" '
        'aria-label="%s – %s (%s)"><span class="social-icon si-%s">%s</span>'
        '<span class="social-text"><strong>%s</strong><span translate="no" dir="ltr">%s</span></span>'
        '<span class="social-badge" title="%s">%s</span></a></li>'
        % (e(p["url"]), e(p["platform"]), e(L["social"]["visit"]), nt, p["id"], brand_svg(p["icon"]),
           e(p["platform"]), e(p["handle"]), e(L["social"]["verified"]), icon("check", "ic-sm"))
        for p in profiles
    )
    footer_social = "".join(
        '<li><a href="%s" target="_blank" rel="noopener noreferrer" aria-label="%s (%s)">%s</a></li>'
        % (e(p["url"]), e(p["platform"]), nt, brand_svg(p["icon"])) for p in profiles
    )
    year = date.today().year

    return f"""<!doctype html>
<html lang="{L['lang']}" dir="{L['dir']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(L['meta']['title'])}</title>
  <meta name="description" content="{e(L['meta']['description'])}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="author" content="Cy Logic Software">
  <meta name="theme-color" content="#050b1a">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="{page_url(L)}">
{alternates}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="CYLOGIC SOFTWARE">
  <meta property="og:title" content="{e(L['meta']['title'])}">
  <meta property="og:description" content="{e(L['meta']['description'])}">
  <meta property="og:url" content="{page_url(L)}">
  <meta property="og:image" content="{LOGO_LARGE}">
  <meta property="og:image:width" content="512">
  <meta property="og:image:height" content="512">
  <meta property="og:image:alt" content="{e(L['meta']['ogAlt'])}">
  <meta property="og:locale" content="{L['locale']}">
{og_alt}
  <meta name="twitter:card" content="summary">
  <meta name="twitter:site" content="@cylogicsoftware">
  <meta name="twitter:title" content="{e(L['meta']['title'])}">
  <meta name="twitter:description" content="{e(L['meta']['description'])}">
  <meta name="twitter:image" content="{LOGO_LARGE}">
  <meta name="twitter:image:alt" content="{e(L['meta']['ogAlt'])}">
  <link rel="icon" href="{LOGO}" type="image/png">
  <link rel="apple-touch-icon" href="{LOGO}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
  <link rel="preload" as="image" href="{LOGO}">
  <link rel="stylesheet" href="{prefix}assets/css/style.css">
  <script type="application/ld+json">
{ld}
  </script>
</head>
<body>
  <a class="skip" href="#main">{e(L['ui']['skip'])}</a>
  <header class="site-header" id="top">
    <nav class="nav container" aria-label="{e(L['ui']['menu'])}">
      <a class="logo" href="{prefix}{L['path'] or './'}" aria-label="CYLOGIC SOFTWARE">
        <img src="{LOGO}" width="40" height="40" alt="{e(L['meta']['ogAlt'])}">
        <span translate="no">CYLOGIC <b>SOFTWARE</b></span>
      </a>
      <ul class="nav-links" id="nav-links">{nav_links}</ul>
      <div class="nav-actions">
        <div class="lang">
          <button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="lang-menu" aria-label="{e(L['ui']['language'])}">
            {icon('globe')}<span>{L['short']}</span>
          </button>
          <ul class="lang-menu" id="lang-menu" role="menu" aria-label="{e(L['ui']['language'])}">
{lang_items}
          </ul>
        </div>
        <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="{e(L['ui']['menu'])}"><span></span><span></span><span></span></button>
      </div>
    </nav>
  </header>

  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-bg" aria-hidden="true"><span class="orb o1"></span><span class="orb o2"></span><span class="grid"></span></div>
      <div class="container hero-inner">
        <img class="hero-logo" src="{LOGO}" width="112" height="112" alt="{e(L['meta']['ogAlt'])}" fetchpriority="high">
        <p class="eyebrow">{e(L['hero']['eyebrow'])}</p>
        <h1 id="hero-title"><span class="brand-name" translate="no">CYLOGIC SOFTWARE</span><span class="hero-title">{e(L['hero']['title'])}</span></h1>
        <p class="lead">{e(L['hero']['lead'])}</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{main_site}" target="_blank" rel="noopener" aria-label="{e(L['hero']['cta'])} ({nt})">{e(L['hero']['cta'])}{icon('arrow', 'ic-sm flip')}</a>
          <a class="btn btn-ghost" href="#services">{e(L['hero']['cta2'])}</a>
        </div>
        <ul class="hero-badges">{badges}</ul>
      </div>
    </section>

    <section class="section" id="about" aria-labelledby="about-title">
      <div class="container about">
        <div class="reveal">
          <p class="kicker">01</p>
          <h2 id="about-title">{e(L['about']['title'])}</h2>
          <p class="section-lead">{e(L['about']['lead'])}</p>
          <p>{e(L['about']['p1'])}</p>
          <p>{e(L['about']['p2'])}</p>
        </div>
        <ul class="points">{points}</ul>
      </div>
    </section>

    <section class="section alt" id="services" aria-labelledby="services-title">
      <div class="container">
        <header class="section-head reveal">
          <p class="kicker">02</p>
          <h2 id="services-title">{e(L['services']['title'])}</h2>
          <p class="section-lead">{e(L['services']['lead'])}</p>
        </header>
        <div class="cards">{services}</div>
        <p class="center reveal"><a class="link-arrow" href="{main_site}" target="_blank" rel="noopener">{e(L['services']['more'])}{icon('arrow', 'ic-sm flip')}</a></p>
      </div>
    </section>

    <section class="section" id="tech" aria-labelledby="tech-title">
      <div class="container">
        <header class="section-head reveal">
          <p class="kicker">03</p>
          <h2 id="tech-title">{e(L['tech']['title'])}</h2>
          <p class="section-lead">{e(L['tech']['lead'])}</p>
        </header>
        <div class="tech">{tech}</div>
      </div>
    </section>

    <section class="section alt" id="social" aria-labelledby="social-title">
      <div class="container">
        <header class="section-head reveal">
          <p class="kicker">04</p>
          <h2 id="social-title">{e(L['social']['title'])}</h2>
          <p class="section-lead">{e(L['social']['lead'])}</p>
        </header>
        <ul class="socials">{socials}</ul>
      </div>
    </section>

    <section class="section" id="contact" aria-labelledby="contact-title">
      <div class="container">
        <header class="section-head reveal">
          <p class="kicker">05</p>
          <h2 id="contact-title">{e(L['contact']['title'])}</h2>
          <p class="section-lead">{e(L['contact']['lead'])}</p>
        </header>
        <div class="contact-grid">
          <a class="card contact-card reveal" href="{main_site}" target="_blank" rel="noopener">{icon('globe')}<span><small>{e(L['contact']['website'])}</small><strong dir="ltr">www.cylogicsoftware.com</strong></span></a>
          <a class="card contact-card reveal" href="mailto:{social['email']}">{icon('mail')}<span><small>{e(L['contact']['email'])}</small><strong dir="ltr">{social['email']}</strong></span></a>
          <a class="card contact-card reveal" href="{contact_url}" target="_blank" rel="noopener">{icon('form')}<span><small>{e(L['contact']['form'])}</small><strong>{e(L['contact']['formCta'])}</strong></span></a>
          <div class="card contact-card reveal">{icon('pin')}<span><small>{e(L['contact']['location'])}</small><strong>{e(L['contact']['locationValue'])}</strong></span></div>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <a class="logo" href="{main_site}" target="_blank" rel="noopener"><img src="{LOGO}" width="36" height="36" alt="{e(L['meta']['ogAlt'])}" loading="lazy"><span translate="no">CYLOGIC <b>SOFTWARE</b></span></a>
        <p>{e(L['footer']['tagline'])}</p>
        <p class="muted">{e(L['footer']['hub'])}</p>
      </div>
      <ul class="footer-social">{footer_social}</ul>
    </div>
    <div class="container footer-bottom">
      <p>© {year} <span translate="no">Cy Logic Software</span>. {e(L['footer']['rights'])}</p>
      <p><a href="https://www.cylogicsoftware.com/" target="_blank" rel="noopener" dir="ltr">www.cylogicsoftware.com</a> · <a href="{REPO_URL}" target="_blank" rel="noopener">{e(L['footer']['source'])}</a> · <a href="#top">{e(L['ui']['backToTop'])}</a></p>
    </div>
  </footer>
  <script src="{prefix}assets/js/main.js" defer></script>
</body>
</html>
"""


def main():
    locales = [load("locales/%s.json" % l) for l in LANGS]
    social = load("data/social-links.json")
    for loc in locales:
        target_dir = os.path.join(OUT, loc["path"])
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(render(loc, locales, social))
        print("built", os.path.join(loc["path"], "index.html"))

    today = date.today().isoformat()
    urls = []
    for loc in locales:
        alts = "".join(
            '\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (x["lang"], page_url(x)) for x in locales
        ) + '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % BASE_URL
        urls.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>%s\n  </url>" % (page_url(loc), today, alts))
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
               + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap)
    print("built sitemap.xml")


if __name__ == "__main__":
    main()
