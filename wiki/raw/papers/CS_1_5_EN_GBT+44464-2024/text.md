<!-- Page 1 -->

Unofficial translation for reference only 
 
ICS 43.020CCS T 40
 
National Standard of the People'sRepublic of ChinaGB/T 44464-2024
 
 
 
 
 
General Requirements of Vehicle Data
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Published date: 2024-08-23Implemented date: 2024-08-23Published byState Administration for Market Regulation
Standardization Administration of the People's Republic of China 
 


<!-- Page 2 -->

Unofficial translation for reference only 
GB/T 44464-2024
I 
 
Table of Contents
 
Foreword ............................................................................................................................................................... III 
1 
Scope .............................................................................................................................................................. 1 
2 
Normative References .................................................................................................................................... 1 
3 
Terms and Definitions .................................................................................................................................... 1 
4 
General Requirements .................................................................................................................................... 3 
4.1
Requirements for vehicle data security management system .............................................................. 3 
4.2
General requirements for vehicle data processing ............................................................................... 4 
5 
Requirements for Personal Information Protection......................................................................................... 4 
5.1
General requirements for personal information processing ................................................................. 4 
5.2
Individual consent ............................................................................................................................... 5 
5.3
Collection of personal information ...................................................................................................... 6 
5.4
Storage of personal information .......................................................................................................... 6 
5.5
Use of personal information ................................................................................................................ 6 
5.6
Transmission of personal information ................................................................................................. 6 
5.7
Deletion of personal information ......................................................................................................... 8 
5.8
Cross-border transfer of personal information .................................................................................... 8 
6 
Requirements for Important Data Protection .................................................................................................. 8 
6.1
General requirements for important data processing ........................................................................... 8 
6.2
Collection of important data ................................................................................................................ 8 
6.3
Storage of important data .................................................................................................................... 8 
6.4
Use of important data .......................................................................................................................... 8 
6.5
Transmission of important data ........................................................................................................... 8 
6.6
Deletion of important data ................................................................................................................... 8 
6.7
Cross-border transfer of important data ............................................................................................... 8 
7 
Audit, Assessment and Test Requirements ..................................................................................................... 9 
Annex A  (Informative) Example of Classification and Grading of Vehicle Data ................................................ 10 
A.1
Principles for data classification and grading .................................................................................... 10 
A.2
Data classification ............................................................................................................................. 10 
A.3
Data grading ...................................................................................................................................... 10 
A.4
Examples of personal information classification and grading ........................................................... 11 
Annex B (Normative)  Test Method for Anonymization of Personal Information ............................................... 13 
B.1
Test conditions .................................................................................................................................. 13 
B.2
Test equipment .................................................................................................................................. 13 
B.3
Test process of requirements for anonymization performance .......................................................... 15 
B.4
Termination conditions of test on requirements for anonymization performance ............................. 15 
B.5
Processing of test results ................................................................................................................... 15 
B.6
Evaluation on anonymization effect .................................................................................................. 17 
Annex C  (Informative)  Calculation Methods for False Detection Rate of Anonymization ................................ 18 


<!-- Page 3 -->

Unofficial translation for reference only 
GB/T 44464-2024C.1
Calculation method for the number of face objects falsely anonymized ........................................... 18 
C.2
Calculation method for the number of face objects anonymized ...................................................... 18 
C.3
Calculation method for the false detection rate of face object........................................................... 18 
C.4
Calculation method for the number of vehicle license plate objects falsely anonymized ................. 18 
C.5
Calculation method for the number of vehicle license plate objects anonymized ............................. 19 
C.6
Calculation method for false detection rate of vehicle license plate objects ..................................... 19 
Annex D (Normative)  Testing Methods for Processing of Personal Information and Important Data ................ 20 
D.1
Test input information ....................................................................................................................... 20 
D.2
Testing methods for obtaining individual consent ............................................................................. 20 
D.3
Testing methods for collection of personal information and important data ..................................... 21 
D.4
Testing methods for storage of personal information and important data ......................................... 21 
D.5
Testing methods for the use of personal information ........................................................................ 21 
D.6
Testing methods for transmission of personal information and important data................................. 21 
D.7
Testing methods for deletion of personal information and important data ........................................ 22 
D.8
Testing methods for cross-border transfer of personal information and important data .................... 22 
Bibliography ......................................................................................................................................................... 23 
 
 


<!-- Page 4 -->

Unofficial translation for reference only 
GB/T 44464-2024
 
 
This document was drafted in accordance with the provisions given in GB/T 1.1-2020 
Directives for Standardization - Part 1: Rules for the Structure and Drafting of Standardizing 
Documents.
Attention is drawn to the possibility that some of the elements of this document may be 
the subject of patent rights. The issuing body of this document shall not be held responsible 
for identifying any or all such patent rights. 
This document was proposed by the Ministry of Industry and Information Technology of 
the People's Republic of China.
This document is under the centralized management of the National Technical Committee 
of Auto Standardization (SAC/TC 114).
Drafting organizations of this document: Ministry of Industry and Information 
Technology Equipment Industry Development Center, China Automotive Technology and 
Research Center Co., Ltd., Horizon Robotics Inc., Chongqing Changan Automobile Co., Ltd., 
Great Wall Motor Company Limited, NIO Technology (Anhui) Co., Ltd., Shanghai Motor 
Vehicle Inspection Certification & Tech Innovation Center Co., Ltd., Huawei Technologies 
Co., Ltd., Guangzhou Xpeng Motors Technology Co., Ltd., BYD Auto Industry Co., Ltd., 
Qualcomm Wireless Communication Technologies (China) Ltd., Beijing Saimo Technology 
Co., Ltd., China Information and Communication Technologies Group Corporation, China 
Software Testing Center (the Software and Integrated Circuit Promotion Center of the 
Ministry of Industry and Information Technology), Beijing CHJ Automotive Technology Co., 
Ltd., BAIC Research Institute Co., Ltd., 360 Digital Security Technology Group Co., Ltd., 
Banma Network Technology Co., Ltd., Mercedes-Benz (China) Investment Co., Ltd., Volvo 
Car (Asia Pacific) Investment Holding Co., Ltd., Pan Asia Technical Automotive Center Co., 
Ltd., BMW (China) Service Co., Ltd., FAW Jiefang Automotive Co., Ltd., Geely Automobile 
Research Institute (Ningbo) Co., Ltd., National Industrial Information Security Development 
Research Center, China Intelligent and Connected Vehicles (Beijing) Research Institute Co., 
Ltd., Anhui Jianghuai Automobile Group Co., Ltd., Volkswagen (China) Investment Co., Ltd., 
Shanghai Lingang Jueying Intelligent Technology Co., Ltd., Beijing Apollo Co., Ltd., Neusoft 
Reach Automotive Technology (Shenyang) Co., Ltd., PATEO Inc. and Shanghai Songhong 
Intelligent Automotive Technology Co., Ltd. 
Main drafters of this document: Qiu Bin, Wu Hanbing, Sun Hang, Xie Hanguang, Zhang 
Lu, Tian Shengming, Zhang Xiaodong, Jin Xiulian, Xia Xianzhao, Zhao Zijian, Pan Kai, 
Chen Jinfeng, Zhong Yilin, Wang Jiangsheng, Zhang Yanan, Li Guangyou, Hou Xintian, Bai 
Zhimin, Fang Jiayi, Wang Wei, Zhang Chunwang, Mou Hongyu, Yan Minrui, Man Zhiyong, 
Liu Fan, Li Tong, Gu Jinjin, Wu Yan, Zhao Chao, Xia Huan, Pan Yan, Chen Guihua, Zhu 
Chenwei, Zhao Wen, Shi Jianping, Cheng Zhou, Qi Shuai, Li Yujia, Li Xuesong, Teng Tianyi, 
Zou Bosong, Zou Xue, Tang Yan and Huo Yanyan. 


