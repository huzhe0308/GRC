---
title: GB 17675 汽车转向系基本要求
created: 2026-08-06
updated: 2026-08-06
type: entity
tags: [steering, gb-standard, requirement, functional-safety, test-method, procedure]
sources: ['raw/papers/FuSa_16_GB+17675-2021.md', 'raw/papers/FuSa_17_GB+17675-2025.md', 'raw/transcripts/EX_02_征求意见_GB+17675-2021《汽车转向系+基本要求》附录B+功能安全要求合规性总结文档.md']
confidence: high
---

# GB 17675 汽车转向系基本要求

## Overview

GB 17675 is a Chinese mandatory national standard specifying basic requirements for motor vehicle steering systems (汽车转向系基本要求). The 2021 version (GB 17675-2021) replaces the 1999 version and was technically developed with reference to UN Regulation No. 79 (Rev. 4). A 2025 revision (GB 17675-2025) is also available as an image-only PDF. The standard covers steering system terminology, technical requirements for vehicles and trailers, failure provisions, warning signals, test methods, and functional safety requirements (Appendix B). It introduces functional safety requirements for steering electronic control systems such as EPS and ARS, aligning with GB/T 34590 (ISO 26262 equivalent).

## Key Facts

| Field | GB 17675-2021 | GB 17675-2025 |
|-------|---------------|---------------|
| Full Title (CN) | 汽车转向系 基本要求 | 汽车转向系 基本要求 |
| Full Title (EN) | Steering system of motor vehicles — Basic requirements | — |
| ICS | 43.040 | 43.040 |
| CCS | T23 | T23 |
| Published Date | 2021-02-20 | 2025 |
| Effective Date | 2022-01-01 | — |
| Supersedes | GB 17675-1999 | GB 17675-2021 |
| Issuing Body | 国家市场监督管理总局、国家标准化管理委员会 (SAMR/SAC) | SAMR/SAC |
| Proposed by | 中华人民共和国工业和信息化部 (MIIT) | — |
| Applicable Categories | M, N, O (per GB/T 15089) | M, N, O |
| Technical Reference | UN R79 (Rev. 4) | — |
| Source Format | Full text extractable | Image-only PDF |

## Scope and Requirements (GB 17675-2021)

- **Scope (Clause 1):** Applies to M, N category vehicles and O category trailers per GB/T 15089. Does NOT apply to pneumatic steering transmission systems or vehicles with autonomous steering systems (3.1.1.5).
- **Key Changes from 1999:** Removed left-hand steering wheel requirement; removed prohibition on full-power steering; added EMC requirements (4.1.5); added functional safety requirements for steering electronic control systems (4.1.9, Appendix B); added comprehensive trailer requirements.
- **Steering System Types (3.1.3):** Manual steering (人力转向), power-assisted steering (助力转向), full-power steering (全动力转向), self-tracking steering (随动转向), auxiliary steering equipment (ASE, 辅助转向装置).
- **Vehicle Requirements (4.1):** Steering system must ensure ease and safety of steering within maximum design speed range. Table 1 specifies steering control force, time, and turning radius limits.
- **Trailer Requirements (4.2):** Tractor-trailer alignment during straight driving; semi-trailer steered wheels; turning circle requirements; swing value (外摆值) ≤0.5 m when leaving 25 m radius turning circle at 25 km/h.
- **Failure Provisions (4.3):** If any non-mechanical transmission failure occurs, must warn driver per 4.4. Table 2 specifies post-failure steering control force limits. Single-fault assumption: only one fault assumed at any time.
- **Full-Power Steering Failure (4.3.3):** Vehicle speed limited to ≤10 km/h after main steering system fault. Energy storage must support at least 24 figure-8 turns at 10 km/h with 20 m radius when power source fails.
- **Warning Signals (4.4):** Red warning = main steering system fault (4.3.1.4); Yellow warning = electrical self-test defect not meeting red threshold. Warning symbol per ISO 2575:2010 J04 (ISO 7000-2441). Auditory warnings must include Chinese voice if voice messages used.
- **Test Methods (Clause 5):** Tests on horizontal road with good adhesion. Vehicle loaded to max design mass. Tests include: abnormal vibration when leaving 50 m circle (M1: 50 km/h; others: 40 km/h), understeer test, steering control force measurement (10 km/h entering turn), fault condition force measurement.
- **Appendix A (normative):** Supplementary provisions for vehicles with Auxiliary Steering Equipment (ASE). ASE test at specified speeds (M1: 80 km/h @ R=100 m; M2/M3: 45–50 km/h @ R=50 m; N1: 80 km/h @ R=100 m; N2/N3: 45–50 km/h @ R=50 m).
- **Appendix B (normative):** Functional safety requirements for steering electronic control systems per GB/T 34590 (all parts). Requires hazard analysis and risk assessment (HARA), safety goals, ASIL classification, safety analysis (FMEA/FTA), and verification/confirmation.
- **Appendix C (normative):** Hydraulic steering transmission trailer requirements. Min burst pressure ≥4× max working pressure. Pressure relief valve at 1.1–2.2× working pressure.
- **Appendix D (normative):** Special requirements for tractor-trailer steering system power supply (electrical).
- **Implementation (Clause 6):** New type approvals from effective date; existing approved types from 13th month after implementation.

