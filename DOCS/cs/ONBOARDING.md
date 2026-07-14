# Onboarding: první bezpečný pilot

## Za pět minut

Veřejný v0.2.2 profil dává host projektu koleje pro AI-assisted práci:
explicitního lidského decision ownera, omezený scope, lokální kontrakty,
bootstrap review a dohledatelnou evidenci. Je to reference a offline kontrola,
ne automatická autorizace.

## První pilot

1. Spusť `python -m public_rail init --target docs/ai-rail`.
2. Vyplň `WORKSPACE.json` a pět autoritativních dokumentů. Začni
   `PROJECT.md`, potom doplň kontext, architekturu, codebase voice a integrační
   body podle skutečné potřeby.
3. Každý dokument drž ve strict front matter: typ, stav, schema verzi,
   lidského ownera, datum review a konflikt `NONE`.
4. V `PROJECT.md` explicitně uveď `Selected-Modules` a `Change-Surfaces`.
   Každý aktivní surface musí mít právě jeden vlastnický modul.
5. Spusť `validate`, oprav nálezy a proveď `freeze`. Bootstrap review smí
   označit `READY` až po kontrole dokumentů, hashů, workspace a data platnosti.
6. Teprve potom validuj request, output a evidence řetězec. Nic z toho samo
   nespouští změnu.

## Kontrola před prací

Reviewer musí být schopen odpovědět:

- Kdo je lidský decision owner a kdo pouze reviewuje?
- Co je v rozsahu, mimo rozsah a `do-not-touch`?
- Který dokument a manifest jsou autoritativní?
- Který modul vlastní každý aktivní change surface?
- Jaké request, authorization, output a evidence artefakty se váží k jednomu
  intentu?

Pokud odpověď chybí, stav je `BLOCKED` nebo vyžaduje další bootstrap práci.
`DRAFT` není instrukce k implementaci a modelovaný příklad není schválení pro
jiný projekt.

## Co onboarding nedokazuje

CLI nedokazuje identitu člověka, produkční bezpečnost, kvalitu provideru ani
správnost externího účinku. Tyto otázky vyžadují vlastní kontrolu a důkaz
hostitelského projektu.
