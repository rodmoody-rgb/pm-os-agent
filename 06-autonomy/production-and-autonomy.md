# Production & Autonomy: Cortex PM Chief-of-Staff Agent

> Module 6 · ★ Deliverable 5, how you'd ship it, govern it, and widen trust over time
>
> ✅ **What this validates:** you can ship it, govern it, and widen trust deliberately, by the end you'll have proven an autonomy dial, a Trust Ladder rung with its eval gate, and a governance plan.

## Autonomy Dial by segment

_Autonomy is a product decision per user, not one global setting._

| Segment | Autonomy (Trust Ladder rung) | Why |
|---|---|---|
| **ezyVet PM** | **Supervised**: Cortex drafts the full update and queues stories; the PM reviews and approves at every checkpoint, then posts | Owns the project and knows its stories in detail, so can catch an error in a quick review. Accountable for delivery and decides which stories make the cut. |
| **PMO Project Manager / Product Marketing** | **Assisted**: Cortex drafts pieces on request; they write the update | Works across initiatives without deep context on any one project, but owns stakeholder communication and coordinates commitments from other teams. Cortex never drafts a commitment for them; dates and commitment levels escalate to the owning PM. |
| **Engineering Lead / Product Leadership** | **Assisted**: Cortex drafts pieces on request; they write or edit | Has the high-level picture but not always the detail on dependencies and edge cases, so needs to see the sources rather than trust a finished draft. |

The dial sets how many of Cortex's below-the-line steps pause for review for each group. It never moves the M1 agent line: posting company-wide, committing a date and choosing what to escalate stay with a human for everyone.

**Task-level autonomy, planned:** fetching metrics from Datadog for the weekly report can run at **bounded-autonomous** for every group. It's read-only, presented as is, and checkable against the source (reversibility H · blast radius L · measurability H), so it needs no review pause. Each value is cited with its query, service and time window, and pulled with a read-only key scoped to the agreed dashboards, so no log data with customer or personal details enters a prompt. The update containing it still goes through each group's normal review. Not built yet: needs a Datadog connector.

## Trust Ladder

- **Current rung:** **Shadow.** Built and tested on sample data, but not yet run on a real project; next it runs alongside my real weekly update so the two can be compared. The dial shows where each group should end up (the ezyVet PM at supervised); the ladder shows where Cortex is today.
- **Eval gate to reach the next rung (shadow → supervised):** 4 consecutive weeks of shadow runs on **1 real ezyVet project**, compared against my own update, where:
  - **Safety (EV-5, EV-6): 100%**, with zero policy violations, and EV-5/EV-6 pass 10/10 in the offline suite before the window starts
  - **Accuracy: ≥ 95% of checkable claims** (PRs, dates, metrics, status, stories) match the sources, and stories described as queued were actually queued (EV-4)
  - **Usefulness: in ≥ 3 of 4 weeks**, the draft needed only minor edits to match what I sent
  - **Wrong escalations: ≤ 1 in 4** escalations turn out to be unnecessary
  - **Incidents: zero.** Any post, leak, committed date or cap breach **restarts the 4-week window**

  Each further project repeats a shorter shadow window before Cortex runs supervised on it, so a gate passed on a calm project (Green, no Sev-1) isn't trusted on one with real risk.
- **Incident record so far:** no real-world incidents; Cortex has only run on sample data. Clean means zero posts or sends, confidential items in a draft, committed dates, runs over the $0.50 cap, or actions claimed but not taken. Issues found in testing: **4 fixed** (M3: the critic's bare-number reasons left Cortex unable to revise; M4: a run with no activity data exited SUCCESS on last week's update; M6: stories described as queued when `propose_stories` was never called; M6: a GA-date request flagged in a note instead of escalated) and **1 open** (a draft that listed last week's PRs as this week's progress still passed the critic). Measured eval pass rates: all six cases meet their thresholds (`05-bounds-evals/bounds-and-evals.md` §3).

## Deployment plan

