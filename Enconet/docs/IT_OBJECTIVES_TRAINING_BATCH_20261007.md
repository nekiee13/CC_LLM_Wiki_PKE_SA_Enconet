# Enconet — infrastruktura, ciljevi i pripravnici

## Rezultat

Pročitana su sva poglavlja triju uputa: 449 sadržajnih blokova.
Prvi prolaz tražio je izravne kontrole, drugi potporu kvalitetnom cilju
i slabije tragove. Puna evidencija izvora ostaje u keyword sweepu.
Ključna riječ nije automatski dokaz. DOCUMENT v3 nije mijenjan.

| Dokument i stvarne mrvice | Run | Mrvice | Točne citatne veze | Izravno / potpora / trag |
| --- | --- | ---: | ---: | --- |
| [DOC-0013: infrastruktura, rev. 2](../sieving/runs/RUN-20261007-12/REVIEW.md) | RUN-20261007-12 | 61 | 142 | 35 / 21 / 5 |
| [DOC-0014: ciljevi kvalitete, rev. 3](../sieving/runs/RUN-20261007-13/REVIEW.md) | RUN-20261007-13 | 40 | 91 | 23 / 14 / 3 |
| [DOC-0015: pripravnici, rev. 3](../sieving/runs/RUN-20261007-14/REVIEW.md) | RUN-20261007-14 | 49 | 100 | 37 / 10 / 2 |
| **Ovaj paket** | | **150** | **333** | **95 / 45 / 10** |

Ukupno je sada **1.523 aktivnih dobavljačkih mrvica** i **2.646 točnih
poveznica na izvorna poglavlja**. Završeno je **14 od 26** dobavljačkih
dokumenata; **12 ostaje**. Ovo nisu bodovi ni konačne ocjene.

## Što je prikupljeno i zašto je važno

- Infrastruktura: korisnička i administratorska odgovornost, privatne mape,
  ograničena prava, kontrolirani SUK dokumenti, svakodnevne kopije i provjera
  kopiranih datoteka. Te kontrole štite dokumentaciju i zapise od gubitka
  ili neovlaštene promjene.
- Ciljevi: mjerljiv cilj, razdoblje, odgovorna osoba, prethodni podatak,
  planirani rezultat, potpisano izvršenje i direktorova analiza. Za
  neostvareni cilj prema potrebi slijedi radnja s nositeljem i rokom.
- Pripravnici: imenovani mentor, njegova stručnost, program i dnevnik,
  mjesečno izvješće, praktično praćenje i pisana završna ocjena.
  To podupire osposobljenost za posao, ne dokazuje posebnu nuklearnu kvalifikaciju.

## Granice i tragovi za kasniju provjeru

Prazni obrasci nisu izvršeni zapisi. Popunjeni inventari stare opreme
pokazuju dokumentirani pregled konfiguracije, ali ne današnje stanje.
Prava pristupa nisu sama dokaz uspješnog vraćanja sigurnosne kopije.
Pričuvna kopija nije automatski kontrolirani dugoročni arhiv.

IT uputa još navodi GPD, dok postupak upravljanja dokumentima navodi njegovo
ukidanje. Zapis postavki backup profila ima pokvarenu poveznicu
Error! Reference source not found. Dnevno kopiranje veže se uz Logoff ili
gašenje računala. Treba provjeriti kako kopiranje radi kada se računalo ne
odjavljuje ili ne gasi. Izvorni tekst nije popravljen niti nadopunjen.

Privatni backup sadržaj može se brisati; javne mape imaju različita prava,
od kojih jedna dopušta svima brisanje. To treba razlikovati od ograničenih
prava SUK i Arhiva grupa. Stari operativni sustavi u inventaru razlog su
za provjeru aktualne konfiguracije, ne zaključak o današnjoj nesukladnosti.

Cilj smanjenja broja popravnih radnji nije dozvola za neprijavljivanje
problema. Uvođenje pripravnika i pozitivna mentorska ocjena ne zamjenjuju
potrebnu provjeru kvalifikacije za konkretan kvalitetno važan posao.

## Provjera i očuvanje

[Evidencija integriteta](IT_OBJECTIVES_TRAINING_INTEGRITY_20261007.json)
sadrži reproducibilne naredbe, jednake prije/poslije hash vrijednosti
ranijih 11 runova i nove runove. Ranije mrvice, citati, veze i kontekst
nisu promijenjeni. Svih 36 incoming datoteka ostaje hash-identično,
bez dodanih ili nestalih datoteka. Registrirani izvori i poglavlja prolaze.

Za runove RUN-20261007-12, -13 i -14 te odgovarajuće DOC-0013, -0014 i -0015,
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
   Kasnije provjere su SKIPPED. JSON i traceability zato su provjereni zasebno.

Neovisni SQL pregled svih 2.646 veza našao je nula netočnih citata,
nula veza na drugi dokument i nula metoda različitih od EXACT.
Semantički pregled proveo je Codex; Claudeova potvrda nije pretpostavljena.
Continuity check završio je kodom 1 zbog ranijeg handoff commita i faze u
tijeku. Ownerovo proceed znači nastavak chunked, ne rollback.
Framework, prompt, regulativna baza i pravila ocjenjivanja nisu mijenjani.

## Sljedeća radnja

Nastaviti softverske upute DOC-0016 (konfiguracija), DOC-0017 (verifikacija
i validacija) i DOC-0018 (instalacija i rukovanje). Prilagoditi veličinu paketa
stvarnom opsegu teksta; bez nove prompt odluke i razvojnih paketa.
Ostaje 12 dobavljačkih dokumenata. Regulatorna ekstrakcija, primjenjivost
i kasnije ocjenjivanje još nisu završeni. Novi score nije izračunat.
