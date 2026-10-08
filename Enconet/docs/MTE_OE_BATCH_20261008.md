# Enconet — mjerna oprema i pogonsko iskustvo

Pročitana su sva poglavlja dviju uputa: **283 neprazna sadržajna i naslovna
bloka**. Prvi prolaz traži izravne kontrole, drugi kvalitetni cilj i slabije
tragove. Keyword hit nije automatski dokaz. DOCUMENT v3 nije mijenjan.

| Dokument i stvarne mrvice | Run | Mrvice | Točne veze | Izravno / potpora / trag |
| --- | --- | ---: | ---: | --- |
| [DOC-0025 MTE, rev. 2](../sieving/runs/RUN-20261008-10/REVIEW.md) | RUN-20261008-10 | 65 | 112 | 54 / 8 / 3 |
| [DOC-0026 OE, rev. 0](../sieving/runs/RUN-20261008-11/REVIEW.md) | RUN-20261008-11 | 58 | 107 | 32 / 22 / 4 |
| **Paket** | | **123** | **219** | **86 / 30 / 7** |

Ukupno **2.348 aktivnih dobavljačkih mrvica** i **4.395 točnih citatnih veza**.
Završeno **25 od 26** dobavljačkih dokumenata; **1 ostaje**.
Nove ocjene nisu pisane; ovo nije konačni conformance score.

## Prikupljene kontrole

- MTE: specificirana nabava, auditom provjerena kvalifikacija dobavljača,
  jedinstven ID bez ponovne uporabe, kalibracijski interval, valjanost na
  naljepnici, uvjeti čuvanja, osposobljen korisnik i certifikati as-found/as-left.
- Sumnjivo mjerenje: rad se prekida, problem prijavljuje, pokreće kalibracija
  i ponavljaju posljednja sumnjiva mjerenja. Oštećenje pokreće korektivnu radnju.
- OE: kvalificirana raspodjela posla, pregled postojeće CAP aktivnosti,
  provjera pogođene opreme i skladišta, dokumentirana pretraga i provjera
  sigurnosnih ili projektnih podataka uz razgovor s nadležnim ljudima.
- Zaključak: jasna primjenjivost ili daljnje preporuke kada podaci nisu
  dovoljni. Primjenjivo ili korisno neizravno iskustvo vodi preporučenim
  korektivnim ili preventivnim mjerama. Završni izvještaj ima voditeljev i QA pregled.

To su pisane kontrole, ne današnji kalibracijski certifikati ili izvedene OE
evaluacije. Prazni obrasci nisu ispunjeni zapisi. OE pregled Part 21 izvještaja
drugih institucija nije dokaz Enconetova izvršenja vlastite reporting obveze.
NE Krško je klijent i podatkovni kontekst; nije novi zasebni audit target.

## Tragovi za kasniju provjeru

MTE definicija izuzima trajno ugrađenu opremu, a nabava se veže uz kupčev
zahtjev. Treba provjeriti kontrolu već korištene ili posuđene opreme.
Treba potvrditi definicije instrumentnih klasa i sljedivost referentnih
etalona; iz samih ovih odlomaka ne zaključujemo da je puna sljedivost dokazana.

OE popis i definicija različito pripisuju NSAL izvještaje. Dio dodatne
dokumentacije može se nalaziti izvan DCM-a, pa treba potvrditi njezinu važeću
reviziju. Neizravne preventivne preporuke treba dosljedno razlikovati od
oznake Not applicable. To su tragovi za pregled, ne automatski negativni nalazi.

## Provjera i očuvanje

[Integritet i reproducibilne naredbe](MTE_OE_INTEGRITY_20261008.json): ranijih
23 runova ima jednake prije/poslije hash vrijednosti mrvica, citata, veza i
konteksta. Svih 36 incoming datoteka hash-identično je inventaru.
Prije uvoza svih 219 citata potvrđeno je u točnom poglavlju svojeg izvora.
Nakon uvoza svih 4.395 veza je EXACT, literalno i na isti dokument; nula grešaka.

Za runove RUN-20261008-10 i -11 te DOC-0025 i -0026, izlazni kod **0**:

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

Continuity check ima izlazni kod 1 zbog ranijeg handoff commita i faze u tijeku.
Ownerovo proceed odobrava nastavak, ne rollback. Claudeov pregled je odgođen,
ne pretpostavljen kao odobren. Framework, prompt i scoring nisu mijenjani.

## Sljedeće

Završiti veliki **DOC-0002** (pravilnik rada, sistematizacija i organizacija)
kao zaseban cjeloviti pregled. Izvor ima 151.780 bajtova i 2.081 coverage
blok; nije djelomično obrađen niti proglašen završenim.
SQL je potvrdio da je to jedini preostali vendor izvor bez aktivnog runa.
Regulatorna ekstrakcija, primjenjivost i kasnije ocjenjivanje još su otvoreni.
