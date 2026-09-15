---
title: ECall Regulations — Middle East (Saudi & UAE)
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [ecall, other-national, requirement, test-method, timeline]
sources: ['raw/papers/ECall法规-中东沙特-SASO2944-2023 1.md', 'raw/papers/ECall法规-中东阿联酋-UAE-S5019-2024 1.md']
confidence: high
---

# ECall Regulations — Middle East (Saudi & UAE)

## Overview

Two Middle Eastern countries have established mandatory eCall (emergency call) regulations for motor vehicles. Saudi Arabia published SASO 2944:2023, and the United Arab Emirates published UAE.S 5019:2024 through the Ministry of Industry & Advanced Technology (MOIAT). Both regulations require new light vehicles to be equipped with eCall systems capable of automatically or manually triggering emergency calls to number 999 and transmitting a Minimum Set of Data (MSD) to Public Safety Answering Points (PSAPs). The UAE regulation was extracted as full text; the Saudi source document is image-only (binary PDF) but follows a similar regulatory scope for the Saudi market.

## Key Facts

| Field | Saudi Arabia | United Arab Emirates |
|-------|-------------|---------------------|
| Standard Number | SASO 2944:2023 | UAE.S 5019:2024 |
| Issuing Body | Saudi Standards Organization (SASO) | Ministry of Industry & Advanced Technology (MOIAT) |
| Full Title (EN) | eCall Emergency Call Technical Requirements | Motor vehicle — "eCall" Emergency Calls Technical Requirements |
| ICS Code | — | 43.020 |
| Applicable Vehicles | New light vehicles | Passenger vehicles ≤8 seats + ≤3.5 t; Goods vehicles ≤3.5 t |
| Emergency Number | — | 999 |
| MSD Reference | EN 15722 | EN 15722:2015 |
| Test References | — | EU Delegated Regulation 2017/79 (Annexes I–VIII) |

## Scope and Requirements

- **Scope (UAE Clause 1):** Applies to new light vehicles for passenger/baggage transport with weight not exceeding 3,500 kg, imported or manufactured for registration and licensing in the UAE.
- **eCall Definition (UAE 2.1):** Calling emergency number 999, triggered automatically by in-vehicle sensors or manually by passengers, transferring a minimum set of data (MSD) and establishing an audio channel between the vehicle and an eCall-enabled PSAP via public mobile wireless communications networks.
- **Applicability (UAE 4.2–4.3):** Passenger vehicles ≤8 seats + driver, mass ≤3.5 t, must be equipped with eCall. Goods vehicles ≤3.5 t must also be equipped.
- **Implementation Timeline (UAE 4.4–4.5):** New models must have eCall starting from production year 2020 (model year 2021). All registered/licensed vehicles must have eCall regardless of production year as of **1 January 2028**.
- **Small Series Exemption (UAE 4.6, Table 1):** Declining thresholds: 60 vehicles (2024), 50 (2025), 40 (2026), 30 (2027).
- **System Operation (UAE 4.7–4.9):** The eCall system must make an emergency call through available public wireless communication networks after an accident. Must operate automatically after a severe accident. Must transfer MSD including dynamic data (geographic location, time) and static data (VIN, propulsion system type).
- **HMI (UAE 4.12):** Information given to passengers via HMI must be available at minimum in Arabic and English.
- **Third-Party eCall (UAE 4.13):** Third-party eCall service provision is allowed with approval of the concerned telecommunications authority.
- **Manufacturer Obligation (UAE 4.14):** Manufacturers must demonstrate that in a serious accident, eCall is automatically triggered to emergency number 999.
- **Crash Resistance (Annex 2):** Post-deceleration event, the eCall system must transmit MSD to a PSAP test point, determine up-to-date timestamp, determine accurate vehicle location, and connect/transmit data via mobile network. Test procedure per EU Delegated Regulation 2017/79 Annex I.
- **Full-Scale Impact Test (Annex 3):** Automatic triggering per UN Regulation No. 94 (Annex 3) or No. 95 (Annex 4). Manual triggering must be available. Call status indication via visual/audible signal. MSD emission and vehicle-specific data determination verified post-impact.
- **Audio Equipment Crash Resistance (Annex 4):** Loudspeakers and microphones must reconnect after MSD transmission. Hands-free voice communication of sufficient intelligibility required. Standard test sentences provided in English.
- **Automatic Triggering Documentation (Annex 5):** Manufacturer must provide a statement that triggering strategy ensures activation in accident configurations dissimilar from full-scale crash tests. Airbag control unit documentation required. Extended documentation package is confidential, may be retained by manufacturer.
- **TPS Co-existence (Annex 6):** The 112/999-based system must be deactivated while TPS is active. The 112/999-based system must auto-trigger if TPS fails. Manufacturer must provide FMEA or FTA documentation for fallback mechanism.
- **GNSS Compatibility (Annex 7):** Receiver must support GPS, GLONASS, and Galileo (L1/E1 band) plus SBAS. NMEA-0183 output (RMC, GGA, VTG, GSA, GSV messages). Horizontal position error: ≤15 m open sky (95% confidence, PDOP 2.0–2.5), ≤40 m urban canyon (95% confidence, PDOP 3.5–4.0). Cold start TTFF: ≤60 s at −130 dBm, ≤300 s at −140 dBm. Re-acquisition: ≤20 s after 60 s blockout at −130 dBm. Position fix at least every second.
- **Self-Test (Annex 8):** Self-test at each system power-up monitoring: eCall ECU, mobile network antenna, communication device, GNSS antenna/receiver, crash control unit, bus connections, SIM presence, power source. Visual tell-tale or warning message on failure detection.
- **Privacy and Data Protection (Annex 9):** System must not be traceable in normal operation (PSAP cannot initiate communication). Log files must be deleted within **13 hours** of eCall initiation. Maximum **3 recent locations** retained in internal memory. No personal data exchange between 999-based system and TPS.

## Technical Details

| Parameter | Value |
|-----------|-------|
| Emergency number | 999 |
| Vehicle weight limit | ≤3,500 kg |
| Max seats (passenger) | 8 + driver |
| Small Series threshold (2024→2027) | 60 → 50 → 40 → 30 vehicles |
| Full mandate date | 1 January 2028 |
| GNSS horizontal error (open sky) | ≤15 m at 95% confidence |
| GNSS horizontal error (urban canyon) | ≤40 m at 95% confidence |
| Cold start TTFF (−130 dBm) | ≤60 s |
| Cold start TTFF (−140 dBm) | ≤300 s |
| Re-acquisition time | ≤20 s after 60 s blockout |
| GNSS cold start (−144 dBm) | ≤3,600 s |
| GNSS tracking (−155 dBm) | ≥600 s |
| GNSS re-acquisition (−150 dBm) | ≤60 s |
| Position fix interval | ≤1 s |
| Speed range for accuracy | 0–140 km/h |
| Linear acceleration range | 0–2 g |
| Log file retention limit | 13 hours |
| Max stored locations | 3 |
| Position fix rate | At least once per second |

## Source Documents

- [ECall法规-中东沙特-SASO2944-2023 1.md](raw/papers/ECall法规-中东沙特-SASO2944-2023 1.md) — image-only PDF (binary)
- [ECall法规-中东阿联酋-UAE-S5019-2024 1.md](raw/papers/ECall法规-中东阿联酋-UAE-S5019-2024 1.md) — full text extracted

## Cross-References

- [[bs-en-15722-2020]]
- [[gb-t-34590-series]]
- [[gb-44496-2024]]
- [[un-r155]]
