# Česká veřejná dokumentační sada

Tato sada je český vstup do veřejného Bootstrap-Complete profilu v0.2.2.
Vysvětluje přenositelné kontrakty, offline validaci a hranice balíčku. Není
interním provozním manuálem ani důkazem produkční bezpečnosti.

## Pro koho je sada určena

- pro člověka, který framework dosud nezná;
- pro developera nebo operátora při prvním pilotu;
- pro reviewera, který ověřuje autoritu, scope a důkazy;
- pro autora veřejné dokumentace, který odděluje přenositelné kontrakty od
  interního know-how.

## Doporučené pořadí čtení

1. [Onboarding](./ONBOARDING.md) — pětiminutová orientace a první pilot;
2. [FAQ](./FAQ.md) — hranice a časté omyly;
3. [Slovník](./GLOSSARY.md) — české a anglické termíny;
4. [Use cases](./USE-CASES.md) — modelované situace a adopční profily;
5. [Traceability](./TRACEABILITY.md) — zdroje, důkazní kvalita a rozpory.

## Veřejná hranice

Profil obsahuje dokumentaci, šablony, datové kontrakty a standard-library CLI.
CLI ověřuje dodané dokumenty a data, ale nevolá model, neuděluje oprávnění,
neověřuje lidskou identitu a nic nevykonává. Executor, provider adapter,
sandbox, secrets, telemetry a model qualification runtime jsou mimo tento
profil.

Začni také [QUICKSTART.md](../../QUICKSTART.md),
[BOOTSTRAP-COMPLETE.md](../BOOTSTRAP-COMPLETE.md) a hranicí
[PUBLIC-DISTRIBUTION.md](../PUBLIC-DISTRIBUTION.md).
