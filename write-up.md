# Deterministic Reflection Agent — Design Write-up

## 1. Overview

This project implements a deterministic end-of-day reflection tool that guides an employee through a structured conversation across three psychological axes: **Locus (agency), Orientation (contribution), and Radius (perspective)**.

The core idea is to transform abstract psychological concepts into a **navigable decision tree**, where each question, option, and reflection is predefined. The system does not rely on any runtime AI/LLM calls. Instead, it encodes insight directly into structure, ensuring that the same inputs always lead to the same outputs.

The result is a reflection experience that is **predictable, auditable, and consistent**, while still feeling personal and thoughtful.

---

## 2. Design Philosophy

### 2.1 Determinism over Generation

The system avoids free-text input and AI interpretation entirely. Every interaction is based on fixed options, and all branching is explicitly defined. This eliminates ambiguity and ensures reliability across sessions.

### 2.2 Reflection as a Conversation, Not a Survey

A key design goal was to make the experience feel like a guided conversation rather than a checklist. This is achieved through:

* Progressive questioning (broad → specific → reflective)
* Context-aware reflections based on prior answers
* Smooth transitions (bridge nodes) between axes

### 2.3 Awareness without Judgment

The tree is designed to surface patterns (e.g., external locus, entitlement) without labeling or judging the user. Reflections are framed as observations rather than evaluations, allowing the user to arrive at insights independently.

---

## 3. Axis Design

### 3.1 Axis 1: Locus (Victim vs Victor)

**Objective:** Help the user recognize their degree of agency in the day’s events.

**Design Approach:**

* Start with an emotional anchor (“How was your day?”)
* Branch into different follow-ups based on tone (positive vs negative)
* Surface agency through questions about reactions and control

**Key Trade-off:**
Instead of directly asking “Did you take responsibility?”, the design uses indirect questions (e.g., reactions, control points) to avoid defensiveness.

**Insight Mechanism:**
Users begin to notice that even in difficult situations, they made choices — introducing the idea of agency without forcing it.

---

### 3.2 Axis 2: Orientation (Contribution vs Entitlement)

**Objective:** Shift focus from “What did I get?” to “What did I give?”

**Design Approach:**

* Start with a real interaction (grounded in experience)
* Introduce subtle “entitlement traps” (e.g., “others weren’t doing enough”)
* Use a deep question to surface missed opportunities for contribution

**Key Trade-off:**
Explicitly calling out entitlement would feel accusatory. Instead, the design uses contrast and reflection to gently redirect attention toward contribution.

**Insight Mechanism:**
Users realize that even when others fall short, they still have opportunities to contribute.

---

### 3.3 Axis 3: Radius (Self → Others → System)

**Objective:** Expand the user’s perspective beyond self to others and broader impact.

**Design Approach:**

* Begin with “who comes to mind” (natural cognitive framing)
* Progressively introduce impact awareness
* Use perspective-taking (“someone else’s view”) as the key shift

**Key Trade-off:**
Rather than forcing empathy, the design enables it through structured perspective shifts.

**Insight Mechanism:**
Users recognize that their work affects others — teammates, outcomes, and end users — increasing meaning and context.

---

## 4. Branching Logic

Branching is implemented using:

* **Option-based routing** (nextMap)
* **Signal accumulation** (axis-wise tallies)
* **Decision nodes** (conditional routing based on dominant signals)

This allows the system to:

* Adapt reflections to user behavior
* Maintain determinism (no randomness)
* Keep logic transparent and traceable

---

## 5. State and Signals

The system maintains a simple state:

* User answers (for interpolation)
* Axis signals (internal/external, contribution/entitlement, self/others)

Signals are incremented based on selected options. At key points, the system determines the dominant tendency and routes accordingly.

This approach avoids complex scoring models while still capturing meaningful patterns.

---

## 6. Summary Design

The summary synthesizes all three axes into a single reflection.

Instead of reporting scores, it:

* Translates axis results into natural language
* Connects behavior → interaction → perspective
* Suggests that small changes can influence future experience

This ensures the session ends with **insight, not evaluation**.

