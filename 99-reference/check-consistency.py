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

# --- Single source of truth. Update here when prices change. ------------------
PRICES = {          # model            (input $/MTok, output $/MTok)
    "Fable 5":      (10, 50),
    "Opus 5":       (5, 25),
    "Sonnet 5":     (3, 15),
    "Haiku 4.5":    (1, 5),
}
CHEAPEST = "Haiku 4.5"

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
# Any "N× cheaper than X" must match the table.
base_in = PRICES[CHEAPEST][0]
valid_ratios = {m: p[0] / base_in for m, p in PRICES.items()}

for path in files:
    text = open(path).read()
    for m in re.finditer(r"(\d+)×\s*cheaper than (\w+)", text):
        claimed, model = int(m.group(1)), m.group(2)
        match = next((k for k in PRICES if k.split()[0].lower() == model.lower()), None)
        if match is None:
            continue
        actual = valid_ratios[match]
        if abs(claimed - actual) > 0.01:
            fail(f"{path}: claims '{m.group(0)}' but table says {actual:.0f}×")


# --- 2. Price tables agree with each other -----------------------------------
for path in files:
    for line in open(path):
        for model, (inp, out) in PRICES.items():
            if f"Claude {model}" in line and "$" in line:
                found = re.findall(r"\$(\d+)", line)
                if len(found) >= 2 and (int(found[0]), int(found[1])) != (inp, out):
                    # Intro/promotional pricing is called out explicitly; allow it.
                    if "intro" not in line.lower():
                        fail(f"{path}: {model} priced ${found[0]}/${found[1]}, "
                             f"table says ${inp}/${out}")


# --- 3. Internal links resolve ------------------------------------------------
for path in files:
    d = os.path.dirname(path)
    for m in re.finditer(r"\[[^\]]*\]\((?!https?:|#|mailto:|vscode:|cursor:)([^)#]+)", open(path).read()):
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


# --- 7. No stray http:// links in markdown content ----------------------------
# localhost/example placeholders in config samples are fine; real links must be https.
NON_URL_HOSTS = ("localhost", "127.0.0.1", "0.0.0.0", "example.com")
for path in files:
    for lineno, line in enumerate(open(path), start=1):
        for m in re.finditer(r"http://[^\s\"'\)\]]+", line):
            url = m.group(0)
            host = url[len("http://"):].split("/")[0].split(":")[0]
            if host in NON_URL_HOSTS:
                continue
            fail(f"{path}:{lineno}: insecure http:// link -> {url}")


# --- Report -------------------------------------------------------------------
for w in warnings:
    print(f"WARN  {w}")
for f in failures:
    print(f"FAIL  {f}")

print(f"\n{len(files)} files checked · {len(failures)} failures · {len(warnings)} warnings")
sys.exit(1 if failures else 0)
