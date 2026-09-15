---
title: AIS-189 — India CSMS Certification
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [cybersecurity, csms, other-national, requirement, vehicle-testing]
sources: ['raw/papers/AIS-189_CSMS.md']
confidence: high
---

# AIS-189 — India CSMS Certification

## Overview

AIS-189 is an Indian Automotive Industry Standard establishing uniform provisions for the approval of vehicles with regard to Cyber Security and Cyber Security Management System (CSMS). Published in April 2024 by the Automotive Research Association of India (ARAI) on behalf of the Automotive Industry Standards Committee (AISC), it was developed under the Ministry of Road Transport and Highways (MoRTH). The standard derives considerable assistance from UN Regulation No. 155 (UN R155), which entered into force on 22 January 2021. AIS-189 is structured in 8 clauses plus 6 annexures (A–F) totaling 27 pages, covering the full CSMS certification lifecycle from application through modification and extension of type approvals.

## Key Facts

| Field | Value |
|-------|-------|
| Standard Number | AIS-189 |
| Full Title (EN) | Approval of Vehicles with regards to Cyber Security and Management System |
| Issuing Body | ARAI / AISC / CMVR-TSC, Ministry of Road Transport and Highways, Government of India |
| Published Date | April 2024 |
| Effective Date | Per CMVR implementation schedule |
| Applicable Vehicle Categories | M, N; Category T (if fitted with ≥1 ECU); L7 (if equipped with automated driving Level 3+) |
| Based On | UN R155 (entry into force 22 Jan 2021) |
| SAE Automation Ref | SAE J-3016 for automation levels |
| Document Structure | 8 clauses + 6 annexures (A–F), 27 pages |

## Scope and Requirements

- **Clause 1.1**: Applies to vehicles of Categories M and N with regard to cyber security; also applies to Category T vehicles if fitted with at least one Electronic Control Unit (ECU) (Clause 1.1)
- **Clause 1.2**: Applies to Category L7 vehicles if equipped with automated driving functionalities from Level 3 onwards per SAE J-3016 (Clause 1.2)
- **Clause 2**: Defines key terms including "Cyber Security" (condition where road vehicles and their functions are protected from cyber threats to E/E components), "CSMS" (systematic risk-based approach defining organizational processes, responsibilities and governance), "Risk Assessment", "Risk Management", "Threat", "Vulnerability", and "Mitigation"
- **Clause 3**: Application for approval must be submitted by the vehicle manufacturer or their accredited representative, accompanied by a description of the vehicle type (Annexure A) and the Certificate of Compliance for CSMS (Clause 6)
- **Clause 5.1.1**: Test Agency verifies by document checks that the manufacturer has: (a) collected and verified supply chain risk information; (b) documented risk assessments, test results and mitigations; (c) implemented appropriate cyber security measures in design; (d) established detection and response to cyber attacks; (e) logged data to support forensic analysis of attempted/successful attacks
- **Clause 5.1.2**: Test Agency verifies by testing (sampling focused on risks assessed as high) that the manufacturer has implemented documented cyber security measures
- **Clause 5.1.3**: Test Agency refuses type approval if the manufacturer did not perform exhaustive risk assessment (Clause 7.3.3), did not protect against identified risks, did not secure dedicated environments for aftermarket software, or did not perform sufficient pre-approval testing
- **Clause 6**: CSMS Certificate of Compliance valid for maximum 3 years; manufacturer must inform Test Agency of any change affecting CSMS relevance; renewal requires new assessment
- **Clause 7.2.2.1**: CSMS must cover development phase, production phase, and post-production phase
- **Clause 7.2.2.2**: CSMS processes must ensure security is adequately considered, including risks and mitigations listed in Annexure D (threats spanning pages 12–24, covering 13 threat categories)
- **Annexure A**: Information document template for vehicle type description
- **Annexure C**: Model certificate of compliance for CSMS
- **Annexure D**: Comprehensive List of Threats and Corresponding Mitigations (pages 12–24)
- **Clause 8**: Covers modification and extension of vehicle type approvals

## Technical Details

- CSMS Certificate validity: **3 years maximum** from date of deliverance (Clause 6.7)
- Documentation retention period: **10 years** from discontinuation of vehicle type production (Clause 3.3(a))
- Test Agency personnel must have cyber security skills and automotive risk assessment knowledge (e.g., ISO 26262-2018, ISO/PAS 21448-2019, ISO/SAE 21434-2021) (Clause 5.3.1(a))
- Reference standards: ISO 26262-2018, ISO/PAS 21448-2019, ISO/SAE 21434-2021
- The standard explicitly states it cannot include all possible security threats; real-world conditions and threats should not result in system failure

## Source Documents

- [AIS-189_CSMS.md](raw/papers/AIS-189_CSMS.md)

## Cross-References

- [[iso-sae-21434-2021]]
- [[un-r155]]
- [[csms-notification]]
- [[gb-44495-2024]]
