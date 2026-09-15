---
title: GB/T 44461-2024 智能网联汽车组合驾驶辅助系统技术要求及试验方法
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [adas, gbt-standard, requirement, test-method, connected-vehicle]
sources: ['raw/papers/FuSa_4_GB+T_44461.1-2024.md', 'raw/papers/FuSa_5_GB+T_44461.2-2024.md']
confidence: high
---

# GB/T 44461-2024 智能网联汽车组合驾驶辅助系统技术要求及试验方法

## Overview

GB/T 44461 is a multi-part standard specifying technical requirements and testing methods for combined driver assistance systems (CDAS, 组合驾驶辅助系统) in intelligent connected vehicles. Part 1 covers single-lane driving control (单车道行驶控制) and Part 2 covers multi-lane driving control (多车道行驶控制). These standards define the performance requirements, general requirements, and test methods for Level 2+ assisted driving systems that continuously control both lateral and longitudinal vehicle motion, including specific acceleration/deceleration limits, lane-keeping accuracy, and lane change procedure requirements.

## Key Facts

| Field | Part 1 | Part 2 |
|-------|--------|--------|
| Standard Number | GB/T 44461.1-2024 | GB/T 44461.2-2024 |
| Full Title (CN) | ...第1部分:单车道行驶控制 | ...第2部分:多车道行驶控制 |
| Full Title (EN) | ...Combined driver assistance system — Part 1: Single-lane manoeuvre | ...Part 2: Multi-lane manoeuvre |
| ICS | 43.020 | 43 |
| CCS | T 40 | T40 |
| Published Date | 2024-08-23 | 2024-08-23 |
| Effective Date | 2024-08-23 | 2024-08-23 |
| Applicable Categories | M类、N类汽车 | M类、N类汽车 |
| Managed By | SAC/TC114 | SAC/TC114 |
| Normative References | GB 5768.3, GB/T 12534, GB 34660, GB/T 44373 | GB 5768.3, GB/T 12534, GB 34660, GB/T 44373-2024, GB/T 44461.1-2024 |

## Scope and Requirements

### Part 1: Single-Lane Driving Control

- **Scope**: Specifies general requirements, performance requirements, and test methods for single-lane driving control systems — CDAS that continuously control lateral and longitudinal vehicle motion to keep the vehicle within a selected single lane
- **General Requirements** (Ch.4):
  - 4.1 Functional requirements: system must not interfere with emergency braking; adjustable cruise speed settings
  - 4.2 Self-check: must complete self-check before activation; detect electrical component and sensor anomalies
  - 4.3 State transition: activation requires driver action per manufacturer specification; deactivation via single driver action
  - 4.4 Optical signal: must continuously emit optical signal distinguishing non-active, partial active, and active states
  - 4.5 Driver monitoring: hands-off detection required at speeds between 10 km/h and vsmin-SL (or vsmax-SL)
  - 4.6 System must respond to driver's active intervention
  - 4.7 EMC per GB 34660
  - 4.8 Functional safety per Annex A
- **Performance Requirements** (Ch.5):
  - 5.1 Lateral control: lateral distance from lane boundary must be maintained at (W/2 ±0.3)m; no wheel crossing lane boundary inner edge
  - 5.1.3 Lateral acceleration limits (M₁/N₁): [10,60]km/h: max 3.0 m/s²; (60,100]: 0.5–3.0; (100,120]: 0.8–3.0; change rate ≤5 m/s³ per 0.5s
  - 5.1.4 Lateral acceleration limits (M₂/M₃/N₂/N₃): [10,30]: max 2.5; (30,60]: 0.3–2.5; (60,120]: 0.5–2.5
  - 5.2 Longitudinal control: max deceleration ≤3.5 m/s² (≥72km/h), ≤5 m/s² (≤18km/h), interpolated between

### Part 2: Multi-Lane Driving Control

- **Scope**: Specifies requirements for multi-lane driving control — CDAS that perform lateral and longitudinal control to assist lane changes only after driver-triggered initiation, between same-direction lanes
- **Key Definitions**: Multi-lane manoeuvre system, target lane boundary line, original lane, target lane, lane change procedure (from trigger to completion)
- **Lane Change Procedure Phases**: preparation phase (触发→contact target lane boundary), manoeuvre phase (cross boundary→complete), completion phase (→signal off or completion prompt)
- **General Requirements** (Ch.4):
  - 4.1.1(a): For roads with ≥2 lanes, no pedestrians/bicycles, physical median: must detect M/N/L category vehicles; no lane change at solid lane markings
  - 4.1.1(b): For M₁ vehicles on other road types: must detect vehicles, pedestrians, and non-motor vehicles
  - 4.1.2: Must maintain safe forward and rear distance with target lane vehicles
  - 4.1.4: Lane change only triggerable when single-lane control is active; auto-resume after completion
  - 4.1.6: Must not change ≥2 lanes consecutively during one lane change procedure

^[raw/papers/FuSa_4_GB+T_44461.1-2024.md]
^[raw/papers/FuSa_5_GB+T_44461.2-2024.md]

## Source Documents

- [FuSa_4_GB+T_44461.1-2024.md](raw/papers/FuSa_4_GB+T_44461.1-2024.md)
- [FuSa_5_GB+T_44461.2-2024.md](raw/papers/FuSa_5_GB+T_44461.2-2024.md)

## Cross-References

- [[gb-t-34590-series]]
- [[gb-t-44721-2024]]
- [[gb-t-41797-2022]]
- [[gb-t-39263-series]]
