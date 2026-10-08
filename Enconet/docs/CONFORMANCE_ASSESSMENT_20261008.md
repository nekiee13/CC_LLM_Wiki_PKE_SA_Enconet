# Enconet — dokumentacijska procjena sukladnosti

## Rezultat: 80,6 % — substantially matched

**1.450 / 1.800 bodova**. Procijenjeno je svih **18 kriterija**.

- **6** potpuno usklađenih po dokumentaciji — fully.
- **10** u velikoj mjeri usklađenih — substantially.
- **2** djelomično usklađena — partially.
- Nema neocijenjenih kriterija, N/A ili izmišljene nule zbog neunesene ljudske ocjene.

Run: `RUN-20261008-17`. Procjenu je pripremio **Codex** iz vendor dokumenata.
To je pre-flight rezultat za usmjeravanje stvarnog audita, ne potvrda terenske
provedbe niti potvrda da nijedan nedostatak postoji u praksi.
**G3 odobrenje rezultata i brojčane kalibracije još je pending.** Rezultat nije
uskraćen: izračunan je prema postojećoj skali `0.1-placeholder`, bez promjene
brojeva. Scope je već odobren pod G2.

## Kako čitati ocjenu

Postojeća skala daje **100 / 75 / 50 / 25 / 0** bodova. Rangovi **5/5, 4/5,
3/5, 2/5, 1/5** označuju pet razina; nisu matematički razlomak za postotak.
Svaki primjenjivi kriterij ima jednaku težinu. Part21 ne ulazi u zbroj.

Fully ovdje znači da opisane kontrole funkcionalno pokrivaju relevantnu
svrhu kriterija u odobrenom opsegu, bez utvrđene materijalne dokumentarne
praznine. Ne znači da smo bili na radu i provjerili provedbu. Substantially
znači dobru kontrolu uz ograničen nerazriješen detalj. Partially znači da
ostaje važna praznina ili nedosljednost za taj kriterij.

Fuzzy pristup dopušta dokaz iste kontrolne svrhe drugim riječima ili kroz
više povezanih postupaka. Sam navod standarda, prazan obrazac ili velik broj
crumbs nije dovoljan. Otvoreno pitanje stvarne provedbe ne spušta automatski
ocjenu dokumentacijske adekvatnosti. Ne ocjenjuje se zavarivanje ili opća
logistika koju Enconet nije preuzeo.

## Pregled svih kriterija

| Kriterij | Ocjena | Rang | Bodovi |
|---|---|---:|---:|
| I | fully | 5/5 | 100 |
| II | substantially | 4/5 | 75 |
| III | substantially | 4/5 | 75 |
| IV | substantially | 4/5 | 75 |
| V | fully | 5/5 | 100 |
| VI | substantially | 4/5 | 75 |
| VII | substantially | 4/5 | 75 |
| VIII | fully | 5/5 | 100 |
| IX | partially | 3/5 | 50 |
| X | substantially | 4/5 | 75 |
| XI | fully | 5/5 | 100 |
| XII | substantially | 4/5 | 75 |
| XIII | substantially | 4/5 | 75 |
| XIV | substantially | 4/5 | 75 |
| XV | fully | 5/5 | 100 |
| XVI | fully | 5/5 | 100 |
| XVII | substantially | 4/5 | 75 |
| XVIII | partially | 3/5 | 50 |
| Ukupno | substantially | — | 1.450 / 1.800 |

## Glavna mjesta za stvarni audit

1. **IX — posebni procesi.** Nuclear QA Plan navodi vizualni QC/VT i
   kvalifikacije, dok generički priručnik izuzima IX. Treba povezati stvarni
   VT opseg s kontroliranom uputom, kvalifikacijom postupka i izvršitelja.
2. **XVIII — pokrivenost audita.** PP-82-01 ima godišnji audit, ali dopušta
   tri godine za punu kriterijsku pokrivenost. Dostavljeni NQA-1:2015
   Req18§201.3 za dobavljače traži godišnje ili opravdano produženje do dvije
   godine. Provjeriti stvarne matrice pokrivenosti prije zaključka o prošlom radu.
3. **IV/VII — nabava.** PP-74-01 je referenciran, ali nije zasebno dostavljen.
   Opsežne kontrole iz NQAP-a i priručnika su priznate; detaljan acceptance tok
   treba dovršiti uz narudžbu, supplier approval i relevantnu metodu prihvata.
