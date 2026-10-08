# Enconet — prijedlog primjenjivosti za G2

**Status: nacrt za vlasnika. Nije odobren ni primijenjen.**
Predložena referenca odluke: `G2-RUN-20261008-17`.
Budući evaluation run: `RUN-20261008-17`; taj run još ne postoji u bazi.

## Kratko: što predlažemo

U pregled uključiti **svih 18 kriterija**, ali samo za dokumentirane
Enconetove odgovornosti. Part21 ostaje zasebna provjera.
To nije tvrdnja da su kriteriji zadovoljeni. Primjenjivo znači: **ovo trebamo
provjeriti**. Ocjena će tek opisati koliko dobro dokumenti pokrivaju zahtjev.

Enconet je jedini dobavljač u auditu. NEK je korisnik, a ne drugi auditirani
dobavljač. Podugovarače gledamo kroz Enconetovu kontrolu njihovog rada.
Nije pretpostavljeno da su svi mogući ugovorni poslovi stvarno izvođeni.

**Važna odluka: kriterij XIII.** NQAP §14.1 kaže da ga dotadašnje usluge ne
traže. RU-82-05 ipak uređuje fizičko čuvanje instrumenata, a RU-73-03
fizičke softverske medije. Predlažem ograničen pregled tih odgovornosti,
a ne zahtjeve opće logistike ili vlastite proizvodnje. Vlasnik treba
odobriti taj prijedlog ili navesti drukčiju granicu. Sukob izvora nije skriven.

## Jedna matrica — bez novih kategorija

Postojeći runtime koristi DA/NE za kriterij. Posebni uvjeti aktivnosti
ostaju u obrazloženju. Nisu dodane nove oznake ili kategorije ocjene.

| Kriterij | Tema | Prijedlog | Glavni izvor |
|---|---|---|---|
| I | Ustrojstvo | DA | NP3.1 |
| II | QA program | DA | NP2.1-2.3 |
| III | Projektiranje | DA | NP1.2 i5.1-5.4 |
| IV | Nabavni dokumenti | DA | NP6.1 |
| V | Postupci i upute | DA | NP2.2 |
| VI | Kontrola dokumenata | DA | NP4.1-4.3 |
| VII | Dobavljači i prihvat | DA | NP6.2-6.3 |
| VIII | Identifikacija i sljedivost | DA | NP7.1 |
| IX | Posebni procesi | DA | NP8.1-8.2 |
| X | Inspekcija | DA | NP9.1 |
| XI | Ispitivanje | DA | NP9.2 i softverske upute |
| XII | Mjerna i testna oprema | DA | NP9.3 i RU-82-05 |
| XIII | Rukovanje i skladištenje | DA — ograničen opseg, vidi sukob izvora | RU-82-05§6.2; NP7.2 i14.1; RU-73-03§1.2/4.2 |
| XIV | Status pregleda, testa i rada | DA | NP9.4 |
| XV | Nesukladnosti | DA | NP10.1-10.2 |
| XVI | Korektivne radnje | DA | NP11.1 |
| XVII | QA zapisi | DA | NP12.1-12.2 |
| XVIII | Auditi | DA | NP13.1 |

## Obrazloženje i stvarni vendor citati

Primjeri niže birani su radi opsega, ne radi broja crumbs ili buduće ocjene.
Prazna tablica ili naslov nisu uzeti kao dokaz provedbe. Citati su povezani
s postojećim, aktivnim vendor crumbs i stvarnim poglavljima u bazi.


### I — Ustrojstvo

Predloženo: **DA**.

Ustrojstvo, ovlasti i QA odgovornosti vrijede za Enconet i posao podugovarača. Ocjenjuje se njegov sustav, ne druge tvrtke kao zasebni dobavljači.

Granica: Ugovorni i organizacijski odnosi; NEK nije drugi auditirani dobavljač.

Izvor: NP3.1; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_I-0009`,
citat `QUOTE-DOC-0001-0060-01`, poglavlje `CHUNK-DOC-0001-0014`.

~~~~text
Principi organizacije, komuniciranja i obavješćivanja u Enconetu koji su razrađeni i predstavljeni u Priručniku kvalitete prema normi ISO 9001:2015 vrijede za sve djelatnosti Enconeta.
~~~~

### II — QA program

Predloženo: **DA**.

NQAP pokriva nuklearne projekte, kontrolirane uvjete, kvalifikaciju i ocjenu uprave. Primjenjivost ne znači da je tvrdnja o sukladnosti dokazana.

Granica: Razina kontrole prati važnost posla, uz odobrenu audit osnovu.

Izvor: NP2.1-2.3; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_II-0017`,
citat `QUOTE-DOC-0001-0036-01`, poglavlje `CHUNK-DOC-0001-0009`.

