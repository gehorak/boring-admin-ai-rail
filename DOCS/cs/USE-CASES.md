# Use cases

Následující situace jsou modelované profily pro adopci v0.2.2. Nejsou měřením,
reálnou case study ani univerzální autorizací.

## UC-01: první dokumentační pilot

**Situace:** Tým chce upravit README a doplnit lokální technické konvence.

**Minimum:** Jeden human decision owner, aktivní `PROJECT.md`, malý scope,
`CODEBASE-VOICE.md`, request, review a evidence closure.

**Ověření:** `validate-request`, `validate-output` a evidence chain ověří
strukturu a vazby, ale neověří kvalitu samotného návrhu.

## UC-02: změna chráněné integrační hranice

**Situace:** Návrh se dotkne externí služby, identity, credentials nebo dat.

**Minimum:** `INTEGRATION-POINTS.md`, vlastník hranice, security/data modul,
explicitní denied paths a samostatné lidské review.

**Hranice:** CLI nedává přístup, nevolá službu a nepotvrzuje bezpečnost změny.

## UC-03: rozšíření scope během práce

**Situace:** Objeví se další soubor, modul nebo vedlejší účinek mimo původní
request.

**Reakce:** Zastavit, zapsat nový scope, zkontrolovat vlastníka a vyžádat nové
rozhodnutí. Původní authorization se nesmí znovu použít pro širší práci.

## UC-04: chybějící nebo konfliktní pravda

**Situace:** Dokument nemá ownera, review je prošlé, hash nesedí nebo dva
authority sources říkají něco jiného.

**Reakce:** Stav `BLOCKED`, konkrétní finding a eskalace k decision ownerovi.
AI nesmí konflikt vyřešit tichým výběrem pohodlnějšího zdroje.

## UC-05: veřejný export dokumentace

**Situace:** Autor chce zveřejnit interní materiál.

**Kontrola:** Zachovat pouze přenositelné kontrakty, odstranit host-project
truth, memory, task evidence, secrets a privátní prompty, ověřit manifest a
oddělit popis od důkazu.

**Výsledek:** Export může být veřejný reference profil. Bez samostatného
runtime profilu nesmí být popsán jako autonomní nebo produkční systém.
