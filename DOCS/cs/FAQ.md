# FAQ

## Je profil v0.2.2 autonomní agent?

Ne. Je to dokumentační a kontraktová reference s offline validací. Neobsahuje
model call, request gate, tool gate, executor ani provider adapter.

## Potřebuji GitHub oprávnění, sandbox nebo AI agenta?

Ne pro lokální validaci a první pilot. Stačí Python standard library a možnost
číst/zapisovat hostitelský repozitář. GitHub permissions, sandbox, secrets,
síťová politika a skutečný agent jsou odpovědností host projektu, pokud je
vůbec používá.

## Lze Rail používat bez AI nebo sólo?

Ano. Lidský tým nebo solo owner může vést stejné dokumenty, review a evidence
bez modelu. AI je pouze volitelný asistent v omezené roli a nikdy není
decision owner.

## Proč nestačí jeden prompt nebo `AGENTS.md`?

Mohou být užitečným kontextem, ale samy obvykle neoddělí lidskou autoritu,
projektovou pravdu, scope, konflikt a důkaz výsledku. Profil tyto otázky váže
na dokumenty a strukturovaná data host projektu.

## Je Rail náhrada CI?

Ne. CLI je lokální strukturální kontrola dokumentů, requestů, outputů a
evidence. Může být krokem v CI, ale nenahrazuje testy, deploy policy, secret
scanning, sandbox ani provozní monitoring.

## Co když si dokumenty a kód odporují?

Není bezpečné vybrat pohodlnější zdroj. Označ rozpor, zastav delivery, určete
human decision ownera a aktualizujte autoritativní dokument i review. Do té doby
je správný stav `BLOCKED`.

## Co když je během práce lepší řešení mimo původní scope?

Zapiš návrh jako nové rozhodnutí nebo nový intent. Scope expansion nesmí být
potichu připsán k původní autorizaci; vyžaduje nové review a vlastní důkazní
stopu.

## Znamená model-evaluation `PASS`, že je bezpečné spustit model?

Ne. Veřejný profil validuje dodané registry a evaluation reports jako
evidence-only data. Neověřuje jejich vydavatele, metriky, identitu ani runtime
politiku.

## Kdy je Rail zbytečně těžký?

U jednorázové osobní poznámky bez sdíleného scope a bez rizik může být plný kit
overkill. Jakmile se mění kód, hranice, data, přístupy nebo předává výsledek
další osobě, malý adoption profil obvykle sníží nejasnost.

## Musím použít všechny role a moduly?

Ne. Veřejný model má čtyři role a pět modulů jako referenční slovník. Host
projekt vybere jen role a moduly relevantní pro skutečné change surfaces.

## Co znamená `READY` a `BLOCKED`?

`READY` je odvozený bootstrap stav aktivních dokumentů, mapování, frozen
manifestu a platného review. Neznamená oprávnění k provedení. `BLOCKED` znamená
chybějící, konfliktní, prošlou nebo nesouladnou pravdu; nález se opraví nebo
eskaluje, neobchází.

## Co je evidence a je fikční příklad case study?

Evidence spojuje intent, scope, authorization, output, review a closure.
Hash dokládá integritu obsahu, nikoli jeho pravdivost. `examples/fictional-*`
jsou modelované scénáře, ne skutečné case studies ani univerzální schválení.

## Je veřejná sada interním know-how?

Ne. Public profil obsahuje přenositelné kontrakty a omezenou referenční
implementaci. Memory, task-local evidence, secrets, host-project truth,
privátní prompty a komerční provozní know-how jsou mimo něj.