<!-- Page 5 -->

Unofficial translation for reference only 
GB/T 44464-2024
1 
General Requirements of Vehicle Data
1 
This document specifies general requirements for data generated and collected during the 
research and development (R&D), design, and manufacturing of automotive products. It 
outlines requirements for personal information protection, important data protection, and audit, 
assessment and test requirements, along with descriptions of relevant testing methods. 
This document is applicable to automotive products and vehicle data processors. 
2 
Normative ReferencesThere are no normative references in this document.
3 
Terms and Definitions
For the purposes of this document, the following terms and definitions apply. 
3.1the act of obtaining vehicle data by certain means3.2vehicle data security management system
a systematic approach used to regulate the process of vehicle data processing activities to 
ensure the security of vehicle data3.3cabin data
the data that may contain personal information collected from the vehicle cabin by 
various means such as cameras, infrared sensors, fingerprint sensors or microphones, and data 
generated from processing of such data[Source: GB/T 41871-2022, 3.6, modified]3.4personal information subjecta natural person identified by personal information[Source: GB/T 35273-2020, 3.3, modified]
3.5face object
the part of a natural person's head from the top of the frontal eyebrows to the bottom line 
of the chin and from the left ear to the right ear (excluding the ears) 
3.6face boundary frame
the smallest rectangle or a rotating rectangle covering the face object 
Example: See Fig. 1 for the schematic diagram of face boundary frame. 


<!-- Page 6 -->

Unofficial translation for reference only 
GB/T 44464-2024
2 
 
Fig. 1Schematic Diagram of Face Boundary Frame3.7vehicle license plate object
the official metal motor vehicle license plate installed on a vehicle 
Note:
The sprayed enlarged license plate and the temporary paper motor vehicle 
license plate are excluded.3.8vehicle license plate boundary frame
the smallest rectangle or a rotating rectangle formed by the outer edge of the vehicle 
license plate object3.9mask covering rate
the area ratio of the anonymized area within the face or vehicle license plate boundary 
frame to the whole boundary frame area
Example: See Fig. 2 for the schematic diagram of the mask covering rate. In this figure, 
the solid line area represents the face boundary frame area, the dotted line area represents the 
anonymized area, and the shaded area represents the overlapped area between the solid line 
area and the dotted line area. The mask covering rate is the area ratio of the shaded area to the 
solid line area.
 
Fig. 2Schematic Diagram of Mask Covering Rate3.10detection rate
rate of the number of face or vehicle license plate objects correctly anonymized to the 
number of those to be anonymized
Note 1: The number of objects correctly anonymized is the number of objects that have 


<!-- Page 7 -->

Unofficial translation for reference only 
GB/T 44464-2024
3 
been anonymized according to the requirements of this document. 
Note 2: The number of objects to be anonymized is the number of objects that shall be 
anonymized according to the requirements of this document. 
3.11false detection rate
rate of the number of face or vehicle license plate objects falsely anonymized to the 
number of objects anonymized
Note 1: The number of objects anonymized is the number of objects marked as objects of 
anonymization and anonymized.
Note 2: The number of objects falsely anonymized is the number of objects anonymized 
that do not conform to the definition of objects of anonymization in this 
document.
4 
General Requirements
4.1 Requirements for vehicle data security management system 
4.1.1
Vehicle data processors shall establish and implement a vehicle data security 
management system, and take technical measures for the protection of vehicle data security to 
ensure that vehicle data is always under effective protection and in legal use. 
4.1.2
Vehicle data processors shall develop vehicle data security objectives and policies, 
analyze the internal and external environment of the vehicle data security management system, 
and determine the boundaries and scope of application of the vehicle data security 
management system.4.1.3
Vehicle data processors shall establish a vehicle data security management 
organization and define the responsibilities of relevant personnel. 
4.1.4
Vehicle data processors shall establish a vehicle data classification and grading 
system and form a vehicle data asset management ledger.  
Note:
See Annex A for examples of vehicle data classification and grading. 
4.1.5
Vehicle data processors shall formulate specific hierarchical protection requirements 
and operating procedures for such processes as data collection, storage, use, processing, 
transmission, provision, disclosure and deletion for the whole life cycle of vehicle data. 
4.1.6
Vehicle data processors shall establish data security management procedures 
covering the entire vehicle lifecycle, including R&D, design, and manufacturing stages.  
Note:
Other stages, such as operation, maintenance and decommissioning, shall be 
implemented by reference.4.1.7
If vehicle data processors need to store personal information and important data 
collected and generated within the territory of the People's Republic of China, they shall store 
such information and data in China. If it is necessary to provide such information and data 
overseas, they shall pass the cross-border data transfer security assessment. 
4.1.8
Vehicle data processors shall establish systems for monitoring data security risks and 
managing incidents. Upon identifying a risk, they shall take immediate corrective actions. In 
the event of a data security incident, they shall promptly handle it, notify users as required 
promptly, and report to relevant authorities. They shall also conduct regular risk assessments 
of important data processing activities and submit reports to authorities. 
4.1.9
Vehicle data processors shall establish a complaint report handling mechanism, 
establish a data security complaint report channel, and timely handle users' complaint reports. 


<!-- Page 8 -->

Unofficial translation for reference only 
GB/T 44464-2024
4 
4.1.10 Vehicle data processors shall establish a data security management system for related 
parties of data processing, including signing data security agreements and verifying data 
security protection capabilities.4.2 General requirements for vehicle data processing4.2.1
When vehicle data processors process personal information generated and collected 
during the R&D, design, and manufacturing of automotive products, they shall comply with 
the requirements of Chapter 5, except in cases specified by mandatory national standards. 
Automotive products shall have the necessary capabilities to ensure that data processors meet 
the requirements of Chapter 5 or other circumstances stipulated by laws, administrative 
regulations and mandatory national standards when processing personal information. 
4.2.2
Automotive products shall have corresponding capabilities to ensure that when 
vehicle data processors process personal information, in-vehicle processing and default non-
collection shall comply with the requirements of 5.1, accuracy range application shall comply 
with the requirements of 5.3, masking processing by anonymization shall comply with the 
requirements of 5.6, and conspicuous notification shall comply with the requirements of 5.2. 
4.2.3
When vehicle data processors process important data generated and collected during 
the R&D, design, and manufacturing of automotive products, they shall comply with the 
requirements of Chapter 6, except in cases specified by mandatory national standards. 
Automotive products shall have the necessary capabilities to ensure that data processors meet 
the requirements of Chapter 6 or other circumstances stipulated by laws, administrative 
regulations and mandatory national standards when processing the important data. 
4.2.4
When data generated and collected during the R&D, design, and manufacturing of 
automotive products processed by vehicle data processors constitutes both personal 
information and important data, they shall comply with the requirements of both Chapter 5 
and Chapter 6 simultaneously.
5 
Requirements for Personal Information Protection 
5.1 General requirements for personal information processing 
5.1.1
Vehicle data processors shall process personal information for a clear and reasonable 
purpose in a manner that has the least impact on the personal rights and interests, and the 
personal information shall be directly related to the purpose of the processing. Unless 
otherwise set by the driver, the vehicle shall be set to not collect personal information by 
default. Personal information shall not be provided to parties outside the vehicle unless the 
consent of the personal information subject is obtained. 
5.1.2
Vehicle data processors may process personal information without obtaining the 
individual's consent in any of the following exceptions: 
-
for functions that are necessary to protect the life, health and property safety of 
natural persons in an emergency;-
processing of personal information that is disclosed by individuals themselves or that 
has been legally disclosed within a reasonable scope; 
-
collection of exterior personal information without the individual's consent to ensure 
the driving safety;-
other cases specified by laws, administrative regulations, mandatory national 
standards and other provisions.
Vehicle data processors shall explain the exceptions and reasons for obtaining the 
individual's consent in at least one form such as user manual, on-board display panel, voice 
and vehicle use-related applications.


