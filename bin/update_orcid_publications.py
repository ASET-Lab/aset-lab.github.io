#!/usr/bin/env python
"""Regenerate _bibliography/orcid.bib from the ORCID records of lab members.

ORCID iDs are read from the `orcid` field of each person in _data/coauthors.yml.
Settings (output file, earliest year, work types, exclusions) live under
`orcid_publications` in _config.yml.

For every work with a DOI, full metadata (authors, venue, pages, abstract) is
fetched from doi.org as CSL-JSON, which covers both Crossref and DataCite
(arXiv, Zenodo). Works without a DOI fall back to the ORCID record itself.

Works that already appear in another .bib file in _bibliography/ (matched by
DOI or title) are skipped, so a hand-edited entry in papers.bib always wins.

Usage: python bin/update_orcid_publications.py
"""

import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

import yaml

CONFIG_FILE = "_config.yml"
PEOPLE_FILE = "_data/coauthors.yml"
BIB_DIR = "_bibliography"
ORCID_API = "https://pub.orcid.org/v3.0"
USER_AGENT = "aset-lab.github.io publication updater (https://github.com/ASET-Lab/aset-lab.github.io)"

DEFAULTS = {
    "output": "_bibliography/orcid.bib",
    "since_year": None,
    "work_types": ["journal-article", "conference-paper", "book", "book-chapter", "edited-book", "preprint"],
    "exclude": [],
}

# CSL type -> (BibTeX type, field that holds the venue)
CSL_TYPES = {
    "article-journal": ("article", "journal"),
    "paper-conference": ("inproceedings", "booktitle"),
    "chapter": ("incollection", "booktitle"),
    "book": ("book", None),
    "edited-book": ("book", None),
    "report": ("techreport", "institution"),
    "thesis": ("phdthesis", "school"),
    "posted-content": ("article", "journal"),
    "article": ("article", "journal"),
}

# ORCID work type -> CSL type, used when no DOI metadata is available
ORCID_TYPES = {
    "journal-article": "article-journal",
    "conference-paper": "paper-conference",
    "book-chapter": "chapter",
    "book": "book",
    "edited-book": "edited-book",
    "preprint": "posted-content",
    "report": "report",
    "dissertation-thesis": "thesis",
}

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
TITLE_STOPWORDS = {"a", "an", "the", "on", "of", "in", "for", "to", "and", "towards", "toward", "using", "with"}


def fetch_json(url, accept="application/json", attempts=4):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": USER_AGENT})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == attempts - 1:
                raise
            time.sleep(int(e.headers.get("Retry-After") or 0) or 2**attempt)


def load_settings():
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f) or {}
    settings = dict(DEFAULTS)
    settings.update(config.get("orcid_publications") or {})
    exclude = settings["exclude"] or []
    settings["exclude"] = {doi_key(x) for x in exclude} | {normalize(x) for x in exclude}
    return settings


def load_members():
    with open(PEOPLE_FILE) as f:
        people = yaml.safe_load(f) or {}
    members = []
    for entries in people.values():
        for person in entries or []:
            orcid = str(person.get("orcid") or "").strip()
            if orcid:
                name = f"{person['firstname'][0]} {person['lastname']}"
                members.append((name, orcid.rsplit("/", 1)[-1]))
    return members


def doi_key(doi):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", str(doi).strip().lower())


def normalize(text):
    """Lower-case, accent- and punctuation-free form used for matching titles."""
    text = unicodedata.normalize("NFKD", html.unescape(str(text))).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def title_key(title):
    """Titles are only used for matching when specific enough ("Editorial" is not)."""
    key = normalize(title)
    return key if len(key.split()) >= 4 else None


def known_entries(output):
    """DOIs and titles already present in hand-maintained .bib files."""
    known = set()
    for name in os.listdir(BIB_DIR):
        path = os.path.join(BIB_DIR, name)
        if not name.endswith(".bib") or os.path.abspath(path) == os.path.abspath(output):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for field, key in (("doi", doi_key), ("title", normalize)):
            for value in re.findall(rf"^\s*{field}\s*=\s*[{{\"](.+?)[}}\"]\s*,?\s*$", text, re.M | re.I):
                known.add(key(value.replace("{", "").replace("}", "")))
    return known


