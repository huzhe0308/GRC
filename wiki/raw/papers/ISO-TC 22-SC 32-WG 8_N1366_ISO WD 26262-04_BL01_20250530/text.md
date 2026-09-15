<!-- Page 1 -->

ISO/TC 22/SC 32/WG 8 N 1366ISO/TC 22/SC 32/WG 8 "Functional safety"Convenorship: DINConvenor: Knapp Andreas Mr Dipl.-Ing.
 
ISO WD 26262-04_BL01_20250530Document typeRelated contentDocument date Expected actionGeneral / Other2025-05-31
COMMENT/REPLY by2025-07-28DescriptionISO WD 26262_BL01 – Commenting cycle for 1st WD
ISO TC22/SC32/WG08 decided to run the first WD commenting cycle under the following conditions:
-Duration: starting 2025-05-31 / ending 2025-07-28 (midnight GMT).
-Project is on OSD, but commenting will be provided as for BL0 using the XLS commenting sheet. 
-Comments shall be send via e-mail before the deadline (2025-07-28) by e-mail to 
egbert.fritzsche@vda.de and andreas.knapp@mercedes-benz.com and to the relevant PL.
-The comment sheet is available CC-CommentsOnISO26262-XX-BL01_general - Documents (Policiy
for file naming: “CC” to be replaced by country short cut / “XX” to be replaced by Part No / “general” to
be used for General comments for clauses 1 to 4 / “general” for technical comments to be deleted). 
Guidance for commenting is provided InstructionUsageCommentsSheet - Documents
-Only one commenting sheet per participating nation is accepted, first provided file is valid.
-Commenting shall be based on the distributed PDF documents with line numbers, but in case of 
ambiguities, the document in OSD shall be taken as “master document” for formulating comments
-All experts registered as members of ISO TC22/SC32/WG08 (having access in ISO.DOCs) are 
obliged to vote. Only the central contact expert for the country shall vote with “yes” (in case that 
comments will be send via e-mail), all others are kindly requested to vote “no”.
-Please refrain from sending editorial comments at this commenting circle.
-In case of questions for the procedure please contact: egbert.fritzsche@vda.de 


<!-- Page 2 -->

ISO/AWI 26262-4(en)Third edition
 
Date: 2025-05-30Road vehicles — Functional safety —Part 4:Product development at the system levelVéhicules routiers — Sécurité fonctionnelle —Partie 4: Développement du produit au niveau du système


<!-- Page 3 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved© ISO 2025
1 
All rights reserved. Unless otherwise specified, or required in the context of its implementation, no part of this publication 
2 
may be reproduced or utilized otherwise in any form or by any means, electronic or mechanical, including photocopying, 
3 
or posting on the internet or an intranet, without prior written permission. Permission can be requested from either ISO 
4 
at the address below or ISO’s member body in the country of the requester. 
5 
ISO copyright office
6 
CP 401 • Ch. de Blandonnet 8
7 
CH-1214 Vernier, Geneva
8 
Phone: + 41 22 749 01 11
9 
E-mail: copyright@iso.org
10 
Website: www.iso.org
11 
Published in Switzerland
12 
 
 
13 


<!-- Page 4 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
14 
Foreword ...................................................................................................... Fehler! Textmarke nicht definiert. 
15 
Introduction ................................................................................................ Fehler! Textmarke nicht definiert. 
16 
 
Scope ..................................................................................................... Fehler! Textmarke nicht definiert. 
17 
 
Normative references ..................................................................... Fehler! Textmarke nicht definiert. 
18 
 
Terms and definitions ..................................................................... Fehler! Textmarke nicht definiert. 
19 
 
Requirements for compliance ..................................................... Fehler! Textmarke nicht definiert. 
20 
 
Purpose ................................................................................................ Fehler! Textmarke nicht definiert. 
21 
 
General requirements .................................................................... Fehler! Textmarke nicht definiert. 
22 
 
Interpretations of tables ................................................................ Fehler! Textmarke nicht definiert. 
23 
 
ASIL-dependent requirements and recommendations ...... Fehler! Textmarke nicht definiert. 
24 
 
Adaptation for motorcycles .......................................................... Fehler! Textmarke nicht definiert. 
25 
 
Adaptation for trucks, buses, trailers and semi-trailers .... Fehler! Textmarke nicht definiert. 
26 
 
General topics for the product development at the system level ..... Fehler! Textmarke nicht 
27 
definiert.
28 
 
Objectives ............................................................................................ Fehler! Textmarke nicht definiert. 
29 
 
General ................................................................................................. Fehler! Textmarke nicht definiert. 
30 
 
Functional safety concept on system level .............................. Fehler! Textmarke nicht definiert. 
31 
 
Objectives ............................................................................................ Fehler! Textmarke nicht definiert. 
32 
 
General ................................................................................................. Fehler! Textmarke nicht definiert. 
33 
 
Inputs to this clause ......................................................................... Fehler! Textmarke nicht definiert. 
34 
 
Requirements and recommendations ...................................... Fehler! Textmarke nicht definiert. 
35 
 
Work products ................................................................................... Fehler! Textmarke nicht definiert. 
36 
 
System integration and testing .................................................... Fehler! Textmarke nicht definiert. 
37 
 
Objectives ............................................................................................ Fehler! Textmarke nicht definiert. 
38 
 
General ................................................................................................. Fehler! Textmarke nicht definiert. 
39 
 
Inputs to this clause ......................................................................... Fehler! Textmarke nicht definiert. 
40 
 
Requirements and recommendations ...................................... Fehler! Textmarke nicht definiert. 
41 
 
Work products ................................................................................... Fehler! Textmarke nicht definiert. 
42 
(informative) Overview of and workflow of product development at the system level ... Fehler! 
43 
Textmarke nicht definiert.
44 
(informative) Example contents of hardware-software interface (HSI) . Fehler! Textmarke nicht 
45 
definiert.
46 
Bibliography ............................................................................................... Fehler! Textmarke nicht definiert. 
47 
 
48 


<!-- Page 5 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
49 
ISO (the International Organization for Standardization) is a worldwide federation of national standards 
50 
bodies (ISO member bodies). The work of preparing International Standards is normally carried out through 
51 
ISO technical committees. Each member body interested in a subject for which a technical committee has been 
52 
established has the right to be represented on that committee. International organizations, governmental and 
53 
non-governmental, in liaison with ISO, also take part in the work. ISO collaborates closely with the 
54 
International Electrotechnical Commission (IEC) on all matters of electrotechnical standardization. 
55 
The procedures used to develop this document and those intended for its further maintenance are described 
56 
in the ISO/IEC Directives, Part 1. In particular, the different approval criteria needed for the different types of 
57 
ISO documents should be noted. This document was drafted in accordance with the editorial rules of the 
58 
ISO/IEC Directives, Part 2 (see www.iso.org/directives). 
59 
Attention is drawn to the possibility that some of the elements of this document may be the subject of patent 
60 
rights. ISO shall not be held responsible for identifying any or all such patent rights. Details of any patent rights 
61 
identified during the development of the document will be in the Introduction and/or on the ISO list of patent 
62 
declarations received (see www.iso.org/patents). 
63 
Any trade name used in this document is information given for the convenience of users and does not 
64 
constitute an endorsement.
65 
For an explanation on the voluntary nature of standards, the meaning of ISO specific terms and expressions 
66 
related to conformity assessment, as well as information about ISO's adherence to the World Trade 
67 
Organization (WTO) principles in the Technical Barriers to Trade (TBT) see the following URL: 
68 
www.iso.org/iso/foreword.html.
69 
This document was prepared by Technical Committee ISO/TC 22, Road vehicles Subcommittee, SC 32, 
70 
Electrical and electronic components and general system aspects. 
71 
This edition of ISO 26262 series of standards cancels and replaces the edition ISO 26262:2011 series of 
72 
standards, which has been technically revised and includes the following main changes: 
73 
— extensions to address the nominal performance of E/E systems including safety of the intended 
74 
functionality considerations;
75 
— requirements for trucks, buses, trailers and semi-trailers; 
76 
— extension of the vocabulary;
77 
— more detailed objectives;
78 
— objective oriented confirmation measures; 
79 
— management of safety anomalies;
80 
— references to cyber security;
81 
— updated target values for hardware architecture metrics; 
82 
— guidance on model based development and software safety analysis; 
83 
— evaluation of hardware elements;
84 
— additional guidance on dependent failure analysis; 
85 


<!-- Page 6 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reservedv
— guidance on fault tolerance, safety related special characteristics and software tools; 
86 
— guidance for semiconductors;
87 
— requirements for motorcycles; and
88 
— general restructuring of all parts for improved clarity. 
89 
Any feedback or questions on this document should be directed to the user’s national standards body. A 
90 
complete listing of these bodies can be found at www.iso.org/members.html. 
91 
A list of all parts in the ISO 26262 series can be found on the ISO website. 
92 


<!-- Page 7 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reservedIntroduction
93 
The ISO 26262 series of standards is the adaptation of IEC 61508 series of standards to address the sector 
94 
specific needs of electrical and/or electronic (E/E) systems within road vehicles. 
95 
This adaptation applies to all activities during the safety lifecycle of safety-related systems that include 
96 
electrical, electronic and software components. 
97 
Safety is one of the key issues in the development of road vehicles. Development and integration of automotive 
98 
functionalities strengthen the need for functional safety and the need to provide evidence that functional 
99 
safety objectives are satisfied.
100 
With the trend of increasing technological complexity, software content and mechatronic implementation, 
101 
there are increasing risks from systematic failures and random hardware failures, these being considered 
102 
within the scope of functional safety. ISO 26262 series of standards includes guidance to mitigate these risks 
103 
by providing appropriate requirements, methods and processes. 
104 
To achieve functional safety, the ISO 26262 series of standards: 
105 
a) provides a reference for the automotive safety lifecycle and supports the tailoring of the activities to be 
106 
performed during the phases of the safety lifecycle, i.e., development, production, operation, service and 
107 
decommissioning;
108 
b) provides an automotive-specific risk-based approach to determine integrity levels [Automotive Safety 
109 
Integrity Levels (ASILs)];
110 
c) uses ASILs to specify which of the requirements of ISO 26262 are applicable to avoid unreasonable 
111 
residual risk;
112 
d) provides requirements for functional safety management, design, implementation, verification, validation 
113 
and confirmation measures; and
114 
e) provides requirements for relations between customers and suppliers. 
115 
The ISO 26262 series of standards is concerned with functional safety of E/E systems that is achieved through 
116 
safety measures including safety mechanisms. It also provides a framework within which safety-related 
117 
systems based on other technologies (e.g. mechanical, hydraulic and pneumatic) can be considered. 
118 
The achievement of functional safety is influenced by the development process (including such activities as 
119 
requirements specification, design, implementation, integration, verification, validation and configuration), 
120 
the production and service processes and the management processes. 
121 
Safety is intertwined with common function-oriented and quality-oriented activities and work products. The 
122 
ISO 26262 series of standards addresses the safety-related aspects of these activities and work products. 
123 
Functional safety assumes that the intended functionality is safe. To substantiate this assumption on the 
124 
applicable systems, the ISO 21448 standard can be used for the items in scope. The link with ISO 26262 series 
125 
of standards addressing the intended functionality can be considered (e.g. See Part 10, Clause 15 for the link 
126 
to [1]).
127 
Figure 1 shows the overall structure of the ISO 26262 series of standards. The ISO 26262 series of standards 
128 
is based upon a V-model as a reference process model for the different phases of product development. Within 
129 
the figure:
130 


