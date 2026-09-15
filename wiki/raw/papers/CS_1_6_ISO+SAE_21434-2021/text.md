<!-- Page 1 -->

Road vehicles — Cybersecurity
engineering
Véhicules routiers — Ingénierie de la cybersécurité
© ISO/SAE International 2021
INTERNATIONAL
STANDARD
ISO/SAE
Reference number
ISO/SAE 21434:2021(E)
First edition


<!-- Page 2 -->


ISO/SAE 21434:2021(E)

© ISO/SAE International 2021 – All rights reserved
COPYRIGHT PROTECTED DOCUMENT
©  ISO/SAE International 2021
conce  in tion      e     
e  in  in  e  in  e  e  in
in  e  in  in


<!-- Page 3 -->


ISO/SAE 21434:2021(E)
Foreword
bodies (ISO member bodies). The work of preparing International Standards is normally carried out
through ISO technical committees. Each member body interested in a subject for which a technical
committee has been established has the right to be represented on that committee. International
e  e  e
ISO collaborates closely with the International Electrotechnical Commission (IEC) on all matters of
are used to advance mobility engineering throughout the world. The SAE Technical Standards
e   e   e   e
The procedures used to develop this document and those intended for its further maintenance are
the different approval criteria needed for the different types of ISO documents should be noted. This
           A e  ʹ I www
.iso. org/ directives).
Attention is drawn to the possibility that some of the elements of this document may be the subject of
patent rights. ISO and SAE International shall not be held responsible for identifying any or all such
the Introduction and/or on the ISO list of patent declarations received (see www. iso. org/ patents).
in  e  e
responsibility of the user.”
Any trade name used in this document is information given for the convenience of users and does not
constitute an endorsement.
in                e          conc    
   II        IIe  www. iso. org/
iso/ foreword. html.
        A ʹʹe Road vehiclese 
  ͵ʹe  Electrical and electronic components and general system aspectse      ͳͺ  Vehicle
Cybersecurity Systems Engineering Committee.
The main changes are as follows:
— complete rework of contents and structure.
complete listing of these bodies can be found at www. iso. org/ members. html e  
   e   https:// www. sae. org/ standards/ content/ ISO/ SAE 21434/.

© ISO/SAE International 2021 – All rights reserved
iii


<!-- Page 4 -->


ISO/SAE 21434:2021(E)
Introduction
Purpose of this document
This document addresses the cybersecurity perspective in engineering of electrical and electronic
document aims to enable the engineering of E/E systems to keep up with state-of-the-art technology
and evolving attack methods.
engineering as a foundation for common understanding throughout the supply chain. This enables
— foster a cybersecurity culture.
This document can be used to implement a cybersecurity management system including cybersecurity
risk management.
Organization of this document
An overview of the document structure is given in Figure 1. The elements of Figure 1 do not prescribe

© ISO/SAE International 2021 – All rights reserved


<!-- Page 5 -->


ISO/SAE 21434:2021(E)
Figure 1 — Overview of this document
Clause 4  I
approach to road vehicle cybersecurity engineering taken in this document.
conc     e   
cybersecurity activities at the project level.
I  in  in
cybersecurity activities between customer and supplier.
Clause 8 (Continual cybersecurity activities) includes activities that provide information for ongoing
support.
Clause 10 I I    c   conce 
Clause 11 (Cybersecurity validation) includes the cybersecurity validation of an item at the vehicle level.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 6 -->


ISO/SAE 21434:2021(E)
Clause 12 II   Ǧ      
an item or component.
Clause 13 (Operations and maintenance) includes activities related to cybersecurity incident response
and updates to an item or component.
Clause 14 (End of cybersecurity support and decommissioning) includes cybersecurity considerations
for end of support and decommissioning of an item or component.
 ͳͷ (Threat analysis and risk assessment methods) includes modular methods for analysis and
  ͷ through ͳͷ        e    I  e  e
that are different from the persons responsible for the cybersecurity activities.
A summary of cybersecurity activities and work products can be found in  .
IW in   e  W in   e  W in   in
Ie  e  e
in  e  e
in  e O e

© ISO/SAE International 2021 – All rights reserved


<!-- Page 7 -->


Road vehicles — Cybersecurity engineering
1 Scope
    conc       in        
e  e  e  e
for communicating and managing cybersecurity risk.
     conc   in    
2 Normative references
in  e  in
 ʹ͸ʹ͸ʹǦ͵ǣʹͲͳͺe Road vehicles — Functional safety — Part 3: Concept phase
