---
title: EV Safety Framework
created: 2026-08-06
updated: 2026-08-06
type: concept
tags: [ev-safety, overview, glossary, requirement, test-method]
sources: [raw/papers/NET_1_GB_18384-2025.md, raw/papers/FuSa_12_GB+T_39086-2020.md, raw/papers/FuSa_12a_GB+T_39086-2020_附录A_REESS.md, raw/papers/FuSa_12b_GB+T_39086-2020_附录B_BMS.md]
confidence: high
---

# EV Safety Framework

## Definition

Electric vehicle (EV) safety addresses electrical hazards, thermal risks, and functional
safety requirements specific to vehicles with high-voltage traction systems, rechargeable
energy storage systems (REESS), and battery management systems (BMS). The regulatory
framework in China is anchored by GB 18384 (vehicle-level electrical safety) and GB/T 39086
(BMS functional safety), with complementary standards for battery safety (GB 38031) and
charging infrastructure. ^[raw/papers/NET_1_GB_18384-2025.md] ^[raw/papers/FuSa_12_GB+T_39086-2020.md]

## Regulatory Landscape

### Primary Standards

1. **[[gb-18384-2025]]** — GB 18384-2025: 电动汽车安全要求 (Electric vehicles safety
   requirements). Published 2025-12-31, effective 2026-07-01. Replaces GB 18384-2020.
   The standard covers M and N category electric vehicles and defines:
   - **Clause 4 — Voltage Classification:** Class A (0-60V DC / 0-30V AC) and Class B
     (60-1500V DC / 30-1000V AC) voltage levels
   - **Clause 5.1 — Electrical Shock Protection:** Four components: high-voltage marking,
     direct contact protection, indirect contact protection, water protection
   - **Clause 5.2 — Underbody Protection:** Battery pack underside impact protection
   - **Clause 5.3 — Safety Function Protection:** Functional safety for EV-specific functions
   - **Clause 5.4 — Traction Battery Requirements:** REESS safety including thermal runaway
     containment, overcharge/overdischarge protection
   - **Clause 5.5 — Vehicle Crash Protection:** Post-crash electrical safety (insulation,
     voltage discharge, physical barrier integrity)
   - **Clause 5.6 — Fire Resistance:** Battery fire propagation requirements
   - **Clause 5.7 — Charging Interface:** Safety during AC/DC charging including V2L
   - **Clause 5.8 — Alarm and Warning:** Electrical hazard warning systems
   - **Clause 5.9 — Event Data Recording:** EV-specific event data
   - **Clause 5.10 — EMC:** Electromagnetic compatibility for EV systems

   Key technical requirements:
   - Insulation resistance: ≥100Ω/V for DC circuits, ≥500Ω/V for AC circuits
   - Direct contact protection via IPXXD (passenger cabin) or IPXXB (exterior) enclosures
   - Voltage discharge to ≤60V DC / ≤30V AC within 1 second of barrier removal
   - Energy discharge to <0.2J within 1 second
   - Potential equalization: ≤0.1Ω connection impedance to electrical chassis
   - Capacitive coupling: <0.2J stored energy, ≤5mA AC / ≤25mA DC contact current
   - Orange-colored B-class voltage cable identification

   ^[raw/papers/NET_1_GB_18384-2025.md]

2. **[[gb-t-39086-2020]]** — GB/T 39086-2020: 电动汽车用电池管理系统功能安全要求及试验方法
   (Functional safety requirements and testing methods for battery management system of
   electric vehicles). Published 2020-09-29, effective 2021-04-01.
   - Scope: EV lithium-ion traction battery BMS for passenger vehicles
   - Covers: general requirements, item definition, HARA, functional safety requirements,
     verification and validation
   - Appendix A (informative): HARA example with BMS as relevant item
   - Appendix B (informative): HARA example with traction battery system as relevant item
   - Appendix C (informative): Fault Tolerant Time Interval (FTTI) determination method
   - References: GB 18384-2020, GB/T 19596-2017, GB/T 34590 (all parts), GB 38031-2020,
     GB/T 38661-2020

   ^[raw/papers/FuSa_12_GB+T_39086-2020.md] ^[raw/papers/FuSa_12a_GB+T_39086-2020_附录A_REESS.md]

### Supporting Standards

3. **[[gb-18352-6-c6]]** — Emission standards exempt EVs from tailpipe requirements
4. **[[gb-t-47025-2026]]** — May contain EV-specific FuSa requirements
5. **[[gb-44496-2024]]** — OTA update requirements for EV software components

## Key Concepts

- **Voltage Class A (A级电压):** 0 < U ≤ 60V DC or 0 < U ≤ 30V AC
- **Voltage Class B (B级电压):** 60 < U ≤ 1500V DC or 30 < U ≤ 1000V AC
- **REESS (Rechargeable Energy Storage System / 可充电储能系统):** System storing energy
  for electric propulsion — includes battery pack, housing, management system, and associated
  circuits (thermal management, high-voltage circuit, low-voltage circuit)
- **BMS (Battery Management System / 电池管理系统):** Electronic system monitoring battery
  state (temperature, voltage, SOC), providing communication, safety, cell balancing, and
  control functions
- **High-Voltage System (高压系统):** B-class voltage components connected to traction battery
  DC bus — includes traction battery, high-voltage distribution (relays, fuses, switches),
  motor and controller, DC/DC converter, onboard charger
- **FTTI (Fault Tolerant Time Interval / 故障容错时间间隔):** Shortest time from fault
  occurrence to potential hazard event when safety mechanism is not activated
- **Insulation Resistance (绝缘电阻):** Minimum 100Ω/V (DC) or 500Ω/V (AC) between
  high-voltage bus and vehicle chassis
- **Direct Contact Protection (直接接触防护):** Physical isolation via insulation, enclosures,
  or barriers — IPXXD in passenger cabin, IPXXB outside
- **Potential Equalization (电位均衡):** ≤0.1Ω connection impedance between exposed
  conductive parts and electrical chassis; ≤0.2Ω between any two parts within 2.5m
- **Thermal Runaway (热失控):** Uncontrolled exothermic reaction in battery cells
- **V2L (Vehicle to Load):** EV traction battery powers external loads via charging interface

^[raw/papers/NET_1_GB_18384-2025.md] ^[raw/papers/FuSa_12_GB+T_39086-2020.md]

## Timeline

- 2020-09-29: GB/T 39086-2020 (BMS FuSa) published
- 2021-04-01: GB/T 39086-2020 effective
- 2025-12-31: GB 18384-2025 published (replaces GB 18384-2020)
- 2026-07-01: GB 18384-2025 effective date

^[raw/papers/NET_1_GB_18384-2025.md] ^[raw/papers/FuSa_12_GB+T_39086-2020.md]

## Cross-References

- [[vehicle-cybersecurity-framework]] — EV systems need cybersecurity (BMS, charging)
- [[functional-safety-framework]] — EV safety functions require FuSa compliance
- [[ota-software-update-framework]] — OTA updates for EV software components
- [[gb-t-34590-series]] — FuSa baseline for EV component safety (referenced by GB/T 39086)
- [[gb-44496-2024]] — OTA update requirements for EV software
- [[gb-t-47025-2026]] — EV-specific FuSa requirements
- [[gb-18384-2025]] — Related charging infrastructure standards
