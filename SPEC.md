# Společník — AI právní spoluzakladatel

> **„Každý startup má technického cofoundera. My jsme ten právní."**
>
> Linie VEŘEJNÁ SPRÁVA · ČAIO 2026 národní finále · záštita Aricoma

---

## TL;DR

**Společník** je agentní AI systém, který tě **provede založením s.r.o.** a pak
**zůstane jako tvůj legální agent** na pozadí: sám si dohledá data v registrech,
odvodí z nich povinnosti (i ty skryté a odložené), **simuluje budoucnost firmy**
a upozorní tě na termín **dřív, než propásneš povinnost a přijde pokuta**.

Název je dvojsmysl: *společník* = parťák/cofounder **i** právní termín pro
společníka s.r.o. → tvůj AI **společník**, co řeší právní stranu firmy.

**K čemu to je: šetří ti peníze.** Jedna propásnutá povinnost = pokuta v řádu
desítek až stovek tisíc Kč. Společník stojí pár stovek měsíčně. Pojistka, co se
zaplatí stokrát.

---

## 1. Problém

Založit firmu je pakárna, ale to nejhorší přijde **až potom**. Část povinností
není z formuláře vidět — vyplývají z předmětu podnikání, z růstu firmy nebo z
času. Zakladatel něco propásne a po měsících mu to vyskočí jako **pokuta**.

Dnešní nástroje (online založení, Portál podnikatele, účetní) buď **skončí
okamžikem založení**, nebo jsou drahé a reaktivní. Nikdo firmu **proaktivně
nehlídá v čase**.

## 2. Řešení — co to je

AI **agent** (ne formulář), který má dvě fáze:

1. **Onboarding** — provede tě založením, sestaví registrace a povinnosti na
   míru záměru.
2. **Ongoing legal cofounder** — zůstává na pozadí a hlídá firmu dál v čase.

## 3. Pro koho (zákazník)

- **Primárně:** zakladatel a malá s.r.o. — typicky **jednatel + účetní**, co
  nemají právníka na telefonu.
- **B2B2C:** účetní a poradenské firmy (white-label pro jejich klienty).
- **Enterprise / stát:** úřad nabízí službu zakladatelům (Aricoma-friendly,
  otevírá to zadání samo).

## 4. Co to dělá — tři schopnosti, co formulář nikdy neudělá

Tohle je důkaz **„agent, ne formulář"** (a přesně to, co řekl zakladatel týmu):

1. **Sám odvozuje povinnosti** — i skryté a odložené, co z formuláře nejsou
   vidět (skuteční majitelé, označení sídla, správné zatřídění živnosti, DPH
   po překročení obratu, povinnosti vůči zaměstnanci).
2. **Kříží data z víc registrů** (ARES, OR, živnostenský) — ptá se **státu, ne
   tebe** (princip **once-only**). Co jde dohledat, nedotazuje.
3. **Simuluje budoucnost firmy** — kdy překročíš obrat pro DPH, kdy z prvního
   zaměstnance vznikne povinnost vůči ČSSZ/ZP — a **pohlídá termín dopředu**.

> Formulář skončí u „založeno". Společník teprve začíná.

## 5. Jak to funguje — architektura

```
INTENT (záměr firmy)
   │
   ▼
[LLM PLANNER]  ── agentní tool-use loop, sám volí co a kdy zavolá
   ├─ lookup_registry()   ← once-only: dohledá, místo aby se ptal (burden ↓)
   ├─ klasifikace oboru   ← i novel/free-text obory, co statická tabulka nezná
   └─ derivace skrytých + odložených povinností z volného textu
   │
   ▼
[RULE / LEGISLATION GROUNDING]  ← každá povinnost má § + práh + zdroj
   │                              (anti-halucinace: LLM navrhuje, zákon uzemní)
   ▼
[TEMPORAL ENGINE]  ← schedule() odložených povinností v čase (DPH, zaměstnanci)
   │
   ▼
[HUMAN-IN-THE-LOOP]  ← zelená/oranžová/červená dle jistoty; člověk potvrdí
   │
   ▼
PODKLAD (ne závazná rada) + úspora v Kč + kalendář budoucích povinností
```

**Proč hybrid (a ne jen LLM, ani jen pravidla):**
- Čisté if-else = „chytřejší formulář", porota strhne.
- Čistý LLM = může se sebevědomě mýlit (zadání to říká doslova).
- **Hybrid:** LLM dělá agentní plánování + derivaci + vysvětlení; citovaná
  legislativa každý závěr uzemní; člověk potvrdí. → odpovídá přímo na otázku
  poroty *„jak bráníte tomu, aby systém vydával neověřené závěry"*.

## 6. Datová zjištění + odvozená pravidla (build spec pro agenta)

