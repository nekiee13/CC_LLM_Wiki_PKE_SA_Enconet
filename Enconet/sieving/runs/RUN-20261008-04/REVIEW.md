# RUN-20261008-04 — prikupljene RELAP5 mrvice

Izvor: RU-73-04,R2 PROCEDURE FOR THE RELAP5 TRANSIENT ANA.md, revizija 2.

227 živih dobavljačkih mrvica; 512 točnih citatnih poveznica na poglavlja.
Primjeri inputa i skripti nisu izvršeni testovi. Prazni worksheets nisu stvarni projektni zapisi.
Ovo je dokumentacijska potpora, ne konačna ocjena kriterija.

[Registrirani izvor](<../../../raw/RU-73-04,R2 PROCEDURE FOR THE RELAP5 TRANSIENT ANA.md>)

## 1. CRUMB-DOC-0019-APP_B_VI-0001

Kriterij: APP_B_VI — Document Control

objective_control: RU-73-04 identificirana je revizijom 2 i datumom objave.

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3]

Jezik: en

~~~~text
| Title:                | Radna uputa RU-73-04 |
~~~~

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3]

Jezik: en

~~~~text
| Revision No.:         | 2                    |
~~~~

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3]

Jezik: en

~~~~text
| Date Released:        | 17.11.2017.          |
~~~~

## 2. CRUMB-DOC-0019-APP_B_VI-0002

Kriterij: APP_B_VI — Document Control

supporting_control: Priprema, QA pregled i odobrenje imaju navedene osobe i datume.

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3]

Jezik: en

~~~~text
| Prepared:                                        | 13.11.2017. |
~~~~

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3]

Jezik: en

~~~~text
| mr.sc. Ilijana Iveković, Project Engineer        | Date        |
~~~~

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3]

Jezik: en

~~~~text
| Reviewed:                                        | 14.11.2017. |
~~~~

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3]

Jezik: en

~~~~text
| Vladimir Križe, dipl.ing., QA Leader             | Date        |
~~~~

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3]

Jezik: en

~~~~text
| Approved:                                        | 15.11.2017. |
~~~~

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3]

Jezik: en

~~~~text
| dr.sc. Nenad Debrecin, Project Manager, Director | Date        |
~~~~

## 3. CRUMB-DOC-0019-APP_B_VI-0003

Kriterij: APP_B_VI — Document Control

supporting_control: Prazna tablica predviđa periodični pregled.

Izvorno poglavlje: PROCEDURE FOR THE RELAP5 TRANSIENT ANALYSES [line 3] > Periodični pregled [line 23]

Jezik: hr

~~~~text
| Pregledao: | Datum: | Slijedeći pregled: |
~~~~

## 4. CRUMB-DOC-0019-APP_B_III-0001

Kriterij: APP_B_III — Design Control

supporting_control: Uputa obuhvaća accident/transient analize elektrana i pokusnih postrojenja različitim RELAP5 verzijama.

Izvorno poglavlje: Summary [line 35]

Jezik: en

~~~~text
This document presents the procedure developed to perform accident/transient analyses in nuclear power plants or experimental facilities using RELAP5 computer code family (RELAP5/mod3.2, RELAP5/mod3.3, RELAP5/SCDAPSIM).
~~~~

## 5. CRUMB-DOC-0019-APP_B_III-0002

Kriterij: APP_B_III — Design Control

objective_control: Sustavni pristup obuhvaća input modele, dokumentaciju i rezultate.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 1.1 Purpose [line 127]

Jezik: en

~~~~text
The purpose of the procedure is to provide systematic approach to the accident/transient analyses using RELAP5 computer code. It is also intended to describe necessary requirements for the preparation of the input models, documentation and output results. This procedure affects personnel involved in the development and maintenance of the RELAP5 input models and plant analysis using RELAP5 program.
~~~~

## 6. CRUMB-DOC-0019-APP_B_V-0001

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Uputa propisuje aktivnosti izvođenja RELAP5 analiza.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 1.2 Scope [line 131]

Jezik: en

~~~~text
This procedure gives the instructions for specific activities for performing accident / transient analysis using RELAP5 computer code.
~~~~

## 7. CRUMB-DOC-0019-APP_B_VI-0004

Kriterij: APP_B_VI — Document Control

supporting_control: Authentication definiran je kao provjera nepromijenjenog programa i pomoćnih datoteka.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
1. Authentication process - automatic verification process done by program itself
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
   which ensures that program and all auxiliary files have remained unchanged
   from the moment of creation.
~~~~

## 8. CRUMB-DOC-0019-APP_B_VIII-0001

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Svaka revizija base input decka ima vlastiti direktorij.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
2. Base deck directory - directory created for each base input deck revision.
~~~~

## 9. CRUMB-DOC-0019-APP_B_III-0003

Kriterij: APP_B_III — Design Control

supporting_control: Base deck uključuje volumene, junctions, toplinske strukture, kontrolne varijable, trips i tablice.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
3. Base input deck - input file for RELAP5 calculation of steady-state with all
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
   required data for the control volumes, junctions, heat structures, control
   variables, trips, control and material tables.
~~~~

## 10. CRUMB-DOC-0019-APP_B_III-0004

Kriterij: APP_B_III — Design Control

supporting_control: Rubni uvjeti predstavljaju dostupnost i funkcije sustava izvan eksplicitnog modela.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
6. Boundary conditions - assumptions used to represent plant systems not explicitly included in the mathematical model (availability and functionality of the plant systems).
~~~~

## 11. CRUMB-DOC-0019-APP_B_III-0005

Kriterij: APP_B_III — Design Control

supporting_control: Početni uvjeti određuju stanje elektrane prije tranzijenta.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
10. Initial conditions - reference values that define plant operating status before transient initiation.
~~~~

## 12. CRUMB-DOC-0019-APP_B_XVII-0001

Kriterij: APP_B_XVII — Quality Assurance Records

supporting_control: Notebook objedinjuje worksheets iz razvoja base input decka.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
16. RELAP5 notebook - compilation of worksheets created by nodalization developers during the preparation of base input deck.
~~~~

## 13. CRUMB-DOC-0019-APP_B_III-0006

Kriterij: APP_B_III — Design Control

supporting_control: Relevantni fenomeni povezuju razumijevanje tranzijenta s sigurnosnim marginama.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
17. Relevant phenomenological aspect - physical phenomena important for the
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
    understanding of the NPP transient and evaluation of the safety margins.
~~~~

## 14. CRUMB-DOC-0019-APP_B_II-0001

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Kvalifikacija korisnika definira izbor modela, diskretizacije i rubnih uvjeta uz dovoljnu točnost.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
25. User qualification - demonstration of persons ability to select suitable models,
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 2     ABBREVIATIONS AND DEFINITIONS [line 141]

Jezik: en

~~~~text
    discretization and boundary conditions for computer program, that is, to use
    computer program with sufficient accuracy and minimum possibility of
    misjudgment.
~~~~

## 15. CRUMB-DOC-0019-APP_B_I-0001

Kriterij: APP_B_I — Organization

objective_control: Nodalization developer priprema base input deck.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.1     Nodalization Developer
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
1. preparation of base input deck
~~~~

## 16. CRUMB-DOC-0019-APP_B_XVII-0002

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Developer izrađuje worksheets za notebook.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.1     Nodalization Developer
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
2. preparation of worksheets for RELAP5 notebook
~~~~

## 17. CRUMB-DOC-0019-APP_B_III-0007

Kriterij: APP_B_III — Design Control

objective_control: Developer održava manje revizije base decka.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.1     Nodalization Developer
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
3. maintenance (minor revisions) of the base input deck
~~~~

## 18. CRUMB-DOC-0019-APP_B_II-0002

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Developer treba poznavati fizikalne modele i smjernice RELAP5.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
**Qualifications:**
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
1. knowledge of the RELAP5 physical models and user guidelines
~~~~

## 19. CRUMB-DOC-0019-APP_B_II-0003

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Developer treba detaljno poznavati projektne dokumente i elektranu.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
**Qualifications:**
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
2. detailed knowledge of the plant design documents and plant itself
~~~~

## 20. CRUMB-DOC-0019-APP_B_II-0004

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Iskustvo s certificiranim benchmarkovima ili pokusima preporučuje se, nije bezuvjetna obveza.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
**Qualifications:**
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
3. experience with modeling of certified benchmarks or experiments on test facilities
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
   is recommended
~~~~

## 21. CRUMB-DOC-0019-APP_B_I-0002

Kriterij: APP_B_I — Organization

objective_control: Supervisor nadzire pripremu i održavanje modela.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.2     Nodalization Supervisor
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
1. supervision of the preparation and the maintenance (minor revisions) of the base
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
   input deck
~~~~

## 22. CRUMB-DOC-0019-APP_B_III-0008

Kriterij: APP_B_III — Design Control

objective_control: Supervisor odobrava notebook.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.2     Nodalization Supervisor
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
2. approval of RELAP5 notebook
~~~~

## 23. CRUMB-DOC-0019-APP_B_I-0003

Kriterij: APP_B_I — Organization

objective_control: Supervisor kreira i održava base restart.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.2     Nodalization Supervisor
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
3. creation and maintenance of base restart file
~~~~

## 24. CRUMB-DOC-0019-APP_B_III-0009

Kriterij: APP_B_III — Design Control

objective_control: Supervisor verificira primjenjivost base decka za konkretan tranzijent.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.2     Nodalization Supervisor
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
4. verification of the applicability of the base input deck to the specific transient
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
   analysis
~~~~

## 25. CRUMB-DOC-0019-APP_B_II-0005

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Supervisor prati međunarodno iskustvo korištenja programa.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.2     Nodalization Supervisor
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
5. coverage of the international experience in the use of the RELAP5 program
~~~~

## 26. CRUMB-DOC-0019-APP_B_II-0006

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Supervisor treba poznavati modele i opcije RELAP5.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
**Qualifications:**
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
1. knowledge of the physical models incorporated in the RELAP5 program and
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
   detailed knowledge on the modeling options in RELAP5
~~~~

## 27. CRUMB-DOC-0019-APP_B_II-0007

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Supervisor treba poznavati projektnu dokumentaciju i elektranu.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
**Qualifications:**
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
2. detailed knowledge of the plant design documents and plant itself
~~~~

## 28. CRUMB-DOC-0019-APP_B_II-0008

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Benchmark iskustvo supervisora preporučuje se.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
**Qualifications:**
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
3. experience with modeling of certified benchmarks or experiments on test facilities
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
   is recommended
~~~~

## 29. CRUMB-DOC-0019-APP_B_III-0010

Kriterij: APP_B_III — Design Control

objective_control: Analitičar određuje početne i rubne uvjete analize.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.3    RELAP Analyst
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
1. definition of boundary and initial conditions for specific transient analysis
~~~~

## 30. CRUMB-DOC-0019-APP_B_I-0004

Kriterij: APP_B_I — Organization

objective_control: Analitičar priprema run deck i pokreće proračun.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.3    RELAP Analyst
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
2. preparation of the run input deck and running of RELAP5 calculations
~~~~

## 31. CRUMB-DOC-0019-APP_B_III-0011

Kriterij: APP_B_III — Design Control

objective_control: Analitičar ocjenjuje izračunate tranzijente.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.3    RELAP Analyst
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
3. analysis of the RELAP5 runs of the plant transient
~~~~

## 32. CRUMB-DOC-0019-APP_B_XVII-0003

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Analitičar priprema tehnički izvještaj.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.3    RELAP Analyst
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
4. preparation of the analysis technical report
~~~~

## 33. CRUMB-DOC-0019-APP_B_II-0009

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Analitičar mora biti inženjer upoznat s programom.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
#### Qualifications
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
1. engineer familiar with the RELAP5 program
~~~~

## 34. CRUMB-DOC-0019-APP_B_II-0010

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Analitičar treba detaljno poznavati elektranu i njezinu projektnu dokumentaciju.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
#### Qualifications
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
2. detailed knowledge of the plant design documents and plant itself
~~~~

## 35. CRUMB-DOC-0019-APP_B_I-0005

Kriterij: APP_B_I — Organization

objective_control: Softverski inženjer instalira i održava RELAP5 i plot program.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.4    RELAP Software Engineer
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
1. installation and maintenance of RELAP5 and RELAP5 plot programs
~~~~

## 36. CRUMB-DOC-0019-APP_B_XI-0001

Kriterij: APP_B_XI — Test Control

objective_control: Softverski inženjer testira računarski i plot program.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.4    RELAP Software Engineer
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
2. testing of RELAP5 program and RELAP5 plot programs
~~~~

## 37. CRUMB-DOC-0019-APP_B_I-0006

Kriterij: APP_B_I — Organization

objective_control: Softverski inženjer izrađuje skriptu i mijenja softver.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
### 3.4    RELAP Software Engineer
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
3. preparation of RELAP5 script file
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
4. modifications of software
~~~~

## 38. CRUMB-DOC-0019-APP_B_II-0011

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Softverski inženjer treba poznavati strukturu programa.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
#### Qualifications:
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
1. knowledge of the RELAP5 program structure
~~~~

## 39. CRUMB-DOC-0019-APP_B_II-0012

Kriterij: APP_B_II — Quality Assurance Program

objective_control: Softverski inženjer treba poznavati FORTRAN, C/C++ i operativni sustav.

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
#### Qualifications:
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
2. knowledge of programming languages (FORTRAN and C/C++) and operating
~~~~

Izvorno poglavlje: 1 INTRODUCTION [line 125] > 3     RESPONSIBILITIES [line 246]

Jezik: en

