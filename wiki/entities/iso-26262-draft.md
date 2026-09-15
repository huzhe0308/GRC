---
title: ISO 26262 (Draft) Road vehicles — Functional safety
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [functional-safety, iso-standard, requirement, draft]
sources: ['raw/papers/ISO-TC 22-SC 32-WG 8_N1366_ISO WD 26262-04_BL01_20250530.md']
confidence: high
---

# ISO 26262 (Draft) Road vehicles — Functional safety

## Overview

This is a working draft (WD) of ISO 26262 Part 4 (Product development at the system level), circulated by ISO/TC 22/SC 32/WG 8 for the first commenting cycle (Ballot 01). The draft represents the third edition of the ISO 26262 functional safety standard series, which provides a framework for developing safety-related electrical/electronic (E/E) systems in road vehicles. This edition cancels and replaces the second edition (2018), incorporating significant extensions including SOTIF considerations, motorcycle/truck/bus adaptations, semiconductor guidance, and cybersecurity references. Part 4 specifically addresses product development at the system level — the central V-model phase connecting concept, hardware, and software development.

## Key Facts

| Field | Value |
|-------|-------|
| Standard Number | ISO WD 26262-4 (Working Draft, Ballot 01) |
| Document Reference | ISO/TC 22/SC 32/WG 8 N 1366 |
| Full Title | Road vehicles — Functional safety — Part 4: Product development at the system level |
| Document Date | 2025-05-30 |
| Comment Deadline | 2025-07-28 |
| Issuing Committee | ISO/TC 22/SC 32/WG 8 (Functional Safety) |
| Convenor | Knapp Andreas (DIN), Mercedes-Benz |
| Comment Coordinator | Egbert Fritzsche (VDA) |
| Status | Working Draft — 1st commenting cycle |
| Edition | Third edition (replaces ISO 26262:2018) |

## Scope and Requirements

- **Scope**: Applies to safety-related systems including one or more E/E systems installed in series production road vehicles (excluding mopeds). Does not address unique E/E systems in special vehicles (e.g., for drivers with disabilities).
- **Exemptions**: Systems released for production or already under development prior to publication are exempted; alterations to existing systems addressed through lifecycle tailoring.
- **Hazards Covered**: Addresses hazards caused by malfunctioning behaviour of safety-related E/E systems, including electric shock, fire, smoke, heat, radiation, toxicity, flammability, reactivity, corrosion, and release of energy — only when directly caused by E/E system malfunctions or when E/E systems contribute to prevention/control/mitigation.
- **System-Level Development** (Clause 5): Specifies requirements for:
  - General topics for initiation of product development at system level
  - Functional safety concept at system level (Clause 6)
  - System architectural design
  - Item integration and testing (Clause 7)
  - Safety validation
- **ASIL-Dependent Requirements** (§4.4): Requirements met for ASIL A, B, C, and D unless stated otherwise; ASIL decomposition per Part 9 Clause 5; parenthetical ASIL notation indicates recommendation rather than requirement.
- **Compliance** (§4.2): When claiming compliance, each requirement shall be met unless (a) tailoring per Part 2 shows non-applicability, or (b) rationale for non-compliance is acceptable per Part 2 evaluation.
- **Method Tables** (§4.3): Methods rated "++" (highly recommended), "+" (recommended), or "o" (no recommendation); consecutive entries all apply; alternative entries require appropriate combination per ASIL.

## Technical Details

- **Key Changes from 2018 Edition**:
  - Extensions to address nominal performance of E/E systems including SOTIF (Safety of the Intended Functionality) considerations per ISO 21448
  - Requirements for trucks, buses, trailers, and semi-trailers
  - Extension of vocabulary and more detailed objectives
  - Objective-oriented confirmation measures
  - Management of safety anomalies
  - References to cybersecurity
  - Updated target values for hardware architecture metrics
  - Guidance on model-based development and software safety analysis
  - Evaluation of hardware elements
  - Additional guidance on dependent failure analysis
  - Guidance on fault tolerance, safety-related special characteristics, and software tools
  - Guidance for semiconductors
  - Requirements for motorcycles
  - General restructuring of all parts for improved clarity
- **Normative References**: ISO 26262-1:2018 (Vocabulary), -2 (Management), -3 (Concept), -5 (Hardware), -6 (Software), -7 (Production/Operation), -8 (Supporting processes), -9 (ASIL-oriented analyses).
- **Motorcycle Adaptation** (§4.5): For motorcycle items, ISO 26262-12 requirements supersede corresponding Part 4 requirements.
- **T&B Adaptation** (§4.6): Content unique to trucks, buses, trailers, and semi-trailers is indicated as such.
- **V-Model Structure**: Shaded V's in Figure 1 show interconnection among Parts 3, 4, 5, 6, and 7; motorcycle clauses from Part 12 (Clauses 9-10) support Part 4.
- **Annexes**: Annex A (informative) overview/workflow of system-level development; Annex B (informative) example HSI contents.

^[raw/papers/ISO-TC 22-SC 32-WG 8_N1366_ISO WD 26262-04_BL01_20250530.md]

## Source Documents

- [ISO-TC 22-SC 32-WG 8_N1366_ISO WD 26262-04_BL01_20250530.md](raw/papers/ISO-TC 22-SC 32-WG 8_N1366_ISO WD 26262-04_BL01_20250530.md)

## Cross-References

- [[gb-t-34590-series]]
- [[gb-t-44721-2024]]
- [[vda-450]]
- [[gb-t-43267-2023]]