ISO Online browsing platform: available at https:// www .iso .org/ obp
IEC Electropedia: available at https:// www .electropedia .org/
architectural design
       in  c    components (͵ͳ͹Ie    e    
interactions
asset
Note 1 to entry: An asset has one or more cybersecurity properties (3.1.20) whose compromise can lead to one or
more damage scenarios (3.1.22).
attack feasibility
attribute of an attack path (3.1.4) describing the ease of successfully carrying out the corresponding set
of actions
INTERNATIONAL STANDARD
ISO/SAE 21434:2021(E)
© ISO/SAE International 2021 – All rights reserved


<!-- Page 8 -->


ISO/SAE 21434:2021(E)
attack path
attack
       threat scenario (3.1.33)
attacker
e e  in      attack path (3.1.4)
audit
e  e  E
component
part that is logically and technically separable
customer
in  in
e  e  E  W in
Wǳe   W    in  in tion     in ǳ  e 
cybersecurity
road vehicle cybersecurity
condition in which assets (3.1.2I  c    threat scenarios (3.1.33) to items
(͵ͳʹͷI   e       in  components (͵ͳ͹)
e  in  e
cybersecurity.
cybersecurity assessment
judgement of cybersecurity (͵ͳͻ)
cybersecurity case
structured argument supported by evidence to state that risks (͵ͳʹͻ) are not unreasonable
cybersecurity claim
statement about a risk (͵ͳʹͻ)
in  in
cybersecurity concept
        item (͵ͳʹͷI          operational environment
(͵ͳʹ͸Ie     cybersecurity controls (3.1.14)
cybersecurity control
measure that is modifying risk (͵ͳʹͻ)
[SOURCE: ISO 31000:2018 [3]e ͵ͺe c E   ̶̶     e 

© ISO/SAE International 2021 – All rights reserved


<!-- Page 9 -->


ISO/SAE 21434:2021(E)
cybersecurity event
cybersecurity information (3.1.18) that is relevant for an item (͵ͳʹͷ) or component (͵ͳ͹)
cybersecurity goal
Ǧ       in  threat scenarios (3.1.33)
cybersecurity incident
   c    vulnerability (3.1.38I 
cybersecurity information
information with regard to cybersecurity (͵ͳͻ) for which relevance is not yet determined
cybersecurity interface agreement
agreement between customer (3.1.8) and supplier concerning distributed cybersecurity activities (3.1.23)
cybersecurity property
attribute that can be worth protecting
e  A in
 conc
    architectural design (3.1.1)
damage scenario
      in      road user (3.1.31)
distributed cybersecurity activities
cybersecurity activities for the item (͵ͳʹͷ) or component (͵ͳ͹) whose responsibilities are distributed
between customer (3.1.8) and supplier
impact
estimate of magnitude of damage or physical harm from a damage scenario (3.1.22)
item
component or set of components (͵ͳ͹) that implements a function at the vehicle level
e  e  E  W
1 to entry has been replaced.]
operational environment
Note 1 to entry: Operational use of an item (͵ͳʹͷ) or a component (͵ͳ͹I       e 
e  A in

© ISO/SAE International 2021 – All rights reserved


<!-- Page 10 -->


ISO/SAE 21434:2021(E)
out-of-context
       conc item (͵ͳʹͷ)
penetration testing
cybersecurity testing in which real-world attacks are mimicked to identify ways to compromise
cybersecurity goals (͵ͳͳ͸)
risk
cybersecurity risk
effect of uncertainty on road vehicle cybersecurity (͵ͳͻI     attack feasibility (3.1.3)
and impact (3.1.24)
risk management
           risk (͵ͳʹͻ)
[SOURCE: ISO 31000:2018 [3]e ͵ʹȐ
road user
person who uses a road
e  e  e  e  in
tailore verb
to omit or perform an activity in a different manner compared to its description in this document
threat scenario
potential cause of compromise of cybersecurity properties (3.1.20) of one or more assets (3.1.2) in order
   damage scenario (3.1.22)
triage
analysis to determine the relevance of cybersecurity information (3.1.18) to an item (͵ͳʹͷ) or
component (͵ͳ͹)
trigger
criterion for triage (3.1.34)
validation
ce      e   cybersecurity goals (͵ͳͳ͸) of the
item (͵ͳʹͷI     
Oǣ AA ͳͷʹͺͺǣʹͲͳͷ  [4]e Ͷͳͷ͵e c E   W  in  conc
ce            e    conc      
A A e  e  E

© ISO/SAE International 2021 – All rights reserved


<!-- Page 11 -->


ISO/SAE 21434:2021(E)
vulnerability
weakness (3.1.40I         attack path (3.1.4)
A e  e  E  in
vulnerability analysis
 c    vulnerabilities (3.1.38)
weakness
defect or characteristic that can lead to undesirable behaviour
   in conc
a security protocol.
3.2 Abbreviated terms
CAL
cybersecurity assurance level
CVSS
common vulnerability scoring system
electrical and electronic
ECU
electronic control unit
on-board diagnostic
permission
recommendation
RASIC
e  e  e  e
TARA
threat analysis and risk assessment
work product
4 General considerations
    conc    e      in   
with its operational environment.
The application of this document is limited to cybersecurity-relevant items and components of a series

© ISO/SAE International 2021 – All rights reserved


<!-- Page 12 -->


ISO/SAE 21434:2021(E)
to the vehicle (e.g. back-end servers) can be considered for cybersecurity purposes but are not in the
scope of this document.
This document describes cybersecurity engineering from the perspective of a single item. The suitable
       A        conc 
in  e  in
cases of its cybersecurity-relevant items and components can be considered. If cybersecurity activities
cybersecurity risk is addressed.
throughout all lifecycle phases as illustrated in Figure 2.
Figure 2 — Overall cybersecurity risk management
Cybersecurity risk management is applied throughout the supply chain to support cybersecurity
                conc          
       conc  I  ͸). Development partners for a
conc   in     Ǧ       
performed (see  ͹).
Figure 3      e e    

© ISO/SAE International 2021 – All rights reserved


<!-- Page 13 -->


ISO/SAE 21434:2021(E)
Figure 3 — Relationship between item, function, component and related terms
  ͳͷ describes modular methods for assessment of cybersecurity risk that are invoked in
cybersecurity activities described in other clauses.
performed by abstract adversarial actors with malicious intent and the damage that can arise from
the compromise of cybersecurity of the vehicle E/E systems. Coordination between cybersecurity
conc   I A ͶͺͲͶ [͸]I  e   
response activities complement concept and product development activities as a reactive approach
acknowledging the changing conditions in the environment (e.g. new attack technologies) and the
ongoing need to identify and manage weaknesses and vulnerabilities in road vehicle E/E systems.
A defence-in-depth approach can be used to mitigate cybersecurity risk. The defence-in-depth approach
the assets.
5 Organizational cybersecurity management
5.1 General
      con    
that are independently audited against the objectives of this document.
e   in
5.2 Objectives
The objectives of this clause are to:
I   in
I                  tion    

© ISO/SAE International 2021 – All rights reserved


<!-- Page 14 -->


ISO/SAE 21434:2021(E)
I   e   e
5.3 Inputs
Prerequisites
None.
Further supporting information
The following information can be considered:
e   e   e
A e  A A A A
5.4 Requirements and recommendations
Cybersecurity governance
NOTE 2
The cybersecurity policy can include a statement regarding the risk treatment of generic threat
in   e   e
e  e  e
e  e  e  e  e
e   e   e   e
  conc     ʹͻͳͶ͹ [14].
the convenience of users of this document and does not constitute an endorsement by ISO of these products.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 15 -->


ISO/SAE 21434:2021(E)
Figure 4         I OǦͲͷǦͲͳȐIe 
Ǧconc     I OǦͲͷǦͲʹȐIe  I OǦͲͷǦͲ͵ȐI 
Figure 4 — Cybersecurity governance
in   e   e
incident management.
RQ- e  in  e
and establish and maintain communication channels between those disciplines in order to:
E   I e  I
E   I e
E   in  I
Cybersecurity culture
NOTE 1
See    in 

© ISO/SAE International 2021 – All rights reserved


<!-- Page 16 -->


ISO/SAE 21434:2021(E)
E   e
— known attack methods and cybersecurity controls.
NOTE 3
Continuous improvement applies to all cybersecurity activities in this document.
Information sharing
   tione e  in e   in    
NOTE
Circumstances to share information can be based on:
E   in
E   in
E   in
E      in conc Ǣ
E   in
e  e  e
Management systems
e  in  e  e
NOTE 1
The scope of change management in cybersecurity is to manage changes in items and their
review of the changes in production processes against the production control plan to prevent such changes
from introducing new vulnerabilities.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 17 -->


ISO/SAE 21434:2021(E)
NOTE 2
A work product can be combined or mapped to different documentation repositories.
[RQ-05-12]  c  tion  in       
remedial actions.
[RC-05-13] A cybersecurity management system for the production processes should be established in
order to support the activities of Clause 12.
Tool management
RQ- in
in  in  e  e
in  e  in
NOTE
Such management can be established by:
E   in
E   in
— authentication of the tool.
[RC-05-15] An appropriate environment to support remedial actions for cybersecurity incidents (see
13.3) should be reproducible until the end of cybersecurity support for the product.
e   in
vulnerabilities.
Information security management
system.
deletion.
Organizational cybersecurity audit
[RQ-05-17] A cybersecurity audit shall be performed independently to judge whether the
e  in  e

© ISO/SAE International 2021 – All rights reserved


<!-- Page 18 -->


ISO/SAE 21434:2021(E)
e  in  e
in   e
performed periodically.
5.5 Work products
e  e  to
of ͷͶͶ and ͷͶ͸
6 Project dependent cybersecurity management
6.1 General
  in  conc 
         I ͸Ͷͳ) and
planning of the cybersecurity activities (see ͸ͶʹI   c    
applied (see ͸Ͷ͵I         c      
when tailoring can be used include:
— reuse (see ͸ͶͶIe
E   Ie
— use of an off-the-shelf component (see ͸Ͷ͸Ie
— update (see 13.4).
e  e  in  e
introduce vulnerabilities that might not have been considered for the original item or component.
e  e  in
E      e            I  8.3) and/or
cybersecurity event evaluation (see 8.4Ie 
— a change of the assets since the original development.
in  e
in  in
with a rationale.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 19 -->


ISO/SAE 21434:2021(E)
in  in  e  in
 ǦǦ             conc  
in   e
developed in accordance with this document.
into an item or component in accordance with this document. The integration can involve activities
similar to reuse analysis in ͸ͶͶe           
management (see ͷͶͶ) applies. The changes can be made to a component that is intended to be
integrated and/or to the component or item that is the target of the integration.
Figure 5 — Integration of off-the-shelf and out-of-context components
The cybersecurity case (see ͸Ͷ͹) is an input to a cybersecurity assessment and to the release for post-
development.
The cybersecurity assessment (see ͸Ͷͺ) judges independently the cybersecurity of an item or
component and is an input for the decision to the release for post-development (see ͸Ͷͻ).
6.2 Objectives
The objectives of this clause are to:
e) decide whether the item or component can be released for post-development from a cybersecurity
perspective.
6.3 Inputs
Prerequisites
None.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 20 -->


ISO/SAE 21434:2021(E)
Further supporting information
The following information can be considered:
— project plan.
6.4 Requirements and recommendations
Cybersecurity responsibilities
[RQ-06-01] The responsibilities regarding the project’s cybersecurity activities shall be assigned and
NOTE
Responsibilities for cybersecurity activities can be transferred provided that this is communicated
and that the relevant information is made available.
Cybersecurity planning
RQ- in  in  e  in
component shall be analysed to determine:
I   in
NOTE 1
  provides a method and criteria that can be used to assess the cybersecurity relevance.
in   e
I   in   e   in
whether tailoring in accordance with ͸Ͷ͵ is applied.
[RQ-06-03] The cybersecurity plan shall include the:
I   in
I  tion   in   Ǣ
I   in  e
RQ- in   e   in
tracking the progress of the cybersecurity activities against the cybersecurity plan shall be assigned in
[RQ-06-05] The cybersecurity plan shall either be:
I   in
NOTE 3
The cybersecurity plan can incorporate cross-references to other plans (e.g. the project plan) which

© ISO/SAE International 2021 – All rights reserved


<!-- Page 21 -->


ISO/SAE 21434:2021(E)
[RQ-06-06]         con          tion   in  
 ͻe 10e 11 and ͳͷ.
RQ- in
[PM-06-08] For threat scenarios of risk value 1 that are determined from an analysis in accordance
with ͳͷͺe   ͻͷe Clause 10 and Clause 11 may be omitted.
e  e  in
E   conc  c   ǯ   
for accuracy until and at the release for post-development.
cybersecurity plan regarding their respective cybersecurity activities and interfaces in accordance
with  ͹.
e   e   e   e
accordance with ͷͶͶ.
Tailoring
[PM-06-13] A cybersecurity activity may be tailored.
NOTE
Activities that are not performed because they are performed by another entity in the supply chain
e  I  e
cybersecurity activities can lead to joint tailoring (see ͹Ͷ͵).
Reuse
[RQ-06-15] A reuse analysis shall be carried out if an item or component has been developed and:
in   e   in   in
interacting with it (see 	 ͸).

© ISO/SAE International 2021 – All rights reserved


<!-- Page 22 -->


ISO/SAE 21434:2021(E)
Can be changed as a result of the reuse analysis.
Figure 6 — Reuse analysis examples
concerning the item or component.
E   e  in
E   e   in   in
e  e  in  in
[RQ-06-16] A reuse analysis of an item or component shall:
I   in
e  e  e
in  e  in
d) specify the cybersecurity activities necessary to conform with this document in the cybersecurity
plan (see ͸Ͷʹ).
NOTE 4
This can imply tailoring (see ͸Ͷ͵).
[RQ-06-17] A reuse analysis of a component shall evaluate whether:
I   in
I   e  in
component.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 23 -->


ISO/SAE 21434:2021(E)
Component out-of-context
RQ- e   e   in
RQ- in  e
RQ- in  e
Off-the-shelf component
shall be gathered and analysed to determine whether:
I       in  conc      Ǣ 
performed.
NOTE
This can imply tailoring (see ͸Ͷ͵).
Cybersecurity case
[RQ-06-23] A cybersecurity case shall be created to provide the argument for the cybersecurity of the
in  e
work products then that part of the argument can be omitted).
generated by the respective parties. Then the overall argument of the item is supported by arguments from all
parties.
Cybersecurity assessment
[RQ-06-24] A decision whether to perform a cybersecurity assessment for an item or component shall
be made supported by a rationale applying a risk-based approach.
NOTE 1
The rationale can be based on:
— TARA results (see  ͳͷIǢ
E   in
cybersecurity case.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 24 -->


ISO/SAE 21434:2021(E)
[RQ-06-26] The cybersecurity assessment shall judge the cybersecurity of the item or component.
work products (see  ).
cybersecurity assessment and other cybersecurity activities.
Figure 7 — Cybersecurity assessment in relation to other cybersecurity activities
in  e  e
[RQ-06-27] A person responsible to plan and perform independently a cybersecurity assessment shall
[RQ-06-28] A person who carries out a cybersecurity assessment shall have:
b) the cooperation of the personnel performing the cybersecurity activities.
[PM-06-29] A cybersecurity assessment may be based on a judgement of whether the objectives of this
document are achieved.
[RQ-06-30] The scope of a cybersecurity assessment shall include:

© ISO/SAE International 2021 – All rights reserved


<!-- Page 25 -->


ISO/SAE 21434:2021(E)
the appropriateness and effectiveness of implemented cybersecurity controls and cybersecurity
I   e  e
NOTE 10 A person responsible for the creation of a work product can provide a rationale why the
objective of this document.
RQ- in
e  in  in
NOTE 12 The assessment report can also include recommendations for continuous improvement.
RQ- in
then the cybersecurity assessment report shall include the conditions for acceptance.
Release for post-development
[RQ-06-33] The following work products shall be available prior to the release for post-development:
RQ- in  in
or component:
I   in
claims.
6.5 Work products

© ISO/SAE International 2021 – All rights reserved


<!-- Page 26 -->


ISO/SAE 21434:2021(E)
7 Distributed cybersecurity activities
7.1 General
This clause applies if responsibilities for cybersecurity activities for an item or component are
distributed.
This clause describes management of distributed cybersecurity activities and applies to:
all phases where an agreement is applicable to the customer/supplier interface.
component. This is illustrated in Figure 8.
Figure 8 — Use cases for customer/supplier relationships in the supply chain
7.2 Objectives
e   e   in
distributed cybersecurity activities between customers and suppliers.
7.3 Inputs
None.
7.4 Requirements and recommendations
Supplier capability
RQ- e   e
development activities in accordance with this document shall be evaluated.
NOTE 1
This evaluation supports supplier selection and can be based on the supplier’s capability to conform to
e  in  in
with regard to cybersecurity engineering.
record of cybersecurity capability.
NOTE 2
A record of cybersecurity capability can include:
e  e  e  e
— evidence of continual cybersecurity activities (see Clause 8) and cybersecurity incident response (see
Clause 13IǢ 

© ISO/SAE International 2021 – All rights reserved


<!-- Page 27 -->


ISO/SAE 21434:2021(E)
— summary of previous cybersecurity assessment reports.
Request for quotation
RQ- in
with ͹Ͷ͵Ǣ 
A in  in
Alignment of responsibilities
[RQ-07-04] A customer and a supplier shall specify the distributed cybersecurity activities in a
cybersecurity interface agreement including:
NOTE 1
The shared information can include:


in   in   e
results of cybersecurity assessments.
in  in
[RC-07-05] The cybersecurity interface agreement should be mutually agreed upon between customer
and supplier prior to the start of the distributed cybersecurity activities.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 28 -->


ISO/SAE 21434:2021(E)
customer and supplier shall agree on actions and responsibility for those actions.
RQ- e  e  in
appropriate decisions and actions can be taken.
[RC-07-08]     conc     
7.5 Work products
8 Continual cybersecurity activities
8.1 General
Continual cybersecurity activities are performed during all the phases of the lifecycle and can be done
   conc 
Cybersecurity monitoring (see 8.3) collects cybersecurity information and analyses the cybersecurity
Cybersecurity event evaluation (see 8.4) determines if the cybersecurity event presents a weakness for
an item or component.
Vulnerability analysis (see ͺͷI          
Vulnerability management (see ͺ͸I       c  
items and components until their end of cybersecurity support.
8.2 Objectives
The objectives of this clause are to:
I   in
8.3 Cybersecurity monitoring
Inputs
Prerequisites
The following information shall be available:
E   in

© ISO/SAE International 2021 – All rights reserved


<!-- Page 29 -->


ISO/SAE 21434:2021(E)
Further supporting information
The following information can be considered:
E   conc OǦͳͲǦͲͳȐǢ
Requirements and recommendations
[RQ-08-01] Sources shall be selected for collection of cybersecurity information.
NOTE 2
Internal sources can include those listed in 8.3.1.2.
E   in
— government sources.
RQ- in
e   in   e   in
suppliers.
[RQ-08-03] Cybersecurity information shall be collected and triaged to determine if the cybersecurity
information becomes one or more cybersecurity events.
Work products
in  e

© ISO/SAE International 2021 – All rights reserved


<!-- Page 30 -->


ISO/SAE 21434:2021(E)
8.4 Cybersecurity event evaluation
Inputs
Prerequisites
The following information shall be available:
E   in  e
Further supporting information
The following information can be considered:
E   conc OǦͳͲǦͲͳȐǢ
Requirements and recommendations
[RQ-08-04] A cybersecurity event shall be evaluated to identify weaknesses in an item and/or
component.
   Ie       I ͺ͸) as an assumed vulnerability
without any other activity.
Work products
8.5 Vulnerability analysis
Inputs
Prerequisites
The following information shall be available:
E   c OǦͲͻǦͲͳȐ  in  conc OǦͳͲǦͲͳȐ
 conc           
Further supporting information
The following information can be considered:

© ISO/SAE International 2021 – All rights reserved


<!-- Page 31 -->


ISO/SAE 21434:2021(E)
— information from past cybersecurity incidents.
Requirements and recommendations
NOTE 1
The analysis can include:
— attack path analysis in accordance with ͳͷ͸Ǣ A
— attack feasibility rating in accordance with ͳͷ͹.
NOTE 2
A root cause analysis can be performed to determine any underlying factors that contribute to the
possibility of a weakness being a vulnerability.
vulnerability.
is not treated as a vulnerability.
RQ- in
Work products
8.6 Vulnerability management
Inputs
Prerequisites
The following information shall be available:
Further supporting information
None.
Requirements and recommendations
[RQ-08-07] Vulnerabilities shall be managed such that for each vulnerability:
a) the corresponding cybersecurity risks are assessed and treated in accordance with ͳͷͻ such that
b) the vulnerability is eliminated by applying an available remediation independent of a TARA.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 32 -->


ISO/SAE 21434:2021(E)
in   e
activities (see ͹Ͷ͵e      I      I ͷͶ͵).
[RQ-08-08] If a risk treatment decision in accordance with ͳͷͻ necessitates cybersecurity incident
e  13.3 shall be applied.
NOTE 3
The cybersecurity incident response process can be applied independent of a TARA.
Work products
9 Concept
9.1 General
e        c   W cǳ I ͻ͵). The
      conc       in      I  ͻͶIe            
in   e   e
methods of  ͳͷ (see also  e Figure H.1I  e ͻͶ conc  e
The cybersecurity concept (see ͻͷI              
comprehensive view of the item.
9.2 Objectives
The objectives of this clause are to:
I  con     Ǣ 
specify the cybersecurity concept to achieve cybersecurity goals.
Inputs
Prerequisites
None.
Further supporting information
The following information can be considered:

© ISO/SAE International 2021 – All rights reserved


<!-- Page 33 -->


ISO/SAE 21434:2021(E)
Requirements and recommendations
NOTE 1
The item boundary distinguishes the item from its operational environment. The description of
the item boundary can include interfaces with other items internal to the vehicle and/or with E/E systems
NOTE 2
This describes the intended behaviour of the item during the lifecycle phases [e.g. product
Ie  e  e
preliminary architecture.
  ce con   e         
(generic) item and description of the functions of the components within the item.
[RQ-09-02] Information about the operational environment of the item relevant to cybersecurity shall
be described.
identifying and/or analysing relevant threat scenarios and attack paths.
Work products
9.4 Cybersecurity goals
Inputs
Prerequisites
The following information shall be available:
Further supporting information
The following information can be considered:

© ISO/SAE International 2021 – All rights reserved


<!-- Page 34 -->


ISO/SAE 21434:2021(E)
Requirements and recommendations
impact rating in accordance with ͳͷͷǢ
d) attack path analysis in accordance with ͳͷ͸Ǣ
e) attack feasibility rating in accordance with ͳͷ͹Ǣ 
risk value determination in accordance with ͳͷͺ.
assumed.
RQ- e  in
threat scenario in accordance with ͳͷͻ.
NOTE 2
Avoiding a risk by removing the risk source can lead to change in the item in accordance with change
management (see ͷͶͶ).
RQ- in  e  in
      conc
    conc  in      
[RQ-09-06] If the risk treatment decision for a threat scenario includes:
I   in
   in       conc
I   e
item.
Work products

© ISO/SAE International 2021 – All rights reserved


<!-- Page 35 -->


ISO/SAE 21434:2021(E)
in  e
9.5 Cybersecurity concept
Inputs
Prerequisites
The following information shall be available:
Further supporting information
The following information can be considered:
Requirements and recommendations
[RQ-09-08] Technical and/or operational cybersecurity controls and their interactions to achieve the
b) cybersecurity claims.
NOTE 1
The description can include:
E   in  e  e
E          conc        e            
channel.
NOTE 2
The description can serve to evaluate designs and to determine targets for cybersecurity validation.
       in e conc    e   
capabilities or the capability to obtain user consent during operations.
achieved.
RQ- e  in
more of its components.
              conc      
the cybersecurity concept.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 36 -->


ISO/SAE 21434:2021(E)
RQ- e O
I   e  e
b) consistency with respect to cybersecurity claims.
Work products
e  e O
10 Product development
10.1 General
    conc        I
     conc  c  c  c
ce  10.4.1 corresponds to the left side of the V-model and 10.4.2 corresponds to the right

© ISO/SAE International 2021 – All rights reserved


<!-- Page 37 -->


ISO/SAE 21434:2021(E)
Key
 Ǧ   c    conc   
level of architectural abstraction during design as described in 10.4.1.
   conc    10.4.2.
Figure 9 — Example of product development activities in the V-model
Development approaches or methods that differ from the V-model (e.g. agile software development) can
be applied.
CAL can be used to scale the depth and rigour of the activities in this clause and the methods used for
them (see  ).
10.2 Objectives
The objectives of this clause are to:
I  c  concǢ
    conc  Ǧ      
I     c  conc     conc
NOTE 2
Vulnerability analysis and management are described in Clause 8.
d) provide evidence that the results of the implementation and integration of components conform to
  conc

© ISO/SAE International 2021 – All rights reserved


<!-- Page 38 -->


ISO/SAE 21434:2021(E)
10.3 Inputs
10.3.1 Prerequisites
The following information shall be available:
E   conc       OǦͳͲǦͲͳȐǢ
  conc     Ǣ
information assumed on the operational environment of the component under development.
ͲͻǦͲ͸Ȑ  in      c OǦͲͻǦͲͳȐ       conc
from higher levels of architectural abstraction.
10.3.2 Further supporting information
The following information can be considered:
— known weaknesses and vulnerabilities from reused components.
10.4 Requirements and recommendations
10.4.1 Design
[RQ-10-01]   conc   c  ǣ
I   conc      Ǣ
I   in  e
in  in
NOTE 1
Cybersecurity controls can be selected from trusted catalogues.
 conc   conc    Ǧ  
 c  conce    Ǧ 
    conc        c    c    
in  e  in

© ISO/SAE International 2021 – All rights reserved


<!-- Page 39 -->


ISO/SAE 21434:2021(E)
architectural design.
conce  
in   e
maintaining cybersecurity throughout production.
RQ- e  in  in  in
conc  in  e          
or language:
I   in  e
I   in
resilience of the language against vulnerabilities due to its improper use.
RQ- I   in   e   in   in
   ǣʹͲͳʹ [ͳ͹] or CERT C [18]  in     Wǳ  
[RC-10-06] Established and trusted design and implementation principles should be applied to avoid
in  in
NOTE 8
Known weaknesses and vulnerabilities from reused components can be considered.
in   I
managed (see ͺ͸I e c          
without performing a vulnerability analysis.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 40 -->


ISO/SAE 21434:2021(E)
[RQ-10-08]   c    conc      c      e
e      conc     
abstraction.
— prototyping.
  c  c  conc
[RQ-10-10]     c   OǦͳͲǦͲͻȐ   conc ǣ
I   c  concǢ
I   in  e
c            conc      c  
concǢ 
I   e  e
— static analysis.
E   in
E   in
e  in  in
in  in
E   in  in

© ISO/SAE International 2021 – All rights reserved


<!-- Page 41 -->


ISO/SAE 21434:2021(E)
in   e   in
software.
— penetration testing.
in   I
managed (see ͺ͸I e c          
without performing a vulnerability analysis.
provided.
— capabilities to (directly or indirectly) access the component in combination with compromise of other
— simplicity of the component.
10.5 Work products
 conce   OǦͳͲǦͲͳȐ  OǦͳͲǦͲʹȐ
e   in
c   in   conce   OǦͳͲǦͲͺȐ
  c conce   OǦͳͲǦͳͲȐ
e  e O
11 Cybersecurity validation
11.1 General
This clause describes activities for cybersecurity validation at the vehicle level for the item (see
 ͻ). The item is considered in its operational environment at the vehicle level along with the

© ISO/SAE International 2021 – All rights reserved


<!-- Page 42 -->


ISO/SAE 21434:2021(E)
11.2 Objectives
The objectives of this clause are to:
11.3 Inputs
11.3.1 Prerequisites
The following information shall be available:
E   e
11.3.2 Further supporting information
The following information can be considered:
— work products from product development (see ͳͲͷ).
11.4 Requirements and recommendations
RQ- in   in
addressed in accordance with ͻͶ.
NOTE 2
Validation activities can include:
E  c            ͻͷ and Clause 10Ǣ
E       c   ͻ and 10.
NOTE 3
CAL can be used to scale the depth and rigour of the penetration testing (see  ).
(see ͺͷI  c    I ͺ͸).
[RQ-11-02] A rationale for the selection of validation activities shall be provided.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 43 -->


ISO/SAE 21434:2021(E)
11.5 Work products
12 Production
12.1 General
in  e
are applied to the item or component and to ensure that vulnerabilities cannot be introduced during
production.
12.2 Objectives
The objectives of this clause are to:
I   in
b) prevent the introduction of vulnerabilities during production.
12.3 Inputs
12.3.1 Prerequisites
The following information shall be available:
E   in
E   in
12.3.2 Further supporting information
None.
12.4 Requirements and recommendations
RQ- in
post-development.
NOTE 1
The production control plan can be included as part of an overall production plan.
[RQ-12-02] The production control plan shall include:
I   in
I   in

© ISO/SAE International 2021 – All rights reserved


<!-- Page 44 -->


ISO/SAE 21434:2021(E)
in  e
can use privileged access. Such access can introduce vulnerabilities in the item or component if used in an
[RQ-12-03] The production control plan shall be implemented.
12.5 Work products
13 Operations and maintenance
13.1 General
This clause describes cybersecurity incident response (see 13.3) and updates (see 13.4) to items or
management (see ͺ͸).
Updates are changes made to an item or component during post-development and can include additional
e   conce  e     
in   e   in   e
improvements. The work products concerning updates are documented as work products of other
clauses.
in   e   in
phases are covered by change management (see ͷͶͶ) instead of this clause.
13.2 Objectives
The objectives of this clause are to:
I   in
b) maintain cybersecurity during and after updates to items or components after production until
their end of cybersecurity support.
13.3 Cybersecurity incident response
13.3.1 Inputs
13.3.1.1 Prerequisites
None.
13.3.1.2 Further supporting information
The following information can be considered:
— cybersecurity information related to the vulnerability that caused the cybersecurity incident

© ISO/SAE International 2021 – All rights reserved


<!-- Page 45 -->


ISO/SAE 21434:2021(E)
13.3.2 Requirements and recommendations
RQ- in  e
that includes:
NOTE 1
Remedial actions are determined by vulnerability management in ͺ͸.
e  e  e  e  e
I e e   e I    conc   in
these audiences.
NOTE 4
Those responsible can have:
in  e
e  e  e
decision authority.
I   in
e  in
end-user complaints.
I   in
percentage of items or components affected by remedial actions.
g) actions for the closure.
[RQ-13-02] The cybersecurity incident response plan shall be implemented.
13.3.3 Work products

© ISO/SAE International 2021 – All rights reserved


<!-- Page 46 -->


ISO/SAE 21434:2021(E)
13.4 Updates
13.4.1 Inputs
13.4.1.1 Prerequisites
The following information shall be available:
E   in
13.4.1.2 Further supporting information
The following information can be considered:
E   in
13.4.2 Requirements and recommendations
[RQ-13-03] Updates and update-related capabilities within the vehicle shall be developed in accordance
with this document.
13.4.3 Work products
None.
14 End of cybersecurity support and decommissioning
14.1 General
in  in  e  in
those implications are considered separately.
of this document.
End of cybersecurity support and decommissioning are considered in the concept and product
development phases.
14.2 Objectives
The objectives of this clause are to:
b) enable decommissioning of items and components with regard to cybersecurity.
14.3 End of cybersecurity support
14.3.1 Inputs
None.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 47 -->


ISO/SAE 21434:2021(E)
14.3.2 Requirements and recommendations
to end cybersecurity support for an item or component.
customers.
NOTE 2
Communication to vehicle owners can be delivered by an announcement.
14.3.3 Work products
14.4 Decommissioning
14.4.1 Inputs
14.4.1.1 Prerequisites
The following information shall be available:
E   in
14.4.1.2 Further supporting information
None.
14.4.2 Requirements and recommendations
RQ- in
shall be made available.
decommissioning with regard to cybersecurity.
14.4.3 Work products
None.
15 Threat analysis and risk assessment methods
15.1 General
scenario. These methods and their work products are collectively known as a threat analysis and risk
of an item or component:
— impact rating (see ͳͷͷIǢ
— attack path analysis (see ͳͷ͸IǢ

© ISO/SAE International 2021 – All rights reserved


<!-- Page 48 -->


ISO/SAE 21434:2021(E)
— attack feasibility rating (see ͳͷ͹IǢ
— risk value determination (see ͳͷͺIǢ 
— risk treatment decision (see ͳͷͻ).
of work products produced by other clauses.
See    in         
 conc   in  e        
15.2 Objectives
The objectives of this clause are to:
g) select appropriate risk treatment options for threat scenarios.
15.3.1 Inputs
15.3.1.1 Prerequisites
The following information shall be available:
15.3.1.2 Further supporting information
The following information can be considered:
E   conc OǦͳͲǦͲͳȐ
15.3.2 Requirements and recommendations
NOTE 1
A damage scenario can include:
— relevant assets.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 49 -->


ISO/SAE 21434:2021(E)
[RQ-15-02] Assets with cybersecurity properties whose compromise leads to a damage scenario shall
integrity. The damage scenario is collision with following vehicle (rear-end collision) caused by unintended full
braking when the vehicle is travelling at high speed.
15.3.3 Work products
15.4.1 Inputs
15.4.1.1 Prerequisites
The following shall be available:
15.4.1.2 Further supporting information
The following information can be considered:
E   conc OǦͳͲǦͲͳȐǢ
15.4.2 Requirements and recommendations
— cause of compromise of the cybersecurity property.
in   e
e  e  e  e
in  A in

© ISO/SAE International 2021 – All rights reserved


<!-- Page 50 -->


ISO/SAE 21434:2021(E)
E   A in
— threat modelling approaches based on frameworks such as EVITA [20]e  [21]e  [22]e  Ice
e  e  e  e
NOTE 3
A damage scenario can correspond to multiple threat scenarios and a threat scenario can lead to
multiple damage scenarios.
thereby to loss of integrity of the braking function.
15.4.3 Work products
15.5 Impact rating
15.5.1 Inputs
15.5.1.1 Prerequisites
The following shall be available:
15.5.1.2 Further supporting information
The following information can be considered:
15.5.2 Requirements and recommendations
RQ- in
e c e  e  e 	e  e  I
NOTE 1
This document does not provide relationships (e.g. weighting) between different impact categories.
NOTE 2
Additional impact categories can be considered.
can be shared in the supply chain in accordance with  ͹.
[RQ-15-05] The impact rating of a damage scenario shall be determined for each impact category to be
one of the following:
— negligible.
Table F.1 in  	 can be used for mapping safety impact criteria to impact ratings.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 51 -->


ISO/SAE 21434:2021(E)
in  in
[PM-15-07] If a damage scenario results in an impact rating and an argument can be made that every
category may be omitted.
damage scenario is not further analysed.
15.5.3 Work products
15.6 Attack path analysis
15.6.1 Inputs
15.6.1.1 Prerequisites
The following information shall be available:
E   c OǦͲͻǦͲͳȐ  in  conc OǦͳͲǦͲͳȐǢ 
 conc            
15.6.1.2 Further supporting information
The following information can be considered:
15.6.2 Requirements and recommendations
[RQ-15-08] The threat scenarios shall be analysed to identify attack paths.
NOTE 1
An attack path analysis can be based on:
— top-down approaches that deduce attack paths by analysing the different ways in which a threat scenario
attack path can be stopped.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 52 -->


ISO/SAE 21434:2021(E)
attack path.
     e       in   conc
                      conc      
analysis.
E   in
and thereby to loss of integrity of the braking function.
15.6.3 Work products
15.7 Attack feasibility rating
15.7.1 Inputs
15.7.1.1 Prerequisites
The following information shall be available:
15.7.1.2 Further supporting information
The following information can be considered:
15.7.2 Requirements and recommendations
RQ- in   e
Table 1.
Table 1 — Attack feasibility ratings and respective descriptions
Attack feasibility
rating
Description
High
Medium
Low
Very low

© ISO/SAE International 2021 – All rights reserved


<!-- Page 53 -->


ISO/SAE 21434:2021(E)
approaches:
attack vector-based approach.
NOTE 1
Selection of the approach can depend upon the phase in the lifecycle and available information.
determined based on core factors including:
I  con Ǣ
NOTE 3

ʹ provides guidelines on determining attack feasibility based on attack potential.
 tionǢ 
d) user interaction.
NOTE 4

͵ provides guidelines on determining attack feasibility based on a CVSS-based approach.
determined based on evaluating the predominant attack vector (cf. CVSS [24] 2.1.1) of the attack path.

Ͷ provides guidelines on determining attack feasibility based on an attack vector-based approach.
 conc  e   Ǧ        
15.7.3 Work products
15.8 Risk value determination
15.8.1 Inputs
15.8.1.1 Prerequisites
The following information shall be available:

© ISO/SAE International 2021 – All rights reserved


<!-- Page 54 -->


ISO/SAE 21434:2021(E)
15.8.1.2 Further supporting information
None.
15.8.2 Requirements and recommendations
[RQ-15-15] For each threat scenario the risk value shall be determined from the impact of the
associated damage scenarios and the attack feasibility of the associated attack paths.
NOTE 1
If a threat scenario corresponds to more than one damage scenario and/or an associated damage
each of those impact ratings.
ratings of the corresponding attack paths.
RQ- I  e
a value of 1 represents minimal risk.
— risk formulas.
15.8.3 Work products
15.9 Risk treatment decision
15.9.1 Inputs
15.9.1.1 Prerequisites
The following information shall be available:
15.9.1.2 Further supporting information
The following information can be considered:
E   conc OǦͳͲǦͲͳȐǢ
E   in  e  in  in

© ISO/SAE International 2021 – All rights reserved


<!-- Page 55 -->


ISO/SAE 21434:2021(E)
15.9.2 Requirements and recommendations
RQ- in   e   e   in
treatment option(s) shall be determined:
activity that gives rise to the risk.
d) retaining the risk.
NOTE
The rationales for retaining the risk and sharing the risk are recorded as cybersecurity claims and are
subject to cybersecurity monitoring and vulnerability management in accordance with Clause 8.
15.9.3 Work products

© ISO/SAE International 2021 – All rights reserved


<!-- Page 56 -->


ISO/SAE 21434:2021(E)
Annex A
(informative)

Summary of cybersecurity activities and work products
A.1 General
Table A.1 provides a summary of the cybersecurity activities and their corresponding work products.
activities are thus in the scope of a cybersecurity assessment. All work products listed from  ͳͷ
are documented as work products in other clauses.
A.2 Overview of cybersecurity activities and work products
Table A.1 — Cybersecurity activities and work products of this document
Sub-clauses
Work products
Organizational cybersecurity management
ͷͶͳ Cybersecurity governance
ͷͶʹ Cybersecurity culture
management and continuous improvement
ͷͶ͵ Information sharing
ͷͶͷ Tool management
ͷͶ͸ Information security management OǦͲͷǦͲ͵Ȑ     ǯ  
Project dependent cybersecurity management
͸Ͷͳ Cybersecurity responsibilities
͸Ͷʹ Cybersecurity planning
͸Ͷ͵ Tailoring
͸ͶͶ Reuse
͸Ͷ͸ Off-the-shelf component
͸Ͷ͹ Cybersecurity case
͸Ͷͺ Cybersecurity assessment
͸Ͷͻ Release for post-development
Distributed cybersecurity activities
͹Ͷͳ Supplier capability
None
None
͹Ͷ͵ Alignment of responsibilities
Continual cybersecurity activities

© ISO/SAE International 2021 – All rights reserved


<!-- Page 57 -->


ISO/SAE 21434:2021(E)
Sub-clauses
Work products
8.3 Cybersecurity monitoring
8.4 Cybersecurity event evaluation
ͺͷ Vulnerability analysis
ͺ͸ Vulnerability management
Concept phase
ͻͶ Cybersecurity goals
ͻͷ Cybersecurity concept
Product development phase
10.4.1 Design
OǦͳͲǦͲͳȐ   conc
programming languages and coding guidelines
OǦͳͲǦͲͶȐ  c   in   conc
OǦͳͲǦͲ͸Ȑ    c conc
Clause 11 Cybersecurity validation
Post-development phases
Clause 12 
13.3 Cybersecurity incident response
13.4 Updates
None
14.3 End of cybersecurity support
support
14.4 Decommissioning
None
Threat analysis and risk assessment methods
ͳͷͷ Impact rating
ͳͷ͸ Attack path analysis
ͳͷ͹ Attack feasibility rating
ͳͷͺ Risk value determination
ͳͷͻ Risk treatment decision

Table A.1 (continued)
© ISO/SAE International 2021 – All rights reserved


<!-- Page 58 -->


ISO/SAE 21434:2021(E)
Annex B
(informative)

Examples of cybersecurity culture
Table B.1 — Examples of weak and strong cybersecurity culture
Examples indicative of a
weak cybersecurity culture
Examples indicative of a
strong cybersecurity culture
Accountability for decisions related to cybersecurity is
not traceable.
The process ensures that accountability for decisions
related to cybersecurity is traceable.
in  Ie
cost or schedule take precedence over cybersecurity.
Cybersecurity and safety have the highest priority.
The reward system favours cost and schedule over cy-
bersecurity.
The reward system supports and motivates the effective
Cybersecurity personnel force inappropriate and very
strict adherence to cybersecurity without considering
conc   A
Cybersecurity personnel act as role models with a good
sense for appropriateness and practical implementation
the appropriate degree of independence in cybersecurity
assessment.
— heavy dependence on testing at the end of the
— not being prepared for potential weaknesses or
— management reacting only when there is a
or if there is a lot of attention in the media about
competitor products.

— cybersecurity issues are discovered and resolved
from the earliest stage in the product lifecycle
 tion   in      tion   in   
Skilled resources have the competence commensurate
with the activity assigned.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 59 -->


ISO/SAE 21434:2021(E)
Examples indicative of a
weak cybersecurity culture
Examples indicative of a
strong cybersecurity culture
acceptance or conformity to prevailing points of
view).
desired outcome) when forming review groups to
prevent potential dissention.
E   in
person).
reviews.
E   in
e W in
repercussion.
The process uses diversity to its advantage:
— behaviour which counters the use of diversity is
The supporting communication and decision-making chan-
— responsible disclosure by anyone (internal or
— the discovery and resolution process continues in
other products.
ing cycles or other forms of lessons learned.
Continuous improvement is integral to all processes.

Table B.1 (continued)
© ISO/SAE International 2021 – All rights reserved


<!-- Page 60 -->


ISO/SAE 21434:2021(E)
Annex C
(informative)

Example of cybersecurity interface agreement template
C.1 General
e   e   in
cybersecurity activities between customer and supplier (Figure C.1).
methods or tools for collaborations.
C.2 Example template
a) Phaseǣ    Ǣ
b) Work product: work products of this document that are related to the interface of the distributed
Doc refǣ     Ǣ
d) Supplierǣ    Ǣ
e) Customerǣ    Ǣ
                     in  conc  