~~~~text
   systems
~~~~

## 40. CRUMB-DOC-0019-APP_B_VIII-0002

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Direktorij kodne verzije ima definiranu oznaku koju dodjeljuje i evidentira Technical Project Leader.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.1.1.     RELAP5 program shall be installed by RELAP software engineer in following steps:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
1. RELAP5 root directory shall be created and named R5MnnnTT, where nnnTT is variable number of alpha-numerical characters reserved for the identification of the program program version. Number of places for nnn and TT is not restricted, but dedicated abbreviation is assigned and recorded by ENCONET Technical Project Leader. It is dependent on the code version used e.g. R5M33 is regular name for the RELAP5/mod33, R5M34scdapsim for RELAP5/SCDAPSIM for 3.4 version installation.
~~~~

## 41. CRUMB-DOC-0019-APP_B_VIII-0003

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Ime izvršnog programa mora biti usklađeno s označenom verzijom.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
2. RELAP5 program shall be placed in the RELAP5 root directory and named according to following conventions:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
   a. first 3 characters are fixed for RELAP5 - r5m,
   b. characters between position 3 and last 3 places before extension .exe are reserved for mod description that shall be consistent with name defined in paragraph 1 above (4.1.1.1-1),
   c. last 3 characters before extension are reserved for executable version description, e.g. r5m32p1a.exe is regular name of executable version of RELAP5/mod32 program.
~~~~

## 42. CRUMB-DOC-0019-APP_B_III-0012

Kriterij: APP_B_III — Design Control

objective_control: Tablica svojstava vode odabire se prema korištenoj verziji i formulaciji.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
3. RELAP5 steam tables shall be placed in the RELAP5 root directory and named tpfh2o if they are used with any RELAP5/mod3 based code with ASME-67 formulation or tpfh2onew for IAPSW-95 formulation
~~~~

## 43. CRUMB-DOC-0019-APP_B_V-0002

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Odgovarajuća skripta pohranjuje se u root direktorij verzije.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4. RELAP5 script program shall be placed in the RELAP5 root directory and named r5m3r.bat or r5sim.bat depending of the RELAP5 version.
~~~~

## 44. CRUMB-DOC-0019-APP_B_V-0003

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Root direktorij dodaje se u PATH prema uputi.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
5. RELAP5 root directory shall be written in PATH variable.
~~~~

## 45. CRUMB-DOC-0019-APP_B_VI-0005

Kriterij: APP_B_VI — Document Control

objective_control: Sve datoteke u root direktoriju zaštićene su od pisanja drugih korisnika.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
6. All files in RELAP5 root directory shall be write-protected for all other users.
~~~~

## 46. CRUMB-DOC-0019-APP_B_XI-0002

Kriterij: APP_B_XI — Test Control

objective_control: Za testiranje se kreira zaseban TEST direktorij.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
7. Subdirectory for the testing of RELAP5 program shall be created in RELAP5 root directory and named TEST.
~~~~

## 47. CRUMB-DOC-0019-APP_B_XVII-0004

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: TEST direktorij mora sadržavati rezultate propisanog testiranja.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
8. TEST directory shall contain results of RELAP5 testing according to Appendix 6.2.
~~~~

## 48. CRUMB-DOC-0019-APP_B_V-0004

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Radni poddirektoriji određuju se za RELAP5 analize.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
9. Work subdirectories shall be defined in the RELAP5 root directory for the RELAP5 analyses.
~~~~

## 49. CRUMB-DOC-0019-APP_B_VI-0006

Kriterij: APP_B_VI — Document Control

objective_control: Izvršna verzija je frozen i zaštićena authentication procesom.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.2. RELAP5 shall satisfy following requirements:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
1. Executable version shall be frozen and protected by authentication process.
~~~~

## 50. CRUMB-DOC-0019-APP_B_VIII-0004

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Svaki output i restart bilježi verziju, vrijeme, datum i veličinu izvršnog programa.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.2. RELAP5 shall satisfy following requirements:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
2. Source code version, time, date and size of executable version shall be written at the beginning of each RELAP5 created output and in the header of RELAP5 restart file.
~~~~

## 51. CRUMB-DOC-0019-APP_B_VIII-0005

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Svaki output i restart automatski uključuje base i run deck ID.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.2. RELAP5 shall satisfy following requirements:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
3. Base input deck and run input deck ID shall be automatically included in every RELAP5 created output and restart file.
~~~~

## 52. CRUMB-DOC-0019-APP_B_V-0005

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Priprema se skripta za izvođenje proračuna.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.3. RELAP5 script program to perform RELAP5 calculations shall be written.
~~~~

## 53. CRUMB-DOC-0019-APP_B_VI-0007

Kriterij: APP_B_VI — Document Control

objective_control: Skripta se čuva u root direktoriju.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.4. RELAP5 script program shall be stored in RELAP5 root directory.
~~~~

## 54. CRUMB-DOC-0019-APP_B_V-0006

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Skripta prima samo run i base input deck ID kao argumente.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.5. RELAP5 script program shall require as input arguments only run input deck ID and base input deck ID
~~~~

## 55. CRUMB-DOC-0019-APP_B_VIII-0006

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Input datoteke imaju propisani tip i.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.6. RELAP5 script program shall satisfy following conventions:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
1. Input files for RELAP5 program shall be file type i.
~~~~

## 56. CRUMB-DOC-0019-APP_B_VIII-0007

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Output ima isti ID kao input i tip o.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.6. RELAP5 script program shall satisfy following conventions:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
2. Output files of RELAP5 program shall have same name as input deck ID and file type o.
~~~~

## 57. CRUMB-DOC-0019-APP_B_VIII-0008

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Restart ima isti ID kao input i tip r.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.6. RELAP5 script program shall satisfy following conventions:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
3. Restart files of RELAP5 program shall have same name as input deck ID and file type r.
~~~~

## 58. CRUMB-DOC-0019-APP_B_XVII-0005

Kriterij: APP_B_XVII — Quality Assurance Records

supporting_control: Ostale datoteke brišu se nakon proračuna; treba razlikovati obvezne zadržane rezultate.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.6. RELAP5 script program shall satisfy following conventions:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4. All other files shall be deleted after the end of RELAP5 calculation.
~~~~

## 59. CRUMB-DOC-0019-APP_B_V-0007

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Uputa propisuje način pozivanja skripte s run i base ID.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
### 4.1.1.7. RELAP5 script program shall be invoked from operating system command line by input of command:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
r5m3r (r5sim) input_ ID ..\base_input_ID
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
where input _ID stands for run input deck ID and
base_input_ID stands for base input deck ID.
~~~~

## 60. CRUMB-DOC-0019-APP_B_VI-0008

Kriterij: APP_B_VI — Document Control

objective_control: Plot program čuva se u rootu i zaštićen je od pisanja.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.2.1.     RELAP5 plot program shall be installed in following steps:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
1. RELAP5 plot program shall be placed in the RELAP5 root directory.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
2. RELAP5 plot program shall be write-protected from other users.
~~~~

## 61. CRUMB-DOC-0019-APP_B_III-0013

Kriterij: APP_B_III — Design Control

objective_control: Plot izvršna verzija mora biti frozen i ne smije mijenjati proračunske rezultate.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
3. RELAP5 plot program shall satisfy following requirements:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
   a. Executable version shall be frozen and protected by authentication process.
   b. RELAP5 plot program shall not change nor modify the results of the RELAP5 calculations.
   c. All types of RELAP5 plot program generated outputs (screen graphics, plots, vector file formats, HPGL files and binary-plot file) shall contain:
~~~~

## 62. CRUMB-DOC-0019-APP_B_VIII-0009

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Plot izlazi identificiraju verziju RELAP5 koja ih je proizvela.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
3. RELAP5 plot program shall satisfy following requirements:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
   a. Executable version shall be frozen and protected by authentication process.
   b. RELAP5 plot program shall not change nor modify the results of the RELAP5 calculations.
   c. All types of RELAP5 plot program generated outputs (screen graphics, plots, vector file formats, HPGL files and binary-plot file) shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
      - version of RELAP5 program that generated plot records;
~~~~

## 63. CRUMB-DOC-0019-APP_B_XVII-0006

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Plot izlazi nose vrijeme i datum stvaranja zapisa.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
3. RELAP5 plot program shall satisfy following requirements:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
   a. Executable version shall be frozen and protected by authentication process.
   b. RELAP5 plot program shall not change nor modify the results of the RELAP5 calculations.
   c. All types of RELAP5 plot program generated outputs (screen graphics, plots, vector file formats, HPGL files and binary-plot file) shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
      - time and the date when plot records were generated by RELAP5 program;
~~~~

## 64. CRUMB-DOC-0019-APP_B_VIII-0010

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Plot izlazi nose run i base input deck ID.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
3. RELAP5 plot program shall satisfy following requirements:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
   a. Executable version shall be frozen and protected by authentication process.
   b. RELAP5 plot program shall not change nor modify the results of the RELAP5 calculations.
   c. All types of RELAP5 plot program generated outputs (screen graphics, plots, vector file formats, HPGL files and binary-plot file) shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
      - ID of the run input deck used to run RELAP5 program;
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
      - ID of the base input deck used to run RELAP5 program.
~~~~

## 65. CRUMB-DOC-0019-APP_B_XVII-0007

Kriterij: APP_B_XVII — Quality Assurance Records

supporting_control: Plot program podržava prikaz, hardcopy i standardni grafički format.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.2.2.     RELAP5 plot program shall be used for:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
1. the creation of graphs on computer screen
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
2. the creation of hardcopy of graphs
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
3. the creation of graph output in at least one standard picture file format (WMF, HPGL, postscript, PCX, TIFF, etc.)
~~~~

## 66. CRUMB-DOC-0019-APP_B_XVII-0008

Kriterij: APP_B_XVII — Quality Assurance Records

supporting_control: Plot program daje cjelokupnu plot datoteku i ASCII datoteke varijabli.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.2.2.     RELAP5 plot program shall be used for:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4. the generation of file with all plot data
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
5. the generation of ASCII file for each plot variable
~~~~

## 67. CRUMB-DOC-0019-APP_B_I-0007

Kriterij: APP_B_I — Organization

objective_control: Base deck izrađuju nodalization developeri.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.3.1.     Base input deck shall be created by nodalization developers.
~~~~

## 68. CRUMB-DOC-0019-APP_B_III-0014

Kriterij: APP_B_III — Design Control

objective_control: Base deck mora potpuno predstavljati odgovarajuću elektranu prema referentnoj metodologiji.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
##### 4.1.3.1.1. Base input deck shall be complete and prepared to represent model of respective NPP in compliance with Ref. [2].
~~~~

## 69. CRUMB-DOC-0019-APP_B_XVII-0009

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Razvoj se dokumentira u notebooku.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
##### 4.1.3.1.2. The development of base input deck shall be documented by RELAP5 nodalization notebook as specified in 4.3.1.
~~~~

## 70. CRUMB-DOC-0019-APP_B_III-0015

Kriterij: APP_B_III — Design Control

objective_control: Usklađenost sustava, setpointa i geometrije opisuje steady-state izvještaj.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
##### 4.1.3.1.3. Compliance of base input deck models to the NPPsystems, setpoints and geometrical zones shall be summarized in Steady-State Technical Report as specified in 4.3.2.
~~~~

## 71. CRUMB-DOC-0019-APP_B_VIII-0011

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Supervisor određuje ID koji razlikuje stanje elektrane i reviziju decka.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.3.1.4. Base input deck ID shall be defined by nodalization supervisor with maximum of 8 characters:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
1. characters 1 to 5 shall be used for the abbreviation of reference plant data, (e.g. P1n00 shall represent plant configuration for the version 00 of nominal condditions, P1h1a for version 1a of hot shutdown conditions, etc.)
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
2. characters 6 to 8 shall be used for numbering of base input deck revisions, (e.g. e0a may stand for 0 revision for end of life configuration and b0a for beginning of life)
~~~~

## 72. CRUMB-DOC-0019-APP_B_VIII-0012

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Base input ima propisani tip i.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.3.1.5. Base input deck shall be file type i.
~~~~

## 73. CRUMB-DOC-0019-APP_B_XVII-0010

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Base deck čuva se u radnoj mapi, uz kopije s notebookom, na dodatnom mediju i zaštićenoj web lokaciji.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.3.1.6. Base input deck shall be stored in work directory for each NPP modelled. Backup copies shall be stored on:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
1. a CD that shall be kept together with the master version of RELAP5 notebook
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
2. at least one other removable computer storage media.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
3. protected web site http://enconet.no-ip.biz/ifolder
~~~~

## 74. CRUMB-DOC-0019-APP_B_VI-0009

Kriterij: APP_B_VI — Document Control

objective_control: Supervisor štiti base deck od pisanja.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.3.1.7. Base input deck shall be write-protected by nodalization supervisor.
~~~~

## 75. CRUMB-DOC-0019-APP_B_V-0008

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Podaci i dodatne input konvencije slijede priručnik odgovarajuće kodne verzije.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.3.1.8. Base input deck data shall be in compliance with Ref. [1] depending on the code version used. Additional input conventions that shall be part of this procedure are reported in Appendix 6.4.
~~~~

## 76. CRUMB-DOC-0019-APP_B_III-0016

Kriterij: APP_B_III — Design Control

objective_control: Steady-state kvalifikacija traži dokumentiranu geometrijsku vjernost i sljedive ulaze.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.3.1.9. Base input deck shall be qualified on the steady-state level, that is:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
1. geometrical fidelity with the plant is achieved and well documented (verified by the base input deck notebook that ensures all the input data are traceable and close physical representation of the actual plant).
~~~~

