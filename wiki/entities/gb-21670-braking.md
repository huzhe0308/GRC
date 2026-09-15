---
title: GB 21670-2025 乘用车制动系统技术要求及试验方法
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [braking, gb-standard, requirement, test-method, vehicle-testing, functional-safety]
sources: ['raw/papers/FuSa_20_GB_21670-2025.md', 'raw/transcripts/EX_06_GB+21670-202X+乘用车防抱制动系统EMC测试规程.md', 'raw/transcripts/EX_07_GB+21670-XXXX《乘用车制动系统技术要求及试验方法》测试规程（制动性能部分）.md']
confidence: high
---

# GB 21670-2025 乘用车制动系统技术要求及试验方法

## Overview

GB 21670-2025 is a mandatory Chinese national standard specifying technical requirements and testing methods for passenger car braking systems. Published on 30 May 2025, it replaces GB 21670-2008 and introduces over 70 technical modifications including Electronic Transmission Braking System (ETBS) requirements, emergency braking signal requirements, updated functional safety requirements (Annex A), and comprehensive test method revisions. The standard is accompanied by detailed test procedure documents covering EMC testing for ABS systems and braking performance testing methodology, addressing modern braking technologies including electric regenerative braking and electronic control systems.

## Key Facts

| Field | Value |
|-------|-------|
| Standard Number | GB 21670-2025 |
| Full Title (CN) | 乘用车制动系统技术要求及试验方法 |
| Full Title (EN) | Technical requirements and testing methods for passenger car braking systems |
| ICS | 43.040.40 |
| CCS | T24 |
| Published Date | 2025-05-30 |
| Effective Date | 2026-01-01 |
| Supersedes | GB 21670-2008 |
| Issuing Body | 国家市场监督管理总局、国家标准化管理委员会 |
| Applicable Vehicles | Passenger cars (M₁) |

## Scope and Requirements

- Covers braking system structure and functional requirements, test and performance requirements, test methods, and type approval
- Key changes from 2008 version (70+ technical modifications):
  - Updated EMC requirements for braking electronic control systems (5.1.1.4, 6.5.1.5)
  - Enhanced functional safety requirements for braking electronic control systems (Clause 5.1.3, Annex A)
  - New ETBS (Electronic Transmission Braking System) requirements: transmission failure warning, response time, special requirements (5.2.24)
  - New emergency braking signal requirements (Clause 5.2.23)
  - New temporary spare wheel/tire braking and deviation test requirements (5.2.25, Annex E)
  - New M₁ ABS installation requirement (Clause 5.2.26)
  - Updated power battery state of charge inspection (Annex D)
  - Removed inter-axle braking force distribution and ABS type classification
  - Added kpeak and klock calculation methods (Clauses 6.5.5.1–6.5.5.3)
  - Added Type A and Type B electric regenerative braking system requirements for accelerator release (5.2.18f)
  - Updated parking brake electronic transmission requirements (5.2.19)
- Annex A (normative): Braking electronic control system functional safety requirements
- Annex B (normative): Functional safety test report requirements
- Annex C (normative): Functional safety description requirements
- Annex D: Power battery state of charge inspection
- Annex E: Temporary spare wheel/tire braking and deviation test

## EMC Test Procedure (from EX_06 transcript)

- ABS immunity testing in semi-anechoic chamber, 20 MHz–2 GHz frequency range per GB/T 33012.1-2016
- Field strength: 30 V/m (RMS) in ≥90% of band, ≥25 V/m in remainder
- Modulation: AM (1kHz, 80% depth) for 20–800 MHz; PM (577µs pulse, 4600µs period) for 800–2000 MHz
- 16 test frequency points: 27, 45, 65, 90, 120, 150, 190, 230, 280, 380, 450, 600, 750, 900, 1300, 1800 MHz
- Vehicle reference point: front axle rear 0.2m±0.2m at 1m±0.05m height (vehicle roof ≤3m); 1.8m±0.05m for roof >3m
- TLS placement: any part ≥0.5m from vehicle, radiation element ≥1m vertical distance from reference point, covers ≥75% of vehicle length
- Failure criteria: ABS fails to activate, unexpected wheel lock, or ABS warning lamp illuminates

## Braking Performance Test Procedure (from EX_07 transcript)

- Test sequence: static checks first, then dynamic tests; Type I (hot performance) test last
- Vehicle load: unladen (kerb + 110 kg including driver and test equipment) and laden (max design mass)
- Brake bedding: 200 cycles from 80% Vmax (≤120 km/h) at 3 m/s² deceleration, initial brake temperature 65°C–100°C
- Equipment precision: speed/distance ±1%, control force ±2%, brake temperature ±5%, deceleration ±3%, time ±1s (response time ±0.01s)
- Failure detection signal may temporarily (<10ms) interrupt control transmission without reducing braking performance

^[raw/papers/FuSa_20_GB_21670-2025.md]
^[raw/transcripts/EX_06_GB+21670-202X+乘用车防抱制动系统EMC测试规程.md]
^[raw/transcripts/EX_07_GB+21670-XXXX《乘用车制动系统技术要求及试验方法》测试规程（制动性能部分）.md]

## Source Documents

- [FuSa_20_GB_21670-2025.md](raw/papers/FuSa_20_GB_21670-2025.md)
- [EX_06_GB+21670-202X+乘用车防抱制动系统EMC测试规程.md](raw/transcripts/EX_06_GB+21670-202X+乘用车防抱制动系统EMC测试规程.md)
- [EX_07_GB+21670-XXXX《乘用车制动系统技术要求及试验方法》测试规程（制动性能部分）.md](raw/transcripts/EX_07_GB+21670-XXXX《乘用车制动系统技术要求及试验方法》测试规程（制动性能部分）.md)

## Cross-References

- [[gb-17675-steering]]
- [[gb-12676-braking]]
- [[un-r13-braking]]
- [[un-r152-aebs]]
- [[un-r131-aebs]]
- [[gb-t-34590-series]]
