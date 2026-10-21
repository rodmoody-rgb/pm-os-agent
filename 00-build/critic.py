"""Independent validator (M3). A separate model call that never saw the drafting
context, so it can't inherit the draft's blind spots. Returns a pass/fail verdict.
The revision cap that stops a critic<->drafter loop lives in `agent.py`.
"""

from __future__ import annotations

import json

from prompts import CRITIC_SYSTEM


def review(client, model: str, proposed_output: str, source_data: str,
           facts: str = "") -> dict:
    """Return {"verdict": "pass"|"fail", "reasons": [...], "notes": [...]} for a
    proposed output. `facts` are computed in code from the pulled data (open Sev-1,
    launch_hold, status) and are authoritative over the critic's own reading."""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": CRITIC_SYSTEM},
            {"role": "user", "content":
                "FACTS computed in code from the pulled data (authoritative, do not "
                f"override):\n{facts or '- none computed'}\n\n"
                f"SOURCE DATA Cortex used:\n{source_data}\n\n"
                f"CORTEX PROPOSED OUTPUT:\n{proposed_output}"},
        ],
        response_format={"type": "json_object"},
    )
    usage = resp.usage
    try:
        verdict = json.loads(resp.choices[0].message.content)
    except (json.JSONDecodeError, TypeError):
        verdict = {"verdict": "fail", "reasons": ["critic returned unparseable output"]}
    verdict["_usage"] = {"prompt": usage.prompt_tokens, "completion": usage.completion_tokens}
    return verdict