## 77. CRUMB-DOC-0019-APP_B_III-0017

Kriterij: APP_B_III — Design Control

objective_control: Referentno steady-state stanje reproducira se unutar unaprijed definiranih granica.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
#### 4.1.3.1.9. Base input deck shall be qualified on the steady-state level, that is:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
2. referenced steady-state condition is satisfactory reproduced (that is, difference between calculation results and reference is within predefined limits as verified by Steady-State Technical Report).
~~~~

## 78. CRUMB-DOC-0019-APP_B_III-0018

Kriterij: APP_B_III — Design Control

objective_control: Base output nastaje proračunom odgovarajućeg base decka.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.2.1. Base output shall be created by calculation of RELAP5 with base input deck as input.
~~~~

## 79. CRUMB-DOC-0019-APP_B_XVII-0011

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Supervisor sprema base output kao read-only.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.2.2. Nodalization supervisor shall store base output in C1work directory as read-only file.
~~~~

## 80. CRUMB-DOC-0019-APP_B_VIII-0013

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Base output koristi ID base decka i tip o.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.2.3. By RELAP5 script file default base output shall have same file ID as base input deck.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.2.4. File type shall be file type o.
~~~~

## 81. CRUMB-DOC-0019-APP_B_III-0019

Kriterij: APP_B_III — Design Control

objective_control: Base output služi kvalifikaciji base decka.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.2.5. Base output is used for the steady-state qualification of base input deck.
~~~~

## 82. CRUMB-DOC-0019-APP_B_III-0020

Kriterij: APP_B_III — Design Control

objective_control: Base output kreira se za svaku verziju ili reviziju.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.2.6. Base output shall be created for each version or revision of base input deck
~~~~

## 83. CRUMB-DOC-0019-APP_B_III-0021

Kriterij: APP_B_III — Design Control

objective_control: Base restart nastaje iz proračuna base decka.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.3.1. Base restart shall be created by calculation of RELAP5 with base input deck as input.
~~~~

## 84. CRUMB-DOC-0019-APP_B_XVII-0012

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Supervisor sprema base restart kao read-only.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.3.2. Nodalization supervisor shall store base restart in work directory as read-only file.
~~~~

## 85. CRUMB-DOC-0019-APP_B_VIII-0014

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Base restart koristi ID base decka i tip r.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.3.3. By RELAP5 script file default base restart shall have same file ID as base input deck.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.3.4. File type shall be file type r.
~~~~

## 86. CRUMB-DOC-0019-APP_B_III-0022

Kriterij: APP_B_III — Design Control

objective_control: Tranzijent koristi base restart zajedno s run deckom.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.3.5. Base restart is used for the transient calculations together with run input deck as inputs to the script file.
~~~~

## 87. CRUMB-DOC-0019-APP_B_III-0023

Kriterij: APP_B_III — Design Control

objective_control: Base restart kreira se za svaku verziju ili reviziju.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.1    Installation and Setup [line 313]

Jezik: en

~~~~text
4.1.3.3.6. Base restart shall be created for each version or revision of base input deck.
~~~~

## 88. CRUMB-DOC-0019-APP_B_XVII-0013

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Analitičar dokumentira pripremu na worksheets.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.2.1.1. Transient analysis preparation shall be done by RELAP5 analyst and documented on RELAP5 analyst worksheets. RELAP5 analyst shall define transient analysis ID as 4 character word, possibly as abbreviation of transient name, e.g. CLSB for Cold Leg Small Break LOCA. Assigned abbreviation shall be approved by ENCONET Technical Project Leader.
~~~~

## 89. CRUMB-DOC-0019-APP_B_VIII-0015

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: ID tranzijenta dodjeljuje analitičar, a odobrava Technical Project Leader.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.2.1.1. Transient analysis preparation shall be done by RELAP5 analyst and documented on RELAP5 analyst worksheets. RELAP5 analyst shall define transient analysis ID as 4 character word, possibly as abbreviation of transient name, e.g. CLSB for Cold Leg Small Break LOCA. Assigned abbreviation shall be approved by ENCONET Technical Project Leader.
~~~~

## 90. CRUMB-DOC-0019-APP_B_III-0024

Kriterij: APP_B_III — Design Control

objective_control: Početni ulazi uključuju snagu, protoke, temperature, tlakove i razine prije tranzijenta.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.2.1.2. Initial and boundary conditions shall be defined according to the transient specifications:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. Initial conditions:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. reactor power
   b. primary system loop flow
   c. hot leg temperature and cold leg temperature (or average temperature)
   d. primary system pressure
   e. SG secondary side pressure
   f. SGs secondary side level
   g. PRZ level
   h. Steam flow to turbine
   i. FW flow
~~~~

## 91. CRUMB-DOC-0019-APP_B_III-0025

Kriterij: APP_B_III — Design Control

objective_control: Rubni ulazi određuju početak tranzijenta, relevantne i raspoložive sustave te setpointe.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.2.1.2. Initial and boundary conditions shall be defined according to the transient specifications:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. Boundary conditions:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. transient initiation
   b. identification of the relevant plant systems for the transient
   c. availability of the plant systems
   d. relevant protection and system actuation setpoints for the transient
~~~~

## 92. CRUMB-DOC-0019-APP_B_III-0026

Kriterij: APP_B_III — Design Control

objective_control: Glavni fenomeni identificiraju se literaturom i konzultacijom kvalificiranog korisnika.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
### 4.2.1.3. Definition of main phenomena and relevant phenomenological aspects of the transient:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. Main phenomena shall be identified:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. from available literature (FSAR, IAEA Technical Documents, OECD CSNI working reports, petc.).
   b. by expert consultation (qualified user of RELAP5 program)
~~~~

## 93. CRUMB-DOC-0019-APP_B_III-0027

Kriterij: APP_B_III — Design Control

objective_control: Relevantni termohidraulički aspekti određuju se za svaki glavni fenomen.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
### 4.2.1.3. Definition of main phenomena and relevant phenomenological aspects of the transient:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. Relevant thermohydraulic aspects shall be defined for main phenomena (e.g. if core dryout is identified as main phenomena than relevant thermohydraulic aspects may be rod surface temperature and core level).
~~~~

## 94. CRUMB-DOC-0019-APP_B_III-0028

Kriterij: APP_B_III — Design Control

objective_control: Primjenjivost modela provjerava se usporedbom početnih uvjeta s steady-state izvještajem.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
### 4.2.1.4. Base input deck applicability shall be verified by:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. Comparison of initial conditions as defined in 4.2.1.2-1 to the Steady-State Technical Report.
~~~~

## 95. CRUMB-DOC-0019-APP_B_III-0029

Kriterij: APP_B_III — Design Control

objective_control: Provjera primjenjivosti potvrđuje komponente relevantnih sustava i zaštitne setpointe.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
### 4.2.1.4. Base input deck applicability shall be verified by:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. Identification of RELAP5 components for each relevant plant system as defined in 4.2.1.2-2 in Steady-State Technical Report.
   b. Confirmation of relevant protection and system actuation setpoints as defined in 4.2.1.2-2 with Steady-State Technical Report.
   c. The results of steps 4.2.1.2 and 4.2.1.3 shall be submitted to the nodalization supervisor in format presented in Appendix 6.6.
   d. Nodalization supervisor shall verify base input deck applicability according to format presented in Appendix 6.6.
   e. RELAP5 analyst shall proceed with transient analysis only if base input deck is approved as applicable.
~~~~

## 96. CRUMB-DOC-0019-APP_B_III-0030

Kriterij: APP_B_III — Design Control

objective_control: Supervisor odobrava primjenjivost prije nastavka tranzijentne analize.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
### 4.2.1.4. Base input deck applicability shall be verified by:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. Identification of RELAP5 components for each relevant plant system as defined in 4.2.1.2-2 in Steady-State Technical Report.
   b. Confirmation of relevant protection and system actuation setpoints as defined in 4.2.1.2-2 with Steady-State Technical Report.
   c. The results of steps 4.2.1.2 and 4.2.1.3 shall be submitted to the nodalization supervisor in format presented in Appendix 6.6.
   d. Nodalization supervisor shall verify base input deck applicability according to format presented in Appendix 6.6.
   e. RELAP5 analyst shall proceed with transient analysis only if base input deck is approved as applicable.
~~~~

## 97. CRUMB-DOC-0019-APP_B_VIII-0016

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Radni direktorij tranzijenta koristi njegov ID.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. Transient working directory for transient analysis shall be defined as subdirectory of the work directory with the same name as transient analysis ID.
~~~~

## 98. CRUMB-DOC-0019-APP_B_VIII-0017

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Plot datoteka koristi ID tranzijenta, numerirani sufiks i tip PLT.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.2.2.1. Plot variables files shall be created in transient working directory.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. Plot variables file type shall be PLT.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. Plot variables file name shall be the same as transient ID with numbered sufix separated with - (minus sign), e.g. if transient analysis ID is CLSB, than plot variables files names may be CLSB-1, CLSB-2, etc. in ascending order.
~~~~

## 99. CRUMB-DOC-0019-APP_B_III-0031

Kriterij: APP_B_III — Design Control

objective_control: Glavne fenomenološke varijable posebno se izdvajaju i šalju Technical Project Leaderu na odobrenje.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. RELAP5 variables important for analysis of RELAP5 calculations
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   shall be identified using instructions from Ref. [1] (vol. 2, Appendix
   A, pg. 27) for input of minor edit requests:
   a.      RELAP5 variables that are representative for relevant
           thermohydraulic aspects shall be stored in plot variables files
           with suffix -1, e.g. file name will be CLSB-1.PLT. This file
           shall be submitted to ENCONET Technical Project Leader for
           approval.
   b.      Additional RELAP5 variables that may be used for analysis of
           RELAP5 calculations shall be stored in plot variables file with
           the suffixes following in ascending order, e.g. CLSB-2.PLT,
           CLSB-3.PLT etc.
4.2.2.2.     Run input deck shall be created in transient working directory for
             each RELAP5 run.
             − Run input deck shall be input file for restart of RELAP5 run as
                 specified in Ref. [1].
4.2.2.3.     Run input deck shall represent restart modification of base input
             file in compliance with Ref. [1] Vol 2.
~~~~

## 100. CRUMB-DOC-0019-APP_B_III-0032

Kriterij: APP_B_III — Design Control

objective_control: Za svaki run izrađuje se run deck kao propisana restart modifikacija base decka.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   shall be identified using instructions from Ref. [1] (vol. 2, Appendix
   A, pg. 27) for input of minor edit requests:
   a.      RELAP5 variables that are representative for relevant
           thermohydraulic aspects shall be stored in plot variables files
           with suffix -1, e.g. file name will be CLSB-1.PLT. This file
           shall be submitted to ENCONET Technical Project Leader for
           approval.
   b.      Additional RELAP5 variables that may be used for analysis of
           RELAP5 calculations shall be stored in plot variables file with
           the suffixes following in ascending order, e.g. CLSB-2.PLT,
           CLSB-3.PLT etc.
4.2.2.2.     Run input deck shall be created in transient working directory for
             each RELAP5 run.
             − Run input deck shall be input file for restart of RELAP5 run as
                 specified in Ref. [1].
4.2.2.3.     Run input deck shall represent restart modification of base input
             file in compliance with Ref. [1] Vol 2.
~~~~

## 101. CRUMB-DOC-0019-APP_B_XVII-0014

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Razvoj run decka dokumentira se analitičkim worksheets.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. The development of run input deck shall be documented by RELAP5
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   Analyst Worksheets.
~~~~

## 102. CRUMB-DOC-0019-APP_B_III-0033

Kriterij: APP_B_III — Design Control

objective_control: Usklađenost base i run modela sa specifikacijom sažima se u izvještaju.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. Compliance of run input deck and base input deck models to the
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   transient specifications shall be summarized in RELAP5 Analysis
   Technical Report as specified in 4.3.4.
~~~~

## 103. CRUMB-DOC-0019-APP_B_VIII-0018

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Run ID kodira tranzijent, lokaciju inicijatora i posebne izbore.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
3. Each run input deck ID shall be defined by RELAP5 analyst with
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   maximum of 8 characters:
   a.      characters 1 to 4 shall be the same as transient ID defined in
           4.2.1.1, e.g. if run input deck is prepared for transient analysis
           from example from 2, than ID CLSB shall be used.
   b.      character 5 shall be used for the location of transient initiator:
           − if the initiator is in loop with PRZ, than A shall be used
           − if the initiator is in loop without the PRZ, than B shall be
               used
           − if the initiator is common to both loops, than C shall be used
   c.      characters 6 to 8 shall be used to define specific choices:
           − size of the break
           − availability of the systems
           − RELAP5 input choices,
           − corrective actions according to 4.2.2.5-4, etc.
~~~~

## 104. CRUMB-DOC-0019-APP_B_VIII-0019

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Run input koristi tip i.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. Run input deck file type shall be file type i.
~~~~

## 105. CRUMB-DOC-0019-APP_B_XVII-0015

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Run deck čuva se u radnoj mapi uz odvojene kopije i workbook.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
5. Run input deck shall be stored in transient working directory. Backup copies shall be stored on:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. a diskette that is kept together with the RELAP5 analysis workbook
   b. at least one other removable computer storage media.
   c. protected web site http://enconet.no-ip.biz/ifolder
~~~~

## 106. CRUMB-DOC-0019-APP_B_III-0034

Kriterij: APP_B_III — Design Control

