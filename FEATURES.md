# Featury — Společník (co konkrétně umí)

> **Legenda:**
> 🟢 **[DEMO]** = reálně běží v živém demu (postavíme)
> 🟡 **[DEMO-vizuál]** = v demu vidět, data reálná, akce naznačená
> 🔵 **[ROADMAP]** = produkční vize, jen na slidu (nestavíme)

---

## A. Onboarding — provede tě založením

| # | Featura | Co dělá | Tag |
|---|---|---|---|
| A1 | **Zadání záměru** | Founder zadá: forma, předmět, sídlo, společníci, obrat, plán zaměstnanců | 🟢 |
| A2 | **Plán registrací na míru** | Agent sestaví seznam povinností k založení podle záměru | 🟢 |
| A3 | **Baseline srovnání** | Vedle ukáže, co by zvládl běžný průvodce (split screen) | 🟢 |

## B. Tři agentní schopnosti (jádro „agent, ne formulář")

| # | Featura | Co dělá | Tag |
|---|---|---|---|
| B1 | **Odvození skrytých povinností** | Z předmětu/obratu/zaměstnanců odvodí i to, co ve formuláři není: skuteční majitelé, označení sídla, regulovaná živnost, provozovna | 🟢 |
| B2 | **Křížení registrů (once-only)** | `lookup_registry`: ARES (IČO společníků), klasifikace živnosti. Ptá se státu, ne foundera → counter **„Dotazů na zakladatele: 0"** | 🟢 |
| B3 | **Simulace budoucnosti** | Time-travel: projekce obratu → práh DPH (2 mil.); první zaměstnanec → ČSSZ/ZP. Naplánuje termíny dopředu (`schedule`) | 🟢 |

## C. Hlídání v čase (po založení)

| # | Featura | Co dělá | Tag |
|---|---|---|---|
| C1 | **Kalendář povinností** | Odložené povinnosti s termíny, vizuálně na časové ose | 🟢 |
| C2 | **Včasné alerty** | Upozornění před deadlinem („DPH přihláška do 15 dnů") | 🟢 |
| C3 | **Hlídání změn předpisů** | Sleduje novely (DPH 2025, JMHZ 2026) a jejich dopad na konkrétní firmu | 🔵 |
| C4 | **Stav registrací** | Sleduje, co je podáno / čeká / hotovo | 🔵 |

## D. Akční režim — předvyplněná podání (s tvým povolením)

| # | Featura | Co dělá | Tag |
|---|---|---|---|
| D1 | **Předvyplnění podání** | Vygeneruje vyplněný formulář z dohledaných dat (přihláška DPH, ohlášení živnosti/provozovny…) | 🟡 |
| D2 | **Provenience u každého pole** | „Sídlo z RÚIAN, IČO z ARES" — nic si nevymýšlí; co nedohledá, flagne | 🟡 |
| D3 | **Permission gate (semafor)** | 🟢 zelená = klik potvrdit · 🟡 oranžová = zkontroluj · 🔴 červená = chybí data, zeptá se | 🟢 |
| D4 | **Odeslání přes datovou schránku** | Reálné podání na úřad | 🔵 |
| D5 | **Audit trail** | Kdo co potvrdil a kdy (odpovědnost při chybě) | 🔵 |

## E. Transparentnost, peníze & důvěra

| # | Featura | Co dělá | Tag |
|---|---|---|---|
| E1 | **Citace zdroje u každé povinnosti** | § zákona + registr, klikatelné → ověřitelné | 🟢 |
| E2 | **ÚSPORA-meter** | Kolik Kč na pokutách ti to zatím ušetřilo (reálné sazby) | 🟢 |
| E3 | **Riziko v Kč (breakdown)** | Co baseline propásl = expozice po položkách | 🟢 |
| E4 | **Plain-language vysvětlení** | Vysvětlí povinnost lidsky (i cizí jazyk — UA founder) | 🟡 |

## F. Rozšíření (jen slide, nestavíme)

- **Predikce růstu** — z trendu obratu odhadne, kdy vznikne další povinnost.
- **OCR / vytěžení dokumentů** — nahraj smlouvu/fakturu, agent vytěží údaje.
- **Koordinace víc úřadů** kolem jedné události (např. zaměstnání cizince).
- **Dashboard pro účetní firmy** (B2B2C) — všichni klienti a jejich termíny na jednom místě.

---

## Co je „pod tím" reálně (anti-formulář důkaz)

Brain (Python `agent/`) nad `tools.py`: derivace povinností z pravidel uzemněných
v zákonech (viz `SPEC.md` §6) + `schedule()` odložených + `founder_burden()==0`.
Na označených případech ověřeno přes `bodovac.py`: **0 propásnutých / 0 zbytečných
vs baseline.** UI jen renderuje výstup brainu → „pod tím je reálná AI, ne formulář".

## Demo = které featury jsou na pódiu vidět

Pořadí v demu (viz `DEMO.md`): A1→A2→A3 (split screen) · B2 (once-only counter) ·
B1 (skryté povinnosti) · E2/E3 (úspora + riziko) · **B3 (přetočení času → DPH alert)** ·
D1/D3 (předvyplněné podání + zelené potvrzení) · C1 (kalendář). Vše ostatní = slide.