def orcid_works(name, orcid, settings):
    """Filtered work summaries from one ORCID record."""
    data = fetch_json(f"{ORCID_API}/{orcid}/works")
    works = []
    for group in data.get("group", []):
        summary = group["work-summary"][0]
        if summary.get("type") not in settings["work_types"]:
            continue
        date = summary.get("publication-date") or {}
        year = int((date.get("year") or {}).get("value") or 0)
        if not year or (settings["since_year"] and year < int(settings["since_year"])):
            continue
        ids = {}
        for ext in group.get("external-ids", {}).get("external-id", []):
            if ext.get("external-id-relationship") == "self":
                ids.setdefault(ext["external-id-type"], ext["external-id-value"])
        month = int((date.get("month") or {}).get("value") or 0)
        works.append(
            {
                "orcid": orcid,
                "put_code": summary["put-code"],
                "type": summary["type"],
                "title": ((summary.get("title") or {}).get("title") or {}).get("value", "").strip(),
                "venue": (summary.get("journal-title") or {}).get("value"),
                "year": year,
                "month": month,
                "doi": doi_key(ids["doi"]) if "doi" in ids else None,
                "arxiv": ids.get("arxiv"),
                "url": (summary.get("url") or {}).get("value"),
            }
        )
    print(f"  {name} ({orcid}): {len(works)} works")
    return works


def dedupe(works):
    """Collapse the same paper reported by several members, or as preprint + published version."""

    def rank(w):
        return (w["type"] != "preprint", w["doi"] is not None, w["year"])

    by_key = {}
    for w in sorted(works, key=rank, reverse=True):
        keys = [k for k in (w["doi"], title_key(w["title"])) if k]
        existing = next((by_key[k] for k in keys if k in by_key), None)
        if existing:
            existing["arxiv"] = existing["arxiv"] or w["arxiv"]
            if w["doi"] and w["doi"].startswith("10.48550/"):
                existing["arxiv"] = existing["arxiv"] or w["doi"].split("arxiv.", 1)[-1]
        else:
            existing = w
        for k in keys:
            by_key.setdefault(k, existing)
    unique = {id(w): w for w in by_key.values()}
    return list(unique.values())


def from_crossref(item):
    """Crossref's native JSON is CSL-JSON apart from type names and list-valued titles."""
    types = {
        "journal-article": "article-journal",
        "proceedings-article": "paper-conference",
        "book-chapter": "chapter",
        "monograph": "book",
        "dissertation": "thesis",
    }
    csl = dict(item)
    csl["type"] = types.get(item.get("type"), item.get("type"))
    csl["title"] = (item.get("title") or [None])[0]
    # Book chapters list [series, book title], e.g. ["Lecture Notes in Computer Science", "Search-Based ..."]
    csl["container-title"] = (item.get("container-title") or [None])[-1]
    return csl


def fetch_metadata(works):
    """Attach CSL-JSON metadata to every work with a DOI (as `csl`, or None if unavailable)."""
    by_doi = {w["doi"]: w for w in works if w["doi"]}
    for w in works:
        w["csl"] = None
    # Crossref holds most DOIs and answers up to 40 per request.
    dois = list(by_doi)
    for i in range(0, len(dois), 40):
        chunk = dois[i : i + 40]
        query = urllib.parse.quote(",".join(f"doi:{d}" for d in chunk), safe=":,/")
        try:
            data = fetch_json(f"https://api.crossref.org/works?rows={len(chunk)}&filter={query}")
        except Exception as e:
            print(f"  warning: Crossref lookup failed ({e})")
            continue
        for item in data["message"]["items"]:
            if item["DOI"].lower() in by_doi:
                by_doi[item["DOI"].lower()]["csl"] = from_crossref(item)
    # The rest (DataCite: arXiv, Zenodo, ...) one at a time via doi.org content negotiation.
    for doi, w in by_doi.items():
        if w["csl"] is None:
            try:
                url = "https://doi.org/" + urllib.parse.quote(doi, safe="/")
                w["csl"] = fetch_json(url, "application/vnd.citationstyles.csl+json")
            except Exception as e:
                print(f"  warning: no DOI metadata for {doi} ({e}); using ORCID record")


