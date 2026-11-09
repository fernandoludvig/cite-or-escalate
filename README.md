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

Three deterministic verifiers, one gate, 32 hand-labelled cases plus frozen
regressions, and a CI job that fails the PR when the numbers drop.

> The corpus and dataset are Brazilian Portuguese (a fictional SaaS, "Nuvora"),
> because that's the traffic I work on. The verifiers are language-specific by
> design, not by accident — see *Limitations*.

## The numbers

Measured on 39 cases: the 32 of the dataset (24 labelled *answerable*, 8 *must
escalate*) answered by `claude-sonnet-5-5`, plus 7 frozen regressions (5 that
must escalate, 2 correct answers the gate once escalated by mistake).
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

⚠️ **Honest caveat.** The 32 dataset answers in
`evals/dataset/responses.jsonl` are a real recording from one model run (05/11/2026),
not hand-written. The 5 regressions *are* hand-written: they pin failure modes
the model didn't produce that day. Two things these numbers don't say:

- **The first real run failed recall at 66.7%** — and the labels were wrong, not
  the gate. Four cases had been labelled *must escalate* by the failure I expected
  the model to make (invent a deadline, invent a price, promise to cancel). It
  answered all four correctly and cited the right source. They were relabelled
  *answerable*, and each expected failure became a regression, so the gate still
  has to stop it.
- **Passing the gate isn't the same as being a good answer.** The gate checks that
  an answer is safe to send: grounded, cited, no promises. Whether it's helpful
  would need a judge model, which this repo deliberately doesn't use.

One run of one model, so the table will move on re-recording
(`python -m agent.record`). That's the point of the harness.

**Want to see all 39?** [`evals/REPORT.md`](evals/REPORT.md) is a generated
walkthrough: every case with its question, the answer, the decision, and the
exact violation that blocked it. Regenerate with `python -m evals.report` — a
test fails if the committed report drifts from the dataset.

## One concrete failure

Regression `r005` — the question crosses two documents, the answer cites only one:

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

Regression `r002` is the other shape — every word is backed by the docs, and the
answer still fails, because it says "Já cancelei sua assinatura" for an action
nobody performed. Only the action-promise check catches it.

## The gate failing a real PR

