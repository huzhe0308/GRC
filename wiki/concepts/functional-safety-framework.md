---
title: Functional Safety Framework (FuSa)
created: 2026-08-06
updated: 2026-08-06
type: concept
tags: [functional-safety, overview, glossary]
sources: [raw/papers/FuSa_29_GB+T_34590-1-2022.md, raw/papers/FuSa_6_GB+T_43267-2023.md, raw/articles/Functional Safety Overview_2026 Q2.md]
confidence: high
---

# Functional Safety Framework (FuSa)

## Definition

Functional safety addresses the absence of unreasonable risk caused by hazards resulting from
malfunctioning behaviors of electrical/electronic (E/E) systems in road vehicles. It is distinct
from cybersecurity (which addresses intentional threats) and SOTIF (which addresses performance
insufficiencies without system malfunction).

## Regulatory Landscape

### Core Standards

1. **[[gb-t-34590-series]]** — Chinese adaptation of ISO 26262, 11 parts covering:
   vocabulary, management of functional safety, concept phase, product development at system level,
   hardware, software, production, supporting processes, ASIL-oriented guidelines, and guidelines
   on [[gb-t-44721-2024]]. ^[raw/papers/FuSa_29_GB+T_34590-1-2022.md]

2. **[[iso-26262-draft]]** — The original ISO 26262 international standard, currently under
   revision (working draft for Part 4). ^[raw/papers/ISO-TC 22-SC 32-WG 8_N1366_ISO WD 26262-04_BL01_20250530.md]

3. **[[gb-t-43267-2023]]** — SOTIF (Safety of the Intended Functionality), adapted from
   ISO 21448:2022. Addresses hazards from system performance limitations, not malfunctions.
   ^[raw/papers/FuSa_6_GB+T_43267-2023.md]

### Supporting Standards

- **[[gb-t-43253-series]]** — Functional safety audit and assessment methods (4 parts: general,
  concept/system level, software level, hardware level)
- **[[gb-t-44461-series]]** — New FuSa standards replacing parts of [[gb-t-44721-2024]]
- **[[gb-z-42285-2022]]** — Guidelines for ASIL determination
- **[[gb-t-39263-series]]** — STPA-based control system safety analysis
- **[[gb-t-33594-series]]** — System theory process safety analysis
- **[[vda-450]]** — Electrical power supply for automated driving in ISO 26262 context

### Domain-Specific FuSa Standards

- **Braking:** [[gb-21670-braking]], [[gb-12676-braking]], [[un-r13-braking]]
- **Steering:** [[gb-17675-steering]], [[un-r79-steering]]
- **EV Battery:** [[gb-t-39086-2020]]
- **EV Safety:** [[gb-18384-2025]]
- **Testing:** [[gb-t-44850-2024]] (ICV driving safety tests)

## Key Concepts

- **ASIL (Automotive Safety Integrity Level):** Risk classification A (lowest) to D (highest)
- **HARA (Hazard Analysis and Risk Assessment):** Process of identifying hazards and assigning ASIL
- **Safety Goal:** Top-level safety requirement derived from hazard analysis
- **Safety Concept:** Architecture and requirements to satisfy safety goals
- **SOTIF:** Addresses hazards from expected function performance insufficiencies (sensor limitations,
  algorithmic inadequacy) rather than system malfunction
- **STPA:** System-Theoretic Process Analysis — hazard analysis method for complex control systems

## Additional Functional Safety Standards

The following standards are part of the broader
functional safety ecosystem but have narrower scope:

- [[gb-11562-2025]]
- [[gb-t-30677-2014]]
- [[gb-t-35360-2017]]
- [[gb-t-39323-2020]]
- [[gb-t-41797-2022]]
- [[gb-t-41798-2022]]
- [[gb-t-43254-2023]]
- [[gb-t-43758-series]]
- [[gb-t-43766-2024]]
- [[gb-t-44298-2024]]
- [[gb-t-44719-2024]]
- [[gb-t-45312-2025]]
- [[gb-t-45829-2025]]
- [[gb-t-47001-2025]]
- [[gb-t-47031-2026]]
- [[gb-t-47341-2026]]
- [[gb-t-47351-2026]]

## Cross-References

- [[vehicle-cybersecurity-framework]] — Related cybersecurity domain
- [[functional-safety-overview]] — Landscape overview 2026 Q2
- [[fusa-wd-drafts]] — Upcoming standards replacing existing ones
- [[gb-t-39901-series]] — Additional FuSa standard (2021/2025)
- [[fusa-vs-cybersecurity-vs-sotif]] — Comparison of FuSa vs Cybersecurity vs SOTIF
