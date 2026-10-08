# Enconet — nacrt nalaza i plan stvarnog audita

## Sažetak za vlasnika

Run: `RUN-20261008-17`. G1, G2 i G3 su odobreni. **G4 nije još odobren.**
Procjena ostaje **80,6 %**, odnosno **1.450 / 1.800 bodova**.
Ocjene nisu ponovno izračunane drugim pravilom niti ručno promijenjene.

Pripremljen je jedan povezani paket:

- **12 nacrta nalaza** za 10 substantially i dva partially kriterija.
- **18 otvorenih auditorskih radnji**, po jedna za svaki kriterij.
- **18 redaka registra pokrivenosti**: šest covered, 10 mostly-covered,
  dva partially-covered. Šest covered redaka nisu nedostaci.
- **7 prioritetnih radnji**: IV, VI, VII, IX, XIV, XVII i XVIII.

Nalazi se odnose na dokumentaciju. Nisu dokaz da je posao na terenu izveden
pogrešno. Confidence medium znači da je zaključak ograničen dostavljenim setom.
Severity medium za IX i XVIII označava veću dokumentarnu slabost za planiranje
audita, ne procjenu posljedica za sigurnost postrojenja. Ostali nalazi su low.
Svih 12 verification statusa ostaje pending.

## Što provjeriti prvo i zašto

1. **IX — VT.** Nuklearni plan opisuje vizualni QC/VT, ali priručnik izuzima
   kriterij IX. Treba uskladiti opseg i pokazati kontroliranu uputu te
   kvalifikaciju postupka i osobe. Ne tražimo dokaz zavarivanja izvan opsega.
2. **XVIII — audit.** PP-82-01 opisuje punu pokrivenost u tri godine.
   Odabrani NQA-1:2015 Req18 §201.3 za dobavljački program traži godišnje
   ili opravdano produženje do dvije godine. Provjeriti matrice i ugovorno
   izdanje prije tvrdnje o prošloj povredi. Lead Auditor zahtjevi postoje.
3. **IV/VII — nabava.** Pribaviti referencirani PP-74-01. Jedan zahtjev za
   dokument služi objema radnjama; ne tražimo dvije kopije. Ostale kontrole
   nabave već su priznate. Nedostaje dokument u setu, ne nužno u tvrtki.
4. **VI/XVII — registri i zapisi.** Razriješiti canceled status GPD-a prema
   postupcima koji ga još traže. Pokazati važeći registar i primjer obnove
   zapisa. Retencijske klase postoje; ne tvrdimo da retencija nedostaje.
5. **XIV — hitna isporuka.** Pokazati da poslovna iznimka ne dopušta preranu
   uporabu nuklearno relevantnog predmeta bez potrebnih provjera.

## Nacrti nalaza

Svaki nalaz sadrži argumente u prilog, ograničenje, zaključak i sve odabrane
crumb IDs iz odobrene procjene. Veza ide nalaz → gap/coverage redak → evaluation
→ aktivan vendor crumb → točan citat → pohranjeno poglavlje → registrirani izvor.
Regulatorni tekst služi usporedbi; nije vendor dokaz.

| Nalaz | Kriterij | Tema | Severity |
|---|---|---|---|
| [FIND-0001](../wiki/findings/FIND-0001.md) | II | Kvalifikacijski detalji i preuzeti programi | low |
| [FIND-0002](../wiki/findings/FIND-0002.md) | III | Sljedivost softverskih zahtjeva zaštite | low |
| [FIND-0003](../wiki/findings/FIND-0003.md) | IV | Detaljan pregled nabavne dokumentacije | low |
| [FIND-0004](../wiki/findings/FIND-0004.md) | VI | Nedosljedan status registra GPD | low |
| [FIND-0005](../wiki/findings/FIND-0005.md) | VII | Detaljan tok prihvata dobavljačkih usluga | low |
| [FIND-0006](../wiki/findings/FIND-0006.md) | IX | VT opseg i kontrola posebnog procesa | medium |
| [FIND-0007](../wiki/findings/FIND-0007.md) | X | Projektna inspekcijska podloga i hold-point ovlasti | low |
| [FIND-0008](../wiki/findings/FIND-0008.md) | XII | Tehnička osnova referentne kalibracije | low |
| [FIND-0009](../wiki/findings/FIND-0009.md) | XIII | Granica zaštite opreme i fizičkih medija | low |
| [FIND-0010](../wiki/findings/FIND-0010.md) | XIV | Nuklearna granica hitne isporuke | low |
| [FIND-0011](../wiki/findings/FIND-0011.md) | XVII | Važeći registar i zaštita/obnova zapisa | low |
| [FIND-0012](../wiki/findings/FIND-0012.md) | XVIII | Pokrivenost i interval audita | medium |