4. **VI/XVII — važeći registar i pohrana.** GPD je označen canceled, ali
   drugi kontrolirani koraci i dalje ga traže. Pokazati aktivni registar,
   pravilnu retenciju i primjenjivu zaštitu/obnovu podataka.
5. **XIV — iznimka isporuke.** Razjasniti nuklearnu granicu hitne isporuke
   bez navedenih pregleda: poslovno odobrenje nije dokaz svakog safety waivera.

To su predloženi pravci provjere, ne već potvrđene terenske nesukladnosti.
Nisu samostalno odobreni findings ili završna auditorova zaključna mišljenja.

## Svaki kriterij: zašto ta ocjena

### I — Organization

**fully — 100 bodova**.

U prilog: Uloge, delegiranje, izravan put QA prema direktoru i pravo obustave rada čine povezanu kontrolu kvalitete; imenovanja i organizacijske veze postoje u dokumentima.

Ograničenje/protuargument: Današnja raspodjela uloga i neovisnost pod stvarnim pritiskom nisu terenski provjereni; to nije utvrđena dokumentacijska praznina u ovom ograničenom kriteriju.

Zaključak: Funkcionalna svrha organizacijskih kontrola pokrivena je kroz NQAP, imenovanja i stop-work postupak, ne samo citat propisa.

Provjera na auditu: Potvrditi važeće QA imenovanje i jedan primjer eskalacije ili obustave.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_I-0002`, `CRUMB-DOC-0001-APP_B_I-0011`, `CRUMB-DOC-0001-APP_B_I-0012`, `CRUMB-DOC-0001-APP_B_I-0013`, `CRUMB-DOC-0003-APP_B_I-0006`, `CRUMB-DOC-0003-APP_B_I-0044`, `CRUMB-DOC-0008-APP_B_I-0005`.

### II — Quality Assurance Program

**substantially — 75 bodova**.

U prilog: Program, kontrolirani uvjeti, godišnja ocjena uprave, obuka, promjene i uvođenje osoblja imaju konkretne postupke i odgovornosti.

Ograničenje/protuargument: Za sve inspekcijske/testne uloge treba razjasniti kvalifikacijske intervale i dostupnost preuzetih NEK programa; opći plan obuke nije cijela kvalifikacijska shema.

Zaključak: Sustav je dobro dokumentiran. Ograničeni kvalifikacijski detalji i veza na preuzete programe ostaju za dokaz, bez automatske kazne zbog praznih obrazaca.

Provjera na auditu: Uzorkovati jedan kvalifikacijski dosje QC/test osobe i zadnju upravinu godišnju ocjenu.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_II-0021`, `CRUMB-DOC-0001-APP_B_II-0025`, `CRUMB-DOC-0001-APP_B_II-0035`, `CRUMB-DOC-0006-APP_B_II-0013`, `CRUMB-DOC-0006-APP_B_II-0020`, `CRUMB-DOC-0006-APP_B_II-0021`, `CRUMB-DOC-0006-APP_B_II-0028`, `CRUMB-DOC-0006-APP_B_II-0031`.

### III — Design Control

**substantially — 75 bodova**.

U prilog: Kontrolirani ulazi, neovisni stručni pregled, promjene prije primjene, konfiguracijski baseline i V&V podupiru stvarne inženjerske usluge.

Ograničenje/protuargument: Za NQA-1:2015 softversku osnovu treba povezati zahtjeve zaštite od neovlaštene uporabe s projektnim/V&V zapisom; opći IT opis nije taj trag.

Zaključak: Projektni životni ciklus i provjera su jaki. Specifični suvremeni softverski zahtjevi trebaju jasniji dokaz; nije pretpostavljena safety-control ili dedication uloga.

Provjera na auditu: Uzorkovati jedan projekt/softverski baseline: ulaz, neovisni pregled, promjenu, acceptance test i zahtjeve zaštite.

Dokazni crumbs: `CRUMB-DOC-0008-APP_B_III-0022`, `CRUMB-DOC-0008-APP_B_III-0033`, `CRUMB-DOC-0008-APP_B_III-0034`, `CRUMB-DOC-0008-APP_B_III-0040`, `CRUMB-DOC-0008-APP_B_III-0043`, `CRUMB-DOC-0016-APP_B_III-0009`, `CRUMB-DOC-0017-APP_B_III-0003`, `CRUMB-DOC-0019-APP_B_III-0001`.