<!-- Page 9 -->

Unofficial translation for reference only 
GB/T 44464-2024
5 
5.1.3
Vehicles shall not provide cabin data to the outside of the vehicle unless the 
individual's consent has been obtained or any exception listed in 5.1.2 is met. 
5.1.4
For personal information processed based on the individual's consent, its storage 
period shall be consistent with that of the personal information for which consent has been 
obtained or its rules.5.1.5
Withdrawal of the individual's consent shall not affect the validity of personal 
information processing activities carried out based on the individual's consent before the 
withdrawal.5.1.6
In any of the following cases, the vehicle data processor shall take the initiative to 
delete or anonymize personal information, and individuals have the right to request deletion if 
the vehicle data processor fails to do so: 
-
The processing purpose has been achieved or cannot be achieved, or it is no longer 
necessary to achieve the processing purpose; 
-
The vehicle data processor has stopped providing products or services, or the storage 
period has expired;-The individual has withdrawn his/her consent;-
The vehicle data processor processes personal information in violation of laws, 
administrative regulations or agreements; 
-
Other circumstances stipulated by laws and administrative regulations. 
If the storage period stipulated by laws and administrative regulations does not expire, or 
it is technically difficult to delete personal information, vehicle data processors shall stop 
processing personal information except storing it and taking necessary security protection 
measures.5.2 Individual consent5.2.1General requirements for individual's consent
Vehicle data processors shall obtain the individual's consent for the processing of personal 
information, and obtain separate consent for the processing of sensitive personal information. 
Under the above two circumstances, individuals shall be notified in at least one conspicuous 
way. The notice shall clearly explain the specific situation and necessity of processing 
personal information, and convenient personal information management functions such as 
access, copying and deletion shall be provided. The specific requirements are as follows: 
-
Individuals may be notified in the form of user manual, on-board display panel, voice, 
vehicle use-related application, etc.-The notification shall include at least:●
types of personal information to be processed and the necessity of processing 
various types of personal information, including purpose, use and method; 
●
specific scenarios where various types of personal information are collected, and 
ways and means to stop collecting personal information; 
●
storage place and period of personal information, or rules for determining the 
storage place and period;●
ways and means of accessing and copying personal information, deleting in-
vehicle personal information, and requesting the deletion of personal information 
that has been provided to the outside of the vehicle; 
●
name and contact information of the person for user rights and interests affairs; 


<!-- Page 10 -->

Unofficial translation for reference only 
GB/T 44464-2024
6 
●
other matters that shall be notified according to laws and administrative 
regulations.5.2.2Option settings for obtaining individual's consent
Vehicle data processors shall set the options for obtaining the individual's consent as 
follows:-Provide means of consent and refusal of consent;-
Provide a way to independently set the consent period for processing sensitive 
personal information (the period shall not be set to "always permissible" or 
"permanent").5.2.3Re-obtaining individual's consent
5.2.3.1 Vehicle data processors shall process personal information within the consent period 
obtained. After the individual's consent period expires, vehicle data processors shall re-obtain 
the individual's consent if they still need to continue the personal information processing 
activities other than deletion.
5.2.3.2 In case of change in the processing purpose, method or the type of personal 
information, vehicle data processors shall re-obtain the individual's consent. 
5.2.4Withdrawal of individual's consent
Vehicle data processors shall provide a means to withdraw the individual's consent. 
5.3 Collection of personal information5.3.1
When collecting personal information, vehicle data processors shall determine the 
coverage and resolution of cameras and radars according to the requirements of the provided 
functional services for data accuracy.5.3.2
When the same data collection equipment supports multiple functional services and 
there are different requirements on the required data accuracy, at least one functional service 
shall meet the requirements of 5.3.1. For other functional services that do not meet the 
requirements of 5.3.1, vehicle data processors shall make a reasonable explanation. 
5.4 Storage of personal information5.4.1
The vehicle shall use secure access technology, encryption technology or other 
security technologies to protect the sensitive personal information stored within it from 
unauthorized access and acquisition.5.4.2
The vehicle shall have a security defense mechanism to prevent unauthorized 
deletion and modification of the vehicle identification number (VIN) and other data stored 
within it for vehicle identification.Note:
Security defense mechanisms that prevent unauthorized deletion and 
modification of data include secure access technology and read-only technology. 
5.5 Use of personal information5.5.1
When using personal information, vehicle data processors shall take access control 
measures to prevent unauthorized access to the stored personal information. 
5.5.2
Personal biometric identification shall not be used as the only means of 
implementing personal identity authentication functions. 
5.6 Transmission of personal information 
5.6.1
Requirements for data transmission to the outside of the vehicle 


<!-- Page 11 -->

Unofficial translation for reference only 
GB/T 44464-2024
7 
5.6.1.1 Vehicles shall implement confidentiality protection measures for sensitive personal 
information transmitted externally.
5.6.1.2 When it is necessary to collect exterior personal information and provide it to the 
outside of the vehicle for the sake of safety during driving, but it is impossible to obtain the 
individual's consent, such information shall be anonymized, including deleting the picture 
containing the face of a natural person, or conducting local contouring of the face or vehicle 
license plate information in the picture. 
The anonymization processing shall comply with the requirements of 5.6.2. After 
anonymization, the process data shall be deleted timely and shall not be provided to the 
outside of the vehicle.5.6.2Requirements for anonymization5.6.2.1 Objects of anonymization5.6.2.1.1Objects of face anonymization
Vehicle data processors shall at least anonymize the face objects in the images or videos 
that meet the following requirements:-
The minimum side length of the face boundary frame is greater than or equal to 32 
pixels;-
In the face boundary frame, the visible range ratio is greater than 50% and the eyes, 
nose or mouth is clearly visible within the visible range. 
Note 1: The visible range ratio refers to the area ratio of the face object's visible range to 
the face object. The visible range is the area of the face object that can be 
directly observed within the face boundary frame. 
Note 2: Face objects appearing in advertising boards and reflections of smooth surfaces 
are not objects of anonymization.5.6.2.1.2Objects of vehicle license plate anonymization
Vehicle data processors shall at least anonymize the vehicle license plate objects in the 
images or videos that meet the following requirements: 
-
The minimum side length of the vehicle license plate boundary frame is greater than 
or equal to 16 pixels;-
The vehicle license plate object is unobstructed and all figures and characters are 
identifiable.5.6.2.2 Requirements for anonymization performance5.6.2.2.1Detection rate of anonymization
The detection rates of anonymization shall be greater than or equal to 90% for both face 
objects and vehicle license plate objects.  
Note:
See Annex B for the calculation method of detection rate of anonymization. 
5.6.2.2.2False detection rate of anonymization
The false detection rates of anonymization should be less than or equal to 10% for both 
face objects and vehicle license plate objects. 
Note:
See Annex C for the calculation method of false detection rate of anonymization. 
5.6.2.3 Anonymization effect
The face objects and vehicle license plate objects that meet the requirements of 5.6.2.1 


