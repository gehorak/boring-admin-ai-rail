# První pilot: malá dokumentační změna

## Cíl a hranice

Pilot doplní část `README.md` o krátké vysvětlení lokálního testování CI.
Nevolá model, nespouští nástroje, nemění workflow a nepřistupuje k produkci.
Výstupem je pouze návrh dokumentační změny, který projde lidským review.

## 1. Vyber malý úkol

Zapiš jednu větu: „Chci vysvětlit, jak se lokálně spouští existující testy.“
Mimo rozsah jsou kód, credentials, deployment, workflow a všechny soubory mimo
README. Jeden člověk bude `decision owner`.

## 2. Inicializuj contract root

V kořeni hostitelského repozitáře spusť:

```text
python -m public_rail init --target docs/ai-rail
```

`init` zkopíruje šest operational šablon, vytvoří `WORKSPACE.json`,
placeholder `BOOTSTRAP-MANIFEST.json` a adresář `evidence/`. Výsledek je
`UNPACKED`. `--force` používej jen při vědomém přepsání.

## 3. Vyplň workspace a autoritativní dokumenty

V `WORKSPACE.json` nahraď placeholdery skutečným `workspace_id`, názvem
repozitáře, `contract_root` a ponech `allowed_repository_root: "."`.

V `PROJECT.md` uveď lidského ownera, účel, in-scope a out-of-scope oblasti,
`Selected-Modules: development` a `Change-Surfaces: application_code` nebo
konkrétní surface, který projekt skutečně používá. Doplň
`PROJECT-CONTEXT.md`, `ARCHITECTURE-CANON.md`, `CODEBASE-VOICE.md` a podle
potřeby `INTEGRATION-POINTS.md`. Každý aktivní dokument musí mít vlastníka,
`Contract-Status: ACTIVE`, `Review-Date` a `Document-Conflict: NONE`.

## 4. Zkontroluj bootstrap

```text
python -m public_rail validate --root docs/ai-rail
python -m public_rail status --root docs/ai-rail
```

Po inicializaci je očekávaný stav `UNPACKED`, později `SEEDED` nebo `MAPPED`.
Oprav nálezy místo jejich obcházení: chybějící owner, placeholder, prázdný
scope nebo prošlé datum znamenají, že se nedá bezpečně pokračovat.

## 5. Freeze a bootstrap review

```text
python -m public_rail freeze --root docs/ai-rail --manifest-id ci-readme-001
```

`freeze` lze provést až ve stavu `MAPPED` nebo `READY` a vrátí
`STRUCTURALLY_VALID`. Doplň `BOOTSTRAP-REVIEW.md`: reviewer, decision owner,
workspace, manifest hash, výsledek `READY` a platnost review. Poté:

```text
python -m public_rail status --root docs/ai-rail
```

Výsledek může být `READY`. `READY` pouze říká, že bootstrap je strukturálně
konzistentní; není to povolení ke spuštění modelu nebo změny.

## 6. Vytvoř a validuj request

Request je JSON podle [request schema](../../schemas/request.schema.json).
Musí obsahovat jeden `intent_id`, actor, roli, action, scope, vybrané moduly,
change surfaces, authority sources, frozen manifest hash, `authorization_ref`
a `execution_capability: false`.

```text
python -m public_rail validate-request request.json --root docs/ai-rail
```

Validní výsledek je `AUTHORIZATION_RECORD_CONSISTENT`. Pokud request uvede
surface mimo `PROJECT.md`, cestu v denied scope nebo AI actor roli
`System Architect`, výsledek je `BLOCKED`.

## 7. Příklad outputu

Minimální tvar podle [output schema](../../schemas/output.schema.json):

```json
{
  "request_id": "request-001",
  "intent_id": "intent-001",
  "workspace_id": "demo-repo",
  "role": "Senior Developer",
  "actor": {
    "type": "human",
    "id": "github:developer",
    "delegation_ref": null,
    "model_registry_ref": null,
    "model_evaluation_ref": null,
    "model_version": null
  },
  "action_mode": "propose_changes",
  "execution_capability": false,
  "artifacts": [
    {"path": "README.md", "change_kind": "documentation"}
  ]
}
```

Ověř jej:

```text
python -m public_rail validate-output request.json output.json --root docs/ai-rail
```

`README.md` v povoleném scope může projít. `../secrets.txt`, `.env` nebo
`.git/config` musí skončit `BLOCKED`. Validator ověřuje deklarovaný path a
scope; neprokazuje skutečný diff ani kvalitu textu.

## 8. Evidence a closure

Vytvoř intent, authorization, output, review result a closure podle schémat v
`schemas/`. Zapiš je do contract rootu a v `evidence.json` je propojíš
`previous_record_id`, `artifact_sha256`, `request_ref`, `intent_id` a
`workspace_id`.

```text
python -m public_rail validate-evidence evidence.json --root .
```

Úspěšný výsledek je `EVIDENCE_CHAIN_VALID`. Reviewer může zapsat
`REJECTED`; pak closure nesmí tvrdit `APPROVED`. Evidence chain je
rekonstruovatelná strukturální stopa, ne důkaz externího provedení.

## 9. Co pilot neprovedl

Public profil v tomto pilotu nevolal AI, neaplikoval patch, necommitoval,
nepoužil síť, sandbox, secrets broker ani tool runtime. Tyto schopnosti musí
host projekt řešit odděleně, pokud je vůbec potřebuje.

## Když se stav změní

Úprava zmrazeného dokumentu po `freeze` zneplatní manifest a `status` přejde
na `BLOCKED`. To je očekávaná ochrana proti práci nad jinou projektovou pravdou.

Další pomoc najdeš v [Častých chybách](./CASTE-CHYBY-A-RESENI.md) a
[bezpečnostní hranici](./BEZPECNOSTNI-HRANICE.md).