### IV — Procurement Document Control

**substantially — 75 bodova**.

U prilog: NQAP određuje tehničke/QA zahtjeve, revizije, kriterije prihvata, prijavu nesukladnosti, dokumentaciju i prijenos zahtjeva poddobavljačima.

Ograničenje/protuargument: Detaljni PP-74-01 nije zasebno dostavljen; potrebno je potvrditi kontrolu pregleda/odobrenja narudžbe prije ugovaranja prema stvarnom nabavnom toku.

Zaključak: Većina potrebnih sadržaja nabave je konkretna, a manjkava detaljna procesna podloga ograničuje dokaz potpune usklađenosti.

Provjera na auditu: Otvoriti jednu narudžbu za nuklearnu uslugu ili MTE s QA pregledom, revizijama i flow-downom.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_IV-0006`, `CRUMB-DOC-0001-APP_B_IV-0010`, `CRUMB-DOC-0001-APP_B_IV-0011`, `CRUMB-DOC-0001-APP_B_IV-0015`, `CRUMB-DOC-0001-APP_B_IV-0016`, `CRUMB-DOC-0003-APP_B_IV-0005`, `CRUMB-DOC-0002-APP_B_IV-0004`.

### V — Instructions, Procedures, and Drawings

**fully — 100 bodova**.

U prilog: Pisane upute određuju izvođenje, resurse, nadzor i kvantitativne/kvalitativne kriterije; tehnički testni postupci daju dubinu izvan same izjave politike.

Ograničenje/protuargument: Primjena točne revizije na radu treba se potvrditi uzorkom; ne traži se da svaki prazan predložak bude popunjen da bi postupak bio adekvatan.

Zaključak: Dokumentirana kontrola izvođenja i prihvata funkcionalno pokriva kriterij u odobrenoj uslužnoj djelatnosti.

Provjera na auditu: Na jednom zadatku usporediti odobrenu uputu, radni nalog i mjerila prihvata.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_V-0001`, `CRUMB-DOC-0001-APP_B_V-0002`, `CRUMB-DOC-0004-APP_B_V-0005`, `CRUMB-DOC-0008-APP_B_V-0001`.

### VI — Document Control

**substantially — 75 bodova**.

U prilog: Priprema, QA pregled, odobrenje, kontrolirana distribucija, povrat starih revizija i formalne promjene imaju definiran slijed.

Ograničenje/protuargument: GPD sekcija označena je obsolete/canceled, dok isti tok i noviji zapisni postupak i dalje zahtijevaju GPD; važeći način evidencije nije dovoljno jasan.

Zaključak: Osnovne kontrole su snažne, ali unutarnja nedosljednost registra zahtijeva razrješenje. Stara izdanja normi sama nisu automatska nesukladnost.

Provjera na auditu: Pokazati važeći master registar, jednu distribucijsku listu i povučenu prethodnu reviziju.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_VI-0016`, `CRUMB-DOC-0001-APP_B_VI-0021`, `CRUMB-DOC-0004-APP_B_VI-0019`, `CRUMB-DOC-0004-APP_B_VI-0026`, `CRUMB-DOC-0004-APP_B_VI-0046`, `CRUMB-DOC-0004-APP_B_VI-0049`, `CRUMB-DOC-0004-APP_B_VI-0055`, `CRUMB-DOC-0004-APP_B_VI-0067`, `CRUMB-DOC-0005-APP_B_VI-0006`.

### VII — Control of Purchased Material, Equipment, and Services

**substantially — 75 bodova**.

U prilog: Izbor dobavljača, odobrene liste, godišnje ocjene, nadzor outsourcinga i dokaz prihvata prije uporabe su propisani.

Ograničenje/protuargument: Bez PP-74-01 ne može se završiti pregled detaljnog nabavnog/acceptance toka. Specifične certificate/dedication puteve provjeravati samo ako se stvarno koriste.

Zaključak: Dokumentirana dobavljačka kontrola prelazi visoku politiku, ali dio provedbenog toka ostaje izvan dostavljenog seta.

Provjera na auditu: Zatražiti PP-74-01 i uzorkovati odobrenog podugovarača ili kalibracijski laboratorij i njegov prihvat.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_VII-0005`, `CRUMB-DOC-0001-APP_B_VII-0007`, `CRUMB-DOC-0001-APP_B_VII-0012`, `CRUMB-DOC-0003-APP_B_VII-0014`, `CRUMB-DOC-0003-APP_B_VII-0019`, `CRUMB-DOC-0008-APP_B_VII-0003`, `CRUMB-DOC-0025-APP_B_VII-0003`.