~~~~text
Enconet NQAP predstavlja dokument kvalitete najviše razine (razine 1 – krovni dokument). Organiziran je tako da postavlja QA Program koji odgovara na sve zahtjeve sigurnosnog propisa IAEA General Safety Requirements, No. GSR Part 2, Vienna 2016, Leadership and Management for Safety, 10CFR50, App. B, 10CFR21, Reporting of Defects and Noncompliance, ASME NQA-1, QA Requirements for Nuclear Facility Aplications i dodatnih sigurnosnih uputa. NQAP će biti uključen u svaki nuklearni projekt u kojem Enconet sudjeluje.
~~~~

### III — Projektiranje

Predloženo: **DA**.

Sigurnosne analize, projekti, modifikacije i verifikacija dokumentirani su dio usluga. Projektiranje i provjera softvera također su uključeni.

Granica: Samo preuzete projektne odgovornosti. PartII2.7 vrijedi za primjenjivi softver; rezultat može imati dopušten put neovisne provjere svake primjene.

Izvor: NP1.2 i5.1-5.4; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_III-0006`,
citat `QUOTE-DOC-0001-0091-01`, poglavlje `CHUNK-DOC-0001-0022`.

~~~~text
- Razvijanje, obnavljanje ili pojednostavljenje postupaka upravljanja projektom značajnih za kvalitetu sukladno zahtjevima korisnika;
~~~~

### IV — Nabavni dokumenti

Predloženo: **DA**.

Enconet izrađuje ili procjenjuje nabavne dokumente i prenosi tehničke i QA zahtjeve.

Granica: Nabava i uloga ovlaštenika kupca u okviru ugovora, ne automatski cijela nabava NEK-a.

Izvor: NP6.1; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_IV-0003`,
citat `QUOTE-DOC-0001-0108-01`, poglavlje `CHUNK-DOC-0001-0028`.

~~~~text
- Izrada ili procjena nabavnih dokumenata glede primjerenosti zahtjeva kvalitete;
~~~~

### V — Postupci i upute

Predloženo: **DA**.

Rad koji utječe na kvalitetu vodi se prema pisanim postupcima, uputama ili nacrtima s mjerilima prihvata.

Granica: Upute za Enconetov kvalitetno značajan rad.

Izvor: NP2.2; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_V-0001`,
citat `QUOTE-DOC-0001-0050-01`, poglavlje `CHUNK-DOC-0001-0011`.

~~~~text
Aktivnosti koje utječu na kvalitetu moraju se izvoditi prema pisanim postupcima,
uputama ili nacrtima. U svakom postupku utvrditi će se kvantitativno i/ili
kvalitativno kriterij prihvaćanja. Ovi postupci moraju biti odobreni, objavljeni i
razdijeljeni u kontroliranim uvjetima.
~~~~

### VI — Kontrola dokumenata

Predloženo: **DA**.

Kontroliraju se vlastiti, korisnički i vanjski dokumenti te njihova izdanja i promjene.

Granica: Kontrola propisujućih dokumenata, ne zamjena za čuvanje gotovih zapisa iz XVII.

Izvor: NP4.1-4.3; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_VI-0013`,
citat `QUOTE-DOC-0001-0079-01`, poglavlje `CHUNK-DOC-0001-0018`.

~~~~text
Upute, postupci i nacrti koje koristi Enconet moraju se kontrolirati. Nadzor dokumenata mora zadovoljavati, neovisno o podrijetlu dokumenata (izrađeni u Enconetu, dobiveni od trećih ili od kupca) sljedeće minimalne zahtjeve:
~~~~

### VII — Dobavljači i prihvat

Predloženo: **DA**.

Program propisuje izbor dobavljača i dokaz prihvata proizvoda ili usluge. To uključuje kvalitetno značajne podugovarače i softver.

Granica: Samo dobave za koje Enconet odgovara. PartII2.14 kad se obavlja primjenjivi dedication, ne za svaku uredsku kupnju.