activity.
and

© ISO/SAE International 2021 – All rights reserved


<!-- Page 61 -->


ISO/SAE 21434:2021(E)
public: the work product can be shared without any restrictions.
g) Comment: additional information concerning results of negotiation and discussion between
Figure C.1 — Example of a cybersecurity interface agreement template

© ISO/SAE International 2021 – All rights reserved


<!-- Page 62 -->


ISO/SAE 21434:2021(E)
Annex D
(informative)

Cybersecurity relevance – example methods and criteria
D.1 General
D.2 Methods
The cybersecurity relevance of a candidate item or component can be determined using the decision
diagram in Figure D.1    

© ISO/SAE International 2021 – All rights reserved


<!-- Page 63 -->


ISO/SAE 21434:2021(E)

in  e  in
data.
e  e  Ie
in  Ie
Figure D.1 — Cybersecurity relevance example method and criteria

© ISO/SAE International 2021 – All rights reserved


<!-- Page 64 -->


ISO/SAE 21434:2021(E)
Annex E
(informative)

Cybersecurity assurance levels
E.1 General
 con       e        
c    con    in  e  
 e   conc     tion     
E.2 Determining a CAL
     e        conce e
in  e
between a CAL and associated risk is illustrated in Figure E.1.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 65 -->


ISO/SAE 21434:2021(E)
Key
 ͳǣ    conc
