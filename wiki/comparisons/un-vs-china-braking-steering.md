---
title: UN Regulations vs Chinese National Standards — Braking & Steering
created: 2026-08-06
updated: 2026-08-06
type: comparison
tags: [braking, steering, adas, comparison, requirement, test-method, vehicle-testing]
sources: [raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md, raw/papers/EX_07_UN_R152_02_Suppl.5_AEBS.md, raw/papers/FuSa_20_GB_21670-2025.md, raw/papers/FuSa_16_GB+17675-2021.md]
confidence: medium
---

# UN Regulations vs Chinese Standards — Braking & Steering

## What is being compared

UN regulations (UN R13, R79, R152, R157, R131) versus Chinese national standards (GB 21670,
GB 17675, GB 12676) for braking and steering systems. Both regulatory frameworks cover similar
technical domains — braking performance, steering requirements, AEBS, and automated driving
functions — but with different scopes, implementation approaches, and administrative procedures.

Understanding the differences is essential for OEMs operating in both European (UNECE 1958
Agreement) and Chinese markets, as vehicles must satisfy both regulatory frameworks
simultaneously.

^[raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md] ^[raw/papers/EX_07_UN_R152_02_Suppl.5_AEBS.md] ^[raw/papers/FuSa_20_GB_21670-2025.md] ^[raw/papers/FuSa_16_GB+17675-2021.md]

## Comparison Table

| Domain | UN Regulation | Chinese Standard | Key Relationship |
|---|---|---|---|
| **Passenger Car Braking** | [[un-r13-braking]] (R13-H, Suppl.5) | [[gb-21670-braking]] (GB 21670-2025) | GB 21670 adapts UN R13-H principles, adds FuSa annex |
| **Heavy Vehicle Braking** | [[un-r13-braking]] (R13, Suppl.1) | [[gb-12676-braking]] (GB 12676-2014) | GB 12676 covers commercial vehicles (2014 version) |
| **AEBS (Passenger)** | [[un-r152-aebs]] (R152, Suppl.5) | [[gb-21670-braking]] (includes AEBS) | GB 21670 incorporates AEBS requirements directly |
| **AEBS (Heavy)** | [[un-r131-aebs]] (R131, Suppl.3) | [[gb-12676-braking]] (may reference) | Separate UN regulation for heavy vehicles |
| **ALKS** | [[un-r157-alks]] (R157, Suppl.4) | (No direct GB equivalent yet) | UN R157 is standalone, no Chinese equivalent |
| **Steering** | [[un-r79-steering]] (R79, Suppl.9) | [[gb-17675-steering]] (GB 17675-2021) | GB 17675 covers steering basics + FuSa |
| **Steering FuSa** | — (within R79) | GB 17675 Appendix B | GB 17675 has dedicated FuSa appendix |
| **Functional Safety** | Referenced but not embedded | Embedded (GB 21670 Annex A, GB 17675 App. B) | Chinese standards integrate FuSa directly |
| **EMC Testing** | Referenced | GB 21670 includes EMC test procedure | Chinese standard has detailed EMC test methods |
| **Same-Type Judgment** | Extension/amendment process | 同一型式判定 (same-type judgment) | Chinese concept unique to national system |

^[raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md] ^[raw/papers/EX_07_UN_R152_02_Suppl.5_AEBS.md] ^[raw/papers/FuSa_20_GB_21670-2025.md] ^[raw/papers/FuSa_16_GB+17675-2021.md]

## Analysis

### Scope Integration

UN regulations are domain-specific, with separate regulations for each function: UN R13 for
braking, UN R79 for steering, UN R152 for passenger car AEBS, UN R131 for heavy vehicle AEBS,
and UN R157 for ALKS. This modular approach allows targeted updates to individual regulations
through supplements (e.g., R13 Suppl.6, R152 Suppl.5).

Chinese standards take a more integrated approach. GB 21670 covers passenger car braking
including ABS, AEBS, and functional safety requirements in a single standard. GB 17675 covers
steering system basic requirements including functional safety compliance in Appendix B.
This integration means a single Chinese standard may reference multiple UN regulations.

^[raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md] ^[raw/papers/FuSa_20_GB_21670-2025.md]

### Functional Safety Integration

