# Jak Společník funguje — fact sheet pro pitch deck

> Zdroj **reálných** faktů a čísel pro deck. Zároveň = technické shrnutí na 1 A4
> do odevzdání. Vše níže je ověřené z `agent/` (čísla ze scoreru, ne odhady).
> ⚠️ Sekce „real vs simulace" čti pozorně — ať deck netvrdí nic, co v Q&A neobhájíme.

## Co to je (1 věta)

AI **právní spoluzakladatel**: provede založením s.r.o. a pak **hlídá firmu v čase**
— sám odvodí povinnosti, dohledá je v registrech (once-only) a upozorní **před
pokutou**.

## Co dělá — 3 schopnosti („agent, ne formulář")

1. **Odvozuje skryté/odložené povinnosti** — skuteční majitelé, označení sídla,
   DPH po překročení obratu, povinnosti vůči zaměstnanci. (Co formulář nevidí.)
2. **Kříží registry místo ptaní** — ARES (společníci), klasifikace živnosti →
   ptá se **státu, ne uživatele** (princip once-only).
3. **Simuluje budoucnost** — projektuje konkrétní termíny (DPH za ~5 měsíců →
   datum) a hlídá je dopředu.

## Jak to funguje (kde je reálná AI)

```
ZÁMĚR → [PLANNER: agentní rozhodování, sám volí co dohledá]
          → lookup_registry (once-only)  → derivace skrytých/odložených povinností
        → [GROUNDING: každá povinnost má § zákona]   ← anti-halucinace
        → [TIMELINE: projekce termínů v čase]
        → [HUMAN-IN-THE-LOOP: semafor, člověk potvrdí]
        → PODKLAD (ne závazná rada) + úspora v Kč + kalendář
```

Reálná AI = agentní plánování + derivace + grounding, ne vyplněný formulář.

## 🎯 DŮKAZ — reálná čísla (slide „kvalita / AI model")

| Metrika (na 6 označených případech) | Baseline | **Společník** |
|---|---|---|
| Propásnuté povinnosti | **28** | **0** |
| Zbytečně naložené | **2** | **0** |
| Otázky na zakladatele (zátěž) | — | **0** (once-only) |

**Demo case FIRMA-0002** (e-shop, obrat 4,46 mil., 2 zam.): úspora **720 000 Kč**,
**5 skrytých povinností** odchyceno (DPH, sídlo, skuteční majitelé, ČSSZ, ZP).

## Odkud bere data — REÁLNÉ vs SIMULOVANÉ (pozor na Q&A)

| Co | Teď (reálně běží) | V produkci (slide) |
|---|---|---|
| Data o firmě | sandbox `get_intent` (reálného tvaru) | onboarding + předvyplnění z registrů |
| ARES / živnost | sandbox `lookup_registry` | živé ARES API, RŽP |
| Legislativa (§, prahy) | researchnutá KB v `legislation.py` | sledování novel (ROADMAP) |
| **Čas / timeline / kalendář** | **SIMULACE** (projekce z obratu) | reálné události (založení, banka, HR) |

➡️ **NEtvrdit** v pitchi živé napojení na ARES ani reálné hodiny. Registry = sandbox
reálného tvaru přes oficiální rozhraní; časová osa = **projekce** (každá budoucí
položka má `predpoklad`). Tohle je naopak silné: *„živé napojení a zákonný titul
k registrům je ten eGov problém — patří do byznys plánu a etiky."*

## Klíčová fakta + citace (pro slidy a Q&A)

- **DPH práh 2 000 000 Kč**; od 2025 reforma (počítá se za kalendářní rok, lhůta
  10 prac. dnů, horní práh 2 536 500 Kč); od 2026 **JMHZ** → *„hlídáme i změny předpisů"*.
- **Skuteční majitelé**: až **500 000 Kč** + **nelze vyplatit zisk z vlastní firmy**.
- **ČSSZ** (zaměstnanec) až **100 000 Kč** · **provozovna** 50k · **sídlo** 20k.
- Zdroje: ESM (konecna-zacha.com), ČSSZ (podnikatel.cz), MPO (sídlo/provozovna),
  Finanční správa (DPH 2025). Plné odkazy v `SPEC.md` §8.

## Co běží v demu vs co je slide

- **Demo (reálné):** split screen vs baseline · once-only counter (0 otázek) ·
  skryté povinnosti se zdrojem · ÚSPORA-meter · **time-travel** (projekce termínů) ·
  předvyplněný formulář + zelené potvrzení.
- **Slide (nestavíme):** živé registry API, odeslání přes datovku, 34 skrytých
  případů, B2B2C dashboard pro účetní.

## Etika (1 blok do slidu)

Podklad, **ne závazná rada** · člověk potvrzuje (HITL, semafor) · **citace § u každé
povinnosti** (transparentnost) · EU AI Act: AI ve veřejné správě = riziková kategorie
→ nerozhodujeme za uživatele, jen navrhujeme.

---
*Technický detail a JSON kontrakt: [`agent/README.md`](./agent/README.md). Demo
scénář: [`DEMO.md`](./DEMO.md). Konkurence: [`KONKURENCE.md`](./KONKURENCE.md).*
