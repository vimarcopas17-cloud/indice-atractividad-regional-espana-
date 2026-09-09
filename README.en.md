# Regional Attractiveness Index for Spain 🇪🇸

*🌐 [Versión en español](README.md)*

**Which Spanish region should a company choose for its next office or operation?**
An end-to-end data analysis case that turns 4 official public indicators (INE) into a
clear, defensible business recommendation.

## What it solves

Comparing Spain's 17 autonomous communities is hard because each one wins on something
different: Madrid has the wealthiest market but the highest costs; the south is cheap but
has higher unemployment. This project builds a **composite index (0–100)** combining four
dimensions —**market wealth, labour-market health, market size and labour cost**— so the
regions can be ranked objectively and transparently.

## Headline result

- 🥇 **Most robust choice: Catalonia** — the only region in the Top-2 across all three
  strategy scenarios (large market, low unemployment, and lower labour cost than Madrid).
- 🏙️ **If market matters most (commercial HQ): Madrid.**
- 💶 **If cost matters most (back-office / shared-services centre): Andalusia.**

The key takeaway is methodological: **the "best location" depends on the strategy**, and
the sensitivity analysis demonstrates this rather than hiding it.

## How it's built

`read → clean & quality-check → normalise 0-100 → weighted index → sensitivity analysis
→ visualise`. All in **Python (pandas + matplotlib)**. Quality check included: the
population-weighted mean unemployment rate lands at **9.89%** versus the **9.87%**
official INE figure.

## Repository structure

```
data/     indicadores_ccaa.csv        · dataset (real INE data)
notebooks/analisis_atractividad.ipynb · full analysis with narrative and charts
src/      analisis.py                 · reproducible script version
output/   ranking + 4 charts          · exported results
memo/     memo_ejecutivo.md           · consulting-style deliverable (1 page)
```

## Reproduce

```bash
pip install -r requirements.txt
python src/analisis.py          # generates ranking and charts in output/
# or open notebooks/analisis_atractividad.ipynb
```

## Sources (INE)

GDP per capita 2024 (Regional Accounts), unemployment rate Q2 2026 (Labour Force Survey),
population as of 1 Jan 2025 (Continuous Population Statistics) and labour cost 2024
(Labour Cost Survey). Details and limitations in [`memo/memo_ejecutivo.md`](memo/memo_ejecutivo.md).

---
*Personal data-analysis project · Vicente Marco Pastor*