<!-- Page 8 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
— the shaded “V”s represent the interconnection among ISO 26262-3, ISO 26262-4, ISO 26262-5, ISO 26262-
131 
6 and ISO 26262-7;
132 
— for motorcycles:
133 
— ISO 26262-12:2018, Clause 8 supports ISO 26262-3; 
134 
— ISO 26262-12:2018, Clauses 9 and 10 support ISO 26262-4;  
135 
— the specific clauses are indicated in the following manner: “m-n”, where “m” represents the number of the 
136 
particular part and “n” indicates the number of the clause within that part. 
137 
“2-6” represents ISO 26262-2:2018, Clause 6. 
138 
 
139 
Figure 1 — Overview of the ISO 26262 series of standards 
140 


<!-- Page 9 -->



<!-- Page 10 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
1 
Road vehicles — Functional safety —
141 
Part 4:
142 
Product development at the system level
143 
1 Scope
144 
This document is intended to be applied to safety-related systems that include one or more electrical and/or 
145 
electronic (E/E) systems and that are installed in series production road vehicles, excluding mopeds. This 
146 
document does not address unique E/E systems in special vehicles such as E/E systems designed for drivers 
147 
with disabilities.
148 
Other dedicated application-specific safety standards exist and can complement the ISO 26262 series of 
149 
standards or vice versa.
150 
Systems and their components released for production, or systems and their components already under 
151 
development prior to the publication date of this document, are exempted from the scope of this edition. This 
152 
document addresses alterations to existing systems and their components released for production prior to the 
153 
publication of this document by tailoring the safety lifecycle depending on the alteration. This document 
154 
addresses integration of existing systems not developed according to this document and systems developed 
155 
according to this document by tailoring the safety lifecycle. 
156 
This document addresses hazards to which malfunctioning behaviour of safety-related E/E systems can 
157 
contribute. This includes hazards directly caused by malfunctioning behaviour of safety-related E/E systems, 
158 
including interactions between these systems. This also includes hazards for which safety-related E/E systems 
159 
contribute to the prevention or control of their causes or mitigate their harmful effects. It can address hazards 
160 
related to electric shock, fire, smoke, heat, radiation, toxicity, flammability, reactivity, corrosion, release of 
161 
energy and similar hazards, only if
162 
— directly caused by malfunctioning behaviours of safety-related E/E systems, or 
163 
— safety-related E/E systems contribute to the prevention or control of their causes or mitigate their harmful 
164 
effects.
165 
This document describes a framework for functional safety to assist the development of safety-related E/E 
166 
systems. This framework is intended to be used to integrate functional safety activities into a company-specific 
167 
development framework. Some requirements have a clear technical focus to implement functional safety into 
168 
a product; others address the development process and can therefore be seen as process requirements in 
169 
order to demonstrate the capability of an organization with respect to functional safety. 
170 
This document specifies the requirements for product development at the system level for automotive 
171 
applications, including the following:
172 
— general topics for the initiation of product development at the system level; 
173 
— specification of the functional safety requirements on system level; 
174 
— the functional safety concept on system level; 
175 
— system architectural design;
176 
— item integration and testing; and
177 


<!-- Page 11 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
2 
— safety validation.
178 
Annex A provides an overview on objectives, prerequisites and work products of this document.  
179 
2 Normative references
180 
The following documents are referred to in the text in such a way that some or all of their content constitutes 
181 
requirements of this document. For dated references, only the edition cited applies. For undated references, 
182 
the latest edition of the referenced document (including any amendments) applies.  
183 
ISO 26262-1:2018, Road vehicles — Functional safety — Part 1: Vocabulary 
184 
ISO 26262-2:2018, Road vehicles — Functional safety — Part 2: Management of functional safety 
185 
ISO 26262-3:2018, Road vehicles — Functional safety — Part 3: Concept phase 
186 
ISO 26262-5:2018, Road vehicles — Functional safety — Part 5: Product development at the hardware level 
187 
ISO 26262-6:2018, Road vehicles — Functional safety — Part 6: Product development at the software level 
188 
ISO 26262-7:2018,vehicles — Functionalsafety — Part 7: Production,operation,
189 
decommissioning
190 
ISO 26262-8:2018, Road vehicles — Functional safety — Part 8: Supporting processes 
191 
ISO 26262-9:2018, Road vehicles — Functional safety — Part 9: Automotive Safety Integrity Level (ASIL)-
192 
oriented and safety-oriented analyses
193 
3 Terms and definitions
194 
For the purposes of this document, the terms, definitions and abbreviated terms given in ISO 26262-1:2018 
195 
apply.
196 
ISO and IEC maintain terminological databases for use in standardization at the following addresses: 
197 
— IEC Electropedia: available at http://www.electropedia.org/ 
198 
— ISO Online browsing platform: available at https://www.iso.org/obp 
199 
4 Requirements for compliance
200 
4.1 Purpose
201 
This clause describes how:
202 
a) to achieve compliance with the ISO 26262 series of standards; 
203 
b) to interpret the tables used in the ISO 26262 series of standards; and 
204 
c) to interpret the applicability of each clause, depending on the relevant ASIL(s). 
205 
4.2 General requirements
206 
When claiming compliance with the ISO 26262 series of standards, each requirement shall be met, unless one 
207 
of the following applies:
208 


<!-- Page 12 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
3 
a) tailoring of the safety activities in accordance with ISO 26262-2 has been performed that shows that the 
209 
requirement does not apply; or
210 
b) a rationale is available that the non-compliance is acceptable and the rationale has been evaluated in 
211 
accordance with ISO 26262-2.
212 
Informative content, including notes and examples, is only for guidance in understanding, or for clarification 
213 
of the associated requirement, and shall not be interpreted as a requirement itself or as complete or 
214 
exhaustive.
215 
The following clauses, organized by "objectives", contain sets of requirements for their achievement and the 
216 
expected results are given as "work products". "Prerequisites" are information which is required to fulfil the 
217 
requirements of a clause. Given that certain requirements of a clause are ASIL‑dependent or can be tailored, 
218 
certain work products may not be needed as prerequisites. 
219 
“Further supporting information” is information that can be considered, but which in some cases is not 
220 
required by the ISO 26262 series of standards as a work product to fulfill the requirements of a clause and 
221 
which may be made available by external sources that are different from the persons or organizations 
222 
responsible for the functional safety activities. 
223 
4.3 Interpretations of tables
224 
Tables are normative or informative depending on their context. The different methods listed in a table 
225 
contribute to the level of confidence in achieving compliance with the corresponding requirement. Each 
226 
method in a table is either:
227 
a) a consecutive entry (marked by a sequence number in the leftmost column, e.g. 1, 2, 3), or 
228 
b) an alternative entry (marked by a number followed by a letter in the leftmost column, e.g. 2a, 2b, 2c). 
229 
For consecutive entries, all listed highly recommended and recommended methods in accordance with the 
230 
ASIL apply. A highly recommended or recommended method may be substituted by others not listed in the 
231 
table, in this case, a rationale shall be given describing why these comply with the corresponding requirement. 
232 
If a rationale can be given to comply with the corresponding requirement without choosing all entries, a 
233 
further rationale for omitted methods is not necessary. 
234 
For alternative entries, an appropriate combination of methods shall be applied in accordance with the ASIL 
235 
indicated, independent of whether they are listed in the table or not. If methods are listed with different 
236 
degrees of recommendation for an ASIL, the methods with the higher recommendation should be preferred. 
237 
A rationale shall be given that the selected combination of methods or even a selected single method complies 
238 
with the corresponding requirement.
239 
A rationale based on the methods listed in the table is sufficient. However, this does not imply a bias for or 
240 
against methods not listed in the table. 
241 
For each method, the degree of recommendation to use the corresponding method depends on the ASIL and 
242 
is categorized as follows:
243 
— “++” indicates that the method is highly recommended for the identified ASIL; 
244 
— “+” indicates that the method is recommended for the identified ASIL; and 
245 
— “o” indicates that the method has no recommendation for or against its usage for the identified ASIL. 
246 


<!-- Page 13 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
4 
4.4 ASIL-dependent requirements and recommendations 
247 
The requirements or recommendations of each sub-clause shall be met for ASIL A, B, C and D, if not stated 
248 
otherwise. These requirements and recommendations refer to the ASIL of the safety goal. If ASIL 
249 
decomposition has been performed at an earlier stage of development, in accordance with ISO 26262-9:2018, 
250 
Clause 5, the ASIL resulting from the decomposition shall be met.  
251 
If an ASIL is given in parentheses in the ISO 26262 series of standards, the corresponding sub-clause shall be 
252 
considered as a recommendation rather than a requirement for this ASIL. This has no link with the parenthesis 
253 
notation related to ASIL decomposition.
254 
4.5 Adaptation for motorcycles
255 
For items or elements of motorcycles for which requirements of ISO 26262-12 are applicable, the 
256 
requirements of ISO 26262-12 supersede the corresponding requirements in this document. Requirements of 
257 
ISO 26262‑2 that are superseded by ISO 26262-12 are defined in Part 12. 
258 
4.6 Adaptation for trucks, buses, trailers and semi-trailers 
259 
Content that is intended to be unique for trucks, buses, trailers and semi-trailers (T&B) is indicated as such. 
260 
5 General topics for the product development at the system level 
261 
5.1 Objectives
262 
The objective of this clause is to provide an overview of product development at the system level. 
263 
5.2 General
264 
The necessary activities during the development of a system are given in Figure 2. In an iterative process, the 
265 
functional safety concept on system level is developed, incorporating functional safety requirements on 
266 
system level and the system architectural design. The system architecture is established, the functional safety 
267 
requirements are allocated to elements of the system, and, if applicable, on other technologies. In addition, the 
268 
functional safety requirements are refined and requirements arising from the system architecture are added, 
269 
including the hardware-software interface (HSI). Depending on the complexity of the architecture, the 
270 
requirements for subsystems can be derived iteratively. 
271 
The system architectural design, in addition to the functionality defined on item level, also relates to the 
272 
technology resources used to realise the functionality and the means used to distribute information or energy. 
273 
After their development, the hardware and software elements are integrated and tested to form a system. 
274 
This document applies to the development of systems. ISO 26262-5 and ISO 26262-6 describe the 
275 
development requirements for hardware and software, respectively. Figure 3 is an example of a system with 
276 
multiple levels of integration, illustrating the application of this document, ISO 26262-5 and ISO 26262-6. 
277 
NOTE 1
Table A.1 provides an overview of objectives, prerequisites and work products during product development 
278 
at the system level.
279 