### VIII — Identification and Control of Materials, Parts, and Components

**fully — 100 bodova**.

U prilog: Identitet predmeta, oznake MTE, serijski brojevi, zabrana ponovne uporabe identifikatora, AOV tag provjera i softverske verzije daju konkretan trag.

Ograničenje/protuargument: Stvarna označenost i lanac zapisa provjeravaju se na radu; nije pretpostavljena proizvodnja niti potreba heat/lot praćenja kad je ugovor ne traži.

Zaključak: Identifikacija i sljedivost u ograničenom predmetnom opsegu su potpuno dokumentirane, kroz stvarne kontrolne korake.

Provjera na auditu: Povezati jedan instrument/AOV ili softverski paket s radnim nalogom, verzijom i zapisom rezultata.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_VIII-0002`, `CRUMB-DOC-0001-APP_B_VIII-0004`, `CRUMB-DOC-0016-APP_B_VIII-0002`, `CRUMB-DOC-0016-APP_B_VIII-0005`, `CRUMB-DOC-0020-APP_B_VIII-0004`, `CRUMB-DOC-0025-APP_B_VIII-0001`, `CRUMB-DOC-0025-APP_B_VIII-0005`.

### IX — Control of Special Processes

**partially — 50 bodova**.

U prilog: NQAP priznaje vizualni QC kao poseban proces; kvalifikacija VT II/CP-189 i zdravstveni uvjeti su navedeni.

Ograničenje/protuargument: Generički priručnik izuzima IX, dok nuklearni plan opisuje aktivni VT. Kontrolirana VT radna uputa i kvalifikacija primijenjenog postupka nisu prikazane u ovom setu.

Zaključak: Postoje važne kontrole, ali dokumentarna granica i specifičan procesni dokaz ostaju materijalno nedovoljni. Ne traži se dokaz zavarivanja koje nije preuzeto.

Provjera na auditu: Uzorkovati ugovorenu VT uputu, odgovornost za njezinu kvalifikaciju i aktualan VT/vidni dosje izvršitelja.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_IX-0001`, `CRUMB-DOC-0001-APP_B_IX-0003`, `CRUMB-DOC-0001-APP_B_IX-0004`, `CRUMB-DOC-0002-APP_B_IX-0001`, `CRUMB-DOC-0003-APP_B_IX-0004`, `CRUMB-DOC-0003-APP_B_IX-0006`.

### X — Inspection

**substantially — 75 bodova**.

U prilog: Neovisni pregled, pisani kriteriji, hold/witness točke i provjera prije nastavka rada jasno su propisani.

Ograničenje/protuargument: Za konkretne nuklearne preglede treba dovršiti kontroliranu projektnu/NEK podlogu, ovlasti izuzeća na hold pointu i granicu izravnog nadzora izvršitelja.

Zaključak: Inspekcijska kontrola je sadržajno dobro pokrivena; pojedine specifične ovlasti i detaljna podloga ostaju za potvrdu, ne kao dokaz da pregled ne postoji.

Provjera na auditu: Uzorkovati inspection plan, odobrenje hold-point odstupanja ako ga ima i neovisnost potpisanog inspektora.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_X-0003`, `CRUMB-DOC-0001-APP_B_X-0004`, `CRUMB-DOC-0001-APP_B_X-0006`, `CRUMB-DOC-0001-APP_B_X-0007`, `CRUMB-DOC-0003-APP_B_X-0006`, `CRUMB-DOC-0010-APP_B_X-0001`.

### XI — Test Control

**fully — 100 bodova**.

U prilog: V&V plan, testovi namjeravanih primjena, usporedba s referencama, in-use test nakon promjene okružja i detaljni AOV preduvjeti/kriteriji pokrivaju svrhu testa.

Ograničenje/protuargument: Nazivi/primjeri testnih deckova i nedostajući FDS prilozi traže provjeru aktualnog seta, ali ne brišu izričite zahtjeve za puni opseg, prihvat i dokumentiranje.

Zaključak: Kriterij je dokumentacijski potpuno pokriven za odobreni testni opseg; nije tvrdnja da su testovi stvarno prošli.

Provjera na auditu: Uzorkovati jedan RELAP5 acceptance/in-use test ili AOV As-Found/As-Left paket s kriterijima i odobrenjem.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_XI-0003`, `CRUMB-DOC-0017-APP_B_XI-0004`, `CRUMB-DOC-0018-APP_B_XI-0003`, `CRUMB-DOC-0019-APP_B_XI-0003`, `CRUMB-DOC-0019-APP_B_XI-0005`, `CRUMB-DOC-0019-APP_B_XI-0018`, `CRUMB-DOC-0019-APP_B_XI-0028`, `CRUMB-DOC-0020-APP_B_XI-0023`, `CRUMB-DOC-0020-APP_B_XI-0041`, `CRUMB-DOC-0020-APP_B_XI-0049`.

