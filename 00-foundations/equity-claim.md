---
title: What Is a Stock? The Equity Claim Explained
topic_id: 00-foundations/equity-claim
tags: [equity, stock, share, ownership, common-stock, preferred-stock, market-cap, foundational]
last_updated: 2026-07-18
confidence: robust
sources: [S13, S14, S15, S16, S17, S18, S19]
---

## TL;DR
- A stock (share, equity) is a **fractional ownership claim** on a corporation: a residual claim on its assets and earnings, plus (for common stock) voting rights.
- Equity sits at the **bottom of the capital structure**. In liquidation, bondholders are paid first, then preferred shareholders, then common shareholders — who may get nothing.
- Share *counts* are decisive: **market cap = price × shares outstanding**, and you must distinguish authorized, issued, outstanding, and treasury shares. Market cap is a market price, not intrinsic value.

## Core explanation
**Plain language.** When you buy a share of stock you buy a slice of ownership in a company. That slice entitles you to a proportionate share of what the company earns (often paid as dividends) and, for common stock, a vote in major corporate decisions such as electing the board of directors. The company issues stock to raise money — to pay down debt, fund growth, or build facilities [S13].

**Precise definition.** A share of common stock is an *equity security*: a perpetual, divisible claim on the residual assets and residual earnings of a corporation after all fixed obligations (debts, taxes, preferred dividends) are met. It is a **residual claim** — shareholders are paid only what remains, which can be zero [S13][S16]. Ownership is generally accompanied by **limited liability**: a shareholder's downside is capped at the amount invested; they are not personally liable for corporate debts [S13].

Two principal classes exist:
- **Common stock** — carries voting rights and a variable claim on earnings/dividends; last in line on liquidation [S13][S16].
- **Preferred stock** — usually *non-voting*, pays a fixed (often cumulative) dividend, and has priority over common stock for dividends and on liquidation [S13][S17]. It blends debt-like (fixed income, rate-sensitive price) and equity-like (ownership) features [S17].

Stocks are also categorized by style (growth, income, value, blue-chip) and by size via **market capitalization** (large-, mid-, small-, micro-cap) [S13][S19].

## Math / formulas

**Market capitalization** — the total market value of a company's equity:
```
Market Cap = Current Share Price × Total Shares Outstanding        [S19]
```
This is what the market currently pays; it is *not* the company's intrinsic value or acquisition cost [S19].

