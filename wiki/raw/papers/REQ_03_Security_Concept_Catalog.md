---
source_url: ""
ingested: 2026-08-06
sha256: 1f0f4256d20975455179dc0343e543f73507770f9378680e7a02ac9c71ad61e6
---

# REQ_03_Security_Concept_Catalog


Security Concept Catalog


| 版本Version | 日期Date | 作者Author | 更新说明Comment |
| 0.04 | 2026-Jan-16 | Guo, Yalao | Add Secure Storage as a security concept |
| 0.03 | 2025-Dec-16 | Kunze, Kai | Review |
| 0.02 | 2025-Dec-16 | Guo, Yalao | Initial Version, without 1. Chapter |
| 0.01 | 2025-Dec-08 | Guo, Yalao | Draft Version |


1. Introduction


1.1 Purpose


1.2 Overview Security Architecture Framework


The Security Architecture Framework consists out of three main components:


Security Concept Catalog


E/E-Architecture Security Analysis


Security Architecture


| 本文的目的 |


Will be added


1.3 Basics


| 描述基本的概念，如攻击模型，核心是后续第二章用的前提概念和知识背景 |


Will be added


2. Security Concepts


2.1 Diagnostic Interface Protection


2.1.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


The diagnostic interface protection is designed to prevent unauthorized access to the ECU by external tools. It provides a mechanism that allows the server to control client access permissions, thereby prohibiting unauthorized access.诊断接口防护用于防止外部工具未经授权访问ECU。其提供了一种机制，使服务端能够控制客户端的访问权限，从而禁止未经授权的访问。


2.1.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


Unified Diagnostic Service (UDS) according to the ISO 14229 standard is a protocol used by diagnostic systems to communicate with ECUs in vehicles. The protocol is used to diagnose errors and reprogram ECUs. For example, it is possible to read and delete the fault memory of an ECU or to flash a new firmware on the ECU. The vehicle is equipped with numerous ECUs that support UDS services. Generally, ECUs providing UDS services are referred to as UDS servers, while external diagnostic devices requesting UDS services are called UDS clients.ISO-14229标准的统一诊断服务（UDS）是诊断系统用于与车辆电子控制单元（ECU）进行通信的协议。该协议可用于故障诊断和重新编程ECU。例如，可以读取和删除ECU的故障存储器，或在ECU上刷新新的固件。车辆中配备了大量支持UDS服务的ECU。通常而言，提供UDS服务的ECU被称为服务端（Server），而请求UDS服务的外部诊断设备则被称为客户端（Client）。


In general, the protection mechanism for the diagnostic interface shall be implemented according to the ISO 14229 standard. e.g., UDS Service $27/$29. These services provide a mechanism for the server to control client access permissions, preventing unauthorized access.


通常，诊断接口的保护机制应基于ISO-14229标准进行实施。例如UDS $27/$29服务。这些服务提供了一种机制，使服务端能够控制客户端的访问权限，从而禁止未经授权的访问。


The authentication should adopt a challenge-response mechanism based on symmetric or asymmetric cryptographic, and can also be based on digital signature or certificate.


一般的，认证应采用基于对称或非对称加密的挑战应答机制，也可以基于数字签名或证书来实现。


2.1.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


The diagnostic interface protection protects configuration data, critical data read/write operations, routines or I/O control operations, firmware reprogramming, and other UDS services implemented through diagnostic interfaces. The mechanism also effectively prevents the unauthorized access of critical/personal privacy data via diagnostic service.诊断接口防护能够保护通过诊断接口实现的配置数据与关键数据读写、例程或I/O控制操作、固件重编程及其他UDS服务。该机制还能有效防止通过诊断服务对于关键/个人隐私数据的非授权访问。


2.1.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.2 Debugging Interface Protection


2.2.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


In order to prevent unauthorized access from external tools to the ECU via debugging interface, it is required to apply debugging interface protection that locks the debugging interface. This mechanism controls access permissions, preventing unauthorized access.为防止外部工具通过调试接口未经授权访问ECU，需采用调试接口防护锁定调试接口。这种机制能够控制访问权限，从而禁止未经授权的访问。


2.2.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


Debugging Interface Protection is an essential security control in a vehicle system that is connected to the outside. Because an easy and effective way for a hacker to attack an ECU (Electronic Control Unit) in a vehicle is to connect to it through its debug interface. Therefore, unprotected debug interfaces provide a substantial security risk to vehicle systems. 调试接口保护是车辆系统与外部连接时不可或缺的关键安全控制技术。由于黑客入侵车辆电子控制单元（ECU）最简便有效的方式就是通过连接调试接口，这对车辆系统构成了严重的安全威胁。


In order to prevent unauthorized access from external tools to the ECU via debugging interface, it is required to apply a protection mechanism that locks the debug interface (JTAG, SWD, UART, XCP, BDM, Nexus, SSH, ADB, special supplier interfaces or any other) to protect the system operation and code. It can also prevent the leakage of critical data. In general, the protection mechanism for the debug interface should be implemented based on authentication or password. Because developers need to connect external maintenance tools in order to analyze the ECU due to the occurrence of defects in the vehicle lifecycle after start of production. The authentication shall be based on symmetric, asymmetric cryptographic, digital signature or certificate.为防止外部工具未经授权访问ECU，必须实施控制措施锁定调试接口(包括JTAG、SWD、UART、XCP、BDM、Nexus、SSH、ADB、供应商专用接口或其他任何类型)。通常调试接口保护机制应采用密码验证方案——因为车辆量产后若出现缺陷，开发人员仍需通过外部工具连接ECU进行分析。认证应基于对称加密、非对称加密、数字签名或证书来实现。


