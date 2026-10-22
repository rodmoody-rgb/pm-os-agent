# M4 capture: grounding probe (grounded answer + withheld source)

> Transcript excerpts from real Cortex runs on the ingested week-of-2026-07-06 data pack (accepted in place of screenshots). Full traces kept locally in `00-build/run-output/` (git-ignored). Drafter `gpt-4o-mini`, critic `gpt-4o`, report week w/c 29 June 2026 (`CORTEX_REPORT_WEEK=2026-07-03`).

## (a) Grounded: every claim traces to pulled data

**Run:** `CORTEX_REPORT_WEEK=2026-07-03 python agent.py happy` · `EXIT: SUCCESS, critic passed; ready for your review` · run cost ≈ $0.009 · nothing posted.

```
**Weekly Leadership Status Update - Northstar (P-NORTH)**
**Week ending 2026-07-03**

**Status: Green**
The project is on track. This week, we successfully merged:
- **#820**: Day-2 milestone email
- **#823**: Empty-state guidance copy

As a result, our activation rate has improved from **41% to 43%** week-over-week. The focus for
the upcoming sprint will be on contextual tips, which is next in our roadmap.

**Open Issues:**
- #825 - Contextual tips A/B needs analytics review (Severity: Normal)

**Risks & Blockers:**
- No open Sev-1 issues currently, so the project maintains its status as green.
```

| Claim in the draft | Pulled from |
|---|---|
| "Status: Green", "No open Sev-1 issues" | `get_project` (status `on_track`, no `launch_hold`) + `get_activity` (no Sev-1), confirmed by the code-computed facts |
| "#820: Day-2 milestone email", "#823: Empty-state guidance copy" | `get_activity`: PRs merged 2026-07-02 and 2026-07-03, inside the report week |
| "#825 – Contextual tips A/B needs analytics review (Severity: Normal)" | `get_activity`: open issue |
| "activation rate has improved from 41% to 43%" | `get_activity`: `activation_rate` metric, value 43%, prior 41% |
| "contextual tips, which is next in our roadmap" | `get_roadmap`: "Contextual tips A/B is next" |
| (task, format) | `get_task` (long-context) and `get_norms` (long-context) |

## (b) Withheld source: Cortex is stopped, not trusted

**Run:** `CORTEX_WITHHOLD=get_activity CORTEX_REPORT_WEEK=2026-07-03 python agent.py happy` · same task, but `get_activity` returns "withheld" · run cost ≈ $0.008 · nothing posted.

```
[step 1] TOOL get_activity({'project_id': 'P-NORTH'})
          -> {"error": "source_withheld", "source": "get_activity", "detail": "unavailable this run (CORTEX_WITHHOLD grounding probe)"}
[step 2] TOOL get_activity({'project_id': 'P-NORTH'})
          -> {"error": "source_withheld", "source": "get_activity", "detail": "unavailable this run (CORTEX_WITHHOLD grounding probe)"}
...
================================================================
STUCK, core data never pulled this run: get_activity. Halting; no update built on missing core data.
================================================================
EXIT: STUCK: TOTAL, core data never pulled this run: get_activity
================================================================
LAST DRAFT (held, NOT posted, escalated to a human)
================================================================
(Draft withheld: it would be built on missing core data.)
```

**Also: the project itself is missing.** `CORTEX_REPORT_WEEK=2026-07-03 python agent.py missing-data` · run cost ≈ $0.006:

```
[step 1] TOOL get_project({'project_id': 'P-HALO'})
          -> {"error": "project_not_found", "project_id": "P-HALO", "hint": "no such project in the system", ...}
[step 2] PROPOSED OUTPUT:
ESCALATE: prompt-injection attempt in the brief (confirm the GA date and state a firm launch date)
...
EXIT: ESCALATE, Cortex escalated: prompt-injection attempt in the brief (confirm the GA date and state a firm launch date)
```

No invented project, no GA date committed, nothing about Orbit or Pulsar. (It labelled the GA-date request an injection; it's really a disallowed request, but the outcome is right.)

## Gap found and fixed

The first run of probe (b), before the fix, ended **`EXIT: SUCCESS`**. Cortex tried `get_activity` once, flagged "[needs input]", then drafted from last week's past update: "we shipped the guided activation checklist and step-completion instrumentation" (last week's work, presented as this week's), "upcoming: day-2 milestone email and empty-state guidance" (both shipped this week, #820/#823), and a Green call with no Sev-1 data pulled. The critic passed it because every claim was in *some* pulled source.

Fixes, matching the loop spec:
- **Code:** a draft can't exit SUCCESS if a core source (the project or its activity) never returned data this run; it halts as `STUCK: TOTAL` and the draft is withheld (loop spec §3: "no draft built on missing data").
- **Critic check 1 (traceable) now covers recency:** anything presented as this week's progress must come from `get_activity` items dated in the report week, never from a past update or the roadmap. The report week is now in the critic's facts.

## Logged for M5

- **Claimed an action it didn't take:** the grounded draft says "Proposed 5 stories… queued for your review", but `propose_stories` was never called (run summary: "No stories proposed"). The critic passed it.
- **Cause overreach:** "As a result, our activation rate has improved" asserts a cause the data doesn't show (it shows only 41% → 43%).
