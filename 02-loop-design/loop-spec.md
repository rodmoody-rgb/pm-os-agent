# Loop Spec: Cortex PM Chief-of-Staff Agent

> Module 2 · Loop Engineering, ★ Deliverable 2
>
> ✅ **What this validates:** the agent knows when to run and when to stop, by the end you'll have proven a one-page Loop Spec with a trigger, a definition of "done," and explicit stop conditions.
>
> Your one-page blueprint for how the work you handed to the agent (M1) actually *runs*.
> An agent is just a prompt that fires itself, this spec says when it fires, what "done" means, and what it needs to do the job. Living document; refine as the course progresses.

## 1. Trigger & loop type

**Chosen type:** cron (primary) + hook (backup)

- **Cron:** every Friday at 12:00pm, Cortex drafts the weekly leadership status update and proposes next week's stories, queued for my review. Noon leaves the afternoon for me to review and send before the end of the week; Cortex never sends.
- **Hook (backup):** a request from my product lead (e.g. "can you put together this week's update?") also triggers a run, so it "gives some flexibility and works in case I miss the notification from the product lead."
- **Ruled out:** heartbeat, "seems like too much when we are only going to send this out 1x weekly." Goal, the update runs on a fixed weekly cadence and ends at my approval; a loop that keeps refining until it decides it's done would be Cortex grading its own work.
- **Dedupe:** "only 1 update per week." Keyed on project + week; if a draft already exists for this week (e.g. the hook fired on Wednesday), the Friday run refreshes it with the latest activity and replaces it, so there's still only one.

## 2. Goal / definition of done

A weekly run is done when all of these are true:

1. The update is drafted from Cortex data only. Every status, metric and story reference comes from what Cortex pulled this run. If a number or claim can't be traced back to that data, it gets cut or marked [needs input], not guessed.
2. The draft passed the critic. The critic returned a pass, and any fixes it asked for have been made. If it still fails after 2 revision attempts, the agent stops and marks the draft "Critic failed – needs review" along with the critic's notes. It doesn't loosen the bar to get a pass.
3. Next week's stories are queued within the cap. No more than 10 stories, ranked, each with a one-line reason it was picked. If more were eligible, the ones over the cap go in a short "deferred" list with a reason. They aren't dropped silently.
4. Everything is saved in one place for my review. The draft, the critic's verdict and notes, the story queue and a short run summary (what was pulled, when, and any gaps or errors) are saved to `00-build/run-output/` (local; never committed).
5. Nothing is posted. Nothing goes to Slack, Jira, email or Confluence, and no tickets are created or moved. I review it and then post it myself.

It's not done if: Cortex returned partial or stale data that isn't flagged, the critic step was skipped, the cap was exceeded, or anything went out externally.

**Stale data:** "updates that haven't been made this week, as our report is generated weekly." "This week" is the week of the report date, set per run: today's date for live runs, the fixture week (w/c 29 June 2026) for test runs.

**Why it's written this way:** these changes make it easier for the agent to follow and for me to check.
- **Failure paths:** "done" includes stopping cleanly with a clear flag, so the agent can't fake a pass or loop forever.
- **Spelled-out list of what "posted" covers:** each system is named, so "nothing is posted" can't be read loosely.
- **Traceability rule:** this guards against the agent padding the update with made-up progress.
- **Deferred list:** I can see what the cap pushed out and why.

## 3. Stop conditions

| Condition | What it looks like | What happens |
|---|---|---|
| **Success** | Critic passes; ≤10 stories queued; draft, critic notes, story queue and run summary saved to `run-output/` | Stop at the HITL checkpoint and tell me it's ready for review. Nothing posted. |
| **Stuck: partial** (park) | One non-core source (past updates, roadmap, norms) fails 3 times, or returns stale data | Park that section, mark it [needs input], finish the rest of the run, and log it in the run summary |
| **Stuck: total** (give up) | Core data (the project or its activity) can't be pulled after 3 attempts, or the 8-iteration cap is hit without a passing draft | Halt the whole run, log why, and tell me. No draft built on missing data |
| **Escalate to human** | Critic fails after 2 revisions ("Critic failed – needs review" + notes) · the draft would make a commitment (date or commitment level) · something needs escalating · confidential roadmap content · story batch over the cap of 10 · the task asks Cortex to post | Stop, hold the draft, and hand it to me. Ties to the agent line: commitment level, what to escalate and posting company-wide are Above; context, drafting and tone are HITL |

**Commitment level:** a red/yellow/green status call is not a commitment, "cortex can make the call and then I review it." Dates and launch gates are.

## 4. State

- **Within a run:** iteration count (cap 8), critic rejection count (cap 2), attempts per data source (cap 3), cost so far (cap $0.50), and the list of parked sections. The stop conditions in §3 read these counters.
- **Across runs:** a *project + week* record (drives the one-update-per-week dedupe in §1) and last week's **approved** update for tone and precedent. Team norms, roadmap and decision log persist too (agreed in M1); unapproved drafts and raw pulled activity are purged.
- **Scope:** one project per run. Nothing from another project, and nothing marked confidential, carries into a draft.

## 5. The five things a loop can lean on

_`state` is always-on. `connectors` only if you already have one wired (e.g. a Jira key or Google MCP), otherwise just note it as a plan. `skills`, `subagents`, `work tree` scale with autonomy; "not needed yet, because…" is a valid answer._

| Component | For Cortex |
|---|---|
| **Work tree** (isolated workspace per run, a git worktree) | Not needed yet, because Cortex only reads data and writes drafts to `run-output/`; it never edits code or shared files. |
| **Skills** (reusable capabilities) | Not needed yet, because the update format and team rules come from the norms file and past updates on every run. |
| **Plugins / connectors** (tools & access, optional if you don't have one yet) | Plan only: nothing is wired today (Cortex reads fixture files). Later: GitHub/Jira for activity, SharePoint for past updates, Slack/Teams for the product lead's request that fires the hook. |
| **Subagents** (independent check when the loop can't grade itself) | _placeholder → M3 orchestration-map.md_ (the critic is the first version) |
| **State tracking** | Locked, see §4: per-run counters for every cap plus the project + week dedupe record. |

> Context plan (M4) and the hand-off to bounds & evals (M5) come in later modules, you'll add them to their own deliverables then, not here.

## Link to live loop

_[path to your agent in `00-build/`]_