Izvor: NP6.2-6.3; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_VII-0005`,
citat `QUOTE-DOC-0001-0126-01`, poglavlje `CHUNK-DOC-0001-0030`.

~~~~text
Enconet mora vrednovati sposobnosti isporučitelja, te na temelju dobivenih
rezultata izvršiti izbor isporučitelja. Voditelj QA poslova odgovoran je za
uspostavljanjem i obnavljanjem odobrene liste isporučitelja.
~~~~

### VIII — Identifikacija i sljedivost

Predloženo: **DA**.

Za predmete pod nadzorom Enconeta traži se identifikacija i sljedivost. Relevantni su i instrumenti te kontrolirani softverski konfiguracijski predmeti.

Granica: Predmeti i zapisi u preuzetoj ulozi; ne pretpostavlja se vlastita proizvodnja dijelova.

Izvor: NP7.1; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_VIII-0002`,
citat `QUOTE-DOC-0001-0134-01`, poglavlje `CHUNK-DOC-0001-0033`.

~~~~text
Enconet mora obavljati identifikaciju i kontrolu materijala, dijelova i komponenti koji su pod nadzorom Enconeta prilikom isporuke, ugradnje i rada, pomoću oznaka šarže, broja dijela, serijskog broja ili nekim drugim odgovarajućim načinom, bilo oznakom na dijelu bilo pomoću zapisa o sljedivosti dijelova.
~~~~

### IX — Posebni procesi

Predloženo: **DA**.

NQAP izričito navodi vizualne QC aktivnosti kao specijalne procese. Zato kriterij nije izuzet samo zbog konzultantske djelatnosti.

Granica: Vizualne QC aktivnosti i kvalifikacije u odobrenom opsegu. Zavarivanje, toplinska obrada i drugi procesi ne pretpostavljaju se bez ugovora.

Izvor: NP8.1-8.2; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_IX-0003`,
citat `QUOTE-DOC-0001-0146-01`, poglavlje `CHUNK-DOC-0001-0038`.

~~~~text
Enconet je do sada uključen u kategoriju specijalnih procesa na području vizualne kontrole QC aktivnosti. Trening i zdravstveni uvjeti osiguravaju se u sklopu zahtjeva NE Krško. Direktni izvršioci imaju odgovarajući trening i zdravstvene kontrole vida. Specijalni procesi provode se u skladu sa zahtjevima ugovorenih poslova.
~~~~

### X — Inspekcija

Predloženo: **DA**.

Inspekcija proizvoda, usluga ili rada pod Enconetovim nadzorom ima kriterije i neovisne izvršitelje.

Granica: Samo preuzeti pregled i svjedočenje; ne sva inspekcija u elektrani.

Izvor: NP9.1; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_X-0003`,
citat `QUOTE-DOC-0001-0151-01`, poglavlje `CHUNK-DOC-0001-0040`.

~~~~text
Ispitivanje dijelova, proizvoda ili usluga u opsegu isporuke Enconeta ili pod njegovim nadzorom mora provoditi osoblje koje nije sudjelovalo u izvođenju aktivnosti koje se pregledavaju. Kriteriji prihvatljivosti i verifikacije sukladnosti moraju se utvrditi u dokumentiranim uputama, postupcima i nacrtima. Ukoliko nije moguće ispitivanje obrađenog dijela, proizvoda ili usluge, provodit će se praćenje procesa na način naveden u poglavlju 8. ovog NQAP.
~~~~

### XI — Ispitivanje

Predloženo: **DA**.

Dokumenti uređuju ugovorene ili regulatorne testove, a programski testovi i dijagnostika dio su razmotrenih usluga.

Granica: Primjenjivi software/diagnostic testovi i ugovoreni programi. Ne izmišlja se laboratorijska djelatnost.

Izvor: NP9.2 i softverske upute; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_XI-0002`,
citat `QUOTE-DOC-0001-0156-01`, poglavlje `CHUNK-DOC-0001-0041`.

~~~~text
Ukoliko je testiranje ugovorna ili regulatorna obveza, mora se izraditi program testiranja i dokumentirati rezultate testova.
~~~~

### XII — Mjerna i testna oprema

Predloženo: **DA**.

Odabir, umjeravanje i kontrola mjerne/testne opreme uređeni su dokumentima.

Granica: Prijenosna MTE kad je potrebna za posao; ne sva trajno ugrađena oprema NEK-a ili svako računalo.

Izvor: NP9.3 i RU-82-05; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_XII-0002`,
citat `QUOTE-DOC-0001-0158-01`, poglavlje `CHUNK-DOC-0001-0042`.

