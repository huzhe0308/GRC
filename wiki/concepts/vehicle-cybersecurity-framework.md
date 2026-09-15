---
title: Vehicle Cybersecurity Framework
created: 2026-08-06
updated: 2026-08-06
type: concept
tags: [cybersecurity, overview, glossary]
sources: [raw/papers/CS_1_1_GB_44495-2024.md, raw/papers/CS_1_6_ISO+SAE_21434-2021.md, raw/papers/UN-R_155-00_S3_EN_2025-01-03.md]
confidence: high
---

# Vehicle Cybersecurity Framework

## Definition

Vehicle cybersecurity refers to the protection of automotive electrical/electronic (E/E) systems,
components, and functions so that their assets are not compromised by threats. It encompasses
the full vehicle lifecycle: development, production, and post-production.

## Regulatory Landscape

The cybersecurity domain is governed by three interconnected pillars:

1. **[[iso-sae-21434-2021]]** — The international standard for automotive cybersecurity engineering.
   Defines requirements for cybersecurity management, risk assessment (TARA), and product development.
   Supersedes SAE J3061:2016. ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md]

2. **[[un-r155]]** — UN regulation mandating a Cybersecurity Management System (CSMS) and type approval
   for vehicle cybersecurity. Requires OEMs to demonstrate risk management capabilities across the
   vehicle lifecycle. Effective from 2022 for new type approvals. ^[raw/papers/UN-R_155-00_S3_EN_2025-01-03.md]

3. **[[gb-44495-2024]]** — Chinese national standard for vehicle cybersecurity technical requirements.
   References UN R155 and mandates CSMS, information security basic requirements, and technical
   requirements. Effective 2026-01-01. ^[raw/papers/CS_1_1_GB_44495-2024.md]

Supporting standards in this domain include [[gb-t-44464-2024]] (data security),
[[gb-t-46194-2025]], [[gb-t-45181-2024]], [[gb-t-47324-2026]], and
[[internal-security-specs]] (secure boot, storage, diagnosis, flashing).

Regional implementations: [[ais-189-csms]] (India), [[csms-notification]] (notification),
[[korean-reg-1520]] (Korea). ^[raw/papers/CS_1_1_GB_44495-2024.md] ^[raw/papers/UN-R_155-00_S3_EN_2025-01-03.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md]

## Key Concepts

- **CSMS (Cybersecurity Management System):** Risk-based systematic approach including organizational
  processes, responsibilities, and governance to manage vehicle cyber threats.
- **TARA (Threat Analysis and Risk Assessment):** Method defined in ISO/SAE 21434 for identifying
  assets, threat scenarios, impact rating, attack feasibility, and risk treatment.
- **Risk:** Expressed as a combination of attack feasibility and impact severity.
- **Vulnerability:** Weakness in an asset or mitigation measure that can be exploited by threats.
- **Vehicle Lifecycle:** Development → Production → Post-development (operations, maintenance,
  incident response, decommissioning).

## Cross-References

- [[functional-safety-framework]] — Related safety domain (FuSa vs Cybersecurity)
- [[gb-44496-2024]] — OTA updates, closely linked to cybersecurity
- [[gb-t-44373-2024]] — Terminology and definitions for ICV
- [[ota-software-update-framework]] — OTA updates, cybersecurity implications
- [[ev-safety-framework]] — EV safety, cybersecurity for high-voltage systems
- [[ecall-emergency-call-framework]] — Emergency call systems, data security
- [[cybersecurity-standards-comparison]] — Detailed comparison of GB 44495 vs ISO/SAE 21434 vs UN R155
