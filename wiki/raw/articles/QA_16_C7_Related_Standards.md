---
source_url: ""
ingested: 2026-08-06
sha256: c278ff8e6a54db6de657c518554d1fb94bf6f840b1ad91f76159323b3587079a
---

# QA_16_C7_Related_Standards


Related Standards for China 7 (C7) Emission Regulation - GB 18352.7


Source: Analysis of all 13 documents in 00.Emission_Regulation directory


This document lists all GB, GB/T, ISO, SAE, EU, and UN standards referenced by the C7 emission regulation.


C7 introduces fundamental changes including: SAE J1979-2 (UDS) for OBD, BEV OBD (SAE J1979-3), remote data upload (RDU), anti-tampering protection, and brake particle emissions.


1.  GB / GB/T Standards (China)


| Standard | Title / Reference | Used In |
| GB 18352.6-2016 | Limits and measurement methods for emissions from light-duty vehicles (CHINA 6) | Annex G, J.6.4.3.1 - OBD interface, REESS monitoring, PVE references |
| GB/T 32694 | Plug-in hybrid electric vehicles - Test methods for fuel consumption and electric range | Annex G - OVC-HEV SOCE verification trigger conditions |
| GB/T 34598 | Plug-in hybrid electric vehicles - Technical conditions | Annex G - OVC-HEV SOCE verification trigger conditions |
| GB/T 19753 | Testing methods for emissions from hybrid electric vehicles | Annex G - OVC-HEV GE.1 formula for BER calculation |
| GB/T 42193.2 | Road vehicles - Diagnostics on controller networks - Part 2: Transport protocol and network layer services | J.3.1.5.3 - Replaces SAE references for OBD documentation in C7 |
| GB/T 22239-2019 | Information security technology - Cybersecurity level protection (Level III+ required) | JD.1.2, JD.7 - RDU enterprise platform cybersecurity requirement |
| HJ 509-2009 | Measurement methods for catalyst carrier and precious metal content of vehicle exhaust gas purification devices | Annex G - Catalyst carrier/precious metal CoP requirements |
| HJ RDE Technical Specification | Technical specification for real driving emissions measurement of light-duty vehicles | Annex D (Type II RDE) - PEMS, boundary conditions, trip validity, emission calculation |
| HJ 1014-2021 | Technical specification for non-road mobile machinery emissions (turbo/supercharger reference) | Annex G - Turbo/supercharger reference for bench aging methodology |


2.  ISO Standards


| Standard | Title / Reference | Used In |
| ISO 13400-2:2019 | Road vehicles - Diagnostics on CAN - Part 2: Transport protocol and network layer services [NEW in C7] | J.6.1.12 - Communication protocol for non-OBD diagnostic data reading |
| ISO 13400-3:2019 | Road vehicles - Diagnostics on CAN - Part 3: Implementation of diagnostic communication [NEW in C7] | J.6.1.13 - Communication protocol for non-OBD diagnostic data reading |
| ISO 13400-4:2019 | Road vehicles - Diagnostics on CAN - Part 4: Requirements for USD and OBD compliance [NEW in C7] | J.6.1.14 - ZEV-specific DoIP diagnostic protocol |
| ISO 15765-4:2011 | Road vehicles - Diagnostics on CAN - Part 4: Requirements for fuel-related and evaporative emission-related systems | J.6.4.2.3 - Data stream contents for vehicles using DoCAN protocol |
| ISO 27145-4:2012 | Road vehicles - Diagnostics communication - Part 4: Requirements for USD and OBD compliance | J.6.1.15 - Per C7 comments: not relevant to OBD |


3.  SAE Standards (USA)