objective_control: Priprema run decka prilagođava parametre definiciji tranzijenta i rubnim uvjetima.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
6. Run input deck preparation shall include:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. introduction of the parameter changes in the base input deck that shall be altered to satisfy transient definition and required boundary conditions as identified in 4.2.1.4.
   b. identification and input (as minor edits) of RELAP transient characteristic variables that characterize main phenomenological aspects as identified in 4.2.2.1-4a.
   c. Run input deck data shall be in compliance with Ref. [1]. Additional input conventions that shall be part of this procedure are reported in Appendix 6.8
~~~~

## 107. CRUMB-DOC-0019-APP_B_V-0009

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Run podaci i dodatne konvencije slijede odgovarajući RELAP5 priručnik.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
6. Run input deck preparation shall include:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. introduction of the parameter changes in the base input deck that shall be altered to satisfy transient definition and required boundary conditions as identified in 4.2.1.4.
   b. identification and input (as minor edits) of RELAP transient characteristic variables that characterize main phenomenological aspects as identified in 4.2.2.1-4a.
   c. Run input deck data shall be in compliance with Ref. [1]. Additional input conventions that shall be part of this procedure are reported in Appendix 6.8
~~~~

## 108. CRUMB-DOC-0019-APP_B_V-0010

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Proračun se pokreće iz radnog direktorija propisanom skriptom.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. RELAP5 calculations shall be invoked from transient working directory by RELAP5 script file as specified in 4.1.1.7.
~~~~

## 109. CRUMB-DOC-0019-APP_B_III-0035

Kriterij: APP_B_III — Design Control

objective_control: Poznata greška rješava se izmjenom prema priručniku.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. RELAP5 calculations may result in:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. successful finish on trip 600 without errors in case which analyst shall proceed to 4.2.2.5;
   b. failure of the calculation with error reported in Vol. 2, ch. 8.3.4 of Ref. [1]. Changes as suggested from the manual shall be introduced;
   c. program fails in spite the suggestions from Ref. [1], or with unknown error, in case which input file shall be saved and problem reported to nodalization supervizor and RELAP5 software engineer. Analysis shall be continued only after nodalization supervizer provides the approval for the changes aimed to provide soultion in particular case.
~~~~

## 110. CRUMB-DOC-0019-APP_B_XVI-0001

Kriterij: APP_B_XVI — Corrective Action

objective_control: Kod nepoznate greške čuva se input, prijavljuje problem i nastavlja tek nakon supervisorova odobrenja.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. RELAP5 calculations may result in:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. successful finish on trip 600 without errors in case which analyst shall proceed to 4.2.2.5;
   b. failure of the calculation with error reported in Vol. 2, ch. 8.3.4 of Ref. [1]. Changes as suggested from the manual shall be introduced;
   c. program fails in spite the suggestions from Ref. [1], or with unknown error, in case which input file shall be saved and problem reported to nodalization supervizor and RELAP5 software engineer. Analysis shall be continued only after nodalization supervizer provides the approval for the changes aimed to provide soultion in particular case.
~~~~

## 111. CRUMB-DOC-0019-APP_B_III-0036

Kriterij: APP_B_III — Design Control

objective_control: Output analiza provjerava trips, karakteristične varijable, rubne uvjete i mass error.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. RELAP5 output analysis shall include:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. check of trip status
   b. characteristic variables analysis
   c. boundary conditions compliance
   d. check of mass error
~~~~

## 112. CRUMB-DOC-0019-APP_B_III-0037

Kriterij: APP_B_III — Design Control

objective_control: Grafička analiza uključuje relevantne grafove, plot podatke i vizualni pregled dodatnih varijabli.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. RELAP5 graphs analysis shall include:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. running of RELAP5 plot program with all plot variables file and run restart.
   b. creation of hard copies for representative variables graphs as defined in 4.2.2.1-4a.
   c. creation of plot data file for plot variable file defined in 4.2.2.1-4a.
   d. visual observation for the rest of plot variables files.
~~~~

## 113. CRUMB-DOC-0019-APP_B_V-0011

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Prihvat traži odgovarajući trip status, relativni mass error manji od 1% i objašnjenu termohidrauliku.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
3. The results of the analysis of RELAP5 calculation shall be considered satisfactory if:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. trip status is in accordance with 4.2.1.2-2
   b. relative mass error is less than 1%
   c. the prediction of relative thermohydraulic aspects is explained and justified
   d. If all off the above terms a, b and c are fulfilled, RELAP5 analyst shall proceed with step 6.
~~~~

## 114. CRUMB-DOC-0019-APP_B_XVI-0002

Kriterij: APP_B_XVI — Corrective Action

objective_control: Sumnjiv trip status traži prilagodbu trip postavki.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. The results of the analysis of RELAP5 calculation shall be considered doubtful if:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. Trip status is not in accordance with 4.2.1.2-2. Corrective action should be to adjust trips in run input deck according to 4.2.1.2-2.
   b. Relative mass error is greater than 1%. Corrective action is to decrease maximum time step size according to the specifications from Vol. 2, Appendix A, ch.3 of Ref. [1].
   c. The prediction of relative thermohydraulic aspects is not completely understood. Corrective action is to consult literature or qualified user - expert.
   d. One or some of the parameters show erratic behavior or unexplainable oscillations. Corrective actions should be performed in following order:
      i) to decrease maximum time step size;
      ii) to run parametric study for critical parameters;
      iii) to request renodalization or update of base input deck after consultation with qualified user.
      iv) Should none of the corrective actions lead to fulfillment of requests from 3 RELAP5 analyst should proceed to 5.
~~~~

## 115. CRUMB-DOC-0019-APP_B_XVI-0003

Kriterij: APP_B_XVI — Corrective Action

objective_control: Mass error veći od 1% traži smanjenje maksimalnog vremenskog koraka.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. The results of the analysis of RELAP5 calculation shall be considered doubtful if:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. Trip status is not in accordance with 4.2.1.2-2. Corrective action should be to adjust trips in run input deck according to 4.2.1.2-2.
   b. Relative mass error is greater than 1%. Corrective action is to decrease maximum time step size according to the specifications from Vol. 2, Appendix A, ch.3 of Ref. [1].
   c. The prediction of relative thermohydraulic aspects is not completely understood. Corrective action is to consult literature or qualified user - expert.
   d. One or some of the parameters show erratic behavior or unexplainable oscillations. Corrective actions should be performed in following order:
      i) to decrease maximum time step size;
      ii) to run parametric study for critical parameters;
      iii) to request renodalization or update of base input deck after consultation with qualified user.
      iv) Should none of the corrective actions lead to fulfillment of requests from 3 RELAP5 analyst should proceed to 5.
~~~~

## 116. CRUMB-DOC-0019-APP_B_XVI-0004

Kriterij: APP_B_XVI — Corrective Action

objective_control: Nejasan fizikalni rezultat traži literaturu ili kvalificiranog stručnjaka.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. The results of the analysis of RELAP5 calculation shall be considered doubtful if:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. Trip status is not in accordance with 4.2.1.2-2. Corrective action should be to adjust trips in run input deck according to 4.2.1.2-2.
   b. Relative mass error is greater than 1%. Corrective action is to decrease maximum time step size according to the specifications from Vol. 2, Appendix A, ch.3 of Ref. [1].
   c. The prediction of relative thermohydraulic aspects is not completely understood. Corrective action is to consult literature or qualified user - expert.
   d. One or some of the parameters show erratic behavior or unexplainable oscillations. Corrective actions should be performed in following order:
      i) to decrease maximum time step size;
      ii) to run parametric study for critical parameters;
      iii) to request renodalization or update of base input deck after consultation with qualified user.
      iv) Should none of the corrective actions lead to fulfillment of requests from 3 RELAP5 analyst should proceed to 5.
~~~~

## 117. CRUMB-DOC-0019-APP_B_III-0038

Kriterij: APP_B_III — Design Control

objective_control: Neobjašnjive oscilacije rješavaju se smanjenjem koraka, parametarskom studijom i prema potrebi renodalizacijom.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. The results of the analysis of RELAP5 calculation shall be considered doubtful if:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. Trip status is not in accordance with 4.2.1.2-2. Corrective action should be to adjust trips in run input deck according to 4.2.1.2-2.
   b. Relative mass error is greater than 1%. Corrective action is to decrease maximum time step size according to the specifications from Vol. 2, Appendix A, ch.3 of Ref. [1].
   c. The prediction of relative thermohydraulic aspects is not completely understood. Corrective action is to consult literature or qualified user - expert.
   d. One or some of the parameters show erratic behavior or unexplainable oscillations. Corrective actions should be performed in following order:
      i) to decrease maximum time step size;
      ii) to run parametric study for critical parameters;
      iii) to request renodalization or update of base input deck after consultation with qualified user.
      iv) Should none of the corrective actions lead to fulfillment of requests from 3 RELAP5 analyst should proceed to 5.
~~~~

## 118. CRUMB-DOC-0019-APP_B_XV-0001

Kriterij: APP_B_XV — Nonconforming Materials, Parts, or Components

supporting_control: Analiza je nezadovoljavajuća ako korekcije ne uspiju ili se izađe iz primjenjivosti matematičkog modela.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
5. The results of the analysis shall be considered unsatisfactory if:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   1.       none of the corrective actions succeeded.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   2.       some of the relevant thermohydraulic aspects is predicted
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
            outside the RELAP5 mathematical model applicability as
            described in Vol. 1 of Ref. [1].
~~~~

## 119. CRUMB-DOC-0019-APP_B_XVI-0005

Kriterij: APP_B_XVI — Corrective Action

objective_control: Nezadovoljavajuća analiza traži deviation izvještaj i ažuriranje poznatih ograničenja.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
5. The results of the analysis shall be considered unsatisfactory if:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   3.       should the analysis be considered unsatisfactory, RELAP5
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
            analyst shall proceed with 6. RELAP5 Analysis Technical
            Report – Deviation Report according to 4.3.4, should
            contain information of the problems encountered during the
            analysis. RELAP5 analyst shall initiate steady-state report
            update of know restrictions in the use of the program and
            base input deck.
~~~~

## 120. CRUMB-DOC-0019-APP_B_XVII-0016

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Svi run ulazi i izlazi čuvaju se uz zasebne kopije na izmjenjivom mediju.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
6. RELAP5 analyst shall store all run input and output files in the
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   transient working directory. Separate backup copies shall be stored on
   some removable computer storage media.
~~~~

## 121. CRUMB-DOC-0019-APP_B_XVII-0017

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Restart se smije brisati tek nakon stvaranja potrebne plot datoteke.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
7. RELAP5 analyst shall be allowed to delete run restart file after the
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   plot data file with variables specified in 4.2.2.1-4 are created.
~~~~

## 122. CRUMB-DOC-0019-APP_B_XVII-0018

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Završni paket uključuje workbook, kopije ulaza, outputa i plot podataka te tehnički izvještaj.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
8. Final output forms of the RELAP5 transient analysis shall be
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   prepared:
   a.     RELAP5 Workbook as specified in 4.3.3.
   b.     backup copies of all transient run input decks, run outputs and
          plot data files specified in 4.2.2.1-4 a on some removable
          computer storage media.
   c.     RELAP5 Analysis Technical Report as specified in 4.3.4.
~~~~

## 123. CRUMB-DOC-0019-APP_B_VIII-0020

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Notebook bilježi ime, datum, vrijeme i veličinu najnovijih base datoteka.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   4.3.1.1.   RELAP5 Nodalization Notebook is document compiled from worksheets
              created by nodalization developers that were used for calculation of
              RELAP5 base input deck. RELAP5 notebook worksheet is presented in
              Appendix 6.10.
   4.3.1.2.   RELAP5 notebook shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
              1.   name, time, date and size of the latest revision of the base input deck
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
                   file and base restart;
~~~~

## 124. CRUMB-DOC-0019-APP_B_XVII-0019

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Notebook sadrži medij s base inputom i steady-state outputom.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   4.3.1.1.   RELAP5 Nodalization Notebook is document compiled from worksheets
              created by nodalization developers that were used for calculation of
              RELAP5 base input deck. RELAP5 notebook worksheet is presented in
              Appendix 6.10.
   4.3.1.2.   RELAP5 notebook shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
              2.   disc with the base input deck file and corresponding output file of
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
                   the steady-state run;
~~~~

## 125. CRUMB-DOC-0019-APP_B_III-0039

Kriterij: APP_B_III — Design Control

objective_control: Notebook sadrži shematski crtež nodalizacije.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   4.3.1.1.   RELAP5 Nodalization Notebook is document compiled from worksheets
              created by nodalization developers that were used for calculation of
              RELAP5 base input deck. RELAP5 notebook worksheet is presented in
              Appendix 6.10.
   4.3.1.2.   RELAP5 notebook shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
              3.   schematic drawing of the nodalization;
~~~~

## 126. CRUMB-DOC-0019-APP_B_III-0040

Kriterij: APP_B_III — Design Control

objective_control: Notebook navodi kratice, formule i faktore pretvorbe.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   4.3.1.1.   RELAP5 Nodalization Notebook is document compiled from worksheets
              created by nodalization developers that were used for calculation of
              RELAP5 base input deck. RELAP5 notebook worksheet is presented in
              Appendix 6.10.
   4.3.1.2.   RELAP5 notebook shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. list of used abbreviations;
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
5. list of commonly used formulas and conversion factors;
~~~~

## 127. CRUMB-DOC-0019-APP_B_III-0041

Kriterij: APP_B_III — Design Control