<!-- Page 14 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
5 
 
280 
Figure 2 — Reference phase model for the development of a safety-related item 
281 
NOTE 2
Within the figures 2 and 3, the specific clauses of each part of ISO 26262 are indicated in the following manner: 
282 
“m-n”, where “m” represents the number of the part and “n” indicates the number of the clause, e.g. “4-6” represents 
283 
ISO 26262-4:2018, Clause 6.
284 
 
285 
Figure 3 — Example of a product development at the system level 
286 
NOTE 3
Further information regarding product development at the system level can be found in References 
287 
[ISO/IEC/IEEE 15288[2]] and [ISO/IEC/IEEE 16326[3]]. 
288 
6 Functional safety concept on system level 
289 
6.1 Objectives
290 
The objectives of this clause are:
291 
a) to specify functional safety requirements regarding the functionality, dependencies, constraints and 
292 
properties of the system elements and interfaces needed for their implementation; 
293 
b) to specify functional safety requirements regarding the safety mechanisms to be implemented in the 
294 
system elements and interfaces;
295 
c) to specify requirements regarding the functional safety of the system and its elements during production, 
296 
operation, service and decommissioning;
297 
d) to verify that the functional safety requirements on system level are suitable to achieve functional safety 
298 
at the system level and are consistent with the functional safety requirements on item level; 
299 


<!-- Page 15 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
6 
e) to develop a system architectural design and a functional safety concept on system level that satisfy the 
300 
functional safety requirements on item level and that are not in conflict with the non-safety-related 
301 
requirements;
302 
f)
to identify the necessary safety-related special characteristics for production and service; and 
303 
g) to verify that the system architectural design and the functional safety concept on system level are suitable 
304 
to satisfy the safety requirements according to their respective ASIL. 
305 
6.2 General
306 
The functional safety concept on system level is an aggregation of the functional safety requirements on 
307 
system level and the corresponding system architectural design that provides rationale as to why the system 
308 
architectural design is suitable to fulfil functional safety requirements on item level resulting from activities 
309 
described in ISO 26262-3 (with consideration of non-safety requirements) and design constraints. 
310 
The functional safety requirements on system level specify the technical implementation of the functional 
311 
safety requirements at their respective hierarchical level; considering both the item definition and the system 
312 
architectural design, and addressing the detection of latent failures, fault avoidance, safety integrity and 
313 
operation and service aspects.
314 
The system architectural design is the selected system-level solution that is implemented by a technical 
315 
system. The system architectural design aims to fulfil both, the allocated functional safety requirements and 
316 
the non-safety requirements.
317 
System development can be performed iteratively, i.e. functional safety requirements defined on system level 
318 
and assigned to elements of the system can be iteratively refined on sub-system levels. 
319 
6.3 Inputs to this clause
320 
6.3.1Prerequisites
321 
The following information shall be available: 
322 
— functional safety concept on item level in accordance with ISO 26262-3:2018, 7.5.1; 
323 
— system architectural design (from an external source); and 
324 
— requirements to the item from other safety relevant items if applicable. 
325 
Requirements from a park assist system to a brake system. 
326 
NOTE 1
In a distributed development, a functional safety concept can be based on another functional safety concept 
327 
realized by subsystems.
328 
NOTE 2
SOTIF measures taken in accordance with ISO 21448:2022[1] can be integrated into the functional safety 
329 
concept on system level.
330 
6.3.2Further supporting information
331 
The following information can be considered: 
332 
— hazard analysis and risk assessment report (see ISO 26262-3:2018, 6.5.1); and 
333 
— item definition (see ISO 26262-3:2018, 5.5.1). 
334 


<!-- Page 16 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
7 
6.4 Requirements and recommendations
335 
6.4.1
Specification of the functional safety requirements on system level 
336 
6.4.1.1
The functional safety requirements on system level shall be specified in accordance with the 
337 
functional safety concept on item level and the system architectural design of the item considering the 
338 
following:
339 
a) the safety-related dependencies and constraints of items, systems and their elements; 
340 
b) the external interfaces of the system, if applicable; and 
341 
c) the configurability of the system.
342 
NOTE 1
Design constraints can result from: environmental conditions, the installation space, the implementation itself 
343 
(e.g. available performance, thermal capacity, thermal dissipation), and other functional or non-functional requirements 
344 
(e.g. security, physical limits of used technology). 
345 
NOTE 2
The configurability of systems is determined by variants in the system elements, by configuration data or by 
346 
calibration data and is often used as part of the strategy to reuse existing systems for different applications. 
347 
6.4.1.2
The functional safety requirements on system level shall specify the stimulus response of the system 
348 
that affects the achievement of safety requirements. This includes the combinations of relevant stimuli and 
349 
failures with each relevant operating mode and defined system state. 
350 
The Brake System Electronic Control Unit (ECU) disables Adaptive Cruise Control (ACC) braking if a 
351 
received ACC command message fails error detection code checks. 
352 
6.4.1.3
If other functions or requirements are implemented by the system or its elements, in addition to 
353 
those functions for which functional safety requirements are specified, then these functions or requirements 
354 
shall be specified or their specification referenced. 
355 
Other requirements can come from Economic Commission for Europe (ECE) rules, Federal Motor Vehicle 
356 
Safety Standard (FMVSS), company platform strategies, functional concepts or other concepts such as cybersecurity 
357 
concept.
358 
6.4.1.4
Functional safety and non-safety requirements shall not contradict. 
359 
6.4.2Safety mechanisms
360 
6.4.2.1
The functional safety requirements on system level shall specify the safety mechanisms that detect 
361 
faults and prevent or mitigate failures present at the output of the system that violate the functional safety 
362 
requirements on item level (see ISO 26262-3:2018, Clause 7) including: 
363 
a) the safety mechanisms related to the detection, indication and control of faults in the system itself; 
364 
NOTE 1
This includes the system self-monitoring to detect random hardware faults and, if appropriate, to detect 
365 
systematic faults.
366 
NOTE 2
This includes safety mechanisms for the detection and control of communication channel failures (e.g. 
367 
data interfaces, communication buses, wireless radio link). 
368 
NOTE 3
Safety mechanisms can be specified with respect to the appropriate level within the system architecture. 
369 
b) the safety mechanisms related to the detection, indication and control of faults in other external elements 
370 
that interact with the system;
371 
External devices include other electronic control units, power supplies or communication devices. 
372 


<!-- Page 17 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
8 
c) the safety mechanisms that contribute to the system achieving or maintaining the safe state of the item; 
373 
NOTE 4
This includes arbitration in the case of multiple control requests from safety mechanisms. 
374 
d) the safety mechanisms to define and implement the warning and degradation strategy. 
375 
6.4.2.2
For each safety mechanism that enables an item to achieve or maintain a safe state, the following 
376 
shall be specified:
377 
NOTE 1
In-vehicle testing and experimentation can be used to determine the emergency operation tolerance time 
378 
interval.
379 
a) the transition between states;
380 
NOTE 2This includes the requirements to control the actuators.
381 
b) the fault handling time interval with respect to the timing requirements apportioned from the appropriate 
382 
architectural level;
383 
c) the emergency operation tolerance time interval, see ISO 26262-1:2018, 3.45, if the safe state of the item 
384 
cannot be reached within the FTTI; and
385 
NOTE 3
This sub-requirement aims to achieve a consistent timing within the boundary of the fault tolerant time 
386 
interval (FTTI) which is specified for each Safety Goal. 
387 
d) a summary of the concept of the safety mechanism, including a rationale for the achievement of safety. 
388 
EXAMPLE 1Duration of the degraded operation prior to the safe state.
389 
EXAMPLE 2
A safety mechanism for a brake-by-wire application, which depends on the power supply, can include the 
390 
specification of a secondary power supply or storage device (capacity, time to activate and operate, etc.). 
391 
6.4.2.3
This requirement applies to ASILs (A), (B), C, and D. If applicable, safety mechanisms shall be 
392 
specified to prevent faults from being latent. 
393 
NOTE 1
Only random hardware faults which are multiple-point faults have the potential to be latent. 
394 
Self-tests are safety mechanisms which verify the status of components during the different operation 
395 
modes (e.g. power-up, power-down, during operation or in an additional self-test mode) to detect multiple-point faults. 
396 
Valve, relay or lamp function tests that take place during power up routines are examples of self-tests. 
397 
NOTE 2
The need for safety mechanisms preventing faults from being latent can be identified in accordance with the 
398 
latent fault metric, given in ISO 26262-5:2018, Clause 8. 
399 
NOTE 3
These safety mechanisms are usually related to self-tests that take place during power up (pre-drive checks), 
400 
during operation, during power-down (post-drive checks), and as part of maintenance. 
401 
6.4.2.4
This requirement applies to ASILs (A), (B), C, and D. To avoid multiple‑point failures, the diagnostic 
402 
test strategy shall be specified for each safety mechanism implemented to detect multiple-point faults, 
403 
considering:
404 
a) the reliability requirements of the hardware components with consideration given to their role in the 
405 
architecture and their contribution to a multiple-point failure; 
406 
b) the specified quantitative target values for the maximum probability of violation of each safety goal due 
407 
to random hardware failures (see ISO 26262-5:2018, Clause 9); 
408 


