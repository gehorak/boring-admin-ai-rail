# Česká veřejná dokumentační sada

Česká vstupní vrstva k veřejnému Bootstrap-Complete profilu v0.2.2. Vysvětluje
proč AI Rail existuje, jak probíhá první pilot a kde končí veřejný balíček.
České texty jsou popularizační; normativní názvy kontraktů a CLI zůstávají
anglicky.

## Začni podle cíle

- [Proč AI Rail](./PROC-AI-RAIL.md) — problém, který řeší, a co zůstává mimo
  scope.
- [Jak to funguje](./JAK-TO-FUNGUJE.md) — průchod od záměru přes `READY` až po
  evidence.
- [První pilot](./PRVNI-PILOT.md) — bezpečný tutorial na malém fiktivním
  projektu.
- [Příklad repozitáře](./PRIKLAD-REPOZITARE.md) — worked example s mapou modulů,
  rozšířením scope a review.
- [Pro koho je Rail](./PRO-KOHO-JE-RAIL.md) — role, adopční cesty a limity pro
  solo ownera, tým i AI asistenta.
- [Bezpečnostní hranice](./BEZPECNOSTNI-HRANICE.md) — co znamená strukturální
  kontrola a co veřejný profil nedělá.
- [Časté chyby a řešení](./CASTE-CHYBY-A-RESENI.md) — praktické nálezy při
  prvním použití.

## Referenční navigace

- [Onboarding](./ONBOARDING.md) — krátká orientace před pilotem.
- [FAQ](./FAQ.md) — odpovědi na hranice a adopční otázky.
- [Slovník](./GLOSSARY.md) — česká vysvětlení při zachování contract names.
- [Use cases](./USE-CASES.md) — modelované situace, ne produkční důkazy.
- [Traceability](./TRACEABILITY.md) — tvrzení, zdroje, důkazní kvalita a
  rozpory.
- [Český rychlý start](../../QUICKSTART-CS.md) a
  [anglický quickstart](../../QUICKSTART.md).

## Veřejná hranice

Profil obsahuje dokumentaci, šablony, JSON kontrakty a standard-library CLI.
CLI ověřuje dodané dokumenty a data, ale nevolá model, neuděluje oprávnění,
neověřuje lidskou identitu a nic nevykonává. Executor, provider adapter,
sandbox, secrets, telemetry a model qualification runtime jsou mimo tento
profil. Úplný seznam je v [Security Hardening](../SECURITY-HARDENING.md) a
[Documentation Matrix](../DOCUMENTATION-MATRIX.md).
