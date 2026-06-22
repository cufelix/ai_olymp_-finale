# Agent core — Společník

Mozek produktu: nad rozhraním sandboxu (`tools.py`) odvodí povinnosti firmy
(i skryté a odložené), kříží registry (once-only), naplánuje termíny v čase a
spočítá úsporu na pokutách. **UI jen renderuje tenhle výstup** → „pod tím je
reálná AI, ne formulář".

## Soubory

| Soubor | Co dělá |
|---|---|
| `engine.py` | `analyze(id)` — jeden cyklus rozhodování, vrací JSON kontrakt |
| `rules.py` | derivace povinností ze záměru (pravidla uzemněná v zákonech) |
| `legislation.py` | citace § + sazby pokut (`POKUTY`) + práh DPH |
| `baseline.py` | reprodukce naivního průvodce (pro split screen) |
| `run_eval.py` | důkaz vs baseline přes `bodovac.py` (0/0) |
| `server.py` | tenké HTTP API (jen stdlib) pro UI |
| `export.py` | statické JSON fixtures do `fixtures/` (offline, bez backendu) |
| `fixtures/` | předgenerované rozbory — **UI může číst přímo, žádný server** |

## Spuštění

```bash
# 1) Datový balíček (sandbox od organizátorů) musí ležet v ../data/
#    (tools.py, bodovac.py, *.json) — NENÍ v repu, máte ho lokálně.

python3 agent/run_eval.py          # důkaz: Společník 0/0 vs baseline 28/2
python3 agent/engine.py FIRMA-0002 # JSON rozbor jednoho záměru
python3 agent/server.py            # API na http://localhost:8000
python3 agent/export.py            # vygeneruje fixtures/*.json pro UI
```

## JSON kontrakt (co UI dostane z `/analyze?id=…` i z `fixtures/<id>.json`)

```jsonc
{
  "id": "FIRMA-0002", "nazev": "...", "predmet": "Provoz e-shopu",
  "obrat": 4460716, "zamestnanci": 2, "provozovna": false, "dph_prah": 2000000,

  "povinnosti": [                       // VŠECHNY povinnosti (náš výstup)
    { "kod": "SKUTECNI_MAJITELE", "nazev": "...",
      "kdy": "ihned",                   // "ihned" | "odlozena"
      "trigger": "...",                 // proč povinnost platí (lidsky)
      "zdroj": "z. 37/2021 Sb. ...",    // § + zákon (transparentnost / klik)
      "lhuta": "...", "verified": false,
      "semafor": "zelena",              // zelena=jisto | oranzova=ověřit | cervena=chybí data (HITL)
      "skryta": true,                   // baseline ji mine?
      "pokuta_kc": 500000 }             // expozice pokuty pokud propásnuto
  ],

  "nase_kody": ["..."],                 // naše kódy (po scoreru = ground truth)
  "baseline_kody": ["..."],             // co by dal naivní průvodce (split screen)
  "skryte_kody": ["DPH","SIDLO_OZNACENI","SKUTECNI_MAJITELE","ZAM_CSSZ","ZAM_ZP"],

  "plan": [                             // odložené povinnosti = HLÍDÁNÍ V ČASE (time-travel)
    { "povinnost": "DPH", "nazev": "...",
      "termin": "do 15 dnu po mesici prekroceni obratu",
      "duvod": "obrat 4 460 716 Kc > prah 2 000 000 Kc", "lhuta": "..." }
  ],

  "timeline": {                         // PROJEKCE konkrétních dat (time-travel + kalendář)
    "datum_zalozeni_cz": "22. 6. 2026", "mesicni_obrat": 371726,
    "udalosti": [                       // seřazeno dle termínu; typ: "ihned" | "projekce"
      { "povinnost": "DPH", "typ": "projekce",
        "udalost": "prekroceni obratu 2 mil. Kc",
        "datum_udalosti_cz": "3. 12. 2026",   // kdy událost nastane (projekce)
        "termin_cz": "15. 1. 2027", "za_dni": 207, "za_mesicu": 5.4,
        "predpoklad": "linearni rust obratu (rocni/12)" }   // jasně označeno = simulace
    ]
  },

  "uspora_kc": 720000,                  // ÚSPORA-meter (suma vyhnutých pokut)
  "riziko_breakdown": [                 // rozpad expozice po položkách
    { "kod": "SKUTECNI_MAJITELE", "castka": 500000, "typ": "max", "text": "...", "zdroj": "..." }
  ],

  "burden": 0,                          // founder_burden = otázky na zakladatele (0 = once-only)
  "registry_lookups": [                 // pro once-only animaci („ptáme se státu, ne tebe")
    { "typ": "ares", "klic": "21668732",
      "vysledek": "Partner Holding 10 s.r.o. - aktivni",
      "nahradil_otazku": "Existuje a je aktivni spolecnik-firma?" }
  ]
}
```

`/cases` (a `fixtures/cases.json`) → `[{id, nazev, predmet}, …]` pro výběr v UI.
`fixtures/eval.json` → čísla do pitch slidu (baseline 28/2 vs Společník 0/0, burden 0).

## Demo hero cases

- **FIRMA-0002** (e-shop, 4,46 mil., 2 zam.) → úspora **720 000 Kč**, 5 skrytých,
  3 odložené v plánu. Hlavní demo case.
- **FIRMA-0001** (účetnictví = **vázaná** živnost, provozovna) → ukáže, že baseline
  chybně hádá volnou živnost; my správně zatřídíme.