## Plan provjera — svih 18 kriterija

Radnje su prijedlog što zatražiti ili uzorkovati. Nisu potvrda da uzorak
postoji, da je odabran ili da je prošao provjeru. Radnja sample_test ovdje
znači pregled objektivnog uzorka; nije izvođenje testa na postrojenju.

| Radnja | Kriterij | Što učiniti | Prioritet |
|---|---|---|---|
| [ACT-0001](../wiki/actions/ACT-0001.md) | I | QA imenovanje i primjer eskalacije/obustave; rutinska provjera | ne |
| [ACT-0002](../wiki/actions/ACT-0002.md) | II | QC/test kvalifikacijski dosje i godišnja upravina ocjena | ne |
| [ACT-0003](../wiki/actions/ACT-0003.md) | III | Projektni/softverski baseline, neovisni pregled, V&V i zaštita | ne |
| [ACT-0004](../wiki/actions/ACT-0004.md) | IV | PP-74-01 i nuklearna narudžba s QA pregledom i flow-downom | da |
| [ACT-0005](../wiki/actions/ACT-0005.md) | V | Uputa, radni nalog i kriteriji prihvata; rutinska provjera | ne |
| [ACT-0006](../wiki/actions/ACT-0006.md) | VI | Važeći registar, distribucija i povučena revizija | da |
| [ACT-0007](../wiki/actions/ACT-0007.md) | VII | Isti PP-74-01, odobrenje dobavljača i prihvat prije uporabe | da |
| [ACT-0008](../wiki/actions/ACT-0008.md) | VIII | Veza instrumenta/AOV/softvera i rezultata; rutinska provjera | ne |
| [ACT-0009](../wiki/actions/ACT-0009.md) | IX | VT uputa, opseg, procesna i osobna kvalifikacija | da |
| [ACT-0010](../wiki/actions/ACT-0010.md) | X | Inspection plan, hold-point izuzeće ako postoji i neovisnost | ne |
| [ACT-0011](../wiki/actions/ACT-0011.md) | XI | RELAP5/AOV testni paket i odobrenje; rutinska provjera | ne |
| [ACT-0012](../wiki/actions/ACT-0012.md) | XII | Etalon/točnost, as-found/as-left i prethodna mjerenja | ne |
| [ACT-0013](../wiki/actions/ACT-0013.md) | XIII | Čuvanje MTE/medija i preuzeta odgovornost pri prijenosu | ne |
| [ACT-0014](../wiki/actions/ACT-0014.md) | XIV | Release/test-tag i granica hitne isporuke | da |
| [ACT-0015](../wiki/actions/ACT-0015.md) | XV | NCR, tehnički razlog, odobrenja i dorada; rutinska provjera | ne |
| [ACT-0016](../wiki/actions/ACT-0016.md) | XVI | Uzrok, verifikacija i sprječavanje ponavljanja; rutinska provjera | ne |
| [ACT-0017](../wiki/actions/ACT-0017.md) | XVII | Trajni zapis, rok, registar i restore primjer | da |
| [ACT-0018](../wiki/actions/ACT-0018.md) | XVIII | Coverage matrice, produženje i Lead Auditor requalifikacija | da |

## Granice koje ostaju na snazi

