# Use cases

Následující situace jsou modelované profily pro adopci v0.2.2. Nejsou měřením,
reálnou case study ani univerzální autorizací.

## UC-01: solo owner a první dokumentační pilot

**Situace:** Jeden člověk chce bezpečně upravit README nebo lokální konvence.

**Minimum:** Decision owner, `PROJECT.md`, malý scope, `CODEBASE-VOICE.md`,
request, review a closure. AI není nutná; pokud pomáhá, zůstává v přidělené
roli a `DRAFT` výstup není automaticky schválen.

## UC-02: dokumentace a kódová změna

**Situace:** Tým navrhuje změnu dokumentace nebo aplikačního kódu.

**Minimum:** Aktivní autoritativní dokumenty, vlastnický module/surface,
explicitní denied paths, request a nezávislé review. `validate-output` ověří
strukturu a vazby, nikoli kvalitu návrhu.

## UC-03: CI jako kontrolní krok

**Situace:** Repozitář chce spouštět strukturální kontrolu v CI.

**Minimum:** CI pouze zavolá standard-library CLI a zachová jeho výstup.
Rail nenahrazuje testy, deploy policy, secret scanning ani schválení merge.

## UC-04: infrastruktura nebo externí integrace

**Situace:** Návrh se dotkne identity, credentials, sítě, dat nebo externí
služby.

**Minimum:** `INTEGRATION-POINTS.md`, security/data/infrastructure modul,
vlastník hranice, denied paths a samostatné lidské review.

**Hranice:** CLI nedává přístup, nevolá službu a nepotvrzuje bezpečnost změny.

## UC-05: rozšíření scope během práce

**Situace:** Objeví se další soubor, modul nebo vedlejší účinek mimo request.

**Reakce:** Zastavit, zapsat nový scope, zkontrolovat vlastníka a vyžádat nové
rozhodnutí. Původní authorization se nesmí znovu použít pro širší práci.

## UC-06: model qualification evidence

**Situace:** Tým chce přiložit registry nebo evaluation report modelu.

**Reakce:** Evidence se validuje jako dodaný datový artefakt. `PASS` neznamená
ověřeného vydavatele, bezpečný runtime ani oprávnění k nasazení.

## UC-07: chybějící nebo konfliktní pravda

**Situace:** Dokument nemá ownera, review je prošlé, hash nesedí nebo dva
authority sources říkají něco jiného.

**Reakce:** Stav `BLOCKED`, konkrétní finding a eskalace k decision ownerovi.
AI nesmí konflikt vyřešit tichým výběrem pohodlnějšího zdroje.

## UC-08: veřejný export dokumentace

**Situace:** Autor chce zveřejnit interní materiál.

**Kontrola:** Zachovat pouze přenositelné kontrakty, odstranit host-project
truth, memory, task evidence, secrets a privátní prompty, ověřit manifest a
oddělit popis od důkazu.

**Výsledek:** Export může být veřejný reference profil. Bez samostatného
runtime profilu nesmí být popsán jako autonomní nebo produkční systém.