Z 6 označených případů (`ukazkove_pripady.json`) jsme **zpětně odvodili přesná
pravidla**, kterými vznikl ground truth. Deterministická vrstva s nimi dává na
scoreru **propásnuté = 0, zbytečné = 0**; baseline nasbírá hromadu.

| Povinnost (kód) | Spouštěč | Předpis |
|---|---|---|
| `OR_ZAPIS`, `DPPO`, `DATOVKA`, `SIDLO_OZNACENI`, `SKUTECNI_MAJITELE` | **vždy** (každé s.r.o.) | z.o.k. 90/2012, z. 586/1992 §39, z. 300/2008, živn.z. §31, z. 37/2021 |
| `ZIVNOST_VOLNA / VAZANA / KONCESE` | `lookup_registry('zivnost', předmět)` | živn.z. 455/1991, přílohy 1–4 |
| `DPH` | obrat **> 2 000 000 Kč** | z. 235/2004 §6 |
| `ZAM_CSSZ` + `ZAM_ZP` | zaměstnanci **≥ 1** | z. 589/1992 / 48/1997, do 8 dnů |
| `PROVOZOVNA` | provozovna vyplněná | živn.z. 455/1991 §17 |

**Baseline vždy plivne to samé**, ať je záměr jakýkoli:
`OR_ZAPIS, DPPO, DATOVKA, ZIVNOST_VOLNA` → systematicky propásne 2–5 povinností
a navíc chybně hádá volnou živnost i u regulovaných oborů.

**Datové shapy** (pozor, liší se):
- `zamery_firem.json` (hlavní vstup přes `get_intent`): `predmet`,
  `predpokladany_obrat_rok`, `plan_zamestnancu`, `provozovna` (objekt|null),
  `spolecnici` (PO mají `ico` → dohledatelné v ARES).
- `ukazkove_pripady.json` (ground truth): `predmet`, `obrat`, `zamestnanci`,
  `provozovna` (bool), `spravne_povinnosti`, `baseline_povinnosti`.

**DPH nuance (killer detail do pitche):** práh 2 mil. Kč sedí na data i na zákon,
ALE **od 2025 se mechanika změnila** (počítá se za kalendářní rok, lhůta 10
pracovních dnů, přibyl horní práh 2 536 500 Kč). Od 2026 je nové **JMHZ**
(jednotné měsíční hlášení zaměstnavatele). → *„hlídáme i změny předpisů."*

## 7. Rozhraní k datům (`tools.py`)

```
get_intent(id)                  -> záměr firmy (vidí každý)
lookup_registry(typ, klíč)      -> 'ares' (klíč=IČO) | 'zivnost' (klíč=předmět)
lookup_legislation(téma)        -> předpis (placeholder → nahradit citacemi)
ask_founder(id, otázka)         -> dotaz na zakladatele (POČÍTÁ SE DO ZÁTĚŽE)
schedule(id, povinnost, termín) -> hlídání povinnosti v čase
founder_burden()                -> kolik dohledatelných otázek jsme položili (níž = líp)
```

**Cíl agenta:** `founder_burden() == 0` (vše dohledáno z registrů + záměru),
přitom propásnuté = 0. Each `ask_founder` je minus.

## 8. Úspora-ledger — reálné pokuty (ověřeno, zdroje viz níže)

| Skrytá povinnost (baseline propásne) | Reálná sankce |
|---|---|
| **Skuteční majitelé** nezapsáni | až **500 000 Kč** + **nesmíš vyplatit zisk z vlastní firmy** + pozastavená hlasovací práva |
| **Pozdní přihlášení zaměstnance** (ČSSZ) | až **100 000 Kč** za opomenutí |
| **Neohlášená provozovna** | až **50 000 Kč** |
| **Neoznačené sídlo** | až **20 000 Kč** (+ nedoložení titulu k sídlu až 10k) |
| **Pozdní registrace DPH** | doměření daně + penále 0,05 %/den (max 5 %) + úrok z prodlení |

**Demo hero case FIRMA-0002** (e-shop, obrat 4,46 mil., 2 zaměstnanci): baseline
propásne skuteční majitele + sídlo + DPH + 2× zaměstnance → **max. expozice
~670 000 Kč**, kterou Společník odchytí.

> **Hard hook (nezpochybnitelný):** „Bez zápisu skutečných majitelů si nesmíš
> vyplatit zisk z vlastní firmy." 500k uváděj jako zákonné maximum.

## 9. Jak se měří kvalita

`bodovac.py` porovná náš seznam povinností s baseline na označených případech:
- **propásnuté** (FN — povinnost, kterou jsme vynechali) → hlavní metrika, co nejníž
- **zbytečné navíc** (FP — povinnost, co neplatí) → ať nenakládáme vše
- **zátěž zakladatele** (`founder_burden`) → dohledatelné otázky

Cíl: **propásnuté 0, zbytečné 0, burden 0** vs. baseline, který propásne hodně.

