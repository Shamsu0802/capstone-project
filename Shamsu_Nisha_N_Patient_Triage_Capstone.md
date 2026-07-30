# Capstone — Shamsu Nisha N
## AI-Powered Patient Triage & Risk Assessment Assistant

## Business context

A telehealth startup's nurse triage line is overwhelmed — patients describe
symptoms in free text or over chat before a human nurse ever reviews the
case, and cases sit in an unsorted queue. They want a system that reads a
patient's self-reported symptoms, estimates an urgency/risk level to help
prioritize the queue, and surfaces relevant guidance from their internal
clinical protocol documents for the reviewing nurse — while making it
extremely clear this is a **triage priority aid for a human nurse**, not a
diagnosis, and behaving safely and conservatively whenever it's uncertain.

## Problem statement

Build an end-to-end service that:
1. Accepts free-text patient-reported symptoms and extracts structured
   information from them using an LLM (symptoms mentioned, duration,
   severity indicators, relevant patient context)
2. Uses a trained ML model on structured intake data (age, reported vitals
   if available, symptom flags, medical history flags) to estimate a
   priority/risk tier
3. Retrieves relevant guidance from a small set of clinical protocol
   documents to show the reviewing nurse alongside the priority score
4. Has explicit, non-negotiable safety guardrails — anything indicating a
   potential emergency must be flagged as highest priority and routed to
   immediate human review, never auto-resolved or downplayed
5. Is tested, containerized, and documented

## Data guidance

There's no dataset provided. Two reasonable paths:

- **Structured risk model**: a public dataset like the CTG (cardiotocography)
  or a general vitals-based triage dataset can inform your modeling approach,
  or you can simulate a plausible dataset — patient age, reported symptom
  flags (fever, chest pain, difficulty breathing, etc.), duration, and a
  target urgency label — with a realistic, non-trivial relationship between
  features and urgency (some genuinely ambiguous/borderline cases, not
  everything cleanly separable).
- **Free-text symptom descriptions**: write or generate a set of ~30–40
  realistic patient-reported symptom messages of varying clarity and
  severity (including some deliberately ambiguous or minimizing language —
  patients often understate how serious something is), for your LLM
  extraction step to work on.

Document your data approach and its limitations clearly — in a real
healthcare context, data provenance and limitations are not a footnote,
they're central to whether the system is safe to use at all.

## Required architecture

**Extraction layer**
- LLM-based structured extraction from free-text symptom reports into a
  defined schema (symptoms, duration, severity indicators, red-flag terms)
- Extraction output must be schema-validated, same standard as Day 4

**Risk model layer**
- A trained classifier estimating urgency/priority tier from structured
  intake data
- Clear metric justification given the safety context — think specifically
  about which error type (missing a truly urgent case vs. over-flagging a
  mild one) is more costly here, and design your threshold/metric choice
  around that reasoning explicitly

**Safety guardrail layer — required, not optional**
- A deterministic, rule-based override layer that sits on top of both the
  extraction and the model: certain red-flag terms or combinations (e.g.
  chest pain + shortness of breath, mentions of loss of consciousness, etc.)
  must force a "highest priority / immediate human review" result
  regardless of what the ML model or LLM extraction alone would output.
  This should not be solely LLM-driven — a keyword/rule safety net that
  cannot be silently overridden by model uncertainty is the point.
- Document your guardrail list and reasoning.

**Retrieval layer**
- Write 5–8 short internal clinical protocol snippets (a few sentences
  each — general triage guidance, not real medical advice) and retrieve
  relevant guidance to display alongside the priority tier for the human
  nurse reviewing the case
- The system should never present retrieved guidance as a diagnosis or
  autonomous medical decision — frame all output as decision support for
  a human reviewer

**API layer**
- `POST /intake` — accepts free-text symptoms + structured fields, returns
  extracted structured data, priority tier, and relevant retrieved guidance
- `GET /health`
- Clean schemas, input validation

**Reliability & deployment layer**
- Tests covering normal cases, ambiguous cases, and at least 2-3 guardrail
  trigger cases explicitly
- Retry/fallback for the LLM extraction call — and clear behavior if it's
  unavailable (the rule-based guardrail layer should still function even if
  the LLM is down)
- Dockerized, config via environment variables, structured logging
- `README.md`

## Deliverables

- Full source code (extraction, model, guardrails, retrieval, API, tests,
  Dockerfile)
- Data/generation approach used, documented with limitations
- `CAPSTONE_REPORT.md`: problem framing, extraction design, model and
  metric choice with safety reasoning, guardrail list and rationale,
  what you'd do differently with more time, and an explicit statement of
  this system's limitations and what it is NOT (a diagnostic tool)

## Evaluation criteria specific to this project

- Guardrail layer actually works and cannot be bypassed by ambiguous or
  adversarial input — this is the single most important thing to test
- Metric/threshold reasoning explicitly engages with the asymmetric cost of
  errors in a safety-relevant context, not just "F1 was highest"
- Extraction stays grounded and doesn't invent symptoms not mentioned by
  the patient
- Report is honest about system limitations, doesn't overstate what it can
  safely do

## Live defense — things to probe

- Feed it a message with a clear red-flag combination — does the guardrail
  layer trigger regardless of how the rest of the pipeline scores it?
- Feed it a minimizing/ambiguous message ("probably nothing but my chest
  has felt tight since yesterday") — how does the system handle genuine
  ambiguity?
- "Kill the LLM connection — does the guardrail layer still work?"
- "Walk me through why you chose this metric/threshold, specifically in
  terms of what a missed urgent case costs versus an over-flagged mild one."
- "What would you tell a nurse using this about what it can and can't be
  trusted for?"
