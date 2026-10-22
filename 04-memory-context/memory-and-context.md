# Context Engineering & Memory: Cortex PM Chief-of-Staff Agent

> Module 4 · Context Engineering & Memory
>
> ✅ **What this validates:** the agent reasons on the right, safe inputs, by the end you'll have proven a context budget, per-source retrieve-vs-long-context decisions, and a memory map with risk mitigations.
>
> 🗂️ **How the lab maps to this file:** In **Part A** (before the lecture) you don't edit this file, you rough-draft on scratch, focused on the per-source calls in **section 2** plus a quick remember/forget + "how it rots" sketch. In **Part B** (after the lecture) you complete **all five sections**; the Lab Guide's guided builder writes this file for you to copy in and commit.

## 1. Context budget

When the prompt is tight, keep in this order (1 = keep first, 5 = trim first):
1. The task brief (`get_task`)
2. Team norms (`get_norms`)
3. This week's activity for this project (`get_activity`)
4. The shareable roadmap slice (`get_roadmap`)
5. Past updates and decisions (`search_past_updates`), the first to trim

## 2. Retrieve vs. long-context: per source

For each data source, decide: **retrieve** (narrow a large/changing corpus to the relevant slice) or **long-context** (just include a bounded set you can reason over).

| Source | Size / volatility | Decision | Why (deciding factor) |
|---|---|---|---|
| `get_task` | One static doc | Long-context | Small, and must be read in full (size) |
| `get_norms` | Medium, must stay current | Long-context | "Key with the get_norms is to not miss any context," so Cortex reads every rule, not a search hit (size) |
| `get_activity` | Large, grows | Retrieve | "Big and changing"; every claim must trace to an item (volatility) |
| `get_roadmap` | Medium, confidential flags | Retrieve | Only the shareable slice, so Orbit and Pulsar never enter the prompt (citation/audit) |
| `search_past_updates` | Unbounded | Retrieve | Grows every week forever (size) |

**Trickiest call:** `get_norms`. "Key with the get_norms is to not miss any context so hence the decision to have long-context." A search could return only some of the rules, and Cortex can't apply a rule it never saw.

## 3. Retrieval quality plan

Only the moves each retrieved source's failure mode needs. (Long-context sources, `get_task` and `get_norms`, are read whole and need none.)

| Source | Failure mode (seen in my runs) | Routing | Doc grading | Reranking | Self-verification | Caching | Built today? |
|---|---|---|---|---|---|---|---|
| `get_activity` | Cites old or already-done work ("Finalize design for the day-2 milestone email" after #820 merged) | ✅ only the task's project | ✅ drop/flag items outside the report week | | ✅ critic check 1, traceable | | Routing ✅ · grading partly (stale check covers dated PRs; issues and metrics have no dates) · self-verification ✅ (doesn't yet catch already-done work) |
| `get_roadmap` | Confidential items (Orbit, Pulsar) leak into the draft | | ✅ drop CONFIDENTIAL items before Cortex sees them | | ✅ critic check 2, no confidential item | | Grading ❌ (whole file returned with a warning) · self-verification ✅ |
| `search_past_updates` | Returns irrelevant precedent when nothing matches (falls back to the first two entries) | | ✅ drop other projects' entries and unapproved drafts | ✅ newest approved update first, top 2–3 only (this handles size) | | | Grading ❌ · reranking ❌ |

**Not caching:** Cortex runs once a week and the lookup is quick, so a cache saves almost nothing and risks serving a stale copy. Size is handled by retrieval + reranking + a top-2–3 limit. Last week's approved update is reused as **episodic memory** (§4), not a cache.

## 4. Memory map (your PM brain)

| Memory type | What Cortex stores | Scope / TTL |
|---|---|---|
| **Working** (in-loop) | The task brief, data pulled this run, drafts, critic verdicts, cap counters, parked sections, computed facts | This run. The draft and run summary are saved to `run-output/` (local, git-ignored) for my review and kept **4 weeks** |
| **Episodic** (past runs) | **My approved updates** (tone and precedent), the project + week dedupe record, decision-log entries | Approved updates **12 weeks** (a quarter); dedupe record **1 week** |
| **Semantic** (durable facts/prefs) | Team norms, shareable roadmap facts, the update format | Until the source changes; re-read every run, never held as a stale copy |
| **Shared** (across agents) | Cortex and the critic share the pulled data, the draft and the computed facts (M3 field 6) | This run. Critic notes go to my run summary, never to Cortex |

**Write scope (ties to the M1 agent line):** Cortex writes only to working memory. A draft becomes episodic precedent **only after I approve it** (HITL), so a rejected or unreviewed draft never becomes "how we write updates". Confidential roadmap items are never stored in any memory.

## 5. Memory risks & mitigations

| Risk | Where it bites Cortex | Mitigation |
|---|---|---|
| **Drift** | Tone and format slowly change as Cortex copies its own past output | Only my approved updates become precedent; norms are read in full every run, so they outrank precedent |
| **Poisoning** | A bad input gets stored and trusted forever (jailbreak text in a brief, a wrong figure in an update) | Brief content is never written to memory; only updates I approve enter episodic memory |
| **Staleness** | Old facts treated as current (quoting 41% when it's now 43%) | Activity retrieved fresh every run; report-week stale check; 12-week TTL on episodic memory. Gap: metrics and issues carry no dates |
| **Confidential / retention** | Embargoed items (Orbit, Pulsar) retained or repeated | Drop CONFIDENTIAL items before they reach Cortex (§3); never store them; `run-output/` stays local and out of git, cleared after 4 weeks |

TTLs (12 weeks, 1 week, 4 weeks) carry forward as bounds in M5.
