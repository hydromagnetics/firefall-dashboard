#!/usr/bin/env python3
"""Validate the dataset embedded in index.html and (optionally) export it to data/.

Usage:
  python tools/validate.py            # check only; exit code 1 on any failure
  python tools/validate.py --export   # check, then write data/psi_data.json and data/tests.csv

Standard library only. Run it before every commit that touches index.html.
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
CONTEXT_ONLY = {"PSI-179"}          # non-combustion context entries
INVERSE_SOURCES = {"PSI-10", "PSI-159"}  # ACME investigations with inverse flames

def load():
    for line in HTML.read_text(encoding="utf-8").split("\n"):
        if line.startswith("window.PSI_DATA"):
            body = line[line.index("{"):].rstrip().rstrip(";")
            return json.loads(body)
    sys.exit("index.html: no line starting with window.PSI_DATA")

def check(d):
    errs, warn = [], []
    inv, tests, cfg = d["investigations"], d["tests"], d["config"]
    ids = [i["id"] for i in inv]
    if len(ids) != len(set(ids)): errs.append("duplicate investigation ids")
    comb = [i for i in ids if i not in CONTEXT_ONLY]
    if len(comb) != 24: errs.append(f"expected 24 combustion investigations, found {len(comb)}")
    for i in ids:
        if i not in cfg.get("investigations", {}): errs.append(f"{i}: missing from config.investigations (no scoring rules)")
        if not next(x for x in inv if x["id"] == i).get("doi"): warn.append(f"{i}: no DOI")
    known = set(ids)
    seen = set()
    for t in tests:
        tid = t.get("id")
        if tid in seen: errs.append(f"duplicate test id {tid}")
        seen.add(tid)
        if t.get("p") not in known: errs.append(f"{tid}: unknown investigation {t.get('p')}")
        if not t.get("ln") and not t.get("src"): warn.append(f"{tid}: no source line")
        f = t.get("f", {})
        for k in ("o2_frac", "o2_burner_frac", "co2_frac", "he_frac"):
            v = f.get(k)
            if v and v.get("n") and v["n"][0] is not None:
                lo, hi = v["n"]
                if not (0 <= lo <= 1 and 0 <= hi <= 1): errs.append(f"{tid}: {k} {v['n']} outside 0-1")
        fc = ((f.get("flame_config") or {}).get("v") or "").lower()
        if t.get("p") in INVERSE_SOURCES and fc == "inverse" and "o2_frac" in f:
            errs.append(f"{tid}: inverse flame has burner-stream O2 in o2_frac (should be o2_burner_frac)")
    return errs, warn

def export(d):
    out = ROOT / "data"; out.mkdir(exist_ok=True)
    (out / "psi_data.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    keys = sorted({k for t in d["tests"] for k in t.get("f", {})})
    with open(out / "tests.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["test_id", "psi_id", "row_type", "fuel_phase", "outcome", "source_line", "flags"] + [f"{k}_raw" for k in keys] + [f"{k}_lo" for k in keys] + [f"{k}_hi" for k in keys])
        for t in d["tests"]:
            f = t.get("f", {})
            raw = [(f.get(k) or {}).get("r", (f.get(k) or {}).get("v", "")) for k in keys]
            lo = [((f.get(k) or {}).get("n") or [None, None])[0] for k in keys]
            hi = [((f.get(k) or {}).get("n") or [None, None])[1] for k in keys]
            w.writerow([t.get("id"), t.get("p"), t.get("g"), t.get("ph"), t.get("o"), t.get("ln"), " | ".join(t.get("fl", []))] + raw + ["" if x is None else x for x in lo] + ["" if x is None else x for x in hi])
    print(f"wrote data/psi_data.json and data/tests.csv ({len(d['tests'])} rows, {len(keys)} fields)")

if __name__ == "__main__":
    d = load()
    errs, warn = check(d)
    print(f"{len(d['investigations'])} investigations, {len(d['tests'])} test rows")
    for w_ in warn[:20]: print("warning:", w_)
    if len(warn) > 20: print(f"... {len(warn) - 20} more warnings")
    for e in errs: print("ERROR:", e)
    if errs: sys.exit(1)
    print("OK: all checks passed")
    if "--export" in sys.argv: export(d)
