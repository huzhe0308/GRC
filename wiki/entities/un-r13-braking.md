---
title: UN R13 Braking System Regulation
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [braking, un-regulation, requirement, test-method]
sources: ['raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md', 'raw/papers/EX_06_UN_R13-H_01_Suppl.5_Passenger_car_braking.md']
confidence: high
---

# UN R13 Braking System Regulation

## Overview

UN Regulation No. 13 establishes uniform provisions for the approval of vehicles of categories M, N, and O with regard to braking, while UN Regulation No. 13-H provides an alternative set of requirements specifically for passenger cars (M1) and light goods vehicles (N1). Together these regulations define comprehensive braking system requirements including service, secondary, and parking braking performance, as well as provisions for advanced technologies such as anti-lock braking systems (ABS), electronic stability control (ESC), endurance braking, and electric regenerative braking. The regulations have been continuously amended through 15 series of amendments for R13 and Supplement 5 for R13-H, with the latest supplements addressing compatibility bands for towing vehicles and trailers, and provisions for Automated Driving Systems (ADS).

^[raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md]
^[raw/papers/EX_06_UN_R13-H_01_Suppl.5_Passenger_car_braking.md]

## Key Facts

| Field | UN R13 (Heavy) | UN R13-H (Passenger) |
|-------|----------------|----------------------|
| Regulation Number | UN R13 | UN R13-H |
| Current Version | 15 series of amendments + Suppl.1 | Revision 4, 01 series + Suppl.5 |
| Latest In Force | 2026-01-11 (Suppl.1 to 15th series) | 2025-01-10 (Suppl.5 to 01 series) |
| Applicable Categories | M2, M3, N, O | M1, N1 |
| Issuing Body | UNECE | UNECE |
| Exclusions | Design speed ≤25 km/h; invalid driver vehicles; vehicles without manual braking controls | Same + ESC/BAS approval excluded |

## Scope and Requirements

### UN R13 (Heavy Vehicles)

- **Scope**: Applies to vehicles of categories M2, M3, N, and O with regard to braking. M1 category braking is exclusively covered by Regulation 13-H.
- **Braking Principles**: Defines friction brakes, electrical brakes, fluid brakes, and engine brakes as braking force generation methods.
- **System Requirements**:
  - **Service braking**: Progressive speed reduction, graduated, initiated by driver without removing hands from steering control
  - **Secondary braking**: Halt vehicle within reasonable distance on service brake failure
  - **Parking braking**: Hold stationary at 20% incline via mechanically locked elements
- **General Characteristics**: At least two independent controls; service braking independent of parking braking; braking acts on all wheels with appropriate axle distribution; wear inspection from outside/underside of vehicle.
- **Warning Signals**: Required when prescribed service braking performance not achieved and/or independent circuits not functioning; visible in daylight; persist as long as failure/defect exists.
- **Endurance Braking**: Defines independent, integrated, and combined endurance braking system configurations for heavy vehicles requiring sustained braking capacity.
- **Electric Regenerative Braking**: Category A (not part of service braking) and Category B (part of service braking); SOC monitoring required.
- **Compatibility Bands** (Annex 10): Sets matched braking performance bands for towing vehicles and trailers for simultaneous wheel lock-up; ABS-equipped vehicles exempt from unladen compatibility bands. Latest supplement raises upper band for control pressures ≥500 kPa to enable ~25% more brake force.

### UN R13-H (Passenger Cars) ^[raw/papers/EX_06_UN_R13-H_01_Suppl.5_Passenger_car_braking.md]

- **Scope**: Applies to braking of M1 and N1 vehicles. Contracting Parties applying both R13 and R13-H recognize approvals to either as equally valid.
- **Advanced Systems**: Includes provisions for ABS (prevent wheel lock, maintain steering control), ESC, and electric regenerative braking systems (Category A and B).
- **ADS Provisions** (Suppl.5): Introduces definitions and requirements for vehicles equipped with both Automated Driving System and manual driving mode. Defines ADS as hardware/software capable of performing the entire Dynamic Driving Task (DDT) on a sustained basis.
- **Testing**: Type-0 tests (cold brake stopping distances, both laden and unladen), Type-I tests (brake fade and recovery), parking brake gradient tests, ABS tests on low-adhesion surfaces and high-low adhesion transitions.
- **Brake Linings**: Shall not contain asbestos; effectiveness not adversely affected by magnetic/electrical fields (per UN R10).

## Technical Details

- **Braking System Tests**: Performance with cold brakes (<100°C); heated brake performance retention; downhill behavior; continuous braking effect.
- **ABS Exemption**: Vehicles with ABS exempt from unladen compatibility bands since ABS prevents wheel lock-up and maintains stability across all loads.
- **Emerging Challenge**: Modern trucks using endurance/electric recuperative braking reduce friction-brake use, causing pads to not reach optimal operating temperature ("fall-asleep" effect).
- **Compatibility Band Solution**: Raise upper band for ≥500 kPa by revising semitrailer diagram 4A and adding new full-trailer diagram 5; maintain current band below 500 kPa.
- **Automatically Commanded Braking**: Function within complex electronic control system for generating vehicle retardation via automatic evaluation of on-board information.
- **Selective Braking**: Function for vehicle behaviour modification via automatic individual brake actuation.
- **Braking/Emergency Braking Signals**: Logic signals per §5.2.22 and §5.2.23 respectively.

^[raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md]
^[raw/papers/EX_06_UN_R13-H_01_Suppl.5_Passenger_car_braking.md]

## Source Documents

- [EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md](raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md)
- [EX_06_UN_R13-H_01_Suppl.5_Passenger_car_braking.md](raw/papers/EX_06_UN_R13-H_01_Suppl.5_Passenger_car_braking.md)

## Cross-References

- [[gb-21670-braking]]
- [[gb-12676-braking]]
- [[un-r152-aebs]]
- [[un-r131-aebs]]