<!-- Page 18 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
9 
c) the assigned ASIL derived from the related safety goal, the related functional safety requirement or 
409 
functional safety requirement at a higher hierarchical level; and 
410 
d) the multiple-point fault detection time interval. 
411 
NOTE 1
The diagnostic test strategy can be time driven (e.g. using the diagnostic test time interval) or event driven 
412 
(e.g. a start-up test).
413 
NOTE 2
A second-order multiple-point failure comprises two faults, separated by the multiple-point fault detection 
414 
time interval.
415 
NOTE 3
The use of the following measures depends on the time constraints: 
416 
—   periodic testing of the system or elements during operation; 
417 
—   self-tests of elements during power-up or power-down; and 
418 
—   testing the system or elements during maintenance. 
419 
NOTE 4
Systems with always-on properties might need detection mechanisms for multiple-point faults which can be 
420 
executed during runtime or define special self-testing states. 
421 
6.4.2.5
This requirement applies to ASILs (A), (B), C, and D. The development of safety mechanisms that are 
422 
implemented only to prevent dual point faults from being latent shall at least comply with: 
423 
a) ASIL B for functional safety requirements assigned ASIL D; 
424 
b) ASIL A for functional safety requirements assigned ASIL B and ASIL C; and 
425 
c) QM for functional safety requirements assigned ASIL A. 
426 
If ASIL decomposition is applied to a requirement, then this clause is applied to the decomposed requirement. 
427 
A memory has a parity as its safety mechanism, with requirements rated ASIL B. The requirement for the 
428 
self-test that tests the capability of the parity to detect and signal memory faults can be rated ASIL A. 
429 
6.4.3
System architectural design specification and functional safety concept on system level 
430 
6.4.3.1
The system architectural design and the functional safety concept on system level shall be based on 
431 
the item definition, functional safety concept on item level and the prior system architectural design. 
432 
6.4.3.2
The consistency of the system architectural design in ISO 26262-3:2018, 7.3.1 and the system 
433 
architectural design shall be checked. If discrepancies are identified, an iteration of the activities described in 
434 
ISO 26262-3:2018 may be necessary.
435 
6.4.3.3
The system architectural design shall implement the functional safety requirements on system level. 
436 
6.4.3.4
With regard to the implementation of the functional safety requirements on system level, the 
437 
following shall be considered in the system architectural design: 
438 
a) the ability to verify the system architectural design; 
439 
b) the technical capability of the intended hardware and software elements with regard to the achievement 
440 
of functional safety; and
441 
c) the ability to execute tests during system integration. 
442 


<!-- Page 19 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
10 
6.4.3.5
The internal and external interfaces of safety-related elements shall be defined such that other 
443 
elements shall not have adverse safety-related effects on the safety-related elements. 
444 
6.4.3.6
If ASIL decomposition is applied to the safety requirements during system architectural design, it 
445 
shall be applied in accordance with ISO 26262-9:2018, Clause 5. 
446 
6.4.4Safety Analyses and avoidance of systematic failures
447 
6.4.4.1
Safety analyses on the system architectural design shall be performed in accordance with Table 1 
448 
and ISO 26262-9:2018, Clause 8 in order to: 
449 
— provide evidence for the suitability of the system design to provide the specified safety-related functions 
450 
and properties with respect to the ASIL; 
451 
— identify the causes of failures and the effects of faults; 
452 
— identify or confirm the safety-related system elements and interfaces; and 
453 
— support the design specification and verify the effectiveness of the safety mechanisms based on identified 
454 
causes of faults and the effects of failures. 
455 
Table 1 — System architectural design analysis 
456 
AB
C 
D 
1 
Deductive analysiso+++++
2 
Inductive analysis++++++++NOTE 1
Safety-related properties include independency and freedom from interference requirements, see ISO 26262-
457 
9:2018, 7.2.
458 
NOTE 2
The purpose of these analyses is to assist in the design. Therefore at this stage, qualitative analysis is sufficient. 
459 
Quantitative analysis can be performed if necessary. 
460 
NOTE 3
The analysis is conducted at the level of detail necessary to identify causes and effects of random hardware 
461 
failures and systematic failures.
462 
NOTE 4
The aim of using a combination of deductive and inductive methods is to provide complementary approaches 
463 
to analysis, see also ISO 26262-9:2018, 8.2. 
464 
6.4.4.2
Identified internal causes of failure shall be eliminated, or their effects mitigated where necessary, 
465 
to comply with the safety goals or requirements. 
466 
6.4.4.3
Identified external causes of failure shall be eliminated, or their effects mitigated where necessary, 
467 
to comply with the safety goals or requirements. 
468 
6.4.4.4
To reduce the likelihood of systematic failures, well-trusted systems design principles should be 
469 
applied where applicable. These may include the following: 
470 
a) reuse of well-trusted functional safety concepts; 
471 
b) reuse of well-trusted designs for elements, including hardware and software components; 
472 
c) reuse of well-trusted mechanisms for the detection and control of failures; and 
473 
d) reuse of well-trusted or standardized interfaces. 
474 


|  | Deductive analysis |  |  | ++ | ++ |
|  | Inductive analysis | ++ | ++ | ++ | ++ |



<!-- Page 20 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
11 
6.4.4.5
An analysis of the suitability of well-trusted design principles shall be performed and documented 
475 
to ensure consistency and suitability to the product’s application. 
476 
6.4.4.6
In order to avoid systematic faults, the system architectural design shall exhibit the following 
477 
properties:
478 
a) modularity;
479 
b) granularity; and
480 
c) simplicity.
481 
Aforementioned properties can be achieved by a design strategy for handling the configurability of the system 
482 
and by the use of design principles such as hierarchical design, precisely defined interfaces, avoidance of unnecessary 
483 
complexity of components and interfaces, maintainability, and verifiability. 
484 
6.4.4.7
Evidence that the system architectural design is fulfilling the requirements for independence shall 
485 
be provided, if applicable, based on the analysis of dependent failures in accordance with ISO 26262-9:2018, 
486 
Clause 7.
487 
6.4.4.8
Hazards newly identified during safety analyses or during the system architectural design that are 
488 
not already covered by a safety goal shall be included in an updated hazard analysis and risk assessment 
489 
(HARA) in accordance with ISO 26262-3.
490 
Hazards not already covered by a safety goal may be non-functional hazards. Non-functional hazards are 
491 
outside the scope of ISO 26262, but they can be annotated in the hazard analysis and risk assessment; e.g. by annotating 
492 
the hazard with the following statement “No ASIL is assigned to this hazard as it is not within the scope of ISO 26262”. 
493 
6.4.5
Measures for control of random hardware failures during operation 
494 
6.4.5.1
Measures for the detection, control or mitigation of random hardware failures shall be specified 
495 
with respect to the system architectural design given in 6.4.3. 
496 
EXAMPLE 1
Such measures can be hardware diagnostic features and their usage by the software to detect random 
497 
hardware failures.
498 
EXAMPLE 2
A hardware design having random hardware failures that always result in the safe state being entered 
499 
without detection (i.e. a fail-safe hardware design). 
500 
A quantitative approximation of the inductive and deductive analyses in 6.4.4.1 is helpful to decide if further 
501 
safety measures are necessary. A final decision may be necessary after hardware analysis according to ISO 26262-5. 
502 
6.4.5.2
This requirement applies to ASILs (B), C, and D of the safety goal. One of the alternative procedures 
503 
for the evaluation of violation of the safety goal due to random hardware failures (see ISO 26262-5:2018, 
504 
Clause 9) shall be chosen and the target values shall be specified for final evaluation at the item level. 
505 
6.4.5.3
This requirement applies to ASILs (B), C, and D of the safety goal. Appropriate target values for 
506 
failure rates and diagnostic coverage should be specified at the element level in order to comply with: 
507 
a) the target values of the metrics in ISO 26262-5:2018, Clause 8; and 
508 
b) the procedures in ISO 26262-5:2018, Clause 9. 
509 
6.4.5.4
This requirement applies to ASILs (B), C, and D. For distributed developments (see ISO 26262-
510 
8:2018, Clause 5) the derived target values shall be communicated to each relevant party. 
511 
Architectural constraints described in ISO 26262-5:2018, Clauses 8 and 9, are not necessarily applicable to 
512 
COTS parts and components. This is because suppliers usually cannot foresee the usage of their products in the end-item 
513 
and the potential safety implications. In such a case, basic data such as failure rate, failure modes, failure rate distribution 
514 


<!-- Page 21 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
12 
per failure modes, built-in diagnostics, etc. are made available by the supplier in order to allow the estimation of 
515 
architectural constraints at overall hardware architecture level. 
516 
6.4.6Allocation to hardware and software
517 
6.4.6.1
The functional safety requirements on system level shall be allocated to the system architectural 
518 
design elements with system, hardware or software as the implementing technology. 
519 
If the requirements are allocated to system as implementing technology, ISO 26262-4 is used again for further 
520 
development of these requirements until they can be allocated to hardware and software. 
521 
6.4.6.2
The allocation and partitioning decisions shall comply with the system architectural design. 
522 
To achieve independence and to avoid propagation of failures, the system architectural design can implement 
523 
the partitioning of functions and components. 
524 
6.4.6.3
Each system architectural design element shall inherit the highest ASIL from the functional safety 
525 
requirements that it implements.
526 
6.4.6.4
If a system architectural design element is comprised of sub-elements with different ASILs assigned, 
527 
or of safety-related and non-safety-related sub-elements, then each of these shall be treated in accordance 
528 
with the highest ASIL, unless the criteria for coexistence (in accordance with ISO 26262-9:2018, Clause 6) are 
529 
met.
530 
6.4.6.5
If functional safety requirements are allocated to custom hardware elements that incorporate 
531 
programmable behaviour (such as ASICs, FPGA or other forms of digital hardware) an adequate development 
532 
process, combining requirements from ISO 26262-5 and ISO 26262-6, shall be defined and implemented. 
533 
NOTE 1
The evidence of compliance with an allocated safety requirement for some of those hardware elements can 
534 
be provided through evaluation methods in accordance with ISO 26262-8:2018, Clause 13, if the criteria for applying this 
535 
clause are met.
536 
NOTE 2Guidance can be found in ISO 26262-11:2018.
537 
6.4.7Hardware-software interface (HSI) specification
538 
6.4.7.1
The HSI specification shall specify the hardware and software interaction and be consistent with the 
539 
functional safety concept on system level. The HSI specification shall include the component's hardware parts 
540 
that are controlled by software and hardware resources that support the execution of the software. 
541 
The aspects and characteristics detailed in the HSI are given in Annex B. 
542 
6.4.7.2
The HSI specification shall include the following characteristics: 
543 
a) the relevant operating modes of the hardware devices (in their respective system configurations) and the 
544 
relevant configuration parameters;
545 
EXAMPLE 1
Operating modes of hardware devices such as default, initialization, test or advanced modes. 
546 
EXAMPLE 2
Configuration parameters such as gain control, band pass frequency or clock pre-scaler. 
547 
b) the hardware features that ensure the independence between elements or that support software 
548 
partitioning;
549 
c) shared and exclusive use of hardware resources; 
550 
EXAMPLE 3
Memory mapping, allocation of registers, timers, interrupts, I/O ports. 
551 
d) the access mechanism to hardware devices; and 
552 