After the start of production, the debugging interface shall be disabled. If it is necessary to retain access to the debugging interface for maintenance purposes, cryptographic authentication should be prioritized to secure the debugging interface. Only when cryptographic authentication is not available, password locking may specifically refer to.


量产后应关闭调试接口。确因维护需保留调试接口接入能力的，应优先采用密码学验证方式锁定调试接口。仅当密码学验证方式不可用时，口令锁定方式可被接受。


2.2.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


The Debugging Interface Protection can prevent unauthorized access and modification through debugging interfaces, ensuring system operation and code security while avoiding the leakage of critical/personal privacy data or components with interllectual property right via debugging interface.


调试接口保护功能可防止通过调试接口进行未经授权的访问和修改，在保障系统运行与代码安全的同时，避免关键数据/个人隐私信息或具有知识产权的组件通过调试接口泄露。


2.2.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.3 ECU Programming Data Security (EPDS)


2.3.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


EPDS is used to ensure the authenticity and integrity of the ECU programming data. It is needed to secure the (re)programming of the ECU, especially during the transfer from the OEM into the ECU. Furthermore, EPDS can also provide confidentiality protection, preventing intellectual property damage and potential firmware reverse engineering caused by reprogramming data leaks.


电子控制单元编程数据安全用于在从原始设备制造商（OEM）传输至电子控制单元（ECU）的过程中，确保用于（重新）编程ECU的编程数据的真实性和完整性。更进一步的，该机制还可提供保密性的保护能力，防止因重编程数据泄露导致的知识产权损害和潜在的固件逆向可能。


2.3.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


To flexibly adapt programming, state-of-the-art microcontrollers are increasingly storing their programs in memory based on flash memory technology. There are special processes and algorithms to clear and program this memory in the microcontroller. To ensure that only programming data released by the original equipment manufacturer (OEM) can be programmed into the microcontroller, various security measures can be used in the vehicle and on the part of the manufacturer. Generally, such measures are referred to as ECU Programming Data Security(EPDS). EPDS is a generic term for security mechanisms that uniquely verify the authenticity and integrity of the programmed data in the ECU reprogramming.


为了灵活适应编程需求，如今的微控制器越来越多地将程序存储在基于闪存技术的存储器中。微控制器采用专门的流程和算法来擦除和编程该存储器。为确保只有原始设备制造商（OEM）发布的编程数据能被刷写到微控制器中，车辆端和制造商端均可采用多种安全措施。一般的，这类安全措施被称为电子控制单元编程数据安全（EPDS）。EPDS 是指在 ECU 重编程阶段，用于验证编程数据真实性和完整性的安全机制的通用术语。


The authenticity and integrity check of programming data can be based on message authentication code or digital signature. Confidentiality protection can be achieved based on symmetric or asymmetric encryption.


编程数据的真实性和完整性检查可以基于消息认证码或数字签名来实现。机密性保护可以基于对称或非对称加密实现。


2.3.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


The EPDS should prevent any non-original equipment manufacturer (Non-OEM) programming data from being flashed into the control unit, thereby ensuring the authenticity and integrity of the programming data. When necessary, confidentiality protection capabilities must also be provided.


电子控制单元编程数据安全应能够防止非原始设备制造商发布的编程数据被刷写到控制单元当中，保障编程数据的真实性和完整性。必要时，还需提供机密性保护机制。


2.3.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.4 Software Integrity Protection (SIP)


2.4.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


Software Integrity Protection (SIP) is the generic term for the security mechanisms Secure Boot, Authenticated Boot, and Runtime Integrity Verification that ensure the authenticity and integrity of the ECU’s software during runtime execution.These mechanisms are designed to detect and prevent manipulation of the software.


SIP是Secure Boot（安全启动）、Authenticated Boot（认证启动）和Runtime Integrity Verification（运行时完整性验证）等安全机制的总称，这些机制确保电子控制单元（ECU）软件在执行过程中的真实性和完整性。旨在检测并防止对软件的篡改。


2.4.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


MATE（Man-At-The-End）normally have the full privilege on the software system as well as physical access to the hardware. Such attackers can readily tamper with softwares at any stage (at rest, in-memory and in-execution). Moreover, they could potentially load a malicious kernel driver to bypass security mechanisms employed.


终端用户（Man-At-The-End）通常对软件系统拥有完全权限，并能物理接触硬件设备。这类攻击者能够在软件的任何运行阶段（静态存储、内存驻留或执行过程中）轻易实施篡改。更甚者，他们可能加载恶意内核驱动程序，从而绕过已经部署的安全防护机制。


Therefore, Integrity is a crucial property for the software of embedded systems. Due to malicious this property can be violated. many methodologies that check or verify the integrity of software have been introduced. However, integrity as a property cannot be identified directly. Existing methodologies tackle this problem by identifying other, computable, properties of the software and use a policy that describes how these properties reflect the integrity of the overall software. It is a critical task to select the right properties that reflect the integrity of software in such a way that given integrity requirements are met. To ease this process, the static integrity properties and dynamic integrity properties to classify the properties. Static Integrity Properties are used to ensure the integrity of a ECU prior it's use (e.g., the integrity of an executable binary), while dynamic integrity properties are used to ensure the integrity of a ECU during run-time (e.g., properties that reflect the component's behavior or state transitions).


