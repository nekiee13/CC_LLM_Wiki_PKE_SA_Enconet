# Enconet — G2 odobren i primijenjen

Vlasnik je odgovorio **G2-eun Approved** na odmah prethodno predstavljen
prijedlog `G2-RUN-20261008-17`. Odluka je evidentirana kao odobrenje te
matrice, ne kao odobrenje ocjena.

## Što je primijenjeno

- Svih **18 kriterija** je uključeno u odobrenom opsegu odgovornosti.
- XIII je ograničen na opisanu MTE i relevantnu fizičku softversku mediju,
  uz granice iz odobrenog prijedloga. Nije uvedena opća proizvodnja ili logistika.
- Part21 spremnost ostaje zasebna. Neposredna NRC jurisdikcija, US ugovor i
  dedication uloga nisu pretpostavljeni.
- U bazi je evaluation run `RUN-20261008-17` i **18 odobrenih applicability redova**.
- Odobrio: `project-owner`, datum: `2026-10-08`, referenca: `G2-RUN-20261008-17`.
- Faza je **evidence_reviewed**; G2 approved, G3–G7 pending.
- **Nema conformance ocjena.** G2 odabire što se procjenjuje, ne koliko dobro.

Nije izmijenjen sadržaj prethodnog prijedloga ili njegove matrice.
Importer čuva to odobreno obrazloženje uz novu approval metapodatkovnu vezu.
Historijski nacrt ostaje nacrt kakav je vlasnik pregledao; ovaj zapis pokazuje
kasniju odluku i stvarnu primjenu.

## Normalni redoslijed — bez zaobilaženja gatea

1. Potpisani G2 red dodan je u approvals manifest.
2. Uobičajena tranzicija chunked → sieved; svih šest provjera te faze prolazi.
3. Canonical dispatcher stvorio je G2 packet u ispravnoj fazi.
4. Packet recorder preuzeo je postojeće odobrenje vlasnika i evidentirao G2.
5. Postojeći importer dodao je odobrenu matricu, bez ocjena.
6. Uobičajena tranzicija sieved → evidence_reviewed; osam provjera prolazi.

Creatorova poruka STOP označuje da alat ne bira odluku. Nakon nje je
recorder upotrijebio već izričito dano odobrenje vlasnika. Nije traženo novo,
istovjetno odobrenje niti je alat sam odobrio scope.

## Dokazi i provjere

- [Odobreni G2 packet](../wiki/gates/G2-RUN-20261008-17-enconet.md).
- [Matrica koju je vlasnik odobrio](G2_APPLICABILITY_MATRIX_20261008.json).
- [Prijedlog s obrazloženjima i citatima](G2_APPLICABILITY_OWNER_REVIEW_20261008.md).
- [Naredbe, exit codes i prije/poslije hashes](G2_APPLICABILITY_APPLIED_EVIDENCE_20261008.json).

Neovisna read-only provjera potvrdila je da su svih 18 uvezenih redova,
obrazloženja, source IDs i approval vrijednosti točno jednaki odobrenom inputu.
Svi raniji redci 15 DB tablica ostaju hash-exact. Dodani su samo evaluation
run i 18 applicability redova. Broj criterion_evaluations i evaluation_evidence
redova ostaje nula. Matrica nije ponovno uvezena radi retry testa jer postojeći
importer ne služi prepisivanju odobrenih runova.

Vendor stanje ostaje **2.700 crumbs i 5.171 poveznica**. Ukupno je i dalje
**2.998 crumbs i 5.677 poveznica**. Svi izvori, poglavlja, governing zahtjevi i
ranije aktivne generacije ostaju nepromijenjeni. Svih 36 incoming datoteka je
hash-exact. Nije napravljen repair, migration, resieve ili izračun ocjena.

Finalni aggregate: exit **0**, **osam provjera** faze evidence_reviewed prolazi.
Ocjene, report i dashboard provjere su SKIPPED jer ti rezultati još ne postoje.
To nije tvrdnja da je završni audit izvještaj već provjeren. Početne reporting
JSON/PowerShell dijagnostičke greške zabilježene su i ne prikazuju se kao passed.

## Sljedeća zadaća

Dokumentacijska procjena svih 18 kriterija pod `RUN-20261008-17`, prema
postojećoj petostupanjskoj metodologiji, s vendor crumbs i objašnjenjem svake
ocjene. Part21 ostaje odvojen. Ne tražimo da vlasnik sam unosi ocjene.

Lokalni scoring model je pročitan: run nosi `0.1-placeholder`, s postojećim
vrijednostima 100/75/50/25/0 i jednakom težinom primjenjivih kriterija. YAML
izričito označuje kalibraciju kao pending do G3. Sljedeća zadaća može
pripremiti dokumentacijske ocjene i izračun prema toj postojećoj skali za
G3 pregled; G2 nije odobrio konačnu kalibraciju ili promjenu brojeva.
Ne smije se izmišljati nova skala ili kategorija niti tražiti da vlasnik
sam ocjenjuje svaki kriterij. Ograničenje modela mora biti jasno označeno
u nacrtu rezultata, bez glumljenja konačnog G3 odobrenja.

ASME2.7 §201 ostaje izvorni fragment za provjeru. Nedostajući PP-74-01 ostaje
zahtjev za provjeru ili dostavu, ne automatsko isključenje kriterija. Claude
review je odgođen; G2 approval ne predstavlja Claudeovu tehničku potvrdu.
