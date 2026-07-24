# Sources Registry — Stock Market Analysis Knowledge Base

## Tier Definitions
- **Tier 1 (Primary/Authoritative):** SEC, FINRA, Investor.gov, CFA Institute, NYSE/NASDAQ papers, peer-reviewed (q-fin/arXiv/SSRN), textbooks (Graham & Dodd, Damodaran, Hull, Grinold & Kahn, López de Prado, O'Hara)
- **Tier 2 (High-quality Secondary):** Damodaran NYU materials, Quantocracy, library docs (pandas/numpy/statsmodels/scikit-learn/backtrader/zipline-reloaded/QuantLib/vectorbt/PyPortfolioOpt), reputable financial media (WSJ, FT, Bloomberg), BIS/Fed notes, CRS reports, Investopedia (curated), Corporate Finance Institute
- **Tier 3 (Tertiary/Blog/Opinion):** Personal blogs, YouTube, forums, trading educators, vendor marketing — **use sparingly, flag explicitly, never as sole source for claims**

---

## Source Index

| ID | Tier | Citation | URL / DOI | Used In | Notes |
|----|------|----------|-----------|---------|-------|
| S1 | 1 | SEC, "Equity Market Structure Literature Review Part II: High-Frequency Trading" (2014) | https://www.sec.gov/marketstructure/research/hft_lit_review_march_2014.pdf | 00-foundations/market-structure.md, 00-foundations/exchanges-ats-regnms.md | Authoritative HFT/structure review |
| S2 | 1 | SEC Investor.gov, "Stocks — FAQs" | https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks | 00-foundations/equity-claim.md, 00-foundations/market-structure.md | Official retail education |
| S3 | 1 | FINRA, "Order Types" | https://www.finra.org/investors/insights/order-types | 00-foundations/market-structure.md | Regulator guidance |
| S4 | 1 | NYSE, "Designated Market Makers" | https://www.nyse.com/market-makers | 00-foundations/market-structure.md | Exchange primary source |
| S5 | 1 | O'Hara, M. (2015). "High frequency market microstructure." JFE 116(2), 257-270 | DOI: 10.1016/j.jfineco.2015.03.005 | 00-foundations/market-structure.md, 00-foundations/exchanges-ats-regnms.md | Peer-reviewed, Tier 1 |
| S6 | 2 | Investopedia, "Bid-Ask Spread" | https://www.investopedia.com/terms/b/bid-askspread.asp | 00-foundations/market-structure.md | Good secondary explainer |
| S7 | 2 | Investopedia, "Market Maker" | https://www.investopedia.com/terms/m/marketmaker.asp | 00-foundations/market-structure.md | Good secondary explainer |
| S8 | 1 | SEC Investor.gov, "Initial Public Offerings" | https://www.investor.gov/introduction-investing/investing-basics/glossary/initial-public-offering-ipo | 00-foundations/market-structure.md | Primary/secondary distinction |
| S9 | 1 | SEC Investor.gov, "Primary vs Secondary Markets" | https://www.investor.gov/introduction-investing/investing-basics/glossary/primary-market | 00-foundations/market-structure.md | Primary/secondary distinction |
| S10 | 2 | Investopedia, "Maker-Taker Model" | https://www.investopedia.com/terms/m/makertaker-model.asp | 00-foundations/market-structure.md | Secondary |
| S11 | 2 | Corporate Finance Institute, "Market Maker" | https://corporatefinanceinstitute.com/resources/equities/market-maker/ | 00-foundations/market-structure.md | Secondary |
| S12 | 1 | SEC, "Regulation NMS FAQ" | https://www.sec.gov/divisions/marketreg/nmsfaq610-11.htm | 00-foundations/exchanges-ats-regnms.md | Official Reg NMS FAQ |
| S13 | 1 | SEC Investor.gov, "Stocks" | https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks | 00-foundations/equity-claim.md | Primary retail education |
| S14 | 1 | SEC Investor.gov, "Shareholder Voting" | https://www.investor.gov/shareholder-voting | 00-foundations/equity-claim.md | Voting rights |
| S15 | 1 | SEC Investor.gov, "Investor Bulletin: Holding Your Securities" | https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-97 | 00-foundations/equity-claim.md | Street name / beneficial owner |
| S16 | 2 | Investopedia, "Common Stock" | https://www.investopedia.com/terms/c/commonstock.asp | 00-foundations/equity-claim.md | Secondary |
| S17 | 2 | Corporate Finance Institute, "Common vs Preferred Shares" | https://corporatefinanceinstitute.com/resources/equities/common-vs-preferred-shares/ | 00-foundations/equity-claim.md | Secondary |
| S18 | 2 | BDC, "Shares Authorized, Issued and Outstanding" | https://www.bdc.ca/en/articles-tools/entrepreneur-toolkit/templates-business-guides/glossary/shares-authorized-issued-and-outstanding | 00-foundations/equity-claim.md | Share count hierarchy |
| S19 | 2 | Investopedia, "Market Capitalization" | https://www.investopedia.com/terms/m/marketcapitalization.asp | 00-foundations/equity-claim.md | Market cap definition |
| S20 | 1 | SEC, "Regulation of NMS Stock Alternative Trading Systems (Form ATS-N)" | https://www.sec.gov/rules-regulations/2018/07/regulation-nms-stock-alternative-trading-systems | 00-foundations/exchanges-ats-regnms.md | ATS/dark pool regulation |
| S21 | 1 | FINRA, "Can You Swim in a Dark Pool?" | https://www.finra.org/investors/insights/can-you-swim-dark-pool | 00-foundations/exchanges-ats-regnms.md | FINRA investor education on ATS |
| S22 | 1 | CRS Report R43739, "Dark Pools in Equity Trading: Policy Concerns and Recent Developments" | https://www.everycrsreport.com/reports/R43739.html | 00-foundations/exchanges-ats-regnms.md | Congressional Research Service |
| S23 | 1 | SEC, "Regulation NMS — Release No. 34-51808" | https://www.sec.gov/rules/final/34-51808.pdf | 00-foundations/exchanges-ats-regnms.md | Original Reg NMS adoption |
| S24 | 1 | SEC, "Order Protection Rule (Rule 611) FAQ" | https://www.sec.gov/divisions/marketreg/nmsfaq610-11.htm | 00-foundations/exchanges-ats-regnms.md | Rule 611 mechanics |
| S25 | 1 | SEC Chair Atkins, "Statement on Minimum Pricing Increments and Access Fee Caps" (Oct 2025) | https://www.sec.gov/newsroom/speeches-statements/atkins-101525-statement-regarding-minimum-pricing-increments-access-fee-caps | 00-foundations/exchanges-ats-regnms.md | 2024 amendments upheld |
| S26 | 2 | Sidley Austin, "SEC Proposes Rescission of the Order Protection Rule" (Jun 2026) | https://www.sidley.com/en/insights/newsupdates/2026/06/sec-proposes-rescission-of-the-order-protection-rule | 00-foundations/exchanges-ats-regnms.md | Legal analysis of 2026 proposal |
| S27 | 2 | Nasdaq, "Off-Exchange Trading Increases Across All Types of Stocks" | https://www.nasdaq.com/articles/exchange-trading-increases-across-all-types-stocks | 00-foundations/exchanges-ats-regnms.md | Recent volume share data |
| S28 | 1 | SEC, "Minimum Pricing Increments and Access Fee Caps — Final Rule" (2024) | https://www.sec.gov/rules/final/2024/34-97457.pdf | 00-foundations/exchanges-ats-regnms.md | 2024 Rule 610/612 amendments |

---

## Adding Sources
When adding a new source:
1. Assign next sequential ID (S29, S30, ...)
2. Assign Tier (1/2/3)
3. Provide full citation + stable URL/DOI
4. Note which articles use it
5. Flag any Tier 3 usage with justification

| S29 | 1 | MIT OpenCourseWare, "Topics in Mathematics with Applications in Finance (18.S096/18.642)", Fall 2013/2024 | https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/ | 00-foundations/math-review.md | Lecture notes: Linear Algebra, Probability Theory, Stochastic Processes |
| S30 | 1 | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley. | DOI: 10.1002/9781119482116 | 00-foundations/math-review.md, 08-backtesting-methodology/ | Purged/embargoed CV, deflated Sharpe, bet sizing |
| S31 | 1 | Ledoit, O. & Wolf, M. (2004). "A well-conditioned estimator for large-dimensional covariance matrices." J. Multivariate Anal. 88(2), 365-411. | DOI: 10.1016/S0047-259X(03)00096-4 | 00-foundations/math-review.md | Shrinkage covariance estimation |
| S32 | 1 | Grinold, R. & Kahn, R. (2000). "Active Portfolio Management," 2nd ed. McGraw-Hill. | ISBN: 978-0071355218 | 00-foundations/math-review.md | Factor models, risk models, fundamental law |
| S33 | 1 | Cont, R. (2001). "Empirical properties of asset returns: stylized facts and statistical issues." Quant. Finance 1, 223-236. | DOI: 10.1088/1469-7688/1/2/304 | 00-foundations/math-review.md | Fat tails, volatility clustering, stylized facts |
| S34 | 2 | Brenndoerfer, M. (2025). "Linear Algebra for Quantitative Finance: Portfolio Math." | https://mbrenndoerfer.com/writing/linear-algebra-quantitative-finance-vectors-matrices-pca | 00-foundations/math-review.md | Practitioner-focused linear algebra with Python |
| S35 | 2 | Brenndoerfer, M. (2025). "Probability Distributions in Finance: Normal, Lognormal & Fat Tails." | https://mbrenndoerfer.com/writing/probability-distributions-quantitative-finance | 00-foundations/math-review.md | Practitioner-focused probability with Python |
| S36 | 2 | Quantt. "Linear Algebra for Quant Finance" & "Probability for Quant Finance." | https://www.quantt.co.uk/resources/ | 00-foundations/math-review.md | Interactive educational platform by industry practitioners |
| S37 | 2 | Damodaran, A. (NYU Stern). "Statistics for Finance" webcasts & materials. | https://pages.stern.nyu.edu/~adamodar/New_Home_Page/webcaststatistics.htm | 00-foundations/math-review.md | Academic finance statistics curriculum |
| S38 | 2 | Risk Hub. "Maths for Quant Finance (MQF)" program. | https://riskhub.org/maths-for-quants/ | 00-foundations/math-review.md | Industry practitioner curriculum (JPM, GS, HSBC alumni) |

---

## Tier 3 Usage Log (requires explicit justification)
*None yet — avoid Tier 3 as sole support for any claim*