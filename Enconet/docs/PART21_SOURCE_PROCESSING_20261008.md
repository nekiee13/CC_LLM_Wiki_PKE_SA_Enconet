# Enconet — zasebna Part 21 obrada

## Rezultat

Pročitan je cijeli dostavljeni DOC-0027: svih 14 odjeljaka Part21.
Run `RUN-20261008-16` ima **41 izvorni item** i **41 točan citat**
povezan s odgovarajućim pohranjenim poglavljem.

- **24** proceduralne obveze.
- **5** definicijskih items.
- **11** referentnih ili opsegovnih items.
- **1** preporučeni sadržaj interim reporta, izvorno označen riječju should.

Part21 je odvojen od 18-kriterijskog AppendixB rezultata. Kriterijski ID
služi klasifikaciji, ne dodaje bodove ili nove governing requirement redove.
Nisu pisane ocjene ni odluke G2.

## Rokovi se ne smiju pomiješati

| Obveza | Rok i početak |
|---|---|
| Ocjena potencijalno značajnog odstupanja | Što prije, najkasnije 60 dana od discovery |
| Interim report kad ocjena ne može završiti | Pisano unutar 60 dana od discovery |
| Interna obavijest odgovornoj osobi | Najkasnije pet radnih dana od dovršene ocjene, uz navedeni nalaz |
| Dobavljač koji ne može ocijeniti defekt | Kupci ili pogođeni nositelji licence: pet radnih dana od utvrđenja nedostatka sposobnosti |
| Početna NRC obavijest | Dva dana od primitka informacije odgovorne osobe prema navedenoj klauzuli |
| Pisani NRC izvještaj | 30 dana od primitka informacije odgovorne osobe prema navedenoj klauzuli |

Pet radnih dana nije isto što i pet kalendarskih dana. Početna NRC
obavijest nije isto što i interim report. Potrebno je zabilježiti točan
okidač roka, a ne samo jedan datum za cijeli postupak.

Zapisi ocjene i dobavljačke obavijesti imaju najmanje pet godina čuvanja.
Dobavljački zapisi kupaca imaju deset godina od isporuke. Posebne design
certification/approval uloge imaju petnaestogodišnje rokove zapisa kupaca;
nije pretpostavljeno da Enconet ima te uloge.

## Uvjeti i dopušteni putevi

Ne prijavljuje se NRC-u automatski svaka interna nesukladnost. Izvor traži
određeni opseg, odgovornu ulogu, događaj i sigurnosni učinak. Definicija
basic component obuhvaća i određene sigurnosno povezane usluge, ne samo robu.
Dedicating entity ima vlastite obveze; komercijalno izuzeće nije isto što i
izuzeće od dedication odgovornosti. Ovlaštenje druge osobe za prijavu ne
ukida odgovornost direktora ili odgovornog dužnosnika.

Izričito izuzeće zbog ranije prijave traži stvarno saznanje da je NRC
**pisano** obaviješten. Pretpostavka ili samo obavijest kupcu nije taj dokaz.
Dobrovoljna prijava ostaje dopuštena, ne nova obveza svakog subjekta.

G1 je odobrio zasebnu Part21 obradu. **Neposredna NRC jurisdikcija za
Enconet nije pretpostavljena.** US/licencni ili ugovorni temelj, uloga i
primjenjive dužnosti moraju biti jasno navedeni u sljedećem scope/G2 pregledu.
Nije korištena Ekonergova odluka kao Enconetova pravna činjenica.

Kontaktni podaci u citatima dio su dostavljenog izvora. Njihova aktualnost
nije potvrđena. Prije stvarne vanjske prijave treba provjeriti službeni
kanal. Ovim zadatkom nije poslana nikakva prijava van projekta.

## Dokazi i stanje

- [Stvarni items i citati](../sieving/runs/RUN-20261008-16/REVIEW.md).
- [Zasebna duty mapa i uvjeti](../sieving/runs/RUN-20261008-16/part21-duty-map.json).
- [Naredbe, rezultati i hashes](PART21_SOURCE_EVIDENCE_20261008.json).

Vendor stanje ostaje **2.700 crumbs i 5.171 poveznica**. Governing AppendixB
ostaje 18 redova i 18 crumbs. ASME ostaje 239 interpretivnih items.
Ukupno je **2.998 crumbs i 5.677 točnih poveznica**, uz odvojenu Part21 skupinu.
Svi raniji redci 15 provjerenih DB tablica ostaju hash-exact, kao i 36 incoming
files. Postojeći izvori, poglavlja i aktivne generacije nisu mijenjani.

Strict JSON, traceability, requirements i exact-link retry prolaze s exit 0.
Aggregate ima exit 0: četiri provjere faze chunked prolaze; downstream je
SKIPPED. Te provjere nisu zamjena za odgođeni Claude semantic review.
Raniji koordinacijski metadata problem ostaje otvoren, nije proglašen passed.

## Sljedeće

Pripremiti obrazloženu primjenjivost svih 18 kriterija i zasebni Part21 scope
za G2. Ne širiti obradu na ostatak Part II ili Parts III–IV. Provjeriti
fragment ASME2.7 §201 i razriješiti raniju metadata korekciju uz izričito
odobrenje. Faza ostaje chunked; G2–G7 ostaju pending.
