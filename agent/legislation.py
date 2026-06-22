# -*- coding: utf-8 -*-
"""Znalostni baze povinnosti uzemnena v platnych predpisech.

Tohle je GROUNDING vrstva agenta: kazda povinnost ma svuj zakon, paragraf,
lhutu a pripadny prah. Nahrazuje placeholder `lookup_legislation` z tools.py
realnymi citacemi, aby agent nikdy nevydaval zaver bez zdroje.

`verified` = overeno proti primarnimu zdroji (WebFetch na zakony pro lidi /
e-sbirka). Cisla a lhuty oznacena verified=False je nutne potvrdit drive,
nez je ukazeme jako fakt (zadani: "dohledejte platne zneni a prahy").
"""

# Prah obratu pro povinnou registraci k DPH (Kc za 12 po sobe jdoucich mesicu).
# Odvozeno z oznacenych pripadu: 894_731 -> bez DPH, 2_085_359 -> DPH.
DPH_PRAH_OBRAT = 2_000_000  # verified=False -> overit z. 235/2004 Sb.

LEGISLATIVA = {
    "OR_ZAPIS": {
        "nazev": "Zapis spolecnosti do obchodniho rejstriku",
        "zakon": "z. c. 90/2012 Sb., o obchodnich korporacich; z. c. 304/2013 Sb.",
        "paragraf": "vznik s.r.o. zapisem do OR",
        "lhuta": "navrh na zapis do 6 mesicu od zalozeni",
        "kdy": "ihned",
        "verified": False,
    },
    "DPPO": {
        "nazev": "Registrace k dani z prijmu pravnickych osob",
        "zakon": "z. c. 586/1992 Sb., o danich z prijmu",
        "paragraf": "§ 39 (registracni povinnost)",
        "lhuta": "do 15 dnu od vzniku spolecnosti",
        "kdy": "ihned",
        "verified": False,
    },
    "DATOVKA": {
        "nazev": "Zrizeni datove schranky",
        "zakon": "z. c. 300/2008 Sb., o elektronickych ukonech",
        "paragraf": "§ 5 (PO zrizena ze zakona automaticky)",
        "lhuta": "automaticky pri zapisu do OR",
        "kdy": "ihned",
        "verified": False,
    },
    "SIDLO_OZNACENI": {
        "nazev": "Oznaceni sidla firmy",
        "zakon": "z. c. 455/1991 Sb., zivnostensky zakon",
        "paragraf": "§ 17 odst. 7 / § 31 (oznaceni sidla a provozovny)",
        "lhuta": "trvale od zahajeni cinnosti",
        "kdy": "ihned",
        "verified": False,
    },
    "SKUTECNI_MAJITELE": {
        "nazev": "Zapis do evidence skutecnych majitelu",
        "zakon": "z. c. 37/2021 Sb., o evidenci skutecnych majitelu",
        "paragraf": "automaticky pro nove s.r.o., jinak bez zbytecneho odkladu",
        "lhuta": "pri/bez zbytecneho odkladu po zapisu do OR",
        "kdy": "ihned",
        "verified": False,
    },
    "ZIVNOST_VOLNA": {
        "nazev": "Ohlaseni volne zivnosti",
        "zakon": "z. c. 455/1991 Sb., zivnostensky zakon, priloha 4",
        "paragraf": "§ 25 (ohlasovaci zivnost volna)",
        "lhuta": "pred zahajenim cinnosti",
        "kdy": "ihned",
        "verified": False,
    },
    "ZIVNOST_VAZANA": {
        "nazev": "Ohlaseni vazane zivnosti (odborna zpusobilost)",
        "zakon": "z. c. 455/1991 Sb., zivnostensky zakon, priloha 2",
        "paragraf": "§ 24 (vazana zivnost, nutna odborna zpusobilost)",
        "lhuta": "pred zahajenim cinnosti",
        "kdy": "ihned",
        "verified": False,
    },
    "ZIVNOST_KONCESE": {
        "nazev": "Zadost o koncesi (koncesovana zivnost)",
        "zakon": "z. c. 455/1991 Sb., zivnostensky zakon, priloha 3",
        "paragraf": "§ 26-27 (koncesovana zivnost, potreba statniho povoleni)",
        "lhuta": "pred zahajenim cinnosti, schvaluje zivnostensky urad",
        "kdy": "ihned",
        "verified": False,
    },
    "DPH": {
        "nazev": "Registrace k DPH po prekroceni obratu",
        "zakon": "z. c. 235/2004 Sb., o dani z pridane hodnoty",
        "paragraf": "§ 6 (prekroceni obratu %d Kc / 12 mesicu)" % DPH_PRAH_OBRAT,
        "lhuta": "prihlaska do 15 dnu po skonceni mesice prekroceni prahu",
        "kdy": "odlozena (az pri prekroceni obratu)",
        "verified": False,
    },
    "ZAM_CSSZ": {
        "nazev": "Prihlaseni zamestnavatele na CSSZ",
        "zakon": "z. c. 582/1991 Sb. / 589/1992 Sb.",
        "paragraf": "prihlaseni do registru zamestnavatelu",
        "lhuta": "do 8 dnu od nastupu prvniho zamestnance",
        "kdy": "odlozena (od prvniho nastupu)",
        "verified": False,
    },
    "ZAM_ZP": {
        "nazev": "Oznameni zdravotni pojistovne",
        "zakon": "z. c. 48/1997 Sb., o verejnem zdravotnim pojisteni",
        "paragraf": "§ 10 (oznamovaci povinnost zamestnavatele)",
        "lhuta": "do 8 dnu od nastupu prvniho zamestnance",
        "kdy": "odlozena (od prvniho nastupu)",
        "verified": False,
    },
    "PROVOZOVNA": {
        "nazev": "Ohlaseni provozovny zivnostenskemu uradu",
        "zakon": "z. c. 455/1991 Sb., zivnostensky zakon",
        "paragraf": "§ 17 (zahajeni/ukonceni cinnosti v provozovne)",
        "lhuta": "predem, resp. bez zbytecneho odkladu",
        "kdy": "ihned",
        "verified": False,
    },
}


