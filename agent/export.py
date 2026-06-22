# -*- coding: utf-8 -*-
"""Export statickych JSON fixtures pro UI (offline, bez backendu).

Vytvori agent/fixtures/:
    cases.json          - seznam vsech zameru (vyber v UI)
    FIRMA-XXXX.json      - plny rozbor kazdeho zameru
    eval.json           - dukaz vs baseline (0/0) + burden pro pitch slide

UI muze cist tyhle fixtures primo (zadny Python server na podiu = nulove riziko).
"""
import io
import json
import os
import sys
from contextlib import redirect_stdout

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DATA = os.path.join(_ROOT, "data")
for p in (_DATA, _HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import bodovac
import tools
from engine import analyze, list_cases

OUT = os.path.join(_HERE, "fixtures")


def _write(name, obj):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
    os.makedirs(OUT, exist_ok=True)

    cases = list_cases()
    _write("cases.json", cases)

    vse = {}
    for c in cases:
        a = analyze(c["id"])
        vse[c["id"]] = a
        _write(f"{c['id']}.json", a)
    _write("all.json", vse)   # vsechny rozbory v jednom souboru (1 import pro UI)

    # Dukaz vs baseline na oznacenych pripadech (6) + zatez zakladatele.
    ids = [f"FIRMA-{i:04d}" for i in range(1, 7)]
    moje = {fid: analyze(fid)["nase_kody"] for fid in ids}
    with redirect_stdout(io.StringIO()):
        res = bodovac.vyhodnot(moje)  # {"baseline":(bp,bz),"vase":(mp,mz)}
    _write("eval.json", {
        "pripadu": len(ids),
        "baseline": {"propasnute": res["baseline"][0], "zbytecne": res["baseline"][1]},
        "spolecnik": {"propasnute": res["vase"][0], "zbytecne": res["vase"][1]},
        "burden": tools.founder_burden(),
    })

    print(f"Hotovo -> {OUT}")
    print(f"  cases.json ({len(cases)} zameru) + {len(cases)}x rozbor + eval.json")


if __name__ == "__main__":
    main()
