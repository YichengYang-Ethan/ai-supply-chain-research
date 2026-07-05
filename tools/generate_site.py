#!/usr/bin/env python3
"""Generate the "AI Supply Chain Research" website section for yichengyang-ethan.github.io.

Deterministic transform of the VERIFIED content JSONs -> static HTML (GSoC hub+subpage pattern),
scoped SemiAnalysis dark theme (#14101B / #F8A848 / Spectral), English only.

Compliance (enforced here, per SemiAnalysis T&C §4):
  - NO SemiAnalysis images are embedded anywhere.
  - Quotes render ONLY if they resolve to a source URL (properly sourced AND linked); else dropped.
  - Every sector page ends with linked sources; every page carries an independence disclaimer.

Usage: python3 gen_site.py [--site DIR]
"""
import json, os, re, sys, difflib

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
SITE = os.environ.get("SITE_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site_output"))


SIDS = ["01_accelerators","02_foundry","03_memory","04_packaging","05_equipment",
        "06_networking","07_datacenter_power","08_hyperscalers_econ","09_models_software","10_china_geopolitics"]
SLUG = {s: s.split("_",1)[0] + "-" + s.split("_",1)[1].replace("_","-") for s in SIDS}
PAGE = {s: f"ai-supply-chain-{SLUG[s]}" for s in SIDS}

def esc(t):
    if t is None: return ""
    return (str(t).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

# ---------- source-title -> URL mapping ----------
_LINKS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "source_links.json")))
def link_for(title):
    return _LINKS.get(str(title))

# ---------- shared page chrome ----------
DARK_CSS = """
<style>
/* scoped SemiAnalysis-inspired dark theme for this section only */
body{background:#14101B;color:#EDEBF0;font-family:'Spectral',Georgia,serif;}
nav{border-bottom:1px solid #34303A;}
nav .nav-name,nav .nav-links a{color:#B5B4B7!important;}
nav .nav-links a:hover,nav .nav-name:hover{color:#F8A848!important;opacity:1;}
header .label{color:#F8A848;font-family:'Inter',sans-serif;letter-spacing:.08em;text-transform:uppercase;font-size:13px;font-weight:600;}
h1{color:#EDEBF0;} h2{color:#F8A848;margin:36px 0 12px;font-size:24px;}
h3{color:#EDEBF0;margin:22px 0 8px;font-size:19px;}
p.meta,.muted{color:#B5B4B7;}
a{color:#F8A848;} a:hover{color:#FFC069;opacity:1;}
.card{background:#1B1722;border:1px solid #34303A;border-radius:8px;padding:20px 22px;margin:14px 0;}
.card-label{color:#F8A848;font-family:'Inter',sans-serif;font-size:12px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;margin-bottom:6px;}
.card-title{font-weight:600;font-size:19px;margin-bottom:6px;color:#EDEBF0;}
.card-desc{color:#C9C7CE;font-size:16.5px;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;} @media(max-width:640px){.grid2{grid-template-columns:1fr;}}
table{width:100%;border-collapse:collapse;font-size:15px;font-family:'Inter',sans-serif;}
table.wtab{table-layout:fixed;} table.wtab td:first-child{width:150px;font-weight:600;color:#EDEBF0;vertical-align:top;padding-top:10px;}
table.ktab{table-layout:fixed;} table.ktab th:nth-child(1),table.ktab td:nth-child(1){width:26%;} table.ktab th:nth-child(2),table.ktab td:nth-child(2){width:22%;} 
td{vertical-align:top;line-height:1.55;}
th{color:#F8A848;text-align:left;border-bottom:1px solid #56535B;padding:8px 10px;font-weight:600;cursor:pointer;user-select:none;}
td{border-bottom:1px solid #2B2832;padding:7px 10px;color:#D8D6DD;}
tr:hover td{background:#1B1722;}
.pos{color:#57C08A;} .neg{color:#E8756A;}
blockquote{border-left:3px solid #F8A848;background:#1B1722;margin:12px 0;padding:10px 16px;font-style:italic;color:#C9C7CE;font-size:16px;}
blockquote .attr{display:block;font-style:normal;font-size:13.5px;color:#8B8992;margin-top:6px;font-family:'Inter',sans-serif;}
.vc{display:flex;flex-direction:column;gap:0;margin:18px 0;}
.vc .stage{display:grid;grid-template-columns:210px 1fr;gap:14px;align-items:center;background:#1B1722;border:1px solid #F8A848;border-radius:8px;padding:10px 16px;}
.vc .stage b{color:#F8A848;font-family:'Inter',sans-serif;font-size:15px;}
.vc .stage span{color:#B5B4B7;font-size:14.5px;font-family:'Inter',sans-serif;}
.vc .arrow{color:#F79C2F;text-align:center;line-height:1.1;font-size:15px;margin:1px 0;}
.klist p{margin:0 0 12px;} .klist b{color:#F8A848;}
.thesis{margin:0 0 18px;} .thesis .tclaim{font-weight:600;color:#EDEBF0;font-size:17.5px;}
.thesis .trat{color:#C9C7CE;font-size:16px;margin-top:4px;}
.pill{display:inline-block;background:#221E29;border:1px solid #34303A;border-radius:20px;padding:2px 12px;margin:2px 4px 2px 0;font-family:'Inter',sans-serif;font-size:13.5px;color:#C9C7CE;}
.bars{font-family:'Inter',sans-serif;font-size:14px;margin:14px 0;}
.bars .row{display:grid;grid-template-columns:110px 1fr 70px;gap:10px;align-items:center;margin:6px 0;}
.bars .track{background:#221E29;border-radius:4px;height:16px;position:relative;}
.bars .fill{height:16px;border-radius:4px;position:absolute;top:0;}
.disclaimer{border-top:1px solid #34303A;margin-top:44px;padding-top:16px;font-size:13.5px;color:#8B8992;font-family:'Inter',sans-serif;}
.srcs{font-size:14.5px;color:#B5B4B7;} .srcs li{margin:3px 0;}
footer{border-top:none!important;color:#8B8992!important;}
.section-label{color:#F8A848!important;}
</style>"""

