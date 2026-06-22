# -*- coding: utf-8 -*-
"""Derivace povinnosti ze zameru firmy.

Pravidla jsou zpetne odvozena z oznacenych pripadu a uzemnena v predpisech
(viz legislation.py). Kazda povinnost nese: kod, nazev, kdy (ihned/odlozena),
trigger (proc plati), zdroj (§), a semafor (zelena/oranzova/cervena = HITL).

Pozor: derivujeme, NEcteme spravne odpovedi z ukazkove_pripady.json.
"""
from legislation import DPH_PRAH_OBRAT, cite

# Povinnosti, ktere plati pro KAZDE nove s.r.o. (deterministicke, vysoka jistota).
VZDY = ["OR_ZAPIS", "DPPO", "DATOVKA", "SIDLO_OZNACENI", "SKUTECNI_MAJITELE"]

# Mapovani typu zivnosti (z registru) -> kod povinnosti.
ZIV_MAP = {"volna": "ZIVNOST_VOLNA", "vazana": "ZIVNOST_VAZANA", "koncese": "ZIVNOST_KONCESE"}

# Ktere povinnosti jsou odlozene v case (hlidaji se, nevznikaji ihned pri zalozeni).
ODLOZENE = {"DPH", "ZAM_CSSZ", "ZAM_ZP"}


def normalize(intent):
    """Sjednoti dva tvary zameru (zamery_firem.json vs ukazkove_pripady.json)."""
    predmet = intent.get("predmet")
    obrat = intent.get("predpokladany_obrat_rok", intent.get("obrat", 0)) or 0
    zam = intent.get("plan_zamestnancu", intent.get("zamestnanci", 0)) or 0
    provoz = intent.get("provozovna")  # objekt | null | bool
    return predmet, int(obrat), int(zam), bool(provoz)


def _polozka(kod, kdy, trigger, semafor="zelena"):
    c = cite(kod)
    return {
        "kod": kod,
        "nazev": c["nazev"],
        "kdy": kdy,                 # "ihned" | "odlozena"
        "trigger": trigger,        # proc povinnost plati (lidsky)
        "zdroj": c["zdroj"],       # § + zakon (transparentnost)
        "lhuta": c["lhuta"],
        "verified": c["verified"],
        "semafor": semafor,        # zelena = jisto+citovano | oranzova = overit | cervena = chybi data
    }


def derive(predmet, obrat, zam, provoz, ziv_typ):
    """Vrati seznam povinnosti odvozenych ze zameru (s metadaty)."""
    out = []

    for kod in VZDY:
        out.append(_polozka(kod, "ihned", "kazde nove s.r.o. ze zakona"))

    # Zivnost: zatrideni z registru (ne hadame volnou jako baseline).
    if ziv_typ in ZIV_MAP:
        out.append(_polozka(ZIV_MAP[ziv_typ], "ihned",
                            f"obor '{predmet}' = {ziv_typ} zivnost (klasifikace ze ZR)"))
    else:
        # Neznamy obor -> default volna, ale ORANZOVA (nutna lidska kontrola).
        out.append(_polozka("ZIVNOST_VOLNA", "ihned",
                            f"obor '{predmet}' neni v klasifikaci -> default volna, OVERIT",
                            semafor="oranzova"))

    # DPH: odlozena povinnost pri prekroceni obratu.
    if obrat > DPH_PRAH_OBRAT:
        out.append(_polozka("DPH", "odlozena",
                            f"obrat {obrat:,} Kc > prah {DPH_PRAH_OBRAT:,} Kc".replace(",", " ")))

    # Zamestnanci: odlozene povinnosti od prvniho nastupu.
    if zam >= 1:
        out.append(_polozka("ZAM_CSSZ", "odlozena", f"plan {zam} zamestnancu -> od 1. nastupu"))
        out.append(_polozka("ZAM_ZP", "odlozena", f"plan {zam} zamestnancu -> od 1. nastupu"))

    # Provozovna.
    if provoz:
        out.append(_polozka("PROVOZOVNA", "ihned", "zamer ma vyplnenou provozovnu"))

    return out
