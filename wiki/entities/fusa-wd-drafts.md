---
title: WD Drafts — New FuSa Standards Replacing GB/T 44721 and GB/T 44461
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [functional-safety, gbt-standard, draft, adas, automated-driving, requirement, test-method, same-type-judgment]
sources: ['raw/papers/FuSa_10_GB+XXXXX-XXXX_replaces_44461_WD_draft.md', 'raw/papers/FuSa_9_GB+XXXXX-XXXX_replaces_44721-2024_WD_draft_source.md']
confidence: high
---

# WD Drafts — New FuSa Standards Replacing GB/T 44721 and GB/T 44461

## Overview

This entity covers two working draft (WD) documents for upcoming Chinese national standards that will replace existing FuSa-related standards. The first draft (GB XXXXX-XXXX) defines safety requirements for intelligent and connected vehicle Combined Driver Assistance Systems (CDA, 组合驾驶辅助系统), covering basic single-lane, basic multi-lane, and advanced (领航) combined driver assistance systems. The second draft replaces GB/T 44721-2024 (Automated Driving System General Technical Requirements). Both are in the 征求意见稿 (public comment draft) stage as of September 2025. The CDA safety requirements draft is a substantial document with 12 clauses and 6 normative annexes, establishing comprehensive safety requirements, test methods, and same-type judgment criteria for M and N category vehicles.

## Key Facts

| Field | Draft 1 (CDA Safety) | Draft 2 (Replaces 44721) |
|-------|----------------------|--------------------------|
| Standard Number | GB XXXXX-XXXX | GB XXXXX-XXXX |
| Full Title (CN) | 智能网联汽车 组合驾驶辅助系统安全要求 | (Replaces GB/T 44721-2024) |
| Full Title (EN) | Intelligent and connected vehicle — Safety requirements of combined driver assistance system | — |
| ICS | 43.020 | — |
| CCS | T40 | — |
| Proposed by | 中华人民共和国工业和信息化部 (MIIT) | — |
| Draft Stage | 征求意见稿 (Public comment draft) | WD draft |
| Draft Date | September 2025 | — |
| Source Format | Full text | Image-only PDF (binary) |

## Scope and Requirements — GB XXXXX-XXXX (CDA Safety Requirements)

- **Scope (Clause 1):** Specifies safety requirements for basic single-lane CDA, basic multi-lane CDA, and advanced (领航) CDA systems. Describes corresponding inspection and test methods. Applicable to M and N category vehicles equipped with these systems.
- **System Types (Clause 3):** Three CDA categories defined: basic single-lane CDA (A-type road environment only, single-lane control), basic multi-lane CDA (A-type road, driver-triggered lane change), and advanced (领航) CDA (A and/or B-type roads, lane cruise + non-lane cruise + risk mitigation function). Parking CDA is a 4th category treated separately.
- **Functions (Clause 3):** Lane cruise control (车道巡航控制), non-lane cruise control (非车道巡航控制) including driver-initiated lane change, driver-confirmed lane change, system-initiated lane change, obstacle navigation by lane crossing, intersection passage, and roundabout passage.
- **Risk Mitigation Function (RMF, 风险减缓功能, Clause 3.9):** Automatic vehicle stop when driver is disengaged — defined as the system stopping the vehicle in a target parking area when the driver fails to respond to disengagement warnings.
- **Driver Disengagement (Clause 3):** Driver disengagement (驾驶员脱离) includes hands-on request (HOR, 手握转向盘提示) and eyes-on request (EOR, 视线回归提示). Direct control alert (DCA, 立即控制警告) requires the driver to immediately resume lateral control.
- **General Requirements (Clause 4.1):** System design must ensure the driver continuously performs dynamic driving tasks. Must respond to driver override at any time. Must operate only within designed speed range. In A-type road environments, max driver-set speed ≤ road's posted speed limit. System must not suppress or interrupt active AEB systems.
- **ODC Boundary Detection (Clause 4.3):** For A-type roads, ODC elements must include: traffic signs, toll stations, road construction, ramps, tunnels, vehicles, pedestrians, obstacles, speed range, lane width, time, weather. For B-type roads: traffic signals, traffic signs, road construction, intersections, roundabouts, tunnels, vehicles, non-motorized vehicles, pedestrians, obstacles, speed range, lane width, time, weather.
- **Lateral Acceleration Limits (Clause 4.6.1.4–4.6.1.8):** M1/N1 vehicles: max lateral acceleration ≤3 m/s²; M2/M3/N2/N3 vehicles: ≤2.5 m/s². Tolerance: not exceeding declared max by more than 0.3 m/s². Controllability exception: up to 2 s exceeding the limit, but not exceeding 1.4× declared max (M1/N1: ≤3.3 m/s²; M2/M3/N2/N3: ≤2.8 m/s²). Lateral acceleration change rate: ≤5 m/s³ averaged over 0.5 s.
- **Imminent Collision Risk (Clause 3.34):** Defined as the system being unable to avoid collision with a deceleration command below 5 m/s².
- **Mandatory Equipment (Clause 4.1.16):** Vehicles must have AEB systems (per GB XXXXX light/heavy vehicle AEBS standards) and lane keeping assistance systems (per GB/T 39323 or GB/T 41796).
- **Test Methods (Clauses 7–8):** Clause 7 defines closed-course (场地) test methods; Clause 8 defines road test methods. Each test item conducted once. Road test "should" requirements verified by documentation if external factors prevent compliance.
- **Same-Type Judgment (Clause 11):** Criteria for 同一型式判定 (same-type approval judgment) for CDA-equipped vehicles.
- **Implementation Date (Clause 12):** Defines transition timeline for market entry.
- **Annex A (normative):** Safety requirement-to-test mapping table.
- **Annex B (normative):** Simulation test credibility assessment requirements (仿真试验可信度评估).
- **Annex C (normative):** Functional safety (FuSa) and SOTIF requirements — references GB/T 34590 (all parts) and GB/T 43267.
- **Annex D (normative):** FuSa and SOTIF description requirements.
- **Annex E (normative):** CDA safety assurance requirements.
- **Annex F (normative):** Data recording requirements — references GB 44497-2024 (自动驾驶数据记录系统).

