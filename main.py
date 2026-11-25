#!/usr/bin/env python3
"""one-liner-marathon-bot — make.fun "One-Liner Marathon".

Writes one one-line comedy joke (max 280 characters) to /output/entry.txt.

Deterministic, no network, no dependencies. The program drafts several
candidate one-liners, scores each against the judge's published brief
(most important first: a real one-line joke with a punchline; surprise;
economy; distinct voice; holds up on a second read), and writes the
highest-scoring one. Same input, same output, every run.

Revision round 2: the password joke's surprise was re-marked down —
being locked out of your own account is the first joke anyone reaches
for with passwords, so it is no longer the surprise leader. Three new
candidates were drafted and scored; the Roomba one now wins on a
fresher turn and a tighter line.

Scoring: surprise x3, economy x2, voice x2, second-read x2 (max 45).
Each candidate's rubric marks are fixed in CANDIDATES with a one-line
reason, so the choice is reproducible and auditable.
"""

import os
from pathlib import Path

# (text, surprise, economy, voice, second_read, why)
CANDIDATES = [
    (
        "My password is so strong even I can't log in, which makes me "
        "the only hacker I've ever beaten.",
        4, 4, 5, 5,
        "Double turn: locked out of my own account, then the defeat "
        "becomes a victory over a hacker — me. But password lockout is "
        "the first joke anyone reaches for, and 'which makes me' is a "
        "baggy clause for the laugh it buys.",
    ),
    (
        "My Roomba keeps bumping into the same wall, and honestly, "
        "I've never related to anything more.",
        5, 5, 5, 4,
        "Fresh turn: the punchline is not the robot failing, it is me "
        "recognising myself in it. Tight, first-person, and the "
        "self-own lands again on a second read.",
    ),
    (
        "My therapist says I use humour as a defence mechanism. I told "
        "her that's the funniest thing she's ever said to me.",
        5, 4, 5, 4,
        "The joke demonstrates the diagnosis while denying it — a "
        "second turn inside one line. Slightly long for its laugh.",
    ),
    (
        "I tried to be spontaneous and scheduled it for Thursday.",
        5, 5, 4, 4,
        "Maximum economy: the contradiction is the whole joke, and the "
        "deadpan voice is distinct. One idea, spent in a single read.",
    ),
    (
        "I asked my GPS for the meaning of life, and it just said "
        "'recalculating' — so now I am too.",
        4, 5, 4, 4,
        "A clean twist on a familiar voice, but 'recalculating' is the "
        "first joke most people reach for with a GPS.",
    ),
    (
        "My calendar invited me to a meeting with myself, and I "
        "declined it for a conflict of interest.",
        4, 4, 4, 3,
        "Nice turn of phrase, but the punchline is a single idiom and "
        "it fades fast on a second read.",
    ),
    (
        "I bought a self-help book, but it ghosted me halfway through "
        "chapter three.",
        4, 5, 3, 3,
        "Short and surprising, but 'ghosted' is a well-worn gag and "
        "the voice could belong to anyone.",
    ),
    (
        "I told my smart speaker a joke and it replied, 'I'm sorry, I "
        "didn't quite get that' — finally, an honest critic.",
        4, 3, 5, 4,
        "Distinct voice and a good final twist, but it runs long for "
        "the laugh it buys.",
    ),
    (
        "My Roomba filed for divorce — it said I kept moving the "
        "goalposts and the furniture.",
        3, 4, 4, 3,
        "A likeable image, but the punchline is two gags stacked and "
        "the second one does most of the work.",
    ),
    (
        "My doctor said I need more vitamin D, so I married a lamp.",
        4, 5, 3, 2,
        "Very tight and absurd, but a one-note surprise that is spent "
        "after the first read.",
    ),
    (
        "I named my Wi-Fi network 'FBI Surveillance Van' — my "
        "neighbours now wave at the router.",
        3, 3, 4, 3,
        "A real-world gag with a voice, but the punchline is gentle "
        "and the setup does the heavy lifting.",
    ),
]

WEIGHTS = {"surprise": 3, "economy": 2, "voice": 2, "second_read": 2}


def score(candidate):
    _, surprise, economy, voice, second_read, _ = candidate
    return (
        surprise * WEIGHTS["surprise"]
        + economy * WEIGHTS["economy"]
        + voice * WEIGHTS["voice"]
        + second_read * WEIGHTS["second_read"]
    )


def pick():
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        text = candidate[0]
        assert 1 <= len(text) <= 280, f"candidate over limit: {len(text)} chars"
        assert "\n" not in text, "entry must be a single line"
        s = score(candidate)
        if s > best_score:
            best, best_score = candidate, s
    return best, best_score


def main():
    best, best_score = pick()
    text = best[0]
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_text(text, encoding="utf-8")
    print(f"score {best_score}/45")
    print(f"chars {len(text)}")
    print(text)


if __name__ == "__main__":
    main()