- Enconet je jedini dobavljač u opsegu. NEK nije zaseban audit target.
- XIII se odnosi na odobreni MTE i relevantne fizičke medije; ne opću logistiku.
- Part 21 ostaje zaseban skup. Ne utječe na ovih 18 ocjena. Jurisdikcija,
  ugovorna uloga i događaj ne pretpostavljaju se iz naziva nuklearnog projekta.
- Fragment ASME Part II 2.7 §201 ostaje ograničenje izvora, ne vendor nalaz.
- Nema novih kategorija ocjena, FAHP-a ni zahtjeva da vlasnik unese 18 ocjena.
- Incoming, raw, poglavlja, crumbs, aktivni runovi, ocjene i izvorna provenance
  ostaju isti. Nisu mijenjani kontrolirani citati niti promptovi.

## Dokazi i provjere

[Kanonski draft paket](../out/2026-10-08/findings-run17/enconet_appendix_b_evaluation_package.json),
[matrica iz DB-a](../wiki/evidence/matrix.md),
[pripremljeni zapisi](../out/2026-10-08/findings-run17/prepared-records.json),
[izvorni trag citata i poglavlja](../out/2026-10-08/conformance-run17/evidence-trace.json).

Komande i stvarni rezultati:

- `python Enconet/out/2026-10-08/findings-run17/execute_draft.py`: exit 0,
  read-only preview. Prvi pokušaj exit 1 zbog cp1252 ispisa; ispis popravljen.
- Ista komanda s `--apply`: exit 0. Normalni gap/finding/action writers.
  Apply ne smije se ponoviti; odbija postojeće retke.
- Ista komanda s `--verify`: exit 0. Svi izvorni DB tablični hashes isti,
  osim tri namjerno dopunjene tablice. Provjereno 18/12/18 zapisa i wiki projekcije.
- `python -m pytest Enconet/tests/test_epic9_matrix_gaps.py
  Enconet/tests/test_epic10_findings.py -q -p no:cacheprovider
  --basetemp Enconet/.test-tmp/g4-draft-20261008-approved`: exit 0, **10 passed**.
  Prvi sandbox pokušaj exit 1 zbog WinError 5; rerun s odobrenim pristupom
  u novoj izoliranoj mapi prolazi. Nije pokrenut puni test suite.
- `python Enconet/scripts/validate_findings.py --no-record`: exit 0.
- `python Enconet/scripts/run_all_validations.py --no-record`: exit 0,
  **11 phase checks pass**. Report/dashboard i benchmarki su phase-skipped.
- `python Enconet/scripts/validate_evidence_bundle.py
  Enconet/outputs/candidates/evidence_access/RUN-20261008-17/evidence_bundle_g4_draft.json`:
  exit 0, 134 jedinstvena crumbs, 164 citata, 169 poglavlja, 17 dokumenata,
  18 coverage redaka, 12 nalaza i 18 radnji.

Novi bundle je odvojen od povijesnog G3 `evidence_bundle.json`; nije prepisan.
Aggregate još provjerava taj G3 bundle, a G4 bundle provjeren je zasebno gore.
Prvi pokušaj G4 bundle u podmapi odbijen je pravilom output lokacije (exit 1),
bez pisanja; ispravan novi naziv izravno u run mapi prošao je.

Scoring fixture nije promijenjen. Poznati version/hash mismatch ostaje otvoren
do zasebne dozvole za metadata-only update; matematika i očekivane vrijednosti
ostaju iste. Benchmark provjere obvezne su prije iduće faze findings_approved.
Claude review je odgođen, ne proglašen dovršenim.

## Jedna odluka G4

Pregledati [G4 paket](../wiki/gates/G4-RUN-20261008-17-enconet.md).
Odobrenje prihvaća **FIND-0001–0012 i ACT-0001–0018** kao dokumentacijske nalaze
i plan provjera. Ne zatvara radnje, ne pretvara pending u verified i ne tvrdi
da je terenski audit završen. Izvještaj/dashboard bit će sljedeći korak.
Za scoring fixture i dalje je potrebna zasebna jasna dozvola.
