---
title: GB/T 34590-2022 道路车辆功能安全 (ISO 26262 MOD)
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [functional-safety, gbt-standard, requirement, glossary]
sources: ['raw/papers/FuSa_29_GB+T_34590-1-2022.md', 'raw/papers/FuSa_37_GB+T_34590-2-2022.md', 'raw/papers/FuSa_37_GB+T_34590-3-2022.md']
confidence: high
---

# GB/T 34590-2022 道路车辆功能安全 (ISO 26262 MOD)

## Overview

GB/T 34590-2022 is the Chinese national standard modifying and adopting ISO 26262:2018, covering the functional safety of electrical/electronic (E/E) systems on road vehicles. The 2022 revision replaces the 2017 version, expanding scope from "mass-produced passenger cars" (量产乘用车) to "mass-produced road vehicles excluding mopeds" (除轻便摩托车外的量产道路车辆). The standard consists of 12 parts spanning the entire automotive safety lifecycle from concept phase through production, operation, service, and decommissioning. It provides a risk-based methodology using ASIL (Automotive Safety Integrity Level, A–D with QM), requirements for functional safety management, design, implementation, verification, validation, and assessment, plus guidelines for semiconductors and motorcycles.

## Key Facts

| Field | Value |
|-------|-------|
| Standard Number | GB/T 34590-2022 (12 parts) |
| Full Title (CN) | 道路车辆 功能安全 |
| Full Title (EN) | Road vehicles — Functional safety |
| Based On | ISO 26262:2018 (MOD) |
| Published Date | 2022-12-30 |
| Effective Date | 2023-07-01 |
| Supersedes | GB/T 34590-2017 |
| Issuing Body | 国家市场监督管理总局、国家标准化管理委员会 |
| Proposed by | 中华人民共和国工业和信息化部 |
| Managed by | SAC/TC114 (全国汽车标准化技术委员会) |
| Scope | Mass-produced road vehicles excluding mopeds |
| ICS | 43 |
| CCS | T35 |

## 12-Part Structure

| Part | Title | Key Changes from 2017 |
|------|-------|----------------------|
| Part 1 | Terms and definitions (术语) | 92 terms modified, 51 added (incl. ASIL capability, FTTI, SEooC, T&B vehicles); 6 removed; 7 abbreviations changed, 59 added (incl. ADC, DMA, SEooC, SoC) |
| Part 2 | Management of functional safety | Expanded scope to trucks/buses/special vehicles/trailers; motorcycle adaptation (Part 12); recognition measures, item-level impact analysis, production release concepts |
| Part 3 | Concept phase | Severity/controllability classification updates; QM requirements; T&B HARA difference management; assumption identification during HARA |
| Part 4 | Product development: system level | Referenced |
| Part 5 | Product development: hardware level | Referenced |
| Part 6 | Product development: software level | Referenced |
| Part 7 | Production, operation, service, decommissioning | Referenced |
| Part 8 | Supporting processes | Referenced |
| Part 9 | ASIL-oriented and safety-oriented analysis | Referenced |
| Part 10 | Guidelines | Referenced |
| Part 11 | Semiconductor application guidelines | Referenced |
| Part 12 | Adaptation for motorcycles | New in 2022 |

## Scope and Requirements

- Provides automotive safety lifecycle (development, production, operation, service, decommissioning) with tailoring support
- Defines ASIL risk-based analysis methodology (A–D, with QM for quality management)
- **Part 1 (Vocabulary)**: Defines 143+ terms including architecture, ASIL decomposition, cascading failure, common cause failure, diagnostic coverage, distributed development, fault model, FTTI, hardware architectural metrics, independence, latent fault, random hardware failure, safety goal, safety case, safety culture, safety mechanism, safety-related special characteristics, SEooC
- **Part 2 (Management)**: Overall safety management (organizational requirements, safety culture, quality management), project-specific safety management (safety lifecycle, safety case, impact analysis, confirmation measures — review, audit, assessment), production release, and production/service/decommissioning management; includes motorcycle (4.5) and T&B vehicle (4.6) applicability
- **Part 3 (Concept phase)**: Item definition (boundary, interface, assumptions), hazard analysis and risk assessment (HARA), functional safety concept; includes severity classification, controllability estimation, safety goal determination, T&B vehicle HARA difference management
- Addresses systematic failures and random hardware failures
- Provides framework for safety-related systems based on other technologies (mechanical, hydraulic, pneumatic)
- T&B vehicle adaptation aligned with GB/T 3730.1-2022 vehicle type definitions (载货汽车, 客车, 专用汽车, 挂车)

^[raw/papers/FuSa_29_GB+T_34590-1-2022.md]
^[raw/papers/FuSa_37_GB+T_34590-2-2022.md]
^[raw/papers/FuSa_37_GB+T_34590-3-2022.md]

## Source Documents

- [FuSa_29_GB+T_34590-1-2022.md](raw/papers/FuSa_29_GB+T_34590-1-2022.md)
- [FuSa_37_GB+T_34590-2-2022.md](raw/papers/FuSa_37_GB+T_34590-2-2022.md)
- [FuSa_37_GB+T_34590-3-2022.md](raw/papers/FuSa_37_GB+T_34590-3-2022.md)

## Cross-References

- [[iso-sae-21434-2021]]
- [[gb-t-44461-series]]
- [[gb-t-43267-2023]]
- [[gb-z-42285-2022]]
- [[gb-t-43254-2023]]
