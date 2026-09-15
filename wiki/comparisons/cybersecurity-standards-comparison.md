---
title: Cybersecurity Standards Comparison — GB 44495 vs ISO/SAE 21434 vs UN R155
created: 2026-08-06
updated: 2026-08-06
type: comparison
tags: [cybersecurity, comparison, requirement, test-method, csms]
sources: [raw/papers/CS_1_1_GB_44495-2024.md, raw/papers/CS_1_6_ISO+SAE_21434-2021.md, raw/papers/UN-R_155-00_S3_EN_2025-01-03.md]
confidence: high
---

# Cybersecurity Standards Comparison

## What is being compared

Three pillars of vehicle cybersecurity regulation: the Chinese national standard (GB 44495-2024),
the international engineering standard (ISO/SAE 21434:2021), and the UN type approval regulation
(UN R155). These are complementary but serve fundamentally different purposes in the regulatory
ecosystem. Understanding their relationships is critical for OEMs operating in multiple markets.

The comparison is necessary because automotive cybersecurity requires a layered approach:
engineering processes (how to design secure systems), regulatory compliance (what must be
demonstrated for market access), and national implementation (country-specific technical
requirements). These three standards represent each layer.

^[raw/papers/CS_1_1_GB_44495-2024.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md] ^[raw/papers/UN-R_155-00_S3_EN_2025-01-03.md]

## Comparison Table

| Dimension | [[gb-44495-2024]] | [[iso-sae-21434-2021]] | [[un-r155]] |
|---|---|---|---|
| **Type** | Chinese National Standard (GB, mandatory) | International Standard (voluntary) | UN Regulation (type approval) |
| **Issuing Body** | SAMR / 国家市场监督管理总局 | ISO/SAE Joint Working Group | UNECE WP.29 |
| **Published** | 2024-08-23 | 2021-08 | 2021-01 (S3: 2025-01-03) |
| **Effective** | 2026-01-01 (new types), 2027 (all types) | N/A (voluntary) | 2022-01 (new types), 2024-01 (all) |
| **Standard Number** | GB 44495-2024 | ISO/SAE 21434:2021 | UN Regulation No. 155 |
| **Scope** | Vehicle cybersecurity technical requirements + CSMS | Full lifecycle cybersecurity engineering | CSMS + vehicle type approval |
| **Focus** | Technical requirements, test methods, same-type judgment | Process, methods, artifacts, risk management | Regulatory approval framework, audit |
| **CSMS Required** | Yes (Clause 5 — management system requirements) | Yes (Clause 5 — defines CSMS process) | Yes (mandates CSMS for type approval) |
| **TARA** | References risk assessment (Clause 5.2) | Defines TARA methodology (Clause 8) | Requires implementation, references ISO/SAE 21434 |
| **Applicability** | M, N, O category with ≥1 ECU | All road vehicles (E/E systems) | M, N, O category with ≥1 ECU |
| **Key Clauses** | 5: CSMS, 6: Basic req, 7: Tech req, 8: Test, 9: Same-type | 5: Org mgmt, 7-8: TARA, 9-10: Dev, 11: Prod | 5: CSMS, 7: Type approval, Annex: Threats |
| **Test Methods** | Detailed (Clause 8: external connection, communication, OTA) | N/A (process standard) | References national/regional implementation |
| **Same-Type Judgment** | Yes (Clause 9 — detailed criteria) | N/A | N/A (type approval process) |
| **Vehicle Lifecycle** | Development → Production → Post-production | Concept → Dev → Production → Operations → Decommission | Development → Production → Post-production |
| **Relationship** | References UN R155 in foreword | Engineering basis for GB 44495 and UN R155 | Referenced by GB 44495 |
| **Normative References** | GB/T 40861, GB/T 44373, GB/T 44464, GB 44496 | ISO 26262 (safety), SAE J3061 (superseded) | 1958 Agreement, ISO/SAE 21434 (referenced) |

^[raw/papers/CS_1_1_GB_44495-2024.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md] ^[raw/papers/UN-R_155-00_S3_EN_2025-01-03.md]

## Analysis

### Layer 1: Engineering Foundation — ISO/SAE 21434

ISO/SAE 21434:2021 is the foundational engineering standard for automotive cybersecurity. It
defines HOW organizations should engineer secure vehicle systems across the full lifecycle:
concept phase, product development, production, operations, and decommissioning. The standard
introduces Threat Analysis and Risk Assessment (TARA) as the core methodology for identifying
assets, threat scenarios, attack feasibility, impact rating, and risk treatment. It covers
organizational cybersecurity management (Clause 5), distributed cybersecurity activities
(Clause 6), item definition (Clause 7), TARA (Clause 8), product development (Clauses 9-10),
and production/post-production (Clauses 11-12). The standard is voluntary but de facto mandatory
because UN R155 and GB 44495 both expect organizations to follow its methodology.

