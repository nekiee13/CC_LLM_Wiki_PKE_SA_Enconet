"""Measure all narrative prose in this plan; print reproducible JSON evidence.

Policy v1: omit headings, tables, code, rules and label-only lines. Keep all
other prose, including tests and acceptance criteria. Join wrapped paragraphs;
treat each list item as a sentence if it lacks final punctuation. Report every
exclusion with its source line. This is a plan-specific Markdown reader, not a
general Markdown parser. Review its emitted prose when changing the document.
"""
import argparse
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import re
import sys


def extract_prose(markdown):
    units, paragraph, excluded = [], [], []
    fence = None

    def flush():
        if paragraph:
            text = " ".join(paragraph)
            units.append(text if text[-1] in ".!?" else text + ".")
            paragraph.clear()

    for number, raw in enumerate(markdown.splitlines(), 1):
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            marker = line[:3]
            fence = None if fence == marker else (fence or marker)
            flush()
            excluded.append({"line": number, "kind": "fence", "text": raw})
            continue
        kind = ("code" if fence else "heading" if line.startswith("#") else
                "table" if line.startswith("|") else
                "rule" if re.fullmatch(r"[-*_]{3,}", line) else None)
        if kind:
            flush()
            excluded.append({"line": number, "kind": kind, "text": raw})
            continue
        if not line:
            flush()
            continue
        if re.match(r"^(?:[-*+] |\d+\. )", line):
            flush()
            line = re.sub(r"^(?:[-*+] |\d+\. )(?:\[[ xX]\] )?", "", line)
        if re.match(r"^\*\*[^*]+:\*\*", line):
            label = re.match(r"^\*\*[^*]+:\*\*", line).group()
            excluded.append({"line": number, "kind": "label", "text": label})
            line = line[len(label):].strip()
        for token in re.findall(r"`[^`]+`", line):
            excluded.append({"line": number, "kind": "inline-code", "text": token})
        line = re.sub(r"`[^`]+`", "", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"\s+", " ", line.replace("**", "")).strip()
        line = re.sub(r"\s+([.,;:!?])", r"\1", line)
        if re.search(r"[A-Za-z]", line):
            paragraph.append(line)
    flush()
    if fence:
        raise ValueError("Unclosed code fence")
    return "\n".join(units), excluded


def grade_from_counts(words, sentences, syllables):
    if min(words, sentences, syllables) <= 0:
        raise ValueError("Nonempty English prose is required")
    return 0.39 * words / sentences + 11.8 * syllables / words - 15.59


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--limit", type=float, default=9)
    parser.add_argument("--details", action="store_true", help="Include prose and exclusions")
    args = parser.parse_args()
    try:
        if not math.isfinite(args.limit):
            raise ValueError("Limit must be finite")
        import nltk
        import textstat

        # Fail before textstat can attempt its implicit dictionary download.
        nltk.data.path[:] = [str(Path(sys.prefix) / "nltk_data")]
        corpus = Path(str(nltk.data.find("corpora/cmudict"))) / "cmudict"
        corpus_hash = hashlib.sha256(corpus.read_bytes()).hexdigest()
        source = args.plan.read_text(encoding="utf-8-sig")
        prose, exclusions = extract_prose(source)
        textstat.set_lang("en_US")
        words = textstat.lexicon_count(prose, removepunct=True)
        sentences = textstat.sentence_count(prose)
        syllables = textstat.syllable_count(prose)
        grade = grade_from_counts(words, sentences, syllables)
        report = {
            "policy": "all-plan-prose-v1", "language": "en_US",
            "plan_lf_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "prose_sha256": hashlib.sha256(prose.encode()).hexdigest(),
            "python": sys.version.split()[0],
            "versions": {name: importlib.metadata.version(name)
                         for name in ("textstat", "nltk", "pyphen")},
            "cmudict_sha256": corpus_hash,
            "words": words, "sentences": sentences, "syllables": syllables,
            "grade": grade, "limit": args.limit, "passed": grade <= args.limit,
            "excluded_items": len(exclusions),
        }
        if args.details:
            report.update(prose=prose, exclusions=exclusions)
        print(json.dumps(report, indent=2, ensure_ascii=True))
        return 0 if report["passed"] else 1
    except (ImportError, LookupError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
