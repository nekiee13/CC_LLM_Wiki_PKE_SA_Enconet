# Enconet — feedback, procesi i projekti

Pročitana su sva poglavlja triju uputa: **322 neprazna sadržajna i naslovna
bloka**. Prvi prolaz traži izravne kontrole, drugi kvalitetni cilj i slabije
tragove. Keyword hit nije automatski dokaz. DOCUMENT v3 nije mijenjan.

| Dokument i stvarne mrvice | Run | Mrvice | Točne veze | Izravno / potpora / trag |
| --- | --- | ---: | ---: | --- |
| [DOC-0022 kupci, rev. 3](../sieving/runs/RUN-20261008-07/REVIEW.md) | RUN-20261008-07 | 36 | 66 | 15 / 18 / 3 |
| [DOC-0023 procesi, rev. 3](../sieving/runs/RUN-20261008-08/REVIEW.md) | RUN-20261008-08 | 30 | 67 | 17 / 11 / 2 |
| [DOC-0024 projekti, rev. 3](../sieving/runs/RUN-20261008-09/REVIEW.md) | RUN-20261008-09 | 30 | 65 | 21 / 7 / 2 |
| **Paket** | | **96** | **198** | **53 / 36 / 7** |

Ukupno **2.225 aktivnih dobavljačkih mrvica** i **4.176 točnih citatnih veza**.
Završeno **23 od 26** dobavljačkih dokumenata; **3 ostaju**.
Nove ocjene nisu pisane; ovo nije konačni conformance score.

## Prikupljene kontrole

- Kupci: uloge za prikupljanje i analizu mišljenja, upitnik, reklamacije,
  njihovi uzroci i učestalost te dostava rezultata direktoru.
- Procesi: QA koristi nalaze internih provjera i audita. Voditelj procesa
  ocjenjuje resurse i metode. Rezultati se bilježe i obvezno razmatraju
  kroz upravinu ocjenu; loši rezultati traže poboljšanje ili hitne radnje.
- Projekti: neovisan stručni pregled, QA pregled, vanjski kupac/recenzent,
  završna ocjena prije isporuke, zapisi i direktorova analiza.

Te kontrole povezuju povratne informacije i nalaze s odlukama o kvaliteti.
Enconetove skale od 100 i 50 bodova nisu prenesene u Appendix B scoring.
Poslovni status kupca nije status QA sukladnosti. Forme su predlošci,
ne ispunjeni feedback, auditni ili projektni zapisi.

## Tragovi za kasniju provjeru

Neki predlošci navode drugo ime direktora od odobrenja upute. Treba
provjeriti važeće predloške i ovlasti, bez prepravljanja izvora.
Anketni interval ovisi o poslovnom statusu i suradnji. Treba provjeriti
kako se zasebno prate kvalitetno važne reklamacije.
Zbroj projektnih bodova sam ne pokazuje da je svaki bitan problem riješen:
treba povezati ocjenu s postojećim kontrolama odobrenja i isporuke.
To su tragovi za pregled, ne automatski negativni nalazi.

## Provjera i očuvanje

[Integritet i reproducibilne naredbe](PERFORMANCE_BATCH_INTEGRITY_20261008.json):
ranijih 20 runova ima jednake prije/poslije hash vrijednosti mrvica,
citata, veza i konteksta. Svih 36 incoming datoteka hash-identično je inventaru.
Prije uvoza svih 198 citata potvrđeno je u točnom poglavlju svojeg izvora.
Nakon uvoza svih 4.176 veza je EXACT, literalno i na isti dokument; nula grešaka.

Za runove RUN-20261008-07, -08 i -09 te DOC-0022, -0023 i -0024, izlazni kod **0**:

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

Završiti DOC-0025 (mjerna/testna oprema), DOC-0026 (pogonsko iskustvo)
i DOC-0002 (pravilnik rada, sistematizacija i organizacija), uz veličinu
paketa prema stvarnom opsegu. SQL je potvrdio da su to jedina tri
preostala vendor izvora bez aktivnog runa.
Regulatorna ekstrakcija, primjenjivost i kasnije ocjenjivanje još su otvoreni.
