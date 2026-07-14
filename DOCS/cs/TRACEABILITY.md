# Traceability a důkazní kvalita

Traceability není jen seznam hashů. Pro jedno tvrzení musí být dohledatelné,
odkud pochází, kdo o něm rozhodl, jak vznikl technický artefakt, co bylo
ověřeno a zda došlo k externímu účinku. Tato mapa ukazuje, kde v profilu v0.2.2
ověřit hlavní části řetězce; nenahrazuje review host projektu.

| Část řetězce | Příklad zdroje v exportu | Co lze doložit | Co zůstává na host projektu |
|---|---|---|---|
| Origin / authority | `PROJECT.md`, `PROJECT-CONTEXT.md`, `ARCHITECTURE-CANON.md` | deklarovaný účel, hranice a autorita | zda dokument odpovídá realitě |
| Human decision | `BOOTSTRAP-REVIEW.md`, authorization record | owner, rozhodnutí, scope a platnost | identitu a organizační oprávnění člověka |
| Technical artifact | request/output/evidence JSON, cesta a hash | vazbu intentu, změny a review | kvalitu kódu, testy a skutečný diff |
| Validation | `public_rail/bootstrap.py`, `requests.py`, `evidence.py` | strukturální konzistenci, pořadí a integrity | vhodnost rozhodnutí a provozní bezpečnost |
| External effect | closure record a lokální provozní důkazy | že byl účinek popsán v řetězci | zda byl externí systém opravdu změněn bezpečně |

## Úrovně podpory

- **Doloženo v exportu:** konkrétní soubor nebo test podporuje tvrzení.
- **Modelované:** příklad ukazuje doporučený postup, ne reálný výsledek.
- **Nedoložené:** export neobsahuje měření, produkční záznam nebo adopční
  studii, která by tvrzení potvrdila.

## Jak řešit rozpor

Pokud se vysvětlující text liší od schématu, kódu nebo veřejné hranice,
označ rozpor a aktualizuj ownera, FAQ, use case a tuto mapu. Historický nebo
interní dokument není automaticky aktuální veřejná autorita. Hash dokládá
integritu konkrétního obsahu, nikoli jeho pravdivost.

## Minimální důkaz pro pilot

Host projekt by měl uchovat alespoň intent, decision ownera, přesný scope,
authority sources, bootstrap manifest, authorization, review výsledek a
closure. Rozsah evidence má odpovídat riziku. Tento veřejný profil neurčuje
konkrétní úložiště ani nenahrazuje lokální bezpečnostní politiku.
