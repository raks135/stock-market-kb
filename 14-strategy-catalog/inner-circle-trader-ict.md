# Inner Circle Trader (ICT) — Smart Money Concepts

- **Topic:** Inner Circle Trader (ICT) methodology — a price-action framework for tracking institutional order flow, liquidity pools, and optimal trade entries/exits
- **Last verified:** 2026-07-19
- **Confidence:** emerging
- **Sources:** ICT mentorship material (Michael Huddleston), institutional order flow literature (Coleman, Zarbai), CME Commitments of Traders (COT) reports, Volume Profile analysis (Dalton, Dalton-Jones)

## TL;DR
ICT teaches retail traders to think and trade like the "smart money" (institutions, banks, proprietary desks) by identifying where large players are likely to enter, stop‑run liquidity, and manipulate price. Core tools: **liquidity pools** (equal highs/lows, buy/sell‑side liquidity), **order blocks** (supply/demand zones), **fair value gaps (FVGs)**, and **optimal trade entries (OTEs)** derived from Fibonacci retracements of impulse legs. Entries are taken when price retraces into a discount/premium zone with confluence of structure; exits use opposite‑side liquidity or time‑based thresholds.

## Core explanation
**Plain language.** Institutions don’t buy or sell at random; they need liquidity to fill large orders without excessive slippage. They create liquidity by running stops (stop hunts) and then reverse in the opposite direction. ICT maps this process in three phases:

1. **Accumulation/Distribution** – price ranges, builds liquidity pools above/below recent swings.
2. **Manipulation** – price spikes through those pools to trigger retail stops (fake breakouts/breakdowns).
3. **Distribution/Re‑accumulation** – price moves aggressively in the intended direction, leaving inefficient price action (fair value gaps) that later act as magnets.

Traders using ICT wait for the manipulation phase, then enter in the direction of the smart‑money move when price retraces to a discounted (bullish) or premium (bearish) area — the OTE (typically 62%–79% Fibonacci retracement of the impulse leg).

**Key concepts (ICT glossary):**

- **Liquidity Pool:** Concentration of stop‑loss orders (buy‑side below lows, sell‑side above highs). Price often revisits these zones to induce retail exits.
- **Order Block:** The last bullish/bearish candle before a strong move — represents institutional footprint. A bullish order block is a demand zone; bearish is a supply zone.
- **Fair Value Gap (FVG):** A three‑candle imbalance where price leaves an inefficient gap (usually due to large order absorption). Price tends to return to “fill” the gap later.
- **Optimal Trade Entry (OTE):** The 62%–79% retracement zone of a bullish/bearish impulse leg (measured from swing low to swing high, or vice‑versa). Entry here offers the best risk‑reward for riding the continuation.
- **Breaker Block:** A failed order block that flips function (e.g., a bullish OB that gets broken becomes a bearish breaker block — now resistance).
- **Market Structure Shift (MSS):** A clear break of swing high/low that signals a change in trend direction.
- **Change of Character (ChoCh):** The first candle that closes opposite the prior trend’s direction after a MSS — early sign of momentum shift.
- **Kill Zones:** Specific times of day (London open, New York open, Asian overlap) when institutional volume spikes and price is most likely to make decisive moves.

## Entry and exit rules (ICT‑style)

### Long bias (bullish market structure)

1. **Identify market structure:** Higher highs and higher lows (uptrend) on the chosen timeframe (e.g., 15 min, 1 h).
2. **Wait for a liquidity sweep:** Price dips below a recent swing low to take out buy‑side stops (creates a low‑liquidity vacuum).
3. **Look for a bullish order block:** The last bearish candle before the price rallies strongly from that low.
4. **Check for a fair value gap (optional but adds confluence):** A three‑candle gap above the order block.
5. **Enter at the OTE:** Wait for price to retrace into the 62%–79% zone of the impulse leg (from the swing low to the high of the move that created the order block). Use a limit order or wait for a bullish rejection candle (pin bar, engulfing) at that level.
6. **Stop loss:** Place just below the low of the liquidity sweep (or below the order block if tighter).
7. **Take profit:** Target the next liquidity pool above (recent swing high, or equal highs). Alternatively, use a 1:2 or 1:3 risk‑reward, or trail the stop using the next opposing order block/FVG.

### Short bias (bearish market structure)

1. **Identify market structure:** Lower lows and lower highs (downtrend).
2. **Wait for a liquidity sweep:** Price rallies above a recent swing high to take out sell‑side stops.
3. **Look for a bearish order block:** The last bullish candle before the price drops sharply from that high.
4. **(Optional) FVG:** A three‑candle gap below the order block.
5. **Enter at the OTE:** Wait for price to retrace into the 62%–79% zone of the bearish impulse leg (from swing high to low of the move). Use a limit order or wait for a bearish rejection candle.
6. **Stop loss:** Just above the high of the liquidity sweep (or above the order block).
7. **Take profit:** Target the next liquidity pool below (recent swing low, or equal lows). Use 1:2‑1:3 RR or trail with the next opposing structure.

## Risk management & trade management

- **Position size:** Risk no more than 1–2 % of equity per trade.
- **Reward‑to‑risk:** Aim for at least 1.5:1; many ICT traders target 2:1 or 3:1 by letting winners run to the next liquidity pool.
- **Time filter:** Only trade during high‑probability kill zones (London 08:00‑11:00 GMT, New York 13:00‑16:00 GMT, Asian overlap 00:00‑04:00 GMT) when institutional participation peaks.
- **News avoidance:** Avoid entering 5 minutes before high‑impact news (NFP, FOMC, CPI) unless trading the news spike with very tight stops.
- **Multiple timeframe confirmation:** Use a higher timeframe (e.g., 4 h) to confirm trend and key liquidity levels; drop to lower timeframe (15 m, 5 m) for entry.

## Common mistakes

1. **Chasing the breakout:** Entering when price first spikes through a liquidity pool (the manipulation phase) instead of waiting for the retracement.
2. **Ignoring market structure:** Taking longs in a downtrend or shorts in an uptrend because a “good” OTE appeared — structure must align.
3. **Over‑reliance on indicators:** ICT is price‑action based; adding oscillators or moving averages often creates noise and false signals.
4. **Wrong OTE range:** Using the entire 38%–62% retracement instead of the stricter 62%–79% zone (the “discount”/“premium” area where smart money typically re‑enters).
5. **Neglecting stop placement:** Placing stops too tight (inside the order block) gets stopped out by random noise; too wide sacrifices reward‑to‑risk.
6. **Trading outside kill zones:** Low‑volume periods (e.g., Friday afternoon, major holidays) produce choppy, unreliable price action.

## Further reading & resources

- **Michael Huddleston (Inner Circle Trader)** – YouTube playlist “ICT Mentorship” (free) covers liquidity, order blocks, OTEs, and kill zones in detail.
- **“The Art and Science of Technical Analysis” by Adam Grimes** – chapters on market structure and price‑action patterns.
- **COT Reports (CFTC)** – weekly breakdown of commercial vs. non‑commercial positioning; extremes often precede reversals.
- **Volume Profile (Viktor Niederhoffer, Jim Dalton)** – shows where volume has accumulated (high‑volume nodes = likely liquidity pools).
- **“Trading Price Action Trends” by Al Brooks** – detailed breakdown of price‑action patterns, spikes, and reversals that underlie ICT concepts.
- **ICT‑style cheat sheets** – many free PDFs online summarizing the key patterns (liquidity sweeps, order blocks, FVGs, OTEs).