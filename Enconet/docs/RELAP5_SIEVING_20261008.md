# Enconet — RELAP5 cjelovito sieving

DOC-0019, RU-73-04 rev. 2, obrađen je zasebno jer ima 60 označenih stranica.
Pročitana su sva poglavlja i prilozi: **824 neprazna bloka**, uključujući
operativne rečenice oblikovane kao naslove i primjere koda ili input podataka.
Prvi prolaz tražio je izravne kontrole; drugi kvalitetni cilj i slabije tragove.
Keyword hit nije automatski dokaz. Framework i DOCUMENT v3 nisu mijenjani.

RUN-20261008-04 sadrži **227 mrvica**: 165 izravnih kontrola, 58 potpora
i četiri traga. Ima **512 točnih citatnih veza** na poglavlja.

[Sve stvarne mrvice i izvorni citati](../sieving/runs/RUN-20261008-04/REVIEW.md).

Ukupno: **1.895 aktivnih dobavljačkih mrvica** i **3.451 točna citatna veza**.
Završeno **18 od 26** dobavljačkih dokumenata; **8 ostaje**.
Nove ocjene nisu pisane. Ovo nije konačan conformance score.

## Što je važno

- Uloge i kvalifikacije: developer, supervisor, analitičar i softverski inženjer
  imaju određene dužnosti i potrebna znanja. Preporučeno benchmark iskustvo
  nije pretvoreno u bezuvjetnu obvezu.
- Projektni ulazi: početni i rubni uvjeti, setpoints, geometrija, fizički fenomeni
  i poznata ograničenja. Model mora biti odobren kao primjenjiv prije analize.
- Verifikacija: svaki razvojni worksheet neovisno se pregledava. Steady-state
  model uspoređuje se s referentnim stanjem unutar određenih granica.
- Proračun: trips, mass error i fizički rezultati imaju kriterije prihvata,
  put korekcije i deviation report ako rješenje ostane neprihvatljivo.
- Testovi: instalacija, promjene okruženja, distribucijski i LSTF benchmarkovi,
  očekivani parametri, preciznost te zapis i kontrola rezultata.
- Sljedivost: verzije programa, base i run ID, read-only datoteke, notebook,
  workbook, odobrenja, reference, inputi, outputi i grafovi povezuju rezultat
  s podacima i korištenom verzijom.

Te kontrole su konkretne i korisne za pre-flight audit. Primjerne skripte i
input deckovi nisu izvršeni ovim auditom. Ne dokazuju današnje izvršene testove.
Prazni worksheets nisu ispunjeni projektni zapisi.

## Tragovi za provjeru, ne automatski nalazi

Uputa navodi pet osnovnih test deckova, a kasnije sedam zaglavlja.
Prag mass error razlikuje manje od 1% i veće od 1%, bez izričite odluke za
točno 1%. Primjer run kartica izgleda zamjenjuje trips 598 i 599 prema
navedenoj konvenciji. Te detalje treba provjeriti prije stvarne uporabe.
Primjer typpwr sam upozorava da ne slijedi sve preporučene prakse modeliranja.
To upozorenje sačuvano je; primjer nije promoviran u dokaz valjanosti modela.

## Provjera i očuvanje

[Integritet i reproducibilne naredbe](RELAP5_INTEGRITY_20261008.json):
svih ranijih 17 runova ima iste prije/poslije hash vrijednosti mrvica,
citata, veza i konteksta. Svih 36 incoming datoteka hash-identično je inventaru.
Prije uvoza provjereno je svih 512 citata u jedinstvenom poglavlju DOC-0019.
Nakon uvoza SQL provjera svih 3.451 veza našla je nula netočnih citata,
nula veza na drugi dokument i nula metoda različitih od EXACT.

Izlazni kod **0**:

- `python Enconet/scripts/validate_app_b_json.py Enconet/sieving/runs/RUN-20261008-04/generated.json --strict` iz workspacea.
- Iz Enconet: `python scripts/audit_command.py audit-sieve -- --run-id RUN-20261008-04 --doc-id DOC-0019 --prompt-version appb_document_v3_context_anchors --document-side DOCUMENT`.
- `python scripts/import_crumbs.py sieving/runs/RUN-20261008-04/generated.json --run-id RUN-20261008-04 --strict`.
- `python scripts/link_exact_run.py --run-id RUN-20261008-04`, potom s `--apply`.
- `python scripts/sieve_metrics.py --run-id RUN-20261008-04`.
- `python scripts/validate_traceability.py --no-record`.
- Iz workspacea: `python Enconet/scripts/run_all_validations.py --no-record`.
  Četiri provjere prolaze u fazi chunked. Kasnije su SKIPPED; JSON i traceability
  provjereni su zasebno. Claudeova semantička potvrda nije pretpostavljena.

Continuity check završio je kodom 1 zbog ranijeg handoff commita i faze u tijeku.
Ownerovo proceed odobrava nastavak, ne rollback. Prvi dohvat velikog JSON-a
bio je skraćen pa se nije mogao parsirati; zamijenjen je potpunim ograničenim
dohvatima. Draft assembler odbio je nepostojeći B00218; ispravljen je popis
blokova prije stvaranja artefakta i prije uvoza. Nijedan takav pokušaj nije
označen uspješnim niti je mijenjao izvor ili ranije rezultate.

## Sljedeće

Nastaviti DOC-0020 (AOV dijagnostika), zatim DOC-0021 (design basis review),
uz pakete prema stvarnom opsegu. Ostaje osam dobavljačkih dokumenata.
Bez nove prompt odluke ili razvoja frameworka. Regulatorna ekstrakcija,
primjenjivost i kasnije ocjenjivanje još nisu završeni.
