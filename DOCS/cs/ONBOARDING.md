# Onboarding: první bezpečný pilot

Veřejný v0.2.2 profil dává host projektu koleje pro AI-assisted práci:
explicitního lidského decision ownera, omezený scope, lokální kontrakty,
bootstrap review a dohledatelnou evidenci. Je to reference a offline kontrola,
ne automatická autorizace.

## Doporučené pořadí

1. Přečti [Proč AI Rail](./PROC-AI-RAIL.md), aby byl jasný problém a hranice.
2. Projdi [Jak to funguje](./JAK-TO-FUNGUJE.md), včetně stavů `UNPACKED` až
   `READY`.
3. Proveď [První pilot](./PRVNI-PILOT.md) na jednom malém, vratném úkolu.
4. Při nejasnosti použij [FAQ](./FAQ.md) nebo
   [Časté chyby a řešení](./CASTE-CHYBY-A-RESENI.md).

## Co musí být pravda před delivery

- `WORKSPACE.json` a pět autoritativních dokumentů odpovídá skutečnému host
  projektu;
- každý aktivní dokument má lidského ownera, platný review a `Document-Conflict:
  NONE`;
- `Selected-Modules` a `Change-Surfaces` jsou explicitní a každý surface má
  právě jeden vlastnický modul;
- `validate`, `status`, `freeze` a bootstrap review dávají konzistentní
  výsledek `READY`;
- request, output a evidence se vážou na jeden intent a stejný scope.

Pokud něco chybí, stav je `BLOCKED` nebo je práce stále bootstrap přípravou.
`DRAFT` není instrukce k implementaci a modelovaný příklad není schválení pro
jiný projekt.

## Co onboarding nedokazuje

CLI nedokazuje identitu člověka, produkční bezpečnost, kvalitu provideru ani
správnost externího účinku. Tyto otázky vyžadují vlastní kontrolu a důkaz
hostitelského projektu. Další hranice shrnuje
[Bezpečnostní hranice](./BEZPECNOSTNI-HRANICE.md).