<!-- Page 12 -->

Unofficial translation for reference only 
GB/T 44464-2024
8 
and have been anonymized shall not be identified. 
5.7 Deletion of personal information5.7.1
If an individual requests deletion of sensitive personal information, the vehicle data 
processor shall complete the deletion within 10 working days, or as otherwise prescribed by 
laws or administrative regulations.5.7.2
Deleted personal information shall be irretrievable and inaccessible. 
5.8 Cross-border transfer of personal information 
Vehicles shall not directly transmit personal information and other data overseas. 
Note:
This provision does not apply to users who access overseas websites through 
browsers, send messages overseas using communication software, install third-
party applications that may involve cross-border data transfer, or engage in other 
autonomous user actions.
6 
Requirements for Important Data Protection 
6.1 General requirements for important data processing 
Vehicle data processors shall process important data for a clear and reasonable purpose, 
and the data shall be directly related to the purpose of the processing. Unless otherwise set by 
the driver, the vehicle shall be set to not collect important data by default. Important data shall 
not be provided for parties outside the vehicle. 
6.2 Collection of important data6.2.1
When collecting important data, vehicle data processors shall determine the coverage 
and resolution of cameras and radars according to the requirements of the provided functional 
services for data accuracy.6.2.2
When the same data collection equipment supports multiple functional services and 
there are different requirements on the required data accuracy, at least one functional service 
shall comply with the requirements of 6.2.1. For other functional services that do not comply 
with the requirements of 6.2.1, vehicle data processors shall make a reasonable explanation. 
6.3 Storage of important data
The vehicle shall use secure access technology, encryption technology or other security 
technologies to protect the important data stored within it from unauthorized access and 
acquisition.6.4 Use of important data
When using important data, vehicle data processors shall take access control measures to 
prevent unauthorized access to the stored important data. 
6.5 Transmission of important data
Vehicles shall implement confidentiality protection measures for important data 
transmitted externally.6.6 Deletion of important data
Deleted important data shall be irretrievable and inaccessible. 
6.7 Cross-border transfer of important data 
Vehicles shall not directly transmit important data and other data overseas. 
Note:
This provision does not apply to users who access overseas websites through 
browsers, send messages overseas using communication software, install third-


<!-- Page 13 -->

Unofficial translation for reference only 
GB/T 44464-2024
9 
party applications that may involve cross-border data transfer, or engage in other 
autonomous user actions.
7 
Audit, Assessment and Test Requirements
7.1 Vehicle data processors shall pass the conformity assessment with respect to the 
requirements of 4.1.
7.2 Personal information anonymization test shall be carried out on vehicles according to 
Annex B, and personal information and important data processing tests shall be carried out on 
vehicles according to Annex D. The corresponding requirements of each test shall be met. 
7.3 Vehicles should be tested for false detection rate of anonymization according to Annex C. 
 
 


<!-- Page 14 -->

Unofficial translation for reference only 
GB/T 44464-2024
10 
Annex A(Informative)Example of Classification and Grading of Vehicle DataA.1 Principles for data classification and grading
The principles for vehicle data classification and grading are as follows: 
-
Compliance: Data classification and grading shall comply with relevant provisions of 
national laws and regulations and those specified by competent authorities of this 
industry, in addition to meeting the requirements of relevant standards for data 
security management in the field of industry and information technology. 
-
Scientificity: Data shall be classified and graded in a scientific and systematic 
manner as per its multi-dimensional characteristics and mutual objective logical 
relationship.-
Practicability: Data shall be so classified and graded that each category contains data 
and there is no meaningless category.-
Expansibility: Data classification and grading shall be general and inclusive to cover 
various types of data to meet the data types and levels that may appear in the future. 
-
Significance: The scheme for data classification shall be determined according to the 
significant characteristics of data content. 
-
Feasibility: The rules shall not be too complicated to guarantee the feasibility of data 
classification and grading.-
Timeliness: Data classification and grading shall have a certain validity period and be 
timely adjusted.-
Stability: Data shall be classified and graded based on its most stable characteristics 
and attributes, and the same security requirements shall apply to data at the same 
level.A.2 Data classification
Vehicle data processors classify the data generated and collected during the R&D, design, 
and manufacturing of automotive products according to relevant laws, regulations and 
standards.A.3 Data gradingA.3.1Grading elementsA.3.1.1 Element type
Vehicle data processors shall grade the data generated and collected during the R&D, 
design, and manufacturing of automotive products based on the affected objects and the 
severity of impact.A.3.1.2 Affected object
An affected object refers to the entity impacted when the data generated and collected 
during the R&D, design, and manufacturing of automotive products is tampered with, 
damaged, leaked, illegally accessed, or misused, including national security, industry security, 
organizational security, and personal rights and interests, among which: 
-
When the affected object is national security, this refers to situations where data, if 
leaked, tampered with, damaged, or illegally accessed, could impact national political 
security, economic security, public security resource security, technological security, 
or cyber security;


<!-- Page 15 -->

Unofficial translation for reference only 
GB/T 44464-2024
11 
-
When the affected object is industry security, this refers to situations where data, if 
leaked, tampered with, damaged, or illegally accessed, could affect the safety of the 
automotive industry supply chain, critical infrastructure, or core technologies in the 
automotive industry;-
When the affected object is organizational security, this refers to cases where data, if 
leaked, tampered with, damaged, or illegally accessed, could impact the 
organization’s technical research, product development, production, and operations. 
-
When the affected object is personal rights and interests, this refers to instances, 
where data, if leaked, tampered with, damaged, or illegally accessed, may violate the 
personal dignity of a natural person or legal rights and interests of a personal 
information subject, including physical and property security. 
A.3.1.3 Severity of impact
The severity of impact is categorized from highest to lowest as severe harm, moderate 
harm, minor harm, and no impact. When the severity of impact for different affected objects 
is determined, the criteria vary. For national or industry security, the overall interests of the 
country, society, or industry are the basis for judgment of the severity of impact. For 
organizational or individual rights, the organization's or personal rights and interests are the 
criteria for judgment.A.3.2Grading method
The method for grading the data generated and collected during the R&D, design, and 
manufacturing processes of automotive products is outlined in Table A.1. Data is graded into 
core data, important data, and general data. Among the important data, those related to 
national security, the lifeline of the national economy, critical public interests, and key public 
services are classified as core data.Table A.1Data Grading MethodAffected objectSeverity of impactSevere harm
Moderate harmMinor harmNo impactNational securityImportant dataImportant data
Important dataGeneral dataindustry securityImportant dataImportant dataGeneral data
General dataOrganizationalGeneral dataGeneral dataGeneral dataGeneral data
Personal rights andinterestsGeneral dataGeneral dataGeneral dataGeneral data
Note:
If a large-scale organization or numerous individual rights and interests are affected, the impact 
may extend beyond organizational or personal rights and interests and could affect national or 
industry security.
Example: High-value sensitive data related to the competitiveness of the automotive 
industry, generated and collected during the R&D and design phases of automotive products, 
is classified as important data. This could include data used in algorithm development that is 
tied to the industry's core technological competitiveness, represents advanced industry 
standards, or could significantly impact industry development if leaked. 
A.3.3Other principles
In addition to the methods in Table A.1, data grading follows the principles below: 
a) The same data may rise in level due to the increase of data volume; 
b) The data level may rise due to the combination of different types of data. 
A.4 Examples of personal information classification and grading 


