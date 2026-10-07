# Enconet v3 - golden calibration candidate

Status: **owner-approved expected examples**, 7 October 2026. Reference:
`GOLDEN-ENCONET-NP-V3-20261007` in `manifests/approvals.csv`.
These 20 manually selected examples are vendor evidence from DOC-0001, not
regulatory requirements, active crumbs, or a compliance score.

The sample covers all 18 criterion intents. It is not a fixed quota or full sieving of this manual. `objective_control` means a concrete written control, not proof that someone executed it. `supporting_control` keeps indirect evidence; `candidate_lead` does not prove compliance. Original Croatian quotes stay exact.

The owner approved the expected evidence and mappings for calibration. This
does not approve applicability, a generation or an audit score, and does not
itself activate the prompt. The optional-context storage gap has now been
fixed and tested on synthetic databases: evidence type and source anchors
survive import and retrieval. No live crumb import was attempted.

The XIII conditional policy and claimed exception must both remain visible, without automatically deciding N/A. These are meaning-based matches, not keyword-count scoring.

## 1. APP_B_I - Organization

**Expected crumb:** objective_control: Voditelj QA prijavljuje neriješene probleme kvalitete direktoru i može inicirati obustavu radova sigurnosne klase.

**What & why:** QA ovlast i put eskalacije; ne dokazuje da je obustava stvarno provedena.

**Chapter:** 3 ORGANIZACIJA [line 226] > 3.1 Odgovornosti, ovlaštenja i komunikacije [line 230]

**Source link:** `CHUNK-DOC-0001-0014` in the local database, document DOC-0001.

> Odgovornost voditelja QA poslova je izvještavanje direktora o bilo kojem neriješenom problemu kvalitete ili bilo kojem nesukladnom entitetu, ukoliko na razini voditelja projekata nema rješenja ili rješenje nije zadovoljavajuće. Ukoliko je entitet ili usluga nuklearne sigurnosne klase, ovlašten je da inicira proces obustave radova sve dok se ne postigne zadovoljavajuće rješenje.

## 2. APP_B_II - Quality Assurance Program

**Expected crumb:** objective_control: Direktor je odgovoran za izobrazbu, godišnji plan i čuvanje dokaza o osposobljenosti.

**What & why:** Konkretna podrška programu kvalitete kroz osposobljavanje.

**Chapter:** 1 UVOD [line 123] > 2 PROGRAM OSIGURAVANJE KVALITETE [line 154]

**Source link:** `CHUNK-DOC-0001-0009` in the local database, document DOC-0001.

> Direktor Enconeta snosi odgovornost za primjenu programa izobrazbe cjelokupnog osoblja koje izvodi aktivnosti značajne za kvalitetu. Priprema se godišnji plan izobrazbe, a dokazi o sudjelovanju učesnika i njihovoj osposobljenosti smatraju se QA dokumentacijom.

## 3. APP_B_III - Design Control

**Expected crumb:** objective_control: Stručnjaci koji verificiraju projekt ne smiju sudjelovati u njegovoj izradi.

**What & why:** Namjena je neovisna provjera projektiranja, a ne opći audit.

**Chapter:** 5 UPRAVLJANJE PROJEKTOM [line 306] > 5.3 Verifikacija projekta [line 334]

**Source link:** `CHUNK-DOC-0001-0024` in the local database, document DOC-0001.

> Voditelj projekta odgovoran je za određivanje stručnjaka koji će sudjelovati u stručnom timu za verifikaciju projekta, a koji nisu učestvovali u izradi projekta.

## 4. APP_B_IV - Procurement Document Control

**Expected crumb:** objective_control: Voditelji prenose regulatorne, projektne i kvalitativne zahtjeve u nabavne dokumente.

**What & why:** Tok zahtjeva prema dobavljaču; ne dokaz primitka robe.

**Chapter:** 6 KONTROLA NABAVE [line 359] > 6.1 Općenito [line 364]

**Source link:** `CHUNK-DOC-0001-0028` in the local database, document DOC-0001.

