# Enconet — softverske kontrole

Pročitana su sva poglavlja triju uputa: 387 sadržajnih i 138 naslovnih blokova.
Naslovi uključuju pune obvezne rečenice o izdavanju, kopijama i testovima;
one nisu odbačene kao izgled stranice. Sve mrvice imaju točne izvorne citate.
DOCUMENT v3, framework i pravila ocjenjivanja nisu mijenjani.

| Dokument i stvarne mrvice | Run | Mrvice | Točne veze | Izravno / potpora / trag |
| --- | --- | ---: | ---: | --- |
| [DOC-0016 konfiguracija, rev. 2](../sieving/runs/RUN-20261008-01/REVIEW.md) | RUN-20261008-01 | 62 | 126 | 41 / 18 / 3 |
| [DOC-0017 V&V, rev. 2](../sieving/runs/RUN-20261008-02/REVIEW.md) | RUN-20261008-02 | 41 | 91 | 29 / 9 / 3 |
| [DOC-0018 instalacija i pohrana, rev. 3](../sieving/runs/RUN-20261008-03/REVIEW.md) | RUN-20261008-03 | 42 | 76 | 29 / 9 / 4 |
| **Paket** | | **145** | **293** | **99 / 36 / 10** |

Ukupno: **1.668 aktivnih dobavljačkih mrvica**, **2.939 točnih poglavljenih
citatnih veza**. Završeno **17 od 26** dobavljačkih dokumenata; **9 ostaje**.
Nove ocjene nisu pisane; ovo je prikupljanje dokaza, ne konačna sukladnost.

## Što je nađeno

- Konfiguracija: pregledan i testiran baseline, identifikacija verzije,
  odobrenje promjene, kontrola međuvezâ, registar promjena i provjera izdanja.
- V&V: plan za svaki softver, fazni kriteriji, test planovi, konfiguracija
  testa, rezultati i NCR. Ugovorni razvijatelji moraju zadovoljiti projektne
  postupke; kupljeni inženjerski softver treba imati V&V dokumentaciju.
- Pohrana: provjera instalacijskog paketa i testova, original u arhivi,
  kopije na više medija, trajno čuvanje originala i dvogodišnja provjera medija.
  Privremeni backup i završni zapisi izričito su različite kategorije.

To omogućuje povezati isporučenu verziju s pregledanim kodom i testovima,
spriječiti neodobrene promjene i kasnije dohvatiti izvorne podatke.
Prazni obrasci nisu izvršeni testovi ni provedene radnje.

## Tragovi za kasniju provjeru

Reference citiraju NQA-1:1994, dok audit koristi odobreni NQA-1:2015.
To nije automatska nesukladnost. Pokvarene reference na priloge sačuvane su.
RU-73-03 navodi datum odobrenja **17.15.2017.**: citat nije ispravljen.
Treba provjeriti odobreni primjerak. RU-73-02 imenuje organizatora pregleda;
neovisnost pregledavatelja treba provjeriti u cijelom QA sustavu.
Konfiguracijski audit nije automatski zamjena za audit QA programa.

## Provjera i očuvanje

[Integritet i reproducibilne naredbe](SOFTWARE_BATCH_INTEGRITY_20261008.json):
ranijih 14 runova ima iste prije/poslije hash vrijednosti mrvica, citata,
veza i konteksta. Svih 36 incoming datoteka hash-identično je inventaru.
SQL provjera svih 2.939 veza: nula netočnih citata, veza na drugi dokument
ili metoda različitih od EXACT.

Za svaki novi run i odgovarajući dokument, izlazni kod **0**:

- Iz workspacea:
  `python Enconet/scripts/validate_app_b_json.py Enconet/sieving/runs/<run>/generated.json --strict`.
- Iz Enconet:
  `python scripts/audit_command.py audit-sieve -- --run-id <run> --doc-id <doc> --prompt-version appb_document_v3_context_anchors --document-side DOCUMENT`.
- `python scripts/import_crumbs.py sieving/runs/<run>/generated.json --run-id <run> --strict`.
- `python scripts/link_exact_run.py --run-id <run>`, potom s `--apply`.
- `python scripts/sieve_metrics.py --run-id <run>`.
- `python scripts/validate_traceability.py --no-record` nakon svakog uvoza.
- Iz workspacea: `python Enconet/scripts/run_all_validations.py --no-record`.
  Četiri provjere prolaze u fazi chunked; kasnije su SKIPPED.
  JSON i traceability zato su provjereni zasebno.

Continuity check završio je kodom 1 zbog ranijeg handoff commita i faze
u tijeku. Ownerovo proceed odobrava nastavak, ne rollback. Claudeov pregled
ostaje odgođen; semantičku potvrdu drugog agenta ne pretpostavljamo.

## Sljedeće

Nastaviti DOC-0019 (RELAP5), zatim DOC-0020 (AOV dijagnostika) i
DOC-0021 (design basis review), u paketima prema stvarnoj veličini izvora.
Bez nove prompt odluke ili dodatnog razvoja frameworka.
Regulatorna ekstrakcija, primjenjivost i kasnije ocjenjivanje još su otvoreni.