| is determined, the criteria vary. For national or industry security, the overall interests of the country, society, or industry are the basis for judgment of the severity of impact. For organizational or individual rights, the organization's or personal rights and interests are the criteria for judgment. A.3.2 Grading method The method for grading the data generated and collected during the R&D, design, and manufacturing processes of automotive products is outlined in Table A.1. Data is graded into core data, important data, and general data. Among the important data, those related to national security, the lifeline of the national economy, critical public interests, and key public services are classified as core data. Table A.1 Data Grading Method |  |  |  |  |
| --- | --- | --- | --- | --- |
| Affected object | Severity of impact |  |  |  |
|  | Severe harm | Moderate harm | Minor harm | No impact |
| National security | Important data | Important data | Important data | General data |
| industry security | Important data | Important data | General data | General data |
| Organizational security | General data | General data | General data | General data |
| Personal rights and interests | General data | General data | General data | General data |
| Note: If a large-scale organization or numerous individual rights and interests are affected, the impact may extend beyond organizational or personal rights and interests and could affect national or industry security. |  |  |  |  |
| Example: High-value sensitive data related to the competitiveness of the automotive |  |  |  |  |



<!-- Page 16 -->

Unofficial translation for reference only 
GB/T 44464-2024
12 
See Table A.2 for examples of personal information classification and grading. 
Table A.2Examples of Personal Information Classification and GradingClassification/GradingGeneral Personal InformationSensitive Personal InformationBasic personal
informationIndividual name, date of birth, e-mailaddress, residential address, privatetelephone number, age, gender, familyrelationship, etc.-
Personal identityinformationSystem account number of personalaccount (excluding password), etc.ID card, driver's license, system accountnumber of personal account (including
password), etc.Personal vehicleidentificationVIN, license plate number, drivinglicense, etc.-
Personal biometricrecognitioninformation-Personal genes, fingerprints, voiceprints,palm prints, auricles, irises, facial features,
etc.Personal propertyinformation-Virtual property, risk assessment records,asset information, credit records, etc.
communicationinformationSMS, e-mail, personal communication,etc.Communication records, contents, etc.Contact information E-mail address list, etc.
Address book, friend list, group list, etc. 
Personal applicationoperation informationApplication or software usage or clickrecords, favorite lists, etc.Website browsing history, etc.Information of
commonly-usedpersonal equipmentHardware serial number, device MACaddress, software list, unique deviceidentification code, etc.-
Personal locationinformation-Track, precise positioning information,longitude and latitude, etc.Additional
information-Personal audio, video, image data, etc.
Note 1: Due to the small range of direct communication and the continuous movement of the vehicle, it is 
difficult for the data receiver to continuously obtain the driving route of the vehicle, and the risk 
of disclosing the vehicle's whereabouts is low. Therefore, the vehicle location and the historical 
vehicle location information sent through direct communication are not considered as sensitive 
personal information.
Note 2: It is an anonymization technology that allows the information identifying the vehicle (such as 
identification and pseudonym certificate) to be changed frequently and randomly to make the 
data receiver within the direct communication range unable to identify a specific natural person 
with its own resources and technical means. 
Note 3: General personal information refers to other personal information, excluding sensitive personal 
information.
 
 


| Classification/Grading | General Personal Information | Sensitive Personal Information |
| --- | --- | --- |
| Basic personal information | Individual name, date of birth, e-mail address, residential address, private telephone number, age, gender, family relationship, etc. |  |
| Personal identity information | System account number of personal account (excluding password), etc. | ID card, driver's license, system account number of personal account (including password), etc. |
| Personal vehicle identification | VIN, license plate number, driving license, etc. |  |
| Personal biometric recognition information |  | Personal genes, fingerprints, voiceprints, palm prints, auricles, irises, facial features, etc. |
| Personal property information |  | Virtual property, risk assessment records, asset information, credit records, etc. |
| Personal communication information | SMS, e-mail, personal communication, etc. | Communication records, contents, etc. |
| Contact information | E-mail address list, etc. | Address book, friend list, group list, etc. |
| Personal application operation information | Application or software usage or click records, favorite lists, etc. | Website browsing history, etc. |
| Information of commonly-used personal equipment | Hardware serial number, device MAC address, software list, unique device identification code, etc. |  |
| Personal location information |  | Track, precise positioning information, longitude and latitude, etc. |
| Additional information |  | Personal audio, video, image data, etc. |
| Note 1: Due to the small range of direct communication and the continuous movement of the vehicle, it is difficult for the data receiver to continuously obtain the driving route of the vehicle, and the risk of disclosing the vehicle's whereabouts is low. Therefore, the vehicle location and the historical vehicle location information sent through direct communication are not considered as sensitive personal information. Note 2: It is an anonymization technology that allows the information identifying the vehicle (such as identification and pseudonym certificate) to be changed frequently and randomly to make the data receiver within the direct communication range unable to identify a specific natural person with its own resources and technical means. Note 3: General personal information refers to other personal information, excluding sensitive personal information. |  |  |



<!-- Page 17 -->

Unofficial translation for reference only 
GB/T 44464-2024
13 
Annex B(Normative)Test Method for Anonymization of Personal InformationB.1 Test conditionsB.1.1
A list of functions for the anonymization of personal information shall be provided 
and the relevant sensor information involved in the anonymization shall be clarified. 
B.1.2
The vehicle under test (VUT) for anonymization of personal information shall meet 
the following requirements:-
It shall be capable of anonymizing the image or video containing face objects and 
vehicle license plate objects outside the vehicle and transmitting such data to the 
outside of the vehicle;-
There shall be specific conditions for enabling functions of anonymization and 
transmission of data to the outside of the vehicle. 
B.1.3
If it is capable of outputting anonymized area range files, anonymized area range 
files can contain the anonymized marking areas such as rectangles, ovals or rotating 
rectangles, as well as the nature (face objects or vehicle license plate objects) and recording 
time of anonymized objects.B.2 Test equipmentB.2.1Recorded contents of test equipment
During the test, the test recording equipment shall be installed and at least the following 
contents shall be recorded:-Test timeline and test duration;-
Video information of the surrounding environment of the VUT. 
B.2.2Accuracy of test recording equipment
The resolution of test recording equipment shall not be less than (1920 x 1080) pixels, 
and the video sampling frame rate shall be 30 f/s at least. 
B.2.3Installation and operation of test recording equipment
The installation and operation of the test recording equipment shall not affect the existing 
configuration of the VUT and the normal operation of its personal information collection and 
transmission functions.B.2.4Requirements for test result marking capability
B.2.4.1 Requirements for picture sets for marking capability 
Select 500 anonymized pictures and 500 unanonymized pictures to form a picture set for 
marking capability verification. The picture set shall meet the following requirements: 
-A picture set not anonymized shall:●
at least include 200 face objects and 200 vehicle license plate objects; 
●
contain documentation describing the true pixels of all side lengths of the 
boundary frames of face objects and vehicle license plate objects; 
●
have documentation for the true value of visible range area of each face object. 
-An anonymized picture set shall:●
contain at least 200 anonymized face objects and 200 anonymized vehicle 


