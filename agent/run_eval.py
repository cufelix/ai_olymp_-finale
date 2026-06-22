# -*- coding: utf-8 -*-
"""Dukaz: porovna agenta s baseline na oznacenych pripadech pres bodovac.py.

Spusti agenta na FIRMA-0001..0006, da jeho seznamy povinnosti scoreru a vypise
propasnute / zbytecne navic vs baseline + zatez zakladatele (founder_burden).
Cil: agent 0 / 0 / 0, baseline propasne hodne.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DATA = os.path.join(_ROOT, "data")
for p in (_DATA, _HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import bodovac
import tools
from engine import analyze


def main():
    ids = [f"FIRMA-{i:04d}" for i in range(1, 7)]
    moje = {}
    for fid in ids:
        r = analyze(fid)
        moje[fid] = r["nase_kody"]

    print("=" * 56)
    print(" SPOLECNIK vs BASELINE  (oznacene pripady, bodovac.py)")
    print("=" * 56)
    bodovac.vyhodnot(moje)
    print("-" * 56)
    print(f"Zatez zakladatele (dohledatelne otazky): {tools.founder_burden()}")
    print("  -> 0 = vse dohledano z registru/zameru (princip once-only)")
    print("=" * 56)


if __name__ == "__main__":
    main()
