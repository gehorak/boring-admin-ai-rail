# Traceability a důkazní kvalita

Tato mapa ukazuje, kde v profilu v0.2.2 ověřit hlavní tvrzení. Neuděluje
schválení a nenahrazuje review host projektu.

| Tvrzení | Zdroj v exportu | Co zdroj dokládá | Co nedokládá |
|---|---|---|---|
| Profil neprovádí práci | `DOCS/BOOTSTRAP-COMPLETE.md`, `DOCS/PUBLIC-DISTRIBUTION.md` | veřejnou hranici a CLI omezení | bezpečnost host projektu |
| Dokumenty mají ownera, stav a review | `public_rail/documents.py`, `templates/operational/` | implementované kontroly a šablony | správnost vyplnění host projektu |
| `READY` je odvozený stav | `public_rail/bootstrap.py`, `DOCS/BOOTSTRAP-COMPLETE.md` | podmínky stavu a invalidaci hashů | skutečnou připravenost týmu |
| Scope a role se kontrolují | `public_rail/requests.py`, `schemas/request.schema.json` | strukturu scope, role a moduly | lidskou vhodnost rozhodnutí |
| Evidence má pořadí a hash | `public_rail/evidence.py`, `schemas/evidence.schema.json` | kontrolované vazby a integritu artefaktů | pravdivost externího účinku |
| Balíček je hashovaný | `tests/verify_public_package.py`, `PUBLIC-MANIFEST.json` | integritu deklarovaného exportu | významovou správnost dokumentů |

## Úrovně podpory

- **Doloženo v exportu:** konkrétní soubor nebo test podporuje tvrzení.
- **Modelované:** příklad ukazuje doporučený postup, ne reálný výsledek.
- **Nedoložené:** export neobsahuje měření, produkční záznam nebo adopční
  studii, která by tvrzení potvrdila.

## Jak řešit rozpor

Pokud se vysvětlující text liší od schématu, kódu nebo veřejné hranice,
označ rozpor a aktualizuj ownera, FAQ, use case a tuto mapu. Historický nebo
interní dokument není automaticky aktuální veřejná autorita.

## Minimální důkaz pro pilot

Host projekt by měl uchovat alespoň intent, decision ownera, přesný scope,
authority sources, bootstrap manifest, authorization, review výsledek a
closure. Rozsah evidence má odpovídat riziku. Tento veřejný profil neurčuje
konkrétní úložiště ani nenahrazuje lokální bezpečnostní politiku.
