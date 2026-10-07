# Enconet — ugovaranje, projektiranje i auditi

## Rezultat

Provedeno je cjelovito čitanje triju postupaka. Prvi prolaz traži izravne
kontrole. Drugi traži potporu cilju zahtjeva, međuvezama i mogućim slabostima.
Svih 640 sadržajnih blokova pregledano je; potpuna pokrivenost izvora,
uključujući naslove i prazne retke, ostaje u evidenciji ranijeg keyword sweepa.
Ključna riječ sama nije prihvaćena kao dokaz. Prompt DOCUMENT v3 nije mijenjan.

| Dokument i stvarne mrvice | Run | Mrvice | Točne citatne veze | Izravno / potpora / trag |
| --- | --- | ---: | ---: | --- |
| [DOC-0007: ugovaranje, rev. 5](../sieving/runs/RUN-20261007-06/REVIEW.md) | RUN-20261007-06 | 84 | 131 | 58 / 24 / 2 |
| [DOC-0008: projektiranje, rev. 6](../sieving/runs/RUN-20261007-07/REVIEW.md) | RUN-20261007-07 | 107 | 208 | 81 / 24 / 2 |
| [DOC-0009: auditi, rev. 6](../sieving/runs/RUN-20261007-08/REVIEW.md) | RUN-20261007-08 | 93 | 196 | 58 / 32 / 3 |
| **Ovaj paket** | | **284** | **535** | **197 / 80 / 7** |

Ukupno je sada **1.170 aktivnih dobavljačkih mrvica** i **1.907 točnih
poveznica na izvorna poglavlja**. Broj veza može biti veći od broja mrvica:
jedna tvrdnja može trebati više izvornih odlomaka. Završeno je **8 od 26**
dobavljačkih dokumenata; **18 ostaje**. Ovo nisu bodovi ni konačne ocjene.

## Što je nađeno i zašto je važno

- Ugovaranje: pisana potvrda usmenih zahtjeva, QA pregled ponude i ugovora,
  potvrda sposobnosti izvedbe, kontrola promjena i praćenje reklamacija.
  To pomaže spriječiti pogrešan početni zahtjev i nekontroliranu izmjenu.
- Projektiranje: ulazi i izlazi, neovisna verifikacija, obvezan neovisan pregled
  safety-related dokumentacije, validacija, odobrenje promjena, nadzor
  podprojekata, kalibracija opreme u planu te testiranje i konfiguracija softvera.
  To povezuje zahtjev s provjerom konačnog rezultata.
- Auditi: godišnji plan, trogodišnja pokrivenost, neovisnost i kvalifikacija
  auditora, obvezni vanjski nuklearni auditi, pisani nalazi i praćenje radnji.
  Upitnik je vodič, ne granica provjere.

## Važne granice tumačenja

Prazni obrasci pokazuju propisani način rada, ne obavljen posao. Upisane
kvalifikacije iz 2001.–2016. jesu povijesni podaci, ali nisu potvrda današnjeg
važenja. Postupak traži godišnje održavanje kvalifikacija. Za realni audit treba
tražiti novije zapise, bez automatske presude o nesukladnosti.

Neke provjere vrijede samo kada je svrsishodno ili potrebno. Te ograde su
sačuvane. Safety-related završni neovisni pregled propisan je izričito.
GPD se još spominje u ugovaranju iako postupak upravljanja dokumentima navodi
njegovo ukidanje: usporediti važeću praksu, ne prepraviti izvor. Predložak
godišnjeg plana navodi drugo ime direktora od odobrenja postupka; provjeriti
važeću odgovornost. Same reference na norme nisu potpuna sukladnost.

Tvrdnje o kupčevim ugovornim zahtjevima nisu automatski proglašene kontrolom
nabave. Kontrole kupnje i dobavljača prihvaćene su kada ih sam izvor opisuje.
Veze s kriterijima VIII, XI, XII i XIV služe odgovarajućem cilju zahtjeva;
njihova primjenjivost i potpunost procjenjuju se kasnije.

## Provjera i očuvanje

[Evidencija integriteta](CONTRACT_DESIGN_AUDIT_INTEGRITY_20261007.json) sadrži
točne upite i jednake prije/poslije hash vrijednosti ranijih pet runova.
Njihove mrvice, citati, veze i kontekst nisu promijenjeni.
Svih 36 datoteka u incoming odgovara reset inventaru: bez novih, nestalih ili
promijenjenih datoteka. Registrirani izvori ostaju hash-identični i read-only.

Sve sljedeće naredbe završile su izlaznim kodom **0**:

1. Za svaki novi run, iz korijena workspacea:
   `python Enconet/scripts/validate_app_b_json.py Enconet/sieving/runs/<run>/generated.json --strict`.
   Konkretni runovi: RUN-20261007-06, RUN-20261007-07 i RUN-20261007-08.
2. Iz Enconet, za svaki odgovarajući par run/dokument:
   `python scripts/audit_command.py audit-sieve -- --run-id <run> --doc-id <doc> --prompt-version appb_document_v3_context_anchors --document-side DOCUMENT`.
3. `python scripts/import_crumbs.py sieving/runs/<run>/generated.json --run-id <run> --strict`.
4. `python scripts/link_exact_run.py --run-id <run>`, zatim ista naredba s `--apply`.
5. `python scripts/sieve_metrics.py --run-id <run>`.
6. `python scripts/validate_traceability.py --no-record` nakon svakog uvoza.
7. `python Enconet/scripts/run_all_validations.py --no-record` iz workspacea.
   Četiri provjere prolaze u fazi chunked: izvori, poglavlja, harness i struktura.
   Kasnije provjere su SKIPPED, ne passed. JSON i traceability zato su zasebno provjereni.

Neovisni SQL pregled svih 1.907 veza našao je **0** netočnih citata,
**0** veza na drugi dokument i **0** veza koje nisu EXACT.
Semantička kvaliteta je Codexov pregled; nije predstavljena kao Claudeova potvrda.

Početni continuity check završio je kodom **1**: prethodni handoff je na ranijem
commitu, status je imao neprepoznat format, a faza chunked je u tijeku.
Ownerovo `proceed` znači nastavak, ne rollback. Novi status i handoff bilježe
nastavak. Skripta i dalje upozorava na fazu u tijeku; to nije prolazna provjera.
Prvi pokušaj na workspace putanji session_continuity.py bio je neuspješan
(datoteka ondje ne postoji); ispravna skripta je lokalno u Enconet/scripts.
Početni pomoćni SQL pokušaj imao je grešku navodnika; ispravljeni hash upit prošao je.

## Sljedeća radnja

Nastaviti DOC-0010 (nesukladni proizvod), DOC-0011 (popravne i preventivne
radnje) i DOC-0012 (rizici) istim odobrenim v3 pristupom.
Ne uvoditi novu prompt odluku ni dodatni razvojni paket.
Primjenjivost, regulatorna ekstrakcija i ocjenjivanje još nisu završeni.
Nove ocjene nisu pisane. Raniji arhivirani rezultat nije rezultat ovoga ciklusa.
