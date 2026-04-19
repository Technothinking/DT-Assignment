# Deterministic Reflection Agent (No LLM at Runtime)

## Overview

This project implements a **deterministic end-of-day reflection tool** that guides an employee through a structured conversation across three psychological axes:

* **Locus (Victim ↔ Victor)** — How you handled situations
* **Orientation (Entitlement ↔ Contribution)** — How you showed up for others
* **Radius (Self ↔ Others)** — How you perceived impact

Unlike typical AI-based tools, this system does **not use any LLM at runtime**.
All intelligence is encoded into a **decision tree**, ensuring:

* Predictable behavior
* Auditable logic
* Consistent reflections

The same inputs will always produce the same outputs.

---

## Key Idea

The system is built as a **deterministic tree-walking agent**:

* Each node represents a question, reflection, or transition
* Each question has **fixed options** (no free text)
* Each option leads to a **predefined next node**
* Signals are accumulated to track behavioral tendencies

The result is a guided reflection that feels conversational while remaining fully deterministic.

---

## Project Structure

```
/tree/
  reflection-tree.json        # Core decision tree (the product)
/agent/
  main.py                     # CLI engine to run the tree
/transcripts/
  persona-1.md                # External / Entitled / Self-focused
  persona-2.md                # Internal / Contributing / Others-focused
write-up.md                   # Design rationale (Part A)
README.md                     # This file
```

---

## How to Run

### 1. Clone the repository

```
git clone <repo-link>
cd <repo-name>
```

### 2. Navigate to agent

```
cd agent
```

### 3. Run the program

```
python main.py
```

---

## How It Works

### 1. Tree Loading

The engine loads the reflection tree from:

```
/tree/reflection-tree.json
```

The tree defines:

* Node types (question, decision, reflection, etc.)
* Options and transitions
* Signals for axis tracking

---

### 2. State Management

The system maintains:

* `answers` → user selections (for interpolation)
* `axis1` → internal vs external
* `axis2` → contribution vs entitlement
* `axis3` → self vs others

---

### 3. Deterministic Flow

* Questions → user selects option
* Signals → update axis scores
* Decisions → route based on conditions
* Reflections → shown based on path

No randomness. No AI calls. Fully traceable.

---

## Axes Design

### Axis 1: Locus (Victim ↔ Victor)

Focus: **Agency**

* Identifies whether the user sees events as happening *to them* or *through them*
* Uses reaction-based questions to surface control

---

### Axis 2: Orientation (Entitlement ↔ Contribution)

Focus: **Behavior toward others**

* Surfaces whether the user focuses on receiving or giving
* Uses subtle framing to reveal entitlement without judgment

---

### Axis 3: Radius (Self ↔ Others)

Focus: **Perspective**

* Expands awareness from self → team → impact
* Uses perspective-taking to introduce meaning

---

## Example Flow

```
Start → Axis 1 → Axis 2 → Axis 3 → Summary → End
```

Each axis builds on the previous one:

* Agency → Contribution → Impact

---

## Transcripts

Two sample runs are included:

1. **Persona A**

   * External locus
   * Entitlement-oriented
   * Self-focused

2. **Persona B**

   * Internal locus
   * Contribution-oriented
   * Others-focused

These demonstrate how different inputs produce different deterministic paths.

---

## Design Principles

* **Determinism over generation**
  No LLM usage at runtime

* **Structured thinking**
  Psychological concepts encoded as trees

* **Guided reflection**
  Questions lead to insight, not evaluation

* **No moralizing**
  Reflections reframe without judging

---

## Limitations & Future Work

* Deeper branching for edge cases
* UI-based interaction (web/mobile)
* Long-term tracking of reflections
* More nuanced cross-axis reflections

---

## Author

Nitish

---

## Summary

This project demonstrates how **human reflection can be encoded into structured systems**.

Instead of generating answers dynamically, the system:

* Guides thinking through design
* Surfaces patterns through structure
* Delivers consistent insight through determinism

---
