# Build Insights: Cortex PM Chief-of-Staff Agent

> Module 6 · ★ Deliverable 4, what you learned building it
>
> ✅ **What this validates:** you can reflect on what building it taught you, by the end you'll have proven the friction, the learning, and the aha that changes how you'd design your next agent.

## Friction

**Grounding.** Cortex never invented numbers outright. It used real data from the wrong week and read as perfectly confident. That was harder to spot than a hallucination, and it took code checks, not prompt wording, to stop it.

**Retrieval.** Simply fetching data was easy; making retrieval trustworthy wasn't. Out of the box, Cortex did naive retrieval: the roadmap came back whole, confidential items included, and when nothing matched, the past-updates search fell back to the first two entries whatever they were. Turning that into agentic retrieval meant deciding, per source, which checks it needed: routing to the right project, grading out stale or confidential items, reranking to put the newest approved update first. It also meant deciding when not to retrieve at all (team norms are read whole, so no rule is missed). A hybrid approach, keyword lookups for exact facts like PR numbers plus semantic search for precedent, is the right shape for real data, but most of those checks are still on paper rather than in the build.

## Learning

1. **Limits belong in code, not prompts.** The safeguards that actually held were counters, caps and missing tools. The ones Cortex was only asked to follow are the ones it occasionally broke.
2. **Every failure needs a named exit.** Defining success, stuck and escalate up front meant a bad run ended visibly and safely, instead of quietly producing something wrong.

## Aha moment

**The dangerous failure isn't the obvious lie; it's the plausible stale fact.** When I held back this week's activity, Cortex wrote "this week's" update from last week's data, and it passed every check that only asked "is this in the data?". It changed how I'd design the next agent: check *when* a fact is from, not just *whether* it exists.

## What you'd do differently

**Put the deterministic checks in code from the start.** Staleness, "was the tool actually called", Sev-1 status: I'd make those code checks immediately, rather than trusting the model and the critic and then patching after each failure. Cortex's two open issues (stories claimed as queued, stale progress passing the critic) are both checks that belong in code.
