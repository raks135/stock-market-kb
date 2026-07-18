#!/usr/bin/env python3
# Run: python3 dcf_demo.py   (Python 3.10+, no external dependencies)
# Illustrative two-stage DCF: FCFF discounted at WACC, two terminal-value methods.

# --- CAPM cost of equity & WACC inputs ---
rf, mrp, beta = 0.04, 0.055, 1.15          # risk-free, equity risk premium, levered beta
cost_of_equity = rf + beta * mrp            # = 0.10325
pre_tax_kd, tax = 0.05, 0.21
E_mv, D_mv = 600.0, 400.0                   # market values of equity & debt ($m)
wacc = (E_mv/(E_mv+D_mv))*cost_of_equity + (D_mv/(E_mv+D_mv))*pre_tax_kd*(1-tax)

# --- explicit FCFF forecast, years 1..5 ($m) ---
fcff = [40.0, 46.0, 53.0, 61.0, 70.0]
n = len(fcff)

# --- terminal value: Gordon growth (must have g < WACC) ---
g = 0.025
tv_gordon = fcff[-1] * (1 + g) / (wacc - g)
pv_explicit = sum(f / (1+wacc)**t for t, f in enumerate(fcff, 1))
pv_tv_gordon = tv_gordon / (1 + wacc)**n
firm_value = pv_explicit + pv_tv_gordon
equity_value_gordon = firm_value - D_mv

# --- terminal value: exit EV/EBITDA multiple ---
ebitda_n, exit_mult = 110.0, 9.0
tv_exit = ebitda_n * exit_mult
pv_tv_exit = tv_exit / (1 + wacc)**n
equity_value_exit = (pv_explicit + pv_tv_exit) - D_mv

# FCFE bridge (illustrative, net borrowing = 0): FCFE = FCFF - Int(1-t)
int_after_tax = D_mv * pre_tax_kd * (1 - tax)
fcfe = [f - int_after_tax for f in fcff]

# sanity check: implied perpetuity growth from the exit-multiple TV
implied_g = (tv_exit * wacc - fcff[-1]) / (tv_exit + fcff[-1])

shares = 20.0  # million shares outstanding
print(f"WACC={wacc:.4f}  CostOfEquity={cost_of_equity:.4f}")
print(f"PV explicit FCFF={pv_explicit:.1f}  TV(Gordon)={tv_gordon:.1f}")
print(f"PV(TV) as % of firm value={pv_tv_gordon/firm_value:.1%}")
print(f"Equity value (Gordon)={equity_value_gordon:.1f}  -> price ${equity_value_gordon/shares:.2f}")
print(f"Equity value (Exit 9x)=${equity_value_exit:.1f}  -> price ${equity_value_exit/shares:.2f}")
print(f"FCFE yr5={fcfe[-1]:.1f} (bridge: FCFF - Int(1-t)={fcff[-1]:.1f}-{int_after_tax:.1f})")
print(f"Implied g from exit TV={implied_g:.4f}  (cf. Gordon g={g})")

# --- sensitivity grid: equity value vs WACC and g (Gordon method) ---
print("\nEquity value ($m) sensitivity [WACC x g]:")
header = "WACC\\g  " + "  ".join(f"{x:.1%}" for x in [0.02,0.025,0.03])
print(header)
for w in [0.07, 0.08, 0.09]:
    row = []
    for gg in [0.02, 0.025, 0.03]:
        tv = fcff[-1]*(1+gg)/(w-gg)
        ev = sum(f/(1+w)**t for t,f in enumerate(fcff,1)) + tv/(1+w)**n - D_mv
        row.append(f"{ev:7.1f}")
    print(f"{w:.1%}  " + "  ".join(row))

assert wacc > g and cost_of_equity > g, "need discount rate > growth rate"
