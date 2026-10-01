# EK-1.2 candidate: local offline evidence links

This slice copies three files from one versioned template: the evidence-link
schema, the navigation helper, and the citation renderer. It supplies a safe
link format for later reports and offline viewers. It does not build a viewer,
claim that an evidence target exists, or make an audit finding.

The bootstrap previews the exact files, checks their hashes, and refuses a
conflicting target. Its first Ekonerg apply used run ID
`evidence-links-20261001-01`; the journal is under
`Ekonerg/.bootstrap/evidence-links-v1/`. A repeat preview preserves all three
files. The old Enconet copy was not changed.

Tests use two fake company names, one with spaces and one with a Croatian
character. They check retry, sibling isolation, valid IDs, missing targets,
literal text, safe relative viewer paths, and rejection of outside paths.
No real documents or source records were read or changed.

This is a candidate pending Claude's technical review. EK-1.2 stays open;
later report and viewer tools still need their own local copies and tests.