**Book equity (shareholders' equity)** from the balance sheet:
```
Book Equity = Total Assets − Total Liabilities
Book Value per Share = Book Equity / Shares Outstanding
```
Market price above book value per share implies the market expects returns above the accounting cost of equity (a premium, not a guarantee).

**Ownership fraction:**
```
Ownership % = (Shares you hold) / (Shares Outstanding) × 100
```

**Share-count relationships** [S18]:
```
Authorized  ≥  Issued  ≥  Outstanding
Outstanding = Issued − Treasury (shares repurchased by the firm)
```
Authorized = maximum shares the charter permits issuing; issued = actually sold; outstanding = issued shares still held by investors (excludes treasury) [S18].

**Liquidation waterfall (who gets paid first):**
```
1. Secured creditors / bondholders
2. Unsecured creditors
3. Preferred shareholders (priority over common)
4. Common shareholders (residual — last, may receive nothing)   [S13][S17]
```

## Worked example / code
Illustrative figures only (synthetic — **not** live market data). Compute market cap, book value per share, one investor's ownership, and a liquidation split.

```python
# Requires: python==3.11 (standard library only; no pandas/numpy needed)
# Illustrative figures are synthetic — not live market data.

# --- Illustrative company inputs (synthetic) ---
price            = 100.0     # current share price ($)
shares_out       = 20_000_000
shares_issued    = 22_000_000
treasury_shares  = shares_issued - shares_out
book_equity      = 1_500_000_000.0   # total shareholders' equity ($)
investor_shares  = 50_000

# --- Derived metrics ---
market_cap       = price * shares_out
bvps             = book_equity / shares_out
ownership_pct    = investor_shares / shares_out * 100

print(f"Market cap        : ${market_cap:,.0f}")
print(f"Book value/share  : ${bvps:,.2f}")
print(f"Investor owns     : {ownership_pct:.4f}% of the company")
print(f"Treasury shares   : {treasury_shares:,}")

# --- Liquidation waterfall (synthetic proceeds available: $1.2B) ---
proceeds = 1_200_000_000.0
debt     = 800_000_000.0
preferred= 200_000_000.0
common_available = max(proceeds - debt - preferred, 0.0)
print(f"Common shareholders receive: ${common_available:,.0f} "
      f"(per share: ${common_available/shares_out:.2f})")
```
Expected output for the waterfall branch: debt and preferred are satisfied first; if proceeds < debt+preferred, common gets $0 — illustrating the residual, last-in-line nature [S13][S17].

## Assumptions & limitations
- **Limited liability** holds for standard corporate stock; it is not absolute in cases of fraud, guarantees, or certain pass-through structures [S13].
- **Voting ≠ control** for a small holder. One share = one vote, but control requires a large bloc; many firms use **dual-class** shares that concentrate voting power irrespective of economic ownership (not covered in depth here — see a governance source before assuming "one share one vote").
- **Preferred is usually non-voting**; do not assume every share votes [S13][S17].
- **Market cap is a price, not value.** It reflects what investors are willing to pay now, not intrinsic worth; it ignores debt (use enterprise value for acquisition cost) [S19].
- **Dilution:** authorized-but-unissued shares, option pools, warrants, and convertible preferred can increase shares outstanding and shrink your ownership % over time [S18][S19].
- **Beneficial vs registered ownership:** most retail shares are held in "street name" via a broker (the registered owner on the books is often Cede & Co., DTC's nominee), but the investor remains the **beneficial owner** with full economic rights; direct registration (DRS) puts your name on the issuer's books [S15].

## Empirical evidence
- Equity offers the highest long-run growth potential of major asset classes, but with real downside: Investor.gov notes that investors who held stocks over long horizons (e.g., ~15 years) were "generally rewarded with strong, positive returns," yet large-company stocks as a group lost money on average about **one year in every three** [S13]. This is descriptive education, not a forward-looking guarantee.
- The equity risk premium is a well-established empirical finding in finance (corroborated broadly in CFA/corporate-finance curricula), but its *current* magnitude is contested and time-varying — do not treat historical averages as promised future returns.

## Conflicting views
- **Equity as "ownership" vs "residual claim":** popular framing emphasizes control/voting, while corporate-finance framing emphasizes the residual, last-in-line claim. Both are correct; the emphasis matters for risk (the residual claim is the riskiest piece of the capital structure) [S13][S16][S17].
- **Preferred stock's nature:** it is legally equity (ownership) but behaves like a hybrid — fixed cumulative dividends and interest-rate sensitivity link it to debt. Practitioners disagree on whether to model it as equity or near-debt in valuation [S17].
- **Market cap as a size proxy:** useful and standard [S19], but critics note it ignores leverage and can mislead cross-company comparisons — hence enterprise value and book multiples as complements [S19].

## Common mistakes
- Equating **market cap with company value / what it would cost to buy** the firm (it does not include debt; use enterprise value) [S19].
- Assuming **all shares vote** — preferred usually does not [S13][S17].
- Ignoring **dilution** from authorized shares, options, and converts [S18][S19].
- Believing **street-name holding** (via broker) means you don't really own the stock — you are the beneficial owner with full rights [S15].
- Reading a **share price** as "expensive/cheap" without normalizing by earnings, book value, or market cap [S19].
- Forgetting that in bankruptcy **common shareholders can get zero** after debt and preferred are paid [S13][S17].

## Further reading
- [S13] SEC Investor.gov, "Stocks — FAQs" (definition, common vs preferred, liquidation priority, risks) — https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks *(Tier 1)*
- [S14] SEC Investor.gov, "Shareholder Voting" (voting rights, elect directors) — https://www.investor.gov/shareholder-voting *(Tier 1)*
- [S15] SEC Investor.gov / FINRA, "Investor Bulletin: Holding Your Securities" (street name, beneficial owner, DTC/Cede & Co., DRS) — https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-97 *(Tier 1)*
- [S16] Investopedia, "Common Stock" — https://www.investopedia.com/terms/c/commonstock.asp *(Tier 2)*
- [S17] Corporate Finance Institute, "Common vs Preferred Shares" — https://corporatefinanceinstitute.com/resources/equities/common-vs-preferred-shares *(Tier 2)*
- [S18] BDC, "Shares authorized, issued and outstanding" — https://www.bdc.ca/en/articles-tools/entrepreneur-toolkit/templates-business-guides/glossary/shares-authorized-issued-and-outstanding *(Tier 2)*
- [S19] Investopedia, "Market Capitalization" — https://www.investopedia.com/terms/m/marketcapitalization.asp *(Tier 2)*