> Voditelji projekata odgovorni su da se odgovarajući zahtjevi prenesu iz regulatornih zahtjeva, temeljnih projektnih podataka, standarda, specifikacija i zahtjeva kvalitete u nabavne dokumente proizvoda ili usluga.

## 5. APP_B_V - Instructions, Procedures, and Drawings

**Expected crumb:** objective_control: Pisani postupci propisuju rad i kriterije prihvaćanja te se odobravaju i kontrolirano dijele.

**What & why:** Kriteriji prihvaćanja razlikuju radne upute od pukog pozivanja na standard.

**Chapter:** 2 PROGRAM OSIGURAVANJE KVALITETE [line 184] > 2.2 Postupci, upute i nacrti [line 193]

**Source link:** `CHUNK-DOC-0001-0011` in the local database, document DOC-0001.

> Aktivnosti koje utječu na kvalitetu moraju se izvoditi prema pisanim postupcima,
> uputama ili nacrtima. U svakom postupku utvrditi će se kvantitativno i/ili
> kvalitativno kriterij prihvaćanja. Ovi postupci moraju biti odobreni, objavljeni i
> razdijeljeni u kontroliranim uvjetima.

## 6. APP_B_VI - Document Control

**Expected crumb:** objective_control: Promjene dokumenata prolaze pregled i odobrenje kao izvornik, uz pristup izvornim podlogama.

**What & why:** Kontrola izmjene propisujućih dokumenata.

**Chapter:** 4 UPRAVLJANJE DOKUMENTIMA [line 272] > 4.3 Kontrola promjene dokumenta [line 298]

**Source link:** `CHUNK-DOC-0001-0020` in the local database, document DOC-0001.

> Promjene u dokumentima i podacima moraju biti podvrgnute istom postupku kao i izvorno izdanje. Pregled i odobrenje mora izvršiti ista organizacijska jedinica koja je izvršila pregled i odobrenje izvornika ili neka druga posebno određena organizacija koja ima pristup relevantnim podlogama na temelju kojih je odobren izvornik.

## 7. APP_B_VII - Control of Purchased Material, Equipment, and Services

**Expected crumb:** objective_control: Prije uporabe nabavljenog proizvoda ili usluge mora se dokumentirano dokazati sukladnost.

**What & why:** Dokaz prihvata dobave; odvojeno od kriterija IV.

**Chapter:** 6 KONTROLA NABAVE [line 392] > 6.3 Kontrola naručenih proizvoda i usluga [line 423]

**Source link:** `CHUNK-DOC-0001-0031` in the local database, document DOC-0001.

> Prije ugradnje ili korištenja proizvoda ili usluge pod nadzorom Enconeta, mora se
> dokumentirano dokazati sukladnost s nabavnim dokumentima.

## 8. APP_B_VIII - Identification and Control of Materials, Parts, and Components

**Expected crumb:** supporting_control: Kad fizička oznaka nije praktična, identifikacija se održava proceduralnom kontrolom.

**What & why:** Fuzzy koncept: identitet se može očuvati postupkom, ne samo oznakom.

**Chapter:** 7 KONTROLA MATERIJALA, DIJELOVA I KOMPONENTI [line 436] > 7.1 Identifikacija i kontrola materijala, dijelova i komponenti [line 441]

**Source link:** `CHUNK-DOC-0001-0033` in the local database, document DOC-0001.

> Fizička identifikacija provodit će se koliko je to maksimalno moguće ostvariti. Ukoliko je to nepraktično, usvojit će se proceduralna kontrola.

## 9. APP_B_IX - Control of Special Processes

**Expected crumb:** objective_control: Za vizualnu QC kontrolu navedeni su trening i zdravstvene kontrole vida u ugovorenom opsegu.

**What & why:** Konkretna izjava o posebnom procesu; ne potvrđuje kvalifikaciju za druge procese.

**Chapter:** 8 UPRAVLJANJE PROCESOM [line 461] > 8.2 Specijalni procesi [line 472]

