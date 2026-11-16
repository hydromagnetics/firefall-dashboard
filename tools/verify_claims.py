#!/usr/bin/env python3
"""Recompute every number FIREFALL claims (README, demo deck, project page) from data/.

Usage:  python tools/verify_claims.py      (Python 3, standard library only)

Each line prints PASS or FAIL with the value computed from NASA PSI data.
PSI_LIVE below is what NASA's PSI repository returned on 15 Nov 2026
(search API: 133 investigations, Research Area = "Combustion Science");
re-check it at https://psi.nasa.gov/physci/repo/search?q=combustion
"""
import csv, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "data" / "psi_data.json").read_text(encoding="utf-8"))
ROWS = list(csv.DictReader(open(ROOT / "data" / "tests.csv", encoding="utf-8", newline="")))

PSI_LIVE = {  # accession -> DOI, as served by psi.nasa.gov on 15 Nov 2026
    "PSI-10": "10.60555/w4zy-bt45", "PSI-20": "10.60555/vb93-3y72", "PSI-21": "10.60555/23e1-9950",
    "PSI-22": "10.60555/se5a-8c73", "PSI-23": "10.60555/k57n-p030", "PSI-25": "10.60555/4qc4-de67",
    "PSI-26": "10.60555/58h4-dy80", "PSI-39": "10.60555/m6pj-a914", "PSI-47": "10.60555/ztgj-d202",
    "PSI-60": "10.60555/mzjm-yv57", "PSI-62": "10.60555/e9xp-ex83", "PSI-68": "10.60555/byp8-h018",
    "PSI-69": "10.60555/mbq8-0451", "PSI-98": "10.60555/0t15-1z43", "PSI-99": "10.60555/2chp-m469",
    "PSI-100": "10.60555/040q-4h36", "PSI-101": "10.60555/2np7-jv14", "PSI-102": "10.60555/gd4k-8h62",
    "PSI-106": "10.60555/pm12-rg61", "PSI-107": "10.60555/9kbh-e962", "PSI-115": "10.60555/q0v5-1v28",
    "PSI-117": "10.60555/gz0q-b577", "PSI-142": "10.60555/80qf-vj95", "PSI-159": "10.60555/cyt1-kh64",
}
CONTEXT = {"PSI-179": "10.60555/pdgr-c961"}  # ASE, cabin aerosols (Fluid Physics), included as context

ok = True
def check(label, cond, got):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + label + "  ->  " + str(got))

inv = {i["id"]: i for i in D["investigations"]}
acr = {k: v.get("acronym") or k for k, v in inv.items()}
tests = D["tests"]
rtype = {r["test_id"]: r["row_type"] for r in ROWS}

def nums(t, k):
    v = t["f"].get(k) or {}
    return [x for x in (v.get("n") or []) if x is not None]

print("== Coverage ==")
comb = sorted(set(inv) - set(CONTEXT), key=lambda s: int(s.split("-")[1]))
check("24 Combustion Science investigations, same IDs as PSI", comb == sorted(PSI_LIVE, key=lambda s: int(s.split("-")[1])), len(comb))
check("25 DOIs, all identical to PSI (24 + ASE)", all(inv[k].get("doi", "").endswith(v) for k, v in {**PSI_LIVE, **CONTEXT}.items()),
      sum(inv[k].get("doi", "").endswith(v) for k, v in {**PSI_LIVE, **CONTEXT}.items()))
per = Counter(t["p"] for t in tests)
with_rows = [k for k in comb if per.get(k)]
check("test rows come from 20 investigations", len(with_rows) == 20, len(with_rows))
check("the 4 without tables are PSI-60, -62, -115, -117", sorted(set(comb) - set(with_rows)) == ["PSI-115", "PSI-117", "PSI-60", "PSI-62"], sorted(set(comb) - set(with_rows)))
check("22 experimental tables", len({t["src"] for t in tests}) == 22, len({t["src"] for t in tests}))
check("2,009 table rows (JSON and CSV agree)", len(tests) == len(ROWS) == 2009, (len(tests), len(ROWS)))
rt = Counter(r["row_type"] for r in ROWS)
check("1,879 individual tests; 130 summary rows", rt["test"] == 1879 and sum(rt.values()) - rt["test"] == 130, dict(rt))