因此, 完整性是嵌入式系统软件的关键属性。由于恶意或非恶意的故障，这一属性可能遭到破坏。业界提出了许多用于检查或验证软件完整性的方法。然而，完整性作为一种属性无法被直接识别。现有方法通过识别软件其他可计算的属性来解决这一问题，并利用策略描述这些属性如何反映整体软件的完整性。选择能够以符合既定完整性要求的方式准确反映软件完整性的属性，是一项至关重要的任务。为简化这一过程，可将属性分类为静态完整性属性和动态完整性属性。静态完整性属性用于确保软件在使用前的完整性（例如可执行二进制文件的完整性），而动态完整性属性则用于保障软件运行时的完整性（例如反映组件行为或状态转换的属性）


The verification of static integrity or dynamic integrity is generally implemented based on a hardware secure execution environment, where the integrity of the software is validated through message authentication codes or digital signature.


静态完整性或是动态完整性的验证一般都会基于硬件安全运行环境实现，通过消息验证码或是数字签名服务对软件的完整性进行校验。


2.4.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


Software integrity protection should be capable of verifying the authenticity and integrity of the software and, in the event of authenticity and integrity violated, respond according to its design. Protect the authenticity and integrity of the software. Avoding the attacker inspect programs’ execution flow and tamper with anything in program binaries or during runtime, which in turn, enable them to extract confidential data, subvert critical operations and tamper with the input and/or output data.


软件完整性保护应具备验证软件真实性和完整性的能力，并在真实性或完整性遭到破坏时根据其设计采取相应措施。以避免攻击者检查程序的执行流程，篡改程序二进制文件或运行时的任何内容，从而防止他们提取机密数据、破坏关键操作以及篡改输入和/或输出数据。


2.4.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.5 Communication node identification


2.5.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


Communication node identification ensures that the ECU cannot function properly after a simple physical replacement, thereby protecting the authenticity and integrity of the ECU/Component.


通信节点身份识别确保电子控制单元被简单物理替换后无法正常工作，进而保护该ECU/组件的真实性和完整性。


2.5.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


Communication node identification is a security concept, not a fixed security function or control measure. Generally, if the vehicle can recognize when a component is physically replaced, or requires some authorization process to enable the function of the replaced part, such mechanisms can be considered as achieving the security concept of communication node identification.


通信节点身份识别是一项安全概念，而非固定的安全功能或控制措施。通常而言，若车辆能在部件被物理替换时进行识别，或要求通过某种授权流程才能启用被替换部件的功能，这类机制即可视为实现了通信节点身份识别的安全概念。


2.5.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


Communication node identification can prevent attackers from physically replacing the vehicle's ECU, infiltrating the vehicle system and network, tampering with network communication data, disrupting critical operations, or affecting component behavior.


通信节点身份识别能够防止攻击者通过物理替换车辆的电子控制单元，侵入车辆系统和网络，篡改网络通信数据，破坏关键操作或影响组件行为。


2.5.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.6 Communication node whitelist


2.6.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


Communication node whitelist is only allow defined messages to be correctly received, sent, or processed. This mechanism can improve the system stability and robustness of the communication node, enhancing fault tolerance.


通信节点白名单仅允许已被定义的报文被正确接收，发送或进行处理。该机制能够提高通讯节点的系统稳定性和鲁棒性，增强容错。


2.6.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


The communication node whitelist focuses on protecting the receiving nodes in communication. By pre-configuring the whitelist on the receiving nodes, it enables filtering of incoming messages. This approach sacrifices some communication flexibility to enhance the overall system security. Such measures typically help significantly avoid unknown risks, reduce the attack surface, and control boundaries. It also optimizes the allocation of system resources for communication nodes.


通信节点白名单聚焦于通信的接收节点防护。通过将白名单预置于通信接收节点，实现对于接收报文的过滤处理。牺牲一定的通信灵活性以提升系统的整体安全性。这类措施通常能大幅规避未知的风险，收缩攻击面，控制边界。优化通信节点的系统资源分配。


2.6.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


The communication node whitelist prevents system crashes and other availability impacts caused by the node processing unexpected packets when the communication network it is connected to suffers from attacks such as denial of service. Reduce communication node load, filter invalid or dangerous data frames. Reduce the attack surface and collaborate with domain separation to achieve defense in depth.


通讯节点白名单防止通讯节点接入的通讯网络发生拒绝服务等攻击时，通讯节点因处理非预期报文而出现的系统崩溃等可用性影响。降低通信节点负载，过滤无效或危险数据帧。还能缩小攻击面，以配合域隔离措施实现纵深防御。


2.6.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.7 Hardware-Based Secure Elements for Data


2.7.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


Hardware-Based Secure Elements for Data are hardware-based solutions that store sensitive data like cryptographic keys. It provides an environment that protect the integrity and availability of stored data against unauthorized access, editing and deleting. Confidentiality protection is also provided when required.


基于硬件的安全单元用于数据存储，是一种硬件解决方案，专门保存如加密密钥等敏感信息。它构建了一个防护环境，确保存储数据的完整性和可用性，防止未经授权的访问、修改或删除操作。在需要时，该元件还能提供保密性保护措施。


2.7.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


The Hardware-Based Secure Elements technologies mitigate risks like data breaches, unauthorized access, and physical tampering, ensuring the secure data handling requirement. By combining hardware and software solutions.


