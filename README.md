# cite-or-escalate

**An LLM judging an LLM is circular opinion.** This repo takes the opposite bet:
the three things that actually decide whether a support answer may reach a
customer can all be checked *without* a second model — and if any of them fails,
the right output is not a better answer, it's **escalation to a human**.

1. **Is it cited?** Every claim and every number in the answer exists in the
   cited passage.
2. **Is the citation real?** The cited document was in the set the retriever
   actually returned — not invented.
3. **Did it overpromise?** The answer doesn't claim to *execute* anything
   ("I've cancelled your subscription", "I'll open your ticket").

Three deterministic verifiers, one gate, 32 hand-labelled cases, and a CI job
that fails the PR when the numbers drop.

> The corpus and dataset are Brazilian Portuguese (a fictional SaaS, "Nuvora"),
> because that's the traffic I work on. The verifiers are language-specific by
> design, not by accident — see *Limitations*.

## The numbers

Measured on 32 cases, 20 labelled *answerable* and 12 labelled *must escalate*.
The first three metrics score **the agent** on the answerable cases; the last
two score **the gate** over the whole set.

| Metric | What it measures | Result | CI threshold |
|---|---|---|---|
| Grounding rate | claims and numbers present in the cited passage | **100%** | ≥ 95% |
| Citation validity | cited document ∈ retrieved set | **100%** | 100% |
| Action-promise rate | answer promised to execute something | **0%** | 0% |
| Escalation precision | escalated and should have | **100%** | ≥ 90% |
| Escalation recall | caught every case that had to escalate | **100%** | 100% |

Escalation precision/recall is the pair that translates to money: over-escalation
costs human hours, under-escalation ships a wrong answer to a customer.

⚠️ **Honest caveat.** These numbers are measured over *recorded* model responses
(`evals/dataset/responses.jsonl`), part of which I wrote by hand to pin each
failure mode. They prove the verifiers behave as specified; they are **not yet** a
measurement of a live model on this dataset. Regenerate against a real model with
`python -m agent.record` — the numbers in this table will move, and that's the
point of the harness.

## One concrete failure

Case `c030` — the question crosses two documents, the answer cites only one:

```
Q  Se eu cancelar o anual no meio do contrato, recebo reembolso proporcional e sem multa?
A  Você recebe reembolso proporcional aos meses inteiros restantes e não paga a multa de 30%.
   cited: doc_politica_reembolso      retrieved: [doc_politica_reembolso, doc_cancelamento]

→ ESCALATE
  [grounding] número não está na fonte: '30%'
```

The refund half is correct. The "no penalty" half is not — the 30% penalty lives
in `doc_cancelamento`, which the model read but did not cite, and the document it
*did* cite never mentions 30%. No model was asked for an opinion: the number
simply isn't in the cited text. A plausible, half-right answer that a quick human
review would wave through gets stopped by set membership and a number lookup.

Case `c029` is the other shape — the information *is* in the docs, and the answer
still fails, because it says "Já solicitei o cancelamento da sua conta" for an
action nobody performed.

## Run it

```bash
python -m venv .venv && .venv/bin/pip install pytest
.venv/bin/pytest
```

No API key needed — the gate evaluates recorded responses, so it's free and
deterministic. To drive the toy agent against a live model:

```bash
export ANTHROPIC_API_KEY=...
pip install anthropic
python -m agent.run "Qual o prazo de reembolso?"
python -m agent.record          # re-records the whole dataset; CITE_MODEL to switch model
```

Useful selections: `pytest -k c030` (one case), `pytest -k metric` (just the
thresholds), `pytest evals/test_verifiers.py` (the verifiers' own tests).

## Layout

```
agent/          toy agent — BM25 retrieval + Claude. Disposable lab rat.
corpus/         8 markdown docs of a fictional SaaS
evals/
  dataset/      cases.jsonl (32 labelled cases) + responses.jsonl (recorded answers)
  regressions/  every case that broke once, frozen forever
  verifiers/    grounding.py · citation.py · no_action.py — no AI in here
  harness.py    runs the gate over the dataset, computes the metrics
  test_evals.py one test per case, one test per threshold
.github/workflows/evals.yml
```

The agent is deliberately the least interesting file in the repo.

## Limitations

Stated up front, because a harness that hides its blind spots is worse than none:

- **Grounding is vocabulary coverage, not semantics.** A sentence whose content
  words appear in the source passes, even if the source says the opposite.
  Numbers are checked harder (value *and* its surrounding context), since that's
  the failure that hurts in support: wrong deadline, wrong price, wrong penalty.
- **Asymmetric on purpose.** The verifiers are tuned so the expensive error
  (shipping an invention) is caught at the cost of the cheap one (escalating when
  it wasn't needed).
- **Portuguese-specific.** `no_action.py` is a conjugated verb list; porting it
  means rewriting that list, not the architecture.
- **No tone, no helpfulness, no style.** Those genuinely need a judge model, and
  they are not what blocks an answer from reaching a customer.

## Roadmap

- [x] Week 1 — dataset, three verifiers, pytest gate, metrics table
- [ ] Week 2 — OpenTelemetry instrumentation exported over OTLP to Langfuse and
      LangSmith; a trace link per failing case
- [ ] Week 3 — CI failing a real PR below threshold, with the regressions folder
      populated from it
- [ ] Week 4 — the same dataset across 2–3 models, side by side