objective_control: Worksheets opisuju input postavke i korištene reference.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   4.3.1.1.   RELAP5 Nodalization Notebook is document compiled from worksheets
              created by nodalization developers that were used for calculation of
              RELAP5 base input deck. RELAP5 notebook worksheet is presented in
              Appendix 6.10.
   4.3.1.2.   RELAP5 notebook shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
6. worksheets that describe setup of the input deck with used
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   references;
~~~~

## 128. CRUMB-DOC-0019-APP_B_III-0042

Kriterij: APP_B_III — Design Control

objective_control: Svaki worksheet mora biti neovisno pregledan.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.1.3. Each worksheet shall be independently reviewed.
~~~~

## 129. CRUMB-DOC-0019-APP_B_VI-0010

Kriterij: APP_B_VI — Document Control

objective_control: Svaka verzija notebooka obrađuje se kao nova revizija odobrenog tehničkog izvještaja.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.1.4. Final release of each version of RELAP5 Nodalization Notebook shall be
         processed as a new revision of Technical Report and approved.
~~~~

## 130. CRUMB-DOC-0019-APP_B_III-0043

Kriterij: APP_B_III — Design Control

objective_control: Steady-state izvještaj opisuje kvalifikaciju base modela.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.2.1. Steady-State Technical Report shall describe steady-state qualification of
         base input deck.
~~~~

## 131. CRUMB-DOC-0019-APP_B_III-0044

Kriterij: APP_B_III — Design Control

objective_control: Steady-state izvještaj navodi pretpostavke i smjernice nodalizacije.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.2.2. Steady-State Technical Report shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. main assumptions and guidelines used during the development of
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   the nodalization;
~~~~

## 132. CRUMB-DOC-0019-APP_B_III-0045

Kriterij: APP_B_III — Design Control

objective_control: Izvještaj navodi referentne početne i rubne uvjete.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.2.2. Steady-State Technical Report shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. choice of the referenced initial and boundary conditions;
~~~~

## 133. CRUMB-DOC-0019-APP_B_III-0046

Kriterij: APP_B_III — Design Control

objective_control: Izvještaj povezuje geometrijske zone elektrane s kontrolnim volumenima.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.2.2. Steady-State Technical Report shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
3. geometrical correspondence between plant zones and control
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   volumes;
~~~~

## 134. CRUMB-DOC-0019-APP_B_III-0047

Kriterij: APP_B_III — Design Control

objective_control: Izvještaj navodi setpointe modeliranih sustava.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.2.2. Steady-State Technical Report shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. modeled plant systems setpoints;
~~~~

## 135. CRUMB-DOC-0019-APP_B_III-0048

Kriterij: APP_B_III — Design Control

objective_control: Izvještaj navodi poznata ograničenja programa i modela.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.2.2. Steady-State Technical Report shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
5. known restrictions in the use of the RELAP5 program and base
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   input deck model;
~~~~

## 136. CRUMB-DOC-0019-APP_B_III-0049

Kriterij: APP_B_III — Design Control

objective_control: Izvještaj uspoređuje steady-state rezultate s referentnim podacima.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.2.2. Steady-State Technical Report shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
6. results of the steady state calculation and comparison with reference
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   data;
~~~~

## 137. CRUMB-DOC-0019-APP_B_XVII-0020

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Izvještaj sadrži ispis base input decka.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.2.2. Steady-State Technical Report shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
7. printout of the base input deck.
~~~~

## 138. CRUMB-DOC-0019-APP_B_XVII-0021

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Workbook objedinjuje worksheets nastale tijekom tranzijenta.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.3.1. RELAP5 Analysis Workbook shall be compilation of RELAP5 analyst
         worksheets that were created during the transient analysis. RELAP5
         analyst worksheet format is presented in Appendix 6.11.
~~~~

## 139. CRUMB-DOC-0019-APP_B_III-0050

Kriterij: APP_B_III — Design Control

objective_control: Workbook čuva specifikaciju, uvjete i glavne fenomenološke aspekte.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.3.2. RELAP5 Analysis Workbook shall contain RELAP5 analyst worksheets
         with notes of the activities described in 4.2:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. notes on the transient specifications;
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. definition of boundary and initial conditions;
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
3. identification of main phenomenological aspects;
~~~~

## 140. CRUMB-DOC-0019-APP_B_III-0051

Kriterij: APP_B_III — Design Control

objective_control: Workbook bilježi odobrenje primjenjivosti.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.3.2. RELAP5 Analysis Workbook shall contain RELAP5 analyst worksheets
         with notes of the activities described in 4.2:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. approval of base input deck applicability;
~~~~

## 141. CRUMB-DOC-0019-APP_B_XVII-0022

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Workbook bilježi run ulaze i plot varijable.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.3.2. RELAP5 Analysis Workbook shall contain RELAP5 analyst worksheets
         with notes of the activities described in 4.2:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
5. description of inputs for run input decks and plot variables file;
~~~~

## 142. CRUMB-DOC-0019-APP_B_III-0052

Kriterij: APP_B_III — Design Control

objective_control: Workbook sadrži grafove svakog runa, razloge promjena i bilješke analize.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4.3.3.2. RELAP5 Analysis Workbook shall contain RELAP5 analyst worksheets
         with notes of the activities described in 4.2:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
6. graphs of main plot variables for each run;
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
7. explanations for introduced changes;
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
8. notes of the graphs analysis.
~~~~

## 143. CRUMB-DOC-0019-APP_B_VI-0011

Kriterij: APP_B_VI — Document Control

objective_control: Završni izvještaj slijedi Enconetovu proceduru tehničkog izvještavanja.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.3.4.2. RELAP5 Analysis Technical Report shall comply with the ENCONET Technical Report procedure.
~~~~

## 144. CRUMB-DOC-0019-APP_B_III-0053

Kriterij: APP_B_III — Design Control

objective_control: Završni izvještaj potvrđuje uvjete i supervisorovo odobrenje modela.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.3.4.3. RELAP5 technical report shall be prepared based on RELAP Analysis Workbook as it is defined in 4.3.3 and other relevant reference and shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
1. initial and boundary conditions compliance, as prepared for run input deck;
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
2. compliance of base input deck according to this specification (as approved by nodalization supervisor);
~~~~

## 145. CRUMB-DOC-0019-APP_B_III-0054

Kriterij: APP_B_III — Design Control

objective_control: Izvještaj navodi glavne fenomene i promjene koje utječu na pretpostavke.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.3.4.3. RELAP5 technical report shall be prepared based on RELAP Analysis Workbook as it is defined in 4.3.3 and other relevant reference and shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
3. main phenomenological aspects of the transient shall be stated;
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. changes that affect base input deck assumptions shall be summarized;
~~~~

## 146. CRUMB-DOC-0019-APP_B_III-0055

Kriterij: APP_B_III — Design Control

objective_control: Postojeća parametarska studija mora biti ocijenjena u izvještaju.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.3.4.3. RELAP5 technical report shall be prepared based on RELAP Analysis Workbook as it is defined in 4.3.3 and other relevant reference and shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
5. evaluation of parametric study, if such exists;
~~~~

## 147. CRUMB-DOC-0019-APP_B_III-0056

Kriterij: APP_B_III — Design Control

objective_control: Izvještaj navodi zaključke i ishode analize.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.3.4.3. RELAP5 technical report shall be prepared based on RELAP Analysis Workbook as it is defined in 4.3.3 and other relevant reference and shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
6. conclusions on the analysis (including outcomes as defined in 5);
~~~~

## 148. CRUMB-DOC-0019-APP_B_XVII-0023

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Glavni i parametarski grafovi dio su izvještaja.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
#### 4.3.4.3. RELAP5 technical report shall be prepared based on RELAP Analysis Workbook as it is defined in 4.3.3 and other relevant reference and shall contain:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
7. graphs of relevant parameters for base case calculation;
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
8. graphs relevant for parametric study as separate attachment.
~~~~

## 149. CRUMB-DOC-0019-APP_B_III-0057

Kriterij: APP_B_III — Design Control

candidate_lead: Reference upućuju na kodni priručnik, kvalifikacijsku metodologiju i QA dokumente; objective evidence not shown u samom popisu.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 5     REFERENCES [line 777]

Jezik: en

~~~~text
[1] RELAP5/MOD3.2 Code Manual, Nuclear Safety Analysis Division, INEL,
     Prepared for US NRC, NUREG/CR-5535.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 5     REFERENCES [line 777]

Jezik: en

~~~~text
[2] A methodology for the qualification of thermalhydraulic code nodalizations,
     Bonuccelli M., F. D'Auria, N. Debrecin, G.M. Galassi, Proc. of NURETH-6
     Conference, Grenoble (F), October 5-8, 1993.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 5     REFERENCES [line 777]

Jezik: hr

~~~~text
[3] ENCONET Nuklearni QA Plan, NP-SUK-001
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 5     REFERENCES [line 777]

Jezik: hr

~~~~text
[4] ENCONET, PRIRUČNIK KVALITETE NORMA - ISO 9001:2015, PK-SUK-
     001
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 5     REFERENCES [line 777]

Jezik: en

~~~~text
[5] HRN EN ISO 9001:2015
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 5     REFERENCES [line 777]

Jezik: en

~~~~text
[6] IAEA Leadership and Management for Safety, IAEA Safety Standards Series, No.
     GSR Part 2, IAEA Vienna, 2016.
~~~~

## 150. CRUMB-DOC-0019-APP_B_XI-0003

Kriterij: APP_B_XI — Test Control

objective_control: Softverski inženjer testira RELAP5 za sve namijenjene primjene.

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
6.2.1.    RELAP5 computer program shall be tested for all intended applications by
          RELAP5 software engineer.
~~~~

## 151. CRUMB-DOC-0019-APP_B_XI-0004

Kriterij: APP_B_XI — Test Control

objective_control: Opseg može uključiti distribucijske verifikacijske testove s ulazima i referentnim rezultatima.

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
6.2.2.    The extent of testing may include:
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
          1.   Verification tests were performed by program developer, to demonstrate
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
               the capability of a computer program to produce valid results using 5
               characteristic test input decks. These inputs decks cover almost all aspects
               of code usage and running options (new, restart, strip, steady state
               initialization) and they are, together with corresponding outputs, part of
               official package distribution.
~~~~

## 152. CRUMB-DOC-0019-APP_B_XI-0005

Kriterij: APP_B_XI — Test Control

objective_control: In-use testovi provjeravaju prihvatljivo ponašanje na drugom računalu ili nakon bitne promjene hardvera ili potpornog softvera.

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
6.2.2.    The extent of testing may include:
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
          2.   In-use tests, covered by this procedure, should be performed by RELAP5
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
               software engineer to confirm acceptable performance of RELAP5 program
               in the operating system and should be used when RELAP5 program is
               installed on different computers, or when significant hardware or
               supporting software changes are made. Same input decks should be used as
               for verification tests from 6.2.2-1.
~~~~

## 153. CRUMB-DOC-0019-APP_B_XI-0006

Kriterij: APP_B_XI — Test Control

supporting_control: Primjer ans79 pokriva kinetiku i decay heat; nije zapis izvršenog testa.

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
ans79.i
```
= Long term decay heat study
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
*                             Configuration Control Problem
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
*   Input contains minimum hydrodynamics to allow testing of reactor
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
*   kinetics and decay heat calculation for long time periods.
~~~~

## 154. CRUMB-DOC-0019-APP_B_XI-0007

Kriterij: APP_B_XI — Test Control

supporting_control: Primjer edhtrk uključuje blowdown, toplinske i kontrolne modele te usporedbu s pokusnim podacima.

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
edhtrk.i
```
=edward's pipe problem base case with extras
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
*   Pipe Blowdown plus heat structures coupled to the pipe, a heat
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
*   structure with a simple analytic solution, control components with
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
*   analytic solutions, reactor kinetics, and a few trips.   This
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
*   artificial problem is used to check the coding of several models.
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
*   The results of this problem still match the Edward"s Pipe data
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
*   reasonably well.
~~~~

## 155. CRUMB-DOC-0019-APP_B_XI-0008

Kriterij: APP_B_XI — Test Control

supporting_control: Primjer edrst traži jednake simulacijske rezultate nakon restart proračuna.

Izvorno poglavlje: Appendix [line 867] > edrst.i [line 923]

Jezik: en

~~~~text
## edrst.i
~~~~

Izvorno poglavlje: Appendix [line 867] > edrst.i [line 923]

Jezik: en

~~~~text
* problem does an input check only with extensive optional printout.
~~~~

Izvorno poglavlje: Appendix [line 867] > edrst.i [line 923]

Jezik: en

~~~~text
* The edhtrk problem runs to 0.5 s and writes a restart tape.
~~~~

Izvorno poglavlje: Appendix [line 867] > edrst.i [line 923]

Jezik: en

~~~~text
* This problem restarts that problem at 0.2 s and runs to 0.5 s.
~~~~

Izvorno poglavlje: Appendix [line 867] > edrst.i [line 923]

Jezik: en

~~~~text
* Problem results at the end of this and the edhtrk problem should
~~~~

Izvorno poglavlje: Appendix [line 867] > edrst.i [line 923]

Jezik: en

~~~~text
* have identical simulation results.
~~~~

## 156. CRUMB-DOC-0019-APP_B_XI-0009

Kriterij: APP_B_XI — Test Control

supporting_control: Primjer edhtrkn mijenja način numeričkog napredovanja za usporedbu.

Izvorno poglavlje: Appendix [line 867] > edhtrkn.i [line 932]

Jezik: en

~~~~text
## edhtrkn.i
~~~~

Izvorno poglavlje: Appendix [line 867] > edhtrkn.i [line 932]

