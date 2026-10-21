# Agent Line Map: Cortex PM Chief-of-Staff Agent

> Module 1 · The Agent Line
>
> ✅ **What this validates:** every risky action has a clear owner, by the end you'll have proven an above/below-the-line map with HITL checkpoints, scored on reversibility, blast radius, and measurability.

## The workflow, decision by decision

List every discrete decision or action in your agent's workflow, then score each one and place it **above** the line (a human owns it) or **below** (the agent owns it). Borderline calls get an HITL checkpoint.

| Decision / action | Reversibility (H/M/L) | Blast radius (H/M/L) | Measurability (H/M/L) | Above / Below | HITL? |
|---|---|---|---|---|---|
| Pull project state + recent activity | H | L | H | Below | · |
| Decide relevant context (within guardrails) | H | L | M | HITL | review in draft |
| Surface "unsure if relevant" items to a human | H | L | H | Below | · (this is the checkpoint for context) |
| Draft the weekly leadership status update | H | L | M | HITL | required |
| Decide tone | M | M | M | HITL | review in draft |
| Decide commitment level | L | M | M | Above | required |
| Flag at-risk / escalation (to a human) | H | L | H | Below | · |
| Choose what to escalate | L | H | H | Above | required |
| Propose a story batch (capped) | H | L | H | Below | · |
| Post the update / approve a company-wide one | L | H | L | Above | required |

## Agent anatomy (sketch)

- **Model:** `gpt-4o-mini` drafts; the critic runs on `gpt-4o`, ~$0.009 a run. Started on `gpt-4o-mini` for both; the cheap critic flip-flopped on Green/Yellow calls, so in M2 the critic moved to the stronger model (the one place judgment matters most, and a short call).
- **Tools:** read-only `get_task` · `get_project` · `get_activity` · `search_past_updates` · `get_roadmap` · `get_norms`, plus `propose_stories`, which only queues a capped batch for human approval. Deliberately no post, create, or merge tools.
- **Memory:** persists across runs: team norms, roadmap, decision log, past *approved* updates. Purged each run: the task brief, raw pulled activity, and unapproved drafts, so a rejected draft never becomes precedent. Never stored or repeated: roadmap items marked confidential.
- **Loop:** _placeholder, defined in M2 loop-spec.md_
- **Bounds:** _placeholder, defined in M5 bounds-and-evals.md_
- **Evals:** _placeholder, defined in M5 bounds-and-evals.md_

## The golden rule, applied

1. **Pull project state + recent activity** sits below the line because it's easy to undo, has a low blast radius, and is easy to verify: "you can pull this from all the different resources autonomously." Deciding factor: blast radius (read-only, changes nothing).
2. **Decide relevant context** is HITL because it's easy to undo and has a low blast radius, but is only medium to verify, since a missed piece of context is hard to spot. Deciding factor: measurability.
3. **Surface "unsure if relevant" items** sits below the line because it's easy to undo, has a low blast radius, and is easy to verify; it only reaches me. Deciding factor: blast radius.
4. **Draft the update** is HITL because it's easy to undo and has a low blast radius, but is only medium to verify: "you can use the information and an example to draft the update." Deciding factor: measurability (even the critic couldn't agree on Green vs Yellow).
5. **Decide tone** is HITL because it's medium on all three axes, so nothing forces it either way. Deciding factor: blast radius (the tone reaches leadership).
6. **Decide commitment level** sits above the line because a commitment in writing is hard to reverse. Deciding factor: reversibility.
7. **Flag at-risk / escalation** sits below the line because it's easy to undo, easy to verify, and has a low blast radius "if the agent is just flagging the risk to the HITL." Deciding factor: blast radius.
8. **Choose what to escalate** sits above the line because it's hard to reverse and has a high blast radius: "this is a human decision ultimately." Deciding factor: reversibility (a missed escalation can't be undone).
9. **Propose a story batch (capped)** sits below the line because it's easy to undo, has a low blast radius, and is easy to verify: "you have the context and guidelines to propose the stories." Deciding factor: blast radius (stories are queued and capped).
10. **Post the update / approve a company-wide one** sits above the line because it fails all three axes: "if it's a company-wide update I'd prefer to update the company-wide resource e.g. SharePoint." Deciding factor: blast radius.

## Hardest call

**Decide tone and commitment level.** I first put it above the line, but my concern was never the tone, it was the *commitment*. Splitting it settled it: committing in writing is hard to walk back, so **reversibility** keeps commitment level above the line, while tone scored medium on every axis and moved to HITL, where I review it in the draft.
