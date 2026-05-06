# SPEC.md — PM Researcher Agent

**Version:** 1.0.0
**Kind:** System Specification
**Status:** Active

> This is the **source of truth** for the PM Researcher agent.
> Changes to agent behavior MUST be reflected here first.

---

## 1. Overview

**Purpose:** Deep web research with iterative refinement, producing a cited markdown report.

**Output:** A comprehensive, cited research report on any topic.

**Architecture:** `SequentialAgent` + `LoopAgent` — the agent runs research in phases, self-evaluates, and loops to fix gaps until the report passes quality review.

---

## 2. Agent Pipeline

```
User Request
    │
    ▼
interactive_planner_agent
    │
    ├── plan_generator ────────────────► [USER APPROVAL LOOP]
    │                                        │
    ▼                                        │
research_pipeline                            │
    │                                        │
    ├── section_planner ──────────────────► │ (iterate until approved)
    │                                        │
    ├── section_researcher                   │
    │     (Phase 1: [RESEARCH] tasks)        │
    │     (Phase 2: [DELIVERABLE] tasks)    │
    │                                        │
    ▼                                        │
iterative_refinement_loop ◄────────────────┘
    │    (max 3 iterations)
    ├── research_evaluator ── grade: pass? ──► escalate → stop
    │         │
    │         └── grade: fail ──► enhanced_search_executor ──► loop again
    │
    ▼
report_composer ──► Final Cited Report
```

---

## 3. Sub-Agent Specifications

### 3.1 `interactive_planner_agent`

**Type:** `LlmAgent`
**Model:** `config.worker_model`
**Role:** Collaborate with user to create and approve a research plan, then delegate execution.

**Instruction Contract:**
- NEVER answer a question directly
- ALWAYS call `plan_generator` first
- Present draft plan, incorporate feedback
- Execute only on explicit user approval ("looks good, run it")

**Task type prefixes (enforced):**
- `[RESEARCH]` — information gathering, requires search
- `[DELIVERABLE]` — synthesis, table, chart, report creation (no search)

**Refinement tags:**
- `[MODIFIED]` — existing task updated based on feedback
- `[NEW]` — new task added from feedback
- `[IMPLIED]` — deliverable implied by research nature

**Plan rules:**
- Initial plan: exactly 5 bullet points, all `[RESEARCH]`
- If `[RESEARCH]` implies a deliverable (e.g., comparison → table), add `[DELIVERABLE][IMPLIED]`
- Maintain original order; new tasks appended

---

### 3.2 `plan_generator`

**Type:** `LlmAgent`
**Model:** `config.worker_model`
**Purpose:** Generate or refine the 5-item research plan.

**Rules:**
- Strictly limited tool use — search only for topic clarification, NOT content research
- Output MUST start with bulleted list of 5 action-oriented goals
- Each goal starts with a verb ("Analyze...", not "The event...")
- Plan must classify each goal as `[RESEARCH]` or `[DELIVERABLE]`

---

### 3.3 `section_planner`

**Type:** `LlmAgent`
**Model:** `config.worker_model`
**Output key:** `report_sections`
**Purpose:** Transform the approved research plan into a 4-6 section markdown outline.

**Rules:**
- Ignore `[RESEARCH]`, `[DELIVERABLE]`, `[MODIFIED]`, `[NEW]` tags
- Design a logical report structure
- Do NOT include "References" or "Sources" section
- Sections must be non-overlapping and comprehensive

---

### 3.4 `section_researcher`

**Type:** `LlmAgent` + `BuiltInPlanner(thinking_config=include_thoughts=True)`
**Model:** `config.worker_model`
**Output key:** `section_research_findings`
**Tools:** `google_search`
**Callback:** `collect_research_sources_callback`

**Two-Phase Execution:**

**Phase 1 — `[RESEARCH]` Tasks (MUST complete all before Phase 2):**
1. For each `[RESEARCH]` goal: generate 4-5 targeted search queries
2. Execute all queries via `google_search`
3. Synthesize results into a coherent summary
4. Store summary tagged by goal (do NOT discard)