<!-- Page 18 -->

Unofficial translation for reference only 
GB/T 44464-2024
14 
license plate objects;●
contain documentation describing the true pixels of all side lengths of the 
boundary frames of face objects and vehicle license plate objects; 
●
have documentation with the true value of the visible range area of each face 
object;●
contain documentation describing the true values of the anonymized area and 
mask covering rate of anonymized face objects and vehicle license plate objects; 
●
have no pictures identical to those in the unanonymized picture set. 
Note:
The pictures in the picture set are those collected during non-test processes. 
B.2.4.2 Marking accuracy requirements
Before the marking processing of pictures in B.5.1, the picture set meeting the 
requirements of B.2.4.1 shall be imported and the marking capability shall be verified. The 
accuracy of marking shall meet the following requirements: 
-
In the unanonymized picture set, face boundary frames in pictures shall be marked. 
When the actual pixel of the minimum side length of the face boundary frame is 
greater than or equal to 27 pixels, rates of marked pixel to the actual pixel of the 
minimum side length of all boundary frames shall be calculated. The number of 
bounding frames with a rate between 0.9 and 1.1 shall account for more than 98% of 
the total number of the face boundary frame. 
-
In the unanonymized picture set, vehicle license plate boundary frames in pictures 
shall be marked. When the actual pixel of the minimum side length of the vehicle 
license plate boundary frame is 11 pixels or more: 
●
When the actual pixel of the minimum side length of the vehicle license plate 
boundary frame is 20 pixels or less, the average for the absolute values of 
calculated deviations between the marked pixels and actual pixels of the 
minimum side length of all boundary frames shall be 1 pixel or less; 
●
When the actual pixel of the minimum side length of the vehicle license plate 
boundary frame is greater than 20 pixels, rates of marked pixels to actual pixels 
of the minimum side length of all boundary frames shall be calculated and the 
average for them shall be greater than or equal to 0.9 and less than or equal to 
1.1.-
In the unanonymized picture set, the visible range of face object shall be marked. 
When the visible range of the face is less than the objective of 100% and the pixel of 
the minimum side length of the face boundary frame is 27 pixels or more, the rate of 
the marked value to the actual value of the visible range area shall be calculated, and 
the average of the rate shall be greater than or equal to 0.9 and less than or equal to 
1.1.-
In the unanonymized picture set, marking shall be performed by following 5.6.2.1. 
The rate between the number of identified face objects or vehicle license plate 
objects to be anonymized and to the actual number in pictures shall be greater than or 
equal to 0.99 and less than or equal to 1.01. 
-
In the anonymized picture set, all anonymized objects shall be marked and their mask 
covering rates shall be calculated. For objects of anonymization with a mask 
covering rate less than 100%, the average for absolute values of deviations between 
mask covering rates calculated by marking and actual mask covering rates shall be 5% 
or less.


<!-- Page 19 -->

Unofficial translation for reference only 
GB/T 44464-2024
15 
-
In the anonymized picture set, marking shall be performed by following 5.6.2.1, and 
the numbers of face objects and vehicle license plate objects correctly anonymized 
and missed shall be calculated. The rate of them to the numbers of the actual objects 
correctly anonymized and missed shall be greater than or equal to 0.98 and less than 
or equal to 1.02.
B.3 Test process of requirements for anonymization performance 
B.3.1
The VUT starts anonymization and transmission to the outside of the vehicle of the 
image or video of face objects and vehicle license plate objects outside the vehicle. 
B.3.2The test recording equipment is turned on during the test.
B.4 Termination conditions of test on requirements for anonymization performance 
B.4.1Overall requirements
The test on requirements for anonymization performance shall be terminated after the 
requirements of B.4.2 and B.4.3 are met. 
B.4.2Test exhaustiveness requirements
Collected data shall cover pictures or videos collected by sensors listed in B.1.1. The 
number of pictures under test corresponding to each sensor shall be no less than 10 or the 
duration of each video under test corresponding to each sensor shall be no less than 10 s, at 
least containing 1 face object or 1 vehicle license plate object that needs to be anonymized. 
B.4.3Test pictures and video requirements
Pictures or videos collected during the test shall meet the following requirements: 
-
In the case of pictures, at least 500 pictures are taken at intervals greater than or equal 
to 1 s;-
In the case of video, the duration of all videos is not less than 1000 s, with the 
duration of each piece of video not less than 10 s; 
-
To meet the requirements of this document, it is necessary that the number of face 
objects to be anonymized is not less than 200, with the same face object counted 
separately in different pictures.-
To meet the requirements of this document, it is necessary that the number of vehicle 
license plate objects to be anonymized is not less than 200, with the same vehicle 
license plate object counted separately in different pictures. 
B.5 Processing of test resultsB.5.1Test data reading
B.5.1.1 After the test, read anonymized pictures or videos of the VUT. If an anonymized area 
range file can be read, read the file.
B.5.1.2 After the test, read videos that can represent the actual driving process in the test 
recording equipment.B.5.1.3 Process the data read based on B.5.1.1 as follows:-
If the files output by the VUT contain anonymized videos, frames shall be extracted 
at a fixed number of frames or a fixed time interval, and no more than 1 picture shall 
be extracted every 2 s, and the number of extracted pictures shall not be less than 500; 
-
The face boundary frame, the vehicle license plate boundary frame and the visible 
area and anonymized area of face objects shall be marked in the direct-output or 
frame-extracted pictures.


<!-- Page 20 -->

Unofficial translation for reference only 
GB/T 44464-2024
16 
B.5.1.4 The size and resolution of anonymized pictures shall not be changed during the 
reading of anonymized pictures and videos, the frame extraction and marking of videos. 
B.5.2Calculation process of mask covering rate
Calculate the mask covering rate based on test results processed in B.5.1.3. 
B.5.3Calculation process of detection rate
B.5.3.1 Calculation method for the number of face objects correctly anonymized 
When a face object meets the following requirements, it shall be included in the number 
of face objects correctly anonymized:-It meets the requirements of 5.6.2.1.1 and is anonymized;-The mask covering rate is greater than or equal to 50%.
B.5.3.2 Calculation method for the number of face objects missed 
When a face object meets the following requirements, it shall be included in the number 
of face objects missed:-It meets the requirements of 5.6.2.1.1;-The mask covering rate is less than 50%.
Example: There is a face object with a mask in the picture as shown in Fig. B.1. The face 
object is not anonymized. According to the comparison of the face object boundary frame, the 
visible range is greater than 50%, including eyebrows and eyes, which can be clearly located, 
and the object is counted in the number of objects missed. 
 
Fig. B.1 Example of the Number of Objects Missed 
B.5.3.3 Calculation method for detection rate of face objects 
Calculate the detection rate of face objects according to formula B.1. 
 