^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md]

### Layer 2: International Regulatory Framework — UN R155

UN R155 establishes the regulatory requirement for vehicle type approval with regard to
cybersecurity. It mandates that manufacturers implement a Cybersecurity Management System
(CSMS) and demonstrate compliance through type approval. The regulation requires OEMs to:
(1) implement CSMS covering the full vehicle lifecycle, (2) demonstrate risk management
capabilities including threat identification and vulnerability handling, (3) ensure supplier
cybersecurity management, (4) maintain monitoring and incident response capabilities
post-production. UN R155 includes Annex 5 with a list of threats and corresponding mitigations
that must be addressed. The regulation applies to M, N, and O category vehicles with at least
one ECU. Contracting parties to the 1958 Agreement must adopt it for national type approval.

^[raw/papers/UN-R_155-00_S3_EN_2025-01-03.md]

### Layer 3: Chinese National Implementation — GB 44495

GB 44495-2024 is the Chinese mandatory national standard implementing vehicle cybersecurity
requirements. Published 2024-08-23, effective 2026-01-01, it explicitly references UN R155 in
its foreword. The standard goes beyond UN R155 by adding specific technical requirements and
testable criteria. Key additions include:

- **Clause 5 — CSMS Management Requirements:** Manufacturer must establish CSMS covering
  development, production, and post-production phases with risk identification, assessment,
  classification, and treatment processes
- **Clause 6 — Basic Requirements:** Product development follows CSMS; key element
  identification; risk treatment; attack monitoring/detection/forensics; cryptographic
  algorithm requirements (public, published, valid); default security settings
- **Clause 7 — Technical Requirements:** External connection security (no unresolved high+
  vulnerabilities, close non-essential ports, authentication for remote control),
  communication security (V2X certificate validation, wireless integrity, DoS detection),
  software upgrade security (references GB 44496)
- **Clause 8 — Test Methods:** Specific test procedures for external connection, communication,
  and software upgrade security — this is unique to GB 44495 and not present in ISO/SAE 21434
  or UN R155
- **Clause 9 — Same-Type Judgment:** Criteria for determining vehicle type equivalency for
  type approval — a Chinese regulatory concept not present in the other standards

^[raw/papers/CS_1_1_GB_44495-2024.md]

### Key Differences

1. **Scope depth:** ISO/SAE 21434 provides engineering process depth (how to do it);
   UN R155 provides regulatory framework depth (what to demonstrate); GB 44495 provides
   technical implementation depth (specific requirements and testable criteria).

2. **Test methods:** Only GB 44495 includes detailed test procedures. ISO/SAE 21434 is a
   process standard without test methods. UN R155 references national/regional implementations
   for testing.

3. **Same-type judgment:** Only GB 44495 defines formal criteria (Clause 9) for determining
   when vehicle variants share the same cybersecurity type. This is a Chinese regulatory
   concept specific to the national type approval system.

4. **Timeline alignment:** GB 44495's 2026-01-01 effective date aligns with the UN R155
   requirement for all vehicle types (2024-01), giving Chinese OEMs a structured transition
   period aligned with international obligations.

## Verdict

These three standards form a coherent regulatory stack: ISO/SAE 21434 (engineering methodology)
→ UN R155 (international regulation) → GB 44495 (Chinese national implementation). They are
complementary, not competing:

- An OEM implementing ISO/SAE 21434 processes will have the engineering foundation needed
  for both UN R155 and GB 44495 compliance
- UN R155 type approval demonstrates international regulatory compliance for export markets
- GB 44495 compliance is mandatory for Chinese domestic market access with additional
  technical requirements and test methods beyond UN R155

An OEM operating in China must comply with all three: implement ISO/SAE 21434 processes,
obtain UN R155 type approval for export markets (or as referenced by GB 44495), and meet
GB 44495 technical requirements and test methods for domestic market access. The unique
Chinese additions (detailed test methods, same-type judgment, specific technical thresholds)
require dedicated engineering effort beyond what ISO/SAE 21434 or UN R155 alone would
necessitate.

^[raw/papers/CS_1_1_GB_44495-2024.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md] ^[raw/papers/UN-R_155-00_S3_EN_2025-01-03.md]

## Cross-References

- [[vehicle-cybersecurity-framework]] — Full cybersecurity concept overview
- [[internal-security-specs]] — Internal specs implementing these requirements
- [[gb-t-44464-2024]] — Data security (complementary standard)
- [[ais-189-csms]] — India's CSMS standard (parallel implementation)
- [[fusa-vs-cybersecurity-vs-sotif]] — Comparison with FuSa and SOTIF domains
