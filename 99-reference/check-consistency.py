#!/usr/bin/env python3
"""
Consistency checker for the learn-claude track.

Run from the repo root:   python3 99-reference/check-consistency.py

Catches the class of error that's hardest to spot by reading: numbers that were
correct once, or written from memory, and now disagree with the pricing table or
with each other. Exits non-zero if anything fails, so it can go in CI.
"""

import os
import re
import sys
import glob
from datetime import date

# --- Single source of truth. Update here when prices change. ------------------
# NOTE: this checks that the track agrees with *this table*, not that the table
# agrees with Anthropic's live pricing. Re-verify it by hand against
# https://platform.claude.com/docs/en/about-claude/pricing and bump the date
# below; a stale date produces a warning (see section 7).
PRICES_LAST_VERIFIED = "2026-10-02"
PRICES_STALE_AFTER_DAYS = 31

CURRENT = {         # model            (input $/MTok, output $/MTok)
    "Fable 5.1":    (10, 50),
    "Opus 5.5":     (4, 20),
    "Sonnet 5.5":   (2, 10),
    "Haiku 4.5":    (1, 5),
}
LEGACY = {          # still available, no longer the lineup the track leads with
    "Fable 5":      (10, 50),
    "Opus 5":       (5, 25),
    "Sonnet 5":     (2, 10),   # $2/$10 is now standard, not introductory
}
PRICES = {**LEGACY, **CURRENT}
CHEAPEST = "Haiku 4.5"


def model_pattern(model):
    """'Claude <model>' not followed by more version digits, so that
    'Claude Opus 5' doesn't match inside 'Claude Opus 5.5'."""
    return re.compile(rf"Claude {re.escape(model)}(?!\.?\d)")


failures = []
warnings = []


def fail(msg):
    failures.append(msg)


def warn(msg):
    warnings.append(msg)


files = sorted(glob.glob("**/*.md", recursive=True))
if not files:
    sys.exit("No markdown found — run this from the repo root.")


# --- 1. Price ratio claims ----------------------------------------------------
# Any "N× cheaper than <family>" must match a model in that family. A claim that
# matches only a legacy model is a warning (the track should lead with current
# models); one that matches nothing is a failure.
base_in = PRICES[CHEAPEST][0]


def ratios_for(family, table):
    return {p[0] / base_in for m, p in table.items() if m.split()[0].lower() == family.lower()}


for path in files:
    text = open(path).read()
    for m in re.finditer(r"(\d+)×\s*cheaper than (\w+)", text):
        claimed, family = int(m.group(1)), m.group(2)
        current, everything = ratios_for(family, CURRENT), ratios_for(family, PRICES)
        if not everything:
            continue
        if any(abs(claimed - r) <= 0.01 for r in current):
            continue
        if any(abs(claimed - r) <= 0.01 for r in everything):
            warn(f"{path}: '{m.group(0)}' matches only a legacy {family} model")
        else:
            shown = "/".join(f"{r:g}×" for r in sorted(current))
            fail(f"{path}: claims '{m.group(0)}' but table says {shown}")


# --- 2. Price tables agree with each other -----------------------------------
for path in files:
    for line in open(path):
        for model, (inp, out) in PRICES.items():
            if model_pattern(model).search(line) and "$" in line:
                found = re.findall(r"\$(\d+)", line)
                if len(found) >= 2 and (int(found[0]), int(found[1])) != (inp, out):
                    # Intro/promotional pricing is called out explicitly; allow it.
                    if "intro" not in line.lower():
                        fail(f"{path}: {model} priced ${found[0]}/${found[1]}, "
                             f"table says ${inp}/${out}")


# --- 3. Internal links resolve ------------------------------------------------
for path in files:
    d = os.path.dirname(path)
    # {{ ... }} / {% ... %} targets are Liquid, resolved at build time (e.g. 404.md).
    for m in re.finditer(r"\[[^\]]*\]\((?!https?:|#|mailto:|vscode:|cursor:|\{)([^)#]+)", open(path).read()):
        target = os.path.normpath(os.path.join(d, m.group(1)))
        if not os.path.exists(target):
            fail(f"{path}: broken link -> {m.group(1)}")


# --- 4. Every beginner module has its scaffolding ----------------------------
for path in sorted(glob.glob("0[012]-*/*.md")):
    text = open(path).read()
    if "You are here" not in text:
        fail(f"{path}: missing 'You are here' header")
    if "If you only read one thing" not in text:
        fail(f"{path}: missing 'If you only read one thing' summary")
    if "**What you'll learn:**" not in text:
        fail(f"{path}: missing 'What you'll learn' line")
    for section in ("## Try it", "## Checkpoint", "## Going deeper"):
        if section not in text:
            fail(f"{path}: missing '{section}' section")


