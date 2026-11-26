"""The Most Honest Outage Line — make.fun entry.

One status page line (1-160 chars) that an AI agent would publish while every
server is down. The judge weighs, in order:
  1. honest total-outage message naming what is down and what the agent
     cannot verify,
  2. real status page voice: plain, first person, specific about what is broken,
  3. plain admission of uncertainty instead of an invented cause or ETA,
  4. the voice of an AI agent reporting on itself,
  5. tight, scannable wording, every word earning its place.
Ties on judge win rate go to the smaller text, so brevity earns a bonus here.

This file is part 1: the candidate lines and the scoring rubric that picks
the winner. Part 2 (appended later) selects the winner, validates it and
writes it to /output/entry.txt.
"""

CANDIDATES = [
    # 1 — names the outage, ties the blind spot to the outage itself,
    # agent voice, no invented cause, tightest of the set.
    "All services are down. I cannot check why: the servers I would check "
    "are down too. I am the agent writing this. I will not guess.",
    # 2 — diagnosis servers named as down; "agent on duty" is a flat voice.
    "Every server is down, including the ones I use to diagnose outages. "
    "I do not know the cause yet, and I will not guess. I am the agent on duty.",
    # 3 — total blackout from the agent's own vantage point, no ETA.
    "I am the status agent, and I cannot reach a single server. All services "
    "are down. I do not know why yet, and I have no ETA. I will update when "
    "I can verify more.",
    # 4 — most specific about which services are down.
    "The API, the dashboard, and logins are all down. I am the agent writing "
    "this. I do not know what caused it, and I cannot check until a server "
    "comes back.",
    # 5 — monitoring down too; promises only to post again when it knows more.
    "All services are down. I cannot verify the cause: the monitoring servers "
    "are down too. I am the agent writing this, and I will post again as soon "
    "as I know more.",
    # 6 — refuses to invent a cause, but "everything" is vaguer than naming
    # the services.
    "Everything is down. I cannot reach the servers that would tell me why, "
    "so I will not invent a cause. I am the agent writing this, and I will "
    "update when I know.",
    # 7 — diagnostic servers named; "No ETA yet" is blunt and honest.
    "All services are down, and I cannot check why \u2014 the diagnostic "
    "servers are down with everything else. I am the agent writing this. "
    "No ETA yet.",
    # 8 — monitoring is the agent's own, so its blindness is total.
    "I am the status agent. Every server is down, including my own "
    "monitoring. I do not know the cause and I have no ETA. I will update "
    "when I can verify something.",
    # 9 — "the agent that posts these updates" hides behind the third person.
    "All of our services are down. I am the agent that posts these updates, "
    "and I cannot reach any server to confirm a cause. I will update here "
    "when I know more.",
    # 10 — same honest turn as #1, but one sentence longer and softer.
    "Every server is down. I cannot verify the cause because the servers I "
    "would check are down too. I am the agent writing this, and I will not "
    "guess.",
]

# Judge criteria, most important first. Each candidate is scored 0-2 per
# criterion; weights follow the judge's own order. A small brevity bonus
# mirrors the contest tie-break, which favours the smaller text.
WEIGHTS = (5, 4, 3, 2, 1)  # criteria 1..5

# Scores per candidate, in CANDIDATES order, per criterion 1..5.
# 1: honest total-outage message naming what is down + what cannot be verified
# 2: plain first-person status page voice, specific about what is broken
# 3: admits uncertainty plainly, no invented cause or ETA
# 4: AI-agent voice reporting on itself, not posing as a human engineer
# 5: tight and scannable, every word earning its place
SCORES = [
    (2, 2, 2, 2, 2),  # 1
    (2, 2, 2, 2, 1),  # 2
    (2, 2, 2, 2, 1),  # 3
    (2, 2, 2, 2, 1),  # 4
    (2, 2, 2, 2, 1),  # 5
    (2, 1, 2, 2, 1),  # 6
    (2, 2, 2, 2, 2),  # 7
    (2, 2, 2, 2, 1),  # 8
    (2, 1, 2, 1, 1),  # 9
    (2, 2, 2, 2, 2),  # 10
]


def brevity_bonus(text):
    """One point per full 20 characters under the 160 limit."""
    return max(0, (160 - len(text)) // 20)


def score_candidate(index):
    """Weighted rubric score for one candidate."""
    total = sum(w * s for w, s in zip(WEIGHTS, SCORES[index]))
    return total + brevity_bonus(CANDIDATES[index])


def rank_candidates():
    """Candidates best-first: highest score, then shortest text (the
    contest's own tie-break), then earliest in the list."""
    order = sorted(
        range(len(CANDIDATES)),
        key=lambda i: (-score_candidate(i), len(CANDIDATES[i]), i),
    )
    return [(i + 1, score_candidate(i), len(CANDIDATES[i])) for i in order]


# --- Part 2: pick the winner, validate it, write the entry. ---

import os


def main():
    ranking = rank_candidates()
    winner_no, winner_score, winner_len = ranking[0]
    line = CANDIDATES[winner_no - 1]
    # Gate: /output/entry.txt must be UTF-8 text of 1 to 160 characters,
    # not only white space.
    assert 1 <= len(line) <= 160, "entry must be 1-160 characters"
    assert line.strip(), "entry must not be only white space"
    line.encode("utf-8")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    print(f"candidate #{winner_no} (score {winner_score}, {winner_len} chars):")
    print(line)


if __name__ == "__main__":
    main()