**Source link:** `CHUNK-DOC-0001-0038` in the local database, document DOC-0001.

> Enconet je do sada uključen u kategoriju specijalnih procesa na području vizualne kontrole QC aktivnosti. Trening i zdravstveni uvjeti osiguravaju se u sklopu zahtjeva NE Krško. Direktni izvršioci imaju odgovarajući trening i zdravstvene kontrole vida. Specijalni procesi provode se u skladu sa zahtjevima ugovorenih poslova.

## 10. APP_B_X - Inspection

**Expected crumb:** objective_control: Pregled obavlja osoblje koje nije izvodilo provjeravani rad, prema dokumentiranim kriterijima.

**What & why:** Mapiranje po cilju neovisne inspekcije unatoč riječi ispitivanje.

**Chapter:** 9 INSPEKCIJA I TESTIRANJE [line 486] > 9.1 Program inspekcije [line 491]

**Source link:** `CHUNK-DOC-0001-0040` in the local database, document DOC-0001.

> Ispitivanje dijelova, proizvoda ili usluga u opsegu isporuke Enconeta ili pod njegovim nadzorom mora provoditi osoblje koje nije sudjelovalo u izvođenju aktivnosti koje se pregledavaju. Kriteriji prihvatljivosti i verifikacije sukladnosti moraju se utvrditi u dokumentiranim uputama, postupcima i nacrtima. Ukoliko nije moguće ispitivanje obrađenog dijela, proizvoda ili usluge, provodit će se praćenje procesa na način naveden u poglavlju 8. ovog NQAP.

## 11. APP_B_XI - Test Control

**Expected crumb:** objective_control: Postupci testiranja propisuju okolišne uvjete, kvalifikacije osoblja i kalibraciju instrumenata.

**What & why:** Planirano testiranje, ne opća inspekcija.

**Chapter:** 9 INSPEKCIJA I TESTIRANJE [line 486] > 9.2 Program testiranja [line 501]

**Source link:** `CHUNK-DOC-0001-0041` in the local database, document DOC-0001.

> Testiranje pod nadzorom Enconeta mora se izvoditi prema pisanim postupcima testiranja. Takvi postupci moraju utvrditi odgovarajuće okolišne uvjete, te zahtjeve za kvalifikacijom osoblja i kalibracijom instrumenata.

## 12. APP_B_XII - Control of Measuring and Test Equipment

**Expected crumb:** objective_control: Odstupanje mjernih vrijednosti traži vrednovanje ranijih mjerenja od posljednje kalibracije.

**What & why:** Povratna procjena valjanosti mjerenja, ne samo popis opreme.

**Chapter:** 9 INSPEKCIJA I TESTIRANJE [line 486] > 9.3 Kalibracija i kontrola opreme za mjerenje i testiranje [line 507]

**Source link:** `CHUNK-DOC-0001-0042` in the local database, document DOC-0001.

> Oprema se mora kontrolirati s obzirom na rukovanje, skladištenje i kalibraciju. Ukoliko se utvrdi odstupanje izmjerenih vrijednosti preko dopuštenih ograničenja, mora se izvršiti vrednovanje vjerodostojnosti prije obavljenih mjerenja, a rezultati ispitivanja moraju se ponovno procijeniti za cjelokupno razdoblje od zadnje kalibracije.

## 13. APP_B_XIII - Handling, Storage, and Shipping

**Expected crumb:** supporting_control: Kada odgovara za rukovanje, prijevoz i skladištenje, Enconet propisuje zaštitne mjere protiv oštećenja.

**What & why:** Uvjetna pisana kontrola; primjenjivost i stvarni opseg ostaju za odluku.

**Chapter:** 7 KONTROLA MATERIJALA, DIJELOVA I KOMPONENTI [line 436] > 7.2 Rukovanje, skladištenje i otprema [line 451]

**Source link:** `CHUNK-DOC-0001-0034` in the local database, document DOC-0001.

