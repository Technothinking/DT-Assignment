# Deterministic Reflection Agent (No LLM at Runtime)

## Live Demo
https://dt-assignment-v46w.vercel.app/

Note:The backend is hosted on Render and may take ~15-30 seconds to start due to cold starts.

## Overview

This project implements a **deterministic end-of-day reflection tool** that guides users through a structured conversation across three psychological axes:

* **Locus (Victim ↔ Victor)** — Agency and control
* **Orientation (Entitlement ↔ Contribution)** — Behavior toward others
* **Radius (Self ↔ Others)** — Perspective and impact

Unlike AI-based tools, this system uses **no LLM at runtime**. All logic is encoded in a decision tree, ensuring predictable, auditable, and consistent reflections.

The project includes both CLI and web interfaces.

---

## Key Idea

A **deterministic tree-walking agent** where:
* Each node = question, reflection, or transition
* Fixed options (no free text)
* Predefined paths based on selections
* Signals track behavioral tendencies

Result: Conversational feel with full determinism.

---

## Project Structure

```
/README.md                     # This file
/write-up.md                   # Design rationale
/tree/reflection-tree.json     # Core decision tree
/agent/
  engine.py                   # Core logic
  main.py                     # CLI interface
/api/app.py                   # FastAPI backend
/frontend/                    # React web app
/transcripts/                 # Sample conversations
```

---

## How to Run

### Web App (Recommended)
```bash
# Backend
cd api && uvicorn app:app --reload --host 127.0.0.1 --port 8000

# Frontend (new terminal)
cd frontend && npm install && npm start
```
Open `http://localhost:3000`

### CLI
```bash
cd agent && python main.py
```

---

## How It Works

### Tree Loading
Loads decision tree defining nodes, options, transitions, and signals.

### State Management
* `answers`: User selections
* `axis1`: Internal vs external
* `axis2`: Contribution vs entitlement
* `axis3`: Self vs others

### Flow
Questions → Signals → Decisions → Reflections → Summary

Fully deterministic and traceable.

---

## Axes Design

### Axis 1: Locus
Surfaces agency through reaction-based questions.
Signals: Internal (control) vs External (circumstances)

### Axis 2: Orientation
Reveals focus on giving vs receiving.
Signals: Contribution vs Entitlement

### Axis 3: Radius
Expands from self → others → impact.
Signals: Self vs Others

---

## Example Flow

Start → Axis 1 → Bridge → Axis 2 → Bridge → Axis 3 → Summary → End

---

## Transcripts

Two sample runs demonstrate different paths:
- **Persona 1**: External/Entitled/Self-focused
- **Persona 2**: Internal/Contributing/Others-focused

---

## Design Principles

* **Determinism over generation** (no LLM)
* **Structured thinking** (trees encode psychology)
* **Guided reflection** (insight, not evaluation)
* **No moralizing** (reframe without judgment)

---

## Summary

Demonstrates encoding human reflection into structured systems. Guides thinking through design, surfaces patterns through structure, delivers consistent insight via determinism. Web interface makes it accessible while maintaining core philosophy.
