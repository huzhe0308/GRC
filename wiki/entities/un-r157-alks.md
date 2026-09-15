---
title: UN R157 ALKS Regulation
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [automated-driving, adas, un-regulation, requirement]
sources: ['raw/papers/EX_08_UN_R157_01_Suppl.4_ALKS.md']
confidence: high
---

# UN R157 ALKS Regulation

## Overview

UN Regulation No. 157 establishes uniform provisions for the approval of vehicles with regard to Automated Lane Keeping Systems (ALKS). The regulation defines requirements for systems activated by the driver that keep the vehicle within its lane at speeds up to 130 km/h by controlling lateral and longitudinal movements for extended periods without further driver input. Supplement 4 introduces terminology harmonization (replacing "engine/run cycle" with "powertrain") and restricts heavy-vehicle lane changes to speed-limited lanes to prevent dangerous speed differentials. The regulation represents a key framework for L3 automated driving approval in contracting parties to the 1958 Agreement.

## Key Facts

| Field | Value |
|-------|-------|
| Regulation Number | UN R157 |
| Full Title | Uniform provisions concerning the approval of vehicles with regard to Automated Lane Keeping |
| Current Version | 01 series of amendments, Revision 1, Amendment 4 (Supplement 4) |
| 01 Series Entry into Force | 2023-01-04 |
| Supplement 1 | 2023-09-24 |
| Supplement 2 | 2024-06-15 |
| Supplement 3 | 2025-06-12 |
| Supplement 4 | 2026-01-11 |
| Issuing Body | UNECE |
| Applicable Categories | M and N category vehicles |

## Scope and Requirements

- **Scope**: Applies to type approval of M and N category vehicles with regard to ALKS
- **System Definition**: ALKS is activated by the driver and keeps the vehicle within its lane at speeds of 130 km/h or less by controlling lateral and longitudinal movements for extended periods without further driver input
- **Sensing Capabilities**: Vehicles must have adequate sensing capabilities around the vehicle to safely assess situations and take appropriate action
- **Lane Change Conditions**: Intentional lane crossing permitted for:
  - Lane change procedures (driver-triggered)
  - Evasive emergency actions
  - Creating access corridors for emergency/enforcement vehicles
  - Navigating around partial obstructions
- **Operational Design Domain**: System must comply with defined ODD including environmental, geographical, and infrastructural limitations
- **Traffic Rule Compliance**: Activated system shall comply with traffic rules in the country of operation, including responding to emergency/enforcement vehicles
- **Transition Demand**: Transition demand (system to human driver) shall not endanger vehicle occupants or other road users; if driver fails to resume control, system shall perform Minimum Risk Manoeuvre (MRM)
- **Self-Checks**: System shall perform self-checks to detect failures and confirm performance at all times
- **Supplement 4 Changes**:
  - Introduces technology-neutral "powertrain" terminology (replacing "engine/run cycle")
  - Restricts heavy vehicles (N₃/M₃) to lane changes only into speed-limited lanes to prevent dangerous speed differentials
  - Rationale: Changing into unrestricted-speed lanes exposes following traffic to dangerous speed differentials and cannot be justified by merely assuming on-coming vehicle speeds

## Technical Details

- Maximum operating speed: 130 km/h
- Lane change restriction (Supplement 4): N₃/M₃ heavy vehicles limited to speed-limited lanes only
- MRM (Minimum Risk Manoeuvre): executed when driver fails to respond to transition demand
- ODD compliance: environmental, geographical, and infrastructural constraints
- Sensing: 360° situational awareness required around the vehicle
- Transition demand: must not endanger occupants or other road users

## Source Documents

- [EX_08_UN_R157_01_Suppl.4_ALKS.md](raw/papers/EX_08_UN_R157_01_Suppl.4_ALKS.md)

## Cross-References

- [[un-r152-aebs]]
- [[un-r131-aebs]]
- [[un-r79-steering]]
- [[gb-t-44721-2024]]