| Standard | Title / Reference | Used In |
| SAE J1699-3:2016 | Vehicle OBD II Compliance Test Cases | Annex G, J.4.14.4.2, JA.7.1, JA.7.3.4.2 - PVE test specs, END MIL no-illumination logic |
| SAE J1699-5:2021 | Electric Vehicle OBD II Compliance Test Cases [NEW in C7] | J.6.1.9, JC.5.3, JC.5.4 - BEV PVE communication testing, standardization verification |
| SAE J1979-2:2021 | Diagnostic Test Modes - OBD on UDS (Unified Diagnostic Services) [FUNDAMENTAL - replaces classic J1979] | J.3.5.7, J.6.1.4, J.6.3.1, J.6.3.3, J.6.3.4, J.6.4.1, J.6.4.3.1 - Core OBD communication for ICE/xHEV |
| SAE J1979-3:2021 | Diagnostic Test Modes - ZEV on UDS [NEW in C7] | J.6.1.4, JC.3.2, JC.3.3.1, JC.3.3.3, JC.3.3.4 - BEV/FCV OBD communication |
| SAE J1979-DA:2021 | Digital Annex - Extended data access for OBD | J.6.1.4, JC.3.3.1, JC.3.3.4, JD.9.2-JD.9.8 - RDU data format, BEV data stream |
| SAE J2841:2010 | Utility Factor Definitions for Plug-In Hybrid Electric Vehicles | Annex CG - OVC-HEV utility factor curve methodology |
| SAE J1939-1 to J1939-13 series | SAE recommended practice for in-vehicle CAN bus communication | Implied for comprehensive component monitoring (J.4.14) and OBD system communication |


4.  EU / UN / GTR Standards


| Standard | Title / Reference | Used In |
| EU 2014/45/EU | Directive on periodic roadworthiness tests on motor vehicles and their trailers | aktiv_EU7 - Warning light/HMI requirements for anti-tampering display concept |
| EU7 Implementing Act ANNEX XIV | EU7 Anti-tampering impact level thresholds (NOx/PM greater than 2.5x limit) | aktiv_EU7 - Impact Level 3 threshold (Security Level Critical), EEEDWS Bit 6 trigger |
| UN-R 154 Series 2, Level 1A | Regulation No. 154 - On-board diagnostic (OBD) compliance for RDE | aktiv_EU7 - OBD limits and functional requirements reference |
| UN-R 39 | Regulation No. 39 - Speedometer and odometer equipment | aktiv_EU7 - Odometer anti-tampering protection (Impact Level 2) |
| GTR 24 (UN/G/R/24) | Global Technical Regulation No. 24 - Electric vehicle safety and environmental requirements | Annex K - C-Factor reference for brake emission testing |


5.  Summary by Category


| Category | Count | Key Standards |
| GB / GB/T / HJ (China) | 9+ | GB 18352.6, GB/T 32694, GB/T 34598, GB/T 19753, GB/T 42193.2, GB/T 22239, HJ 509, HJ RDE Spec, HJ 1014 |
| ISO (International) | 5 | ISO 13400-2/3/4, ISO 15765-4, ISO 27145-4 |
| SAE (USA) | 7+ | J1699-3/5, J1979-2/3/DA, J2841, J1939 series |
| EU / UN / GTR | 5 | EU 2014/45, EU7 Annex XIV, UN-R 154, UN-R 39, GTR 24 |
| TOTAL | ~26 | All above combined across all C7 requirements |


6.  Critical New Standards in C7 (Not Present in C6b)


| Standard | Significance | Impact on C7 |
| SAE J1979-2 (UDS on UDS) | Replaces classic SAE J1979 OBD protocol with Unified Diagnostic Services | FUNDAMENTAL - All OBD communication for ICE/xHEV migrates to UDS. New DTC structures, snapshot, FGID/RGID, NRC responses |
| SAE J1979-3 (ZEV on UDS) | ZEV/FCV OBD communication via UDS | NEW - First time BEV has a standardized OBD protocol. SAE J1979-DA defines data format |
| SAE J1699-5 (EV OBD) | Electric Vehicle OBD II Compliance Test Cases | NEW - BEV PVE and standardization verification requirements, communication protocol testing |
| ISO 13400-2/3/4 (DoIP) | Diagnostic communication over Internet Protocol | NEW - Expands diagnostics beyond OBD to cover full vehicle non-OBD data. VCTC: DoIP not required for BEV |
| GB/T 42193.2 | Replaces SAE references in Chinese OBD documentation context | NEW in C7 Chinese regulatory context - National standard defining diagnostic transport protocol |
| GB/T 22239 (Cybersecurity) | Cybersecurity Level Protection (Level III+) | NEW - Mandatory for RDU enterprise platform. All vehicle-to-platform data transmission must meet Level III+ |
| UN-R 39 (Odometer) | Odometer anti-tampering protection | NEW - Explicitly mandated in C7. Odometer manipulation is an Impact Level 2 security issue |
| GTR 24 (Brake) | Electric vehicle safety and brake emission C-Factor | NEW - First time brake particle emissions are regulated in China |


