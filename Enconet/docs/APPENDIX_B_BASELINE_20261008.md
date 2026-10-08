# Enconet — governing Appendix B baseline

DOC-0028 obrađen je pod postojećim RULE v1 i odobrenom G1 osnovom.
RUN-20261008-13 ima **18 governing RULE mrvica**, po jednu za puni tekst
svakog kriterija, i **18 requirement redaka**. To čuva postojeći Enconetov
model od 18 roditeljskih kriterija; broj potkriterija nije pretvoren u nove
bodovne kategorije. Uvod i opseg pročitani su kao normativni kontekst.

[Stvarni zahtjevi i puni citati](../sieving/runs/RUN-20261008-13/REVIEW.md).
[Integritet i provjere](APPENDIX_B_BASELINE_EVIDENCE_20261008.json).

Svih 18 zahtjeva vodi na RULE mrvicu, izvor DOC-0028, točan citat i
GOVERNING / 10CFR50_APPB autoritet. Vendorovih **2.700 mrvica** i **5.171
citatna veza** nisu promijenjeni. Novi RULE dodaje 18 zasebnih veza.
Svih 36 incoming datoteka hash-identično je ranijem inventaru.
Nema novih ocjena ni zaključka sukladnosti. G2–G7 ostaju pending.

## Minimalni prijenos postojećeg alata

Legacy ingest_appendix_b.py ima brisanje chunkova i runova te zastarjeli
intake datum. Njegova mutirajuća funkcija nije pozvana. Korišten je samo
njegov postojeći čisti parser, zatim guarded run/import i exact-link alati.
Izvorni chunkovi, registry i starije generacije nisu mijenjani.

Enconetu je nedostajao sigurni additive seeder koji Ekonerg već koristi.
Prenesen je kao versioned company-neutral add-on u
audit_template/requirement_seed/v1, s hash manifestom i izvornim Git SHA.
Projekt dobiva svoju kopiju; runtime ne uvozi sibling kod ili podatke.

U prvom koraku kopiran je postojeći algoritam. Prije prve objave dodan je
obvezni **--run-id**, da drugi aktivni RULE izvori ne uđu tiho u governing
baseline. Algoritam ostaje read-only u previewu, dodaje samo nedostajuće
retke, odbija konflikt i u ponovljenom applyu dodaje nula redaka.
Testni mock prilagođen je opcionalnom db_util.local_path atributu.
Pre-release kopirni journali zadržavaju ranije hash vrijednosti; završni
REQ-SEED-20261008-03 potvrđuje točno podudaranje finalnog paketa i lokalne kopije.
Add-on je **candidate pending Claude review**, ne lažno odobren release.

## TDD i provjera

Prvi RED: test nije mogao uvesti nedostajući seeder. Nakon kopiranja,
testovi su otkrili razliku u testnom mocku; popravljena je u reusable payloadu,
ne samo za Enconet. Novi RED testovi tražili su eksplicitni run i isključenje
drugih aktivnih pravila. Nakon promjene, završni rezultat je **10 passed**.

Točna završna naredba, exit **0**:

`python -m pytest -q -p no:cacheprovider Enconet/scripts/tests/test_seed_requirements.py audit_template/tests/test_requirement_seed_bundle.py --basetemp Enconet/.test-tmp/req-seed-20261008-h`

Matrix pokriva Company With Spaces i Županija audit, sa siblingom i bez njega.
Provjerava bootstrap preview/apply/retry i normalni seed preview/apply/retry,
uz nepromijenjene hash vrijednosti owner/sibling sentinel datoteka.
Ostali testovi pokrivaju deduplikaciju, nedostatnu pokrivenost, odabrani run,
obvezan odabir i odbijanje foreign database prije otvaranja.

Live naredbe iz Enconet, exit **0**:

- `python scripts/import_crumbs.py sieving/runs/RUN-20261008-13/generated.json --run-id RUN-20261008-13 --strict`
- `python scripts/link_exact_run.py --run-id RUN-20261008-13`, potom s `--apply`
- `python scripts/sieve_metrics.py --run-id RUN-20261008-13`
- `python scripts/seed_requirements.py --run-id RUN-20261008-13`
- `python scripts/seed_requirements.py --run-id RUN-20261008-13 --apply` — finalni retry dodaje **0**
- `python scripts/validate_requirements.py --no-record`
- `python scripts/validate_traceability.py --no-record`

Iz workspacea, exit **0**:

- `python Enconet/scripts/validate_app_b_json.py Enconet/sieving/runs/RUN-20261008-13/generated.json --strict`
- `python audit_template/bootstrap_requirement_seed.py --target Enconet --apply --run-id REQ-SEED-20261008-03`
- `python Enconet/scripts/run_all_validations.py --no-record` — četiri phase-appropriate provjere prolaze; kasnije su SKIPPED. Requirements, JSON i traceability provjereni su zasebno.

Početni live preview prije run-filter promjene planirao je 18 redaka; prvi
apply dodao je 18, drugi nula. Tada je samo DOC-0028 imao aktivni RULE run.
Finalni eksplicitni run preview/apply također dodaje nula. Dokazni JSON čuva
stvarne source_item_id i requirement_id veze i prije/poslije vendor hash vrijednosti.

## Neuspješni pokušaji — nisu passed

Zapisani su: očekivani RED import failure; Windows pytest-temp permission
greške; nedostajući parent temp direktorij; testni optional-attribute i
foreign-temp-location bugovi; pogrešan broj SQL fixture vrijednosti;
run-selection RED; quoting SyntaxError i odbijeni authority placeholder prije
stvaranja runa; jedan neuspjeli patch hunk. Svi su riješeni prije finalnih
testova i regulativnog uvoza. Missing-path dijagnostika i broad template
search također su prijavili nedostajuće/zaštićene putanje.

NRC web retrieval dobio je HTTP 403. Nismo tvrdili da je live web provjeren;
korišten je postojeći, G1 odobreni kontrolirani izvor bez zamjene teksta.
Continuity check i dalje daje exit 1 za prethodni handoff SHA i fazu u tijeku;
ownerovo proceed odobrava nastavak, ne rollback.

## Sljedeći korak

Obraditi DOC-0030, **ASME NQA-1:2015 Part 1**, kao INTERPRETIVE izvor pod
postojećim RULE v1 i G1 osnovom. Governing baseline identiteti ostaju stabilni.
Part 21 DOC-0027 ostaje zaseban od 18-criterion scorea; Parts 2–4 ne postaju
automatski obvezni. Primjenjivost i kasniji gateovi još nisu odobreni.
