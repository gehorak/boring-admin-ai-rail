# Rychlý start pro veřejnou referenční distribuci

Tento balíček je veřejná, offline a neexekutující referenční distribuce
BORING-ADMIN-AI-RAIL. Je generován z neveřejného kanonického zdroje. Neupravuj
jej ručně a nepřenášej změny zpět do interního repozitáře.

## Co balíček dělá

`public_rail` ověřuje strukturu předaných dokumentů, požadavků a důkazů podle
zabalených schémat a šablon. Nevytváří schválení, nespouští nástroje, nevolá
model ani síťovou službu. Výsledek `ALLOWED` je pouze výsledek lokální
strukturální kontroly.

## Lokální ověření

```bash
python -m pip install --no-deps .
python -m public_rail --help
python -m unittest discover -s tests -v
python tests/verify_public_package.py
```

Tyto příkazy nevyžadují přístup ke kanonickému zdroji. Integritní kontrola
ověřuje úplný povolený strom a SHA-256 každého souboru uvedeného v
`PUBLIC-MANIFEST.json`.

## Kde pokračovat

Anglický přehled a odkazy jsou v [DOCS/INDEX.md](DOCS/INDEX.md). Pro hranice
adopce a bezpečnosti si přečti [DOCS/ADOPTION.md](DOCS/ADOPTION.md) a
[DOCS/SECURITY-BOUNDARY.md](DOCS/SECURITY-BOUNDARY.md).
