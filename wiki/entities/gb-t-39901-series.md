---
title: GB/T 39901 汽车功能安全
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [braking, functional-safety, gbt-standard, requirement, test-method]
sources: ['raw/papers/FuSa_2_GB+T_39901-2021.md', 'raw/papers/FuSa_21_GB_39901-2025.md']
confidence: high
---

# GB/T 39901 汽车功能安全

## Overview

This entry covers the AEBS (Advanced/Automatic Emergency Braking System) standard series for vehicles, spanning two versions: GB/T 39901-2021 (乘用车自动紧急制动系统性能要求及试验方法) and its 2025 revision GB 39901-2025 (轻型汽车自动紧急制动系统技术要求及试验方法). The 2025 version upgrades from a recommended GB/T to a mandatory GB standard, expanding scope from M1 vehicles to M1 and N1 vehicles and adding significant new requirements including pedestrian/cyclist/motorcyclist target detection, simulation testing, and system robustness requirements. The mandatory transition reflects China's push toward universal AEBS adoption across light-duty vehicles.

## Key Facts

| Field | GB/T 39901-2021 | GB 39901-2025 |
|-------|-----------------|---------------|
| Chinese Title | 乘用车自动紧急制动系统(AEBS)性能要求及试验方法 | 轻型汽车自动紧急制动系统技术要求及试验方法 |
| English Title | Performance requirements and test methods for advanced emergency braking system (AEBS) of passenger cars | Technical requirements and testing methods for advanced emergency braking system of light-duty vehicles |
| Published Date | 2021-03-09 | 2025-12-31 |
| Effective Date | 2021-10-01 | 2028-01-01 |
| Standard Type | GB/T (recommended) | GB (mandatory) |
| ICS | 43.040 | 43.040 |
| CCS | T24 | T24 |
| Applicable Categories | M1类车辆 | M1和N1类汽车 |
| Replaces | — | GB/T 39901-2021 |

## Scope and Requirements

### GB/T 39901-2021

- **Scope**: Specifies terms, technical requirements, and test methods for AEBS on passenger cars (M1 vehicles).
- **Normative References**: GB 4094-2016, GB/T 5620, GB 21670-2008, GB/T 34590.1~34590.10-2017, GB 34660.
- **General Requirements**: Vehicles with AEBS must have ABS compliant with GB 21670-2008; EMC per GB 34660; functional safety per Appendix A.
- **Warning Signals**: Collision warning must use at least 2 of acoustic, tactile, optical signals; failure warning must use steady yellow signal.
- **Test Targets**: Stationary, moving, and braking targets defined per GB/T 3730.1.
- **Key Definitions**: AEBS, subject vehicle, target, TTC (time to collision), emergency braking phase (≥4 m/s² deceleration).
- **Performance Requirements**: Collision warning shall be issued when TTC to a stationary target ≥ 0.8s; emergency braking activated when TTC ≤ threshold; system shall not intervene for targets in adjacent lanes.

### GB 39901-2025 (Key Changes from 2021) ^[raw/papers/FuSa_2_GB+T_39901-2021.md]

- **Expanded Scope**: Now covers M1 and N1 vehicles (light-duty vehicles), up from M1 only.
- **New Terms Added**: 碰撞预警, 紧急制动, 激活状态, 待机状态, 不可用状态, 初始化, 相对碰撞速度, 自检, 整备质量, 电子控制系统, 单元, 传输链, 有效工作范围.
- **Deleted Terms**: 被试车辆, 目标, 静止目标, 移动目标, 制动目标, 紧急制动阶段, 共用空间.
- **New Requirements**: Self-check, automatic shutdown, collision warning/emergency braking independent operation, system robustness, false response tests.
- **New Test Targets**: Child pedestrian, bicycle, pedal motorcycle targets for collision warning and emergency braking.
- **New Test Methods**: Simulation testing (Appendix B), vehicle target right-turn false response, pedestrian false response, bicycle false response, independent operation tests.
- **New Appendices**: A (functional safety requirements), B (simulation test requirements), C (system functional safety description).
- **New Chapters**: Same-type determination (Chapter 8), Standard implementation (Chapter 9).
- **Implementation Timeline**: Mandatory effective 2028-01-01, providing a 2-year transition period from publication.

^[raw/papers/FuSa_2_GB+T_39901-2021.md]
^[raw/papers/FuSa_21_GB_39901-2025.md]

## Source Documents

- [FuSa_2_GB+T_39901-2021.md](raw/papers/FuSa_2_GB+T_39901-2021.md)
- [FuSa_21_GB_39901-2025.md](raw/papers/FuSa_21_GB_39901-2025.md)

## Cross-References

- [[gb-t-34590-series]]
- [[gb-t-43267-2023]]
- [[gb-21670-braking]]
