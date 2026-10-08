# Enconet — ASME NQA-1:2015 Part 1

## Što je završeno

Pročitan je cijeli odobreni izvor DOC-0030, uključujući uvod, pojmovnik,
uvjete i iznimke. Izvedeno je **168 interpretivnih RULE crumbs** za svih
**18 kriterija Appendix B**, uz **376 točnih citata** povezanih s poglavljima.
Run: `RUN-20261008-14`; prompt: postojeći `appb_rule_v1`.

To nisu dokazi o Enconetu. To su detalji o tome što QA sustav treba raditi.
Dokazi dobavljača ostaju **2.700 crumbs i 5.171 poveznica** iz svih 26 dokumenata.
Appendix B ostaje glavni propis: njegovih 18 zahtjeva i identiteta nije mijenjano.
ASME ostaje tumačenje. Nismo dodali novih 168 kriterija ni napisali ocjene.

## Pregled po kriteriju

| Kriterij | Interpretivni items |
|---|---:|
| I | 5 |
| II | 21 |
| III | 22 |
| IV | 10 |
| V | 1 |
| VI | 4 |
| VII | 15 |
| VIII | 6 |
| IX | 6 |
| X | 12 |
| XI | 8 |
| XII | 9 |
| XIII | 6 |
| XIV | 1 |
| XV | 8 |
| XVI | 2 |
| XVII | 17 |
| XVIII | 15 |
| Ukupno | 168 |

Broj items ovisi o sadržaju klauzule. Nije cilj svakoj klauzuli dati isti broj.
Jedan item može čuvati nekoliko povezanih poduvjeta. Ponovljen citat daje
kontekst ili drugu obvezu; ne znači novi dokaz dobavljača.

## Kako je sačuvano značenje

- `shall` znači obvezu; `should` je smjernica; `may` daje dopuštenu mogućnost.
- Uvjetna aktivnost ne postaje opća obveza. Izvorne iznimke ostaju vidljive.
- Na primjer, dopušten je usmeni ili praktični ispit auditora, ne samo pisani.
- Kalibracijski odnos 4:1 ima put tehničkog opravdanja kad nije izvediv.
- Dvostruka pohrana zapisa ne traži dvosatnu zaštitu jednostruke pohrane,
  ali mora zadovoljiti svoje uvjete udaljenosti i opću zaštitu zapisa.
- Za Enconet kao dobavljača interval internog audita treba razmotriti prema
  Requirement 18 §201.3. Interval operatora postrojenja nije zadana zamjena.
- Graded approach mijenja dubinu kontrole prema važnosti. Ne briše obvezu.
- Sadržaj i pojmovnik služe razumijevanju; nisu drugi skup kontrolnih obveza.

G2 primjenjivost kriterija još nije odlučena. Oznaka CONDITIONAL u novim
referencama bilježi uvjet iz ASME teksta, ne vlasnikovu odluku o kriteriju.

## Jedno pitanje ostaje otvoreno

Part 1 izričito upućuje na **Part II 2.7** za softver i **2.14** za
komercijalne predmete ili usluge. G1 kaže da Part 2 nije automatski obvezan.
Zato upućivanja čuvamo kao činjenice iz izvora, ali ne uvozimo dodatne obveze.
Šest items označeno je kao povezano s otvorenim pitanjem opsega.

Vlasniku je poslano pitanje: procjenjujemo li samo izričito upućene odjeljke
kad se odgovarajuća aktivnost obavlja, ili isključujemo Part 2 i tada?
Nije pretpostavljen odgovor. Parts 3–4 ostaju podrška, ne obvezni zahtjevi.

## Dokazi i provjere

- [Svi prikupljeni items i citati](../sieving/runs/RUN-20261008-14/REVIEW.md).
- [Klauzule, uvjeti i veze na governing zahtjeve](../sieving/runs/RUN-20261008-14/interpretation-map.json).
- [Dispozicija svih 789 ne-praznih blokova izvora](../sieving/runs/RUN-20261008-14/block-disposition.json).
- [Naredbe, rezultati i prije/poslije hashes](NQA1_PART1_INTERPRETATION_EVIDENCE_20261008.json).

Strict JSON, exact linking, traceability i requirements provjere prolaze,
svaka s exit 0. Ponovni preview povezivanja dodaje nula veza i čuva svih 376.
Hashes vendor zapisa i governing baselinea prije i poslije su jednaki.
Svih 36 incoming datoteka ostaje nepromijenjeno; raw i poglavlja su provjereni.

Finalni aggregate ima exit 0: četiri provjere prolaze u fazi `chunked`.
Kasnije faze su SKIPPED, ne passed. JSON, traceability i requirements
provjereni su zasebno. Prvi aggregate nije prošao jer su metrics spremljeni
u poddirektorij, umjesto korijena runa; finalni metrics su na pravom mjestu.
Početne SQL/path/quoting dijagnostičke pogreške opisane su u dokaznom JSON-u.

Aktivno stanje sada ima **2.886 crumbs i 5.565 točnih poveznica**:
2.700 vendor + 18 governing + 168 interpretivnih crumbs.
Ne miješamo te tri skupine pri ocjeni dobavljača.

## Što slijedi

Obraditi Part 21 DOC-0027 zasebno od 18-kriterijskog rezultata. Zatim
pripremiti kriterijske odluke o primjenjivosti za G2, uz ovaj ASME crosswalk
te odgovore vlasnika. Faza ostaje chunked; G2–G7 ostaju pending.
Claude review je odgođen; nema tvrdnje da je interpretacija neovisno odobrena.
