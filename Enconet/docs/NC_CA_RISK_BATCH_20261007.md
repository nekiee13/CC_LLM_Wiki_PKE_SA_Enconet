# Enconet — nesukladnosti, popravne radnje i rizici

## Rezultat

Pročitana su sva poglavlja triju postupaka: 464 sadržajna bloka.
Prvi prolaz tražio je izravne kontrole; drugi je provjerio kvalitetni cilj,
međuvezâ i slabije tragove. Puna evidencija izvora ostaje u keyword sweepu.
Ključne riječi nisu automatski prihvaćene kao dokaz. DOCUMENT v3 nije mijenjan.

| Dokument i stvarne mrvice | Run | Mrvice | Točne citatne veze | Izravno / potpora / trag |
| --- | --- | ---: | ---: | --- |
| [DOC-0010: nesukladni proizvod, rev. 5](../sieving/runs/RUN-20261007-09/REVIEW.md) | RUN-20261007-09 | 87 | 172 | 56 / 27 / 4 |
| [DOC-0011: popravne i preventivne radnje, rev. 4](../sieving/runs/RUN-20261007-10/REVIEW.md) | RUN-20261007-10 | 60 | 103 | 40 / 16 / 4 |
| [DOC-0012: rizici, rev. 2](../sieving/runs/RUN-20261007-11/REVIEW.md) | RUN-20261007-11 | 56 | 131 | 20 / 33 / 3 |
| **Ovaj paket** | | **203** | **406** | **116 / 76 / 11** |

Ukupno je sada **1.373 aktivnih dobavljačkih mrvica** i **2.313 točnih
poveznica na izvorna poglavlja**. Završeno je **11 od 26** dobavljačkih
dokumenata; **15 ostaje**. Ovo nisu bodovi ni konačne ocjene.

## Što je prikupljeno

- Nesukladnosti: prijava svakog djelatnika, hitno označavanje i izolacija,
  pisani NCR, klasifikacija, stručna dispozicija i ponovna provjera dorade.
  Takve kontrole sprečavaju daljnju uporabu neprihvatljivog rada.
- Radnje: uzrok, nositelj, odobrenje, rok, resursi, praćenje i provjera
  učinkovitosti. Ponavljanje problema vodi prema dubljoj analizi.
- Rizici: odgovorne uloge, projektni kontekst, međuvezâ, kvalifikacije ljudi,
  kvaliteta podizvođačkih dijelova, skale vjerojatnosti i posljedica te
  hitno postupanje za visoki rizik. To je potpora kvalitetnom planiranju,
  a ne zamjena za zasebne nuklearne zahtjeve.

## Granice i tragovi za kasniji pregled

Prazni obrasci dokazuju predviđen način rada, ne izvršene aktivnosti.
Izravno, potpora i trag postojeće su v3 oznake, ne nove kategorije ocjene.
Citati ostaju na izvornom jeziku; engleski odlomci označeni su kao engleski.
Kontekst sadrži samo stvarno navedene revizije; projekt i ugovor nisu izmišljeni.

Part 21 koraci i rokovi sačuvani su kao tekst dobavljača za zasebnu provjeru.
Ovaj paket nije pravna potvrda rokova i ne dodaje Part 21 bodove u 18 kriterija.
Tekst PP-83-01 navodi pet dana, a prikaz pet radnih dana; treba usporediti
propis i konkretan put prijavljivanja. Kontakt u NE Krško također treba
provjeriti prije stvarnog izvještavanja.

Postupci citiraju NQA-1:2008 i neobvezni Appendix 16A-1, dok je odobrena
interpretivna baza ovoga ciklusa NQA-1:2015. To nije automatska nesukladnost.
PP-85-01 ima neusklađene brojeve referenci: tijelo navodi Ref.5 i Ref.6 za
postupke koji su u popisu označeni kao 4 i 5.

Risk postupak u području primjene spominje već utvrđeno odstupanje, ali u
tijelu traži analizu svakog projekta. Treba provjeriti preventivni opseg.
Skala posljedica navodi financije, reputaciju i nesukladnosti bez zasebnog
stupca nuklearne sigurnosti. Treba vidjeti kako je sigurnost uključena u
stvarne procjene. To su tragovi za provjeru, ne automatski negativni nalazi.

## Provjera i očuvanje

[Evidencija integriteta](NC_CA_RISK_INTEGRITY_20261007.json) sadrži točne upite,
jednake prije/poslije hash vrijednosti svih ranijih osam runova i nove runove.
Njihove mrvice, citati, veze i kontekst nisu promijenjeni.
Svih 36 incoming datoteka ostaje hash-identično, bez dodanih ili nestalih datoteka.
Registrirani izvori i poglavlja prolaze validaciju.

Za runove RUN-20261007-09, -10 i -11 te odgovarajuće DOC-0010, -0011 i -0012,
sljedeće naredbe završile su izlaznim kodom **0**:

1. Iz workspacea:
   `python Enconet/scripts/validate_app_b_json.py Enconet/sieving/runs/<run>/generated.json --strict`.
2. Iz Enconet:
   `python scripts/audit_command.py audit-sieve -- --run-id <run> --doc-id <doc> --prompt-version appb_document_v3_context_anchors --document-side DOCUMENT`.
3. `python scripts/import_crumbs.py sieving/runs/<run>/generated.json --run-id <run> --strict`.
4. `python scripts/link_exact_run.py --run-id <run>`, zatim s `--apply`.
5. `python scripts/sieve_metrics.py --run-id <run>`.
6. `python scripts/validate_traceability.py --no-record` nakon svakog uvoza.
7. Iz workspacea: `python Enconet/scripts/run_all_validations.py --no-record`.
   Četiri provjere prolaze u fazi chunked: izvori, poglavlja, harness i struktura.
   Kasnije provjere su SKIPPED. JSON i traceability provjereni su zasebno.

Neovisni SQL pregled svih 2.313 veza našao je nula netočnih citata,
nula veza na drugi dokument i nula metoda različitih od EXACT.
Semantički pregled proveo je Codex; Claudeova potvrda nije pretpostavljena.
Početni continuity check završio je kodom 1 zbog ranijeg handoff commita i
faze u tijeku. Ownerovo proceed znači nastavak chunked, ne rollback.
Pokušaj čitanja skills iz workspace .agents nije uspio; pročitane su pune
lokalne Enconet skills prije rada. Taj pokušaj nije označen uspješnim.

## Sljedeća radnja

Nastaviti DOC-0013 (računalna infrastruktura), DOC-0014 (ciljevi kvalitete)
i DOC-0015 (uvođenje pripravnika). Ne mijenjati odobreni prompt ni dodavati
razvojne pakete. Ostaje 15 dokumenata. Regulatorna ekstrakcija, primjenjivost
i kasnije ocjenjivanje još nisu završeni. Novi score nije izračunat.