Where,Rdf- detection rate of face objects;Naf+Nmf- face objects to be anonymized;
Naf- number of positive detection meeting the requirements of B.5.3.1; 
Nmf- number of missed detection meeting the requirements of B.5.3.2. 
B.5.3.4 Calculation method for the number of vehicle license plate objects correctly 
anonymized
When a vehicle license plate object meets the following requirements, it shall be included 
in the number of vehicle license plate objects correctly anonymized: 


<!-- Page 21 -->

Unofficial translation for reference only 
GB/T 44464-2024
17 
-It meets the requirements of 5.6.2.1.2 and is anonymized;-The mask covering rate is greater than or equal to 50%.
B.5.3.5 Calculation method for the number of vehicle license plate objects missed 
When a vehicle license plate object meets the following requirements, it shall be included 
in the number of vehicle license plate objects missed: 
-It meets the requirements of 5.6.2.1.2;-The mask covering rate is less than 50%.
B.5.3.6 Calculation method for detection rate of vehicle license plate objects 
Calculate the detection rate of vehicle license plate objects according to formula B.2. 
 
Where,Rdv- detection rate of vehicle license plate objects;Nav+Nmv-number of vehicle license plate objects to be anonymized;
Nav- number of positive detection meeting the requirements of B.5.3.4; 
Nmv-
number of missed detection meeting the requirements of B.5.3.5. 
B.6 Evaluation on anonymization effectB.6.1Testing methods for machine identification
B.6.1.1 Testing methods for unidentifiability of human faces 
Select two algorithm models with a face recognition function to identify all anonymized 
objects counted in the number of face objects correctly anonymized, such as the open source 
model and the public security model. Assess whether any anonymized object counted as the 
number of face objects correctly anonymized is recognized as a face object. 
B.6.1.2 Testing methods for unidentifiability of vehicle license plates 
Select two algorithm models supporting figure, letter and character recognition to identify 
all anonymized objects counted in the number of vehicle license plate objects correctly 
anonymized, such as the CRNN algorithm. Assess whether the contents of any vehicle license 
plate to be anonymized counted in the number of vehicle license plate objects correctly 
anonymized can be fully identified.B.6.2Testing methods for manual identification
B.6.2.1 Randomly select 100 anonymized pictures and the test staff will identify anonymized 
objects counted in the number of face objects and vehicle license plate objects correctly 
anonymized.
B.6.2.2 Assess whether it is possible to figure out the full contour ranges of eyes, nose and 
mouth of any anonymized object counted in the number of face objects correctly anonymized. 
B.6.2.3 Assess whether the contents of any vehicle license plate to be anonymized counted in 
the number of vehicle license plate objects correctly anonymized can be fully identified. 
 
 


<!-- Page 22 -->

Unofficial translation for reference only 
GB/T 44464-2024
18 
Annex C(Informative)
 Calculation Methods for False Detection Rate of Anonymization 
C.1 Calculation method for the number of face objects falsely anonymized 
When an anonymized object meets the following requirements, it will be included in the 
number of face objects falsely anonymized: 
-
It is marked as a face object by the anonymization system of the VUT and 
anonymized;-It has no intersection with any face object.
If an anonymized object contains face object images on the advertising board and in the 
reflection of smooth surfaces, it will not be counted in the number of objects falsely 
anonymized. Objects other than vehicle license plates and faces that are masked according to 
other requirements stipulated by laws, administrative regulations and mandatory national 
standards will not be counted in the number of objects falsely anonymized. 
Example 1: If an animal face is anonymized and marked as a human face object, it will 
be included in the number of false detection. 
Example 2: If an anonymized area appears above the head, has no intersection with a 
face object and is marked as a face object, it will be counted in the number of objects falsely 
anonymized.
Example 3: If an anonymized area intersects with a face object, it will not be counted in 
the number of objects falsely anonymized. 
C.2 Calculation method for the number of face objects anonymized 
The total number of anonymized objects marked as face objects by the anonymization 
system of the VUT.
C.3 Calculation method for the false detection rate of face object 
Refer to formula C.1 for the calculation method of the false detection rate of face objects. 
 
Where,RFf- false detection rate of face objects;
NFf- number of objects falsely anonymized meeting the requirements of C.1; 
Ndf- number of objects anonymized meeting the requirements of C.2. 
C.4 Calculation method for the number of vehicle license plate objects falsely 
anonymized
When an anonymized object meets the following requirements, it shall be counted in the 
number of vehicle license plate objects falsely anonymized: 
-
It is marked as a vehicle license plate object by the anonymization system of the 
VUT and anonymized;-
It has no intersection with any vehicle license plate object. 
If an anonymized object contains license plates of electric bicycles and motorcycles and 
temporary license plates of motor vehicles that are marked as vehicle license plate objects, it 
shall not be included in the number of objects falsely anonymized. 
If an anonymized object contains spray-painted and enlarged vehicle license plates, as 


<!-- Page 23 -->

Unofficial translation for reference only 
GB/T 44464-2024
19 
well as vehicle license plate object images on the advertising board and in the reflection of 
smooth surfaces, it will not be counted in the number of objects falsely anonymized. 
Example 1: If areas such as telegraph poles and garbage cans have anonymized areas and 
are marked as vehicle license plate objects, they will be counted in the number of objects 
falsely anonymized;
Example 2: If an anonymized area intersects with a vehicle license plate object, it will 
not be counted in the number of objects falsely anonymized. 
C.5 Calculation method for the number of vehicle license plate objects anonymized 
The total number of anonymized objects marked as vehicle license plate objects by the 
anonymization system of the VUT.
C.6 Calculation method for false detection rate of vehicle license plate objects 
Refer to formula C.2 for the calculation method for the false detection rate of vehicle license 
plate objects.
 
Where,RFv- false detection rate of vehicle license plate objects
NFv- number of false detection meeting the requirements of C.4; 
Ndf- number of objects anonymized meeting the requirements of C.5. 
 
 


<!-- Page 24 -->

Unofficial translation for reference only 
GB/T 44464-2024
20 
Annex D(Normative)
 Testing Methods for Processing of Personal Information and Important Data 
D.1 Test input information
The following information shall be provided prior to commencement of the test: 
a) List of functions involved in the VUT to process personal information and important 
data;b) List of ways to withdraw individual consent;
c) Parameter information of data collection equipment for VUT conforming to Table 
D.1;
d) The address where the personal information and important data are stored in the VUT. 
Table D.1Parameters of Data Collection EquipmentS/NEquipmentEquipmentResolution Coverage Mounting
Functions(fill inaccording torequirementsof thestandard, if
any)FunctionalExplanation(if required)and Necessity
1 
(Example) LiDAR/Camera(brand)1280×960Horizontalangle: ××angle:
××Non-standardfunctions areexplained
 
 
 
 
 
 
 
 
 