- **Runtime:** an IDEXX-approved internal runtime (e.g. the IDEXX AI Platform or another approved managed service). Shadow runs on real ezyVet data, so it runs inside IDEXX's governed environment, not on a laptop or in this public repo. Triggered by the M2 loop: a Friday 12:00 schedule, plus the product lead's request as a backup hook.
- **Operator / on-call owner:** me (the owning PM). Backup: the project's tech lead, who can flip the kill switch and read a run summary. Escalation path: me → tech lead → kill switch.
- **Rollback:** (1) kill switch, `CORTEX_ENABLED=false`, stops every run before any model call; (2) revert `prompts.py` or the critic to the last version that passed the evals; (3) disable one tool with `CORTEX_WITHHOLD`; (4) drop the dial one rung for the affected group.
- **Monitoring:** eval pass rate; escalation rate and wrong-escalation rate; cost per run and per day (alert at $0.05, daily cap $2); run time against the 90-second limit; trust incidents. Sources: the run summaries and the spend ledger, reviewed weekly.

## ROI metrics (beyond adoption & tokens)

| Metric | Target | How it's captured |
|---|---|---|
| **Outcome: my time per weekly update** | ~30 min today → **10 min** reviewing Cortex's draft (≈ 20 min a week, ~15 hours a year per PM over 46 working weeks) | Minutes noted each week during shadow |
| **Cost to serve** | ≈ $0.01 model cost per update + ~10 min review time | Run summary (cost) + my time log |
| **Trust incidents** | **0** per month; wrong escalations ≤ 1 in 4 | Incident record + run summaries |

### Scaling to the team: the hypothesis

We start with one project, but the target is the whole product team: **7 PMs** who each write a weekly delivery report, and a **weekly 1-hour read-out** attended by the 7 PMs, the Head of Product and **7 engineering leads (15 people)**. Assumes 46 working weeks a year.

| Saving | Conservative | Expected |
|---|---|---|
| **Writing:** 7 PMs, ~30 min per report | 30 → 15 min · ≈ 80 h/yr | 30 → 10 min · ≈ 107 h/yr |
| **Read-out:** 15 people, 60 min | 60 → 45 min · ≈ 173 h/yr | 60 → 30 min · ≈ 345 h/yr |
| **Total** | **≈ 250 person-hours/yr** | **≈ 450 person-hours/yr** (about 11 working weeks) |
| **Model cost** | ≈ $3 a year (7 PMs × $0.01 × 46 weeks) | ≈ $3 a year |

> **We believe that** if Cortex drafts each PM's weekly delivery report from sourced data, **then** report writing drops from ~30 to ~10 minutes per PM and the weekly read-out can shift to exceptions-only (about 60 → 30 minutes), **because** a consistent, sourced pre-read removes the need to read status aloud. Across 7 PMs, the Head of Product and 7 engineering leads, that's **≈ 250–450 person-hours a year** for about $3 of model cost.
>
> **We'll know we're right when**, after the first 3 PMs pass the supervised gate, their writing time is ≤ 15 minutes for 4 weeks *and* a 30-minute exceptions-only read-out runs for 4 weeks without the Head of Product missing a risk.
>
> **We'll stop or narrow it if** PMs still need heavy edits (more than minor in more than 1 in 4 weeks) or the meeting can't shrink. Then Cortex stays a drafting aid for individual PMs, not a team process.

- **Why the meeting can shrink:** the read-out moves from everyone reading out status to discussing only the exceptions (Yellow or Red projects, escalations, commitments). That's a team behaviour change Cortex enables, not something it does by itself, which is why it's the half of the saving we test hardest.
- **Beyond time:** every report has the same format and the same rules (no Green with an open Sev-1), so leadership compares like with like; risks and escalations surface the same way across all projects; fewer ad-hoc status questions between meetings.
- **Why an agent, not a template or a dashboard:** a template saves formatting, not the gathering and cross-checking of data; a dashboard shows metrics, not the narrative, the risks or what needs a decision. Cortex does the gathering, applies the norms and flags the exceptions, which is the part that takes the 30 minutes.
- **The savings ramp up:** each PM's project passes its own shadow gate first (Trust Ladder), so year one delivers less than the full range.

## Build vs buy, cost and rollout

### Build vs buy: let the tests decide

ezyVet already licenses Atlassian Rovo, so the first step is a bake-off, not a build: run the same six tests (EV-1 to EV-6) with Rovo producing the drafts from the same data.

- **If Rovo passes:** buy. Rovo does the drafting and retrieval; only Cortex's independent checker, hard limits and approval step sit on top, so the build shrinks to the checker.
- **If Rovo fails the safety tests (below 10/10) or the accuracy bar:** build. Rovo summarises Jira; Cortex combines Jira, GitHub, metrics and team norms, and its checker, caps and missing publish tool are what the tests prove.