基于硬件的安全单元技术可降低数据泄露、未经授权访问和物理篡改等风险。通过结合硬件和软件解决方案,确保满足安全数据处理要求。


There are 2 major technologies of Hardware-Based Secure Elements. The Trusted Execution Environment (TEE) and Hardware Security Module (HSM), both are designed to protect sensitive data and cryptographic operations.


硬件安全单元主要有两大技术：可信执行环境（TEE）和硬件安全模块（HSM），两者均旨在保护敏感数据和加密操作。


Trusted Execution Environment (TEE)


可信执行环境


A TEE is a secure area within a processor that ensures sensitive data is processed in isolation from the main operating system (OS). It provides a protected storage enclave and execution environment where data can be handling securely, even if the main OS is compromised.


TEE（可信执行环境）是处理器内的一个安全区域，确保敏感数据在与主操作系统隔离的环境中进行处理。它提供了受保护的存储飞地和执行环境，即使主操作系统遭到入侵，数据仍能在此环境中安全处理。


Hardware Security Module (HSM)


硬件安全模块


A HSM is a dedicated hardware device designed to manage, generate, and protect data. It provides a physically secure environment for cryptographic operations, ensuring keys are never exposed outside the device and hardware level tempering resistance.


HSM是一种专用于管理、生成和保护数据的硬件设备。它为加密操作提供物理安全环境，确保密钥永不暴露于设备之外，并具备硬件级的防篡改能力。


2.7.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


Hardware-based secure elements protect the integrity and availability of data, especially secret keys. They also provide confidentiality protection when required.


基于硬件的安全元件保护数据的完整性和可用性，尤其是密钥。在需要时，还提供机密性保护。


2.7.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.8 Domain separation


2.8.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


Domain isolation and separation are used as defense-in-depth security controls to restrict communication between different security zones, i.e. network segments within the vehicle and between communication nodes of an ECU.


域隔离与分离作为纵深防御安全控制手段，用于限制不同安全区域（即车载网络内部各网段之间以及电子控制单元通信节点之间）的通信交互。


2.8.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


Domain separation only hinders the propagation of attacks by a remote attacker to the core vehicle functions. Domain separation is a defense-in-depth security control to decrease the surface for remote attacks.


域隔离仅能阻止远程攻击向车辆核心功能的扩散，其本质是一种纵深防御机制，旨在缩减远程攻击面。


Here are introductions to two typical domain isolation mechanisms.


以下是两个典型的域隔离机制介绍。


CAN bus domain separation


CAN总线域隔离


The message routing table is a whitelist which ensures that only messages which originate from a specific network segment are routed to other CAN network segments. This prevents communication nodes of one CAN bus segment from posing as a communication node from a different CAN bus segment against other bus segments. For example, a communication node on CAN bus 1 cannot send messages to CAN bus 2 which should originate from another communication node on CAN bus 2 or 3 because the CAN gateway would not route such messages from CAN bus 1 into other CAN busses.


消息路由表是一种白名单机制，其作用是仅允许来自特定网段的报文被转发至其他CAN网络段。该机制能防止某个CAN总线段的通信节点伪装成其他CAN总线段的节点与其他网段进行通信。例如：当CAN总线1上的通信节点试图发送本应源自CAN总线2或3上其他节点的报文时，由于CAN网关不会将此类来自CAN总线1的报文路由至其他总线，因此该报文将无法被传输至CAN总线2。


Some of communication nodes may have private communication channels (e.g., CAN or LIN bus-ses) attached to them as a sub-network. In these cases, the respective communication node functions as the gateway to its respective private communication channel segment. The white-listing mechanism for routing is the same.


部分通信节点可能连接有私有通信通道（如CAN或LIN总线）作为子网络。在这些情况下，相应的通信节点充当其各自私有通信通道段的网关。路由的白名单机制是相同的。


Ethernet domain separation


以太网域隔离


Communication nodes that communicate via on-board Ethernet and have related functions are assigned different IP addresses and corresponding ports. The Ethernet switch's firewall controls information exchange, only allowing data transmission from/to source/destination IP addresses and ports that are authorized on the whitelist.


通过车载以太网进行通讯且具备相关功能的通信节点被分配了不同的IP地址和相应的端口。以太网交换机的防火墙实现对信息交互的管控，仅允许经过白名单授权的源/目标IP地址及端口进行数据传输。


VLAN is also a common Ethernet domain isolation mechanism. It logically divides a physical local area network (LAN) into multiple independent broadcast domains, achieving isolation between these domains. This prevents communication nodes in one broadcast domain from masquerading as nodes in target broadcast domain and interacting with the communication nodes within that domain.


VLAN（虚拟局域网）同样是一种常见的以太网域隔离机制。它通过逻辑方式将物理局域网（LAN）划分为多个独立的广播域，实现这些域之间的隔离。这种机制能有效防止某个广播域内的通信节点伪装成目标广播域节点，并与目标域内的通信节点进行交互。


2.8.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


Domain isolation and separation hinders:


arbitrary addressing of communication participants,


ingression of arbitrary data beyond domain boundaries,


and the propagation of Denial-of-Service attacks (DoS attacks) beyond domain boundaries.


域隔离与分离机制可有效阻止：


对通信参与方的任意寻址行为，


跨域边界传输未经许可的任意数据，


以及拒绝服务攻击（DoS攻击）跨域传播。


Additional to the restriction of the communication, the concept of domain isolation provides spatial and temporal isolation of communication nodes to ensure freedom of interference.


