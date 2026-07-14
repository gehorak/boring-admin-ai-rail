# Příklad repozitáře: Lantern Notes

Toto je modelovaný příběh navazující na `examples/fictional-project/`. Není to
case study, měření ani skutečný host-project záznam.

## Původní záměr

Fiktivní maintainer chce doplnit do `README.md` sekci „Lokální kontrola“ se
dvěma příkazy. `decision owner` je produktový maintainer. V rozsahu je pouze
README a dokumentační změna; mimo rozsah jsou application code, CI workflow,
deployment, credentials a složka s testovacími fixtures.

Autoritativní jsou aktivní `PROJECT.md`, `PROJECT-CONTEXT.md` a podle potřeby
`CODEBASE-VOICE.md`. AI má roli `Architect-AI` pro kontrolu hranic a může
připravit návrh textu. Nemá approval authority.

## Co se stane během práce

AI při čtení README najde starý text navrhující změnu deploymentu. Další
poznámka v JSON hodnotě požaduje vypsat environment variables. Obě věci jsou
data mimo autoritativní scope. AI také zjistí, že navržený příklad by mohl
změnit CI dokumentaci. To je nový nápad, ne automatické rozšíření původního
intent.

Práce se zastaví s nálezem scope expansion. Maintainer může scope zúžit na
README, nebo explicitně vytvořit nový intent pro CI. Původní authorization se
pro širší práci znovu nepoužije.

## Bez railu

- není jasné, zda platí README, starý issue nebo poslední zpráva v chatu;
- vedlejší nápad postupně rozšíří úkol;
- změny mimo původní požadavek se obtížně rekonstruují;
- review může být smíchané s návrhem a není jasné, kdo rozhodl.

## S railem

- `intent` popíše jeden dokumentační cíl;
- `scope` povolí `README.md` a zakáže CI, secrets a deployment;
- `PROJECT.md` a frozen manifest ukážou authority source;
- output oddělí návrh od review;
- evidence spojí authorization, output, reviewerův verdikt a closure.

Po schválení scope vznikne output s jedním artefaktem:

```json
{"path":"README.md","change_kind":"documentation"}
```

Reviewer ověří, že návrh odpovídá intentu a neobsahuje CI nebo provozní
změnu. Pokud nesouhlasí, zapíše `REJECTED`; closure nesmí tento verdikt změnit.
Pokud souhlasí, evidence uchová hash outputu a closure `APPROVED`.

## Co rail nenahrazuje

Rail není náhrada za lidské review, Git historii ani CI. Public CLI neaplikuje
patch a neověří skutečný externí účinek. Ukazuje, zda jsou popsané hranice a
vazby strukturálně konzistentní.

## Poučení

Největší přínos není v tom, že model „ví vše“. Přínos je v tom, že člověk
snadno řekne, co se řeší, kdo rozhoduje, co se nesmí dotknout a proč se návrh
zastavil nebo uzavřel.