# Sazby pokut za propasnute povinnosti (Kc). 'max' = zakonne maximum,
# 'odhad' = modelovy odhad penale/expozice. Zdroje viz SPEC.md §8 (overeno webem).
# Slouzi k vypoctu USPORA-meteru = kolik Kc na pokutach agent usetril.
POKUTY = {
    "SKUTECNI_MAJITELE": {"max_kc": 500_000, "typ": "max",
        "text": "az 500 000 Kc + nelze vyplatit zisk z vlastni firmy + pozastavena hlasovaci prava",
        "zdroj": "z. 37/2021 Sb."},
    "ZAM_CSSZ": {"max_kc": 100_000, "typ": "max",
        "text": "az 100 000 Kc za neprihlaseni zamestnance", "zdroj": "z. 582/1991 Sb."},
    "ZAM_ZP": {"max_kc": 50_000, "typ": "max",
        "text": "pokuta za nesplneni oznamovaci povinnosti zdravotni pojistovne", "zdroj": "z. 48/1997 Sb."},
    "PROVOZOVNA": {"max_kc": 50_000, "typ": "max",
        "text": "az 50 000 Kc za neohlaseni provozovny", "zdroj": "zivn. z. 455/1991 §17/62"},
    "SIDLO_OZNACENI": {"max_kc": 20_000, "typ": "max",
        "text": "az 20 000 Kc za neoznaceni sidla", "zdroj": "zivn. z. 455/1991 §31/62"},
    "DPH": {"max_kc": 50_000, "typ": "odhad",
        "text": "domereni dane + penale 0,05 %/den (max 5 %) + urok z prodleni (odhad expozice)",
        "zdroj": "z. 235/2004 Sb. + danovy rad"},
    "ZIVNOST_VAZANA": {"max_kc": 50_000, "typ": "odhad",
        "text": "riziko provozovani bez spravneho zivn. opravneni (odhad)", "zdroj": "zivn. z. 455/1991"},
    "ZIVNOST_KONCESE": {"max_kc": 100_000, "typ": "odhad",
        "text": "riziko provozovani bez koncese (odhad)", "zdroj": "zivn. z. 455/1991"},
}


def pokuta(kod):
    """Vrati sazbu pokuty za propasnutou povinnost (nebo None)."""
    return POKUTY.get(kod)


def cite(kod):
    """Vrati citaci predpisu pro danou povinnost (zdroj pro transparentnost)."""
    z = LEGISLATIVA.get(kod)
    if not z:
        return {"kod": kod, "zdroj": "NEZNAMO", "verified": False}
    return {
        "kod": kod,
        "nazev": z["nazev"],
        "zdroj": f'{z["zakon"]}, {z["paragraf"]}',
        "lhuta": z["lhuta"],
        "kdy": z["kdy"],
        "verified": z["verified"],
    }