def fetch_orcid_contributors(works):
    """Author names from full ORCID work records, for works without DOI metadata."""
    by_orcid = {}
    for w in works:
        by_orcid.setdefault(w["orcid"], []).append(w)
    for orcid, items in by_orcid.items():
        for i in range(0, len(items), 100):
            batch = {w["put_code"]: w for w in items[i : i + 100]}
            try:
                data = fetch_json(f"{ORCID_API}/{orcid}/works/{','.join(map(str, batch))}")
            except Exception as e:
                print(f"  warning: could not read full ORCID records for {orcid} ({e})")
                continue
            for result in data.get("bulk", []):
                record = result.get("work") or {}
                names = [
                    (c.get("credit-name") or {}).get("value")
                    for c in (record.get("contributors") or {}).get("contributor", [])
                ]
                if record.get("put-code") in batch:
                    batch[record["put-code"]]["authors"] = [n for n in names if n]


def clean(value):
    """Make a string safe to place inside a braced BibTeX value."""
    if isinstance(value, list):
        value = value[0] if value else ""
    value = html.unescape(re.sub(r"<[^>]+>", " ", str(value)))
    value = value.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s+", " ", value).strip()


def csl_name(person):
    if person.get("family"):
        return f"{person['family']}, {person['given']}" if person.get("given") else person["family"]
    return person.get("literal") or person.get("name") or ""


def plain_name(name):
    """'Neil Walkinshaw' -> 'Walkinshaw, Neil' (ORCID credit names are free text)."""
    if "," in name:
        return name
    parts = name.split()
    return f"{parts[-1]}, {' '.join(parts[:-1])}" if len(parts) > 1 else name


def to_entry(w):
    csl = w.get("csl") or {}
    csl_type = csl.get("type") if csl.get("type") in CSL_TYPES else ORCID_TYPES.get(w["type"], "article")
    if w["type"] == "preprint" or (w["doi"] or "").startswith("10.48550/"):
        csl_type = "posted-content"
    bib_type, venue_field = CSL_TYPES.get(csl_type, ("misc", None))

    date = (csl.get("issued") or {}).get("date-parts", [[None]])[0]
    year = date[0] if date and date[0] else w["year"]
    month = date[1] if date and len(date) > 1 else w["month"]

    venue = csl.get("container-title") or w["venue"]
    if isinstance(venue, list):
        venue = venue[0] if venue else None
    if csl_type == "posted-content":
        venue = venue or csl.get("publisher") or "Preprint"
        if w["arxiv"] or (w["doi"] or "").startswith("10.48550/"):
            w["arxiv"] = w["arxiv"] or w["doi"].split("arxiv.", 1)[-1]
            venue = f"arXiv preprint arXiv:{w['arxiv']}"

    if csl:
        authors = [csl_name(a) for a in csl.get("author") or csl.get("editor") or []]
    else:
        authors = [plain_name(n) for n in w.get("authors", [])]
    abstract = re.sub(r"^\s*abstract[\s:.]*", "", clean(csl.get("abstract") or ""), flags=re.I)

    fields = {
        "title": csl.get("title") or w["title"],
        "author": " and ".join(clean(a) for a in authors if a),
        venue_field: venue,
        "publisher": csl.get("publisher") if bib_type in ("book", "incollection", "inproceedings") else None,
        "volume": csl.get("volume"),
        "number": csl.get("issue"),
        "pages": (csl.get("page") or "").replace("-", "--") or None,
        "year": year,
        "month": MONTHS[month - 1] if month and 1 <= month <= 12 else None,
        "doi": csl.get("DOI") or (w["doi"] if w["doi"] and not w["doi"].startswith("10.48550/") else None),
        "arxiv": w["arxiv"],
        "html": w["url"] if not w["doi"] and not w["arxiv"] else None,
        "abstract": abstract,
        "bibtex_show": "true",
    }
    fields.pop(None, None)
    return bib_type, {k: clean(v) for k, v in fields.items() if v}


