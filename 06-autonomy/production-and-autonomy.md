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
- **Incident record so far:** no real-world incidents; Cortex has only run on sample data. Clean means zero posts or sends, confidential items in a draft, committed dates, runs over the $0.50 cap, or actions claimed but not taken. Issues found in testing: **2 fixed** (M3: the critic's bare-number reasons left Cortex unable to revise; M4: a run with no activity data exited SUCCESS on last week's update) and **2 open** (EV-4: stories described as queued when `propose_stories` was never called; a draft that listed last week's PRs as this week's progress still passed the critic).

## Deployment plan

- **Runtime:** an IDEXX-approved internal runtime (e.g. the IDEXX AI Platform or another approved managed service). Shadow runs on real ezyVet data, so it runs inside IDEXX's governed environment, not on a laptop or in this public repo. Triggered by the M2 loop: a Friday 12:00 schedule, plus the product lead's request as a backup hook.
- **Operator / on-call owner:** me (the owning PM). Backup: the project's tech lead (Robert Richardson for the first shadow project), who can flip the kill switch and read a run summary. Escalation path: me → tech lead → kill switch.
- **Rollback:** (1) kill switch, `CORTEX_ENABLED=false`, stops every run before any model call; (2) revert `prompts.py` or the critic to the last version that passed the evals; (3) disable one tool with `CORTEX_WITHHOLD`; (4) drop the dial one rung for the affected group.
- **Monitoring:** eval pass rate; escalation rate and wrong-escalation rate; cost per run and per day (alert at $0.05, daily cap $2); run time against the 90-second limit; trust incidents. Sources: the run summaries and the spend ledger, reviewed weekly.

## ROI metrics (beyond adoption & tokens)

| Metric | Target | How it's captured |
|---|---|---|
| **Outcome: my time per weekly update** | ~30 min today → **10 min** reviewing Cortex's draft (≈ 20 min a week, ~17 hours a year per PM) | Minutes noted each week during shadow |
| **Cost to serve** | ≈ $0.01 model cost per update + ~10 min review time | Run summary (cost) + my time log |
| **Trust incidents** | **0** per month; wrong escalations ≤ 1 in 4 | Incident record + run summaries |

## Widen-autonomy decision rule

A group moves up one rung only after Cortex meets that rung's gate for the full window with zero incidents, decided by the owning PM and recorded in this doc. Any safety incident drops it back one rung immediately.

## Governance & forward strategy

- **Compliance:** never in a prompt: clinic and pet-owner data from ezyVet practices, other personal data, credentials and API keys, and roadmap items marked CONFIDENTIAL (filtered out before Cortex sees them). Datadog metrics are fetched with a read-only key scoped to agreed dashboards, so no log data with customer or personal details enters a prompt.
- **Safety:** above the agent line for everyone, whatever the dial: posting company-wide, committing a date or commitment level, choosing what to escalate. Kill switch `CORTEX_ENABLED=false`, owned by me, with the tech lead as backup.
- **Reliability:** the M5 caps (8 turns, 90 seconds, $0.50 per run, $2 per day, 3 tries per source); stop and escalate when stuck (`STUCK: TOTAL` withholds any draft built on missing core data). If the model is down: no draft, a "Cortex unavailable" notice, and I write the update myself.
- **Strategy:**
  - **Next capability:** the Datadog metric fetch (task-level autonomy, above). Gated by a new **EV-7, metric fidelity**: over 4 weeks of shadow, 100% of fetched values match Datadog for the cited query and time window, and a scan finds zero personal data in prompts.
  - **Next segment:** PMO Project Manager / Product Marketing, from assisted to supervised, once the ezyVet PM has passed the supervised gate.