### XII — Control of Measuring and Test Equipment

**substantially — 75 bodova**.

U prilog: Raspon/točnost, intervali, oznake kalibracije, provjera prije testa, sljedivost i retrospektivna ocjena od zadnje kalibracije imaju konkretne kontrole.

Ograničenje/protuargument: Tehnički odnos referentne točnosti ili njegovo dopušteno opravdanje te praktični certifikacijski trag trebaju jasniju podlogu; razredi opreme nisu potpuno razrađeni.

Zaključak: Kontrola MTE je dobra, ali dio kalibracijske tehničke osnove nije dovoljno razvidan za puni rang.

Provjera na auditu: Na jednom certifikatu provjeriti etalon, točnost/opravdanje, as-found/as-left i pogođena ranija mjerenja.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_XII-0002`, `CRUMB-DOC-0001-APP_B_XII-0004`, `CRUMB-DOC-0001-APP_B_XII-0005`, `CRUMB-DOC-0020-APP_B_XII-0002`, `CRUMB-DOC-0025-APP_B_XII-0014`, `CRUMB-DOC-0025-APP_B_XII-0015`, `CRUMB-DOC-0025-APP_B_XII-0025`.

### XIII — Handling, Storage, and Shipping

**substantially — 75 bodova**.

U prilog: Uvjeti čuvanja MTE, proizvođačevi zahtjevi, zaštita opreme od kontaminacije i fizičke kopije medija podupiru odobreni ograničeni opseg.

Ograničenje/protuargument: Vendor izuzeća treba uskladiti s konkretnim preuzetim kontrolama. Detaljan transportni put vrijedi samo ako ga Enconet preuzima.

Zaključak: Zaštita i skladištenje su stvarno opisani. Ograničena primjenjivost nije opća logistika; papirna granica odgovornosti ostaje nedovoljno dosljedna.

Provjera na auditu: Provjeriti mjesto/uvjete čuvanja jednog instrumenta i medija te odgovornost ako se predmet prenosi.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_XIII-0001`, `CRUMB-DOC-0001-APP_B_XIII-0003`, `CRUMB-DOC-0020-APP_B_XIII-0001`, `CRUMB-DOC-0025-APP_B_XIII-0003`, `CRUMB-DOC-0025-APP_B_XIII-0005`, `CRUMB-DOC-0018-APP_B_XVII-0001`, `CRUMB-DOC-0018-APP_B_XVII-0007`.

### XIV — Inspection, Test, and Operating Status

**substantially — 75 bodova**.

U prilog: Statusne oznake, NIJE PREGLEDANO/NESUKLADNOST, test tag/clearance i završno oslobađanje sprečavaju preranu uporabu.

Ograničenje/protuargument: Opća mogućnost hitne isporuke bez provjera treba imati jasnu nuklearnu granicu; samo pisano poslovno odobrenje ne dokazuje dopuštenje za svaki safety-related slučaj.

Zaključak: Statusne kontrole su konkretne, ali iznimku isporuke treba uskladiti s potrebnim provjerama i ovlastima prije punog ranga.

