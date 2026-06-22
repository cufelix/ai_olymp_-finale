# Pitch — Společník (3 min + deck)

> Živý pitch 3 min + 2 min Q&A. Hook v úvodu, dodržet čas, zvládnout dotazy.

## 3minutový scénář (časovaný)

| Čas | Blok | Co říct |
|---|---|---|
| **0:00** | **HOOK** | *„Založit firmu umí každý. Problém přijde za 8 měsíců — dopis s pokutou za něco, co ti nikdo neřekl."* (lidský příběh: Anna zakládá e-shop) |
| **0:15** | **Problém + zákazník** | Malá s.r.o. (jednatel + účetní). Část povinností není z formuláře vidět — skryté a odložené. Propásnutí = pokuta v desítkách až stovkách tisíc. |
| **0:45** | **Řešení + proč AGENT** | „Společník — váš AI právní spoluzakladatel." Ne formulář: **sám odvozuje povinnosti, kříží registry, simuluje budoucnost.** → **PUSŤ LIVE DEMO** (přetočení času → DPH alert). |
| **1:30** | **Důkaz vs. baseline** | Na označených případech: baseline propásne X povinností / naloží Y zbytečně, **my 0 / 0**. (Reálná čísla ze `bodovac.py`.) |
| **2:00** | **Konkurence + odlišnost** | „Zalozfirmu.cz a Portál podnikatele skončí u založení. Účetní je drahý a reaktivní. **My jediní hlídáme dál v čase a u každé povinnosti ukážeme zákon.**" |
| **2:20** | **Byznys** | Založení zdarma → hlídání za paušál ~299 Kč/měs. Jedna vyhnutá pokuta = stovky paušálů. Pojistka, co se zaplatí stokrát. |
| **2:40** | **Etika + close** | Podklad, ne závazná rada; člověk potvrzuje; citace zdrojů; EU AI Act = vysoké riziko, ošetřeno HITL. Close = callback na Annu: *„Anna pokutu nedostala. Protože měla Společníka."* |

## Deck — 6 slidů (dle zadání)

1. **Problém & zákazník** — „Co dostaneš po stisku tlačítka." Anna + skrytá pokuta.
2. **Řešení & proč agent** — Společník, tři schopnosti (odvozuje / kříží registry /
   simuluje budoucnost). V čem je samostatnější než formulář.
3. **AI model & kvalita** — architektura (LLM planner + grounding + temporal + HITL);
   na označených případech **0 propásnutých / 0 zbytečných** vs. baseline.
4. **Konkurence & odlišnost** — tabulka (Zalozfirmu / Portál podnikatele / účetní)
   + naše 1věta odlišnosti.
5. **Byznys model** — freemium → paušál; B2B2C přes účetní; enterprise/stát;
   sběr dat v čase = recurring příjem.
6. **Etika** — odpovědnost (HITL), EU AI Act (riziko), data & oprávnění,
   transparentnost (citace zdroje).

## Q&A — připravené odpovědi (2 min dotazů)

- **„Jak to napojíte reálně / kdo dá agentovi přístup k registrům?"**
  → ARES je dnes veřejné API; OR/ŽR/ESM přes zákonný titul a souhlas uživatele
  (delegace identity, datová schránka). Přístup a oprávnění je jádro eGov problému
  → je to v byznys plánu i v etice. MVP běží nad sandboxem reálného tvaru.
- **„Co když se LLM splete?"** → proto **negroundovaný závěr nikdy nevydáme jako
  jistotu**: každá povinnost má § + zdroj, nejistá jde k člověku (oranžová/červená),
  finální krok potvrzuje uživatel. Agent navrhuje, nerozhoduje.
- **„Čím jste lepší než [konkurent]?"** → jediní hlídáme **v čase** + **once-only**
  (ptáme se státu, ne uživatele) + **citujeme zdroj** u každé povinnosti.
- **„Není to jen chytřejší formulář?"** → ne: formulář se ptá a skončí. My
  dohledáváme z registrů, odvozujeme skryté/odložené povinnosti a plánujeme je v
  čase (`schedule`). To formulář neumí.
- **„EU AI Act?"** → AI ve veřejné správě ovlivňující práva = riziková kategorie;
  řešíme HITL, transparentností a tím, že nevydáváme závaznou radu.

## Tón

Money-first, konkrétní čísla, žádné buzzwordy. *„Demo je silnější než slide"* —
co tvrdíme, to v demu ukážeme reálně běžet.
