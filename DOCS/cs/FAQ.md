# FAQ

## Je profil v0.2.2 autonomní agent?

Ne. Je to dokumentační a kontraktová reference s offline validací. Neobsahuje
model call, request gate, tool gate, executor ani provider adapter.

## Proč nestačí jeden prompt nebo `AGENTS.md`?

Mohou být užitečným kontextem, ale samy obvykle neoddělí lidskou autoritu,
projektovou pravdu, scope, konflikt a důkaz výsledku. Profil tyto otázky váže
na dokumenty a strukturovaná data host projektu.

## Musím použít všechny role a moduly?

Ne. Veřejný model má čtyři role a pět modulů jako referenční slovník. Host
projekt vybere jen role a moduly relevantní pro skutečné change surfaces.

## Co znamená `READY`?

`READY` je odvozený bootstrap stav: aktivní dokumenty, mapování, zmrazený
manifest a platný bootstrap review jsou konzistentní. Neznamená povolení
libovolné práce ani potvrzení lidské identity.

## Co znamená `BLOCKED`?

Kontrola nalezla chybějící, konfliktní, prošlou nebo nesouladnou pravdu.
Správná reakce je nález opravit nebo eskalovat k lidskému ownerovi, ne obejít
validaci.

## Co je evidence?

Evidence je řetězec artefaktů a vazeb, podle kterého lze zpětně ověřit intent,
scope, authorization, navržený output, review a closure. Hash dokládá integritu
konkrétního obsahu, nikoli jeho pravdivost.

## Je fikční příklad skutečná case study?

Ne. `examples/fictional-*` jsou modelované scénáře. Skutečná adopce musí mít
samostatný host-project záznam s vlastními daty a review.

## Je veřejná sada interním know-how?

Ne. Public profil obsahuje přenositelné kontrakty a omezenou referenční
implementaci. Memory, task-local evidence, secrets, host-project truth,
privátní prompty a komerční provozní know-how jsou mimo něj.

## Validuje CLI host projekt?

Validuje dodané dokumenty a data podle veřejných kontraktů: stav bootstrapu,
hashy, scope, role, moduly, autoritu, output a evidence chain. Neprovádí změny,
nevolá nástroje a neuděluje oprávnění.