## Normative References

- GB/T 34590 (all parts) — 道路车辆 功能安全 (Road vehicles — Functional safety)
- GB/T 43267 — 道路车辆 预期功能安全 (SOTIF)
- GB 44495 — 汽车整车信息安全技术要求 (Vehicle cybersecurity)
- GB 44496 — 汽车软件升级通用技术要求 (OTA software updates)
- GB 44497-2024 — 智能网联汽车 自动驾驶数据记录系统 (Autonomous driving data recording)
- GB/T 40429-2021 — 汽车驾驶自动化分级 (Driving automation levels)
- GB/T 45312 — 智能网联汽车 自动驾驶系统设计运行条件 (ODD)
- GB/T 44461.1-2024 / GB/T 44461.2-2024 — CDA technical requirements and test methods (single-lane / multi-lane)

## Technical Details

| Parameter | M1/N1 Vehicles | M2/M3/N2/N3 Vehicles |
|-----------|----------------|----------------------|
| Max lateral acceleration | ≤3 m/s² | ≤2.5 m/s² |
| Lateral accel tolerance | +0.3 m/s² | +0.3 m/s² |
| Controllability exception (2 s) | ≤3.3 m/s² (1.4×) | ≤2.8 m/s² (1.4×) |
| Lateral accel change rate | ≤5 m/s³ (0.5 s avg) | ≤5 m/s³ (0.5 s avg) |
| Imminent collision risk threshold | <5 m/s² deceleration | <5 m/s² deceleration |

## Source Documents

- [FuSa_10_GB+XXXXX-XXXX_replaces_44461_WD_draft.md](raw/papers/FuSa_10_GB+XXXXX-XXXX_replaces_44461_WD_draft.md) — full text, 3,989 lines
- [FuSa_9_GB+XXXXX-XXXX_replaces_44721-2024_WD_draft_source.md](raw/papers/FuSa_9_GB+XXXXX-XXXX_replaces_44721-2024_WD_draft_source.md) — image-only PDF (binary)

## Cross-References

- [[gb-t-44461-series]]
- [[gb-t-44721-2024]]
- [[gb-t-34590-series]]
- [[gb-t-43267-2023]]
- [[gb-44495-2024]]
- [[gb-44496-2024]]
- [[gb-44497-2024]]