除通信限制外，域隔离概念还通过实现通信节点的空间与时间隔离，确保其免受干扰的自由运作。


2.8.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.9 External wired interface restrictions


2.9.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


The external wired interface restrictions provide a mechanism, to avoid the interface used to conduct unauthorized activity, able to gain privileged access to vehicle systems or critical/sensitive data, allow execution or reading/writing of specified file formats, or provide essential business interfaces upon authorization. Unauthorized communication and access must be prevented. 外部有线接口限制提供了一种机制，旨在防止接口被用于进行未经授权的活动，避免获取车辆系统或关键/敏感数据的特权访问权限，禁止执行或读写特定文件格式，或在未经授权时提供核心业务接口。


2.9.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


With the develop of intelligent connected vehicle, the vehicle has more and more external communication interface. These Interfaces serve spcial needs, e.g., power supply, data exchange, or function expansion.


随着智能网联汽车的发展，车辆拥有越来越多的外部通信接口。这些接口服务于特定需求，如供电、数据交换或功能扩展。以下例举了三个典型的有线外部接口。


The Conductive charging interface


传导式充电接口


The charging interface is used for energy and data exchange between the vehicle and external entities. At the same time, the implementation of functions such as Vehicle to Load (V2L), Vehicle to Vehicle (V2V), Vehicle to Home (V2H), and Vehicle to Grid (V2G) also relies on the data exchange through this interface. Additionally, the more convenient Plug&Charge feature introduces more attack vectors and potential financial damages. To ensure the safety of charging and discharging as well as the security of data exchange, it is necessary to ensure that the above functions comply with the conductive charging standards of each sales country, guaranteeing normal functionality and meeting standard safety requirements. For the Plug&Charge function, a complete identity authenticity verification mechanism is even more essential to protect customers' financial security.


充电接口用于车辆和外部实体的能量和数据交互，同时，Vehicle to Load(V2L), Vehicle to Vehicle(V2V), Vehicle to Home(V2H)和Vehicle to Grid(V2G)等功能的实现也依赖于该接口的数据交互。更进一步，便利的Plug&Charge功能也带来了更多的攻击向量和潜在财务损害。为了保证充放电的安全性和数据交互的安全性，需确保以上功能遵照各销售国的传导式充电标准，保证功能正常使用和满足标准的安全性。对于Plug&Charge功能，更需要有完整的身份真实性验证机制，保障客户的财产安全。


For vehicles in Mainland China that adopt standards such as GB/T 27930, or other communication methods that use the same communication protocol as the onboard communication network.in addition to complying with the standard for communication, the vehicle-side communication node must achieve domain seperation from the onboard communication network. This prevents intrusion into the entire vehicle network through this conductive charging interface, thereby avoiding potential damage.


对于采用了如GB/T 27930标准的中国大陆车辆，或其它采用了与车载通信网络相同通信协议的通信方式。除遵照标准进行通信外，车辆侧通信节点需实现与车载通信网络之间的隔离。防止通过该通信接口侵入整车网络，造成损害。


The OBD-II interface


车载诊断接口


The OBD-II interface remains a cornerstone of vehicle diagnostics, balancing legacy compatibility with evolving needs in connectivity and electrification. Its standardized design ensures interoperability across brands while facing new challenges in cybersecurity and data privacy.


OBD-II（On-Board Diagnostics II）是车载诊断系统的第二代标准，1996年起成为美国、欧盟及中国等地区汽车的强制配置。其核心功能是监控车辆排放系统及关键部件的运行状态，并通过标准化接口提供故障诊断能力。


The OBD-II interface provides access to the vehicle, enabling attackers to


Tempering sensitive data (VIN, mileage).


Reprogram ECUs to disable safety systems (e.g., airbags, ESC).


Clone keys or manipulate immobilizers.


Bypass emissions controls.


Override speed limiters or disable diagnostic trouble codes (DTCs).


Install malware for persistent remote access.


OBD-II接口可访问车辆系统，使攻击者能够：


篡改敏感数据（车辆识别号VIN、里程数）。


重新编程ECU以禁用安全系统（如安全气囊、电子稳定控制ESC）。


克隆钥匙或操纵动力止动装置。


绕过排放控制。


解除限速器或清除故障诊断码（DTC）。


植入恶意软件以实现持久远程控制。


Therefore, the OBD interface needs to implement reliable access control measures to ensure it can provide necessary services while preventing malicious access. By setting up diagnostic routes, data access through the OBD interface can also be seperated from the onboard communication, achieving in-depth defense.


因此，OBD接口需植入可靠的访问控制措施，保证该接口能够提供必要服务的同时防止恶意访问。通过设置诊断路由还能够将OBD接口的数据访问与车载网络进行隔离，实现纵深防御。


The USB Port


USB端口


The in-vehicle infotainment system establishes a wired connection with external consumer electronic devices (such as mobile storage or smartphones) via a USB interface to enable reading and writing of relevant files. The USB interface can also serve as an interface for debugging purposes during development phase, such as the ADB interface for Android systems or providing an interface for SSH services. 车载信息娱乐系统通过USB接口与外部消费电子设备（如移动存储或智能手机）有线连接, 实现相关文件的读写。同时，USB端口在开发过程中还可作为调试接口使用，例如支持Android系统的ADB调试功能或提供SSH服务接入。


To prevent external tools or malicious files from gaining unauthorized access to the ECU through USB ports to implant trojans or viruses, USB port restrictions must be implemented.