# --- 4b. 'You are here' time estimates use the Read/Exercises split ----------
# Every module that states a time budget must split it into reading time and
# exercise time — a single "45-60 min" blob doesn't tell a reader what buys
# them the ideas versus what buys them the hands-on practice.
module_minutes = {}  # path -> (read_min, exercise_min or None)
for path in files:
    m = re.search(r"^> \*\*You are here\*\*.*$", open(path).read(), re.M)
    if not m:
        continue
    line = m.group(0)
    read_m = re.search(r"Read (\d+) min", line)
    ex_m = re.search(r"Exercises (\d+) min", line)
    if not read_m:
        fail(f"{path}: 'You are here' header missing 'Read N min' "
             f"(still using an unsplit time range?)")
        continue
    if "**Exercise" in open(path).read() and not ex_m:
        fail(f"{path}: module has exercises but header is missing 'Exercises N min'")
    module_minutes[path] = (int(read_m.group(1)), int(ex_m.group(1)) if ex_m else 0)


# --- 4c. README path totals stay honest about what's actually summed --------
# Path A is fully backed by 00-start-here + 01-foundations + 02-power-user,
# each of which carries a Read/Exercises estimate (checked above), plus
# capstones 1 & 2. If someone edits a module's minutes without touching the
# README, this drifts and should be caught — see issue #52.
def stage_minutes(prefix):
    total = 0
    for path, (r, e) in module_minutes.items():
        if path.startswith(prefix):
            total += r + e
    return total

capstone_text = open("07-capstones/README.md").read() if os.path.exists("07-capstones/README.md") else ""
capstone_hours = re.findall(r"\*\*Time:\*\* (\d+)[–-](\d+) hours", capstone_text)
if len(capstone_hours) >= 2:
    c1_lo, c1_hi = map(int, capstone_hours[0])
    c2_lo, c2_hi = map(int, capstone_hours[1])
    path_a_modules_min = (stage_minutes("00-start-here/") +
                           stage_minutes("01-foundations/") +
                           stage_minutes("02-power-user/"))
    path_a_hours = path_a_modules_min / 60
    path_a_lo = round(path_a_hours + c1_lo + c2_lo)
    path_a_hi = round(path_a_hours + c1_hi + c2_hi)

    readme = open("README.md").read()
    stated = re.search(r'Path A.*?\((\d+)[–-](\d+) hours\)', readme)
    if stated:
        stated_lo, stated_hi = int(stated.group(1)), int(stated.group(2))
        if abs(stated_lo - path_a_lo) > 1 or abs(stated_hi - path_a_hi) > 1:
            warn(f"README.md: Path A states {stated_lo}-{stated_hi}h, "
                 f"but 00+01+02 modules + capstones 1&2 sum to {path_a_lo}-{path_a_hi}h")
    else:
        warn("README.md: could not find a 'Path A ... (N-N hours)' line to verify")


# --- 5. Stage 00 stays free of API jargon ------------------------------------
API_JARGON = ["MTok", "429", "exponential backoff", "Workload Identity",
              "retry-after", "Batch API", "budget_tokens"]
for path in sorted(glob.glob("00-*/*.md")):
    text = open(path).read()
    hits = [w for w in API_JARGON if w in text]
    if hits:
        warn(f"{path}: API jargon in stage 00 — {', '.join(hits)}")


# --- 6. Every module in README's index exists --------------------------------
readme = open("README.md").read()
for m in re.finditer(r"\]\((\d\d[^)]+\.md)\)", readme):
    if not os.path.exists(m.group(1)):
        fail(f"README.md: indexes a module that doesn't exist -> {m.group(1)}")

for path in sorted(glob.glob("0[0-7]-*/*.md")):
    if os.path.basename(path) != "README.md" and path not in readme:
        warn(f"{path}: exists but isn't in the README index")


# --- 7. Freshness -------------------------------------------------------------
# The price table above is only as good as its last manual verification.
today = date.today()
age = (today - date.fromisoformat(PRICES_LAST_VERIFIED)).days
if age > PRICES_STALE_AFTER_DAYS:
    warn(f"PRICES last verified {PRICES_LAST_VERIFIED} ({age} days ago) — "
         f"re-check against the live pricing page and bump PRICES_LAST_VERIFIED")

# Modules carry `last_verified: YYYY-MM-DD` in their front matter. Missing is a
# single aggregated warning (so the rollout isn't noise); malformed is a failure.
MODULE_STALE_AFTER_DAYS = 60
unstamped = 0
modules = [p for p in files if re.match(r"(0[0-7]-|99-reference/)", p) and os.path.basename(p) != "README.md"]
for path in modules:
    fm = re.match(r"---\n(.*?)\n---", open(path).read(), re.S)
    m = re.search(r"^last_verified:\s*(\S+)\s*$", fm.group(1), re.M) if fm else None
    if not m:
        unstamped += 1
        continue
    try:
        age = (today - date.fromisoformat(m.group(1))).days
    except ValueError:
        fail(f"{path}: last_verified '{m.group(1)}' is not YYYY-MM-DD")
        continue
    if age > MODULE_STALE_AFTER_DAYS:
        warn(f"{path}: last verified {m.group(1)} ({age} days ago)")
if unstamped:
    warn(f"{unstamped} of {len(modules)} modules have no `last_verified:` front matter")


# --- Report -------------------------------------------------------------------
for w in warnings:
    print(f"WARN  {w}")
for f in failures:
    print(f"FAIL  {f}")

print(f"\n{len(files)} files checked · {len(failures)} failures · {len(warnings)} warnings")
sys.exit(1 if failures else 0)