Chinese standards like GB 17675 and GB 21670 explicitly include functional safety requirements
within the standard itself. GB 21670-2025 includes:
- Annex A (normative): Braking electronic control system functional safety requirements
- Annex B (normative): Functional safety test report requirements
- Annex C (normative): Functional safety description requirements
- Clause 5.1.3: Enhanced functional safety requirements for braking electronic control systems

GB 17675-2021 includes Appendix B dedicated to functional safety compliance for steering
systems, including EPS (Electric Power Steering) safety requirements.

UN regulations reference FuSa (e.g., R79 references safety requirements for steering) but
do not embed detailed FuSa requirements directly. The FuSa specifics are left to national
implementation or ISO 26262 compliance.

^[raw/papers/FuSa_20_GB_21670-2025.md] ^[raw/papers/FuSa_16_GB+17675-2021.md]

### Test Methods and Procedures

Chinese standards include detailed test method procedures. GB 21670 includes specific EMC
test procedures for ABS systems:
- ABS immunity testing in semi-anechoic chamber, 20 MHz–2 GHz
- Field strength: 30 V/m (RMS) in ≥90% of band
- AM modulation (1kHz, 80% depth) for 20–800 MHz
- PM modulation (577µs pulse, 4600µs period) for 800–2000 MHz
- 16 test frequency points from 27 MHz to 1800 MHz

UN regulations define performance requirements but leave implementation details to
manufacturers and technical services, referencing separate test method standards where
applicable.

^[raw/papers/FuSa_20_GB_21670-2025.md]

### Same-Type Judgment vs Type Extension

Chinese standards include 同一型式判定 (same-type judgment) criteria — a regulatory mechanism
for determining when vehicle variants share the same type approval. GB 21670 and GB 17675
both include detailed same-type judgment clauses specifying which parameters must be identical
for variants to be considered the same type.

UN regulations use a type approval extension/amendment process where variants are evaluated
against the original type approval, with separate processes for modifications and extensions.

^[raw/papers/FuSa_20_GB_21670-2025.md] ^[raw/papers/FuSa_16_GB+17675-2021.md]

### Version Management

UN regulations use supplement series (e.g., R13 Suppl.6, R152 Suppl.5, R79 Suppl.9) where
each supplement adds or modifies requirements incrementally. Contracting parties adopt
supplements at their own pace.

Chinese standards use year-dated versions (e.g., GB 17675-2021, GB 21670-2025) where each
new version may comprehensively revise the standard. GB 21670-2025 replaces GB 21670-2008
with 70+ technical modifications. Transition periods are defined within the standard.

^[raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md] ^[raw/papers/FuSa_20_GB_21670-2025.md]

## Verdict

Chinese standards increasingly align with UN regulations but maintain unique features that
reflect China's regulatory system:

1. **Integrated scope:** Chinese standards bundle multiple functions (braking + ABS + AEBS +
   FuSa) into single standards, while UN regulations separate them into individual regulations.

2. **Embedded FuSa:** Chinese standards include functional safety requirements directly,
   while UN regulations reference but do not embed FuSa details.

3. **Detailed test methods:** Chinese standards include specific test procedures (EMC,
   performance), while UN regulations focus on performance requirements.

4. **Same-type judgment:** Chinese standards include formal same-type criteria unique to
   the Chinese regulatory system, absent from UN regulations.

5. **Version management:** Chinese standards use comprehensive year-dated revisions vs.
   incremental UN supplements.

OEMs operating in both markets must satisfy both regulatory frameworks. The frameworks are
largely compatible in technical requirements but differ significantly in administrative
procedures (same-type judgment vs. extension), scope integration, and the level of FuSa
detail embedded in the standards.

^[raw/papers/EX_05_UN_R13_R15_Suppl.1_Heavy_vehicle_braking.md] ^[raw/papers/EX_07_UN_R152_02_Suppl.5_AEBS.md] ^[raw/papers/FuSa_20_GB_21670-2025.md] ^[raw/papers/FuSa_16_GB+17675-2021.md]

## Cross-References

- [[adas-automated-driving-framework]] — Full ADAS concept overview
- [[functional-safety-framework]] — FuSa requirements embedded in Chinese standards
- [[gb-t-44850-2024]] — ICV driving safety test methods
- [[un-r13-braking]] — UN R13 braking regulation details
- [[gb-21670-braking]] — GB 21670-2025 braking standard details
- [[gb-17675-steering]] — GB 17675-2021 steering standard details
