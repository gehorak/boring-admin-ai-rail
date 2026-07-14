# Rychlý start pro public operational profil

Tento profil rozšiřuje malý Adoption Kit o bootstrap, role, moduly, workflow a
datové kontrakty. Neinstaluje runtime ani nedává AI oprávnění něco vykonat.

1. Začni podle `QUICKSTART.md` a vytvoř lokální `PROJECT.md`.
2. Urči lidského decision ownera a vyber jen moduly odpovídající skutečným
   change surfaces.
3. Doplň boundaries, codebase voice, integrační body a do-not-touch areas.
4. Pro každý aktivní change surface zapiš právě jeden vlastnický modul podle
   `ARCHITECTURE/MODULE-COMPOSITION.md`.
5. Proveď bootstrap review pomocí `templates/BOOTSTRAP-REVIEW.md`.
6. Až výsledek `READY` dovolí přejít k omezené delivery práci podle
   `WORKFLOW.md`.

Před `READY` je povolené pouze read-only mapování, doplnění projektu a
vyjasňování. Role ani JSON Schema nepředstavují tool permission, request gate
nebo executor. `validators/validate_operational_profile.py` pouze ověřuje
zadané dokumenty a data; nic nevykonává.
