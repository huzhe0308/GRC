---
title: ECall Emergency Call Framework
created: 2026-08-06
updated: 2026-08-06
type: concept
tags: [ecall, overview, glossary, requirement]
sources: [raw/papers/BS EN 15722-2020 1.md, raw/papers/ECall法规-中东沙特-SASO2944-2023 1.md, raw/papers/ECall法规-中东阿联酋-UAE-S5019-2024 1.md]
confidence: high
---

# ECall Emergency Call Framework

## Definition

Emergency Call (eCall) systems automatically or manually initiate emergency calls from vehicles
to Public Safety Answering Points (PSAPs) with standardized Minimum Set of Data (MSD) including
vehicle location, VIN, timestamp, and crash severity. The regulatory framework spans European
(EN 15722), Middle Eastern (SASO 2944, UAE S5019), and other regional implementations, each
defining technical requirements for in-vehicle emergency call systems, communication protocols,
data formats, and performance criteria.

## Regulatory Landscape

### European Standard

1. **[[bs-en-15722-2020]]** — BS EN 15722:2020: Intelligent transport systems — ESafety —
   ECall minimum set of data (MSD). Published 30 September 2020, supersedes EN 15722:2015.
   Approved by CEN on 5 July 2020, corrected November 2020. ICS: 03.220.20; 13.200; 35.240.60.
   - Defines the standardized data package transmitted during an eCall
   - Covers MSD data concepts, representation, format versions, and ASN.1 encoding
   - The MSD includes: control flags, vehicle identifier (VIN), vehicle propulsion type,
     timestamp, vehicle location (latitude/longitude with confidence), and optional
     diagnostic data
   - Implemented as national standard by all CEN members (33 European countries)
   - Referenced by EU Regulation 2015/758 (mandatory eCall in all new M1/N1 vehicles from 2018)

   ^[raw/papers/BS EN 15722-2020 1.md]

### Middle East Standards

2. **[[ecall-middle-east]]** — Two regional Middle Eastern standards for vehicle eCall:

   - **Saudi Arabia — SASO 2944:2023 (Draft):** Motor vehicle — Technical requirements for
     emergency calls "eCall". Published by Saudi Standards, Metrology and Quality Org (SASO).
     ICS: 43.020. Currently a draft standard (SASO/DS 2944:2023) circulated for comment, subject
     to change until approved by Board of Directors. Defines technical requirements for in-vehicle
     eCall systems including crash detection, communication protocols, and data transmission.

   - **UAE — S5019:2024:** UAE national standard for emergency call system requirements.
     Defines eCall system technical specifications for vehicles in the United Arab Emirates.

   ^[raw/papers/ECall法规-中东沙特-SASO2944-2023 1.md] ^[raw/papers/ECall法规-中东阿联酋-UAE-S5019-2024 1.md]

### Relationship to Other Standards

3. **[[gb-44495-2024]]** — GB 44495 cybersecurity standard includes requirements for
   communication security relevant to eCall data transmission
4. **[[gb-t-44464-2024]]** — Data security requirements apply to personal data handled by eCall
5. **[[gb-44496-2024]]** — OTA update requirements for eCall software updates

## Key Concepts

- **eCall:** Automated or manual emergency call from vehicle to PSAP, triggered by crash sensors
  (automatic) or occupant button press (manual)
- **MSD (Minimum Set of Data):** Standardized data package defined in EN 15722, transmitted
  during eCall. Includes: control flags, VIN (17 characters), vehicle propulsion type (gasoline/
  diesel/electric/hybrid/CNG/LPG/hydrogen), timestamp (Unix epoch), vehicle location
  (latitude/longitude WGS84), location confidence, direction (optional), and optional diagnostic
  data. Total size: ~140 bytes. Encoded using ASN.1 PER (Packed Encoding Rules).
- **PSAP (Public Safety Answering Point):** Emergency services call center receiving and
  processing eCalls. Each country operates its own PSAP network.
- **112-based eCall:** European eCall uses the pan-European emergency number 112 for voice
  call establishment
- **TPS (Time to First Call):** Maximum time from crash event to emergency call initiation
- **Position Accuracy:** GPS/GNSS positioning requirements for vehicle location reporting
- **ASN.1 PER:** Abstract Syntax Notation One Packed Encoding Rules — encoding format for MSD
- **VIN (Vehicle Identification Number):** 17-character unique vehicle identifier included in MSD

^[raw/papers/BS EN 15722-2020 1.md] ^[raw/papers/ECall法规-中东沙特-SASO2944-2023 1.md]

## Timeline

- 2015: EN 15722:2015 published (superseded)
- 2018: EU mandatory eCall for new M1/N1 type approvals (EU Reg 2015/758)
- 2020-07-05: EN 15722:2020 approved by CEN
- 2020-09-30: BS EN 15722:2020 published (UK implementation)
- 2020-11-04: Corrigendum issued by CEN
- 2023: SASO/DS 2944:2023 (Saudi Arabia eCall) draft circulated for comment
- 2024: UAE S5019:2024 published

^[raw/papers/BS EN 15722-2020 1.md] ^[raw/papers/ECall法规-中东沙特-SASO2944-2023 1.md] ^[raw/papers/ECall法规-中东阿联酋-UAE-S5019-2024 1.md]

## Cross-References

- [[vehicle-cybersecurity-framework]] — eCall systems handle personal location data
- [[ota-software-update-framework]] — OTA for eCall software
- [[ev-safety-framework]] — EV crash scenarios trigger eCall
- [[gb-t-44464-2024]] — Data security requirements for eCall personal data
- [[gb-44496-2024]] — OTA update requirements for eCall software
- [[korean-reg-1520]] — Korean regulations may include eCall requirements
