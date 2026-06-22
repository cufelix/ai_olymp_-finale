# Demo skript — „Anna zakládá e-shop"

> Jeden běžící cyklus rozhodování. Reálný case **FIRMA-0002** (e-shop, obrat
> 4,46 mil. Kč, 2 zaměstnanci, společník z UA, bez provozovny). Všechno běží
> reálně — žádná lež, jen nablýskané divadlo.

## Layout: split screen

```
┌───────────────────────────┬───────────────────────────┐
│   BĚŽNÝ PRŮVODCE (baseline)│   SPOLEČNÍK (náš agent)   │
│                           │   ÚSPORA: 0 Kč  Dotazů: 0  │
├───────────────────────────┼───────────────────────────┤
│  ...                      │   ...                     │
└───────────────────────────┴───────────────────────────┘
```

## Scénář (krok po kroku)

1. **Anna zadá záměr** (jeden formulář vlevo i vpravo): s.r.o., provoz e-shopu,
   sídlo Brno, 2 společníci (1× holding s IČO, 1× FO z UA), plán 2 zaměstnanci,
   čekaný obrat ~4,5 mil.

2. **Baseline** vyplní 4 povinnosti → *„✅ Hotovo, firma založená!"* → **zšedne /
   usne**. (To je celý jeho život.)

3. **Společník místo ptaní DOHLEDÁVÁ** (animace volání nástrojů):
   - `lookup_registry('ares', '21668732')` → „Partner Holding 10 s.r.o. ✓ aktivní"
   - `lookup_registry('zivnost', 'Provoz e-shopu')` → „volná živnost ✓"
   - Counter: **Dotazů na zakladatele: 0** ← *once-only naživo* (vedle baseline,
     který by se ptal).

4. **Najde skryté povinnosti**, co baseline vynechal — rozsvítí
   `OZNAČENÍ SÍDLA` + `SKUTEČNÍ MAJITELÉ`. Každá **klikatelná → ukáže § zákona**
   (transparentnost = etický bod).

5. **ÚSPORA-meter naskočí** 🔴 — *„Skryté riziko: 3 přehlédnuté povinnosti →
   expozice až ~XX 000 Kč."* (riziko v korunách = B-hook). Breakdown po
   položkách s reálnými sazbami (viz `SPEC.md` §8).

6. **🚀 HERO MOMENT — přetočení času.** Tlačítko **„▶ Přetoč o 8 měsíců"**:
   - křivka obratu roste, **protne čáru 2 000 000 Kč**
   - agent vystřelí: *„🔔 Překročíš obrat pro DPH — přihláška do 15 dnů.
     Naplánováno na [datum]."* → reálně volá `schedule('FIRMA-0002', 'DPH', …)`
   - *„📅 Nástup 1. zaměstnance → ČSSZ + ZP do 8 dnů, pohlídám."* → `schedule(...)`

7. **Závěr na plátně:** vlevo „Hotovo" (šedé, mrtvé), vpravo **„Hlídám dál"** +
   kalendář budoucích povinností. ÚSPORA-meter ukazuje finální číslo.

> **Punchline:** *„Baseline skončil u založení. Společník teprve začíná."*

## Záložní case (kdyby chtěli druhý příklad)

**FIRMA-0001** (účetnictví, provozovna ano): baseline hádá `ZIVNOST_VOLNA`, ale
účetnictví je **vázaná živnost** → baseline má zároveň povinnost navíc (FP) i
chybí (FN). Ukáže, že Společník i **správně zatřídí regulovanou živnost**.

## Co musí reálně běžet (ne slide)

- Agent loop nad `tools.py` → vrací správné povinnosti (propásnuté 0 / zbytečné 0).
- `schedule()` se reálně volá → kalendář budoucích povinností je z dat, ne mockup.
- `founder_burden()` == 0 → counter „Dotazů: 0" je pravdivý.
- ÚSPORA-meter = součet reálných sazeb pokut z `SPEC.md` §8.

## Technická poznámka pro UI tým

Brain (Python `agent/`) vystaví tenké JSON API / CLI, které UI volá:
`POST /analyze {intent_id}` → `{ povinnosti[], skryte[], plan[], uspora_kc,
burden, citace[] }`. UI (Lovable/v0/Bolt) jen renderuje — logika je v brainu,
aby „pod tím byla reálná AI, ne formulář".