~~~~text
Mora se izvršiti pravilan izbor opreme za pregled, mjerenje i ispitivanje kako bi se zadovoljilo mjerno područje, vrsta, točnost i preciznost mjerenja.
~~~~

### XIII — Rukovanje i skladištenje

Predloženo: **DA**.

Predlaže se ograničena primjenjivost za zaštitu, rukovanje i skladištenje MTE te relevantnih fizičkih softverskih medija. Dokumentirani procesi daju razlog za pregled, unatoč općem izuzeću u NP14.1.

Granica: IZRIČITA ODLUKA VLASNIKA: ograničeni pregled dokumentiranih odgovornosti, ne opća logistika isporučenih komponenti. Trenutna stvarna MTE zaduženja i ugovor treba potvrditi; obrazac nije dokaz korištenja.

Izvor: RU-82-05§6.2; NP7.2 i14.1; RU-73-03§1.2/4.2; dokument `DOC-0025`, crumb `CRUMB-DOC-0025-APP_B_XIII-0003`,
citat `QUOTE-DOC-0025-0041-01`, poglavlje `CHUNK-DOC-0025-0009`.

~~~~text
MTE se čuva i skladišti u prostorijama koje moraju zadovoljavati kriterije koje su predpisane za pojedini instrument (temperature, vlaga, agresivnost atmosfere, pritisak, vibracije itd.)
~~~~

### XIV — Status pregleda, testa i rada

Predloženo: **DA**.

Oznake i zapisnici prikazuju stanje pregleda/testa i sprečavaju uporabu neprihvaćenog predmeta.

Granica: Status u Enconetovoj ulozi pregleda/testa, uključujući relevantne instrumente i odobrenu verziju softvera.

Izvor: NP9.4; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_XIV-0001`,
citat `QUOTE-DOC-0001-0164-01`, poglavlje `CHUNK-DOC-0001-0043`.

~~~~text
Oprema za mjerenje i ispitivanje mora biti jednoznačno obilježena, tako da se u slučaju korištenja te opreme njena oznaka prenosi na pojedinačne entitete koji su pregledani i ispitani. Trebaju se koristiti tipske kartice ili zapisnici pregleda radi utvrđivanja stanja pregleda i ispitivanja, kao i sljedivost testiranih entiteta kroz izvješća. Kod testiranih sustava, komponenti i dijelova koristit će se fizičko označivanje karticama kako bi se spriječila nepažljiva uporaba.
~~~~

### XV — Nesukladnosti

Predloženo: **DA**.

Nesukladan proizvod ili usluga prepoznaje se, ocjenjuje i kontrolira do odobrene odluke.

Granica: QA nesukladnosti nisu automatski reportable defects prema Part21; Part21 provjera ostaje zasebna.

Izvor: NP10.1-10.2; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_XV-0001`,
citat `QUOTE-DOC-0001-0166-01`, poglavlje `CHUNK-DOC-0001-0045`.

~~~~text
Cjelokupno osoblje Enconeta koje izvodi aktivnosti značajne za kvalitetu, snosi odgovornost za prepoznavanje i izvješćivanje o nesukladnostima. Izvješća o takvim entitetima ili uslugama moraju se dostaviti voditelju projekta ili voditelju QA poslova. Nesukladni entiteti moraju se identificirati, označiti i izdvojiti sve dok voditelj projekta ne odredi daljnje postupanje.
~~~~

### XVI — Korektivne radnje

Predloženo: **DA**.

Korektivne radnje i analiza uzroka za značajan problem dio su programa.

Granica: Opseg prati značaj problema; izvještavanje prema Part21 razmatra se zasebno.

Izvor: NP11.1; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_XVI-0001`,
citat `QUOTE-DOC-0001-0171-01`, poglavlje `CHUNK-DOC-0001-0048`.

~~~~text
Uvjeti koji ugrožavaju kvalitetu moraju se popravljati. Utvrđena nesukladnost mora se zabilježiti i rješavati prema poglavlju 10. ovog NQAP.
~~~~

### XVII — QA zapisi

Predloženo: **DA**.

Zapisi dokazuju kvalitetu usluga i moraju biti identificirani, sačuvani i dohvatljivi.

Granica: Gotovi QA zapisi; dopuštene metode čuvanja ostaju vidljive. Prazni obrasci nisu dokazi provedbe.

Izvor: NP12.1-12.2; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_XVII-0004`,
citat `QUOTE-DOC-0001-0174-01`, poglavlje `CHUNK-DOC-0001-0050`.

