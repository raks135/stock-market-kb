# Iteration Log

## 2026-07-15 — iter 1 (kickoff + first loop)
- Initialized repo: tree 00–15, STATE/{backlog,progress,sources}, README, CHANGELOG.
- Selected P0 task: 00-foundations market structure.
- Sub-questions: bid-ask/spread, order types, primary vs secondary, market makers/participants, microstructure/HFT.
- Sources: 12 gathered (Tier 1: SEC 2014, FINRA, Investor.gov, NYSE paper, O'Hara 2015; Tier 2: Investopedia, Optiver, Schwab, CFA-prep). Confirmed each by fetching summary.
- Wrote 00-foundations/market-structure.md (template-compliant, inline cites, conflict + caveat sections).
- Self-critique → backlog: maker-taker & HFT effects flagged as contested/Verify.
- Committed. Repo health: 1/61 nodes done; many P0 open.

## 2026-07-18 — iter 2
- Selected P0 task: 00-foundations what is a stock / share / equity claim.
- Sub-questions: definition/residual claim; common vs preferred; shareholder rights (voting, dividends, limited liability); capital-structure/liquidation priority; share counts (authorized/issued/outstanding/treasury) + market cap vs book value; how ownership is recorded (street name / beneficial / DTC nominee / DRS).
- Sources: 7 (Tier 1: Investor.gov Stocks FAQ, Shareholder Voting, Holding Your Securities; Tier 2: Investopedia Common Stock & Market Cap, CFI common vs preferred, BDC share counts). All URLs opened + verified. Every major claim corroborated by >=2 independent sources.
- Wrote 00-foundations/equity-claim.md (template-compliant; inline cites S13–S19; TL;DR, core, formulas, runnable code verified, assumptions/limits, evidence, conflicts, mistakes, further reading).
- No new Verify tasks; no self-critique gaps beyond noting dual-class voting nuance flagged in Assumptions.
- Repo health: 2/61 nodes done; many P0 open.

## 2026-07-18 — iter 3
- Selected P0 task: 00-foundations exchanges / ATS / dark pools / Reg NMS basics.
- Sub-questions: lit exchanges vs ATS vs dark pools; Reg ATS/Reg NMS origins; Reg NMS four rules (610 access, 611 order protection/NBBO, 612 sub-penny, market-data 604/605/606); protected quotes/trade-throughs/ISO; dark-pool trade reporting (FINRA TRF); fragmentation & volume; 2024 amendments; 2026 rescission proposal.
- Sources: 10 (Tier 1: SEC Reg ATS page S20, FINRA dark-pool S21, CRS R43739 S22, SEC NMS FAQ S23, SEC Atkins S25, + prior S1 HFT; Tier 2: Investopedia S24, Sidley S26, Nasdaq S27, Davis Polk S28). All URLs opened + verified.
- Wrote 00-foundations/exchanges-ats-regnms.md (template-compliant; inline cites S1/S20–S28; runnable stdlib Python for NBBO + trade-through check, verified executing).
- Three-bucket labeling applied; conflicts explicit (Rule 611 benefit vs fragmentation critique; dark-pool efficiency vs transparency; 2026 rescission contested/proposal-only). Failure modes: NBBO size limits, dark pools benchmark lit prices, Reg NMS evolving.
- No new Verify tasks spawned (existing maker-taker/HFT Verify items from iter 1 remain open and still flagged).