Provjera na auditu: Uzorkovati release/test-tag i provjeriti da hitna isporuka ne omogućuje preranu safety-related uporabu.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_XIV-0002`, `CRUMB-DOC-0003-APP_B_XIV-0004`, `CRUMB-DOC-0004-APP_B_XIV-0002`, `CRUMB-DOC-0008-APP_B_XIV-0002`, `CRUMB-DOC-0010-APP_B_XIV-0001`, `CRUMB-DOC-0020-APP_B_XIV-0001`, `CRUMB-DOC-0020-APP_B_XIV-0002`.

### XV — Nonconforming Materials, Parts, or Components

**fully — 100 bodova**.

U prilog: NCR otvaranje, identifikacija/izolacija, stručna ocjena, dispozicija, potpis izvršenja, neovisna verifikacija i ponovno ispitivanje dorade tvore zatvoren tok.

Ograničenje/protuargument: Za uporabu kakav jest ili doradu treba provjeriti stvarno tehničko obrazloženje i primjenjiva kupčeva odobrenja; Part21 procjena nije automatska za svaki NCR.

Zaključak: Nesukladnost je kontrolirana od otkrića do odobrenog prihvata za Enconetove proizvode/usluge. Fizička plant-repair uloga nije pretpostavljena.

Provjera na auditu: Uzorkovati jedan NCR s dispozicijom, tehničkim razlogom, eventualnim customer consentom i provjerom dorade.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_XV-0003`, `CRUMB-DOC-0010-APP_B_XV-0015`, `CRUMB-DOC-0010-APP_B_XV-0023`, `CRUMB-DOC-0010-APP_B_XV-0025`, `CRUMB-DOC-0010-APP_B_XV-0026`, `CRUMB-DOC-0010-APP_B_XV-0027`, `CRUMB-DOC-0010-APP_B_XV-0028`, `CRUMB-DOC-0010-APP_B_XV-0029`, `CRUMB-DOC-0010-APP_B_XV-0030`, `CRUMB-DOC-0010-APP_B_X-0001`.

### XVI — Corrective Action

**fully — 100 bodova**.

U prilog: Uzrok, značaj, nositelj, rok, resursi, verifikacija završetka i razdoblje praćenja učinkovitosti imaju operativno definirane korake.

Ograničenje/protuargument: Stvarni rezultat sprječavanja ponavljanja treba potvrditi uzorkom. Part21 razlike u rokovima razmatraju se odvojeno od ovog rezultata.

Zaključak: Korektivni sustav dokumentacijski pokriva uzrok, provođenje i provjeru učinka, a ne samo brzo zatvaranje prijave.

Provjera na auditu: Uzorkovati značajnu radnju: uzrok, odobrenje, završetak i dokaz praćenja učinkovitosti.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_XVI-0002`, `CRUMB-DOC-0010-APP_B_XVI-0024`, `CRUMB-DOC-0011-APP_B_XVI-0010`, `CRUMB-DOC-0011-APP_B_XVI-0020`, `CRUMB-DOC-0011-APP_B_XVI-0021`, `CRUMB-DOC-0011-APP_B_XVI-0023`, `CRUMB-DOC-0011-APP_B_XVI-0031`, `CRUMB-DOC-0011-APP_B_XVI-0036`.

### XVII — Quality Assurance Records

**substantially — 75 bodova**.

U prilog: Autentifikacija, IOD, ZK klase, trajni projektni zapisi, ugovorni rokovi, zaštita pristupa i kopije imaju jasne kontrole.

Ograničenje/protuargument: GPD nedosljednost te za relevantnu odgovornost dokaz metode zaštite pohrane i obnove nakon katastrofe/promjene tehnologije ostaju otvoreni.

Zaključak: Zapisi su dobro uređeni. Lokalni backup nije sam po sebi dokaz svake potrebne storage metode; ne nameće se operatorova arhiva bez pripadne uloge.

Provjera na auditu: Uzorkovati jedan trajni projektni zapis i restore te potvrditi važeći registar, rok i storage odgovornost.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_XVII-0005`, `CRUMB-DOC-0005-APP_B_XVII-0007`, `CRUMB-DOC-0005-APP_B_XVII-0008`, `CRUMB-DOC-0005-APP_B_XVII-0010`, `CRUMB-DOC-0005-APP_B_XVII-0021`, `CRUMB-DOC-0005-APP_B_XVII-0026`, `CRUMB-DOC-0005-APP_B_XVII-0036`, `CRUMB-DOC-0013-APP_B_XVII-0024`, `CRUMB-DOC-0018-APP_B_XVII-0007`, `CRUMB-DOC-0018-APP_B_XVII-0015`.

### XVIII — Audits

**partially — 50 bodova**.

U prilog: Postupak ima neovisnost, autoritet, plan, pet audita/tri godine i nuklearno iskustvo za Lead Auditor-a te strukturirane izvještaje.

