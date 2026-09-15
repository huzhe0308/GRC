---
title: Internal Security Concept Catalog & Specifications
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [cybersecurity, internal-spec, requirement, procedure, diagnostic-security, data-security]
sources: ['raw/papers/REQ_03_Security_Concept_Catalog.md', 'raw/papers/REQ_04_LAH_080_VCS_002_02_Secure_Storage_Spec.md', 'raw/papers/REQ_05_010_VCS_001_01_Data_Security_Requirements.md']
confidence: high
---

# Internal Security Concept Catalog & Specifications

## Overview

This entity encompasses CEA internal cybersecurity specifications covering the Security Concept Catalog, Secure Storage Specification, and Data Security Requirements. These documents define the security architecture framework, secure storage mechanisms for cryptographic keys and sensitive data, and vehicle data privacy protection requirements for the CEA2.X platform. Together they form the internal cybersecurity baseline for vehicle development, covering diagnostic interface protection, debug interface locking, secure storage with HSM/TEE support, and personal information protection compliant with China's PIPL. ^[raw/papers/REQ_03_Security_Concept_Catalog.md] ^[raw/papers/REQ_04_LAH_080_VCS_002_02_Secure_Storage_Spec.md] ^[raw/papers/REQ_05_010_VCS_001_01_Data_Security_Requirements.md]

## Key Facts

| Field | Value |
|-------|-------|
| Document Set | Security Concept Catalog (v0.04), Secure Storage Spec (V02.3), Data Security Requirements |
| Platform | CEA2.X |
| Issuing Organization | CEA (Volkswagen/JAC joint venture) |
| Catalog Version | 0.04 (2026-Jan-16) |
| Secure Storage Version | V02.3 (2025-09-09) |
| Key Authors | Guo Yalao, Kunze Kai, Huang Si (黄偲), Gong Lei (龚磊) |
| Applicable Scope | CEA2.X platform vehicle models |
| Regulatory References | China PIPL Article 29, GB/T 35273-2020, ISO 14229 (UDS) |

## Scope and Requirements

### Security Concept Catalog (REQ_03)
- **Framework**: Security Architecture Framework consists of three components: Security Concept Catalog, E/E-Architecture Security Analysis, and Security Architecture
- **Diagnostic Interface Protection**: Prevents unauthorized ECU access via external diagnostic tools; implemented per ISO 14229 (UDS Service $27/$29); uses challenge-response authentication based on symmetric/asymmetric cryptography; server controls client access permissions
- **Debugging Interface Protection**: Locks debug interfaces (JTAG, SWD, UART, XCP, BDM, Nexus, SSH, ADB) post-production; requires cryptographic authentication if access retained for maintenance
- **Secure Storage**: Protects stored data, keys, and certificates from tampering and unauthorized disclosure using hardware-protected or cryptography-protected storage spaces
- **Secure Boot**: Ensures only authenticated software executes during vehicle startup
- **Secured Flashing**: Validates software update packages before installation

### Secure Storage Specification (REQ_04)
- **Scope**: Covers key secure storage (symmetric keys, asymmetric private keys) and data secure storage (confidentiality and/or authenticity protection)
- **Key Storage**: Critical keys must be stored in hardware-supported secure storage areas (e.g., HSM); keys require confidentiality and integrity protection
- **Implementation Options**: Supports HSM-based, TEE-based, e.MMC-based, and cryptography-protected external storage approaches
- **Access Control**: Requires identity authentication for subjects accessing secure storage; supports MAC (Mandatory Access Control) or RBAC (Role-Based Access Control)
- **Document Delivery**: ECU suppliers must provide secure storage documentation, test reports, and performance metrics; deviations must be documented and approved

### Data Security Requirements (REQ_05)
- **Product Goal**: Establish clear, compliant, efficient personal information protection processes for in-vehicle systems, ensuring user data security and right to know
- **Privacy Framework**: Covers general personal information protection (privacy policies) and sensitive personal information protection (separate authorization for in-car video, audio, vehicle location, and web browsing history)
- **Regulatory Compliance**: References China's Personal Information Protection Law (PIPL) Article 29 (separate consent for sensitive information) and GB/T 35273-2020 (personal information security specification)
- **User Pain Points**: Addresses complex authorization flows, unclear permission boundaries, and weak compliance awareness through streamlined one-stop authorization, transparent permissions, and embedded compliance prompts

## Technical Details

- UDS diagnostic security: Service **$27** (SecurityAccess) and Service **$29** (Authentication) per ISO 14229
- Debug interfaces locked: JTAG, SWD, UART, XCP, BDM, Nexus, SSH, ADB
- Secure storage options: HSM, TEE (Trusted Execution Environment per GB/T 41388-2022), e.MMC, crypto-protected external
- Access control models: MAC and RBAC
- PIPL Article 29: Separate consent required for sensitive personal information
- GB/T 35273-2020: Personal information security specification
- Challenge-response authentication using symmetric/asymmetric cryptography for diagnostic access

## Source Documents

- [REQ_03_Security_Concept_Catalog.md](raw/papers/REQ_03_Security_Concept_Catalog.md)
- [REQ_04_LAH_080_VCS_002_02_Secure_Storage_Spec.md](raw/papers/REQ_04_LAH_080_VCS_002_02_Secure_Storage_Spec.md)
- [REQ_05_010_VCS_001_01_Data_Security_Requirements.md](raw/papers/REQ_05_010_VCS_001_01_Data_Security_Requirements.md)

## Cross-References

- [[iso-sae-21434-2021]]
- [[gb-44495-2024]]
- [[gb-t-44464-2024]]
- [[gb-t-47341-2026]]