<!-- Page 22 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
13 
EXAMPLE 4Serial, parallel, slave, master/slave.
553 
e) the timing constraints derived from the functional safety concept on system level. 
554 
The HSI specification can contain requirements to be considered for hardware design or software design. 
555 
6.4.7.3
The relevant diagnostic capabilities of the hardware, and their use by the software, shall be specified 
556 
in the HSI specification:
557 
a) the hardware diagnostic features shall be defined; and 
558 
Detection of over-current, short-circuit or over-temperature. 
559 
b) the diagnostic features concerning the hardware, to be implemented in software, shall be defined. 
560 
6.4.7.4
The HSI shall be specified during the system architectural design. 
561 
The HSI is refined during hardware development (see ISO 26262-5:2018, Clause 6) and during software 
562 
development (see ISO 26262-6:2018, Clause 6). 
563 
6.4.8Production, operation, service and decommissioning
564 
6.4.8.1
The requirements addressed in ISO 26262-7:2018 for production, operation, service and 
565 
decommissioning, identified during the system architectural design, shall be specified. These include: 
566 
a) measures required to achieve, maintain or restore the safety-related functions and properties of the item 
567 
and its elements during production, service or decommissioning; 
568 
b) the safety-related special characteristics; 
569 
c) the requirements that ensure proper identification of systems or elements; 
570 
d) the verification measures for production; 
571 
e) the service requirements including diagnostic data and service notes; and 
572 
f)measures for decommissioning.
573 
Assembly or disassembly instructions, service notes, instructions regarding permitted repair for system 
574 
elements, decommissioning instructions, labelling of elements. 
575 
There are two main aspects that ensure functional safety during production, operation, service and 
576 
decommissioning. The first aspect relates to those activities that ensure an adequate system architectural design and the 
577 
specification of suitable safety-related special characteristics during the product development at the system level, which 
578 
are given in requirement 6.4.8.1, while the second aspect relates to those activities that ensure the achievement or 
579 
maintenance of functional safety during the production, operation, service and decommissioning phase (e.g. based on 
580 
specified safety-related special characteristics), which are addressed in ISO 26262-7:2018. 
581 
6.4.8.2
Diagnostic features shall be specified in order to provide the required data that enables field 
582 
monitoring for the item or its elements according to ISO 26262-2:2018, Clause 7, with consideration being 
583 
given to the results of safety analyses and the implemented safety mechanisms. 
584 
6.4.8.3
To restore or maintain functional safety, diagnostic features shall be specified that allow fault 
585 
identification and the effectiveness of maintenance or repair to be checked during servicing. 
586 


<!-- Page 23 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
14 
6.4.9Verification
587 
6.4.9.1
The functional safety requirements on system level shall be verified in accordance with ISO 26262-
588 
8:2018, Clauses 6 and 9, to provide evidence for their correctness, completeness, and consistency with respect 
589 
to the given boundary conditions of the system. 
590 
6.4.9.2
The system architectural design, the hardware-software interface (HSI) specification and the 
591 
specification of requirements for production, operation, service and decommissioning and the functional 
592 
safety concept on system level shall be verified using the verification methods listed in Table 2 to provide 
593 
evidence that the following objectives are achieved: 
594 
a) they are suitable and adequate to achieve the required level of functional safety according to the relevant 
595 
ASIL;
596 
b) there is consistency between the system architectural design and the functional safety concept on system 
597 
level; and
598 
c) validity of and compliance with system architectural designs of prior development steps. 
599 
Safety anomalies and incompleteness identified will be reported in accordance with ISO 26262-2:2018, 5.4.3. 
600 
Table 2 — Verification
601 
AB
C 
D 
1aInspectiona+++++++
1bWalkthrougha+++oo
2aSimulationb++++++
2bSystem prototyping and vehicle testsb++++++
3 
System architectural design analysescsee Table 1a
Methods 1a and 1b serve as a check of complete and correct implementation of the requirements. 
b
Methods 2a and 2b can be used advantageously as a fault injection test to support the argumentation of completeness and 
correctness of a system architectural design with respect to faults. 
c
For conducting safety analyses, see ISO 26262-9:2018, Clause 8. 
6.5 Work products
602 
6.5.1 Functional safety concept on system level resulting from requirements in 6.4.1 to 6.4.6. 
603 
6.5.2 System architectural design specification resulting from requirements in 6.4.3 to 6.4.6. 
604 
6.5.3 Hardware-software interface (HSI) specification resulting from requirements in 6.4.7. 
605 
6.5.4 Specification of requirements for production, operation, service and decommissioning resulting 
606 
from requirements in 6.4.8.
607 
6.5.5 Verification report for system architectural design, the hardware-software interface (HSI) 
608 
specification, the specification of requirements for production, operation, service and 
609 
decommissioning, and the functional safety concept on system level resulting from requirements in 6.4.9. 
610 
6.5.6 Safety analyses report resulting from requirements in 6.4.4. 
611 


| 1a | Inspectiona |  | ++ | ++ | ++ |
| 1b | Walkthrougha | ++ |  |  |  |
| 2a | Simulationb |  |  | ++ | ++ |
| 2b | System prototyping and vehicle testsb |  |  | ++ | ++ |
|  | System architectural design analysesc | see Table 1 |  |  |  |
| a Methods 1a and 1b serve as a check of complete and correct implementation of the requirements. b Methods 2a and 2b can be used advantageously as a fault injection test to support the argumentation of completeness and correctness of a system architectural design with respect to faults. c For conducting safety analyses, see ISO 26262-9:2018, Clause 8. |  |  |  |  |  |



<!-- Page 24 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
15 
7 System integration and testing
612 
7.1 Objectives
613 
The system integration and testing comprises different steps. The first is the integration of the hardware and 
614 
software of each element. The second step is the integration of the elements that form a system. The objectives 
615 
of this clause are:
616 
a) to define the integration steps and to integrate the system elements until the system is fully integrated; 
617 
b) to verify that the defined safety measures, resulting from safety analyses at the system architectural level, 
618 
are properly implemented; and
619 
c) to provide evidence that the integrated system elements fulfil their safety requirements according to the 
620 
system architectural design.
621 
The integration of potentially multiple systems and elements into an item and the integration of the item with 
622 
other systems within a vehicle is described in ISO 26262-3:2018, Clause 8. 
623 
7.2 General
624 
The integration of the item's elements is carried out in a systematic way starting from software-hardware 
625 
integration and testing through system integration and testing to vehicle integration and testing. Specified 
626 
integration tests are performed at each integration stage to provide evidence that the integrated elements 
627 
interact correctly.
628 
In the case when other technology (OT) elements are realized within the item for functional safety, the OT 
629 
system integration and verification are taken into consideration. 
630 
After sufficient development of system, hardware and software in accordance with Clause 6, ISO 26262-5 and 
631 
ISO 26262-6, system integration can be started in accordance with this clause. 
632 
7.3 Inputs to this clause
633 
7.3.1Prerequisites
634 
The following information shall be available: 
635 
— safety goals from the hazard analysis and risk assessment report in accordance with ISO 26262-3:2018, 
636 
6.5.1;
637 
— functional safety concept on item level in accordance with ISO 26262-3:2018, 7.5.1; 
638 
— functional safety concept on system level in accordance with 6.5.1; 
639 
— system architectural design specification in accordance with 6.5.2; and 
640 
— HSI specification in accordance with 6.5.3, ISO 26262-5:2018, 6.5.2 and ISO 26262-6:2018, 6.5.2. 
641 
7.3.2Further supporting information
642 
The following information can be considered: 
643 
— vehicle architecture (from an external source); 
644 
— functional safety concepts of other vehicle systems (from an external source); and 
645 


<!-- Page 25 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
16 
— safety analyses report (see 6.5.6).
646 
7.4 Requirements and recommendations
647 
7.4.1Specification of integration and test strategy
648 
7.4.1.1
To provide evidence that the system architectural design is compliant with the functional safety 
649 
requirements assigned to it and its elements, integration testing activities shall be performed in accordance 
650 
with ISO 26262-8:2018, Clause 9 to check: 
651 
a) the correct implementation of functional safety requirements on all levels; 
652 
b) the correct functional performance, accuracy and timing of safety mechanisms; 
653 
c) the consistent and correct implementation of interfaces; and 
654 
d) the robustness.
655 
The criteria in a)-d) may be checked by analysing data gathered in the field if suitability and relevance of the 
656 
data is justified in accordance with ISO 26262 8:2018, Clause X. 
657 
7.4.1.2
An integration and test strategy shall be defined that considers the system architectural design 
658 
specification, the functional safety concept on item level and the functional safety concept on system level. It 
659 
shall address:
660 
a) the test goals suitable to provide evidence for functional safety; and 
661 
b) the integration and testing of the item and its elements that contribute to the safety concepts. 
662 
This includes elements of other technologies that contribute to the safety concepts. 
663 
7.4.1.3
To enable the item integration, the following shall be performed based on the integration and test 
664 
strategy:
665 
a) the item integration and test strategy shall be defined for the hardware-software integration and testing; 
666 
b) the item integration and test strategy shall be defined to include the specification of integration tests for 
667 
the system and vehicle-levels. It shall ensure that open issues from hardware-software testing are 
668 
addressed;
669 
c) the item integration and test strategy shall consider interfaces between vehicle systems (both internal 
670 
and external to the item) and the environment; 
671 
d) the item integration and test strategy shall consider if systems or elements are being integrated that were 
672 
developed as safety element out of context (SEooC) and if the assumptions made during that development 
673 
need to be verified;
674 
e) the item integration and test strategy shall consider the results of the safety analysis and their associated 
675 
fault models according to ISO26262-9:2018, 8.4.7; and 
676 
f)
the item integration and test strategy shall consider interaction between OT and E/E elements when other 
677 
technology elements are realized within the item for functional safety or if other technology safety 
678 
assumptions made during development need to be verified. 
679 
NOTE 1
Safety analysis considers the evaluation of failure mode coverage, fault detection, and fault reaction capability 
680 
within the FTTI.
681 


<!-- Page 26 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
17 
NOTE 2
The specification of the integration and the testing carried out at the hardware-software integration level and 
682 
the item level considers the interface and the interaction between hardware and software. 
683 
 
