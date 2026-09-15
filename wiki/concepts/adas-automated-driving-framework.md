---
title: ADAS and Automated Driving Framework
created: 2026-08-06
updated: 2026-08-06
type: concept
tags: [adas, braking, steering, overview, glossary]
sources: [raw/papers/EX_07_UN_R152_02_Suppl.5_AEBS.md, raw/papers/EX_08_UN_R157_01_Suppl.4_ALKS.md, raw/papers/EX_09_UN_R131_02_Suppl.3_AEBS.md, raw/papers/EX_10_UN_R79_04_Suppl.9_Steering_equipment.md]
confidence: high
---

# ADAS and Automated Driving Framework

## Definition

Advanced Driver Assistance Systems (ADAS) and Automated Driving (AD) functions are regulated
through a combination of UN regulations and Chinese national standards. These cover automatic
emergency braking (AEBS), automated lane keeping (ALKS), steering assistance, and related
braking/steering requirements.

## Regulatory Landscape

### UN Regulations

1. **[[un-r152-aebs]]** — UN R152: Requirements for Advanced Emergency Braking System (AEBS)
   for M1 and N1 vehicles. Covers collision warning and emergency braking performance.
   ^[raw/papers/EX_07_UN_R152_02_Suppl.5_AEBS.md]

2. **[[un-r157-alks]]** — UN R157: Requirements for Automated Lane Keeping Systems (ALKS).
   Defines requirements for Level 3 automated driving in specific operational design domains.
   ^[raw/papers/EX_08_UN_R157_01_Suppl.4_ALKS.md]

3. **[[un-r131-aebs]]** — UN R131: AEBS requirements for M2/M3/N2/N3 category vehicles
   (heavy vehicles). ^[raw/papers/EX_09_UN_R131_02_Suppl.3_AEBS.md]

4. **[[un-r79-steering]]** — UN R79: Steering equipment requirements, including automated
   steering functions (ASF) and lane keeping assistance.
   ^[raw/papers/EX_10_UN_R79_04_Suppl.9_Steering_equipment.md]

5. **[[un-r13-braking]]** — UN R13: General braking requirements for M, N, and O category
   vehicles. Includes supplements for heavy vehicle and passenger car braking.
   ^[raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md] ^[raw/papers/EX_06_UN_R13-H_01_Suppl.5_Passenger_car_braking.md]

### Chinese Standards

6. **[[gb-21670-braking]]** — Passenger car braking system technical requirements and test
   methods. Includes ABS, AEBS, and functional safety test procedures.

7. **[[gb-17675-steering]]** — Steering system basic requirements. Includes functional safety
   compliance requirements (Appendix B).

8. **[[gb-12676-braking]]** — Commercial vehicle braking system requirements (2014 version).

9. **[[gb-t-44850-2024]]** — Intelligent connected vehicle driving safety test items and methods.

### Supporting Documents

- AEBS meeting materials and performance requirements
- GB 21670 EMC test procedures for ABS
- GB 21670 same-type judgment and filing parameters

## Key Concepts

- **AEBS:** Automatic Emergency Braking System — detects collision risk and applies brakes autonomously
- **ALKS:** Automated Lane Keeping System — SAE Level 3 driving in specific conditions
- **ABS:** Anti-lock Braking System — prevents wheel lockup during braking
- **ESC:** Electronic Stability Control — maintains vehicle directional stability
- **ASF:** Automated Steering Function — steering control without driver input
- **ODD:** Operational Design Domain — conditions under which automated driving is safe
- **Same Type Judgment:** Criteria for determining vehicle variant equivalency

## Cross-References

- [[functional-safety-framework]] — FuSa requirements apply to ADAS safety
- [[vehicle-cybersecurity-framework]] — Cybersecurity requirements for connected ADAS
- [[gb-t-43267-2023]] — SOTIF directly relevant to ADAS performance limitations
- [[gb-t-44850-2024]] — ICV driving safety test methods
- [[un-vs-china-braking-steering]] — UN vs Chinese braking/steering standards comparison