7.  Cross-Reference Matrix - C7 Requirement vs. Standards


| C7 Requirement Area | Related Standards |
| Type I - Exhaust Cold Start (Annex C) | SAE J1979-2, GB/T 19753, ISO 15765-4, HJ RDE Technical Specification |
| Type II - RDE (Annex D) | HJ RDE Technical Specification, UN-R 154 Series 2, ISO 15765-4 |
| Type III - Crankcase (Annex D) | ISO 15765-4, SAE J1979-2 |
| Type IV - EVAP (Annex F) | ISO 15765-4, SAE J1979-2 |
| Type V - Durability (Annex G) | GB 18352.6, GB/T 32694, GB/T 34598, GB/T 19753, SAE J1699-3, HJ 509 |
| Type VI - Extended Temperature (Annex H) | ISO 15765-4, SAE J1979-2 |
| Type VII - Refueling (Annex I) | ISO 15765-4, SAE J1979-2 |
| Type VIII - Brake (Annex K) | GTR 24 |
| OBD - ICE/xHEV (Annex J) | SAE J1979-2, SAE J1699-3, ISO 13400-2/3/4, ISO 15765-4, GB/T 42193.2, GB 18352.6 |
| OBD - BEV (Annex JC) | SAE J1979-3, SAE J1699-5, ISO 13400-4, ISO 15765-4 |
| RDU / Remote Data Upload (Annex JD) | GB/T 22239 (Level III+), SAE J1979-2, SAE J1979-3, SAE J1979-DA |
| Anti-Tampering (aktiv_EU7) | UN-R 39, EU 2014/45, EU7 Implementing Act ANNEX XIV |
| OBD Documentation / Homologation | GB/T 42193.2, SAE J1979-2, SAE J1979-3, GB 18352.6 |
| PVE - ICE/xHEV | SAE J1699-3, GB 18352.6, GB/T 42193.2 |
| PVE - BEV | SAE J1699-5, SAE J1979-3, GB 18352.6 |
| Cybersecurity (RDU Platform) | GB/T 22239 |
| Fleet Management (Annex Q) | GB/T 19753 (CO2e), HJ RDE Technical Specification |
| All Test Types (General Reference) | GB 18352.6, ISO 15765-4 |


8.  Complete Alphabetical Reference List


| No. | Standard | Type |
| 1 | EU 2014/45/EU | EU Directive |
| 2 | EU7 Implementing Act ANNEX XIV | EU Regulation |
| 3 | GTR 24 (UN/G/R/24) | GTR |
| 4 | GB 18352.6-2016 | GB |
| 5 | GB/T 19753 | GB/T |
| 6 | GB/T 22239-2019 | GB/T |
| 7 | GB/T 32694 | GB/T |
| 8 | GB/T 34598 | GB/T |
| 9 | GB/T 42193.2 | GB/T |
| 10 | HJ 1014-2021 | HJ |
| 11 | HJ 509-2009 | HJ |
| 12 | HJ RDE Technical Specification | HJ |
| 13 | ISO 13400-2:2019 | ISO |
| 14 | ISO 13400-3:2019 | ISO |
| 15 | ISO 13400-4:2019 | ISO |
| 16 | ISO 15765-4:2011 | ISO |
| 17 | ISO 27145-4:2012 | ISO |
| 18 | SAE J1699-3:2016 | SAE |
| 19 | SAE J1699-5:2021 | SAE |
| 20 | SAE J1939 series | SAE |
| 21 | SAE J1979-2:2021 | SAE |
| 22 | SAE J1979-3:2021 | SAE |
| 23 | SAE J1979-DA:2021 | SAE |
| 24 | SAE J2841:2010 | SAE |
| 25 | UN-R 154 Series 2 Level 1A | UN Regulation |
| 26 | UN-R 39 | UN Regulation |

