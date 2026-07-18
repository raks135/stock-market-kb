# relative_valuation_demo.py  (pure stdlib; Python 3.10+)
# Data source for real use: SEC EDGAR / Capital IQ / FactSet / Bloomberg.

def enterprise_value(market_cap, total_debt, cash, preferred=0.0, minority=0.0):
    return market_cap + total_debt + preferred + minority - cash

# Peer group (illustrative $ millions). Replace with live filings data.
peers = [
    # name,          mkt_cap, debt, cash, ebitda, ni,   book_eq, sales
    ("Peer_A",        4000,  800,  300,   600,   350,   1200,   3000),
    ("Peer_B",        9000, 1500,  500,  1200,   800,   3000,   7000),
    ("Peer_C",        2500,  400,  200,   400,   180,    800,   2000),
    ("Peer_D",       15000, 3000,  900,  2100,  1300,   5000,  11000),
]

rows = []
for name, mc, d, c, eb, ni, be, sa in peers:
    ev = enterprise_value(mc, d, c)
    rows.append({
        "name": name, "EV": ev, "EBITDA": eb, "NI": ni, "BookEq": be, "Sales": sa,
        "EV_EBITDA": ev / eb,
        "PE": mc / ni,
        "PB": mc / be,
        "PS": mc / sa,
    })

def median(xs):
    s = sorted(xs); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

med = {k: median([r[k] for r in rows]) for k in ("EV_EBITDA", "PE", "PB", "PS")}
print("Peer median multiples:", {k: round(v, 2) for k, v in med.items()})

# Target company (the one we are valuing), $ millions
target = {"mkt_cap": 6000, "debt": 1000, "cash": 400,
          "ebitda": 900, "ni": 500, "book_eq": 1800, "sales": 4500}
t_ev = enterprise_value(target["mkt_cap"], target["debt"], target["cash"])

# Apply peer medians to target fundamentals -> implied values
implied_equity_ev_ebitda = med["EV_EBITDA"] * target["ebitda"] - target["debt"] + target["cash"]
implied_equity_pe        = med["PE"] * target["ni"]
implied_equity_pb        = med["PB"] * target["book_eq"]
implied_equity_ps        = med["PS"] * target["sales"]

print(f"Target actual market cap : ${target['mkt_cap']:.0f}m")
print(f"Implied equity via EV/EBITDA: ${implied_equity_ev_ebitda:.0f}m")
print(f"Implied equity via P/E      : ${implied_equity_pe:.0f}m")
print(f"Implied equity via P/B      : ${implied_equity_pb:.0f}m")
print(f"Implied equity via P/S      : ${implied_equity_ps:.0f}m")
