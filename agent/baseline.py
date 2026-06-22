# -*- coding: utf-8 -*-
"""Reprodukce jednoducheho pruvodce (baseline), proti kteremu se merime.

Baseline vzdy plivne tytez 4 povinnosti, at je zamer jakykoli, a v case nehlida.
Hada VOLNOU zivnost i u regulovanych oboru (chyba). Viz data/baseline_popis.md.
"""

BASELINE_KODY = ["OR_ZAPIS", "DPPO", "DATOVKA", "ZIVNOST_VOLNA"]


def baseline_codes(intent=None):
    """Co by k zameru vratil naivni pruvodce (nezavisle na zameru)."""
    return list(BASELINE_KODY)
