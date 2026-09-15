---
title: Functional Safety vs Cybersecurity vs SOTIF
created: 2026-08-06
updated: 2026-08-06
type: comparison
tags: [functional-safety, cybersecurity, comparison, requirement]
sources: [raw/papers/FuSa_29_GB+T_34590-1-2022.md, raw/papers/CS_1_6_ISO+SAE_21434-2021.md, raw/papers/FuSa_6_GB+T_43267-2023.md]
confidence: high
---

# Functional Safety vs Cybersecurity vs SOTIF

## What is being compared

Three distinct but complementary safety domains in automotive engineering that address
different sources of harm:

- **Functional Safety (FuSa):** Hazards from E/E system malfunctions — the system fails to
  function correctly (e.g., brake ECU fault causes unintended braking)
- **Cybersecurity:** Threats from intentional malicious attacks — an adversary exploits
  vulnerabilities to compromise vehicle systems (e.g., remote brake disable via CAN bus
  injection)
- **SOTIF (Safety of the Intended Functionality):** Hazards from intended functionality
  performance limitations — the system functions as designed but performance is insufficient
  for the operating context (e.g., camera can't detect pedestrian in fog)

Understanding the boundaries and interactions between these domains is critical for
developing safe, secure, and reliable vehicle systems. All three are mandated by separate
but related regulatory frameworks.

^[raw/papers/FuSa_29_GB+T_34590-1-2022.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md] ^[raw/papers/FuSa_6_GB+T_43267-2023.md]

## Comparison Table

| Dimension | FuSa | Cybersecurity | SOTIF |
|---|---|---|---|
| **Hazard Source** | E/E system malfunction | Intentional attack | Performance insufficiency |
| **Core Standard (CN)** | [[gb-t-34590-series]] (GB/T 34590, 11 parts) | [[gb-44495-2024]] (GB 44495) | [[gb-t-43267-2023]] (GB/T 43267) |
| **Core Standard (Intl)** | ISO 26262 | [[iso-sae-21434-2021]] (ISO/SAE 21434) | ISO 21448 |
| **Risk Assessment** | HARA → ASIL (A-D) | TARA → Risk Value | Trigger condition analysis |
| **Key Analysis** | FMEA, FTA, fault injection | Threat analysis, attack paths, vulnerability assessment | Trigger identification, sensor performance analysis |
| **Mitigation** | Safety mechanisms (redundancy, monitoring, diagnostics) | Security controls (encryption, authentication, isolation) | Design improvements, ODD constraints, sensor enhancement |
| **Lifecycle** | Concept → Dev → Production → Decommission | Dev → Production → Post-production (monitoring + response) | Concept → Dev → Production → Operation |
| **Applicable To** | All E/E safety-related systems | All E/E systems with external connectivity or attack surface | Systems with sensing/perception (ADAS, automated driving) |
| **ASIL/SIL** | ASIL A (lowest) to D (highest) | N/A (risk-based, not ASIL) | May inherit ASIL from FuSa |
| **Type of Risk** | Unreasonable risk from malfunction | Risk from cyber threats | Unreasonable risk from performance limitation |
| **Trigger** | Random hardware failure, systematic software error | Intentional exploitation by threat actor | Limitations in sensor, algorithm, or specification |
| **Verification** | Fault injection testing, FMEA verification | Penetration testing, vulnerability scanning | Scenario-based testing, edge case validation |
| **Post-Production** | Field monitoring, recall if needed | Continuous monitoring, incident response, CSMS | Operational monitoring, OTA improvements |

^[raw/papers/FuSa_29_GB+T_34590-1-2022.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md] ^[raw/papers/FuSa_6_GB+T_43267-2023.md]

## Analysis

### Cause of Harm — Fundamental Distinction

The three domains differ fundamentally in what causes harm:

1. **FuSa** addresses harm caused by E/E system malfunctions. The system has a fault (random
   hardware failure or systematic software error) that causes it to behave incorrectly. For
   example, a brake ECU software bug causes unintended braking. The mitigation is safety
   mechanisms: redundancy, monitoring, diagnostics, and safe states.

2. **Cybersecurity** addresses harm caused by intentional attacks. An adversary actively
   exploits a vulnerability in the system. For example, an attacker injects CAN bus messages
   to disable brakes remotely. The mitigation is security controls: encryption, authentication,
   intrusion detection, and access control.

3. **SOTIF** addresses harm caused by the system functioning as designed but being insufficient
   for the situation. There is no fault — the system works correctly but its performance is
   inadequate. For example, a camera-based pedestrian detection system fails in heavy fog
   because the sensor cannot see through the fog. The mitigation is design improvement
   (better sensors, algorithmic redundancy) or ODD (Operational Design Domain) restrictions.

^[raw/papers/FuSa_29_GB+T_34590-1-2022.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md] ^[raw/papers/FuSa_6_GB+T_43267-2023.md]

### Analysis Methods

Each domain uses fundamentally different analysis methods:

- **FuSa:** Deductive (FTA — Fault Tree Analysis) and inductive (FMEA — Failure Modes and
  Effects Analysis) fault analysis. HARA (Hazard Analysis and Risk Assessment) assigns ASIL
  based on severity, exposure, and controllability. Safety goals and safety concepts are
  derived from ASIL ratings.

- **Cybersecurity:** TARA (Threat Analysis and Risk Assessment) identifies assets, threat
  scenarios, attack paths, and vulnerabilities. Risk is expressed as attack feasibility ×
  impact severity. Attack paths are analyzed using attack trees. The output is a security
  concept with security controls.

- **SOTIF:** Trigger condition identification — identifying conditions under which the
  system's intended functionality may be insufficient. Sensor performance analysis, scenario
  classification (known-safe, known-unsafe, unknown). The output is an SOTIF concept with
  design improvements or ODD constraints.

^[raw/papers/FuSa_29_GB+T_34590-1-2022.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md] ^[raw/papers/FuSa_6_GB+T_43267-2023.md]

### Interactions and Dependencies

The three domains interact in important ways:

1. **Cybersecurity → FuSa:** A cybersecurity attack can cause a malfunction (e.g., attacker
   disables a safety mechanism). FuSa safety mechanisms may detect anomalies from attacks,
   providing defense-in-depth.

2. **SOTIF + FuSa:** SOTIF hazards may be exacerbated by system faults. A sensor fault
   (FuSa domain) can worsen performance limitations (SOTIF domain). Systems may share ASIL
   requirements where SOTIF mitigations are safety-related.

3. **Cybersecurity ↔ SOTIF:** Cybersecurity attacks on sensor data (e.g., spoofing) can
   create SOTIF-like hazards. Securing sensor inputs is both a cybersecurity and SOTIF
   concern.

4. **Coordinated concepts:** Modern vehicles require coordinated safety/security concepts
   that address all three domains. A brake system must be functionally safe (FuSa), secured
   against attacks (Cybersecurity), and perform adequately in all conditions (SOTIF).

^[raw/papers/FuSa_29_GB+T_34590-1-2022.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md] ^[raw/papers/FuSa_6_GB+T_43267-2023.md]

## Verdict

These three domains are complementary, not alternatives. A modern vehicle must address all
three: FuSa for malfunction risks, cybersecurity for attack risks, and SOTIF for performance
insufficiency risks. They share common lifecycle phases and safety concepts but use different
analysis methods and mitigation strategies.

In practice:
- FuSa (ISO 26262 / GB/T 34590) provides the foundational safety framework — it defines
  ASIL, safety goals, and safety concepts that other domains build upon
- Cybersecurity (ISO/SAE 21434 / GB 44495) adds threat-focused analysis and security controls
  — it is concerned with intentional attacks rather than random failures
- SOTIF (ISO 21448 / GB/T 43267) adds performance-focused analysis — it is concerned with
  limitations of the intended functionality rather than failures

OEMs should develop integrated safety/security concepts that address all three domains
simultaneously, avoiding siloed approaches that miss interactions between them.

^[raw/papers/FuSa_29_GB+T_34590-1-2022.md] ^[raw/papers/CS_1_6_ISO+SAE_21434-2021.md] ^[raw/papers/FuSa_6_GB+T_43267-2023.md]

## Cross-References

- [[functional-safety-framework]] — Full FuSa concept
- [[vehicle-cybersecurity-framework]] — Full cybersecurity concept
- [[gb-t-43253-series]] — FuSa audit methods
- [[functional-safety-overview]] — Landscape overview 2026 Q2
- [[cybersecurity-standards-comparison]] — Detailed GB 44495 vs ISO/SAE 21434 vs UN R155 comparison
