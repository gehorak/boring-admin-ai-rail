# Časté chyby a řešení

Bezpečný postup je nález pochopit, opravit v autoritativním zdroji a znovu
validovat. Validaci neobcházej změnou výstupu nebo ručním předstíráním stavu.

## Bootstrap a dokumenty

### `UNPACKED` po inicializaci

**Znamená:** šablony existují, ale `WORKSPACE.json` nebo projektová pravda má
placeholdery. **Příčina:** `init` je jen první krok. **Oprava:** vyplň ownera,
účel, hranice, workspace a moduly; spusť `validate`. **Neobcházet:** neoznačuj
`READY` ručně.

### Chybějící nebo neaktivní dokument

**Znamená:** povinný authoritative document chybí nebo nemá `ACTIVE`.
**Oprava:** doplň skutečný dokument, ownera, review datum a `Document-Conflict:
NONE`. **Neobcházet:** `DRAFT` není instrukce.

### Placeholder v dokumentu

**Znamená:** zůstal text jako `<workspace-id>`. **Oprava:** nahraď jej reálnou
projektovou hodnotou nebo záměrně použij platné `N/A`, pokud to kontrakt dovolí.
**Neobcházet:** nemaž nález bez vyplnění pravdy.

### Prošlé review datum

**Znamená:** dokument nebo bootstrap review už není platný. **Oprava:** člověk
prověří obsah a nastaví nové datum. **Neobcházet:** neposouvej datum bez review.

### Nesoulad manifest hash

**Znamená:** dokument se změnil po `freeze`. **Oprava:** zkontroluj změnu,
proveď nové `freeze` a nové bootstrap review. **Neobcházet:** nepřepisuj hash
jen proto, aby kontrola prošla.

### `READY` se změnilo na `BLOCKED`

**Znamená:** frozen dokument, workspace, review nebo linková bezpečnost už
nesedí. **Oprava:** přečti konkrétní findings a oprav zdrojovou příčinu.
**Neobcházet:** `READY` není trvalé oprávnění.

## Scope, role a authorization

### Scope nepokrývá artefakt

**Znamená:** cesta není v allowed paths, je v denied paths nebo překračuje
segmentový glob. **Oprava:** zvaž, zda má být nový artefakt skutečně v intentu;
pokud ano, nech scope rozhodnout ownera. **Neobcházet:** nepoužívej širší `**`
jen kvůli pohodlí.

### Denied path blokuje output

**Znamená:** návrh míří do `.env`, `.git`, secrets nebo jiné zakázané cesty.
**Oprava:** odstraň artefakt nebo vytvoř nový explicitní lidský návrh s
bezpečnostním review. **Neobcházet:** neodstraňuj denied rule.

### Role nemůže provést action

**Znamená:** role/action matrix nepovoluje daný krok. **Oprava:** zkontroluj,
zda akci skutečně dělá správná role a zda má lidského ownera. **Neobcházet:**
nepřepiš roli jen kvůli průchodu.

### AI actor nemá platnou qualification evidence

**Znamená:** chybí registry, evaluation, verze, kategorie, evidence nebo je
report prošlý. **Oprava:** doplň konzistentní dodané evidence a interní review.
**Neobcházet:** nepoužij fallback na neznámý model.

### Authority source není frozen

**Znamená:** request cituje README, neaktivní dokument nebo soubor mimo
manifest. **Oprava:** cituj aktivní adopted contract a znovu proveď freeze.
**Neobcházet:** pracovní text není autorita jen proto, že je nejnovější.

### Authorization má jiný intent nebo workspace

**Znamená:** request a authorization patří k různým záměrům nebo projektům.
**Oprava:** vytvoř správný record a ověř scope hash, owner reference a čas.
**Neobcházet:** neměň ID v jednom souboru bez nového rozhodnutí.

## Evidence a čas

### Broken evidence chain

**Znamená:** špatné pořadí, `previous_record_id`, hash, request reference nebo
closure decision. **Oprava:** oprav navazující artefakty a přepočítej hashy.
**Neobcházet:** nevynechávej review record.

### Neplatný nebo prošlý timestamp

**Znamená:** chybí timezone, `expires_at` není později než `issued_at` nebo
platnost skončila. **Oprava:** použij ISO timestamp s `Z` nebo offsetem a nové
lidské rozhodnutí. **Neobcházet:** nikdy nepoužívej lokální nejednoznačný čas.

## Strukturální kontrola není provedení

`STRUCTURALLY_VALID` nebo `EVIDENCE_CHAIN_VALID` znamená, že dodané soubory
odpovídají části public kontraktu. Neznamená to, že byl spuštěn model, změněn
repozitář, proveden deployment nebo správně ověřena lidská identita. Skutečný
diff, testy, secrets a externí účinky musí kontrolovat host-project nebo
interní control plane.

Příkazy pro opakování kontroly:

```text
python -m public_rail status --root docs/ai-rail
python -m public_rail validate-request request.json --root docs/ai-rail
python -m public_rail validate-output request.json output.json --root docs/ai-rail
python -m public_rail validate-evidence evidence.json --root .
```