Event 2: cybersecurity control is implemented.
Event 3: test shows cybersecurity control is effective.
CAL is determined and assigned.
CAL is applied in cybersecurity activities.
          conce   in 
       1 given the criticality of the assets to be protected prescribes
Figure E.1 — Relationship between a CAL and risk
          c   I ͳͷͶ). Table E.1
Table E.1 — Example CAL determination based on impact and attack vector parameters

Attack vectorb
Physical
Local
Adjacent
Network
Impact
Severe
CAL2
CAL3
CAL4
CAL4
CAL1
CAL2
CAL3
CAL4
CAL1
CAL1
CAL2
CAL3
Negligible
Attack vector is a static parameter of attack feasibility.
Sharing a documented rationale for the determination of a CAL between customer and supplier can
the cybersecurity interface agreement between customer and supplier.
A single CAL can be assigned to all cybersecurity goals of an item or different CALs can be assigned
assigned to the combined cybersecurity goal.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 66 -->


ISO/SAE 21434:2021(E)
E.3 Using a CAL
E.3.1 General considerations
  e          tion 
A CAL can be used to select:
I   in
approaches for cybersecurity assessment.
Table E.2            in     
in   e   e
        Tables E.2e  E.3 and E.4 are provided to enable industry
Table E.2 — Example number of CALs and expected rigour in cybersecurity assurance
measures
CAL
Description
a) Methods to provide con-
activities are performed
with appropriate rigour
b) Methods to provide
aged vulnerabilities do
not remain
c) Independence scheme
that the cybersecurity
activities performed are
appropriate
CAL1
Low to moderate cy-
bersecurity assur-
  tion
   Activities such as analysis