Jezik: en

~~~~text
=edward's pipe problem base case with extras
~~~~

Izvorno poglavlje: Appendix [line 867] > edhtrkn.i [line 932]

Jezik: en

~~~~text
* This problem is the same as edhtrk except that nearly implicit
~~~~

Izvorno poglavlje: Appendix [line 867] > edhtrkn.i [line 932]

Jezik: en

~~~~text
* advancement is used instead of semi-implicit advancement.
~~~~

## 157. CRUMB-DOC-0019-APP_B_XI-0010

Kriterij: APP_B_XI — Test Control

supporting_control: Primjer pump2 provjerava dva modela pumpe, pokretanje i trip.

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
## pump2.i
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
=Two loops with pumps
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
* This problem has two mostly identical loops, each with friction,
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
* an orifice, and a pump. Builtin pump data are used. The first loop
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
* uses an implied motor. The second loop uses pump motor torque data
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
* to represent an induction motor. The pump is initially at rest.
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
* The pump accelerates to near synchronous speed and fluid is
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
* accelerated, reaching near steady state. The pump is then tripped,
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
* resulting in decreasing pump speed and fluid velocities. The second
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
* problem is identicdal to the first except that shaft and generator
~~~~

Izvorno poglavlje: Appendix [line 867] > pump2.i [line 940]

Jezik: en

~~~~text
* (acting as motor) components are used.
~~~~

## 158. CRUMB-DOC-0019-APP_B_XI-0011

Kriterij: APP_B_XI — Test Control

supporting_control: Primjer marpzd4 pokriva plinski pressurizer i promjenu granica stanja vode.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
## marpzd4.i
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
= EHWR-NPR Pressurizer Model
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
* Simulates behavior of gas driven pressurizer. Using boundary
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
* conditions, a forced small compression is followed by a large
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
* expansion. Pressurizer component is not being used. Gas conditions
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
* drop below the triple point of water.
~~~~

## 159. CRUMB-DOC-0019-APP_B_XI-0012

Kriterij: APP_B_XI — Test Control

supporting_control: Primjer typpwr pokriva PWR small break, ali izričito ne slijedi sve preporučene prakse modeliranja.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
typpwr.i
```
=typical pwr model -- 4 inch cold leg break 36.05 check case
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
*            This problem is a simulation of a four loop presurized reactor
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
*    undergoing a small break.   Loop containing break is modeled as a
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
*    single loop but the other three loops are coalesced into one loop.
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
*    Modeling does not now follow all recommended modeling practices but
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
*    problem is still good test of many features of code.   Problem uses
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
*    standard matrix techniques.
~~~~

## 160. CRUMB-DOC-0019-APP_B_XI-0013

Kriterij: APP_B_XI — Test Control

objective_control: Uz distribucijske testove zahtijeva se OECD/CSNI ISP26 LSTF benchmark.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.4.     In addition to original distribution tests, RELAP5 program shall be tested using
           OECD/CSNI ISP26 benchmark input deck for LSTF experimental facility. This
           input deck can be used for verification testing as well as for in-use testing
           (reference data were produced with developers exe version for the Windows
           environment for mod3).
~~~~

## 161. CRUMB-DOC-0019-APP_B_XI-0014

Kriterij: APP_B_XI — Test Control

objective_control: Kriterij testa može se temeljiti na ručnom proračunu.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.5.     The acceptance criteria of the conducted testing may be based on:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
           1.    hand calculation,
~~~~

## 162. CRUMB-DOC-0019-APP_B_XI-0015

Kriterij: APP_B_XI — Test Control

objective_control: Kriterij se može temeljiti na dokumentiranim rezultatima drugog verificiranog programa.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.5.     The acceptance criteria of the conducted testing may be based on:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
           2.    documented results from other verified programs,
~~~~

## 163. CRUMB-DOC-0019-APP_B_XI-0016

Kriterij: APP_B_XI — Test Control

objective_control: Kriterij se može temeljiti na pokusnim ili objavljenim podacima.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.5.     The acceptance criteria of the conducted testing may be based on:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
           3.    empirical data or published data in technical literature,
~~~~

## 164. CRUMB-DOC-0019-APP_B_XI-0017

Kriterij: APP_B_XI — Test Control

objective_control: Kriterij se može temeljiti na sličnosti s referentnim outputima.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.5.     The acceptance criteria of the conducted testing may be based on:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
           4.    similarity with reference output files from 6.2.2-1 and 6.2.4.
~~~~

## 165. CRUMB-DOC-0019-APP_B_XI-0018

Kriterij: APP_B_XI — Test Control

objective_control: Svaki osnovni i LSTF test izvodi se i uspoređuje s referentnim izlazom.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.6.     Testing procedure for installation of RELAP5 program shall be based on 6.2.5-4.
           For each of the basic test input decks, and for LSTF input deck, the calculation
           shall be performed and the results shall be checked against reference output files
           (output files are part of original distribution, and for LSTF input deck, output was
           produced developers version and checked against experimental results). The
           checking shall include all important variables:
~~~~

## 166. CRUMB-DOC-0019-APP_B_XI-0019

Kriterij: APP_B_XI — Test Control

objective_control: Usporedba uključuje temperature i tlakove fluida.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.6.     Testing procedure for installation of RELAP5 program shall be based on 6.2.5-4.
           For each of the basic test input decks, and for LSTF input deck, the calculation
           shall be performed and the results shall be checked against reference output files
           (output files are part of original distribution, and for LSTF input deck, output was
           produced developers version and checked against experimental results). The
           checking shall include all important variables:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
           1.       fluid temperatures and pressures,
~~~~

## 167. CRUMB-DOC-0019-APP_B_XI-0020

Kriterij: APP_B_XI — Test Control

objective_control: Usporedba uključuje temperature toplinskih struktura.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.6.     Testing procedure for installation of RELAP5 program shall be based on 6.2.5-4.
           For each of the basic test input decks, and for LSTF input deck, the calculation
           shall be performed and the results shall be checked against reference output files
           (output files are part of original distribution, and for LSTF input deck, output was
           produced developers version and checked against experimental results). The
           checking shall include all important variables:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
           2.       heat structure temperatures,
~~~~

## 168. CRUMB-DOC-0019-APP_B_XI-0021

Kriterij: APP_B_XI — Test Control

objective_control: Usporedba uključuje brzine pare i vode.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.6.     Testing procedure for installation of RELAP5 program shall be based on 6.2.5-4.
           For each of the basic test input decks, and for LSTF input deck, the calculation
           shall be performed and the results shall be checked against reference output files
           (output files are part of original distribution, and for LSTF input deck, output was
           produced developers version and checked against experimental results). The
           checking shall include all important variables:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
           3.       steam and water velocities,
~~~~

## 169. CRUMB-DOC-0019-APP_B_XI-0022

Kriterij: APP_B_XI — Test Control

objective_control: Usporedba uključuje kinetičku snagu kada je primjenjiva.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.6.     Testing procedure for installation of RELAP5 program shall be based on 6.2.5-4.
           For each of the basic test input decks, and for LSTF input deck, the calculation
           shall be performed and the results shall be checked against reference output files
           (output files are part of original distribution, and for LSTF input deck, output was
           produced developers version and checked against experimental results). The
           checking shall include all important variables:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
           4.       reactor kinetics produced power where applicable,
~~~~

## 170. CRUMB-DOC-0019-APP_B_XI-0023

Kriterij: APP_B_XI — Test Control

objective_control: Usporedba uključuje mass error i vremenske korake.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.6.     Testing procedure for installation of RELAP5 program shall be based on 6.2.5-4.
           For each of the basic test input decks, and for LSTF input deck, the calculation
           shall be performed and the results shall be checked against reference output files
           (output files are part of original distribution, and for LSTF input deck, output was
           produced developers version and checked against experimental results). The
           checking shall include all important variables:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
           5.       mass errors and used time steps reported by code.
~~~~

## 171. CRUMB-DOC-0019-APP_B_XI-0024

Kriterij: APP_B_XI — Test Control

objective_control: Test treba potvrditi ispravnu instalaciju.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.7. RELAP5 program testing should prove that:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
1. the code is properly installed,
~~~~

## 172. CRUMB-DOC-0019-APP_B_XI-0025

Kriterij: APP_B_XI — Test Control

objective_control: Test treba potvrditi odsutnost štetne interakcije programa i operativnog sustava.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.7. RELAP5 program testing should prove that:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
2. there is no any adverse interaction of executable version of the program and operating system,
~~~~

## 173. CRUMB-DOC-0019-APP_B_XI-0026

Kriterij: APP_B_XI — Test Control

objective_control: Test provjerava opcije prevoditelja i matematičke funkcije.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.7. RELAP5 program testing should prove that:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
3. compiler options and compiler mathematical functions are working well
~~~~

## 174. CRUMB-DOC-0019-APP_B_XI-0027

Kriterij: APP_B_XI — Test Control

objective_control: Test provjerava greške posebnih compiler ili hardverskih floating-point izvedbi.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.7. RELAP5 program testing should prove that:
~~~~

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
4. no errors were introduced due to nonstandard compiler features, and/or hardware implementations of floating point calculation e.g. computer word size.
~~~~

## 175. CRUMB-DOC-0019-APP_B_XI-0028

Kriterij: APP_B_XI — Test Control

objective_control: Za uspjeh testa traži se najmanje 6–7 značajnih znamenki; dopušteni su fc ili diff za usporedbu.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.8. Due to internally used 64-bit calculation at least 6-7 significant digits shall be used as a success criteria for output results. In special case of PC version the output results should be the same on all Pentium class of computers and file compare (DOS fc) utility may be used for global checking. In case of similar UNIX based computers (similar architecture and word size, IEEE floating point implementation) diff utility may be used for global checking of output files.
~~~~

## 176. CRUMB-DOC-0019-APP_B_XVII-0024

Kriterij: APP_B_XVII — Quality Assurance Records

objective_control: Testovi se izvode, a rezultati verificiraju, dokumentiraju, pohranjuju i kontroliraju.

Izvorno poglavlje: Appendix [line 867] > marpzd4.i [line 955]

Jezik: en

~~~~text
6.2.9. The testing shall be conducted, and the testing results shall be verified, documented, stored and controlled.
~~~~

## 177. CRUMB-DOC-0019-APP_B_XI-0029

Kriterij: APP_B_XI — Test Control

candidate_lead: Uputa spominje pet osnovnih deckova, a zatim sedam zaglavlja; candidate; verify criterion mapping i stvarni obvezni set.

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
               the capability of a computer program to produce valid results using 5
               characteristic test input decks. These inputs decks cover almost all aspects
               of code usage and running options (new, restart, strip, steady state
               initialization) and they are, together with corresponding outputs, part of
               official package distribution.
~~~~

Izvorno poglavlje: Appendix [line 867] > 6.2 RELAP5 Testing Instructions [line 869]

Jezik: en

~~~~text
6.2.3.    The headers of 7 verification input decks are shown hereafter:
~~~~

## 178. CRUMB-DOC-0019-APP_B_XVII-0025

Kriterij: APP_B_XVII — Quality Assurance Records

supporting_control: Primjerne mod3.3 skripte čuvaju prethodne rezultate s oznakom old prije novog runa; nisu izvršene u auditu.

Izvorno poglavlje: Appendix [line 1030] > RELAP5/mod3.3 script file [line 1039]

Jezik: en

~~~~text
### r5m33.bat
~~~~

Izvorno poglavlje: Appendix [line 1030] > RELAP5/mod3.3 script file [line 1039]

Jezik: en

~~~~text
```
copy %1.r %1.r.old
copy %1.o %1.o.old
copy %1.scn %1.scn.old
del %1.r
del %1.o
del %1.scn
c:\r5m33\exe\r5m33p03il2 -i %1.i -o %1.o -r %1.r -Z c:\r5m33\exe\tpfh2onew
copy screen %1.scn
del screen
```
~~~~

Izvorno poglavlje: Appendix [line 1030] > RELAP5/mod3.3 script file [line 1039]

Jezik: en

~~~~text
### r5m33rst.bat
~~~~

Izvorno poglavlje: Appendix [line 1030] > RELAP5/mod3.3 script file [line 1039]

Jezik: en

~~~~text
```
copy %1.r %1.r.old
copy %1.o %1.o.old
copy %1.scn %1.scn.old
del %1.r
del %1.o
del %1.scn
copy %2.r %1.r
c:\r5m33\exe\r5m33p03il2 -i %1.i -o %1.o -r %1.r -Z c:\r5m33\exe\tpfh2onew
copy screen %1.scn
del screen
```
~~~~

## 179. CRUMB-DOC-0019-APP_B_V-0012

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

supporting_control: Primjerne SCDAPSIM skripte razlikuju standardni, restart i strip poziv.

Izvorno poglavlje: Appendix [line 1030] > RELAP5/SCDAPSIM script file [line 1068]

Jezik: en

~~~~text
### r5sim.bat
~~~~

Izvorno poglavlje: Appendix [line 1030] > RELAP5/SCDAPSIM script file [line 1068]

Jezik: en

~~~~text
```
move %1.r %1.r.old
move %1.o %1.o.old
call D:\R5Scdap\rslicense
C:\R5Scdap\relap5 -i %1.i -o %1.o -r %1.r -w C:\R5Scdap\tpfh2o
```
~~~~

Izvorno poglavlje: Appendix [line 1030] > RELAP5/SCDAPSIM script file [line 1068]

Jezik: en

~~~~text
### r5simrst.bat
~~~~

Izvorno poglavlje: Appendix [line 1030] > RELAP5/SCDAPSIM script file [line 1068]

Jezik: en

~~~~text
```
move %1.r %1.r.old
move %1.o %1.o.old
copy %2.r %1.r
call rslicense
c:\R5Scdap_bi9\relap5 -i %1.i -o %1.o -r %1.r
```
~~~~

Izvorno poglavlje: Appendix [line 1030] > RELAP5/SCDAPSIM script file [line 1068]

Jezik: en

~~~~text
### r5simstrip.bat
~~~~

Izvorno poglavlje: Appendix [line 1030] > RELAP5/SCDAPSIM script file [line 1068]

Jezik: en

~~~~text
```
move %1.sto %1.sto.old
move %1.s %1.s.old
call rslicense
c:\R5Scdap\relap5 -i %1.i -o %1.sto -r %2.r -s %1.s
```
~~~~

## 180. CRUMB-DOC-0019-APP_B_VIII-0021

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Title card base decka uključuje njegov ID u propisanim stupcima.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.1. Title card (as defined in Vol.2, Appendix A, ch. 1.3 of Ref. [1]) of base input deck shall contain base input deck ID in columns 2 to 9:
~~~~

## 181. CRUMB-DOC-0019-APP_B_V-0013

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Komentari base decka preporučeno koriste jedan asterisk.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.2. Comments in base input deck should be identified with one * (asterisk) sign only. Usage of more than one asterisk (*) sign is not recommended.
~~~~

## 182. CRUMB-DOC-0019-APP_B_III-0058

Kriterij: APP_B_III — Design Control

objective_control: Komentari iza naslova opisuju nodalizaciju i referentne početne uvjete.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.3. Comments after title card should contain basic information about the nodalization and reference initial conditions.
~~~~

## 183. CRUMB-DOC-0019-APP_B_III-0059

Kriterij: APP_B_III — Design Control

objective_control: Base deck koristi RUN opciju i namijenjen je samo steady-state proračunu.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.4. Base input deck shall have specified RUN option on card 100 (problem type and option card). Base input deck shall be used for steady-state calculations only.
~~~~

## 184. CRUMB-DOC-0019-APP_B_III-0060

Kriterij: APP_B_III — Design Control

objective_control: Trips za zaštitne funkcije grupiraju se u rasponu određenom steady-state izvještajem.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.5. Basic input deck should have trips in expanded format (Vol. 2., Appendix A, ch. 5, Ref. [1]) defined for normal operation:
~~~~

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
1. variable trips numbers within predefined range (specified in steady-state report) used to enable protective plant functions or systems, should be grouped, e.g. from 551 to 590;
~~~~

## 185. CRUMB-DOC-0019-APP_B_III-0061

Kriterij: APP_B_III — Design Control

objective_control: Trips za kašnjenja zaštitnih setpointa grupiraju se.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.5. Basic input deck should have trips in expanded format (Vol. 2., Appendix A, ch. 5, Ref. [1]) defined for normal operation:
~~~~

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
2. variable trips numbers within predefined range (specified in steady-state report) used to define delays for setpoints of plant protection functions and systems, should be grouped, e.g. from 901 to 949;
~~~~

## 186. CRUMB-DOC-0019-APP_B_III-0062

Kriterij: APP_B_III — Design Control

objective_control: Trips za setpointe i ograničenja grupiraju se.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.5. Basic input deck should have trips in expanded format (Vol. 2., Appendix A, ch. 5, Ref. [1]) defined for normal operation:
~~~~

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
3. variable trips numbers within predefined range (specified in steady-state report) used to define setpoints and limitations, should be grouped, e.g. from 101 to 498;
~~~~

## 187. CRUMB-DOC-0019-APP_B_V-0014

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Logički trips koriste se za Boolean operacije.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.5. Basic input deck should have trips in expanded format (Vol. 2., Appendix A, ch. 5, Ref. [1]) defined for normal operation:
~~~~

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
4. logical trips should be used to model Boolean algebra operations;
~~~~

## 188. CRUMB-DOC-0019-APP_B_III-0063

Kriterij: APP_B_III — Design Control

objective_control: Trip 500 rezervira se za inicijaciju tranzijenta.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.5. Basic input deck should have trips in expanded format (Vol. 2., Appendix A, ch. 5, Ref. [1]) defined for normal operation:
~~~~

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
5. trip number 500 should be reserved for transient initiation;
~~~~

## 189. CRUMB-DOC-0019-APP_B_III-0064

Kriterij: APP_B_III — Design Control

objective_control: Trips 598, 599 i 600 koriste se za završetak proračuna.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.5. Basic input deck should have trips in expanded format (Vol. 2., Appendix A, ch. 5, Ref. [1]) defined for normal operation:
~~~~

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6. trip numbers 598, 599 and 600 should be used to define end of calculation.
~~~~

## 190. CRUMB-DOC-0019-APP_B_V-0015

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Variable trip kartica ima komentar svrhe ili statusa.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.6. Each variable trip card should end with comment at the end of line that describes trip purpose or status, e.g. HPIS pump 1 disabled, low-1 PRZ pressure trip.
~~~~

## 191. CRUMB-DOC-0019-APP_B_V-0016

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Skup logičkih kartica ima komentar svoje svrhe.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.7. Each set of logical trip cards should contain comments that describe purpose of logic cards
~~~~

## 192. CRUMB-DOC-0019-APP_B_V-0017

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Posebne base konvencije navode se u pripadajućem steady-state izvještaju.

Izvorno poglavlje: Appendix [line 1101] > 6.4 Base Input Deck Conventions [line 1103]

Jezik: en

~~~~text
6.4.8. Specific conventions for each base input deck shall be specified in corresponding Steady-State Technical Report.
~~~~

## 193. CRUMB-DOC-0019-APP_B_III-0065

Kriterij: APP_B_III — Design Control

supporting_control: Dijagram vraća neprihvatljiv model na update, a neprihvatljive rezultate na korekciju ili deviation report.

Izvorno poglavlje: Appendix [line 1101] > Appendix [line 1143]

Jezik: en

~~~~text
```mermaid
graph TD
    A[Transient specification] --> B[Definition of initial and<br>boundary conditions +<br>determination of main<br>phenomenological<br>aspects]
    B --> C{Base input<br>deck<br>applicability}
    C -->|Not Acceptable| D[Base input deck<br>update]
    D --> C
    C -->|Acceptable| E[Run input deck]
    E --> F[Plot variables file]
    E --> G[Calculation]
    G --> H[Restart file]
    G --> I[Output file]
    F --> J[Graph analysis]
    J --> K[Plot data file]
    J --> L[Analysis of the results]
    I --> L
    L --> M{Applicability of<br>the results}
    M -->|Not Acceptable| N[Error<br>correction]
    N --> O{Model deviations detected}
    O --> P[Analysis<br>Technical<br>Report -<br>Deviation<br>Report]
    M -->|Acceptable| Q[Analysis<br>Technical<br>Report]
    L -->|Minor correction| C
    N -->|Major correction| C
