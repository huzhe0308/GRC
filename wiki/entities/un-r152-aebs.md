---
title: UN R152 AEBS Regulation
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [braking, adas, un-regulation, requirement, test-method]
sources: ['raw/papers/EX_07_UN_R152_02_Suppl.5_AEBS.md']
confidence: high
---

# UN R152 AEBS Regulation

## Overview

UN Regulation No. 152 establishes uniform provisions for the approval of M1 and N1 category motor vehicles with regard to the Advanced Emergency Braking System (AEBS). The regulation provides requirements for systems designed to avoid or mitigate rear-end collisions with passenger cars, impacts with pedestrians, and impacts with bicycles. It offers an alternative to UN R131 for lighter vehicles with hydraulic braking, with reciprocal recognition between the two regulations. The current version (02 series, Supplement 5) entered into force on 11 January 2026, with the regulation defining Time to Collision (TTC), collision warning timing requirements, and performance criteria including mean fully developed deceleration.

## Key Facts

| Field | Value |
|-------|-------|
| Regulation Number | UN R152 |
| Full Title | Uniform provisions concerning the approval of motor vehicles with regard to the Advanced Emergency Braking System (AEBS) for M1 and N1 vehicles |
| Current Version | 02 series of amendments, Revision 2, Amendment 5 |
| Supplement 5 Entry into Force | 2026-01-11 |
| Earlier Supplements | Suppl. 1 (2022-06-22), Suppl. 2 (2022-10-08), Suppl. 3 (2023-09-24), Suppl. 4 (2025-09-26) |
| 02 Series Entry into Force | 2021-09-30 |
| Issuing Body | UNECE |
| Applicable Categories | M1 and N1 vehicles; also M2 and M3/N2/N3 ≤8t with hydraulic braking |

## Scope and Requirements

- **Scope**: Applies to approval of M1 and N1 category vehicles regarding AEBS
- **Collision Scenarios**: System shall avoid or mitigate severity of: (a) rear-end in-lane collision with a passenger car, (b) impact with a pedestrian, (c) impact with a bicycle
- **Warning Design**: System shall be designed to minimize collision warning signals and avoid emergency braking when no risk of imminent collision exists
- **Collision Warning**: When imminent collision with preceding M1 vehicle detected, warning shall be provided at latest **0.8 seconds** before start of emergency braking; if collision cannot be anticipated in time, warning per paragraph 5.5.1 shall be provided no later than start of emergency braking intervention; warning may be aborted if conditions change
- **Braking Requirements**: Vehicle must be equipped with anti-lock braking function per UN R13-H or R13 requirements
- **Performance**: Vehicle shall meet performance requirements of UN R13-H (01 series) for M1/N1 or UN R13 (11 series) for N1 vehicles
- **Self-Check**: System shall perform self-checks; no appreciable time interval between self-checks; no delay in illuminating warning signal upon detection of electrically detectable failure
- **Failure Detection**: Upon detection of non-electrical failure (e.g., sensor blindness, sensor misalignment), the warning signal per paragraph 5.1.4.1 shall be illuminated
- **Initialization**: If system not initialized after cumulative driving time of **15 seconds** above **10 km/h**, information shall be provided to the driver
- **Alternative to R131**: Offers alternative requirements for M2 vehicles and M3/N2/N3 ≤8t with hydraulic braking; Contracting Parties applying both R131 and R152 recognize approvals to either as equally valid
- **Assessment**: Compliance assessment per Annex 3, including scenarios listed in Appendix 2 (false reaction avoidance)
- **Test Conditions**: Tests with dummy vehicles or "soft targets" must be performed; brakes must be properly operational (temperature, pad condition); no severe uneven load distribution; no trailer coupled

## Technical Details

- Collision warning threshold: **0.8 seconds** before emergency braking (paragraph 5.5.1)
- System initialization: **15 seconds** cumulative driving time above **10 km/h**
- Mean fully developed deceleration on dry road: at least **9 m/s²** (or design maximum deceleration, whichever is lower)
- TTC (Time to Collision): defined as distance between subject vehicle and target divided by longitudinal relative speed
- Speed formula uses: v = initial speed, v at 0.8v, v at 0.1v (for performance calculation)
- Peak Braking Coefficient (PBC): "nominal" value understood as minimum theoretical target value
- Test target types: vehicle target (soft target representing a vehicle), pedestrian target (soft target), bicycle target
- "Dry road affording good adhesion": sufficient nominal PBC for mean fully developed deceleration ≥9 m/s²

## Source Documents

- [EX_07_UN_R152_02_Suppl.5_AEBS.md](raw/papers/EX_07_UN_R152_02_Suppl.5_AEBS.md)

## Cross-References

- [[un-r13-braking]]
- [[un-r131-aebs]]
- [[un-r157-alks]]
- [[gb-12676-braking]]
- [[gb-21670-braking]]
- [[gb-t-44298-2024]]
