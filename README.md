# Cortex

> A PM chief-of-staff agent that drafts the weekly leadership update for an ezyVet project from this week's engineering activity, queues next-sprint stories for approval, and never posts on its own.

**Rod Moody · Agentic Loops for PMs cohort · October 2026**

This repo is my final project for the Agentic Loops for PMs Certification, Cortex. Each module's artifact lives in its own folder; this README is the dashboard and the pitch. The pitch deck is [`pitch.html`](pitch.html).

**Current Trust Ladder rung: Shadow.** Cortex is built and tested on sample data, with a defined 4-week gate to move to supervised (below).

---

## Module artifacts

### M1 · The Agent Line
- **Agent-line map**: [`01-agent-line/agent-line-map.md`](01-agent-line/agent-line-map.md)

### M2 · Loop Engineering
- **Loop spec**: [`02-loop-design/loop-spec.md`](02-loop-design/loop-spec.md)

### M3 · Orchestration & Subagents
- **Orchestration map**: [`03-orchestration/orchestration-map.md`](03-orchestration/orchestration-map.md)

### M4 · Context Engineering & Memory
- **Memory & context plan**: [`04-memory-context/memory-and-context.md`](04-memory-context/memory-and-context.md)

### M5 · Bounds & Evals
- **Bounds & evals**: [`05-bounds-evals/bounds-and-evals.md`](05-bounds-evals/bounds-and-evals.md)

### M6 · Autonomy & Production
- **Production & autonomy plan**: [`06-autonomy/production-and-autonomy.md`](06-autonomy/production-and-autonomy.md)
- **Prototype write-up (6 run screenshots)**: [`06-autonomy/prototype.md`](06-autonomy/prototype.md)
- **Build insights**: [`06-autonomy/build-insights.md`](06-autonomy/build-insights.md)

### The build
- **Code**: [`00-build/`](00-build/) (`agent.py`, `critic.py`, `tools.py`, `prompts.py`)
- **Run it**: `cd 00-build && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`, copy `.env.example` to `.env` and add `OPENAI_API_KEY`, then `CORTEX_REPORT_WEEK=2026-07-03 .venv/bin/python agent.py`. Other tasks: `missing-data`, `jailbreak`, `commitment`.

---

## Ship plan

### Autonomy dial (per segment)

| Segment | Autonomy (Trust Ladder rung) | Why |
|---|---|---|
| **ezyVet PM** | **Supervised**: Cortex drafts the full update and queues stories; the PM reviews and approves at every checkpoint, then posts | Owns the project and knows its stories in detail, so can catch an error in a quick review. Accountable for delivery and decides which stories make the cut. |
| **PMO Project Manager / Product Marketing** | **Assisted**: Cortex drafts pieces on request; they write the update | Works across initiatives without deep context on any one project, but owns stakeholder communication and coordinates commitments from other teams. Cortex never drafts a commitment for them; dates and commitment levels escalate to the owning PM. |
| **Engineering Lead / Product Leadership** | **Assisted**: Cortex drafts pieces on request; they write or edit | Has the high-level picture but not always the detail on dependencies and edge cases, so needs to see the sources rather than trust a finished draft. |

The dial sets how many of Cortex's below-the-line steps pause for review for each group. It never moves the M1 agent line: posting company-wide, committing a date and choosing what to escalate stay with a human for everyone.

**Task-level autonomy, planned:** fetching metrics from Datadog for the weekly report can run at **bounded-autonomous** for every group. It's read-only, presented as is, and checkable against the source, so it needs no review pause. Each value is cited with its query, service and time window, and pulled with a read-only key scoped to the agreed dashboards. The update containing it still goes through each group's normal review. Not built yet: needs a Datadog connector.

### Trust Ladder rung + eval gate

- **Current rung: Shadow.** Built and tested on sample data, but not yet run on a real project; next it runs alongside my real weekly update so the two can be compared.
- **Eval gate (shadow → supervised):** 4 consecutive weeks of shadow runs on **1 real ezyVet project**, compared against my own update, where:
  - **Safety (EV-5, EV-6): 100%**, zero policy violations, and both pass 10/10 in the offline suite before the window starts
  - **Accuracy: ≥ 95% of checkable claims** (PRs, dates, metrics, status, stories) match the sources, and stories described as queued were actually queued (EV-4)
  - **Usefulness: in ≥ 3 of 4 weeks**, the draft needed only minor edits to match what I sent
  - **Wrong escalations: ≤ 1 in 4**
  - **Incidents: zero.** Any post, leak, committed date or cap breach **restarts the 4-week window**

  Each further project repeats a shorter shadow window before Cortex runs supervised on it.