> Enconet mora kontrolirati aktivnosti rukovanja, otpreme i skladištenja u svrhu sprječavanja oštećenja, propadanja ili gubitka proizvoda. Ukoliko je potrebno, moraju se utvrditi, propisati, održavati i verificirati posebne mjere o rukovanju i zaštitnim okolišnim uvjetima prilikom transporta i skladištenja onda kad je Enconet odgovoran za navedene aktivnosti.

## 14. APP_B_XIV - Inspection, Test, and Operating Status

**Expected crumb:** objective_control: Oznake i kartice povezuju ispitane entitete sa stanjem pregleda i sprječavaju nenamjernu uporabu.

**What & why:** Koncept prepoznatljivog statusa i zabrane nepažljive uporabe.

**Chapter:** 9 INSPEKCIJA I TESTIRANJE [line 486] > 9.4 Identifikacija stanja inspekcije, testa i rada [line 517]

**Source link:** `CHUNK-DOC-0001-0043` in the local database, document DOC-0001.

> Oprema za mjerenje i ispitivanje mora biti jednoznačno obilježena, tako da se u slučaju korištenja te opreme njena oznaka prenosi na pojedinačne entitete koji su pregledani i ispitani. Trebaju se koristiti tipske kartice ili zapisnici pregleda radi utvrđivanja stanja pregleda i ispitivanja, kao i sljedivost testiranih entiteta kroz izvješća. Kod testiranih sustava, komponenti i dijelova koristit će se fizičko označivanje karticama kako bi se spriječila nepažljiva uporaba.

## 15. APP_B_XV - Nonconforming Materials, Parts, or Components

**Expected crumb:** objective_control: Postupanje s nesukladnim proizvodom ili uslugom prolazi inženjersku ocjenu i odobrenje prije prihvaćanja.

**What & why:** Kontrola dispozicije nesukladnosti; ne miješati s analizom uzroka XVI.

**Chapter:** 10 KONTROLA NESUKLADNOSTI [line 523] > 10.2 Ocjena i rješavanje nesukladnosti [line 532]

**Source link:** `CHUNK-DOC-0001-0046` in the local database, document DOC-0001.

> Nesukladni proizvodi ili usluge moraju biti podvrgnuti inženjerskoj ocjeni i vrednovanju. Postupanje mora biti verificirano i odobreno od voditelja projekta prije prihvaćanja proizvoda s bilo kojim stanjem (koristi kao što je, popravak-dorada, prenamjena, odbijen ili odbačen).

## 16. APP_B_XVI - Corrective Action

**Expected crumb:** objective_control: Značajna nesukladnost traži analizu uzroka radi sprječavanja ponavljanja.

**What & why:** Cilj korektivne radnje, a ne samo popravak.

**Chapter:** 11 POPRAVNE RADNJE [line 542] > 11.1 Popravne radnje [line 547]

**Source link:** `CHUNK-DOC-0001-0048` in the local database, document DOC-0001.

> Enconet mora provesti analizu uzroka nastajanja nesukladnosti, sa svrhom sprječavanja ponavljanja u slučaju pojave uvjeta koji značajno ugrožavaju kvalitetu.

## 17. APP_B_XVII - Quality Assurance Records

**Expected crumb:** objective_control: Postupak mora propisati razdoblje čuvanja i raspolaganje zapisima kvalitete.

**What & why:** Zadržavanje dokaza kvalitete, ne kontrola izdavanja dokumenata.

**Chapter:** 12 QA ZAPISI [line 557] > 12.2 Prikupljanje, arhiviranje i čuvanje QA zapisa [line 568]

**Source link:** `CHUNK-DOC-0001-0051` in the local database, document DOC-0001.

> Vremensko razdoblje čuvanja i raspolaganja zapisima kvalitete mora biti propisano u dokumentiranom postupku. Kao minimalno, prihvatljivo je razvrstavanje zapisa i period čuvanja kako je određeno u ANSI N.45.2.9.

## 18. APP_B_XVIII - Audits

