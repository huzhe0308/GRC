---
title: GB 12676 汽车制动系统技术要求
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [braking, gb-standard, requirement, test-method, vehicle-testing]
sources: ['raw/papers/FuSa_50_GB_12676-2014.md', 'raw/papers/12676-2014-gb-e-300.md']
confidence: high
---

# GB 12676 汽车制动系统技术要求

## Overview

GB 12676-2014 is a Chinese mandatory national standard specifying technical requirements and testing methods for commercial vehicle and trailer braking systems. It replaces GB 12676-1999 and was issued by the General Administration of Quality Supervision, Inspection and Quarantine and the Standardization Administration of China. The standard is technically based on UN ECE R13 (10 series) with non-equivalent consistency, and covers braking system technical requirements, performance requirements for M2, M3, N, and O category vehicles, response time measurement, type approval/extension, and production conformity. It includes 12 normative annexes covering pneumatic braking, energy storage, force distribution, electronic control system safety, and inertia braking systems. ^[raw/papers/FuSa_50_GB_12676-2014.md] ^[raw/papers/12676-2014-gb-e-300.md]

## Key Facts

| Field | Value |
|-------|-------|
| Standard Number | GB 12676-2014 |
| Full Title (CN) | 商用车辆和挂车制动系统技术要求及试验方法 |
| Full Title (EN) | Technical requirements and testing methods for commercial vehicle and trailer braking systems |
| ICS | 43.040 |
| CCS | T24 |
| Published Date | 2014-10-10 |
| Effective Date | 2015-07-01 |
| Supersedes | GB 12676-1999 |
| Issuing Body | 国家质量监督检验检疫总局、中国国家标准化管理委员会 |
| Proposed By | 中华人民共和国工业和信息化部 |
| Managed By | SAC/TC114 (全国汽车标准化技术委员会) |
| Based On | UN ECE R13 (10 series, including amendments through August 2007) |
| Applicable Categories | M2, M3, N (commercial vehicles) and O (trailers); excludes vehicles with design speed ≤25 km/h |

## Scope and Requirements

- **Clause 1 (Scope)**: Applies to M2, M3, N category motor vehicles and O category trailers per GB/T 15089; excludes vehicles with design speed ≤25 km/h and trailers not connectable to vehicles with design speed >25 km/h
- **Clause 3 (Terms and Definitions)**: Defines braking system components (control device, transmission device, brake), braking types (continuous, semi-continuous, automatic, inertia), regenerative braking (Category A and B), electric control line, coupling force control, and complex electronic vehicle control systems
- **Clause 4.1 (General Requirements)**: Braking system must withstand vibration in normal use; must have corrosion/aging resistance; brake linings must not contain asbestos; system effectiveness must not be adversely affected by magnetic/electric fields
- **Clause 4.1.2 (Braking Functions)**: Service braking must control vehicle at all speeds/loads/uphill/downhill with progressive action; emergency braking must stop vehicle when service brake fails; parking brake must lock via pure mechanical means and hold on slopes
- **Clause 4.1.3 (Pneumatic Connection)**: Motor vehicle-trailer pneumatic connections via: (a) one air supply + one air control line; (b) one air supply + one air control + one electric control line; (c) one air supply + one electric control line; electric control line per ISO 11992-1 and ISO 11992-2:2003
- **Clause 4.1.4**: Added periodic technical inspection requirements for braking systems
- **Clause 4.1.5**: Added safety requirements for complex electronic vehicle control systems (Annex H)
- **Clause 4.2**: Specifies braking system characteristics including ABS installation scope, electric regenerative braking for M2/N1/<5t N2, electronically controlled parking brake, coupling force control
- **Clause 5**: Test and performance requirements — Type 0, Type I, Type II, Type IIA, Type III tests; response time measurement per Annex B; M/N category and O category performance requirements
- **Clause 6**: Type approval and extension procedures
- **Clause 7**: Production conformity requirements
- **Annex A (normative)**: Power battery state of charge (SOC) inspection procedure — defines test method for traction battery SOC
- **Annex B (normative)**: Pneumatic braking system vehicle response time measurement (motor vehicles and trailers)
- **Annex C (normative)**: Energy supply and storage device requirements (pneumatic, vacuum, hydraulic)
- **Annex D (normative)**: Spring braking system special conditions including auxiliary release system
- **Annex E (normative)**: Inter-axle braking force distribution and tractor-trailer coordination; defines symbols, requirements for motor vehicles, semi-trailers, full trailers, and center-axle trailers
- **Annex F (normative)**: Electronic control line functional coordination test procedure
- **Annex G (normative)**: Brake lining inertia dynamometer test method
- **Annex H (normative)**: Complex electronic vehicle control system safety requirements (documentation, validation, testing) — safety concept, electronic control system, higher-level control systems
- **Annex I (normative)**: Electric braking system trailer tests
- **Annexes J–L**: Type test exemption conditions, trailer brake alternative procedures, inertia braking system tests

## Technical Details

- Electric control line must comply with **ISO 11992-1** and **ISO 11992-2:2003** via 7-pin connectors (GB/T 20716.1 or GB/T 20716.2)
- Brake function has priority over driving system information in both normal and failure modes
- Failure detection signal may temporarily interrupt control transmission for **<10 ms** without reducing braking performance (Clause 4.1.1.5)
- Simultaneous lockup of front/rear wheels defined as time interval **<0.1s** between last wheel lockup (Clause 3.1.21)
- Unladen condition = vehicle curb weight + 110 kg (Clause 3.1.17)
- Laden condition = maximum design total mass (Clause 3.1.18)
- Key technical changes from GB 12676-1999: removed M1 content, added ABS scope, electric regenerative braking, coupling force control, complex electronic control system safety

## Source Documents

- [FuSa_50_GB_12676-2014.md](raw/papers/FuSa_50_GB_12676-2014.md)
- [12676-2014-gb-e-300.md](raw/papers/12676-2014-gb-e-300.md)

## Cross-References

- [[gb-21670-braking]]
- [[un-r13-braking]]
- [[functional-safety-overview]]
- [[un-r152-aebs]]