**Phase 2 — `[DELIVERABLE]` Tasks (ONLY after all Phase 1 complete):**
1. For each `[DELIVERABLE]` goal: interpret as a direct instruction
2. Produce the artifact (table, summary, report, chart) using ONLY Phase 1 summaries
3. Do NOT perform new searches
4. Accumulate all artifacts as final output

**Callback behavior:** `collect_research_sources_callback`
- Extracts grounding metadata (URLs, titles, domains) from session events
- Maps URLs → `src-N` short IDs
- Stores in `callback_context.state["sources"]`

---

### 3.5 `research_evaluator`

**Type:** `LlmAgent`
**Model:** `config.critic_model`
**Output schema:** `Feedback` (Pydantic)
**Output key:** `research_evaluation`

**Evaluation rules:**
- ASSUME the topic is correct — do not verify the premise
- Evaluate: comprehensiveness, logical flow, credible sources, depth, clarity
- CRITICAL: be very strict about quality
- `grade: "fail"` → must include 5-7 specific follow-up queries
- `grade: "pass"` → escalate to stop the loop

**Feedback schema:**
```python
class Feedback(BaseModel):
    grade: Literal["pass", "fail"]
    comment: str  # Detailed explanation
    follow_up_queries: list[SearchQuery] | None  # null if pass
```

---

### 3.6 `EscalationChecker`

**Type:** Custom `BaseAgent`
**Purpose:** Stop the `LoopAgent` when `research_evaluation.grade == "pass"`.

**Behavior:**
- Reads `session.state["research_evaluation"]["grade"]`
- If `"pass"`: yields `Event(escalate=True)` → stops the loop
- If `"fail"` or missing: yields empty event → loop continues

---

### 3.7 `enhanced_search_executor`

**Type:** `LlmAgent` + `BuiltInPlanner(thinking_config=include_thoughts=True)`
**Model:** `config.worker_model`
**Tools:** `google_search`
**Callback:** `collect_research_sources_callback`

**Behavior:**
1. Read `research_evaluation.follow_up_queries`
2. Execute ALL follow-up queries
3. Synthesize new findings
4. COMBINE with existing `section_research_findings`
5. Output the complete improved set

---

### 3.8 `report_composer`

**Type:** `LlmAgent`
**Model:** `config.critic_model`
**Output key:** `final_cited_report`
**Callback:** `citation_replacement_callback`

**Citation format (REQUIRED):**
```
<cite source="src-ID_NUMBER" />
```
All citations must be in-line, after the claim they support.

**Rules:**
- Follow `report_sections` outline exactly
- Do NOT include "References" or "Sources" section
- All sources cited in-line
- Use ONLY data from `section_research_findings`

**Callback behavior:** `citation_replacement_callback`
- Replaces `<cite source="src-N"/>` with `[Title](url)` markdown links
- Fixes spacing around punctuation

---

## 4. Session State Keys

| Key | Type | Set By | Used By |
|-----|------|--------|---------|
| `research_plan` | str | `interactive_planner_agent` | section_planner, section_researcher |
| `report_sections` | str (markdown) | `section_planner` | report_composer |
| `section_research_findings` | str | `section_researcher`, `enhanced_search_executor` | research_evaluator, report_composer |
| `research_evaluation` | Feedback | `research_evaluator` | escalation_checker, enhanced_search_executor |
| `sources` | dict | `collect_research_sources_callback` | report_composer |
| `final_cited_report` | str | `report_composer` | output |
| `final_report_with_citations` | str | `citation_replacement_callback` | final output |
| `url_to_short_id` | dict | `collect_research_sources_callback` | citation_replacement_callback |

---

## 5. Configuration

| Config Key | Default | Purpose |
|-----------|---------|---------|
| `worker_model` | `gemini-flash-latest` | Research agents |
| `critic_model` | `gemini-flash-latest` | Evaluation agents |
| `max_search_iterations` | `3` | Max loop iterations |

---

## 6. Output Contract

**Final output:** `final_report_with_citations`
- Fully cited markdown report
- Follows `report_sections` outline
- All claims supported by in-line citations
- Citations rendered as `[Title](url)`
- No "References" section