and/or testing to search
for vulnerabilities based on
known information
Not needed
CAL2
curity assurance is
tion
Cybersecurity assessments
are carried out by a different
person than the originator
CAL3
bersecurity assur-
  tion
All interactions between
components are tested
Activities such as analysis
and/or testing to search for
tory methods
Cybersecurity assessments
are carried out by a person
in a different team than the
originator
CAL4
High cybersecurity
  tion
All combinations of interac-
tions between components
are tested
Cybersecurity assessments
are carried out by a person
who is independent regard-
and release authority from
the originating department
E.3.2 Concept

© ISO/SAE International 2021 – All rights reserved


<!-- Page 67 -->


ISO/SAE 21434:2021(E)
E.3.3 Product development
methods and measures.
Tables E.3 and E.4              Ǣ
further cybersecurity activities can be addressed in a similar way.
Table E.3                
which the respective activities are performed.
Table E.3 — Example of level of independence of cybersecurity activities
Activity
Require-
ments
Level of independence
applies toa
Scope
CAL1
CAL2
CAL3
CAL4
cept and design activities
Applies to the highest CAL among
and integration of components
Cybersecurity validation
Cybersecurity assessment


I1: the activity is performed by a different person in relation to the person(s) responsible for the creation of the


I2: the activity is performed by a person who is independent from the team that is responsible for the creation of the