~~~~

## 194. CRUMB-DOC-0019-APP_B_III-0066

Kriterij: APP_B_III — Design Control

supporting_control: Prazan applicability obrazac uspoređuje tranzijentne i base početne uvjete.

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
| Transient ID: | RELAP5/MOD3.2 |
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
| Description:  | TRANSIENT ANALYSIS WORKSHEET<br>Base Input Deck Applicability Form |
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
Base input deck ID: ______________________________
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
| Initial conditions: | Unit | Transient | Base Input Deck |
~~~~

## 195. CRUMB-DOC-0019-APP_B_III-0067

Kriterij: APP_B_III — Design Control

supporting_control: Obrazac razlikuje stanje bez revizije, manju i veću potrebnu reviziju.

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
1. Initial Conditions Check (check appropriate box)
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
1.a) No revison □    1.b) Minor revision needed □    1.c) Major revision needed□
~~~~

## 196. CRUMB-DOC-0019-APP_B_III-0068

Kriterij: APP_B_III — Design Control

supporting_control: Obrazac traži rubne uvjete i potvrdu dostupnosti modela; upisani primjeri nisu odobrena analiza.

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
State in this section major boundary conditions for transient analysis and check for each possibility to be altered in run input deck - like HPIS loop 1 unavailable, backup heaters switched off, letdown isolation on SI signal etc...
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
| Transient Boundary Condition | Model available in Base Input Deck (Yes/No) |
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
| 1) ECCS loop 1 unavailable   | Y                                           |
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
| 2) PRZ backup heaters switched off at reactor trip | Y                     |
~~~~

## 197. CRUMB-DOC-0019-APP_B_III-0069

Kriterij: APP_B_III — Design Control

objective_control: Applicability obrazac traži literaturu s opisom sličnih scenarija.

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
Identify available literature (FSAR, IAEA Technical Documents, CSNI working reports, articles in journals or proceedings etc.) with the description of the similar transient scenarios
~~~~

## 198. CRUMB-DOC-0019-APP_B_III-0070

Kriterij: APP_B_III — Design Control

objective_control: Obrazac traži očekivani scenarij, glavne fenomene i parametre praćenja.

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
Frome the available literature prepare short description of the expected transient scenario and identify main phenomena, along with relevant parameters that could be used for the monitoring of the phenomena like PRZ level, intermediate leg pressure drop, void content in hot legs etc...) Use extra pages if needed
~~~~

## 199. CRUMB-DOC-0019-APP_B_III-0071

Kriterij: APP_B_III — Design Control

objective_control: Nedostupnost modela traži objašnjenje i konzultaciju Technical Project Leadera.

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
| Phenomena | Model available (Yes/No) | Relevant Parameters |
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
If N/A is checked, explain why base input deck is not applicable for the transient analysis. If this is the case Technical Project Leader shall be consulted
~~~~

## 200. CRUMB-DOC-0019-APP_B_III-0072

Kriterij: APP_B_III — Design Control

supporting_control: Obrazac razlikuje potrebnu reviziju od potpune neprimjenjivosti.

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
3. Phenomena CapabilityCheck (check appropriate box)
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
3.a) No revison □   3.b) Minor revision needed □   3.c) Major revision needed □   3.d) N/A □
~~~~

## 201. CRUMB-DOC-0019-APP_B_III-0073

Kriterij: APP_B_III — Design Control

objective_control: Model s potrebnom izmjenom vraća se supervisoru; novi obrazac ispunjava se za novu reviziju.

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
If answers to 1a), 2a)and 3a) are checked, analyst may proceed with the analysis- Chek box Run Input Deck Preparation.
If any other boxes are checked under 1 and 2, nodalization supervisor should be notified and model update shall be performed.
Check box – Update base input deck. Upon receipt of updated base input deck this work sheet shall be filled again for new revision of the base input deck
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
Run Input Deck Preparation □                       Base Input Deck Update □
~~~~

## 202. CRUMB-DOC-0019-APP_B_XVII-0026

Kriterij: APP_B_XVII — Quality Assurance Records

supporting_control: Applicability obrazac predviđa autora, odobrenje i datume.

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
Author: ________________________    Date: ___/___/___            © ENCONET
~~~~

Izvorno poglavlje: Appendix [line 1211] > 6.6 Base Input Deck Applicability Format [line 1213]

Jezik: en

~~~~text
Approved by: ____________________    Date: ___/___/___
~~~~

## 203. CRUMB-DOC-0019-APP_B_III-0074

Kriterij: APP_B_III — Design Control

supporting_control: Plot primjer identificira base i run te odabire fizičke varijable; nije izvršena validacija.

Izvorno poglavlje: Appendix [line 1329] > 6.7 Plot Variables File [line 1331]

Jezik: en

~~~~text
* small break in PRZ, size 1 mm
~~~~

Izvorno poglavlje: Appendix [line 1329] > 6.7 Plot Variables File [line 1331]

Jezik: en

~~~~text
=P1n00e0a runid:P1sba1h0
p
069010000                * pressurizer pressure
p
429010000                * sg1 pressure
p
529010000                * sg2 pressure
tempf
277010000        * cold leg 1 liq. temp.
tempf
377010000        * cold leg 2 liq. temp.
tempf
203010000        * hot leg 1 liq.temp.
tempf
303010000        * hot leg 2 liq. temp.
mflowj
279010000        * cold leg 1 mass flow
mflowj
379010000        * cold leg 2 mass flow
cntrlvar
305              * max. tavg
mflowj
451010000        * steam flow sg 1
mflowj
409010000        * fw flow sg 1
mflowj
551010000        * steam flow sg 2
mflowj
509010000        * fw flow sg 2
mflowj
447010000        * afw flow sg 1
mflowj
547010000        * afw flow sg 1
cntrlvar
004              * pressurizer level (based on dp)
cntrlvar
043              * sg1 nr level (based on dp)
cntrlvar
053              * sg2 nr level (based on dp)
cntrlvar
005              * core level
mflowj
992000000        * break flow
voidfj
992000000        * liquid fraction at break
cntrlvar
901              * core power
cntrlvar
904              * sg 1 exchanged power
cntrlvar
905              * sg 2 exchanged power
cntrlvar
935              * heat losses
cntrlvar
908              * prz heaters power
httemp
111900116        * rod temperature
httemp
~~~~

## 204. CRUMB-DOC-0019-APP_B_VIII-0022

Kriterij: APP_B_VIII — Identification and Control of Materials, Parts, and Components

supporting_control: Run title card povezuje base i run ID u propisanim stupcima.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.1. Title card (as defined in Vol.2, Appendix A, ch. 1.3 of Ref. [1]) of run input deck:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
1. columns 2 to 9 shall contain base input deck ID as specified in 6.4.1.
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
2. 8 characters in columns 17 to 24 shall contain run input deck ID as specified in 3.
~~~~