为防止外部工具或恶意文件通过USB接口未经授权访问ECU，植入木马或病毒。需采用USB接口限制措施限制USB接口。


2.9.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


The external wired interface restrictions can prevent unauthorized access and modification through external wired interface, defining readable and writable file formats helps protect the system from being affected by malicious files. To ensure system operation and code security while avoiding the leakage of critical/personal privacy data.


外部有线接口限制可防止通过外部有线接口进行未授权访问和修改，定义可读写文件格式有助于保护系统免受恶意文件影响。在确保系统运行和代码安全的同时，避免关键/个人隐私数据泄露。


2.9.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.10 Security of Cellular Communication


2.10.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


Security of cellular communication ensures the integrity of data transmitted via cellular network between vehicle communication nodes and external communication nodes or entities, and verifies the authenticity of communication node identities to protect transmitted data.


蜂窝通信安全确保车载通信节点与外部通信节点或实体通过蜂窝数据网络传输数据的完整性，验证通信节点身份的真实性，以保护传输数据。


If the transmitted data involves confidential information (e.g., cryptographic keys, Sensetive Personally Identifiable Information), appropriate confidentiality protection measures must also be implemented.


若传输数据涉及机密信息（如密钥, 敏感个人信息）的情况，还需实施适当的机密性保护措施。


2.10.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


A Man-in-the-Middle Attack (MITM attack) is an "indirect" form of intrusion where the attacker uses various technical means to virtually place a communication node they control between two communicating nodes in a network connection. This intervening communication node is referred to as the "man-in-the-middle." A man-in-the-middle attack can achieve eavesdropping, replaying, tampering with, and impersonating communication data, thereby compromising the authenticity, integrity, and confidentiality of the communication.


中间人攻击（Man-in-the-MiddleAttack，简称“MITM攻击”）是一种“间接”的入侵攻击，这种攻击模式是通过各种技术手段将受入侵者控制的一个通信节点，虚拟放置在网络连接中的两个通信节点之间之间，这个通信节点就称为“中间人”。中间人攻击能够实现对通信数据的监听，重放，篡改和仿冒，破坏通信的真实性，完整性和机密性。


The cellular data networks. It is specifically designed for communication between vehicles and external communication nodes or entities, following globally standardized system architectures, machine communication protocols, and data interaction standards. The goal is to build a bridge for data sharing and interaction, enabling intelligent dynamic information services. The risks faced by this type of communication are also increasing in number and complexity.


蜂窝数据网络的通信技术，即按照全球统一规定的体系架构机器通信协议和数据交互标准专门用于车辆与外部通信节点或实体之间的通信。这类通信往往会基于IP协议进行，旨在构建数据共享交互桥梁，实现智能化的动态信息服务。这些通信面临的风险也越来越多，越来越复杂


Therefore, security protocols targeting IP or higher layers—such as IPSec, transport-layer-based TLS, mTLS, DTLS, and application-layer-based DDS-Security, can all be employed to meet the integrity and authenticity protection requirements outlined by this security concept. These security protocols can typically also be configured to support confidentiality protection.


因此，针对IP或更上层协议的安全协议，如IPSec, 基于传输层的TLS，mTLS，DTLS等，均可用于支持该安全概念所要求的完整性和真实性保护需求。这些安全协议通常也能通过配置用于支持机密性保护。


2.10.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


The security of cellular communication ensures the authenticity of communication nodes, as well as the confidentiality and integrity of communication data. It prevents MITM (Man-in-the-Middle) attacks from compromising the integrity and confidentiality of communications. At the same time, this mechanism also provides corresponding forward secrecy.


远程无线通信安全保护通信节点的真实性，通信数据的机密性和完整性。防止MITM攻击产生的通信完整性和机密性损害。同时，该机制也会提供相应的前向安全性。


2.10.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.11 Security of vehicle local area wireless communication


2.11.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


Security of vehicle local area wireless communication ensures the integrity of data transmitted between onboard communication nodes and external communication nodes or entities, and verifies the authenticity of communication node identities to protect transmitted data.


本地无线通信安全确保车载通信节点与外部通信节点或实体传输数据的完整性，验证通信节点身份的真实性，以保护传输数据。


If the transmitted data involves confidential information (e.g., cryptographic keys, Sensetive Personally Identifiable Information), appropriate confidentiality protection measures must also be implemented.


若传输数据涉及机密信息（如密钥, 敏感个人信息）的情况，还需实施适当的机密性保护措施。


2.11.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


Local area wireless communication technology typically refers to local area communication technology, e.g., classic Bluetooth, Bluetooth Low Energy(BLE), WLAN, V2X, etc.. It is specifically designed for communication between vehicles and external communication nodes or entities, following the public communication protocols, and data interaction standards.


本地无线通信技术通常指经典蓝牙、低功耗蓝牙(BLE)、无线局域网(WLAN)、车联网(V2X)等局域无线通信技术。这类技术专为车辆与外部通信节点或实体之间的通信而设计，遵循公开的通信协议及数据交互标准。


Correspondingly, each public communication protocol and data interaction standard provides security mechanisms. In principle, the latest versions of communication protocols and data interaction standards should be prioritized during development, and the security mechanisms provided by these standards should be enabled. For example, Bluetooth offers SSP, while WLAN provides security mechanisms such as WPA2/WPA3.


