---
title: GB/T 39263 道路车辆控制系统理论过程安全分析方法
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [functional-safety, gbt-standard, glossary, safety-analysis]
sources: ['raw/papers/FuSa_47_GB+T_39263-2020.md', 'raw/papers/FuSa_51_GB+T_39263-WD_draft_道路车辆+控制系统理论过程安全分析方法.md']
confidence: high
---

# GB/T 39263 道路车辆控制系统理论过程安全分析方法

## Overview

This entry covers two related documents: GB/T 39263-2020, which defines terminology for Advanced Driver Assistance Systems (ADAS), and a WD draft standard (GB/T XXXXX—XXXX) that specifies the System Theoretic Process Analysis (STPA) method for safety-related control systems in road vehicles. GB/T 39263-2020 is the published ADAS terminology standard covering information assistance terms (DFM, TSR, FCW, LDW, BSD, etc.) and control assistance terms (AEB, ACC, LKA, AES, etc.). The STPA draft extends into system-theoretic safety analysis methodology, providing a four-step process for identifying unsafe control actions (UCAs) and loss scenarios across functional safety, SOTIF, cybersecurity, and other technical domains.

## Key Facts

| Field | GB/T 39263-2020 | GB/T XXXXX—XXXX (WD Draft) |
|-------|-----------------|----------------------------|
| Chinese Title | 道路车辆 先进驾驶辅助系统(ADAS)术语及定义 | 道路车辆 控制系统理论过程安全分析方法 |
| English Title | Road vehicles — ADAS — Terms and definitions | Road Vehicles — STPA method of safety related systems |
| Published Date | 2020-11-19 | Draft (2025) |
| Effective Date | 2021-06-01 | TBD |
| ICS | 43 | 43.040 |
| CCS | T04 | T 35 |
| Proposed By | 中华人民共和国工业和信息化部 | 中华人民共和国工业和信息化部 |
| Managed By | SAC/TC114 | SAC/TC114 |
| Applicable Categories | M类、N类和O类车辆 | 除轻便摩托车外的量产道路车辆 |
| Normative References | — | GB/T 34590.1~34590.11—2022, GB/T 43267—2023 |

## Scope and Requirements

### GB/T 39263-2020 (ADAS Terminology)

- **Scope**: Defines terminology for road vehicle ADAS; applies to M, N, and O category vehicles
- **Basic Terms**: ADAS defined as systems using sensing, communication, decision-making, and actuation to assist drivers or actively avoid/mitigate collision hazards
- **Information Assistance Terms** (Section 2.2): DFM (driver fatigue monitoring), DAM (driver attention monitoring), TSR (traffic sign recognition), ISLI (intelligent speed limit information), CSW (curve speed warning), HUD (head-up display), AVM (around view monitoring), NV (night vision), FDM (forward distance monitoring), FCW (forward collision warning), RCW (rear collision warning), LDW (lane departure warning), LCW (lane changing warning), BSD (blind spot detection), SBSD (side blind spot detection), STBSD (steering blind spot detection), RCTA (rear cross traffic alert), FCTA (front cross traffic alert), DOW (door open warning), RCA (reversing condition assist), MALSO (low speed maneuvering aid)
- **Control Assistance Terms** (Section 2.3): AEB (advanced/automatic emergency braking), EBA (emergency braking assist), AES (automatic emergency steering), ESA (emergency steering assist), ISLC (intelligent speed limit control), LKA (lane keeping assist), LCC (lane centering control), LDP (lane departure prevention), IPA (intelligent parking assist), ACC (adaptive cruise control), FSRA (full speed range ACC), TJA (traffic jam assist), AMAP (anti-maloperation for accelerator pedal), ADB (adaptive driving beam), AFL (adaptive front light)

### GB/T XXXXX—XXXX (STPA Draft)

- **Scope**: Specifies STPA-based safety analysis for safety-related systems with E/E components on production road vehicles (excluding mopeds)
- **STPA Four Steps**:
  1. Define analysis purpose and scope — identify losses, system-level hazards, derive system-level constraints
  2. Create control structure — model system as hierarchical control loops with controllers, control actions, feedback, and controlled processes
  3. Identify unsafe control actions (UCAs) — using standard guide words, derive controller constraints
  4. Identify loss scenarios — determine conditions/causes leading to UCAs
- **Analysis Scope Options**: Functional safety, SOTIF, cybersecurity, other technical domains (structure, AI), or combinations
- **Key Concepts**: Accident, control action, control algorithm, control structure, controller, controller constraints, controlled process, loss, loss scenario, process model, system-level hazard, system-level constraints, UCA
- **Appendices**: A (STPA practice/application), B (SOTIF application example), C (functional safety application example), D (human factors analysis), E (comparison with other safety analysis methods)

^[raw/papers/FuSa_47_GB+T_39263-2020.md]
^[raw/papers/FuSa_51_GB+T_39263-WD_draft_道路车辆+控制系统理论过程安全分析方法.md]

## Source Documents

- [FuSa_47_GB+T_39263-2020.md](raw/papers/FuSa_47_GB+T_39263-2020.md)
- [FuSa_51_GB+T_39263-WD_draft_道路车辆+控制系统理论过程安全分析方法.md](raw/papers/FuSa_51_GB+T_39263-WD_draft_道路车辆+控制系统理论过程安全分析方法.md)

## Cross-References

- [[gb-t-34590-series]]
- [[gb-t-43254-2023]]
- [[gb-z-42285-2022]]