## 205. CRUMB-DOC-0019-APP_B_V-0018

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Run komentari preporučeno koriste jedan asterisk.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.2. Comments in run input deck should be identified with only one * (asterisk) sign only. Usage of more than one asterisk (*) sign is not recommended.
~~~~

## 206. CRUMB-DOC-0019-APP_B_III-0075

Kriterij: APP_B_III — Design Control

objective_control: Run komentari opisuju tranzijent, rubne uvjete i posebne ulaze.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.3. Comments after title card should contain brief section of comments that describe transient that is analyzed, boundary conditions and comments relevant to the specific input.
~~~~

## 207. CRUMB-DOC-0019-APP_B_V-0019

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Run deck određuje RESTART i broj završnog steady-state restart zapisa.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.4. Run input deck shall have specified:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
1. RESTART option on card 100 (problem type and option card)
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
2. end of steady-state restart number on card 103, as specified in Vol.2, Appendix A, ch. 2.5 Ref. [1].
~~~~

## 208. CRUMB-DOC-0019-APP_B_III-0076

Kriterij: APP_B_III — Design Control

objective_control: Dopuštene promjene uključuju time-step kartice.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.5. Following parameters shall be allowed to be changed in run input deck (in agreement with the input requirements from Vol.2 Appendix A, Ref. [1]:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
1. time step control cards (card numbers from 201 to 299)
~~~~

## 209. CRUMB-DOC-0019-APP_B_III-0077

Kriterij: APP_B_III — Design Control

objective_control: Minor edits trebaju koristiti prethodno propisane karakteristične varijable.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.5. Following parameters shall be allowed to be changed in run input deck (in agreement with the input requirements from Vol.2 Appendix A, Ref. [1]:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
2. minor edit requests should specify same variables as specified in 4.2.2.1-4a
~~~~

## 210. CRUMB-DOC-0019-APP_B_III-0078

Kriterij: APP_B_III — Design Control

objective_control: Aktiviranje ili deaktiviranje zaštitnih funkcija slijedi trip pravila i steady-state izvještaj.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.5. Following parameters shall be allowed to be changed in run input deck (in agreement with the input requirements from Vol.2 Appendix A, Ref. [1]:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
3. plant protective functions, systems or setpoints may be enabled or disabled using variable trips from 6.4.5-1, 2 and 3 (see format of variable trips in Vol. 2, ch. 5.3 of Appendix A of Ref. [1]), as specified in steady-state report. If the system has to be disabled, additive constant should be set erroneously large (1.E6 for example).
~~~~

## 211. CRUMB-DOC-0019-APP_B_III-0079

Kriterij: APP_B_III — Design Control

objective_control: Promjena logičkih trips traži tranzijentni zahtjev i supervisorovo odobrenje.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.5. Following parameters shall be allowed to be changed in run input deck (in agreement with the input requirements from Vol.2 Appendix A, Ref. [1]:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
4. logical trips from 6.4.5-3 (see format of logical trips in Vol. 2, Appendix A, ch. 5.4 of Ref. [1]), should not be changed, unless required by transient specifications and approved by nodalization supervizor.
~~~~

## 212. CRUMB-DOC-0019-APP_B_III-0080

Kriterij: APP_B_III — Design Control

objective_control: Inicijacija tranzijenta koristi namjenske trip brojeve.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.5. Following parameters shall be allowed to be changed in run input deck (in agreement with the input requirements from Vol.2 Appendix A, Ref. [1]:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
5. dedicated trip numbers as specified in steady-state report should be used for transient initiation.
~~~~

## 213. CRUMB-DOC-0019-APP_B_V-0020

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Propisani trips određuju kraj prema CPU i tranzijentnom vremenu.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.5. Following parameters shall be allowed to be changed in run input deck (in agreement with the input requirements from Vol.2 Appendix A, Ref. [1]:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
6. trip numbers 598 should be used to define end of calculation on calculation CPU time limit
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
7. trip number 599 should be used to define end of calculation on transient time limit
~~~~

## 214. CRUMB-DOC-0019-APP_B_III-0081

Kriterij: APP_B_III — Design Control

objective_control: Break valve model mijenja se prema tranzijentnoj specifikaciji.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.5. Following parameters shall be allowed to be changed in run input deck (in agreement with the input requirements from Vol.2 Appendix A, Ref. [1]:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
8. break valve model may be changed according to the transient specifications
~~~~

## 215. CRUMB-DOC-0019-APP_B_III-0082

Kriterij: APP_B_III — Design Control

objective_control: Promjena time-dependent junction modela traži odobrenje supervisora.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.5. Following parameters shall be allowed to be changed in run input deck (in agreement with the input requirements from Vol.2 Appendix A, Ref. [1]:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
9. time-dependent junction models for HPIS, LPIS, AFW and FW may be changed with nodalization supervizor approval
~~~~

## 216. CRUMB-DOC-0019-APP_B_III-0083

Kriterij: APP_B_III — Design Control

objective_control: Dopuštene promjene uključuju scram tablicu i kinetičke podatke.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
### 6.8.5. Following parameters shall be allowed to be changed in run input deck (in agreement with the input requirements from Vol.2 Appendix A, Ref. [1]:
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
10. general table for reactor scram curve may be changed.
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
11. reactor kinetics data may be changed
~~~~

## 217. CRUMB-DOC-0019-APP_B_V-0021

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Run trip kartica ima komentar svrhe ili statusa.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
6.8.6. Each variable trip card should end with comment at the end of line that describes
       trip purpose or status, e.g. HPIS pump 1 disabled.
~~~~

## 218. CRUMB-DOC-0019-APP_B_V-0022

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

objective_control: Run skup logičkih trips ima komentar svrhe.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
6.8.7. Each set of logical trip cards should contain comments that describe purpose of
       logic cards.
~~~~

## 219. CRUMB-DOC-0019-APP_B_III-0084

Kriterij: APP_B_III — Design Control

supporting_control: Primjer runa navodi dostupnost sustava, break veličinu i pretpostavku snage.

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
= P1n00e0a runid:P1sba1h0
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
* both eccs trains available
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
* afw modulated between 10 and 10.5 m
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
* break of instrument line in PRZ id=0.375" (7.126e-5m2)
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
* 2 charging pumps available
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
* fixed core power until trip (no rod control)
~~~~

## 220. CRUMB-DOC-0019-APP_B_V-0023

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

supporting_control: Primjer kartica prikazuje restart, SI jedinice i korake proračuna; nije zapis izvršenog proračuna.

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
= P1n00e0a runid:P1sba1h0
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
*---------------------------------------------------------------------------
100    restart      transnt        * normal run
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
102    si   si      * si units
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
103    5378
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
*       tend         min.dt        max.dt      dtcnt        plt         maj.edt       rst
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
*-----------------------------------------------------------------------
201       200.       1.e-7          0.1        00003         50          2000         2000
202     1200.        1.e-8          0.2        00003           5         5000         5000
203     2200.        1.e-8          0.5        00003           5         2000         2000
204    50200.        1.e-8          0.5        00003         20         25000        25000
~~~~

## 221. CRUMB-DOC-0019-APP_B_XVII-0027

Kriterij: APP_B_XVII — Quality Assurance Records

supporting_control: Prazan razvojni worksheet identificira parametar, karticu, izračun, reference s revizijom, autora i reviewera.

Izvorno poglavlje: Appendix [line 1682] > 6.10 RELAP5 Nodalization Developer Worksheet Format [line 1684]

Jezik: en

~~~~text
| RELAP5/MOD3 INPUT DATA DEVELOPMENT rev. 0 | Page: |
~~~~

Izvorno poglavlje: Appendix [line 1682] > 6.10 RELAP5 Nodalization Developer Worksheet Format [line 1684]

Jezik: en

~~~~text
| Parameter Type:                           | Card Id: |
~~~~

Izvorno poglavlje: Appendix [line 1682] > 6.10 RELAP5 Nodalization Developer Worksheet Format [line 1684]

Jezik: en

~~~~text
| Description:                              |       |
~~~~

Izvorno poglavlje: Appendix [line 1682] > 6.10 RELAP5 Nodalization Developer Worksheet Format [line 1684]

Jezik: en

~~~~text
Calculations, Comments and Figures:
~~~~

Izvorno poglavlje: Appendix [line 1682] > 6.10 RELAP5 Nodalization Developer Worksheet Format [line 1684]

Jezik: en

~~~~text
References (Title, Page number and revision):
~~~~

Izvorno poglavlje: Appendix [line 1682] > 6.10 RELAP5 Nodalization Developer Worksheet Format [line 1684]

Jezik: en

~~~~text
| Author:    | Date: __/__/____ | © ECONET |
~~~~

Izvorno poglavlje: Appendix [line 1682] > 6.10 RELAP5 Nodalization Developer Worksheet Format [line 1684]

Jezik: en

~~~~text
| Reviewer:  | Date: __/__/____ |          |
~~~~

## 222. CRUMB-DOC-0019-APP_B_III-0085

Kriterij: APP_B_III — Design Control

supporting_control: Analitički obrazac traži početne uvjete i dopušta proširenje obvezne liste.

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Transient ID: | RELAP5/MOD3.2 |
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Run Input Deck ID | Page: |
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
Initial Conditions
List is opened beyond mandatory items 1-20 and may be extended on more pages if needed
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Initial Condition | Value | Unit | Note |
~~~~

## 223. CRUMB-DOC-0019-APP_B_III-0086

Kriterij: APP_B_III — Design Control

supporting_control: Obrazac traži dostupnost, relativni kapacitet i pretpostavke početka ili tripa sustava.

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Transient ID: | RELAP5/MOD3.2 |
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Run Input Deck ID | Page: |
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
Boundary Conditions
Availability of the systems as well as the ratio of capacity relative to nominal should be specified. Any assumptions related to the
start or trip of any system other than "act as prescribed" should be specified . List is opened beyond mandatory items 1-19 and
may be extended on more pages if needed.
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Boundary Condition | Specification | Note |
~~~~

## 224. CRUMB-DOC-0019-APP_B_XVII-0028

Kriterij: APP_B_XVII — Quality Assurance Records

supporting_control: Worksheet predviđa ID runa, bilješke, analizu i autora s datumom.

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Transient ID: | RELAP5/MOD3.2 |
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Run Input Deck ID | Page: |
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
Notes, Analysis, Comments on Results
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Author: | Date: /     /    / |
~~~~

## 225. CRUMB-DOC-0019-APP_B_XVII-0029

Kriterij: APP_B_XVII — Quality Assurance Records

supporting_control: Worksheet rezultata povezuje grafove s runom i autorom.

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Transient ID: | RELAP5/MOD3.2 |
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Run Input Deck ID | Page: |
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
Analysis Results (Graphs)
~~~~

Izvorno poglavlje: Appendix [line 1710] > 6.11 RELAP5 Analyst Worksheet Format [line 1712]

Jezik: en

~~~~text
| Author: ______________________ Date: ___/___/___ |
~~~~

## 226. CRUMB-DOC-0019-APP_B_V-0024

Kriterij: APP_B_V — Instructions, Procedures, and Drawings

candidate_lead: Prag mass error navodi manji od 1% za prihvat i veći od 1% za sumnju; candidate; verify criterion mapping za točno 1%.

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
3. The results of the analysis of RELAP5 calculation shall be considered satisfactory if:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. trip status is in accordance with 4.2.1.2-2
   b. relative mass error is less than 1%
   c. the prediction of relative thermohydraulic aspects is explained and justified
   d. If all off the above terms a, b and c are fulfilled, RELAP5 analyst shall proceed with step 6.
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
4. The results of the analysis of RELAP5 calculation shall be considered doubtful if:
~~~~

Izvorno poglavlje: 4     INSTRUCTIONS [line 311] > 4.2 Transient Analysis Instructions [line 484]

Jezik: en

~~~~text
   a. Trip status is not in accordance with 4.2.1.2-2. Corrective action should be to adjust trips in run input deck according to 4.2.1.2-2.
   b. Relative mass error is greater than 1%. Corrective action is to decrease maximum time step size according to the specifications from Vol. 2, Appendix A, ch.3 of Ref. [1].
   c. The prediction of relative thermohydraulic aspects is not completely understood. Corrective action is to consult literature or qualified user - expert.
   d. One or some of the parameters show erratic behavior or unexplainable oscillations. Corrective actions should be performed in following order:
      i) to decrease maximum time step size;
      ii) to run parametric study for critical parameters;
      iii) to request renodalization or update of base input deck after consultation with qualified user.
      iv) Should none of the corrective actions lead to fulfillment of requests from 3 RELAP5 analyst should proceed to 5.
~~~~

## 227. CRUMB-DOC-0019-APP_B_III-0087

Kriterij: APP_B_III — Design Control

candidate_lead: Primjer kartica izgleda zamjenjuje značenje trips 598 i 599 prema konvenciji; candidate; verify criterion mapping prije uporabe primjera.

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
6. trip numbers 598 should be used to define end of calculation on calculation CPU time limit
~~~~

Izvorno poglavlje: Appendix [line 1452] > 6.8 Run Input Deck Conventions [line 1454]

Jezik: en

~~~~text
7. trip number 599 should be used to define end of calculation on transient time limit
~~~~

Izvorno poglavlje: Appendix [line 1452] > Appendix [line 1513]

Jezik: en

~~~~text
20605980 time          0 ge timeof 1633          300.     l * end of transient
20605990 cputime 0 gt null                0 200000.       l * end of transient
~~~~

