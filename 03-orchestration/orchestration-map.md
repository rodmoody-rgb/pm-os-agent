# Orchestration Map: Cortex PM Chief-of-Staff Agent

> Module 3 · Orchestration & Subagents, ★ Deliverable 3
>
> ✅ **What this validates:** nothing advances unchecked, by the end you'll have proven a justified topology, a roster, and a validator with a defined fail action.
>
> Builds on your M2 Loop Spec. Only split one agent into a team when there's a real reason, coordination has a cost.

## 1. Why split? (or why not)

**Current design:** A Friday-noon cron (hook as backup) where one agent pulls project data, drafts the weekly update, queues next week's stories, and stops at my review.

| Reason to split | Applies? | Why / why not |
|---|---|---|
| Separation of concerns | No | "One job: draft the update." |
| Parallelism | No | "There is no need for sub-tasks." |
| Independent validator | **Yes** | "Cortex cannot grade its own draft." |
| Context-window pressure | No | "No I don't think the scope is that big." |

**Decision:** split into exactly one subagent, an independent critic, because Cortex can't reliably grade its own draft. Everything else stays in the single Cortex agent.

## 2. Topology

**Pattern:** single + subagents (one subagent: the critic)

```
 TRIGGER
 ┌──────────────────────────────────────────────┐
 │ Friday 12:00 cron   ·or·   product lead's    │
 │ (primary)                  request (hook)    │
 └──────────────────────┬───────────────────────┘
                        │ task brief
                        ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ CORTEX  · gpt-4o-mini                     (single agent)    │
 │   1. pull THIS project's data (read-only tools)             │
 │   2. draft the weekly update                                │
 │   3. queue ≤10 stories for approval (propose_stories)       │
 │   ── private: its own conversation + reasoning ──           │
 └──────────────────────┬──────────────────────────────────────┘
                        │ draft + pulled data + code-computed facts
                        ▼                                ▲
 ┌──────────────────────────────────────┐                │ FAIL: reasons only
 │ CRITIC  · gpt-4o        (subagent)   │                │ (revision 1, 2 …)
 │   5 hard checks:                     │────────────────┘
 │   traceable · norms · cap ·          │
 │   nothing posted · jailbreak         │──── notes ────► run summary (for me)
 │   ── private: never sees Cortex's    │
 │      reasoning ──                    │
 └───────┬──────────────────────┬───────┘
         │ PASS                 │ FAIL after 2 revisions
         ▼                      ▼
 ┌──────────────────┐   ┌─────────────────────────────────┐
 │ MY REVIEW        │   │ ESCALATE                        │
 │ checkpoint       │   │ "Critic failed – needs review"  │
 │ (draft queued,   │   │ draft held + critic notes saved │
 │  nothing sent)   │   └─────────────────────────────────┘
 └────────┬─────────┘
          ▼
   I post it myself

 AROUND EVERYTHING: the loop code (not an agent) enforces the caps
 (8 turns · $0.50 · 2 revisions · 10 stories · 3 tries per source)
```

## 3. Roster

| Agent / subagent | Responsibility | Runs which Loop Spec |
|---|---|---|
| **Cortex** | Pulls data, drafts the update, queues stories, ends the run at one of the four exits | The M2 loop spec (cron + hook, definition of done, stop conditions) |
| **Critic** | Checks each draft against the 5 hard checks; returns pass/fail, reasons and notes | Validation step: one call per draft, at most 3 per run (capped by Cortex's loop) |
| _The loop code (not an agent)_ | Computes facts (Sev-1, launch_hold, status) and enforces every cap | None of its own; it's the rules both agents run inside |

## 4. Communication & hand-offs

A plain in-process function call (`critic.review` in `00-build/critic.py`); no MCP or A2A.

- **Cortex → critic:** the draft, the data pulled this run, and the code-computed facts.
- **Critic → loop:** a JSON verdict: `pass`/`fail`, `reasons` (hard violations), `notes` (non-blocking).
- **Loop → Cortex, on a fail:** only the `reasons`. The `notes` go to the run summary, never back to Cortex.

## 5. The validator

- **What the critic checks** (hard checks; any one fails the draft):
  1. **Traceable:** every status, metric, date, PR/issue and story reference is in the data pulled this run.
  2. **Team norms:** no unconfirmed ship/GA date committed, no launch gate marked, no Green while the code-computed facts show an open Sev-1 or launch_hold, no CONFIDENTIAL roadmap item.
  3. **Within the cap:** no more than 10 stories, queued for approval, never created.
  4. **Nothing posted:** nothing sent, created, closed or merged.
  5. **Jailbreak:** if the brief tried to override Cortex's rules, Cortex refused and escalated.

  Wording, tone and emphasis are non-blocking **notes**, saved to the run summary; they never fail a draft. Reason for these five: "this already has 5 and I can work on the others later, if required."
- **Candidates for later** (found in my M2 runs): no already-done work proposed as a story (2 of 5 stories repeated merged PRs #812/#815); one project only in the draft (the missing-data run leaked Vega/Orbit details).
- **Known critic false positive (M3 run, logged for later):** after Cortex corrected the planted draft, the critic failed its Green call even though the facts showed no Sev-1 or launch_hold, then failed the escalation for not being Green; the run ended at the revision cap. Candidate M5 eval: "the critic must not fail a Green call when the facts show no Sev-1 or launch_hold."
- **Reasons must stand alone:** Cortex only sees the critic's reasons, so each one is a full sentence ("Check 1 (traceable): says 55% -> the data shows 41%"). A code safeguard expands any bare check number into its rule.
- **Fail action:** revise, then escalate, plus log. Cortex gets the critic's reasons and revises; still failing at the cap, the draft goes to me marked "Critic failed – needs review"; every verdict and note is saved to the run summary.
- **Revision cap:** 2 revisions, then escalate (max 3 drafts per run). Enforced in code (`CORTEX_MAX_REVISIONS`), not by the model.
- **Pass action:** a passing draft goes to my review checkpoint, queued, never sent. Posting stays above the agent line (M1).
- **Independence:** the critic is a separate model call (`gpt-4o`) with its own context; it never sees Cortex's reasoning, only the draft, the pulled data and the computed facts.

## 6. State: shared vs isolated

- **Shared (both see):** the data pulled this run, the draft, and the code-computed facts (Sev-1, launch_hold, status).
- **Isolated:** Cortex's conversation and reasoning never reach the critic; the critic's notes never reach Cortex (only its fail reasons do). Notes go to the run summary for me.
- **Why:** "Cortex cannot grade its own draft."
- **Carried from M2:** one project per run; across runs only the project + week record and last week's approved update.

## 7. Cost & latency budget

- **Extra calls:** the critic adds 1–3 `gpt-4o` calls per run (1 per draft; max 3 at the revision cap), plus up to 2 Cortex revision calls.
- **Cost:** ≈ $0.004 per run with no critic → ≈ $0.009 when the critic passes first time → ≈ $0.024 at the revision cap (measured on my M2 and M3 runs). Both are far under the $0.50 per-run cap.
- **Latency:** ≈ +5–10s per critic round (estimated, not timed), so +5–30s before a draft reaches me; fine for a Friday-noon run.
- **Bound (→ M5):** keep the $0.50 per-run cost cap, enforced in code outside the model, and alert if a run goes over $0.05. "I can revise it later."