~~~~text
QA zapisi se moraju pripremati kako bi se pružio objektivni dokaz postignute kvalitete.
~~~~

### XVIII — Auditi

Predloženo: **DA**.

Program propisuje neovisne interne i vanjske audite s praćenjem popravnih radnji.

Granica: Auditi Enconetova sustava i njegovih kvalitetno značajnih dobavljača; ne audit svih poduzeća NEK-a.

Izvor: NP13.1; dokument `DOC-0001`, crumb `CRUMB-DOC-0001-APP_B_XVIII-0004`,
citat `QUOTE-DOC-0001-0181-01`, poglavlje `CHUNK-DOC-0001-0053`.

~~~~text
Usvajanje i uspješnost QA Programa Enconeta mora se verificirati kroz nezavisno ocjenjivanje kvalitete. Takvo nezavisno ocjenjivanje mora se provoditi prema pisanim postupcima i upitnicima.
~~~~

## XIII — zašto opće izuzeće treba razriješiti

NQAP §7.2 veže kontrolu uz odgovornost za aktivnost:

~~~~text
Enconet mora kontrolirati aktivnosti rukovanja, otpreme i skladištenja u svrhu sprječavanja oštećenja, propadanja ili gubitka proizvoda. Ukoliko je potrebno, moraju se utvrditi, propisati, održavati i verificirati posebne mjere o rukovanju i zaštitnim okolišnim uvjetima prilikom transporta i skladištenja onda kad je Enconet odgovoran za navedene aktivnosti.
~~~~

NQAP §14.1, `CRUMB-DOC-0001-APP_B_XIII-0003`, navodi drukčiju granicu dotadašnjeg rada:

~~~~text
Izuzetak:
Priručnik kvalitete ne uključuje kriterij XIII Appendix-a B, 10CFR50. Dosadašnje aktivnosti Enconeta po svojoj naravi i opsegu ne zahtijevaju primjenu navedenog kriterija XIII - Handling, Storage and Shipping.
Prilikom pružanja usluga u NEK-u, Enconetovi djelatnici u radu primjenjuju QA program NEK-a.
Ukoliko Enconet u budućnosti bude pružao usluge NE Krško, koje bi zahtijevale primjenu kriterija XIII, Dodatka B, 10CFR50, poštivati će se zahtjevi odgovarajućih postupaka NE Krško, što nije u suprotnosti s kodom i biti će specificirano u ponudi Enconeta. U slučaju opsežnih i dugotrajnih radova na području koje bi zahtijevalo striktnu primjenu tog kriterija Enconet će razviti svoje postupke.
~~~~

RU-82-05 §6.2 ima konkretan zahtjev čuvanja instrumenata; citat je u odjeljku
XIII iznad. Njegov §2 veže nabavu MTE uz zahtjev kupca u projektu. RU-73-03
§1.2 i §4.2 uređuju fizičke medije, uz pohranu i provjeru sadržaja.
To dokazuje da dokumenti opisuju takve kontrole, ali ne dokazuje današnje
zaduženje instrumenta ili izveden projekt. Prazni obrasci nisu izvedeni zapisi.

Predloženo rješenje: zadržati XIII za dokumentiranu spremnost i preuzete
odgovornosti zaštite/rukovanja/skladištenja MTE i relevantnih fizičkih medija.
Ne zahtijevati opće pakiranje i otpremu komponenti koje Enconet ne preuzima.
Sama pohrana QA zapisa ostaje XVII; ne računati je dvaput samo zbog riječi
skladištenje. Konačne ocjene traže zasebno obrazloženje i svrhu svake kontrole.

Ako vlasnik potvrdi da sadašnji audit potpuno isključuje fizičko zaduženje
i zaštitu ovih predmeta, treba izmijeniti XIII na NE uz tu konkretnu granicu,
umjesto odobriti ovaj nacrt. To nije zaključak izveden samo iz nedostatka dokaza.

## Part21 — zaseban opseg, bez bodova u AppendixB rezultatu

