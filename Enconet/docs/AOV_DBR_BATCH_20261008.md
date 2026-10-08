# Enconet — AOV dijagnostika i projektna baza

Pročitana su sva poglavlja dviju uputa: **526 nepraznih sadržajnih i naslovnih
blokova**. Prvi prolaz traži izravne kontrole, drugi kvalitetni cilj i slabije
tragove. Keyword hit nije automatski dokaz. DOCUMENT v3 nije mijenjan.

| Dokument i stvarne mrvice | Run | Mrvice | Točne veze | Izravno / potpora / trag |
| --- | --- | ---: | ---: | --- |
| [DOC-0020 AOV test, rev. 2](../sieving/runs/RUN-20261008-05/REVIEW.md) | RUN-20261008-05 | 162 | 340 | 148 / 10 / 4 |
| [DOC-0021 DBR, rev. 2](../sieving/runs/RUN-20261008-06/REVIEW.md) | RUN-20261008-06 | 72 | 187 | 65 / 3 / 4 |
| **Paket** | | **234** | **527** | **213 / 13 / 8** |

Ukupno **2.129 aktivnih dobavljačkih mrvica** i **3.978 točnih citatnih veza**.
Završeno **20 od 26** dobavljačkih dokumenata; **6 ostaje**.
Nove ocjene nisu pisane; ovo nije konačni conformance score.

## Prikupljene kontrole

- AOV: osposobljene uloge, odobren Work Order, briefing, potrebni crteži,
  kalibrirana oprema i njezina evidencija, pravilni senzori, warm-up,
  provjera curenja, valve tag i test setup prema projektnim podacima.
- As-Found i As-Left: konfiguracija, potpisi, prihvat ili ponavljanje,
  završeno održavanje, obnova normalnog stanja, release test tags i zapisi.
- Test kriteriji: travel, tlakovi, signali, trenje, bench set, spring rate,
  hysteresis, linearity, repeatability i response. Vrijednosti su sačuvane
  u izvornim citatima, bez našeg mijenjanja projektnih granica.
- Stop work: otkriveni problem zaustavlja posao, traži prijavu i evidenciju.
- DBR: normalni i worst-case uvjeti, safety funkcija, valve i actuator
  kompatibilnost, ulazni parametri, thrust/torque, margine i izvještaj.
  Nemogućnost funkcije vodi preporuci održavanja.

To su konkretne pisane kontrole. Generički postupak nije dokaz današnjeg
izvršenog terenskog testa. Prikazane formule nisu neovisno validirani
projektni računi. Nismo provodili rad na ventilu niti tehnički potvrdili
ispravnost svake formule. Točne formule ostaju dostupne za engineering pregled.

## Tragovi za kasniju provjeru

Treba potvrditi tko stvarno izvršava opisane station i maintenance uloge
u odnosu na Enconetovu uslugu. Field Data Sheets traženi su u tijelu,
a Appendix je N/A: tražiti stvarni kontrolirani obrazac i ispunjene zapise.
Neke reference preskaču privremenu I/P postavu ili upućuju na nepostojeće
8.4 i 7.3.4 korake. Provjeriti ih prije terenske uporabe, ne prepraviti izvor.

DBR navodi MECL bazu i ING.MOD dokumentaciju kao podatkovne izvore.
Ta izjava nije dostavljeni projektni zapis. Za realni audit tražiti konkretne
ulaze i Work Report s odgovarajućim odobrenjima. Tvrdnja o EPRI usklađenosti
sama ne zamjenjuje objektivni račun ili verifikaciju.

## Provjera i očuvanje

[Integritet i reproducibilne naredbe](AOV_DBR_INTEGRITY_20261008.json): ranijih
18 runova ima jednake prije/poslije hash vrijednosti mrvica, citata, veza i
konteksta. Svih 36 incoming datoteka hash-identično je inventaru.
Prije uvoza svih 527 citata potvrđeno je u točnom jedinstvenom poglavlju
odgovarajućeg izvora. Nakon uvoza svih 3.978 veza je EXACT, literalno i
na isti dokument; nula grešaka.

Za runove RUN-20261008-05 i -06 te DOC-0020 i -0021, izlazni kod **0**:

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

Nastaviti DOC-0022 (zadovoljstvo kupca), DOC-0023 (osposobljenost procesa)
i DOC-0024 (uspješnost projekata). Preostali vendor dokumenti su još
DOC-0002, DOC-0025 i DOC-0026. Bez nove prompt odluke ili razvoja frameworka.
Regulatorna ekstrakcija, primjenjivost i kasnije ocjenjivanje još su otvoreni.