684 
7.4.1.4
If the system is configurable (e.g. by variance of elements or calibration data), then the testing at the 
685 
system or vehicle level shall provide evidence of compliance with safety requirements for the configurations 
686 
intended for series production.
687 
Testing a justified subset of configurations may be sufficient. 
688 
7.4.1.5
The fulfilment of each functional safety requirement shall be verified (if applicable by testing) at 
689 
least once in the complete integration.
690 
NOTE 1
A common practice is to verify a safety requirement at the next higher level of integration to which it has been 
691 
specified.
692 
NOTE 2
When a SEooC is integrated in a safety-related system, validity of assumptions used for its development is 
693 
also verified.
694 
NOTE 3
Safety anomalies identified during integration testing are reported in accordance with ISO 26262-2:2018, 
695 
5.4.3.
696 
7.4.1.6
To enable the appropriate specification of test cases for the integration tests, test cases shall be 
697 
derived using an appropriate combination of methods, as listed in Table 3, and by considering the integration 
698 
level.
699 
 
700 
Table 3 — Methods for deriving test cases for integration testing 
701 
AB
C 
D 
1aAnalysis of requirements++++++++
1bAnalysis of external and internal interfaces+++++++
1c
Generation and analysis of equivalence classes for hardware-software 
integration++++++1d
Analysis of boundary values++++++1e
Error guessing based on knowledge or experience 
++++++1fAnalysis of functional dependencies
++++++1g
Analysis of common limit conditions, sequences, and sources of dependent 
failures, see ISO 26262-9:2018, Clause 7 
++++++1h
Analysis of environmental conditions and operational use cases 
+++++++1iAnalysis of field experience
+++++++7.4.1.7
The integration and test strategy shall be verified in accordance with ISO 26262-8:2018, Clause 9, 
702 
to provide evidence for its consistency and compliance with the system architectural design and 
703 
corresponding functional safety requirements on system level. 
704 


| 1a | Analysis of requirements | ++ | ++ | ++ | ++ |
| 1b | Analysis of external and internal interfaces |  | ++ | ++ | ++ |
| 1c | Generation and analysis of equivalence classes for hardware-software integration |  |  | ++ | ++ |
| 1d | Analysis of boundary values |  |  | ++ | ++ |
| 1e | Error guessing based on knowledge or experience |  |  | ++ | ++ |
| 1f | Analysis of functional dependencies |  |  | ++ | ++ |
| 1g | Analysis of common limit conditions, sequences, and sources of dependent failures, see ISO 26262-9:2018, Clause 7 |  |  | ++ | ++ |
| 1h | Analysis of environmental conditions and operational use cases |  | ++ | ++ | ++ |
| 1i | Analysis of field experience |  | ++ | ++ | ++ |



<!-- Page 27 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
18 
7.4.2Hardware-software integration and testing
705 
7.4.2.1Hardware-software integration
706 
7.4.2.1.1 The hardware developed in accordance with ISO 26262-5 and the software developed in 
707 
accordance with ISO 26262-6 shall be integrated and used as the subject of the test activities in Table 4 to 
708 
Table 8.
709 
7.4.2.1.2 The integrated hardware and software shall be tested for compliance with the requirements 
710 
addressing the HSI specification.
711 
The use of production-intent hardware and software is preferred. Modified hardware or software might be 
712 
used where necessary for particular test techniques. 
713 
7.4.2.2
Test goals and test methods during hardware-software testing 
714 
7.4.2.2.1 The test goals resulting from the requirements 7.4.2.2.2 to 7.4.2.2.6 shall be addressed by the 
715 
application of adequate test methods, as given in the corresponding tables. 
716 
NOTE 1
These will support the detection of systematic faults in the system architectural design. 
717 
NOTE 2
Depending on the implemented functionality, its complexity or the distributed nature of the system, it may be 
718 
feasible to perform tests in other integration activities than hardware-software integration and testing, provided 
719 
adequate rationale is given.
720 
7.4.2.2.2 Evidence for the correct implementation of the safety-related functions and behaviour according 
721 
to the functional safety requirements at the hardware-software level shall be provided by using test methods 
722 
listed in Table 4.
723 
Table 4 — Correct implementation of functional safety requirements at the hardware-software level 
724 
AB
C 
D 
1aRequirements-based testa++++++++
1bFault injection testb+++++++
1cBack-to-back testc++++++
a
A requirements-based test denotes a test against functional and non-functional requirements. 
b
A fault injection test uses special means to introduce faults into the test object during runtime. This can be done within the 
software via a special test interface or specially prepared hardware. The method is often used to improve the test coverage of the 
safety requirements, because during normal operation safety mechanisms are not invoked. 
c
A back-to-back test compares the responses of the test object with the responses of a simulation model to the same stimuli, to 
detect differences between the behaviour of the model and its implementation. 
The differences in the level of effort applied for Method 1b in Table 4 and Table 9 result from the amount of 
725 
effort needed to conduct fault injection tests at the system level. 
726 
7.4.2.2.3 This requirement applies to ASIL (A), B, C, and D. The correct functional performance, accuracy 
727 
and timing of the safety mechanisms at the hardware-software level shall be demonstrated using test methods 
728 
listed in Table 5.
729 


| 1a | Requirements-based testa | ++ | ++ | ++ | ++ |
| 1b | Fault injection testb |  | ++ | ++ | ++ |
| 1c | Back-to-back testc |  |  | ++ | ++ |
| a A requirements-based test denotes a test against functional and non-functional requirements. b A fault injection test uses special means to introduce faults into the test object during runtime. This can be done within the software via a special test interface or specially prepared hardware. The method is often used to improve the test coverage of the safety requirements, because during normal operation safety mechanisms are not invoked. c A back-to-back test compares the responses of the test object with the responses of a simulation model to the same stimuli, to detect differences between the behaviour of the model and its implementation. |  |  |  |  |  |



<!-- Page 28 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
19 
Table 5 — Correct functional performance, accuracy and timing of safety mechanisms at the 
730 
hardware-software level
731 
AB
C 
D 
1
aBack-to-back testa++++++
1
bPerformance testb+++++++
a
A back-to-back test compares the responses of the test object with the responses of a simulation model to the same stimuli, to 
detect differences between the behaviour of the model and its implementation. 
b
A performance test can verify the performance (e.g. task scheduling, timing, power output) in the context of the whole test 
object, and can verify the ability of the intended control software to run with the hardware. 
7.4.2.2.4 This requirement applies to ASIL (A), B, C, and D. Evidence for the consistent and correct 
732 
implementation of the external and internal interfaces at the hardware-software level shall be provided by 
733 
using test methods listed in Table 6.
734 
Table 6 — Consistent and correct implementation of external and internal interfaces at the 
735 
hardware-software level
736 
AB
C 
D 
1
aTest of external interfacesa+++++++
1
bTest of internal interfacesa+++++++
1cInterface consistency checka+++++++
a
Interface tests of the test object include tests of analogue and digital inputs and outputs, boundary tests and equivalence-class 
tests, to test the compatibility, timings and other specified ratings. Internal interfaces of an ECU can be tested by static tests for the 
compatibility of software and hardware as well as dynamic tests of Serial Peripheral Interface (SPI) or Integrated Circuit (IC) 
communications or any other interface between the elements of an ECU. 
7.4.2.2.5 This requirement applies to ASIL (A), (B), C, and D. The effectiveness of the hardware fault 
737 
detection mechanisms at the hardware-software level, with respect to the fault models, shall be demonstrated 
738 
using test methods listed in Table 7.
739 
For references to fault models, see ISO 26262-5:2018, Annex D. 
740 
Table 7 — Effectiveness of a safety mechanisms at the hardware-software level 
741 
AB
C 
D 
1
aFault injection testa++++++
1
bError guessing testb++++++
a
A fault injection test uses special means to introduce faults into the test object during runtime. This can be done within the 
software via a special test interface or specially prepared hardware. The method is often used to improve the test coverage of the 
safety requirements, because during normal operation safety mechanisms are not invoked. 
b
An error guessing test uses expert knowledge and data collected through lessons learned to anticipate errors in the test object. 
Then a set of tests along with adequate test facilities is designed to check for these errors. Error guessing is an effective method 
given a tester who has previous experience with similar test objects. 


| 1 a | Back-to-back testa |  |  | ++ | ++ |
| 1 b | Performance testb |  | ++ | ++ | ++ |
| a A back-to-back test compares the responses of the test object with the responses of a simulation model to the same stimuli, to detect differences between the behaviour of the model and its implementation. b A performance test can verify the performance (e.g. task scheduling, timing, power output) in the context of the whole test object, and can verify the ability of the intended control software to run with the hardware. |  |  |  |  |  |



| 1 a | Test of external interfacesa |  | ++ | ++ | ++ |
| 1 b | Test of internal interfacesa |  | ++ | ++ | ++ |
| 1c | Interface consistency checka |  | ++ | ++ | ++ |
| a Interface tests of the test object include tests of analogue and digital inputs and outputs, boundary tests and equivalence-class tests, to test the compatibility, timings and other specified ratings. Internal interfaces of an ECU can be tested by static tests for the compatibility of software and hardware as well as dynamic tests of Serial Peripheral Interface (SPI) or Integrated Circuit (IC) communications or any other interface between the elements of an ECU. |  |  |  |  |  |



| 1 a | Fault injection testa |  |  | ++ | ++ |
| 1 b | Error guessing testb |  |  | ++ | ++ |
| a A fault injection test uses special means to introduce faults into the test object during runtime. This can be done within the software via a special test interface or specially prepared hardware. The method is often used to improve the test coverage of the safety requirements, because during normal operation safety mechanisms are not invoked. b An error guessing test uses expert knowledge and data collected through lessons learned to anticipate errors in the test object. Then a set of tests along with adequate test facilities is designed to check for these errors. Error guessing is an effective method given a tester who has previous experience with similar test objects. |  |  |  |  |  |