Predlažemo pregled Part21 spremnosti koju Enconet sam navodi u NQAP §1.1,
§2.1 i §10.2: ocjena problema, odgovornosti, eskalacija kupcu i potrebni
zapisi. Dokaz iz §10.2 je `CRUMB-DOC-0001-APP_B_XV-0004`:

~~~~text
Voditelj QA analizira sve nesukladnosti a posebno obzirom na zahtjeve 10CFR Part21, te o nalazima obavještava direktora, koji je odgovoran za izvještavanje kupca / naručitelja u slučaju potrebe.
~~~~

Ne pretpostavljamo neposrednu NRC jurisdikciju, postojeću obvezu stvarne
NRC prijave, US ugovor ili ulogu dedicating entity. Za to trebaju odgovarajući
ugovorni ili pravni temelj, uloga i događaj. To su uvjeti Part21 provjere,
ne novi kriteriji, ocjene ili dodatni bodovi. Nije poslana vanjska prijava.

## ASME i granice ovog odobrenja

G1 već odabire dostavljeni NQA-1:2015 PartI. Vlasnik je zasebno odobrio samo
izričito upućene PartII2.7/2.14 kad se odgovarajuća aktivnost obavlja.
Ostali PartII te PartsIII–IV ostaju podrška. G2 ne proširuje taj opseg.
Starije reference NQAP-a ostaju pitanje provjere izdanja, ne automatska
nesukladnost. Izvorni fragment §2.7.201 ostaje označen: nedostajuće riječi
nisu izmišljene. To nije dokaz lošeg dobavljača; PartI Requirement17 ostaje
osnova za QA zapise.

PP-74-01 se navodi u NQAP-u, ali zasebna datoteka nije u dostavljenom
inventaru od 26 vendor dokumenata. Treba provjeriti ili zatražiti taj postupak
u pregledu dokaza. Nedostajući dokument nije razlog da nabavu proglasimo NE.

## Paket i provjere

- [Matrica za postojeći importer nakon odobrenja](G2_APPLICABILITY_MATRIX_20261008.json).
- [Točni dokazi, ID veze, hashes i naredbe](G2_APPLICABILITY_EVIDENCE_20261008.json).
- [NP-SUK-001 — dostavljeni tekst](../out/2026-10-07/full-keyword-sweep/sources/DOC-0001.md).
- [RU-82-05 — dostavljeni tekst](../out/2026-10-07/full-keyword-sweep/sources/DOC-0025.md).
- [RU-73-03 — dostavljeni tekst](../out/2026-10-07/full-keyword-sweep/sources/DOC-0018.md).
- Aktivni metrics: [NP run](../sieving/runs/RUN-20261007-01/metrics.json),
  [ASME PartI](../sieving/runs/RUN-20261008-14/metrics.json),
  [upućeni PartII](../sieving/runs/RUN-20261008-15/metrics.json),
  [Part21](../sieving/runs/RUN-20261008-16/metrics.json).

Read-only provjera nacrta: exit **0**, svih 18 jedinstvenih kriterija,
24 postojeće točne evidence veze. Database i project-state hashes ostaju
jednaki; nema applicability, evaluation ili score redova. Traceability i
requirements provjere prolaze s exit0. Incoming: svih 36 datoteka nepromijenjeno.
Aggregate: exit0, četiri provjere faze chunked prolaze; kasnije su SKIPPED.

**Ovo je pre-gate prijedlog, ne već izdani phase-routed G2 packet.**
Faza je i dalje chunked, G2 pending. Canonical G2 packet pripada fazi sieved;
nije zaobiđen dispatcher niti je unos odobrenja glumljen. Nakon vlasnikove
odluke treba dovršiti normalnu faznu provjeru i evidentiranje prije importa.

## Odluka vlasnika

Možete:

1. **Odobriti `G2-RUN-20261008-17`** — svih 18 DA s opisanim granicama,
   uključujući ograničeni XIII te zasebni Part21 QA pregled bez pretpostavljene
   neposredne NRC jurisdikcije.
2. Navesti ispravak kriterija ili opsega, posebno XIII.
3. Odgoditi odluku i zatražiti dodatni ugovorni dokaz.

Odobrenje bira što će se procijeniti. Ne potvrđuje conformance, ne daje
pozitivne ocjene i ne zahtijeva od vlasnika da sam unese ocjenu svakog kriterija.
Dokumentacijsku procjenu priprema Codex u sljedećem koraku prema postojećoj
metodologiji. Claude review ostaje odgođen i nije glumljen.