from the department responsible for the creation of the considered work product(s).
Table E.4              c 

© ISO/SAE International 2021 – All rights reserved


<!-- Page 68 -->


ISO/SAE 21434:2021(E)
Table E.4 — Example of parameters of testing methods
Activity
Require-
ments
Testing parameters apply
toa
Scope
CAL1 CAL2 CAL3 CAL4
Functional testing
Applies to the highest CAL among the cyberse-
Vulnerability scan-
ning


T1:  testing parameter set 1:
E  e  in  A in

T2:  testing parameters set 2:
E  A in
E  e  in  A in

© ISO/SAE International 2021 – All rights reserved


<!-- Page 69 -->


ISO/SAE 21434:2021(E)
Annex F
(informative)

Guidelines for impact rating
F.1 General
in  I  in
ce       I Table F.1 through Table F.4I    
be used for impact rating.
Considerations on how the scalability of damage (i.e. impact to multiple road users in a single damage
 Ǧconc     I  O20Ȑe ͳʹe  ͶI
F.2 Impact rating for safety damage
Table F.1 — Example safety impact rating criteria
Impact rating
Criteria for safety impact rating
Severe
S2: Severe and life-threatening injuries (survival probable)
S1: Light and moderate injuries
Negligible
S0: No injuries a
Impact rating
Severe
not overcome.
able to overcome.
be able to overcome with limited resources.
Negligible

© ISO/SAE International 2021 – All rights reserved


<!-- Page 70 -->


ISO/SAE 21434:2021(E)
F.4 Impact rating for operational damage
Table F.3 — Example operational impact rating criteria
Impact rating
Criteria for operational impact rating
Severe
The operational damage leads to the loss or impairment of a core vehicle function.
enabling of limp home mode or autonomous driving to an unintended location.
The operational damage leads to the loss or impairment of an important vehicle function.
The operational damage leads to partial degradation of a vehicle function.
Negligible
The operational damage leads to no impairment or non-perceivable impairment of a vehicle
function.
F.5 Impact rating for privacy damage
Table F.4 — Example privacy impact rating criteria
Impact rating
Criteria for privacy impact rating
Severe
The privacy damage leads to serious impact to the road user.
The information regarding the road user is:
The information regarding the road user is:
Negligible

© ISO/SAE International 2021 – All rights reserved


<!-- Page 71 -->


ISO/SAE 21434:2021(E)
Annex G
(informative)

Guidelines for attack feasibility rating
G.1 General
rating (see ͳͷ͹):
— attack vector-based.
and targets) can be included in the rating of attack feasibility.
G.2 Guidelines for the attack potential-based approach
G.2.1 Background on attack potential
in  e
E  con Ǣ
E   in
G.2.2 Example of adaptation of the parameters
G.2.2.1 Example customization of elapsed time
The elapsed time parameter includes the time to identify a vulnerability and develop and (successfully)
see 