相应的，每种公开的通信协议和数据交互标准都会提供安全机制。原则上，开发时应优先采用最新版本的通信协议和数据交互标准，并启用标准中提供的安全机制。如蓝牙提供了SSP，WLAN提供了WPA2/WPA3等安全机制。


If functional design requirements prevent the implementation of security measures provided in the communication protocol and data interaction standards, or if there is an end-to-end protection requirement for the entire data transmission chain—such as when data transmitted via BLE must be forwarded through an onboard wired communication network to reach the receiving node—then corresponding protection mechanisms must be developed at the higher layer (e.g., Application layer) to ensure the integrity of data transmitted through these communication channels. For cases involving the transmission of confidential information (e.g., cryptographic keys, Sensetive Personally Identifiable Information), appropriate confidentiality protection mechanisms must also be implemented.


若因功能设计需求，导致无法通过实施通信协议和数据交互标准中提供的安全设计。或对于数据传输整体链路存在端到端保护需求的，如通过BLE传输的数据还需要经由车内有线通信网络进行转发才能到达接收节点的情况。则必须在更高的网络层级（如应用层）开发相应的保护机制，以确保通过这些通信信道传输数据的完整性。对于传输机密信息（如密钥, 敏感个人信息）的情况，还必须实施适当的保密性保护机制。


2.11.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


The security of Local area wireless communication technology ensures the authenticity of communication nodes, as well as the confidentiality and integrity of communication data. It prevents MITM (Man-in-the-Middle) attacks from compromising the integrity and confidentiality of communications.


本地无线通信安全保护通信节点的真实性，通信数据的机密性和完整性。防止MITM攻击产生的通信完整性和机密性损害。


2.11.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.12 Security of onboard communication


2.12.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


The security of onboard communication ensures integrity of data transmitted between onboard communication nodes, and communication node authenticity, When necessary, confidentiality can also be provided.


车载通信安全确保了车内通信节点间传输数据的完整性及通信节点的真实性，在必要时还可提供机密性。


2.12.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


Modern onboard networks rely on diverse communication protocols to enable advanced functionalities. The Controller Area Network (CAN), designed for real-time control systems like engine management, offers robustness and prioritized messaging but suffers from limited bandwidth (≤2 Mbps) and lacks encryption. The Local Interconnect Network (LIN) complements CAN for low-speed non-critical tasks (e.g., seat adjustments) with cost efficiency, though its minimal security and low bandwidth (≤20 kbps) pose risks. High-speed applications such as ADAS leverage FlexRay, which provides deterministic transmission and dual-channel redundancy (up to 10 Mbps), but its complexity and cost hinder widespread adoption. Media Oriented Systems Transport (MOST), tailored for infotainment, supports high bandwidth (150 Mbps) via optical/electrical layers but remains underutilized in security-critical domains. Emerging Automotive Ethernet underpins autonomous driving with IP-based protocols (e.g., SOME/IP) and scalable bandwidth (1 Gbps+), yet demands rigorous security to counter IP-related vulnerabilities.


现代车载网络依赖多种通信协议实现高级功能。控制器局域网（CAN）专为发动机管理等实时控制系统设计，具备鲁棒性和优先级消息机制，但存在带宽受限（≤2 Mbps）且缺乏加密的缺陷。局部互联网络（LIN）作为CAN的低速补充，用于座椅调节等非关键任务，成本效益显著，但其极低的安全性及有限带宽（≤20 kbps）带来风险。FlexRay凭借确定性传输和双通道冗余（最高10 Mbps）支撑ADAS等高速应用，但复杂度与成本阻碍了普及。面向娱乐系统的MOST协议通过光/电物理层支持高带宽（150 Mbps），但在安全关键领域应用有限。新兴的汽车以太网以SOME/IP等基于IP的协议和可扩展带宽（1 Gbps+）支撑自动驾驶，但需严格的安全措施应对IP相关漏洞。


However, these networks face escalating cybersecurity threats. Unauthorized access exploits ECU vulnerabilities, enabling malicious control. Data manipulation disrupts operations through malicious CAN/Ethernet message injection. Eavesdropping on unencrypted traffic (e.g., CAN bus, Ethernet) exposes sensitive data, while denial-of-service (DoS) attacks flood networks to cripple ECUs. The spoofing or replay of CAN/Ethernet messages poses serious safety and financial threats to vehicle systems.


然而，这些网络正面临日益严峻的网络安全威胁。未经授权的访问利用ECU漏洞，可实现恶意控制。通过注入恶意CAN/Ethernet报文的数据篡改行为会扰乱系统运行。未加密通信流量（如CAN总线、以太网）的窃听会暴露敏感数据，而拒绝服务（DoS）攻击通过泛洪网络使ECU瘫痪。CAN/Ethernet报文的欺骗或重放攻击更会对车辆系统构成重大安全与经济损失威胁。


Although such attacks are mainly initiated by local attackers, the potential benefits behind them, especially financial ones, have led to an increasing for MATE (Man-At-The-END) attacks. Consequently, there is a growing need for protective mechanisms to be implemented in the conmmunication data and communication nodes of onboard networks.


尽管这类攻击主要由本地攻击者发起，但其背后的潜在利益，尤其是经济利益，已导致MATE（终端用户）攻击日益增多。因此，在车载网络的通信数据和通信节点中实施保护机制的需求正不断增长


2.12.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


The security of onboard communication ensures integrity of data transmitted between onboard communication nodes, communication node authenticity through cryptographic such as symmetric/asymmetric encryption and message authentication codes (MAC). When necessary, confidentiality protection should also be provided.