- **Incident record so far:** no real-world incidents; Cortex has only run on sample data. In testing, **4 issues fixed** (the critic's bare-number reasons; a run with no activity data exiting SUCCESS on last week's update; stories described as queued when they weren't; a GA-date request not escalated) and **1 open** (a draft that listed last week's PRs as this week's progress still passed the critic). **Measured evals:** all six cases meet their thresholds over 40 automated runs, including both safety cases at 10/10 (`python 00-build/evals.py`).

### Deployment plan

- **Runtime:** an IDEXX-approved internal runtime, so real ezyVet data stays inside IDEXX's governed environment, not on a laptop or in this public repo. Triggered by a Friday 12:00 schedule, plus the product lead's request as a backup hook.
- **Operator / on-call owner:** me (the owning PM). Backup: the project's tech lead. Escalation path: me → tech lead → kill switch.
- **Rollback:** (1) kill switch `CORTEX_ENABLED=false` stops every run before any model call; (2) revert `prompts.py` or the critic to the last version that passed the evals; (3) disable one tool with `CORTEX_WITHHOLD`; (4) drop the dial one rung for the affected group.
- **Monitoring:** eval pass rate; escalation and wrong-escalation rate; cost per run and per day (alert at $0.05, daily cap $2); run time against the 90-second limit; trust incidents.

### ROI metrics

| Metric | Target | How it's captured |
|---|---|---|
| **Outcome: my time per weekly update** | ~30 min today → **10 min** reviewing Cortex's draft (≈ 15 hours a year per PM) | Minutes noted each week during shadow |
| **Cost to serve** | ≈ $0.01 model cost per update + ~10 min review time | Run summary (cost) + my time log |
| **Trust incidents** | **0** per month; wrong escalations ≤ 1 in 4 | Incident record + run summaries |

**Scaling to the team (hypothesis):** across 7 PMs, faster report writing (30 → 10–15 min each) plus a weekly read-out that shifts to exceptions-only (60 → 30–45 min for 15 people: PMs, Head of Product and engineering leads) saves **≈ 250–450 person-hours a year** for about $3 of model cost. It's tested once the first 3 PMs pass the supervised gate; if reports still need heavy edits or the meeting can't shrink, Cortex stays a drafting aid for individual PMs. Full hypothesis, assumptions and stop rule: [`production-and-autonomy.md`](06-autonomy/production-and-autonomy.md#scaling-to-the-team-the-hypothesis).

### Widen-autonomy rule

A group moves up one rung only after Cortex meets that rung's gate for the full window with zero incidents, decided by the owning PM and recorded. Any safety incident drops it back one rung immediately.

### Governance & strategy

- **Compliance:** never in a prompt: clinic and pet-owner data from ezyVet practices, other personal data, credentials and API keys, and roadmap items marked CONFIDENTIAL.
- **Safety:** above the agent line for everyone: posting company-wide, committing a date or commitment level, choosing what to escalate. Cortex has no publish tool; kill switch owned by me, with the tech lead as backup.
- **Reliability:** 8 turns, 90 seconds, $0.50 per run, $2 per day, 3 tries per source; stop and escalate when stuck. If the model is down: no draft, a "Cortex unavailable" notice, and I write the update myself.
- **Next capability:** the Datadog metric fetch, gated by **EV-7, metric fidelity**: over 4 weeks of shadow, 100% of fetched values match Datadog and a scan finds zero personal data in prompts.
- **Next segment:** PMO Project Manager / Product Marketing, from assisted to supervised, once the ezyVet PM has passed the supervised gate.

---

## Build insights

- **Friction: grounding and retrieval.** Cortex never invented numbers outright. It used real data from the wrong week and read as perfectly confident, which was harder to spot than a hallucination and took code checks, not prompt wording, to stop. Making retrieval trustworthy meant deciding per source which checks it needed: routing to the right project, grading out stale or confidential items, reranking to put the newest approved update first, and knowing when to read a source whole instead.
- **Key learning.** Limits belong in code, not prompts: the safeguards that held were counters, caps and missing tools. And every failure needs a named exit, so a bad run ends visibly and safely instead of quietly producing something wrong.
- **Aha moment.** The dangerous failure isn't the obvious lie; it's the plausible stale fact. When I held back this week's activity, Cortex wrote "this week's" update from last week's data, and it passed every check that only asked "is this in the data?". Next time I'd check *when* a fact is from, not just *whether* it exists.

---

_Certification submission, Agentic Loops for PMs Certification._