<!-- Page 29 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
20 
7.4.2.2.6 This requirement applies to ASIL (A), (B), (C), and D. The level of robustness of the elements at the 
742 
hardware-software level shall be demonstrated using test methods listed in Table 8. 
743 
Table 8 — Level of robustness at the hardware-software level 
744 
AB
C 
D 
1
aResource usage testa+++++
1
bStress testb+++++
a
A resources usage test can be done statically (e.g. by checking for code sizes or analysing the code regarding interrupt usage, 
in order to verify that worst-case scenarios do not run out of resources), or dynamically by runtime monitoring. 
b
A stress test verifies the test object for correct operation under high operational loads or high demands from the environment. 
Therefore, tests under high loads on the test object, or with exceptional interface loads, or values (bus loads, electrical shocks, etc.), 
as well as tests with extreme temperatures, humidity or mechanical shocks, can be applied. 
7.4.3System integration and testing
745 
7.4.3.1System integration
746 
7.4.3.1.1 The individual elements of the system shall be integrated in accordance with the system 
747 
architectural design, and tested in accordance with the integration and test strategy. 
748 
The tests are intended to provide evidence that each system element interacts correctly, complies with the 
749 
functional safety requirements, and gives an adequate level of confidence that unintended behaviours, that could violate 
750 
a safety goal, are absent.
751 
7.4.3.2Test goals and test methods during system testing
752 
7.4.3.2.1 The test goals resulting from the requirements 7.4.3.2.2 to 7.4.3.2.5 shall be addressed by the 
753 
application of adequate test methods, as given in the corresponding tables. 
754 
NOTE 1
These will support the detection of systematic faults during system integration and testing. 
755 
NOTE 2
Depending on the implemented functionality, its complexity, or the distributed nature of the system, it may 
756 
be feasible to perform tests in other integration activities than system integration and testing, provided adequate 
757 
rationale is given.
758 
7.4.3.2.2 Evidence for the correct implementation of functional safety and functional safety requirements 
759 
at the system level shall be provided by using test methods as listed in Table 9. 
760 
Table 9 — Correct implementation of functional safety and functional safety requirements at the 
761 
system level
762 
AB
C 
D 
1
aRequirement-based testa++++++++
1
bFault injection testb++++++
1cBack-to-back testco++++
a
A requirements-based test denotes a test against functional and non-functional requirements. 


| 1 a | Resource usage testa |  |  |  | ++ |
| 1 b | Stress testb |  |  |  | ++ |
| a A resources usage test can be done statically (e.g. by checking for code sizes or analysing the code regarding interrupt usage, in order to verify that worst-case scenarios do not run out of resources), or dynamically by runtime monitoring. b A stress test verifies the test object for correct operation under high operational loads or high demands from the environment. Therefore, tests under high loads on the test object, or with exceptional interface loads, or values (bus loads, electrical shocks, etc.), as well as tests with extreme temperatures, humidity or mechanical shocks, can be applied. |  |  |  |  |  |



| 1 a | Requirement-based testa | ++ | ++ | ++ | ++ |
| 1 b | Fault injection testb |  |  | ++ | ++ |
| 1c | Back-to-back testc |  |  |  | ++ |
| a A requirements-based test denotes a test against functional and non-functional requirements. |  |  |  |  |  |



<!-- Page 30 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
21 
AB
C 
D 
b
A fault injection test uses special means to introduce faults into the system. This can be done within the system via a special 
test interface or specially prepared elements or communication devices. The method is often used to improve the test coverage of 
the safety requirements, because during normal operation safety mechanisms are not invoked. 
c
A back-to-back test compares the responses of the test object with the responses of a simulation model to the same stimuli, to 
detect differences between the behaviour of the model and its implementation. 
7.4.3.2.3 This requirement applies to ASIL (A), (B), C, and D. The correct functional performance, accuracy, 
763 
coverage of failure modes at the system level, and timing of the safety mechanisms at the system level shall be 
764 
demonstrated using test methods listed in Table 10. 
765 
Table 10 — Correct functional performance, accuracy, coverage of failure modes and timing of safety 
766 
mechanisms at the system level
767 
AB
C 
D 
1aBack-to-back testao++++
1
bFault injection testb++++++
1cPerformance testco++++
1
dError guessing testd++++++
1eTest derived from field experienceeo+++++
a
A back-to-back test compares the responses of the test object with the responses of a simulation model to the same stimuli, to 
detect differences between the behaviour of the model and its implementation. 
b
In the context of demonstrating the effectiveness of the safety mechanisms' failure mode coverage at the system level, fault 
injection method-based test means to introduce faults into the test object during runtime. This can be done within the software via 
a special test interface or specially prepared hardware. This approach is valid for a limited set of fault models, i.e. the simple ones 
that can be realistically injected at system level (like reproducing a stuck-at in a component pin). For fault models at semiconductor 
level (like soft errors or transistor stuck-at), the fault injection method is applied at a more detailed level as described in ISO 26262-
11:2018, 4.8.c
A performance test can verify the performance (e.g. actuator speed or strength, whole system response times) of the safety 
mechanisms of the system.d
An error guessing test uses expert knowledge and data collected through lessons learned to anticipate errors in the system. 
Then a set of tests along with adequate test facilities is designed to check for these errors. Error guessing is an effective method 
given a tester who has previous experience with similar systems. 
e
A test derived from field experience and data gathered from the field 
7.4.3.2.4 Evidence for the consistent and correct implementation of the external and internal interfaces at 
768 
the system level shall be provided by using test methods listed in Table 11. 
769 
Table 11 — Consistent and correct implementation of external and internal interfaces at the system 
770 
771 
AB
C 
D 
1
aTest of external interfacesa+++++++
1
bTest of internal interfacesa+++++++
1
cInterface consistency checka++++++


| b A fault injection test uses special means to introduce faults into the system. This can be done within the system via a special test interface or specially prepared elements or communication devices. The method is often used to improve the test coverage of the safety requirements, because during normal operation safety mechanisms are not invoked. c A back-to-back test compares the responses of the test object with the responses of a simulation model to the same stimuli, to detect differences between the behaviour of the model and its implementation. |  |  |  |  |



| 1a | Back-to-back testa |  |  |  | ++ |
| 1 b | Fault injection testb |  |  | ++ | ++ |
| 1c | Performance testc |  |  |  | ++ |
| 1 d | Error guessing testd |  |  | ++ | ++ |
| 1e | Test derived from field experiencee |  |  | ++ | ++ |
| a A back-to-back test compares the responses of the test object with the responses of a simulation model to the same stimuli, to detect differences between the behaviour of the model and its implementation. b In the context of demonstrating the effectiveness of the safety mechanisms' failure mode coverage at the system level, fault injection method-based test means to introduce faults into the test object during runtime. This can be done within the software via a special test interface or specially prepared hardware. This approach is valid for a limited set of fault models, i.e. the simple ones that can be realistically injected at system level (like reproducing a stuck-at in a component pin). For fault models at semiconductor level (like soft errors or transistor stuck-at), the fault injection method is applied at a more detailed level as described in ISO 26262- 11:2018, 4.8. c A performance test can verify the performance (e.g. actuator speed or strength, whole system response times) of the safety mechanisms of the system. d An error guessing test uses expert knowledge and data collected through lessons learned to anticipate errors in the system. Then a set of tests along with adequate test facilities is designed to check for these errors. Error guessing is an effective method given a tester who has previous experience with similar systems. e A test derived from field experience and data gathered from the field |  |  |  |  |  |



| 1 a | Test of external interfacesa |  | ++ | ++ | ++ |
| 1 b | Test of internal interfacesa |  | ++ | ++ | ++ |
| 1 c | Interface consistency checka |  |  | ++ | ++ |



<!-- Page 31 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
22 
AB
C 
D 
1
dTest of interaction/communicationb++++++++
a
An interface test of the system includes tests of analogue and digital inputs and outputs, boundary tests, and equivalence-class 
tests, to completely test the specified interfaces, compatibility, timings, and other specified characteristics of the system. Internal 
interfaces of the system can be tested by static tests (e.g. match of plug connectors) as well as by dynamic tests concerning bus 
communications or any other interface between system elements. 
b
A communication and interaction test includes tests of the communication between the system elements, as well as between 
the system under test and other vehicle systems during runtime, against the functional and non-functional requirements. 
7.4.3.2.5 The level of robustness at the system level shall be demonstrated using test methods listed in Table 
772 
12.
773 
Table 12 — Level of robustness at the system level 
774 
AB
C 
D 
1
aResource usage testao+++++
1
bStress testbo+++++
1
c
Test for interference resistance and robustness under certain environmental 
conditionsc++++++++a
At the system level, resource usage testing is usually performed in dynamic environments (e.g. lab cars or prototypes). Issues 
to test include power consumption and bus load. 
b
A stress test verifies the correct operation of the system under high operational loads or high demands from the environment. 
Therefore, tests under high loads on the system, or with extreme user inputs or requests from other systems, as well as tests with 
extreme temperatures, humidity or mechanical shocks, can be applied. 
c
A test for interference resistance and robustness, under certain environmental conditions, is a special case of stress testing. 
This includes EMC and ESD tests (e.g. see [ISO 11451 (all parts)[4]], [ISO 11452 (all parts)[5]], [ISO 7637 (all parts)[6]], 
[ISO 10605[7]]).7.5 Work products
775 
7.5.1 Integration and test strategy resulting from requirements in 7.4.1. 
776 
7.5.2 Verification report for integration and test strategy resulting from requirements in 7.4.1. 
777 
7.5.3 Integration and test report resulting from requirements in 7.4.2, 7.4.3 and ISO 26262-3:2018, Clause 
778 
8.
779 


| 1 d | Test of interaction/communicationb | ++ | ++ | ++ | ++ |
| a An interface test of the system includes tests of analogue and digital inputs and outputs, boundary tests, and equivalence-class tests, to completely test the specified interfaces, compatibility, timings, and other specified characteristics of the system. Internal interfaces of the system can be tested by static tests (e.g. match of plug connectors) as well as by dynamic tests concerning bus communications or any other interface between system elements. b A communication and interaction test includes tests of the communication between the system elements, as well as between the system under test and other vehicle systems during runtime, against the functional and non-functional requirements. |  |  |  |  |  |



| 1 a | Resource usage testa |  |  | ++ | ++ |
| 1 b | Stress testb |  |  | ++ | ++ |
| 1 c | Test for interference resistance and robustness under certain environmental conditionsc | ++ | ++ | ++ | ++ |
| a At the system level, resource usage testing is usually performed in dynamic environments (e.g. lab cars or prototypes). Issues to test include power consumption and bus load. b A stress test verifies the correct operation of the system under high operational loads or high demands from the environment. Therefore, tests under high loads on the system, or with extreme user inputs or requests from other systems, as well as tests with extreme temperatures, humidity or mechanical shocks, can be applied. c A test for interference resistance and robustness, under certain environmental conditions, is a special case of stress testing. This includes EMC and ESD tests (e.g. see [ISO 11451 (all parts)[4]], [ISO 11452 (all parts)[5]], [ISO 7637 (all parts)[6]], [ISO 10605[7]]). |  |  |  |  |  |



<!-- Page 32 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
23 
Annex A
780 
(informative)
781 
 
