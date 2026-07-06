# AI Supply Chain Research

**A ten-sector, source-verified research series on the AI compute build-out — from accelerators to gigawatts — plus an independent credibility audit of the source it distills.**

📖 **Read it live:** [yichengyang-ethan.github.io/ai-supply-chain](https://yichengyang-ethan.github.io/ai-supply-chain) · ⚖️ **Credibility audit:** [How Reliable Is SemiAnalysis?](https://yichengyang-ethan.github.io/ai-supply-chain-credibility)

📕 **PDF (Public Edition):** [AI_Supply_Chain_Research_Complete_Public_Edition.pdf](AI_Supply_Chain_Research_Complete_Public_Edition.pdf) — the full 199-page book (English): an 11-module **Foundations Primer** (no background assumed), the panorama, ten sector deep-dives, and the credibility audit. Per-chapter linked sources.

🎓 **New to AI hardware?** Start with the primer: [live](https://yichengyang-ethan.github.io/ai-supply-chain-primer) · data in [`data/primer/`](data/primer/) — 11 textbook-style modules, **76/76 key numbers source-verified**, own-drawn diagrams (labeled), and attributed institutional images.

By [Yicheng Yang](https://yichengyang-ethan.github.io) · independent, not affiliated with SemiAnalysis · nothing here is investment advice.

---

## What this is

The AI build-out is one machine viewed through ten cross-sections: **accelerators, foundry, memory/HBM, advanced packaging, semi equipment, networking/optics, datacenter power, hyperscaler economics, models/software, and China/export controls**. This repo contains a structured, *verified* distillation of that machine from 311 public SemiAnalysis articles (2020–2026), organized for investment research:

- **~130 theses** across ten sectors — each a claim + rationale + attributed, linked quote
- **~170 quantified data points** — every number grep-verified against the underlying text
- **Per-sector positioning**: winners, bottlenecks, risks, catalysts
- **Six cross-sector through-lines** — the demand shock, the bottleneck relay, chip→rack→campus co-design, the value-capture war, the software moat, China's bifurcation

### Why trust it — the verification layer

This isn't a summary; it's an audited distillation:

| Check | Result |
|---|---|
| Quantitative claims verified against source text | **1,070 / 1,091 (98.1%)** — the 20 flagged were corrected or removed |
| Quotes verified verbatim (or ellipsis-stitched from verbatim fragments) | **131 / 131** after 3 corrections |
| Source images reproduced | **0** — every chart reference is a link, per the source's attribution terms |
| Every claim sourced and linked | ✅ ~190 article links |

## The credibility audit (the part you should read first)

Before trusting one source this much, I audited it: an independent event study of **664 stance-bearing company mentions across 119 tickers** extracted from the corpus, measuring excess returns vs. SMH after SemiAnalysis praised or panned a name (equal-weight by name, ticker-clustered, pre-IPO look-ahead removed, delistings settled).

**Findings** (full scorecards in [`audit/`](audit/)):

1. **The only significant leading signal lasts ~1 month** — bull-minus-bear spread **+3.9%** (Welch t = 2.33).
2. **Long horizons reverse**: the typical bullish name lags SMH by **−5.2% at 1Y** and **−27.2% at 3Y** (t = −4.49).
3. **Aggregate returns are a beta illusion** — excluding the five most-covered names (NVDA/TSM/AMD/GOOGL/AVGO), bullish 1Y excess is **−6.1%**.
4. **Bearish calls beat bullish ones**: panned names lag SMH **−10.7% at 1Y** (t = −2.90). INTC (panned 30×) and Samsung (15×) both played out.
5. **Right industry, wrong stock**: the memory-shortage / CoWoS / datacenter-power narratives were all right — the money still went to NVDA/TSM.

**Takeaway: treat the source as a microscope on mechanisms and bottlenecks, not a buy list.** That is exactly what this series distills. (Fairness note: SemiAnalysis explicitly states it does not provide investment advice or ratings — scoring it as a stock-picker is my frame, not theirs. Methodology limits are stated plainly in [`audit/README.md`](audit/README.md).)

## Repo layout

```
data/
  primer/           primer_XX.json — 11 Foundations modules (EN + ZH), every number sourced
  sectors/          content_XX.json — ten verified sector briefs (EN + ZH), the canonical data
  synthesis/        cross-sector through-lines, chain-wide investment map, audit narrative
  source_links.json title → SemiAnalysis URL map (~190 articles)
audit/
  bullish_scorecard.csv / bearish_scorecard.csv — per-name post-coverage excess returns
  headline_stats.json — aggregate results with t-stats
  README.md — methodology & limits
tools/
  generate_site.py — deterministic JSON → static-site generator (the live site is built from this)
```

## Reproduce the site

```bash
python3 tools/generate_site.py     # writes 12 static pages to ./site_output
```

No dependencies beyond the Python standard library. The generator enforces the compliance rules (no third-party images; quotes render only if resolvable to a source link).

## Method

1. **Corpus**: 311 publicly accessible SemiAnalysis articles (free posts + free previews; no paywall circumvention).
2. **Distillation**: parallel LLM agents read each sector's full bucket and emit structured briefs (theses, data, deep-dives) in both English and Chinese.
3. **Adversarial verification**: independent fact-checking agents grep every number and quote against the corpus; fabrications/distortions are corrected by prescription. Mechanical checks validate all quotes and link mappings.
4. **Credibility audit**: stance extraction (27 agents) → ticker resolution (incl. KRX/TWSE/TSE/HKEX) → event study vs. SMH with the debiasing steps above, after three adversarial audit rounds fixed eight methodological defects.

## License & attribution

- Code (`tools/`): MIT. Data files in `data/` and `audit/`: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- All references to SemiAnalysis research are quoted/excerpted with attribution and links, per their published attribution terms. This project is independent and unaffiliated; for the full research, [subscribe to SemiAnalysis](https://semianalysis.com).