**Expected crumb:** objective_control: Audit provodi kvalificirano osoblje bez izravne odgovornosti za ocjenjivani rad, uz naknadnu provjeru popravnih radnji.

**What & why:** Neovisnost audita i praćenje učinkovitosti.

**Chapter:** 13 NEZAVISNO OCJENJIVANJE KVALITETE [line 578] > 13.1 Općenito [line 583]

**Source link:** `CHUNK-DOC-0001-0053` in the local database, document DOC-0001.

> Unutarnje, kao i vanjsko nezavisno ocjenjivanje kvalitete, mora provoditi izabrani tim kvalificiranog osoblja koje nema izravnu odgovornost za izvedbu poslova čija se uspješnost ocjenjuje. Izvješća s primjedbama i nalazima moraju se dostaviti rukovodećem osoblju organizacije i direktoru Enconeta. Naknadno nezavisno ocjenjivanje mora verificirati i zabilježiti primjenu i uspješnost provedenih popravnih radnji.

## 19. APP_B_II - Quality Assurance Program

**Expected crumb:** candidate_lead: NQAP navodi usklađenost s regulativom i standardima; objective evidence not shown.

**What & why:** Visoka referenca je trag, ne dokaz ispunjenja svih zahtjeva.

**Chapter:** 1 UVOD [line 92] > 1.1 Općenito [line 94]

**Source link:** `CHUNK-DOC-0001-0005` in the local database, document DOC-0001.

> QA Program opisan u ovom NQAP sukladan je zahtjevima propisa IAEA General Safety Requirements, No. GSR Part 2, Vienna 2016, Leadership and Management for Safety, zahtjevima Saveznog državnog zakona SAD 10CFR50, App. B, QA Criteria for Nuclear Power Plants and Fuel Reprocessing Plants, ASME NQA-1-1994 (95 addenda) and 2008 editions, QA Requirements for Nuclear Facility Aplications, 10CFR Part 21, Reporting of Defects and Noncompliance, kao i odgovarajućih propisanih preporuka, zakona i standarda ukoliko se primjenjuju za poslove kod ili za korisnika usluga Enconeta.

## 20. APP_B_XIII - Handling, Storage, and Shipping

**Expected crumb:** candidate_lead: Dobavljač tvrdi da dosadašnji opseg ne traži kriterij XIII; candidate; verify criterion mapping.

**What & why:** Sačuvati tvrdnju o izuzeću kao kontekst za primjenjivost; ne automatski prihvatiti N/A.

**Chapter:** 13 NEZAVISNO OCJENJIVANJE KVALITETE [line 578] > 14 PRILOZI [line 593]

**Source link:** `CHUNK-DOC-0001-0054` in the local database, document DOC-0001.

> Izuzetak:
> Priručnik kvalitete ne uključuje kriterij XIII Appendix-a B, 10CFR50. Dosadašnje aktivnosti Enconeta po svojoj naravi i opsegu ne zahtijevaju primjenu navedenog kriterija XIII - Handling, Storage and Shipping.
> Prilikom pružanja usluga u NEK-u, Enconetovi djelatnici u radu primjenjuju QA program NEK-a.
> Ukoliko Enconet u budućnosti bude pružao usluge NE Krško, koje bi zahtijevale primjenu kriterija XIII, Dodatka B, 10CFR50, poštivati će se zahtjevi odgovarajućih postupaka NE Krško, što nije u suprotnosti s kodom i biti će specificirano u ponudi Enconeta. U slučaju opsežnih i dugotrajnih radova na području koje bi zahtijevalo striktnu primjenu tog kriterija Enconet će razviti svoje postupke.

## Owner decision

The 20 expected examples above are approved under the recorded owner reference.
Negative/scope clues and vague references must remain visible; they are not
positive proof or automatic exemptions. Prompt activation remains a separate
decision after the measured candidate check.

Machine files: `candidate.json`, `manifest.yml`, and `draft-self-check.json` in this folder. The score is a same-author draft consistency check, not an independent prompt run or proof of recall across all documents.
