# -*- coding: utf-8 -*-
"""Simulace casove osy povinnosti (projekce konkretnich dat).

Z rocniho obratu (model linearniho rustu = rocni/12) spocita, KDY firma protne
prah DPH, a deadline prihlasky. U zamestnancu modeluje nastup 1. zamestnance.

DULEZITE: vsechno je PROJEKCE/PREDPOKLAD (typ='projekce'), ne realny cas.
V produkci by datum udalosti prislo z realnych dat (zalozeni, ucetnictvi/banka,
HR feed). V demu je to ten "pretoceni casu" wow moment - oznaceny jako simulace.
"""
from datetime import date, timedelta

from legislation import DPH_PRAH_OBRAT

# Modelovy predpoklad nastupu 1. zamestnance (dni po zalozeni) - jasne oznaceno.
PREDPOKLAD_NASTUP_DNI = 90


def _cz(d):
    return f"{d.day}. {d.month}. {d.year}"


def _konec_mesice(d):
    if d.month == 12:
        return date(d.year, 12, 31)
    return date(d.year, d.month + 1, 1) - timedelta(days=1)


def simulate(obrat, povinnosti, datum_zalozeni=None):
    """Vrati casovou osu s konkretnimi (projektovanymi) daty pro vsechny povinnosti."""
    D = datum_zalozeni or date.today()
    mesicni = round(obrat / 12) if obrat else 0
    udalosti = []

    for p in povinnosti:
        kod = p["kod"]

        if kod == "DPH" and mesicni > 0:
            mesicu = DPH_PRAH_OBRAT / mesicni
            crossing = D + timedelta(days=round(mesicu * 30.44))
            deadline = _konec_mesice(crossing) + timedelta(days=15)
            udalosti.append({
                "povinnost": kod, "nazev": p["nazev"], "typ": "projekce",
                "udalost": "prekroceni obratu 2 mil. Kc",
                "datum_udalosti": crossing.isoformat(), "datum_udalosti_cz": _cz(crossing),
                "termin": deadline.isoformat(), "termin_cz": _cz(deadline),
                "za_dni": (deadline - D).days, "za_mesicu": round(mesicu, 1),
                "predpoklad": "linearni rust obratu (rocni/12)",
                "lhuta": p["lhuta"],
            })

        elif kod in ("ZAM_CSSZ", "ZAM_ZP"):
            nastup = D + timedelta(days=PREDPOKLAD_NASTUP_DNI)
            deadline = nastup + timedelta(days=8)
            udalosti.append({
                "povinnost": kod, "nazev": p["nazev"], "typ": "projekce",
                "udalost": "nastup 1. zamestnance",
                "datum_udalosti": nastup.isoformat(), "datum_udalosti_cz": _cz(nastup),
                "termin": deadline.isoformat(), "termin_cz": _cz(deadline),
                "za_dni": (deadline - D).days,
                "predpoklad": f"modelovy nastup ~{PREDPOKLAD_NASTUP_DNI} dni po zalozeni",
                "lhuta": p["lhuta"],
            })

        else:
            # Okamzite povinnosti - pri zalozeni (den D).
            udalosti.append({
                "povinnost": kod, "nazev": p["nazev"], "typ": "ihned",
                "datum_udalosti": D.isoformat(), "datum_udalosti_cz": _cz(D),
                "termin": D.isoformat(), "termin_cz": _cz(D),
                "za_dni": 0, "lhuta": p["lhuta"],
            })

    udalosti.sort(key=lambda e: e["termin"])
    return {
        "datum_zalozeni": D.isoformat(), "datum_zalozeni_cz": _cz(D),
        "mesicni_obrat": mesicni,
        "udalosti": udalosti,
    }