## 10. Byznys model

- **Freemium:** založení **zdarma** (akvizice) → **„Společník" paušál ~299 Kč/měs**
  (hlídání + alerty + simulace).
- **ROI math:** 299 Kč/měs ≈ 3 600 Kč/rok vs. jediná vyhnutá pokuta = desítky až
  stovky tisíc → pojistka, co se zaplatí stokrát.
- **B2B2C:** white-label pro účetní firmy.
- **Enterprise/stát:** úřad licencuje a nabízí zakladatelům.
- **Sběr dat v čase:** čím déle firmu hlídá, tím přesnější predikce (termíny,
  změny předpisů, stav registrací).

## 11. Konkurence + odlišnost

| Konkurent | Co dělá | Kde je slabý |
|---|---|---|
| Zalozfirmu.cz / e-Firma | jednorázové online založení | **končí, když je firma založená; nehlídá v čase** |
| Portál podnikatele / občana | státní rozcestník | **neradí proaktivně, neodvozuje skryté povinnosti** |
| Účetní / právník | odborné poradenství | **drahé a reaktivní; neřeší dopředu** |

**Naše odlišnost (1 věta):** *„Jediný, kdo po založení hlídá dál, ptá se státu
místo tebe (once-only) a u každé povinnosti ukáže zákon."*

## 12. Etika a odpovědnost (20 % známky — povinné)

- **Odpovědnost:** agent připraví **podklad, ne závaznou radu**. Finální krok a
  odpovědnost zůstávají na člověku → proto u každé povinnosti potvrzení (HITL).
- **EU AI Act:** AI ve veřejné správě, co ovlivňuje práva = **riziková kategorie**.
  Proto nerozhodujeme za uživatele, jen navrhujeme a **citujeme zdroj**.
- **Rovný přístup:** plain-language režim + vícejazyčnost (v datech jsou
  zahraniční společníci, např. UA) — nesmí znevýhodnit toho, kdo neumí právničtinu.
- **Transparentnost:** systém u každého závěru ukáže, **z jakého registru a z
  jakého předpisu** vyšel → závěr jde ověřit.
- **Data & oprávnění:** výhoda „dohledám si to" platí jen tam, kde má agent
  zákonný titul k registrům — kdo a za jakých podmínek přístup dá, patří do
  byznys plánu i etiky.

## 13. Co stavíme (MVP scope) vs. rozšíření

**MVP (musí běžet v demu):**
- Agent loop nad `tools.py` → propásnuté 0 / zbytečné 0 / burden 0 na označených
  případech (proti baseline).
- Derivace skrytých + odložených povinností s citací §.
- `schedule()` odložených povinností (DPH, zaměstnanci) = hlídání v čase.
- Demo UI: split screen baseline vs. Společník + **ÚSPORA-meter** + **simulace
  budoucnosti** (přetočení času → DPH alert).

**Rozšíření (obhájit na slidu, stavět když zbyde čas):**
- Hlídání změn zákonů a jejich dopadu na konkrétní firmu (JMHZ 2026, DPH 2025).
- Predikce růstu obratu → kdy vznikne další povinnost.
- OCR/vytěžení dokumentů, koordinace víc úřadů kolem jedné události.

## 14. Rozdělení práce (návrh)

- **Agent brain + scoring** (Python, `agent/`): loop nad tools.py, pravidla +
  legislativa grounding, eval proti `bodovac.py`. → *primárně Claude/Tim.*
- **Demo UI** (Lovable/v0/Bolt nad brainem): split screen, ÚSPORA-meter, time slider.
- **Pitch deck + strategie**: deck dle `PITCH.md`, nácvik 3 min, Q&A munice.

## Zdroje (citace pro deck)

- ESM sankce: <https://www.konecna-zacha.com/shrnuti-povinnosti-a-sankci-spojenych-s-evidenci-skutecnych-majitelu/>
- ČSSZ pokuty: <https://www.podnikatel.cz/clanky/za-nepodani-prehledu-cssz-pokuta-az-50-000-korun-neprosvihnete-nejzazsi-terminy/>
- Označení sídla/provozovny (MPO): <https://mpo.gov.cz/cz/podnikani/zivnostenske-podnikani/aktualni-informace/dulezite---k-radnemu-oznaceni-sidla-a-zivnostenske-provozovny--275003/>
- DPH 2025 (Finanční správa): <https://financnisprava.gov.cz/cs/financni-sprava/novinky/novinky-2025/informace-ke-zmenam-v-platcovstvi-dph-2025>
- Pozdní DPH: <https://www.az-data.cz/clanky/co-kdyz-jsem-propasl-termin-registrace-dph>

> ⚠️ Čísla pokut jsou ověřená z výše uvedených zdrojů (sekundární). Před pitchem
> ideálně dohledat primární znění (e-Sbírka) — porota Aricoma se ptá na detail.
