---
title: OTA Software Update Framework
created: 2026-08-06
updated: 2026-08-06
type: concept
tags: [ota, overview, glossary, requirement, test-method]
sources: [raw/papers/OTA_1_1_GB_44496-2024.md, raw/papers/CS_1_1_GB_44495-2024.md]
confidence: high
---

# OTA Software Update Framework

## Definition

Over-the-air (OTA) software updates enable remote software updates to vehicle systems via
wireless communication, without physical connection. GB 44496-2024 defines the complete
regulatory framework for vehicle software updates in China, covering management system
requirements, vehicle-side technical requirements, type approval criteria, user notification
obligations, and standardized test methods. The standard applies to M, N, and O category
vehicles equipped with software update functionality. ^[raw/papers/OTA_1_1_GB_44496-2024.md]

OTA updates are closely linked to cybersecurity (GB 44495-2024 Clause 7.3 requires software
upgrade security) and functional safety (updates must not introduce unreasonable risk during
execution). The framework distinguishes between online updates (OTA, via wireless) and offline
updates (via OBD, USB, or other physical connections).

## Regulatory Landscape

### Primary Standard

1. **[[gb-44496-2024]]** — GB 44496-2024: 汽车软件升级通用技术要求 (General technical
   requirements for software update of vehicles). Published 2024-08-23, effective 2026-01-01.
   Amendment No.1 approved 2026-01-28. The standard covers:
   - **Clause 4 — Software Update Management System (SUMS):** Manufacturer must establish SUMS
     including software version identification, compatibility verification, target vehicle
     identification, impact assessment on type approval, user notification process, and
     record-keeping (at least 10 years post-production discontinuation)
   - **Clause 5 — Vehicle Requirements:** Vehicle must protect update package authenticity and
     integrity; support SWIN (Software Identification Number) reading via standard interface
     (OBD); protect stored SWIN from tampering; for OTA: pre-update user notification (purpose,
     changes, duration, unavailable functions, safety instructions); user confirmation required;
     sufficient battery; vehicle immobility during safety-critical updates; result notification;
     rollback to safe state on failure
   - **Clause 6 — Test Methods:** 13 test procedures including package integrity test, SWIN
     update/read test, tamper protection test, user notification test, user confirmation test,
     prerequisite test, power assurance test, vehicle safety test, driving safety test, door
     anti-lock test, result notification test, and failure handling test
   - **Clause 7 — Same-Type Judgment:** Criteria for vehicle type equivalency (9 criteria for
     offline-only, 13 criteria for OTA-capable vehicles)
   - **Clause 8 — User Documentation:** Product manual must declare OTA capability, describe
     failure safe state, and provide operating instructions
   - **Clause 9 — Implementation:** New type approvals: effective from implementation date +7
     months (per Amendment No.1); existing type approvals: effective from implementation date
     +25 months

   ^[raw/papers/OTA_1_1_GB_44496-2024.md]

### Related Standards

2. **[[gb-44495-2024]]** — GB 44495-2024 Clause 7.3 specifies software upgrade security
   requirements as part of vehicle cybersecurity technical requirements. OTA security testing
   follows GB 44495-2024 Section 8.3.4.2.2 (OTA) and 8.3.4.3 (offline).
   ^[raw/papers/CS_1_1_GB_44495-2024.md]

3. **[[gb-t-44464-2024]]** — Data security requirements apply to OTA data handling and
   user information collected during update processes.

4. **[[internal-security-specs]]** — Internal secure flashing specification (REQ_08) defines
   implementation-level requirements for OTA/flashing security.

## Key Concepts

- **SUMS (Software Update Management System / 软件升级管理体系):** Systematic approach for
  managing vehicle software updates safely — renamed to "软件升级保障要求" (Software Update
  Assurance Requirements) per Amendment No.1 (2026-01-28)
- **OTA Update (在线升级):** Software update transmitted via wireless communication (not OBD/USB)
- **Offline Update (离线升级):** Software update via physical connection (OBD, USB, etc.)
- **SWIN (Software Identification Number / 软件识别码):** Manufacturer-defined identifier for
  type-approval-related vehicle system software information; not equivalent to software version
  number; must be unique, readable via standard interface (OBD), and protected from tampering
- **Update Package (升级包):** Software package used for performing a software update
- **Execution (执行):** Process of installing and activating a downloaded update package
- **Safe State (安全状态):** Vehicle operating mode with no unreasonable risk — target state
  for failed OTA updates
- **Integrity Validation Data (完整性校验值):** Data used to verify package integrity (e.g., hash)
- **On-Board Software Update System (车载软件升级系统):** Vehicle-side hardware/software for
  receiving, verifying, and distributing update packages from external sources
- **Vehicle System (车辆系统):** Group of components/subsystems implementing vehicle functions
- **Vehicle User (车辆用户):** Person who operates, drives, owns, or manages the vehicle

^[raw/papers/OTA_1_1_GB_44496-2024.md]

## Key Process Requirements (Clause 4.2)

The SUMS must include processes for:
1. Unique identification of software versions and hardware component info
2. SWIN access and update (when SWIN is present)
3. Target vehicle identification for each update
4. Compatibility verification (software/hardware configuration match)
5. Inter-system dependency identification
6. Type approval impact assessment (does update affect type-approval parameters?)
7. Functional change assessment (does update add/modify/enable functions not present at approval?)
8. Other system impact assessment (safety-relevant systems)
9. User notification of each software update

^[raw/papers/OTA_1_1_GB_44496-2024.md]

## Vehicle Requirements Summary (Clause 5)

- Package authenticity and integrity protection (Clause 5.1.1)
- SWIN update capability and OBD readability (Clause 5.1.2-5.1.3)
- SWIN tamper protection (Clause 5.1.4)
- Pre-OTA user notification: purpose, functional changes, expected duration, unavailable
  functions, safety instructions (Clause 5.2.1)
- User confirmation before OTA execution (Clause 5.2.2)
- Prerequisite verification including sufficient battery (Clause 5.2.3-5.2.4)
- Safety measures during OTA that may affect vehicle/driving safety (Clause 5.2.5-5.2.6)
- Door unlock must remain available during OTA (Clause 5.2.7)
- Post-OTA result notification (success/failure) (Clause 5.2.8)
- Rollback to previous version or safe state on failure (Clause 5.2.9)

^[raw/papers/OTA_1_1_GB_44496-2024.md]

## Timeline

- 2024-08-23: GB 44496-2024 published
- 2026-01-01: GB 44496-2024 effective date
- 2026-01-28: Amendment No.1 approved (renamed SUMS to "assurance requirements", extended
  new type approval deadline by 7 months, modified same-type judgment validity to 3 years)
- New type approvals: effective from implementation date +7 months
- Existing type approvals: effective from implementation date +25 months

^[raw/papers/OTA_1_1_GB_44496-2024.md]

## Cross-References

- [[vehicle-cybersecurity-framework]] — OTA security is a key cybersecurity concern
- [[functional-safety-framework]] — OTA updates must not compromise FuSa
- [[emission-regulations-framework]] — OTA may affect emission-related software
- [[adas-automated-driving-framework]] — OTA for ADAS function updates
- [[internal-security-specs]] — Secure flashing specification (REQ_08)
- [[gb-17675-steering]] — OTA may affect steering system calibration
- [[gb-21670-braking]] — OTA may affect braking system software
- [[gb-t-44464-2024]] — Data security during OTA data handling
