# -*- coding: utf-8 -*-
"""Agent core - orchestrace nad rozhranim k datum (tools.py).

analyze(intent_id) projde jeden cyklus rozhodovani:
  1) get_intent            - nacte zamer
  2) lookup_registry       - ONCE-ONLY: dohleda misto ptani (zivnost, ARES spolecnici)
  3) derive (rules)        - odvodi povinnosti vc. skrytych a odlozenych
  4) schedule              - naplanuje odlozene povinnosti v case
  5) uspora + riziko       - spocita Kc usetrene na pokutach vs baseline
  6) vrati strukturovany JSON pro UI (clovek pak potvrzuje = HITL)

Nikdy nevola ask_founder -> founder_burden() zustava 0 (once-only).
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DATA = os.path.join(_ROOT, "data")
if _DATA not in sys.path:
    sys.path.insert(0, _DATA)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import tools  # rozhrani sandboxu (get_intent, lookup_registry, schedule, ...)
from rules import normalize, derive, ODLOZENE
from baseline import baseline_codes
from legislation import POKUTY, DPH_PRAH_OBRAT


def _termin(kod):
    """Lidsky popis terminu odlozene povinnosti (UI z nej udela konkretni datum)."""
    if kod == "DPH":
        return "do 15 dnu po mesici prekroceni obratu"
    if kod in ("ZAM_CSSZ", "ZAM_ZP"):
        return "do 8 dnu od nastupu 1. zamestnance"
    return "dle udalosti"


def _once_only_lookups(intent, predmet):
    """Dohleda v registrech to, na co bychom se jinak museli ptat (burden)."""
    lookups = []

    ziv = tools.lookup_registry("zivnost", predmet)
    ziv_typ = ziv["typ_zivnosti"] if ziv else None
    lookups.append({
        "typ": "zivnost", "klic": predmet,
        "vysledek": (ziv_typ or "neznamy obor"),
        "nahradil_otazku": "Je obor regulovany (volna/vazana/koncese)?",
    })

    for s in intent.get("spolecnici", []) or []:
        if s.get("typ") == "PO" and s.get("ico"):
            a = tools.lookup_registry("ares", s["ico"])
            lookups.append({
                "typ": "ares", "klic": s["ico"],
                "vysledek": (a["nazev"] + " - aktivni" if a else "nenalezeno"),
                "nahradil_otazku": "Existuje a je aktivni spolecnik-firma?",
            })

    return ziv_typ, lookups


def analyze(intent_id):
    intent = tools.get_intent(intent_id)
    if not intent:
        return {"error": f"neznamy zamer {intent_id}"}

    predmet, obrat, zam, provoz = normalize(intent)

    # ONCE-ONLY: ptame se statu, ne zakladatele.
    ziv_typ, registry_lookups = _once_only_lookups(intent, predmet)

    # Derivace povinnosti (vc. skrytych a odlozenych).
    povinnosti = derive(predmet, obrat, zam, provoz, ziv_typ)
    nase_kody = [p["kod"] for p in povinnosti]
    base = baseline_codes(intent)

    # Co baseline mine = skryte povinnosti (na nich je nase pridana hodnota).
    skryte = [k for k in nase_kody if k not in base]

    # USPORA-meter = suma pokut za skryte povinnosti, ktere bychom jinak propasli.
    uspora = 0
    riziko = []
    for k in skryte:
        p = POKUTY.get(k)
        if p:
            uspora += p["max_kc"]
            riziko.append({"kod": k, "castka": p["max_kc"], "typ": p["typ"],
                           "text": p["text"], "zdroj": p["zdroj"]})

    # Plan v case: naplanuj odlozene povinnosti (realne vola schedule).
    plan = []
    for p in povinnosti:
        if p["kod"] in ODLOZENE:
            t = _termin(p["kod"])
            tools.schedule(intent_id, p["kod"], t)
            plan.append({"povinnost": p["kod"], "nazev": p["nazev"],
                         "termin": t, "duvod": p["trigger"], "lhuta": p["lhuta"]})

    # Oznac skryte + pripoj expozici pokuty k jednotlivym povinnostem.
    for p in povinnosti:
        p["skryta"] = p["kod"] in skryte
        pk = POKUTY.get(p["kod"])
        p["pokuta_kc"] = pk["max_kc"] if (pk and p["kod"] in skryte) else 0

    return {
        "id": intent_id,
        "nazev": intent.get("nazev"),
        "predmet": predmet,
        "obrat": obrat,
        "zamestnanci": zam,
        "provozovna": provoz,
        "dph_prah": DPH_PRAH_OBRAT,
        "povinnosti": povinnosti,
        "nase_kody": sorted(nase_kody),
        "baseline_kody": sorted(base),
        "skryte_kody": sorted(skryte),
        "plan": plan,
        "uspora_kc": uspora,
        "riziko_breakdown": riziko,
        "burden": tools.founder_burden(),     # 0 = nic jsme se nezeptali (once-only)
        "registry_lookups": registry_lookups,
    }


def list_cases():
    """Seznam vsech zameru (pro vyber v UI)."""
    return [{"id": z["id"], "nazev": z.get("nazev"), "predmet": z.get("predmet")}
            for z in tools._ZAMERY.values()]


if __name__ == "__main__":
    import json
    fid = sys.argv[1] if len(sys.argv) > 1 else "FIRMA-0002"
    print(json.dumps(analyze(fid), ensure_ascii=False, indent=2))