GA = ("<script async src=\"https://www.googletagmanager.com/gtag/js?id=G-2F41NJTYWW\"></script>\n"
      "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-2F41NJTYWW');</script>")

def page(title, desc, body, active=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{GA}
<title>{esc(title)} &mdash; Yicheng Yang</title>
<meta name="description" content="{esc(desc)}">
<link href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
{DARK_CSS}
</head>
<body>
<div class="container">
<nav>
  <a href="/" class="nav-name">Yicheng Yang</a>
  <div class="nav-links">
    <a href="/research">Research</a>
    <a href="/ai-supply-chain" class="active" style="color:#F8A848!important">AI Chain</a>
    <a href="/strategies">Strategies</a>
    <a href="/projects">Projects</a>
    <a href="/gsoc">GSoC</a>
    <a href="/about">About</a>
  </div>
</nav>
{body}
<div class="disclaimer">
<strong>Independence &amp; sourcing.</strong> This is independent analysis by Yicheng Yang, distilled from publicly accessible SemiAnalysis articles (free posts and free previews; no paywall circumvention) and verified against the underlying text. It is not affiliated with, endorsed by, or a substitute for <a href="https://semianalysis.com">SemiAnalysis</a> &mdash; subscribe there for the full research. All referenced claims are sourced and linked per SemiAnalysis's attribution terms. No SemiAnalysis images are reproduced. Nothing here is investment advice.
</div>
<footer style="padding:24px 0 40px;font-family:'Inter',sans-serif;font-size:13px;">&copy; 2026 Yicheng Yang</footer>
</div>
</body>
</html>"""

def quote_html(q):
    if not q or not q.get("text"): return ""
    url = link_for(q.get("source_title",""))
    if not url: return ""   # compliance: linked or dropped
    return (f"<blockquote>&ldquo;{esc(q['text'])}&rdquo;"
            f"<span class=\"attr\">&mdash; <a href=\"{url}\">{esc(q.get('source_title',''))}</a> ({esc(q.get('date',''))}), SemiAnalysis</span></blockquote>")

def sources_html(srcs):
    lis=[]
    for s in srcs:
        url = link_for(s.get("title",""))
        t = esc(s.get("title","")); d = esc(s.get("date",""))
        lis.append(f"<li><a href=\"{url}\">{t}</a> ({d})</li>" if url else f"<li>{t} ({d})</li>")
    return "<ul class=\"srcs\">" + "\n".join(lis) + "</ul>"

# ---------- sector page ----------
def sector_page(c):
    sid=c["sector_id"]
    b=[f"""<header>
  <div class="label">AI Supply Chain Research &middot; Sector {sid[:2]}</div>
  <h1>{esc(c['sector_name_en'])}</h1>
  <p class="meta">{esc(c.get('tagline_en',''))} &nbsp;&middot;&nbsp; <a href="/ai-supply-chain">&larr; back to the series</a></p>
</header>
<article>"""]
    # ---- AT A GLANCE (desk-note style: conclusions first) ----
    inv=c.get("investment",{})
    b.append("<div class=\"card\" style=\"margin-top:8px\"><div class=\"card-label\">At a glance</div><div class=\"grid2\">")
    def pillbox(lab, items, key):
        out=[f"<div><div style=\"font-family:Inter;font-size:13px;color:#F8A848;font-weight:600;margin-bottom:4px\">{lab}</div>"]
        for it in items: out.append(f"<span class=\"pill\">{esc(it.get(key,'') if key else it)}</span>")
        out.append("</div>"); return "".join(out)
    b.append(pillbox("Winners",[w.get("name","") for w in inv.get("winners",[])],None))
    b.append(pillbox("Bottlenecks",inv.get("bottlenecks",[]),"en"))
    b.append(pillbox("Risks",inv.get("risks",[]),"en"))
    b.append(pillbox("Catalysts",inv.get("catalysts",[]),"en"))
    b.append("</div></div>")
    b.append(f"<h2>Overview</h2><p>{esc(c.get('overview_en',''))}</p>")
    b.append("<h2>Positioning: Who Wins and Why</h2><table class=\"wtab\"><tbody>")
    for w in inv.get("winners",[]):
        b.append(f"<tr><td>{esc(w.get('name',''))}</td><td>{esc(w.get('why_en',''))}</td></tr>")
    b.append("</tbody></table>")
    b.append("<h2>Key Data</h2><table class=\"ktab\"><thead><tr><th>Metric</th><th>Value</th><th>Note</th></tr></thead><tbody>")
    for d in c.get("key_data",[]):
        b.append(f"<tr><td>{esc(d.get('metric_en',''))}</td><td style=\"color:#F8A848;font-weight:500\">{esc(d.get('value',''))}</td><td>{esc(d.get('note_en',''))}</td></tr>")
    b.append("</tbody></table>")
    b.append("<h2>Key Theses</h2>")
    for i,t in enumerate(c.get("theses",[]),1):
        b.append(f"<div class=\"thesis\"><div class=\"tclaim\">{i}. {esc(t.get('claim_en',''))}</div>"
                 f"<div class=\"trat\">{esc(t.get('rationale_en',''))}</div>{quote_html(t.get('quote'))}</div>")
    dd=c.get("deep_dives",[])
    if dd:
        b.append("<h2>Article Deep-Dives</h2>")
        for d in dd:
            url=link_for(d.get("article_title",""))
            ttl=f"<a href=\"{url}\">{esc(d.get('article_title',''))}</a>" if url else esc(d.get("article_title",""))
            b.append(f"<div class=\"card\"><div class=\"card-title\" style=\"font-size:17px\">{ttl} <span class=\"muted\" style=\"font-size:13.5px\">({esc(d.get('date',''))})</span></div><div class=\"card-desc\">{esc(d.get('summary_en',''))}</div></div>")
    b.append("<h2>Reference: Value Chain</h2><div class=\"vc\">")
    vc=c.get("value_chain",[])
    for i,st in enumerate(vc):
        b.append(f"<div class=\"stage\"><b>{esc(st.get('stage_en',''))}</b><span><strong style=\"color:#EDEBF0\">{esc(st.get('players',''))}</strong> &mdash; {esc(st.get('role_en',''))}</span></div>")
        if i<len(vc)-1: b.append("<div class=\"arrow\">&#9660;</div>")
    b.append("</div>")
    b.append("<h2>Reference: Core Concepts</h2><div class=\"klist\">")
    for k in c.get("core_knowledge",[]):
        b.append(f"<p><b>{esc(k.get('term_en',''))}.</b> {esc(k.get('explain_en',''))}</p>")
    b.append("</div>")
    b.append("<h2>Open Questions</h2><ul>")
    for q in c.get("open_questions",[]): b.append(f"<li>{esc(q.get('en',''))}</li>")
    b.append("</ul>")
    b.append("<h2>Sources (SemiAnalysis)</h2>")
    b.append(sources_html(c.get("sources",[])))
    b.append("</article>")
    return page(c["sector_name_en"], c.get("tagline_en",""), "\n".join(b))

# ---------- hub ----------
def hub(syn, take, contents):
    b=[f"""<header>
  <div class="label">Independent research series</div>
  <h1>AI Supply Chain Research</h1>
  <p class="meta">{esc(syn.get('subtitle_en',''))}<br>Distilled and verified from 311 public SemiAnalysis articles (2020&ndash;2026) &middot; every claim sourced and linked &middot; includes an <a href="/ai-supply-chain-credibility">independent credibility audit</a> of the source itself.</p>
</header>
<article>"""]
    b.append(f"<div class=\"card\"><div class=\"card-label\">Abstract</div><div class=\"card-desc\">{esc(syn.get('abstract_en',''))}</div></div>")
    b.append("<h2>The Ten Sectors</h2><div class=\"grid2\">")
    for sid in SIDS:
        c=contents[sid]
        winners=", ".join(w.get("name","").split(" (")[0] for w in c.get("investment",{}).get("winners",[])[:3])
        b.append(f"<a class=\"card\" style=\"display:block\" href=\"/{PAGE[sid]}\"><div class=\"card-label\">Sector {sid[:2]} &middot; {len(c.get('theses',[]))} theses</div>"
                 f"<div class=\"card-title\" style=\"font-size:17px\">{esc(c['sector_name_en'])}</div>"
                 f"<div class=\"card-desc\" style=\"font-size:14.5px\">{esc(c.get('tagline_en',''))}<br><span style=\"color:#8B8992;font-family:Inter;font-size:13px\">Winners: {esc(winners)}</span></div></a>")
    b.append("</div>")
    b.append("<h2>Six Through-Lines</h2>")
    for i,t in enumerate(syn.get("throughlines",[]),1):
        b.append(f"<div class=\"thesis\"><div class=\"tclaim\">{i}. {esc(t.get('name_en',''))}</div><div class=\"trat\">{esc(t.get('body_en',''))}</div></div>")
    b.append(f"<h2>The Bottleneck Cascade</h2><p>{esc(take.get('cascade_en',''))}</p>")
    b.append("<h2>Chain-Wide Winners</h2><table class=\"wtab\"><tbody>")
    for w in take.get("winners",[]):
        b.append(f"<tr><td>{esc(w.get('name',''))}</td><td>{esc(w.get('why_en',''))}</td></tr>")
    b.append("</tbody></table>")
    b.append("""<h2>How Reliable Is the Source?</h2>
<div class="card"><div class="card-label">Credibility audit</div>
<div class="card-desc">Before trusting a single source this much, I audited it: an independent event study of 664 stance-bearing company mentions across 119 tickers, measuring what happened after SemiAnalysis praised or panned a name. Verdict: the narratives are remarkably right, the stock picks are not. <a href="/ai-supply-chain-credibility">Read the audit &rarr;</a></div></div>
<h2>Watchlist</h2><div>""")
    for w in take.get("watchlist",[]): b.append(f"<span class=\"pill\">{esc(w.get('en',''))}</span>")
    b.append("</div></article>")
    return page("AI Supply Chain Research", "Ten-sector, source-verified research series on the AI compute build-out, with an independent credibility audit of SemiAnalysis.", "\n".join(b))

# ---------- credibility page ----------
def credibility(app, data):
    h=data["head"]; pct=lambda x: f"{100*x:+.1f}%"
    def bar_rows(pairs, maxabs):
        rows=[]
        for lab,val in pairs:
            w=min(100, abs(val)/maxabs*100); col="#57C08A" if val>=0 else "#E8756A"
            side=f"left:50%;width:{w/2}%" if val>=0 else f"right:50%;width:{w/2}%"
            rows.append(f"<div class=\"row\"><div>{lab}</div><div class=\"track\"><div class=\"fill\" style=\"{side};background:{col}\"></div></div><div style=\"text-align:right;color:{col}\">{pct(val)}</div></div>")
        return "<div class=\"bars\">"+ "".join(rows) +"</div>"
    def score_table(tid, rows):
        trs=[]
        for r in rows:
            def cell(v):
                if v is None or v!=v: return "<td>&ndash;</td>"
                cls="pos" if v>=0 else "neg"
                return f"<td class=\"{cls}\" data-v=\"{v}\">{pct(v)}</td>"
            trs.append(f"<tr><td style=\"font-weight:600;color:#EDEBF0\">{esc(r['ticker'])}</td><td data-v=\"{r['n']}\">{r['n']}</td>{cell(r['m1'])}{cell(r['y1'])}{cell(r['y3'])}</tr>")
        return (f"<table class=\"sortable\" id=\"{tid}\"><thead><tr><th>Ticker</th><th>N</th><th>1M</th><th>1Y</th><th>3Y</th></tr></thead>"
                f"<tbody>{''.join(trs)}</tbody></table><p class=\"muted\" style=\"font-size:13.5px;font-family:Inter\">Click a column header to sort. Excess returns vs SMH, equal-weight by name, geometric, from publication date.</p>")
    b=[f"""<header>
  <div class="label">AI Supply Chain Research &middot; Credibility Audit</div>
  <h1>How Reliable Is SemiAnalysis?</h1>
  <p class="meta">An independent event study of what happens after the most influential newsletter in AI hardware praises or pans a stock. &nbsp;<a href="/ai-supply-chain">&larr; back to the series</a></p>
</header>
<article>
<p>{esc(app['intro_en'])}</p>
<h2>Key Findings</h2>"""]
    for i,f in enumerate(app["findings"],1):
        b.append(f"<div class=\"thesis\"><div class=\"tclaim\">{i}.</div><div class=\"trat\">{esc(f['en'])}</div></div>")
    b.append("<h2>Post-Coverage Drift at a Glance</h2>")
    b.append(bar_rows([("Bullish 1M",h['bull_1M']['mean']),("Bullish 1Y",h['bull_1Y']['mean']),("Bullish 3Y",h['bull_3Y']['mean']),
                       ("Bearish 1M",h['bear_1M']['mean']),("Bearish 1Y",h['bear_1Y']['mean']),("Bearish 3Y",h['bear_3Y']['mean'])], 0.30))
    b.append("<p class=\"muted\" style=\"font-family:Inter;font-size:14px\">Bars show mean excess return vs SMH after coverage (equal-weight by name). For bearish coverage, negative = the call was right.</p>")
    b.append(f"<h2>Bullish Scorecard</h2><p class=\"muted\">{esc(app['bull_note_en'])}</p>")
    b.append(score_table("bulls", data["bull_table"]))
    b.append(f"<h2>Bearish Scorecard</h2><p class=\"muted\">{esc(app['bear_note_en'])}</p>")
    b.append(score_table("bears", data["bear_table"]))
    b.append(f"""<h2>How to Use the Source</h2><p>{esc(app['usage_en'])}</p>
<h2>Methodology &amp; Limits</h2>
<p class="muted" style="font-size:15.5px">{esc(app['caveat_en'])}</p>
<ul class="muted" style="font-size:15.5px">
<li><strong>Design.</strong> Classic analyst-coverage event study (Womack 1996 lineage): buy-and-hold geometric excess returns vs a sector benchmark (Barber &amp; Lyon 1997), equal-weight by name with ticker clustering, pre-IPO look-ahead removed, delistings settled at last price.</li>
<li><strong>Fairness.</strong> SemiAnalysis explicitly states it does not provide investment advice, ratings, or price targets &mdash; scoring it as a stock-picker is my frame, not theirs. The audit measures information content, not their stated product.</li>
<li><strong>Limits, stated plainly.</strong> No calendar-time portfolio check (long-horizon t-stats are optimistic under overlapping windows; the 3Y direction is robust, its precision is not). The single positive result (1M spread, t=2.33) does not survive strict multiple-testing correction. Stance extraction is LLM-based on available text without a human-labeled validation sample. Benchmark is a cap-weighted sector ETF rather than characteristics-matched portfolios.</li>
</ul>
<script>
document.querySelectorAll('table.sortable th').forEach(function(th){{
  th.addEventListener('click',function(){{
    var t=th.closest('table'),tb=t.querySelector('tbody'),i=Array.prototype.indexOf.call(th.parentNode.children,th);
    var rows=Array.prototype.slice.call(tb.querySelectorAll('tr'));
    var dir=th.dataset.dir==='asc'?-1:1; th.dataset.dir=dir===1?'asc':'desc';
    rows.sort(function(a,b){{
      var av=a.children[i].dataset.v, bv=b.children[i].dataset.v;
      if(av!==undefined&&bv!==undefined) return (parseFloat(av)-parseFloat(bv))*dir;
      return a.children[i].textContent.localeCompare(b.children[i].textContent)*dir;
    }});
    rows.forEach(function(r){{tb.appendChild(r);}});
  }});
}});
</script>
</article>""")
    return page("How Reliable Is SemiAnalysis?", "An independent event study of 664 stance-bearing company mentions across 119 tickers: what happens after SemiAnalysis praises or pans a stock.", "\n".join(b))

def main():
    site = SITE
    os.makedirs(site, exist_ok=True)
    contents = {sid: json.load(open(f"{BASE}/sectors/content_{sid}.json")) for sid in SIDS}
    syn  = json.load(open(f"{BASE}/synthesis/front_synthesis.json"))
    take = json.load(open(f"{BASE}/synthesis/front_takeaways.json"))
    app  = json.load(open(f"{BASE}/synthesis/appendix_credibility.json"))
    data = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audit", "appendix_data.json")))
    n=0
    open(f"{site}/ai-supply-chain.html","w").write(hub(syn,take,contents)); n+=1
    for sid in SIDS:
        open(f"{site}/{PAGE[sid]}.html","w").write(sector_page(contents[sid])); n+=1
    open(f"{site}/ai-supply-chain-credibility.html","w").write(credibility(app,data)); n+=1
    print(f"wrote {n} pages into {site}")
    # compliance self-check: no substackcdn/SA images anywhere
    bad=[]
    for f in os.listdir(site):
        if f.startswith("ai-supply-chain") and f.endswith(".html"):
            t=open(f"{site}/{f}").read()
            if "substackcdn" in t or re.search(r'<img[^>]+semianalysis',t,re.I): bad.append(f)
    print("compliance image-check:", "FAIL "+str(bad) if bad else "PASS (no SA images embedded)")

if __name__=="__main__": main()