## Functional Safety Compliance (Appendix B)

- **Scope:** Applies to passenger car steering electronic control systems (EPS, ARS) and interacting systems (ADAS, LKA, APA).
- **Table B.1 Hazards and ASIL Levels:**
  - Hazard 1: Unintended lateral movement (非预期的侧向运动) — **ASIL D** — Safety goal: meet unintended lateral movement safety metric
  - Hazard 2: Unintended loss of lateral movement control (非预期地失去侧向运动控制) — **ASIL D** — Safety goal: ensure driver control capability, steering force meets safety metric
  - Hazard 3: Heavy steering after power assistance loss (失去助力情况下的转向沉重) — **ASIL QM or A** — Safety goal: steering force meets heavy steering safety metric
- **Safety Analysis Requirements (B.2.6):** ASIL A+ requires inductive analysis (FMEA, ETA, Markov); ASIL C/D requires both inductive and deductive analysis (FTA, RBD) plus quantitative analysis (SPFM, LFM, PMHF per GB/T 34590.5).
- **Verification Testing:** Two typical scenarios: straight-line (60 km/h, 3.5 m lane width) and turning (25 km/h, 3.5 m lane, 35 m radius). Fault injection via special test interface. Measures: lateral acceleration, steering wheel torque.
- **Example Safety Metrics (from EX_02 transcript):** Unintended lateral movement PMHF: 1.1×10⁻⁸; Loss of steering control: SPF DC 99.75%, LF DC 90.82%, PMHF 0.9×10⁻⁸.

## Technical Details

| Parameter | M1 | M2 | M3 | N1 | N2 | N3 |
|-----------|-----|-----|-----|-----|-----|-----|
| Steering force (normal) | ≤150 N | ≤150 N | ≤200 N | ≤200 N | ≤250 N | ≤200 N |
| Steering time (normal) | ≤4 s | ≤4 s | ≤4 s | ≤4 s | ≤4 s | ≤4 s |
| Turning radius (normal) | 12 m | 12 m | 12 m | 12 m | 12 m | 12 m |
| Steering force (fault) | ≤300 N | ≤300 N | ≤450 N | ≤300 N | ≤400 N | ≤450 N |
| Steering time (fault) | ≤4 s | ≤4 s | ≤6 s | ≤4 s | ≤4 s | ≤6 s |
| Turning radius (fault) | 20 m | 20 m | 20 m | 20 m | 20 m | 20 m |

| Parameter | Value |
|-----------|-------|
| Full-power steering fault speed limit | ≤10 km/h |
| Figure-8 turns (power source failure) | ≥24 turns at 10 km/h, R=20 m |
| Figure-8 turns (energy transmission failure) | ≥25 turns at 10 km/h, R=20 m |
| Trailer swing value (外摆值) | ≤0.5 m |
| Steering circle radius (trailer test) | 25 m |
| Trailer test speeds | (25±1) km/h and 5 km/h |
| Abnormal vibration test (M1) | 50 km/h, R=50 m |
| Hydraulic burst pressure | ≥4× max working pressure |
| Pressure relief valve range | 1.1–2.2× working pressure |
| Signal filtering threshold | <0.2 s signals ignored |

^[raw/papers/FuSa_16_GB+17675-2021.md]
^[raw/transcripts/EX_02_征求意见_GB+17675-2021《汽车转向系+基本要求》附录B+功能安全要求合规性总结文档.md]

## Source Documents

- [FuSa_16_GB+17675-2021.md](raw/papers/FuSa_16_GB+17675-2021.md) — full text, 664 lines
- [FuSa_17_GB+17675-2025.md](raw/papers/FuSa_17_GB+17675-2025.md) — image-only PDF (binary)
- [EX_02 transcript](raw/transcripts/EX_02_征求意见_GB+17675-2021《汽车转向系+基本要求》附录B+功能安全要求合规性总结文档.md) — compliance summary template

## Cross-References

- [[gb-21670-braking]]
- [[gb-12676-braking]]
- [[gb-t-34590-series]]
- [[gb-t-39086-2020]]
- [[fusa-wd-drafts]]
