import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evidence_matching import quote_matches


def test_matches_markdown_formatting_and_html_noise():
    quote = "Revizije i promjene šalju se korisnicima kontroliranih kopija."
    chunk = "**3.8.2.** Revizije i promjene šalju se korisnicima " \
        "kontroliranih kopija. <em>Napomena</em>"
    assert quote_matches(quote, chunk)


def test_matches_explicit_ellipsis_as_ordered_source_segments():
    quote = "Initial notification by facsimile ... within two days following receipt"
    chunk = "Initial notification by facsimile, which is preferred, within two days following receipt"
    assert quote_matches(quote, chunk)


def test_matches_duplicate_list_marker_from_markdown_conversion():
    quote = "6. Verifikacija ulaznih podataka"
    chunk = "6. 6. Verifikacija ulaznih podataka"
    assert quote_matches(quote, chunk)


def test_rejects_unrelated_text():
    assert not quote_matches("A control was approved", "A control was not approved")