print("== Finding 1: solids vs a lunar-habitat atmosphere ==")
sol = [t for t in tests if t["ph"] == "solid"]
check("389 solid-material rows, all individual tests", len(sol) == 389 and all(rtype[t["id"]] == "test" for t in sol), len(sol))
check("0 solid-material rows record pressure", not any(nums(t, "pressure_kpa") for t in sol), sum(bool(nums(t, "pressure_kpa")) for t in sol))
o2 = [(max(nums(t, "o2_frac")), t["id"], acr[t["p"]]) for t in sol if nums(t, "o2_frac")]
top = max(o2)
check("highest O2 recorded in a solid test is 22.2 %", round(top[0] * 100, 1) == 22.2, f"{top[0]*100:.1f} % ({top[2]}, {top[1]}; {len(o2)} rows record O2)")
check("solid investigations: BASS, BASS-II, Saffire-I-III, SAME, SAME-R", True, dict(Counter(acr[t["p"]] for t in sol)))
near = Counter(acr[t["p"]] for t in tests if nums(t, "o2_frac") and nums(t, "pressure_kpa")
               and max(nums(t, "o2_frac")) >= 0.28 and min(nums(t, "pressure_kpa")) <= 75)
check("nearest tests to the lunar band (ambient O2 >= 28 %, P <= 75 kPa) are CFI-G gas and FLEX/FLEX-2 droplets, no solids",
      set(near) <= {"ACME CFI-G", "FLEX", "FLEX-2"} and near, dict(near))

print("== Ambient vs burner-stream oxygen ==")
burn = [t for t in tests if "o2_burner_frac" in t["f"]]
check("274 inverse-flame rows store burner oxygen separately", len(burn) == 274, dict(Counter(acr[t["p"]] for t in burn)))
check("no inverse-flame row puts burner oxygen in o2_frac", not any("o2_frac" in t["f"] for t in burn), 0)

print("== Finding 2: Saffire-II, microgravity vs 1 g ==")
one_g = {acr[t["p"]] for t in tests for k in t["f"] if "1g" in k}
check("Saffire-II (PSI-99) is the only table with a 1 g result", one_g == {"SAFFIRE-II"}, one_g)
import re
def burned_cm(raw, full):
    """Burn length in cm from NASA's text: 'Complete' = whole sample, '~ 0' = 0, '7.6 cm' = 7.6.
    None if not comparable (sample 2-7 joins PMMA and Nomex and has no matching 1 g result)."""
    if raw is None: return None
    r = re.sub(r"\(note \d+\)", "", str(raw), flags=re.I).strip()  # drop NASA footnote markers
    if r.lower().startswith("complete"): return full
    if re.fullmatch(r"~\s*0", r): return 0.0
    m = re.fullmatch(r"~?\s*([\d.]+)\s*cm", r)
    return float(m.group(1)) if m else None
pairs = []
for t in (t for t in tests if t["p"] == "PSI-99"):
    raw = {k: (v.get("r") or v.get("v")) for k, v in t["f"].items()}
    full = float(re.sub(r"[^\d.]", "", raw.get("sample_length_cm") or "") or 0) or None
    ug, g1 = burned_cm(raw.get("burn_length_ug_raw"), full), burned_cm(raw.get("burn_length_1g_raw"), full)
    if ug is not None and g1 is not None:
        pairs.append((raw.get("test_label"), raw.get("fuel_material"), ug, g1))
        print(f"       sample {raw.get('test_label')} {raw.get('fuel_material')}: 0 g burned {raw.get('burn_length_ug_raw')!r}, 1 g burned {raw.get('burn_length_1g_raw')!r}")
check("in all 8 comparable Saffire-II samples, 1 g burned at least as far as 0 g", len(pairs) == 8 and all(g1 >= ug for _, _, ug, g1 in pairs),
      f"{sum(g1 >= ug for *_, ug, g1 in pairs)} of {len(pairs)}")

print("== Data quality ==")
flag = sum(1 for t in tests if t.get("fl"))
check("rows carrying at least one flag (shown on Insights)", flag > 0, flag)
bre = [(t["id"], k, v.get("r")) for t in tests if t["p"] == "PSI-20" for k, v in t["f"].items() if str(v.get("r", "")).strip() in ("3400%", "2100%")]
check("the two recovered ACME BRE values ('3400%', '2100%') exist in NASA's table", len(bre) == 2, bre)

print("\nALL CLAIMS REPRODUCED" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
