# Enconet — tumačenje izričito upućenih Part II odjeljaka

## Rezultat

Vlasnik je odobrio opciju 1. Pod odlukom
`ASME-ENCONET-PARTII-REFS-20261008` obrađeni su samo odjeljci
**2.7** za softver i **2.14** za komercijalne predmete ili usluge.
Vrijede samo za odgovarajuće aktivnosti koje Part I izričito upućuje.
Ostatak Part II te Parts III–IV ostaje podrška, ne automatska obveza.

Cijeli tekst obaju odjeljaka je pročitan. Run `RUN-20261008-15` ima:

- **38** interpretivnih items za softver.
- **33** interpretivnih items za commercial-grade dedication.
- **71** izvorni engleski citat i **71** točnu vezu s pohranjenim poglavljem.

ASME sada ima **239** interpretivnih crumbs: 168 iz Part I i 71 iz upućenih
odjeljaka Part II. Vendor i governing dokazi nisu mijenjani. Ukupno je
**2.957 crumbs**, odnosno 2.700 vendor + 18 governing + 239 ASME, uz
**5.636** točnih poveznica. To nije ocjena sukladnosti dobavljača.

## Važne granice i iznimke

Softver kojem se rezultat neovisno provjerava u svakoj projektnoj primjeni
ima izuzeće od 2.14 dedication puta prema 2.7 §302. Ne smijemo taj dopušteni
put kazniti samo zato što nema opći dedication zapis.

Acceptance test ostaje cjelovit završni test u radnom okolišu prije uporabe.
Dopunski razvojni test nije njegova zamjena. Softverske promjene traže
odgovarajuću provjeru i ponovno ispitivanje, a povučen softver ne ostaje
u rutinskoj uporabi.

Kod commercial-grade dedication bira se jedna ili više dopuštenih metoda.
Ne tražimo sve četiri metode za svaki predmet. Like-for-like ili ekvivalentna
zamjena ima svoje putove, ali dokaz istovjetnosti ili ekvivalentnosti sam
po sebi ne zamjenjuje potrebnu provjeru kritičnih značajki. Sam kataloški
broj također nije dovoljan. Komercijalna usluga može imati dopušten QA put
umjesto dedication, prema uvjetima §700.

CONDITIONAL znači izvorni uvjet aktivnosti ili metode. Ne znači da je G2
primjenjivost kriterija već odobrena. Appendix B ostaje glavni propis;
ASME items tumače zahtjeve, ne dodaju nove kriterije niti bodove.

## Poznato ograničenje izvora

Oba odjeljka nalaze se u velikom pretvorenom poglavlju
`CHUNK-DOC-0031-0041`. Njegov izvedeni naslov je predug. Nismo prepisali
izvor ni postojeće poglavlje. Svaki item ima stvarnu klauzulu, ID poglavlja,
točan citat i početni/završni položaj u cijelom tekstu.

**2.7 §201 počinje fragmentom rečenice.** Ne znamo nedostajuće riječi i
nismo ih izmislili. Fragment je prikazan u REVIEW.md za provjeru izvora.
Obveze QA zapisa iz Part I Requirement 17 ostaju sačuvane. Ova lokalna
praznina nije proglašena potpunim tumačenjem §201.

## Gdje su stvarni items

- [Svi items i citati](../sieving/runs/RUN-20261008-15/REVIEW.md).
- [Klauzule, uvjeti, offsets i governing veze](../sieving/runs/RUN-20261008-15/interpretation-map.json).
- [Odluka vlasnika](ASME_REFERENCED_PARTII_SCOPE_APPROVED_20261008.md).
- [Dokazni JSON s naredbama i hashes](ASME_REFERENCED_PARTII_EVIDENCE_20261008.json).

## Provjere i sljedeći korak

Strict JSON, exact linking, traceability i requirements prolaze s exit 0.
Retry dodaje nula veza. Svi prethodni redci u 15 DB tablica ostaju hash-exact,
uključujući source/chapter podatke, ranije runove, vendor i Part I dokaze,
te 18 governing zahtjeva. Svih 36 incoming datoteka je nepromijenjeno.

Aggregate ima exit 0: četiri provjere primjenjive fazi chunked prolaze.
Kasnije faze su SKIPPED; JSON, traceability i requirements provjereni su
zasebno. Nema novih ocjena, G2 odluka ili promjene aktivnih ranijih generacija.

Sljedeće je zasebna Part 21 obrada DOC-0027, zatim priprema primjenjivosti
za G2. Provjera fragmenta §201 ostaje otvorena. Claude review je odgođen.