2 
 
 
 
 
 
 
 
 
D.2 Testing methods for obtaining individual consent 
D.2.1
Based on the list of functions for personal information processing, activate the 
various personal information processing functions of the VUT (apart from exceptions listed in 
5.1.2), check and record the notification method and contents and the individual consent 
method. Determine whether the test results meet the requirements of 5.2.1 and 5.2.2. 
D.2.2
According to the list of functions for processing personal information, when the 
consent period of each personal information processing function expires, start each personal 
information processing function of the VUT (except for the exceptions listed in 5.1.2), check 
whether personal consent is re-obtained and record the mode of personal consent. Determine 
whether the test results meet the requirements of 5.2.3.1. 
D.2.3
Based on the list of functions for personal information processing, change the 
purpose, method or type of personal information processing of some functions, activate 
corresponding functions, check whether the individual consent is re-obtained, and record the 
individual consent method. Determine whether the test results meet the requirements of 
5.2.3.2.D.2.4
Based on the list of functions for personal information processing, withdraw the 
individual consent for various functions and record the means to withdraw the individual 
consent for the functions (apart from exceptions listed in 5.1.2). Determine whether the test 
results meet the requirements of 5.2.4.


| S/N | Equipment Type | Equipment Model | Resolution |  | Mounting Location | Functions Involved (fill in according to the requirements of the standard, if any) | Functional Explanation (if required) and Necessity Analysis |  |
| 1 (Example) | LiDAR/Camera | XX (brand) and product model | 1280×960 | Horizontal field angle: ×× Vertical field angle: ×× | Vehicle front | Auto parking | Non-standard functions are explained here |  |
| D.2 Testing methods for obtaining individual consent D.2.1 Based on the list of functions for personal information processing, activate the various personal information processing functions of the VUT (apart from exceptions listed in 5.1.2), check and record the notification method and contents and the individual consent method. Determine whether the test results meet the requirements of 5.2.1 and 5.2.2. D.2.2 According to the list of functions for processing personal information, when the consent period of each personal information processing function expires, start each personal information processing function of the VUT (except for the exceptions listed in 5.1.2), check whether personal consent is re-obtained and record the mode of personal consent. Determine whether the test results meet the requirements of 5.2.3.1. |  |  |  |  |  |  |  |  |



<!-- Page 25 -->

Unofficial translation for reference only 
GB/T 44464-2024
21 
D.3 Testing methods for collection of personal information and important data 
Based on the parameter information of data collection equipment such as radar and cameras 
of the VUT, compare the accuracy of data collection equipment required for functions in the 
list of functions, and record the test result. Determine whether the test results meet the 
requirements of 5.3 and 6.2.
D.4 Testing methods for storage of personal information and important data 
D.4.1
Based on the list of functions of personal information and important data processing 
and the storage address list, confirm the test components, trigger the vehicle's functions that 
record sensitive personal information and important data in sequence, and conduct tests in the 
following manner. Then, determine whether the test results meet the requirements of 5.4.1 and 
6.3:
a) If secure access technology is used to protect the stored sensitive personal 
information and important data, access the stored sensitive personal information and 
important data with a user without access control permission through the component 
debugging interface according to the description of the storage area and address 
range of sensitive personal information and important data, to test whether 
unauthorized access to sensitive personal information and important data is allowed; 
b) If encryption technology is used to protect the stored sensitive personal information 
and important data, extract the stored sensitive personal information and important 
data with a software analysis tool through the component debugging interface 
according to the description of the storage area and address range of the sensitive 
personal information and important data, to test whether the information is stored in 
ciphertext;
c) Trigger the vehicle's functions of recording sensitive personal information and 
important data in turn, then log in to the system, and retrieve sensitive personal 
information and important data from the test components, to test whether sensitive 
personal information and important data that is not stored in the list of functions of 
sensitive personal information and important data and the list of storage addresses 
can be retrieved.D.4.2
Determine the test components according to the list of data stored in the vehicle for 
vehicle identification (such as VIN) and the storage address, and use the software analysis 
tool to delete and modify the data stored in the vehicle for vehicle identification (such as VIN) 
without authorization, to determine whether the vehicle meets the requirements of 5.4.3 and 
6.3.3.D.5 Testing methods for the use of personal information
Based on the list of functions for personal information processing, select functions that 
require the use of personal biometric information for identity authentication, stop collecting 
personal biometric recognition information, check whether the corresponding identity 
authentication function operates normally and record the test result. Determine whether the 
test results meet the requirements of 5.5.2. 
D.6 Testing methods for transmission of personal information and important data 
D.6.1
Based on the list of functions for personal information processing, select the function 
that needs to provide cabin data for the outside of the vehicle (except for the exceptions listed 
in 5.1.2), activate the corresponding function, check whether the vehicle sends a request for 
individual consent on providing cabin data for the outside of the vehicle and record the test 
results. Determine whether the test results meet the requirements of 5.1.3. 
D.6.2
According to the list of functions that process personal information and important 


<!-- Page 26 -->

Unofficial translation for reference only 
GB/T 44464-2024
22 
data, trigger the vehicle's function to transmit sensitive personal information and important 
data externally. Use the ports and access permissions provided by the vehicle manufacturer to 
capture the transmitted data packets. Check whether the sensitive personal information and 
important data transmitted by the vehicle are encrypted, and determine whether the test results 
meet the requirements of 5.6.1.1 and 6.5. 
D.6.3
Based on the list of functions for processing of personal information, activate the 
corresponding function meeting the conditions specified in 5.6.1.2, check whether the 
personal information transmitted to the outside of the vehicle is anonymized, and record the 
test results. Determine whether the test results meet the requirements of 5.6.1.2. 
D.7 Testing methods for deletion of personal information and important data 
D.7.1
Based on the list of functions for personal information processing, select functions 
that involve sensitive personal information processing, request the deletion of sensitive 
personal information if the sensitive personal information involved in the corresponding 
function is stored on the vehicle side, check the deletion state and record the test results. 
Determine whether the test results meet the requirements of 5.7.1. 
D.7.2
Based on the list of functions for processing of personal information and important 
data, select relevant functions for storing personal information and important data on the 
vehicle side, request the deletion of personal information and important data, search the 
content of the deleted data on the vehicle side, and record the retrieval results. Determine 
whether the test results meet the requirements of 5.7.2 and 6.6. 
D.8 Testing methods for cross-border transfer of personal information and important 
Activate all cellular communication channels and wireless local area network (WLAN) 
communication channels of the vehicle. Simulate the following states for testing: vehicle 
powered off, vehicle powered on, and all pre-installed data transmission functions enabled. 
Use a network packet capture tool to simultaneously capture data on all external 
communication channels for a duration of no less than 3,600 s. Parse the captured 
communication data packets and check whether the destination IP addresses include any 
foreign IP addresses. Determine whether the vehicle meets the requirements of 5.8 and 6.7. 
 
 


<!-- Page 27 -->

Unofficial translation for reference only 
GB/T 44464-2024
23 
 
Bibliography
 
[1] GB/T 35273-2020 Information Security Technology - Personal Information Security 
Specification
[2] GB/T 41871-2022 Information Security Technology - Security Requirements for 
Processing of Motor Vehicle Data
 
 


<!-- Page 28 -->

Unofficial translation for reference only 
GB/T 44464-2024
24 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
National Standard ofthe People's Republic of China
 
General Requirements of Vehicle DataGB/T 44464-2024*Published by Standards Press of ChinaNo. A2, Hepingli West Street, Chaoyang District,Beijing (100029)
No. 16, Sanlihe North Street, Xicheng District, Beijing 
(100045)Website: www.spc.net.cnService hotline: 400-168-0010First edition in August 2024*Book No.: 155066·1-77646
All Rights Reserved
 
GB/T 44464-2024


