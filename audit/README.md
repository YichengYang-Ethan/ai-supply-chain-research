# Credibility Audit — Methodology & Limits

An independent event study of SemiAnalysis coverage: what happens to a stock after the newsletter praises or pans it.

## Design

- **Extraction.** 27 parallel LLM agents read all 311 corpus articles and extract every stance-bearing company mention (bullish / bearish / mixed / neutral, with conviction and primary-subject flags). 812 raw targets → 664 single-stock events across 119 tickers (384 bullish / 168 bearish) after resolving names to tickers (incl. KRX `.KS`, TWSE `.TW`, TSE `.T`, HKEX `.HK`) and dropping private companies.
- **Returns.** Buy-and-hold geometric excess returns vs. the SMH semiconductor ETF (also computed vs. SOXX/QQQ/SPY and an equal-weight semi peer index), measured 1M/6M/1Y/3Y from publication date. Foreign listings converted to USD.
- **Debiasing** (fixes adopted after three adversarial audit rounds):
  - *Equal-weight by name, ticker-clustered* — event-weighting is a soft look-ahead (winners get covered repeatedly; NVDA appears 62×).
  - *Pre-IPO look-ahead removed* — mentions of ARM/CRWV/etc. before listing are excluded (publish→entry gap > 20 days).
  - *Delistings settled at last price* (acquisitions ≈ deal price; bankruptcies ≈ collapse) rather than dropped.
  - *Geometric excess* rather than arithmetic differences (avoids −161%/+245% artifacts at long horizons).

## Headline results (see `headline_stats.json`)

| Group | 1M | 1Y | 3Y |
|---|---|---|---|
| Bullish (n=78 names) | +2.0% (t=1.63) | −5.2% (t=−1.49) | **−27.2% (t=−4.49)** |
| Bearish (n=58 names) | −1.9% (t=−1.68) | **−10.7% (t=−2.90)** | −17.4% (t=−1.51) |
| Bull−bear spread (1M) | **+3.9% (Welch t=2.33)** | | |

Excluding the five most-covered names (NVDA, TSM, AMD, GOOGL, AVGO), bullish 1Y excess is −6.1%.

## Consistency with the literature

The design follows the analyst-recommendation event-study lineage (Womack 1996; Barber & Lyon 1997 for benchmark-adjusted buy-and-hold returns; Shumway 1997 for delisting handling). The findings replicate known results: short-horizon drift, sell-side calls more informative than buys, and newsletters showing no long-horizon stock-selection alpha (Metrick 1999; Graham & Harvey 1996).

## Limits — stated plainly

1. **No calendar-time portfolio check** (Fama 1998): long-horizon t-stats are optimistic under overlapping windows; the 3Y *direction* is robust, its precision is not.
2. **Multiple testing**: the single significant positive result (1M spread, t=2.33, p≈0.02 across ~12 hypotheses) does not survive strict Bonferroni correction.
3. **LLM stance extraction** has no human-labeled validation sample; paywalled articles contribute preview text only (79% of corpus words captured).
4. **Benchmark** is a cap-weighted sector ETF rather than characteristics-matched portfolios; residual size effects are possible.
5. **Fairness**: SemiAnalysis states it does not provide investment advice, ratings, or price targets. This audit measures the information content of its published stances — a frame it never claimed for itself.