782 
Overview of and workflow of product development at the system level 
783 
Table A.1 provides an overview of objectives, prerequisites and work products of product development at the 
784 
system level.
785 
Table A.1 — Overview of and workflow of product development at the system level 
786 
ObjectivesPrerequisitesWork productsClause 5topics for thedevelopment
at the systemThe objective of this Clause is to provide anoverview of the product development at thesystem level.——
Clause 6FunctionalConcept onsystem levelThe objectives of this Clause are:a) to
functionalrequirementsregardingfunctionality,dependencies,constraints and properties of the
system elements and interfacesneeded for their implementation;b) tofunctionalrequirements regarding the safetymechanisms to be implemented in
the system elements and interfaces;Functional safetyconcept on item level,see ISO 26262- 3:2018,7.5.1.System architectural
design (from an externalsource, see ISO 26262-3:2018, 7.3.1).Requirements to theitem from other safetyrelevant items if
applicable.6.5.1 Functional safetyconcept on system levelresulting fromrequirements in 6.4.1 to6.4.6.
6.5.2 Systemarchitectural designspecification resulting
 
c) to specify requirements regardingthe functional safety of the systemand its elements during production,operation,decommissioning; andd) to verify that the functional safety
requirements are suitable to achievefunctional safety at the system levelconsistentfunctional safety requirements.e) to develop a system architecturaldesign and a functional safety
concept on system level that satisfythe safety requirements and that arenot in conflict with the non-safety-related requirements;
 
from requirements in6.4.3 to 6.4.6.6.5.3 Hardware-softwareinterface (HSI)specification resultingfrom requirements in
6.4.7.6.5.4 Specification ofrequirements forproduction, operation,service anddecommissioning
resulting fromrequirements in 6.4.8.


|  | Objectives | Prerequisites | Work products |
| --- | --- | --- | --- |
| Clause 5 General topics for the product development at the system level | The objective of this Clause is to provide an overview of the product development at the system level. |  |  |
| Clause 6 Functional Safety Concept on system level | The objectives of this Clause are: a) to specify functional safety requirements regarding the functionality, dependencies, constraints and properties of the system elements and interfaces needed for their implementation; b) to specify functional safety requirements regarding the safety mechanisms to be implemented in the system elements and interfaces; | Functional safety concept on item level, see ISO 26262- 3:2018, 7.5.1. System architectural design (from an external source, see ISO 26262- 3:2018, 7.3.1). Requirements to the item from other safety relevant items if applicable. | 6.5.1 Functional safety concept on system level resulting from requirements in 6.4.1 to 6.4.6. 6.5.2 System architectural design specification resulting |
|  | c) to specify requirements regarding the functional safety of the system and its elements during production, operation, service and decommissioning; and d) to verify that the functional safety requirements are suitable to achieve functional safety at the system level and are consistent with the functional safety requirements. e) to develop a system architectural design and a functional safety concept on system level that satisfy the safety requirements and that are not in conflict with the non-safety- related requirements; |  | from requirements in 6.4.3 to 6.4.6. 6.5.3 Hardware-software interface (HSI) specification resulting from requirements in 6.4.7. 6.5.4 Specification of requirements for production, operation, service and decommissioning resulting from requirements in 6.4.8. |



<!-- Page 33 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
24 
ObjectivesPrerequisitesWork products
 
f)to analyse the system architecturaldesign in order to prevent faults andto derive the necessary safety-related special characteristics forproduction and service; and
g) toarchitecturalfunctional safety concept on systemlevel are suitable to satisfy the safetyrequirements according to theirrespective ASIL.
 
6.5.5 Verification reportfor system architecturaldesign, the hardware-software interface (HSI)specification, thespecification of
requirements forproduction, operation,service anddecommissioning, andthe functional safetyconcept on system level
resulting fromrequirements in 6.4.9.6.5.6 Safety analysesreport resulting fromrequirements in 6.4.4.Clause 7
integrationand testingThe objectives of this Clause are:Safety goals from thehazard analysis and riskassessment report (see
ISO 26262-3:2018,6.5.1).Functional safetyconcept on item level(see ISO 26262-3:2018,7.5.1).
Functional safetyconcept on system level(see 6.5.1);System architecturaldesign specification (see6.5.2).
Hardware-softwareinterface specification(HSI) (see 6.5.3).7.5.1 Integration and teststrategy resulting fromrequirements in 7.4.1.
7.5.2 Verification reportfor integration and teststrategy resulting fromrequirements in 7.4.1.7.5.3 Integration and testreport resulting from
requirements in 7.4.2,7.4.3 and ISO 26262-3:2018, Clause 8.a) to define the integration steps and tointegrate the system elements until thesystem is fully integrated;
b) to verify that the defined safety measures, 
resulting from safety analyses at the system 
architectural level, are properlyimplemented; andc) to provide evidence that the integratedsystem elements fulfil their safetyrequirements according to the systemarchitectural design.


|  | Objectives | Prerequisites | Work products |
| --- | --- | --- | --- |
|  | f) to analyse the system architectural design in order to prevent faults and to derive the necessary safety- related special characteristics for production and service; and g) to verify that the system architectural design and the functional safety concept on system level are suitable to satisfy the safety requirements according to their respective ASIL. |  | 6.5.5 Verification report for system architectural design, the hardware- software interface (HSI) specification, the specification of requirements for production, operation, service and decommissioning, and the functional safety concept on system level resulting from requirements in 6.4.9. 6.5.6 Safety analyses report resulting from requirements in 6.4.4. |
| Clause 7 System integration and testing | The objectives of this Clause are: | Safety goals from the hazard analysis and risk assessment report (see ISO 26262-3:2018, 6.5.1). Functional safety concept on item level (see ISO 26262-3:2018, 7.5.1). Functional safety concept on system level (see 6.5.1); System architectural design specification (see 6.5.2). Hardware-software interface specification (HSI) (see 6.5.3). | 7.5.1 Integration and test strategy resulting from requirements in 7.4.1. 7.5.2 Verification report for integration and test strategy resulting from requirements in 7.4.1. 7.5.3 Integration and test report resulting from requirements in 7.4.2, 7.4.3 and ISO 26262- 3:2018, Clause 8. |
|  | a) to define the integration steps and to integrate the system elements until the system is fully integrated; b) to verify that the defined safety measures, resulting from safety analyses at the system architectural level, are properly implemented; and c) to provide evidence that the integrated system elements fulfil their safety requirements according to the system architectural design. |  |  |



<!-- Page 34 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
25 
Annex B
787 
(informative)
788 
 
789 
Example contents of hardware-software interface (HSI) 
790 
B.1 General
791 
This annex provides further explanation on the HSI. 
792 
The specification of the HSI is initiated during the activities described in Clause 6 “Functional safety concept 
793 
on system level”. The HSI specification is refined as development continues through the hardware and 
794 
software development.
795 
Figure B.1 is an overview of the role of the HSI and its relationship between product development at the 
796 
system, hardware and software level. The HSI is used to agree technical dependencies between hardware and 
797 
software development.
798 
Within the figure, the specific clauses of each part of ISO 26262 are indicated in the following manner: “m-n”, 
799 
where “m” represents the number of the part and “n” indicates the number of the clause, e.g. “3-6” represents ISO 26262-
800 
3:2018, Clause 6.
801 
 
802 
Figure B.1 — Overview of the interactions of the hardware-software interface (HSI) 
803 
B.2 HSI elements
804 
To aid the specification of the HSI, the following HSI elements can be considered: 
805 
a) memory:
806 
1) volatile memory (e.g. RAM);
807 
2) non-volatile memory (e.g. NvRAM);
808 


<!-- Page 35 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
26 
b) bus interfaces [e.g. controller area network (CAN), local interconnect network (LIN), internal high-speed 
809 
serial link (HSSL)];
810 
c) converter:
811 
1) A/D converter;
812 
2) D/A converter;
813 
3) pulse-width modulation (PWM);
814 
d) multiplexer;
815 
e) electrical I/O;
816 
f)watchdog:
817 
1) internal;
818 
2) external.
819 
B.3 HSI characteristics
820 
To aid the specification of the HSI, the following characteristics of the HSI can be considered: 
821 
a) interrupts;
822 
b) timing consistency;
823 
c) data integrity;
824 
d) initialization:
825 
1) memory and registers;
826 
2) boot management;
827 
e) message transfer:
828 
1) send message;
829 
2) receive message;
830 
f)network modes:
831 
1) sleeping;
832 
2) awakening;
833 
g) memory management:
834 
1) reading;
835 
2) writing;
836 
3) diagnostic;
837 


<!-- Page 36 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
27 
4) address space;
838 
5) data types;
839 
h) real-time counter:
840 
1) start counter;
841 
2) stop counter;
842 
3) freeze counter;
843 
4) load counter.
844 
Table B.1 provides an example to help with the allocation of HSI characteristics to HSI elements. 
845 
 
846 


<!-- Page 37 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
28 
Table B.1 — Example for inputs of internal signals 
DescriptionHW-IdentifierSW-Identifier
el 1el 2No. -el 1No. -el 2
Data typeInterface
1 
2 
Interfacey (% ofrange ofvalues)
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Input 1IN_1IN_1x
 
4 
 
U160x8000
 
V 
-InternalAnalogue Input
1 
0 to 50,50 %
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 


| Descriptio n | HW- Identifier | SW- Identifier | Chann el 1 | Chann el 2 | MUX No. - Chann el 1 | MUX No. - Chann el 2 | Data type HW Interface | Address Channel 1 | Address Channel 2 |  | Interface Type |  | Range of values | Accurac y (% of range of values) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Input 1 | IN 1 _ | IN 1 _ |  |  |  |  | U16 | 0x8000 |  |  | Analogue -Internal | Analogue Input 1 | 0 to 5 | 0,50 % |



<!-- Page 38 -->

ISO/AWI 26262-4:2025(en)© ISO 2025 – All rights reserved
29 
Bibliography[1]
ISO 21448:2022, Road vehicles — Safety of the intended functionality 
[2]
ISO/IEC/IEEE 15288, Systems and software engineering — System life cycle processes 
[3]
ISO/IEC/IEEE 16326, Systems and software engineering — Life cycle processes — Project management 
[4]
ISO 11451 (all parts), Road vehicles — Vehicle test methods for electrical disturbances from 
narrowband radiated electromagnetic energy 
[5]
ISO 11452 (all parts), Road vehicles — Component test methods for electrical disturbances from 
narrowband radiated electromagnetic energy 
[6]
ISO 7637 (all parts), Road vehicles — Electrical disturbances from conduction and coupling 
[7]
ISO 10605, Road vehicles — Test methods for electrical disturbances from electrostatic discharge 
 


