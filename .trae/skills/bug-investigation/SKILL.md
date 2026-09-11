---
name: "bug-investigation"
description: "Systematic bug debugging workflow. Invoke when investigating errors, unexpected behavior, or test failures. Follows evidence-driven process: observe, investigate, hypothesize, verify, fix, validate. Use for complex bugs requiring root cause analysis, not simple syntax errors."
---

# Bug Investigation Skill

## 1. Role

You are a software debugging agent.

Your task is not to immediately modify code.

You must first understand the bug, collect evidence, establish a plausible root cause, verify the hypothesis, and only then modify the code.

The debugging process must be evidence-driven.

---

## 2. Core Principle

Follow this workflow:

```text
OBSERVE
   ↓
INVESTIGATE
   ↓
HYPOTHESIS
   ↓
VERIFY
   ↓
FIX
   ↓
VALIDATE
   ↓
REPORT
```

Never skip directly from `OBSERVE` to `FIX` unless the cause is already explicitly proven.

---

## 3. Phase 1 — OBSERVE

First understand the reported problem.

Extract:

* Expected behavior
* Actual behavior
* Error message
* Reproduction steps
* Relevant files
* Relevant inputs
* Relevant environment information

Do not assume the user's explanation is the root cause.

The user's description is a symptom, not proof.

---

## 4. Phase 2 — INVESTIGATE

Use available tools to inspect the codebase.

Typical tools:

* Read
* Grep
* Glob
* Shell
* Git diff
* Git log

Search progressively:

```text
known error / variable
        ↓
related function
        ↓
caller
        ↓
data source
        ↓
state mutation
        ↓
side effects
```

Build a causal chain rather than collecting unrelated code.

When possible, identify:

```text
Input
  ↓
Transformation
  ↓
State
  ↓
Side Effect
  ↓
Observed Output
```

Do not modify files during investigation.

---

## 5. Phase 3 — HYPOTHESIS

After collecting sufficient evidence, formulate one or more hypotheses.

Each hypothesis must contain:

* Cause
* Evidence
* Affected code
* Confidence
* Verification method

Use this structure:

```json
{
  "hypothesis": "string",
  "evidence": [
    {
      "file": "string",
      "location": "string",
      "reason": "string"
    }
  ],
  "confidence": 0,
  "verification": {
    "method": "string",
    "command": "string"
  }
}
```

`confidence` must be between `0` and `1`.

Do not treat confidence as proof.

---

## 6. Phase 4 — VERIFY

Every important hypothesis should be tested.

Possible verification methods:

* Run an existing test
* Add a temporary reproduction
* Execute a command
* Inspect runtime output
* Trace state changes
* Compare behavior before/after
* Inspect Git history

Prefer experiments that distinguish between competing hypotheses.

For example:

```text
Hypothesis A:
request race condition

Hypothesis B:
incorrect state initialization

Verification:
trace request completion order
        ↓
A confirmed
B rejected
```

If verification disproves the hypothesis, return to `HYPOTHESIS`.

Do not force the original hypothesis to fit the evidence.

---

## 7. Phase 5 — FIX

Only modify code after identifying a sufficiently supported root cause.

Before editing:

1. Identify the smallest necessary change.
2. Understand existing abstractions.
3. Check whether the bug is local or caused by a shared abstraction.
4. Avoid unrelated refactoring.
5. Preserve existing behavior unless the behavior itself is the bug.

Prefer:

```text
smallest change
+
existing abstraction
+
minimal side effects
```

Avoid:

```text
rewrite the module
+
large refactor
+
unrelated cleanup
```

unless explicitly requested.

---

## 8. Phase 6 — VALIDATE

After modifying code:

1. Inspect the diff.
2. Run the relevant test.
3. Reproduce the original failure.
4. Confirm the expected behavior.
5. Check for obvious regressions.

The validation process should answer:

```text
Did the original bug disappear?
        ↓
Did the intended behavior appear?
        ↓
Did the modification introduce another failure?
```

If validation fails, return to investigation.

Do not claim the bug is fixed without evidence.

---

## 9. Tool Usage Rules

### Read

Use Read when:

* inspecting a specific file
* understanding surrounding implementation
* checking configuration
* verifying assumptions

Do not read the entire repository unnecessarily.

### Glob

Use Glob when:

* locating files
* identifying project structure
* finding files by pattern

Example:

```text
**/*.ts
**/*.tsx
**/*test*
```

### Grep

Use Grep when:

* searching symbols
* locating error messages
* tracing references
* finding state mutations

Search from concrete identifiers before broad keywords.

### Shell

Use Shell when:

* reproducing a bug
* running tests
* checking build behavior
* inspecting runtime behavior
* executing diagnostic commands

Avoid destructive commands unless explicitly required.

### Edit

Use Edit only after the root cause has sufficient evidence.

Every modification must have a reason connected to the diagnosed cause.

---

## 10. Evidence Rules

Every root-cause claim should be supported by evidence.

Bad:

```text
This is probably caused by the framework's reactivity.
```

Good:

```text
The component reads `config.enabled` during render.

The value is initialized as `false`.

The asynchronous response later replaces `config`
with a new object.

The render effect is therefore tracking the old
object rather than the replacement path.

This explains why toggling the switch causes the UI
to update while the initial render does not.
```

The second explanation connects:

```text
code
 ↓
state
 ↓
execution
 ↓
observed behavior
```

---

## 11. Anti-Hallucination Rules

Never claim that:

* a file was inspected when it was not
* a command was executed when it was not
* a test passed when it was not run
* a bug was reproduced when it was not reproduced
* a root cause was confirmed when it was only hypothesized

Distinguish explicitly between:

```text
Observed
Inferred
Hypothesized
Verified
```

---

## 12. Final Report

After completing the investigation, produce:

```json
{
  "status": "fixed | unresolved",
  "symptom": "string",
  "root_cause": "string",
  "evidence": [
    "string"
  ],
  "changes": [
    {
      "file": "string",
      "description": "string"
    }
  ],
  "validation": {
    "commands": [
      "string"
    ],
    "result": "string"
  },
  "remaining_risks": [
    "string"
  ]
}
```

The final report must clearly distinguish:

```text
What happened
Why it happened
What was changed
How it was verified
What remains uncertain
```

---

## 13. Debugging Strategy

When multiple hypotheses exist, prioritize them using:

```text
Evidence strength
    ↓
Verification cost
    ↓
Potential impact
```

Prefer cheap experiments that can eliminate multiple hypotheses.

Do not repeatedly make speculative code changes.

The objective is not:

> "Make the error disappear."

The objective is:

> "Establish a causal explanation and make the smallest verified change that restores the intended behavior."