© ISO/SAE International 2021 – All rights reserved


<!-- Page 72 -->


ISO/SAE 21434:2021(E)
Table G.1 — Elapsed time
G.2.2.2 Example customization of specialist expertise
Table G.2 — Specialist expertise
Layman:
available.
Knowledgeable in that they are familiar with the security behaviour of the product or system
type.
Expert:
e  e  e  e
e  e  in  e  e
in the product or system type.
Multiple experts:
 c    tion      in     
   tion      in     
G.2.2.3 Example customization of knowledge of the item or component
The knowledge of the item or component parameter is related to the amount of information the attacker
in  e
Table G.3 — Knowledge of the item or component
Public information:
forum.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 73 -->


ISO/SAE 21434:2021(E)
Restricted information:
Restricted information concerning the item or component (e.g. knowledge that is controlled within
 conƤ
 conc I
individual undertaking).
 Ͷ   conc   in       -
facturer and/or supplier.
G.2.2.4 Example customization of window of opportunity
perform an attack. It combines access type (e.g. logical and physical) and access duration (e.g. unlimited
e  e  e
Table G.4 — Window of opportunity
Unlimited:
High availability via public/untrusted network without any time limitation (i.e. asset is always ac-
cessible). Remote access without physical presence or time limitation as well as unlimited physical
access to the item or component.
in  I
unlimited physical access by the owner for chip tuning.
Easy:
High availability and limited access time. Remote access without physical presence to the item or
component.
vehicle standing still.
Moderate:
in  A in
   in  in  in    con 
ical access via on-board diagnostic port.
Very low availability of the item or component. Impractical level of access to the item or component
to perform the attack.
faster than the key is rotated.

Table G.3 (continued)
© ISO/SAE International 2021 – All rights reserved


<!-- Page 74 -->


ISO/SAE 21434:2021(E)
G.2.2.5 Example customization of equipment
A in  e
Table G.5 — Equipment
Standard:
Ie  in  e
analyser or simple attack scripts).
e  e  e  e
Specialized:
Ie  in
   in         con  
tion  in           
    e Ǧ e  Ie con 
Bespoke:
  con  I   I      
 I  Ie  in     con     e -
Multiple bespoke:
     in  e        tion  in
distinct steps of an attack.
G.2.2.6 Example mapping between attack potential and attack feasibility
in  e  A e
Table G.6 — Example aggregation of attack potential
Elapsed time
Specialist exper-
tise
Knowledge of the
item or compo-
nent
Window of oppor-
tunity
Equipment
Enumerate Value
Enumerate Value Enumerate Value Enumerate
Value Enumerate Value
0 Layman
0 Unlimited
0 Standard
3 Restricted
3 Easy
perts
Strictly con-

none
spoke
feasibility is mapped using 

© ISO/SAE International 2021 – All rights reserved


<!-- Page 75 -->


