---
title: GB/T 33594 道路车辆系统理论过程安全分析方法
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [functional-safety, gbt-standard, draft, safety-analysis, glossary]
sources: ['raw/papers/FuSa_48_GB+T_33594-2025.md', 'raw/papers/FuSa_52_GB+T_33594-WD_draft_道路车辆+系统理论过程安全分析方法.md']
confidence: high
---

# GB/T 33594 道路车辆系统理论过程安全分析方法

## Overview

GB/T 33594 is a Chinese national standard specifying the System Theoretic Process Analysis (STPA) method for road vehicle safety analysis (道路车辆 系统理论过程安全分析方法). STPA is a safety analysis approach based on a system-theoretic accident model that identifies potential causes of accidents during development, including unsafe interactions between system components — not just component failures. The working group discussion draft (dated 20260529) defines the full STPA methodology applicable to safety-related systems containing electronic/electrical components on road vehicles. The standard covers functional safety, SOTIF, AI safety, and other safety domains. A published 2025 version also exists (image-only PDF). STPA can identify "unknown unknowns" early in the concept phase before they become operational problems.

## Key Facts

| Field | Draft Version | Published Version |
|-------|---------------|-------------------|
| Standard Number | GB/T XXXXX-XXXX (draft) | GB/T 33594-2025 |
| Full Title (CN) | 道路车辆 系统理论过程安全分析方法 | (same) |
| Full Title (EN) | Road Vehicles — System theoretic process safety analysis methods | (same) |
| ICS | 43.040 | 43.040 |
| CCS | T35 | T35 |
| Draft Stage | 工作组讨论稿 (Working group discussion draft, 20260529) | Published 2025 |
| Proposed by | 中华人民共和国工业和信息化部 (MIIT) | — |
| Managed by | SAC/TC114 (全国汽车标准化技术委员会) | — |
| Source Format | Full text, 2,225 lines | Image-only PDF |
| Normative References | GB/T 34590.1–34590.12, GB/T 43267 | — |

## Scope and Requirements

- **Scope (Clause 1):** Defines STPA as a safety analysis method based on system-theoretic accident models. Applicable to safety-related systems with electronic/electrical components on road vehicles. Covers functional safety, SOTIF, AI safety, structural safety, information security, and combinations thereof.
- **STPA Foundation (3.1.1):** Based on extended accident causation model — assumes accidents can be caused by unsafe component interactions (not just component failures). Can handle complex systems including software and human operators. Identifies "unknown unknowns" early in concept phase.
- **Key Terms (Clause 3):** Accident (事故), Constraint (约束), Control Action (控制行为), Control Structure (控制结构), Controller (控制器), UCA (不安全控制行为), Controller Constraint (控制器约束), Controlled Process (受控过程), Loss (损失), Loss Scenario (损失场景), Causal Factor (致因因素), Process Model (过程模型), System Level (系统级), System Level Constraint (系统级约束), System Level Hazard (系统级危害).
- **Four STPA Steps (Clause 4.2, Figure 1):**
  1. **Define Purpose and Scope (4.3):** System purpose, operating mode, expected goals, constraints, participants. Identify system assumptions, define system boundary and elements. Identify potential losses (L-1 through L-5), system-level hazards (Haz-1 through Haz-n), and derive system-level constraints (SLC-1 through SLC-n).
  2. **Create Control Structure (4.4):** Hierarchical model of controllers, controlled processes, control actions, and feedback. Minimum five element types: controller, control action, feedback, other I/O, controlled process. May include human operators and external environment.
  3. **Identify Unsafe Control Actions (4.5):** Four UCA categories: (a) not provided causing hazard; (b) provided causing hazard; (c) provided too early/late or wrong order; (d) stopped too early or duration too long. Guideword-based identification (Table 3). UCA format: source + context + type + control action + hazard link.
  4. **Identify Loss Scenarios (4.6):** Scenarios leading to UCAs; identify causal factors; refine controller constraints. Iterative process with traceability.
- **System-Level Hazard Examples:** Haz-1: Vehicle fails to maintain safe distance from nearby objects [L-1, L-2]; Haz-2: Vehicle enters dangerous area [L-1, L-2]; Haz-3: Vehicle exceeds safe operating envelope (speed, lateral/longitudinal forces) [L-1, L-2]; Haz-4: Vehicle occupants exposed to harmful influences [L-1, L-2].
- **Sub-Hazard Refinement (4.3.6):** Haz-1 decomposed into: deceleration (Haz-1.1–1.3), acceleration (Haz-1.4–1.6), steering (Haz-1.7–1.9) — each with "less than expected," "exceeds expected," and "unintended provision."
- **UCA Guidewords (Table 3, 4.5.1.2):** Four columns: not provided → hazard; provided → hazard; too early/late/wrong order → hazard; stopped too early/duration too long → hazard.
- **Control Structure (4.4):** Functional model (not physical model). Hierarchical: highest-level controller → intermediate controllers → controlled process. Each layer imposes constraints on the layer below; feedback flows upward. Control structure iteration sequence: build → identify UCAs → identify loss scenarios → formulate constraints → update functional design → assign new functions/control actions.
- **Annex A (informative):** STPA application example for advanced CDA (领航组合驾驶辅助系统) — includes detailed control structure with driver, system, and environment interactions.
- **Annex B (informative):** STPA application example for automated parking system.
- **Annex C (informative):** Extended guidewords for UCA identification (HAZOP-style).
- **HARA Integration:** HARA-identified hazards can be used directly in STPA to avoid duplicate work (4.3.5.2 note).

## Technical Details

| Parameter | Value |
|-----------|-------|
| STPA steps | 4 (purpose/scope → control structure → UCA → loss scenarios) |
| UCA categories | 4 (not provided, provided, timing/order, duration) |
| Loss categories | 5 (L-1 through L-5) |
| Control structure element types | 5 (controller, control action, feedback, other I/O, controlled process) |
| Guideword columns | 4 (not provided, provided, too early/late/order, stopped early/long) |

## Source Documents

- [FuSa_48_GB+T_33594-2025.md](raw/papers/FuSa_48_GB+T_33594-2025.md) — image-only PDF (binary)
- [FuSa_52_GB+T_33594-WD_draft.md](raw/papers/FuSa_52_GB+T_33594-WD_draft_道路车辆+系统理论过程安全分析方法.md) — full text, 2,225 lines

^[raw/papers/FuSa_52_GB+T_33594-WD_draft_道路车辆+系统理论过程安全分析方法.md]

## Cross-References

- [[gb-t-34590-series]]
- [[gb-t-43267-2023]]
- [[gb-t-43253-series]]
- [[gb-t-44719-2024]]
- [[fusa-wd-drafts]]