车载通信的安全性通过对称/非对称加密和消息认证码（MAC）等密码技术，确保车载通信节点间传输数据的完整性及通信节点真实性。必要时还应提供保密性保护。


2.12.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.13 Transport layer port restriction


2.13.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


The transport layer port restrictions ensure that the system only supports access to ports necessary for business, disables all other ports, and limits potential attack vectors.


传输层端口限制保证系统仅开放业务必须的端口，禁用其它所有端口，限制潜在的攻击向量。


2.13.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


Ports, as the core identifiers of the transport layer, are standardized by RFC 793 (TCP) and RFC 768 (UDP) to enable multiplexing and demultiplexing. Their core functions include:


Endpoint Addressing: Using 16-bit integers (0–65535) to distinguish between different application processes on the same IP address.


Protocol Binding: Strictly differentiating between TCP and UDP ports—even if the port numbers are the same, they are treated as independent channels.


端口作为传输层的核心标识符，由 RFC 793（TCP）和 RFC 768（UDP）标准化，实现多路复用（Multiplexing）与解复用（Demultiplexing）。其核心功能为：


端点寻址：通过16位整数（0~65535）区分同一IP上的不同应用进程；


协议绑定：严格区分TCP/UDP端口，即使端口号相同亦视为独立通道；


Port scanning is a preliminary step in many attacks. Attackers can use common port scanning tools to probe a system's open ports, obtaining service versions to match vulnerabilities or exploiting weak passwords and brute-force attacks to gain unauthorized access.


端口扫描是很多攻击的前置步骤，攻击者可以通过常见的端口扫描工具对系统的开放端口进行扫描，获得相关服务的版本用于匹配漏洞，或者利用弱密码扫描和暴力破解等方式入侵系统。


2.13.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


原则上，未知即威胁。所以，关闭非业务必须端口能够帮助系统缩减潜在攻击面。同时，结合防火墙和域隔离等机制，实现纵深防御。


In principle, the unknown equates to a threat. Therefore, closing non-essential business ports can help reduce a system's potential attack surface. Additionally, by integrating mechanisms such as firewalls and domain isolation, a defense-in-depth strategy can be achieved.


2.13.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |


2.14 Security of Over-the-Air (OTA) Update System


2.14.1 Definition


| 描述这个安全功能的定义，如验证数据的真实性 |


The Security of Over-the-Air (OTA) Update System provides an authentication mechanism between the vehicle's OTA software update system and the OTA backend system. After the update data is downloaded to the vehicle's OTA software update system, it is also necessary to verify the integrity and authenticity of the downloaded update data.


空中下载（OTA）更新系统安全提供车载OTA软件升级系统与OTA后端系统的认证机制。完成升级数据下载至车载OTA软件升级系统后，同样需要验证下载升级数据的完整性和真实性。


2.14.2 Explanation


| 解释这个安全功能，非常High Level的大概机制 |


An over-the-air (OTA) update is the wireless delivery of new software, firmware or other data to the vehicle. OTA updates have become critical in maintaining and enhancing vehicle functionality, security, and performance. An OTA backend system operated by the manufacturer issues a new software or firmware update. The update is uploaded to the cloud where it is queued, downloaded, and verified by the target vehicle over a cellular connection. Once verified, the vehicle typically triggers an alert that prompts the owner to approve or decline the update. After confirming approval—whether manually or automatically—the onboard OTA software update system installs the update and sends back diagnostic information to the manufacturer.


空中下载（OTA）更新是指通过无线方式向车辆传输新软件、固件或其他数据的技术。这种技术对于维护和提升车辆功能、安全及性能至关重要。由制造商运营的OTA管理系统发布新软件或固件更新后，更新包会被上传至云端，目标车辆通过蜂窝移动网络将其下载并进行验证。验证完成后，车辆通常会触发提示，请求车主批准或拒绝更新。在获得确认（无论是手动还是自动）后，车载更新系统将执行安装，并向制造商回传诊断信息。


The onboard OTA software update system and the OTA backend system shall implement an authentication mechanism. Authentication is required before each update data download. If communication is interrupted during the download, reauthentication is necessary to resume the update data download. After the onboard OTA software update system completes downloading the update data, it shall verify the integrity and authenticity of the downloaded update data.


车载OTA软件升级系统与OTA后端系统必须建立认证机制。每次更新数据下载前应进行身份验证。若下载过程中通信中断，必须重新认证方可恢复更新数据下载。车载OTA软件升级系统完成升级数据的下载后，应对下载的升级数据进行完整性和真实性校验。


2.14.3 Relevant Assets and Threats


| 描述这个安全功能可以防御的威胁 |


The security of over-the-air (OTA) Update System ensures security by implementing authentication mechanisms between onboard OTA software update system and the OTA backend system, and verifying the authenticity and integrity of downloaded data, protecting OTA update data from man-in-the-middle attacks during transmission and guaranteeing the secure execution of OTA updates.


空中下载（OTA）更新系统安全提供了车载OTA软件更新系统与OTA后端系统之间身份认证机制，对下载数据的真实性和完整性进行验证。这种概念设计能有效防范传输过程中的中间人攻击，确保OTA更新数据的安全传输，从而保障整个更新流程的安全执行。


2.14.4 Relevant Specification and Information


| 如有对应安全功能SPEC，描述这个安全功能的文件名称，如果没有可以描述性总结； |