Ograničenje/protuargument: PP-82-01 traži punu kriterijsku pokrivenost u tri godine; supplied NQA-1:2015 Req18§201.3 za dobavljače traži godišnje ili izričito opravdano produženje najviše dvije godine. Ugovorna vanjska učestalost također traži dokaz.

Zaključak: Program audita postoji i detaljan je, ali pokrivenost/interval nije dovoljno usklađen s odabranom 2015 osnovom. Povijesni certifikati nisu proglašeni isteklima bez provjere.

Provjera na auditu: Pribaviti zadnje annual coverage matrice i obrazloženje produženja te aktualnu Lead Auditor requalifikaciju.

Dokazni crumbs: `CRUMB-DOC-0001-APP_B_XVIII-0005`, `CRUMB-DOC-0009-APP_B_XVIII-0009`, `CRUMB-DOC-0009-APP_B_XVIII-0010`, `CRUMB-DOC-0009-APP_B_XVIII-0018`, `CRUMB-DOC-0009-APP_B_XVIII-0021`, `CRUMB-DOC-0009-APP_B_XVIII-0026`, `CRUMB-DOC-0009-APP_B_XVIII-0042`, `CRUMB-DOC-0009-APP_B_XVIII-0058`.

## Veza crumbs → ocjena → izvor

Odabrano je **136 poveznica evaluation–vendor crumb** i **166 poveznica na
citate/poglavlja** u sidecar tragu. Nekoliko istih činjenica podupire različite
kontrolne svrhe, primjerice ponovno ispitivanje nakon dorade ili zaštitu medija.
Te veze su izričite; nisu dodatni bodovi po crumb-u. Primjenjivost i ocjene nisu
izračunani dijeljenjem broja prikupljenih crumbs.

Svi korišteni score-evidence IDs su aktivni DOCUMENT crumbs. RULE tekst
služi usporedbi zahtjeva, ne zamjenjuje vendor dokaz. Part21 je isključen iz
ocjena. Obrada ukupno ostaje 2.700 vendor crumbs; nije rađen novi sieve.

- [Kanonski paket iz baze](../out/2026-10-08/conformance-run17/enconet_appendix_b_evaluation_package.json).
- [Svi odabrani izvorni citati, quote IDs i chapter IDs](../out/2026-10-08/conformance-run17/evidence-trace.json).
- [Ulazni evaluation records](../out/2026-10-08/conformance-run17/records/).
- [Naredbe i dokazi validacije](../out/2026-10-08/conformance-run17/validation-evidence.json).
- [Odobreni G2 opseg](G2_APPLICABILITY_APPLIED_20261008.md).

U recordima su i postojeće dimenzije coverage/completeness/accuracy/clarity/
alignment. To su ordinalne procjene dokumentacije u rasponu 0–1, ne izmjerena
precizna klauzulska pokrivenost. Ne ulaze u novu skrivenu score formulu.

## Provjere i status

`validate_evaluation.py` je neovisno potvrdio svih 18 upisa i evidence gates.
Package schema i source projection prolaze. Neovisni izračun iz pohranjenih
bodova daje **80,6**, jednak kanonskom calculatoru. Scoring benchmark prolazi.
Izvorni citati su točno povezani sa svojim pohranjenim poglavljima.

Svi prijašnji redci 15 provjerenih DB tablica ostaju hash-exact. Dodani su
samo 18 evaluations i 136 evidence veza. Incoming je nepromijenjen, 36/36
hashes. Faza je još evidence_reviewed; G3–G7 nisu automatski odobreni.
Formalni report i dashboard nisu ovim zadatkom objavljeni kao konačno pušteni.

ASME2.7§201 ostaje fragment izvora, ne razlog da se dobavljač automatski
ocijeni nesukladnim. Starije vendor reference na NQA-1 traže provjeru
ugovornog izdanja; G1 odabrani 2015 target ne dokazuje automatski prošlu povredu.
Povijesni auditorski certifikati i prazni obrasci nisu proglašeni lažnima,
važećima ili isteklima bez provjere stvarnih zapisa.

## Sljedeća odluka

Vlasnik može pregledati **G3-RUN-20261008-17**: ove classifications i izračun,
te postojeće jednake težine i vrijednosti 100/75/50/25/0. G3 kalibracija se
ne glumi odobrenom. Ne tražimo da vlasnik osobno unosi 18 ocjena.
Claude dobiva jedan pregled cijele procjene; njegov review ostaje odgođen.