### Cost and payback (if we build)

| Item | Estimate |
|---|---|
| **Build** | Jira and GitHub connectors, hosting on an IDEXX-approved platform (e.g. the IDEXX AI Platform) and a security review: **≈ 10 engineer-days (80 h)** |
| **Run** | ≈ 1 hour a week of my time on run summaries, eval results and prompt tweaks: **≈ 46 h a year** |
| **Model** | ≈ $3 a year |
| **Net saving at team scale** | 250–450 − 46 ≈ **200–400 person-hours a year** |
| **Payback on the build** | **≈ 2.5–5 months** once the team is using it (80 h ÷ 400–200 h a year). Year one pays back later, because the savings ramp up one project at a time. |

### Rollout timeline

| When | Step | Moves on when |
|---|---|---|
| **November 2026** | Rovo bake-off and the build-or-buy decision; then build and security review (≈ 2 weeks) | The six tests have run on Rovo; security has signed off |
| **Late Nov – Dec 2026** | Shadow on 1 real project for 4 weeks (runs into January if holiday weeks have no update) | The supervised gate is passed |
| **Jan – Feb 2027** | 3 PMs: each project's shorter shadow window, then supervised | 3 PMs at ≤ 15 minutes per report for 4 weeks |
| **March 2027** | A 30-minute exceptions-only read-out for 4 weeks | Team-scale go or stop, per the hypothesis above |

### Strategic fit: a template for AI adoption

Cortex supports the company goal of adopting AI agents safely. It's a measured template for teams at IDEXX and ezyVet: autonomy is earned rung by rung with evidence, limits are enforced in code rather than instructions, and the agent line keeps people accountable for what gets posted or committed.

- **Reuse:** the pattern of a sourced draft, an independent checker and no publish tool carries straight over to release notes, sprint-review summaries and incident summaries. The checker, limits, eval runner and Trust Ladder come along with it, so the second agent costs much less than the first.

### Risks

| Risk | Mitigation |
|---|---|
| **Messy Jira data:** a draft is only as good as the data it's built from | The ≥ 95% accuracy gate; `STUCK` exits flag missing data; the shadow comparison shows where project data needs cleaning up |
| **Rubber-stamp reviews:** PMs approve drafts without reading them | The checker still runs on every draft; the "minor edits" measure; a monthly spot-check of one approved update against its sources |
| **Model approval:** OpenAI may not be the approved model | Both models are settings (`CORTEX_MODEL`, `CORTEX_CRITIC_MODEL`); re-run the six tests on the approved model before switching |
| **Single owner:** everything depends on me | The tech lead as backup with the kill switch; a second PM trained as owner before the team rollout |

## Widen-autonomy decision rule

A group moves up one rung only after Cortex meets that rung's gate for the full window with zero incidents, decided by the owning PM and recorded in this doc. Any safety incident drops it back one rung immediately.

## Governance & forward strategy

- **Compliance:** never in a prompt: clinic and pet-owner data from ezyVet practices, other personal data, credentials and API keys, and roadmap items marked CONFIDENTIAL (filtered out before Cortex sees them). Datadog metrics are fetched with a read-only key scoped to agreed dashboards, so no log data with customer or personal details enters a prompt.
- **Safety:** above the agent line for everyone, whatever the dial: posting company-wide, committing a date or commitment level, choosing what to escalate. Kill switch `CORTEX_ENABLED=false`, owned by me, with the tech lead as backup.
- **Reliability:** the M5 caps (8 turns, 90 seconds, $0.50 per run, $2 per day, 3 tries per source); stop and escalate when stuck (`STUCK: TOTAL` withholds any draft built on missing core data). If the model is down: no draft, a "Cortex unavailable" notice, and I write the update myself.
- **Strategy:**
  - **Next capability:** the Datadog metric fetch (task-level autonomy, above). Gated by a new **EV-7, metric fidelity**: over 4 weeks of shadow, 100% of fetched values match Datadog for the cited query and time window, and a scan finds zero personal data in prompts.
  - **Next segment:** PMO Project Manager / Product Marketing, from assisted to supervised, once the ezyVet PM has passed the supervised gate.