ISO/SAE 21434:2021(E)
Table G.7 — Example attack potential mapping
Attack feasibility rating
Values
High
Low
Very low
G.3 Guidelines for the CVSS-based approach
response and security teams (FIRST) [24]        e  
metrics (cf. Reference [24Ȑe ͹ͳI           I 
E   tionǢ 
— user interaction.
They are described by FIRST [24]. Evaluation of the CVSS metrics yields numerical values for each metric
a simple formula:
E  V  C  P
where


        tione   Ͳeʹ͹  ͲeͺͷǢ 

ͺ. This is an
Table G.8 — Example CVSS exploitability mapping
Attack feasibility rating
CVSS exploitability value
High
Low

© ISO/SAE International 2021 – All rights reserved


<!-- Page 76 -->


ISO/SAE 21434:2021(E)
Attack feasibility rating
CVSS exploitability value
Very low
and Reference [24].
e   in
      Ǧconc      
metric value descriptions.
G.4 Guidelines for the attack vector-based approach
Attack feasibility rating will be higher the more remote (logically and physically) an attacker can be
in  e
Table G.9 — Attack vector-based approach
Attack feasibility rating
Criteria
High
Network:
nected and accessible on the internet.
Medium
Adjacent:
is limited physically or logically.
Low
Local:
Very low
Physical:

Table G.8 (continued)
© ISO/SAE International 2021 – All rights reserved


<!-- Page 77 -->


ISO/SAE 21434:2021(E)
Annex H
(informative)

Examples of application of TARA methods – headlamp system
H.1 General
provided for illustrative purposes only and are not intended to imply any particular approach for
practical use.
particular it addresses:
— TARA.
in  e  in
vii. risk treatment decision.
Figure H.1 provides an overview of various interactions between  ͻ and ͳͷ.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 78 -->


ISO/SAE 21434:2021(E)
Figure H.1 — Interactions in concept phase
H.2 Example activities for concept phase of a headlamp system
headlamp system is given in the following:
a) item boundary (see Figure H.2IǢ
— Functional overview of the item: the headlamp system turns on/off the headlamp in accordance
system switches the headlamp automatically to the low-beam mode when an oncoming vehicle
is detected. It also returns the headlamp automatically to the high-beam mode if the oncoming
vehicle is no longer detected.
navigation ECU and the gateway ECU.
preliminary architecture (see Figure H.2).

© ISO/SAE International 2021 – All rights reserved


<!-- Page 79 -->


ISO/SAE 21434:2021(E)
Figure H.2 — Example of item boundary and preliminary architecture of the headlamp system
operational environment provides supplemental information for analysis activities of the TARA.
Table H.1              
Table H.1 — Example description of the operational environment
navigation ECU by data communication.


— cellular.
Assumption:


Assumption:


OǦͲͻǦͲ͵Ȑ   c    ͳͷ͵ to identify assets of the item and their
damage scenarios. Table H.2      c

© ISO/SAE International 2021 – All rights reserved


<!-- Page 80 -->


ISO/SAE 21434:2021(E)
Table H.2 — Example list of assets and damage scenarios
Asset
Cybersecurity property
Damage scenario
Data communication

driver perceives) the headlamp function was
inhibited while parked.
Front collision with a narrow stationary object
(e.g. a tree) caused by unintended turning-off of
headlamp during night driving at medium speed.
Data communication

(oncoming car information)
caused by not being able to change to low beam
during night driving.
by headlamp always remaining at low beam
during night driving.
Firmware of body control ECU
H.2.3 Impact rating
OǦͲͻǦͲ͵Ȑ        ͳͷͷ to rate the impact of damage scenarios.
Table H.3      
Table H.3 — Example of impact ratings for damage scenarios
Damage scenario
Impact
category
Impact
rating
the headlamp function was inhibited while parked.
Front collision with a narrow stationary object (e.g. a tree) caused
by unintended turning-off of headlamp during night driving at
medium speed.
Severe
remaining at low beam during night driving.
OǦͲͻǦͲ͵Ȑ     c    ͳͷͶ. Table H.4  
Table H.4 — Example threat scenarios
Damage scenario
Threat scenario
Front collision with a nar-
row stationary object (e.g.
a tree) caused by unintend-
ed turning-off of headlamp
during night driving at
medium speed
tially causing the headlamp to turn off unintentionally.
Tampering with a signal sent by body control ECU leads to loss of in-
off unintentionally.
high beam caused by head-
lamp always remaining
at low beam during night
driving
Asset: oncoming car information
Cybersecurity property: availability
Associated cause: denial of service of oncoming car information

© ISO/SAE International 2021 – All rights reserved


<!-- Page 81 -->


ISO/SAE 21434:2021(E)
H.2.5 Attack path analysis
attack path analysis and Figure H.3           
according to the assumption.
Table H.5 — Example attack paths for threat scenarios
Threat scenario
Attack path
integrity of the data communica-
potentially causing the headlamp
to turn off unintentionally
Attacker compromises navigation ECU from cellular interface.
Compromised navigation ECU transmits malicious control signals.
Compromised navigation ECU transmits malicious control signals.
Attacker gets local (see 
Denial of service of oncoming car
information
Attacker compromises navigation ECU from cellular interface.
Compromised navigation ECU transmits malicious control signals.
when vehicle is parking unlocked.
ECU.


© ISO/SAE International 2021 – All rights reserved


<!-- Page 82 -->


ISO/SAE 21434:2021(E)
Figure H.3 — Example of an attack path derived by attack tree analysis
H.2.6 Attack feasibility rating
as described in
attack potential-based approach as described in
Table H.6 — Examples of attack feasibility rating with the attack vector-based approach
Attack path
Attack feasibility
rating
Attacker compromises navigation ECU from cellular interface.
Compromised navigation ECU transmits malicious control signals.
High
Attacker compromises navigation ECU from Bluetooth interface.
Compromised navigation ECU transmits malicious control signals.
Attacker sends malicious control signals from OBD2 connector.

Low
in  e
not possible to gather all vulnerability information related item.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 83 -->


ISO/SAE 21434:2021(E)
Table H.7 — Examples of attack feasibility rating with the attack potential-based approach
Threat
scenario
Attack path
Attack feasibility assessment
KoIC
WoO
Value
Attack
feasibility
rating
Denial of
service of
oncoming
car infor-
mation
Attacker compromises navigation
ECU from cellular interface.
Compromised
navigation
ECU
transmits malicious control signals.
signals to power switch actuator.
bus with a large number of messages.
Low
connector when vehicle is parking
unlocked.
Attacker
compromises
driver’s
interface.
iii. Attacker
sends
message
via


signals to power switch actuator.
bus with a large number of messages.
Low
Key
ET elapsed time
  con 
KoIC
knowledge of the item or component
I   in   e
   tion            
H.2.7 Risk value determination
OǦͲͻǦͲ͵Ȑ      in       ͳͷͺ. Risk values
ratings of impact (see ͳͷͷ) and attack feasibility (see ͳͷ͹) to risk values. Table H.8   
    ͻ        Table H.8.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 84 -->


ISO/SAE 21434:2021(E)
Table H.8 — Risk matrix example

Attack feasibility rating
Very Low
Low
High
Impact rating
Severe
Negligible
Table H.9 — Examples of determined risk values
Threat scenario
Aggregated
attack feasibility
rating
Impact rating
Risk value
of integrity of the data communi-
for power switch actuator ECU
High
Severe
Denial of service of oncoming
car information
Low
in the below formula and Table H.10.
Table H.10 — Example translation of impact and attack feasibility to numerical values
Impact
rating
Numerical value I
for impact

Attack feasibility
rating
Numerical value F for
attack feasibility
Negligible

Very low

Low

Severe

High
in    conc            ͻ              
Table H.8 and the above formula would lead to the same risk values.
H.2.8 Risk treatment decision
OǦͲͻǦͲͶȐ        ͳͷͻ. Table H.11  
results of risk treatment decision.
Table H.11 — Example results of risk treatment decision
Threat scenario
Risk value
Risk treatment option
switch actuator ECU
Reducing the risk
Denial of service of oncoming car information
Reducing the risk

© ISO/SAE International 2021 – All rights reserved


<!-- Page 85 -->


ISO/SAE 21434:2021(E)
BIBLIOGRAPHY
 ʹ͸ʹ͸ʹǦͳǣʹͲͳͺe Road vehicles — Functional safety — Part 1: Vocabulary
 ͻͲͲͲǣʹͲͳͷe Quality management systems — Fundamentals and vocabulary
 ͵ͳͲͲͲǣʹͲͳͺe Risk management — Guidelines
AA ͳͷʹͺͺǣʹͲͳͷe Systems and software engineering — System life cycle processes
A  ʹ͹ͲͲͲǣʹͲͳͺe  Information technology — Security techniques — Information security
management systems — Overview and vocabulary
A ͶͺͲͶe Road vehicles — Safety and cybersecurity for automated driving systems — Design,
	  ͳ͸ͻͶͻe  Quality management system requirements for automotive production and relevant
service parts organizations
 ͻͲͲͳe Quality management systems — Requirements
A ͵͵ͲͲͳe Information technology — Process assessment — Concepts and terminology
AA ͳͷʹͺͺe Systems and software engineering — System life cycle processes
AA ͳʹʹͲ͹e Systems and software engineering — Software life cycle processes

Automotive SPICE Process Assessment /
Reference Model, Version 3.1 OȐ ǣ  e  ʹͲͳ͹  ǣ http:// www
.automotivespice .com/ cA software -download/  ̴ _31 .pdf
 ʹͻͳͶ͹e Information technology — Security techniques — Vulnerability disclosure
 ͸ʹͶͶ͵ǦʹǦͳe Industrial communication networks — Network and system security — Part 2-1:
Establishing an industrial automation and control system security program
 ʹ͸ʹ͸ʹ I Ie Road vehicles — Functional safety
  ʹͲͳʹe Guidelines for the use of the C language in critical systems, 3rd Edition, 1st Revision.
SEI CERT C Coding Standard – Rules for developing safe, reliable and secure systems [online].
e   e   e
[viewed 2021-02-12]. Available at: https:// resources .sei .cmu .edu/ library/ asset -view .cfm ?assetid
  e      IʹͲͳͺIe  Systems Security Engineering: Considerations for a Multidisciplinary
Approach in the Engineering of Trustworthy Secure Systems [online]. (National Institute of
e   Ie   I   e
    ʹͲͳͺ  O  ʹͲʹͳǦͲʹǦͳ͸Ȑ    ǣ  https:// doi .org/ 10 ͸ͲʹͺA NIST  .800
Ǧ	     II  ʹ͵ǣ Security
requirements for automotive on-board networks based on dark-side scenarios [online]. Edited by A.
    ʹͲͲͻ O ʹͲʹͳǦͲͳǦͳ͹Ȑ  ǣ https:// doi .org/ 10 ͷʹͺͳA 

© ISO/SAE International 2021 – All rights reserved


<!-- Page 86 -->


ISO/SAE 21434:2021(E)
ETSI    ͳͲʹ  ͳ͸ͷǦͳe  CYBER; Methods and protocols; Part 1: Method and pro forma for Threat,
Vulnerability, Risk Analysis (TVRA), Version 5.2.3  OȐ    ʹͲͳ͹  O  ʹͲʹͳǦͲͳǦͳͻȐ
Available at: https:// www .etsi .org/ deliver/ etsi _ts/ 102100 ̴ͳͲʹͳͻͻA ͳͲʹͳ͸ͷͲͳA Ͳͷ .02 .03 ̴͸ͲA ts
̴ͳͲʹͳ͸ͷͲͳͲͷͲʹͲ͵ .pdf
ĈĊĉĆĴđĊğe      ĔėĆēĆe      Risk Centric Threat Modeling: Process for Attack
Simulation and Threat Analysis e  ǣ e  ʹͲͳͷ ǣ ͻ͹ͺǦͳǦͳͳͺǦͻͺͺ͵ͷǦ
A  ͳͺͲͶͷe  Information technology — Security techniques — Methodology for IT security
evaluation
[online]. Available at: https:// www c .org/ cvss/ v3 .1/ conc -document
A ʹͻͳͲͲe Information technology — Security techniques — Privacy framework
ĚęĔĒĔęĎěĊ e Automotive Cybersecurity Best Practices [online]. Available at: https:// www
.automotiveisac .com/ best -practices/
I	 I  Ie
 Ǧ  ͷͶe OȐ  ǣ https:// www
c .org/ tlp/
ISO/IEC 23822)e Information technology — Vocabulary
A ͳͷͶͲͺ I Ie Information technology — Security techniques — Evaluation criteria for
IT security
A ʹ͹ͲͲͳe Information technology — Security techniques — Information security management
systems — Requirements
A ʹ͹ͲͳͲe Information technology — Security techniques — Information security management
for inter-sector and inter-organizational communications
AA  ʹ͸ͷͳͳe  Systems and software engineering — Requirements for managers of
information for users of systems, software, and services
 ͵ͳͲͳͲe Risk management — Risk assessment techniques
  ͸ͳͷͲͺǦ͹e  Functional safety of electrical/electronic/programmable electronic safety-related
systems — Part 7: Overview of techniques and measures
 e   IʹͲͳ͸I Guide to Cyber Threat Information Sharing [online]. (National
e  Ie  I
ͳͷͲe  ʹͲͳ͸ O ʹͲʹͳǦͲʹǦͳ͸Ȑ  ǣ https:// doi .org/ 10 ͸ͲʹͺA NIST  .800 ǦͳͷͲ
    	  	    ʹͲͳʹIe  Guide for Conducting Risk
Assessments  OȐ  I          e
e   Ie
http://  .doi .org/ 10 .͸ͲʹͺA NIST  .800 -30r1
 ͵Ͳ͸ͳe Cybersecurity Guidebook for Cyber-Physical Vehicle Systems
	  e      IʹͲͲͺIe  Technical Guide to Information Security Testing and
Assessment  OȐ  I          e
e   Ie
https:// doi .org/ 10 ͸ͲʹͺA NIST  .800 Ǧͳͳͷ
2)  Available at: https:// www .iso .org/ obp/ ui #iso: std: iso -iec: 2382.

© ISO/SAE International 2021 – All rights reserved


<!-- Page 87 -->


ISO/SAE 21434:2021(E)
    Fuzzing for Software Security and Quality Assurance, Second Edition. e

© ISO/SAE International 2021 – All rights reserved


<!-- Page 88 -->


ISO/SAE 21434:2021(E)

Price based on 8ͳ pages
© ISO/SAE International 2021 – All rights reserved