def make_key(fields, used):
    author = fields.get("author", "anon").split(" and ")[0].split(",")[0]
    author = re.sub(r"[^a-z]", "", normalize(author)) or "anon"
    words = [x for x in re.findall(r"[a-z0-9]+", normalize(fields["title"])) if x not in TITLE_STOPWORDS]
    base = f"{author}{fields.get('year', '')}{words[0] if words else ''}"
    key, n = base, 1
    while key in used:
        key, n = f"{base}{chr(ord('a') + n)}", n + 1
    used.add(key)
    return key


def format_entry(bib_type, key, fields):
    width = max(len(k) for k in fields)
    lines = [f"  {k.ljust(width)} = {v}" if k == "month" else f"  {k.ljust(width)} = {{{v}}}" for k, v in fields.items()]
    return f"@{bib_type}{{{key},\n" + ",\n".join(lines) + "\n}\n"


def main():
    settings = load_settings()
    output = settings["output"]
    members = load_members()
    if not members:
        print(f"No `orcid` fields found in {PEOPLE_FILE}; nothing to do.")
        return

    print(f"Reading ORCID records for {len(members)} people...")
    try:
        works = [w for name, orcid in members for w in orcid_works(name, orcid, settings)]
    except (OSError, ValueError) as e:
        # Never write a partial list: a transient failure must not delete someone's papers.
        print(f"Error: could not read ORCID records ({e}). Leaving {output} unchanged.")
        sys.exit(1)

    skip = known_entries(output) | settings["exclude"]
    works = [w for w in dedupe(works) if w["doi"] not in skip and normalize(w["title"]) not in skip and w["title"]]
    print(f"{len(works)} unique works after de-duplication and exclusions")

    fetch_metadata(works)
    with_doi = [w for w in works if w["doi"]]
    missing = sum(1 for w in with_doi if not w["csl"])
    if with_doi and missing > len(with_doi) / 4:
        # Most likely a Crossref/doi.org outage; don't replace good entries with ORCID-only ones.
        print(f"Error: no DOI metadata for {missing} of {len(with_doi)} works. Leaving {output} unchanged.")
        sys.exit(1)
    fetch_orcid_contributors([w for w in works if not w["csl"]])

    entries = []
    for bib_type, fields in map(to_entry, works):
        if fields.get("author"):
            entries.append((bib_type, fields))
        else:  # front matter ("Message from the Chairs", "Preface") has no authors
            print(f"  skipped (no authors): {fields['title']}")

    def newest_first(entry):
        fields = entry[1]
        month = MONTHS.index(fields["month"]) + 1 if "month" in fields else 0
        return (-int(fields["year"]), -month, fields["title"].lower())

    entries.sort(key=newest_first)
    used = set()
    body = "\n".join(format_entry(t, make_key(f, used), f) for t, f in entries)
    header = (
        "% AUTO-GENERATED by bin/update_orcid_publications.py from the ORCID iDs in _data/coauthors.yml.\n"
        "% Do not edit by hand: changes are overwritten on the next run. To correct or enrich a paper,\n"
        "% copy its entry into papers.bib and edit it there; that version then replaces this one.\n\n"
    )
    content = header + body

    if os.path.exists(output):
        with open(output, encoding="utf-8") as f:
            if f.read() == content:
                print(f"No changes to {output}.")
                return
    with open(output, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {len(entries)} entries to {output}")


if __name__ == "__main__":
    main()