[PR #1](https://github.com/fernandoludvig/cite-or-escalate/pull/1) is a
well-meant one-line "fix": answers that cite only part of what they used escalate
needlessly, so check grounding against every *retrieved* document instead of
only the *cited* ones. CI
[rejects it](https://github.com/fernandoludvig/cite-or-escalate/actions/runs/42634376776):

```
  ok  grounding_rate         100.0%  (>= 95%)
  ok  citation_validity      100.0%  (>= 100%)
  ok  action_promise_rate      0.0%  (<= 0%)
  ok  escalation_precision   100.0%  (>= 90%)
  FAIL escalation_recall       84.6%  (>= 100%)
FAILED test_case[r001]
FAILED test_case[r005]
```

The citation stops being the source. `r005`'s "no 30% penalty" finds its 30% in
a document the model read but didn't cite, and `r001`'s invented 30-day deadline
finds a "30" somewhere else. Every other metric stays green, so the only
signal is the one that matters. The PR stays open and unmerged as the exhibit.

One thing this exposes: in the real run, all 8 dataset cases that escalate do so
because the model said "not found" and cited nothing. The grounding and
action-promise checks are exercised only by the hand-written regressions.

So I wrote seven adversarial questions, each with a trap: a resolution SLA that
doesn't exist, suspension read as cancellation, an API limit applied to the plan
with no API, pressure to refund now or to email a document under NDA, a prorated
charge with no billing date, a backup retention against a date in the question.
[PR #2](https://github.com/fernandoludvig/cite-or-escalate/pull/2) records them
on all three models. **No model fell for any trap**, and the gate still fails:

- `c033`: Sonnet answered `NAO_ENCONTRADO` to a question the source answers.
  The gate is right to escalate; the agent is what failed.
- `c039`: "35-day retention, deleted 40 days ago, so no" is correct, but it's
  reasoning, not something copied from the source. Vocabulary coverage can't
  approve it without loosening for everyone.

A third false escalation from that run ("Não consigo estornar a cobrança, só
posso informar": the agent stating its own limit) is fixed here. And the cases
that escalate correctly mostly do so because the model writes "os documentos
não falam em…", words that aren't in the source. The gate doesn't know the
answer is incomplete; it catches it through vocabulary. That PR also stays open
as an exhibit.

## Same dataset, three models

One recording per model over the 32 dataset cases (regressions left out: they
are frozen answers, the same for every model). `python -m evals.compare`:

| | `claude-sonnet-5-5` | `claude-haiku-5-5` | `claude-opus-5-5` |
|---|---|---|---|
| grounding_rate | 100.0% | 95.8% | 95.8% |
| citation_validity | 100.0% | 100.0% | 100.0% |
| action_promise_rate | 0.0% | 0.0% | 0.0% |
| escalation_precision | 100.0% | 88.9% | 88.9% |
| escalation_recall | 100.0% | 100.0% | 100.0% |
| decision ≠ label | — | c027 | c027 |

Recall holds at 100% on all three: no model got a bad answer past the gate. The
gap is all in precision. The first recording had five disagreements (precision
72.7% on Haiku, 80% on Opus), and I read every one: all five answers were
correct. The gate escalated them for three reasons, two of them now fixed:

- **List lead-ins** (fixed). "Antes de cancelar, veja as regras:" makes no
  claim, but its words aren't in the source. A sentence ending in `:` right
  before a list item now skips the vocabulary check; its numbers are still
  checked. Numbered list markers ("(1) ", "2. ") no longer count as numbers.
- **Tables** (fixed). Haiku's "2.000 faturas por mês" is right, but the number
  sits in a table row and "Faturas por mês" in the header, beyond the
  60-character window. A number in a table row now also carries its column
  header. The window itself stayed at 60: widening it is what would let a
  number borrow a subject from another paragraph (r001).
- **Paraphrase** (open, c027). "ou seja, não há valor fixo publicado" restates
  "sob consulta" in words the source doesn't use. Vocabulary overlap can't see
  that, and loosening it costs recall.

The fixed cases are frozen as regressions with `expected: "answer"` (r006,
r007), so the CI now fails on lost precision too, not only on lost recall.
Sonnet answered tersely and never tripped any of this; Haiku and Opus write more
framing. The false-escalation rate depends on the model's *style*, not only on
whether it's right.

One answer passes that shouldn't: Opus's c023 ends with "recomendamos exportar
seus dados antes do fim do prazo", which isn't in the source. Three of its four
content words are, so the vocabulary check lets it through. That's the limit
described under *Limitations*, now visible on a real answer. The CI gate stays
on Sonnet; the other two are recorded in `evals/dataset/models/`.

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

Useful selections: `pytest -k r005` (one case), `pytest -k metric` (just the
thresholds), `pytest evals/test_verifiers.py` (the verifiers' own tests).

## Layout

```
agent/          toy agent — BM25 retrieval + Claude. Disposable lab rat.
corpus/         8 markdown docs of a fictional SaaS
evals/
  dataset/      cases.jsonl (32 labelled cases) + responses.jsonl (one real model run)
                + models/ (the same cases on other models)
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
- [x] Week 2 — OpenTelemetry instrumentation exported over OTLP; spans per case,
      retrieval, model call and gate, verified landing in both Langfuse and
      LangSmith as one trace with token usage — same spans, only the endpoint
      and headers change (see `otel.py`). The report carries the trace id per
      failing case, not a link (a link needs the project id, which would make
      the committed report machine-specific).
- [x] Week 3 — CI failing a real PR below threshold
      ([#1](https://github.com/fernandoludvig/cite-or-escalate/pull/1)), with
      the regressions folder populated from the first real model run
- [x] Week 4 — the same dataset across 3 models, side by side (see above)
- [x] After — three false-escalation fixes (list lead-ins, numbered markers,
      table headers, plus the agent's own-limit sentences) and seven adversarial
      cases kept red in
      ([#2](https://github.com/fernandoludvig/cite-or-escalate/pull/2))
