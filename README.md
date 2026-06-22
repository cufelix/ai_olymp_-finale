# Společník — AI právní spoluzakladatel

> **„Každý startup má technického cofoundera. My jsme ten právní."**
>
> ČAIO 2026 · národní finále · linie VEŘEJNÁ SPRÁVA (záštita Aricoma)

AI agent, který tě **provede založením s.r.o.** a pak **zůstane jako tvůj legální
agent**: sám odvozuje povinnosti (i skryté a odložené), kříží data z víc registrů
(once-only — ptá se státu, ne tebe), **simuluje budoucnost firmy** a upozorní na
termín **dřív, než propásneš povinnost a přijde pokuta**.

**K čemu: šetří ti peníze.** Propásnutá povinnost = pokuta v desítkách až stovkách
tisíc. Společník stojí pár stovek měsíčně. Pojistka, co se zaplatí stokrát.

## Dokumentace

| Dokument | Obsah |
|---|---|
| [**SPEC.md**](./SPEC.md) | Master spec: koncept, zákazník, architektura, odvozená pravidla z dat, API, úspora-ledger (pokuty + zdroje), byznys, etika, scope, rozdělení práce |
| [**PITCH.md**](./PITCH.md) | 3min pitch (časovaný) + 6 slidů decku + Q&A munice |
| [**DEMO.md**](./DEMO.md) | Live demo skript „Anna zakládá e-shop" (split screen + ÚSPORA-meter + simulace budoucnosti) |

## Stav

- [x] Koncept zamčený (Společník = legal cofounder, money-first)
- [x] Datová analýza + zpětně odvozená grading pravidla (propásnuté 0 / zbytečné 0)
- [x] Reálné sazby pokut ověřené se zdroji
- [ ] Agent brain (Python, nad `tools.py`) — beat baseline na scoreru
- [ ] Demo UI (split screen, ÚSPORA-meter, time slider)
- [ ] Pitch deck (design dle PITCH.md)
