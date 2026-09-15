---
source_url: ""
ingested: 2026-08-06
sha256: a75a86498b8532bc8d796d114e56f862036efcfbe0db43b8b6c9b79247d4b6df
---

# REQ_07_LAH_080_VCS_004_02_Secure_Boot_Spec

<!-- Page 1 -->

![image](REQ_07_LAH_080_VCS_004_02_Secure_Boot_Spec/images/page1_img1.png)

CEA 整车网络安全
网络安全技术定义_安全启动规范
1 | P a g e
整车网络安全技术定义
安全启动规范
更新记录:
日期
版本号
修订类别
作者
描述
18/10/24
V0.3D
I
黄偲
初始版本
23/10/24
V1.0F
M
黄偲
安全 tech 组评审
11/09/2025
V2.xD
M
黄偲
安全 tech 组评审
V2.1D
M
黄偲
体现变更点
V2.2D
M
黄偲
试生成发布版本
V2.3D
M
黄偲
组内评审版本，删除示例图
V2.0F
I
黄偲
释放版
类别：
I - 初始
A - 增加
M - 修改
D - 删除


<!-- Page 2 -->

CEA 整车网络安全
网络安全技术定义_安全启动规范
2 | P a g e
1 通用 .................................................................................................................................................................. 3
1.1 定义和其他适用文件 ............................................................................................................................. 3
1.2 目的 .......................................................................................................................................................... 3
1.2.1
安全启动概述 .................................................................................................................................. 4
1.2.2
认证启动概述 .................................................................................................................................. 4
1.3 范围 .......................................................................................................................................................... 5
2 组织和文件要求 ............................................................................................................................................. 5
2.1 组织要求 .................................................................................................................................................. 5
2.2 文档要求 .................................................................................................................................................. 5
3 技术要求.......................................................................................................................................................... 5
3.1 通用系统需求 .......................................................................................................................................... 5
3.1.1
功能要求 ........................................................................................................................................... 5
3.1.2
密码学资产的处理 .......................................................................................................................... 6
3.1.4.1
数据 ............................................................................................................................................ 6
3.1.4.1.1
密钥 .................................................................................................................................... 6
3.1.4.1.2
私钥 .................................................................................................................................... 6
3.1.4.1.3
可信根 ................................................................................................................................ 6
3.1.4.1.4
公钥和证书 ........................................................................................................................ 6
3.1.4.1.5
参考值/认证代码 .............................................................................................................. 7
3.1.4.1.6
数字签名 ............................................................................................................................ 7
3.1.4.2
算法 ............................................................................................................................................ 7
3.1.4.2.1
参考值的生成 .................................................................................................................... 7
3.1.4.2.2
对称加密函数 .................................................................................................................... 7
3.1.4.2.3
非对称加密函数................................................................................................................ 7
3.2 安全启动要求 .......................................................................................................................................... 8
3.2.1
具体的硬件要求 .............................................................................................................................. 8
3.2.2
具体的软件要求 .............................................................................................................................. 8
3.3 认证启动需求 .......................................................................................................................................... 8
3.3.1
具体的硬件要求 .............................................................................................................................. 8
4 解决方案示例 ................................................................................................................................................. 9
4.1 基于微控制器的 ECU 示例场景示例 .................................................................................................... 9
5 附件 .................................................................................................................................................................. 9
5.1 参考 .......................................................................................................................................................... 9


<!-- Page 3 -->

CEA 整车网络安全
网络安全技术定义_安全启动规范
3 | P a g e
1 通用
缩写
Abbreviation Description Table:
Abbreviation
Description
CMAC
Cipher-based Message Authentication Code
CPU
Central Processing Unit
ECU
Electronic Control Unit
HCP
High performance Computing Platform
HMAC
Hash-based Message Authentication Code
MAC
Message Authentication Code
OEM
Original Equipment Manufacturer
(here: Vehicle Manufacturer)
PKI
Public Key Infrastructure
1.1 定义和其他适用文件
本文档中的关键词“必须”、“不得”、“必需”、“应”、“不应”、“应该”、“不建议”、“建议”、“可以”
和 “可选”应按照 RFC2119 [1] 中的描述进行解释。
关键词依次对应的英文为： “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”,
“SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” 。
1.2 目的
本文档的目的是为保护电子控制单元 （ECU）的软件和固件的完整性和真实性提供安全要求。
这包括以下要求：
•
安全启动 （Secure Boot）
必须对软件和固件进行验证，该验证过程在启动序列（初始化）过程中逻辑块执行前完成。
•
认证启动 （Authenticated Boot）
必须对软件和固件进行验证，该验证过程可在执行时并行进行，或在执行后的一定时间偏移内完


<!-- Page 4 -->

CEA 整车网络安全
网络安全技术定义_安全启动规范
4 | P a g e
成。
完整性保护应涵盖所有可编程/可交换的非动态存储区域，其中存储了 ECU 按预期方式运行必
须的软件和固件。 这包括
•
硬件制造商/芯片供应商（例如BIOS、Core Bootloader）
•
Tier1/ ECU 供应商（例如客户引导加载程序Customer flash loader、操作系统）
•
OEM / ECU 应用（例如OEM 应用）
如果某软件/固件组件已成功验证，且其之前的所有组件都已成功验证，则该组件可被视为
可信。否则，该组件不应被视为可信。
1.2.1 安全启动概述
安全启动应确保ECU 上的软件和固件不会因为篡改或故障导致非预期更改。
因此 ECU 软件可划分为多个逻辑块，每个逻辑块均须通过独立的完整性保护机制进行防护。
为实现安全启动，完整性验证必须在逻辑块本身被执行或启动前完成。
为实现安全启动，完整性保护机制的验证必须在逻辑块被执行或启动前完成。
若逻辑块验证失败，则必须禁止执行该逻辑块。
注意：某些硬件组件或系统解决方案声称实现了 “Secure Boot”，但不符合本文档中给出的定义。这
些解决方案（例如 SHE1.1）没有原生或本地硬件支持，无法防止在安全启动验证失败后执行代码，由
于 SHE1.1 规范，安全启动验证的结果仅限制密钥访问。
1.2.2 认证启动概述
认证启动应确保ECU软件的任何变更在启动过程中或结束后立即被检测，从而触发特定响应动
作。
认证启动的完整性验证必须在启动过程中或刚结束时执行。
区别于安全启动（第 1.3.1 章）,认证启动必须满足：
1. ECU内部的信任锚（Trusted Element） 需验证所有逻辑块的完整性；
2. 存储每个逻辑块的独立验证结果；
3. 信任锚汇总每一个完整性验证结果，若发现特定失败，则执行关闭系统或切换至后备系
统或封锁敏感数据（如加密密钥钥）的预设动作
在认证启动过程中验证失败后的动作，必须由OEM侧ECU涉及 的FO(Function Owner)、OEM 的安
全部门和功能安全负责人批准（如果适用）。


<!-- Page 5 -->

CEA 整车网络安全
网络安全技术定义_安全启动规范
5 | P a g e
1.3 范围
本文档旨在应用于所有ECU，包括基于微处理的运算平台（例如， HCP）和基于微处理器的
ECU（例如，在传感器-执行器层面中）。
本文档中描述的机制应能够检测ECU 软件和固件的任何完整性损失，但由错误引起的措施不
在本规范范围内。即使给出了可能的对策/应对方法的示例 ，也必须与 ECU 的职能所有者澄清。
在 ECU 运行期间必须更改的动态内存区域和客户数据不在本文档中描述的完整性机制的范围。
2 组织和文件要求
2.1 组织要求
为了能够确定哪些措施适用于某个ECU，必须执行威胁和风险分析（例如基于TARA、
STRIDE,..）。
供应商在开始实施之前，必须准备一个安全概念，描述固件/软件的哪一部分受到安全启动/认
证启动的保护，以及如果验证失败会发生什么。 此概念必须得到 OEM 的批准。
2.2 文档要求
ECU 的供应商必须向 OEM 提供其 ECU 的威胁和风险分析的结果文档。
ECU 的供应商必须向客户提供安全启动方案文档，其中详细说明了如何满足本文档中的每个要
求。
ECU 的供应商必须记录每个CPU，使用哪些方法来确定安全启动相关的固件和软件的真实性和
完整性。
所有与本文件要求相悖的行为必须由供应商记录并得到客户的批准。
3 技术要求
3.1 通用系统需求
每个可编程ECU 都必须确保其所有CPU（微处理器、微控制器或 其他）只能执行完整性被成
功验证的软件和固件。
每个 CPU 必须根据本文档中指定的至少一种方法来验证其软件和固件（可执行程序代码和静
态配置数据）的真实性和完整性。
验证软件和固件真实性和完整性的方法包括安全启动、认证启动。
在相应组件中实施哪些方法或方法由 OEM 决定，并在相应的组件规范中定义。
3.1.1 功能要求


<!-- Page 6 -->

CEA 整车网络安全
网络安全技术定义_安全启动规范
6 | P a g e
所有完整性机制必须支持ECU 应用软件的完整更新和分块更新。
所有完整性机制的设计必须支持ECU应用软件的空中下载（OTA）更新。
所有完整性机制应尽可能与完整/分块更新的逻辑对齐。
所有完整性机制应设计为在软件更新成功后安全触发内部参考值刷新。
所有完整性机制应能够在验证成功后发送可信状态消息。
3.1.2 密码学资产的处理
如果通用安全需求中尚未定义，则必须根据本文档处理所有密码学资产。
3.1.4.1 数据
3.1.4.1.1 密钥
若采用对称加密方案，用于安全启动/认证启动保护的所有对称密钥必须是单个ECU唯一的。
若采用对称加密方案，所有密钥需在ECU内部的可信环境中生成，且必须由专用硬件提供支
持。
测试密钥可由OEM PKI（公钥基础设施）在ECU外部生成，但严禁在量产期间或之后将测试
密钥分发到生产型ECU中。
3.1.4.1.2 私钥
若采用非对称加密方案，用于安全启动/认证启动保护的所有非对称密钥的私钥必须是单个
ECU唯一的，且存储于ECU内部。
若采用非对称加密方案，用于安全启动/认证启动保护的所有非对称密钥的私钥需在ECU内部
的可信环境中生成，且必须由专用硬件提供支持。
所有必须在后端使用的非对称私钥，如使用非对称方法实现安全启动/认证启动，应在 OEM
PKI 中生成，并且只能在硬件安全模块中使用。
测试密钥可由OEM PKI（公钥基础设施）在ECU外部生成，但严禁将测试密钥分发到量产
ECU中在（量产期间或之后）。
3.1.4.1.3 可信根
信任根应被视为长期安全措施。
禁止通过常规软件升级或调试接口在 ECU 内部更换可信根。
任何可信根更换方案必须获得 OEM批准。
可信根的更换方案设计必须基于以下双重验证：
1. 对相应私钥或机密信息本身的知识证明；
2. 至少一项对 ECU 内部额外密钥的附加证明。
3.1.4.1.4 公钥和证书


<!-- Page 7 -->

CEA 整车网络安全
网络安全技术定义_安全启动规范
7 | P a g e
公钥或证书在被认定为有效前，必须通过完整性验证。此验证需依赖密码学机制（如数字签
名），确保密钥未被篡改。
公钥在ECU内必须以公钥证书（Public Key Certificates）形式存储，且证书格式需经OEM功能负责
人批准。格式要求参见证书规范。
公钥证书可以存储在 ECU 内的任何内存区域中，但使用前必须向上验证至可信根，形成完整信任
链。
如果公钥证书不是已成功验证的数据区域（固件和软件）的一部分，又无法根据信任可信根进
行验证，则该证书不应被可信任，ECU应杜绝相关操作。
3.1.4.1.5 参考值/认证代码
若完整性保护基于对称加密方案实现，参考值应实现为CMAC/HMAC。
若完整性保护基于非对称加密方案实现，参考值应实现为数字签名。
必须保证参考值的完整性。
仅允许支持完整性保护的可信硬件更新参考值。
禁止通过诊断命令或调试接口写入参考值。
3.1.4.1.6 数字签名
数字签名可以存储于ECU任意存储区域，但在被视为有效前，应始终验证到信任根。
若无法验证至可信根，签名及相关数据应视为不可信。
3.1.4.2 算法
3.1.4.2.1 参考值的生成
如果使用对称加密方案进行完整性校验，参考值的生成应使用 MAC 算法并满足相应算法。
如果使用不对称加密方案进行完整性检查，参考值的生成应使用经批准的数字签名方法并符合
签名算法要求。
在 ECU 内部执行的对称参考值计算（生成/验证）应在受信任的的环境中执行，并由特定的硬
件支持。
在 ECU 内部执行的非对称参考值生成应在受信任的的环境中执行，并由特定的硬件支持。
在 ECU 中执行的非对称参考值验证可以在已被校验完整性的软件中执行。
3.1.4.2.2 对称加密函数
在 ECU 内部执行的对称加密功能（加密/解密）应在受信任的的环境中执行，并由特定的硬件
支持。
3.1.4.2.3 非对称加密函数


<!-- Page 8 -->

CEA 整车网络安全
网络安全技术定义_安全启动规范
8 | P a g e
在 ECU 内部使用私钥（解密/签名）执行的非对称加密操作应在受信任的的环境中执行，并由
特定的硬件支持。
在 ECU 内部使用公钥（加密/验签）执行的非对称加密操作，可以在已被校验完整性的软件中
执行。
3.2 安全启动要求
实现安全启动的组件必须仅执行在启动过程中已完成验证的代码（执行前验证）。
必须满足第 3.1 章的所有系统要求（例如密钥/可信根/证书/参考值/算法等）。
3.2.1 具体的硬件要求
在初始基于硬件的（原生的）安全启动失败时，硬件应支持阻止代码执行的机制，如熔断锁死，
硬件看门狗触发复位，切换至只读安全固件分区。
3.2.2 具体的软件要求
如果软件块无法成功验证，那么安全启动必须中止。
安全启动的实现不能违反 ECU 的其他功能需求，如启动时间的限制。
为了验证受测软件的完整性，完整性验证功能必须将测量的完整性摘要与存储于可信硬件中的
已有完整性摘要（参考值）进行比较。如果测量的完整性摘要与存储于可信硬件中的完整性摘
要不匹配，那么安全启动必须失败。
3.3 认证启动需求
实现认证启动的组件必须校验启动过程中的所有可执行代码，验证可在代码执行时或执行后立
即完成（非执行前强制）。
必须满足第 3.1 章的所有系统要求（例如密钥/可信根/证书/参考值/算法等）。
认证启动的实现不能违反 ECU 的其他功能需求。
ECU需在安全启动校验成功后，方可发送被系统认证为可信且有效的通信报文。若启动失败，ECU
不应发送业务报文。
3.3.1 具体的硬件要求
认证启动必须由可信的独立硬件支持，该硬件需执行完整性测量和验证执行。
使用的硬件必须得到 OEM 的批准。


<!-- Page 9 -->

CEA 整车网络安全
网络安全技术定义_安全启动规范
9 | P a g e
4 解决方案示例
4.1 基于微控制器的 ECU 示例场景示例
以下段落概述了一个符合这一要求规范的可能解决方案-只要所有实施斜街都符合附加相关文
件的要求。
ECU：基于微控制器的 AUTOSAR 架构
HSM：硬件安全模块，例如：EVITA medium
场景：
•
硬件一级供应商的微控制器
•
一级供应商的 ECU
•
ECU 应用 OEM 特定
解决方案方法：
•
ECU 支持包含 HSM
•
对于 ECU bootloader(由硬件一级供应商)和客户 bootloader(一级供应商)使用对称密钥
•
这些密钥独立于 ECU，应由 HSM 创建
•
密钥由 HSM 存储和保护
•
CMACS 由 ECU 为 ECU bootloader(由硬件一级供应商)和客户 bootloader(一级供应商)生
成，并在 HSM 中存储和保护
•
ECU bootloader 的验证由 HSM 硬件直接执行
•
控制权被移交给 ECU bootloader
•
ECU bootloader 使用 HSM 硬件（算法，存储对称密钥，存储 CMAC）来验证客户
bootloader(一级供应商)
•
控制权被移交给客户 bootloader
•
OEM 应用程序的验证是不对称的
•
OEM 应用程序由 OEM 使用不对称私钥签名，安全存储在 OEM PKI 中。
•
用于验证该签名的相应公钥存储在客户 bootloader 中
•
客户 bootloader 现在负责 OEM 应用程序的验证-这可以通过软件来完成，但仍然建议
使用加密硬件来执行算法
5 附件
5.1 参考
References Table:
Ref. Document/Source
Version
[1]
Secure Boot specification
- Secure Boot, Authenticated Boot
V1.0F


<!-- Page 10 -->

![image](REQ_07_LAH_080_VCS_004_02_Secure_Boot_Spec/images/page10_img1.png)

INTERNAL
Secure Boot specification
- Secure Boot, Authenticated Boot
Author
Huang, Cai
Date of revision
25.10.2024
Version
V1.0F
CONFIDENTIAl


<!-- Page 11 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 2
INTERNAL
1 General ...................................................................................................................................................................................... 4
1.1 Abbreviations ................................................................................................................................................................... 4
1.2 Definitions and Further Applicable Documents ...................................................................................................... 4
1.3 Purpose .............................................................................................................................................................................. 4
1.3.1
Overview Secure Boot ............................................................................................................................................. 5
1.3.2
Overview Authenticated Boot ............................................................................................................................... 6
2 Requirements for Organization and Documentation .................................................................................................... 6
2.1 Regulatory Requirements ............................................................................................................................................. 6
2.2 Organizational Requirements ...................................................................................................................................... 6
2.3 Documentation Requirements ..................................................................................................................................... 7
3 Technical Requirements ........................................................................................................................................................ 8
3.1 General System Requirements ...................................................................................................................................... 8
3.1.1
Functional Requirements ....................................................................................................................................... 8
3.1.2
Handling of cryptographic assets ........................................................................................................................ 8
3.1.2.1
Data ...................................................................................................................................................................... 8
3.1.2.1.1
Secret Keys .................................................................................................................................................. 8
3.1.2.1.2
Private Keys ................................................................................................................................................. 9
3.1.2.1.3
Root of Trust ............................................................................................................................................... 9
3.1.2.1.4
Public Keys and Certificates ..................................................................................................................... 9
3.1.2.1.5
Reference Values / Authentication Codes .......................................................................................... 10
3.1.2.1.6
Digital Signatures .................................................................................................................................... 10
3.1.2.2
Algorithms ........................................................................................................................................................ 10
3.1.2.2.1
Generation of Reference Values ........................................................................................................... 10
3.1.2.2.2
Symmetric Crypto Functions ................................................................................................................ 11
3.1.2.2.3
Asymmetric Crypto Functions .............................................................................................................. 11
3.1.2.2.4
Secure Boot Requirements .................................................................................................................... 11
3.1.3
Specific Hardware Requirements ....................................................................................................................... 11
3.1.4
Specific Software Requirements ......................................................................................................................... 11
3.2 Authenticated Boot Requirements ........................................................................................................................... 12
3.2.1
Specific Hardware Requirements ....................................................................................................................... 12
4 Example Solution Scenarios ................................................................................................................................................ 13
4.1 Example scenario for microcontroller based ECU .................................................................................................. 13


<!-- Page 12 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 3
INTERNAL
5 Appendix ................................................................................................................................................................................. 14
5.1 References Table ............................................................................................................................................................ 14


<!-- Page 13 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 4
INTERNAL
6 General
6.1 Abbreviations
Table: Abbreviations
Abbreviation
Description
CMAC
Cipher-based Message Authentication Code
CPU
Central Processing Unit
ECU
Electronic Control Unit
HCP
High performance Computing Platform
HMAC
Keyed-Hash-based Message Authentication Code
MAC
Message Authentication Code
LAH
Lastenheft (Requirements Specification)
OEM
Original Equipment Manufacturer (here: Vehicle Manufacturer)
PKI
Public Key Infrastructure
6.2 Definitions and Further Applicable Documents
The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”,
“SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be inter-
preted as described in RFC2119 [1].
For all requirements from this document, which relate to cryptographic algorithms and methods, the
implementation must conform to VW-80180-1 [3].
For all requirements from this document, which relate with the handling of cryptographic data and
implementation, the implementation must conform to VW-80180-2 [4].
Definition: "ECU individual" shall be understood as defined VW-80180-1 [3], Chapter 2 “individuell
pro Komponente”. This means individual for every instance of the ECU, not for the ECU type.
6.3 Purpose
The purpose of this document is to provide security requirements for the protection of integ- rity and
authenticity of software and firmware of electronic control units (ECUs). This includes requirements
for:
•
Secure Boot:
must verify software and firmware once during boot sequence (startup) before the logical
block is executed.
•
Authenticated Boot:
must verify software and firmware once parallel or with a certain offset after execution.


<!-- Page 14 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 5
INTERNAL
The integrity protection shall cover all programmable / exchangeable non-dynamic memory areas in
which software and firmware is stored and which is needed to operate the ECU in the way it is
intended. This includes all software and firmware provided by
•
Hardware Manufacturer / Chip Supplier (e.g. BIOS, Core Bootloader)
•
Tier 1 / ECU Supplier (e.g. Customer Bootloader, Operating System)
•
OEM / ECU Application (e.g. OEM Applications)
If a software / firmware component was successfully verified it shall be regarded as trusted – if also
all components before having be verified successfully. Otherwise the component shall not be
regarded as trusted.
In general, the security mechanisms shall be divided in protection mechanisms that are applied dur-
ing
•
the startup (boot process) of the ECU or
•
during the runtime (operational use) of the ECU.
Startup Protection shall use means of:
•
secure boot,
•
authenticated boot
Runtime Protection shall use means of:
•
runtime integrity protection, but shall reuse mechanism of authenticated boot where
applicable
•
runtime integrity protection shall not replace existing runtime integrity monitoring (e.g.
existing watchdog functionality) established for functional safety.
6.3.1 Overview Secure Boot
The Secure Boot shall ensure that the software and firmware on the ECU has not changed unin-
tended, due to manipulation or faults.
Therefore, the ECU software may be divided into multiple to logical blocks, which shall each be
secured by individual integrity protection mechanisms.
For secure boot the verification of the integrity must always be performed once before the logical
block itself is executed / started.
For secure boot the verification of the integrity mechanism must always be performed before the
logical block itself is executed / started.
If the verification of a logical block fails it must not be executed.


<!-- Page 15 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 6
INTERNAL
Note: Some hardware components or system solutions claim an implementation of “Secure Boot”
but do not conform to the definitiongiven in this Document. Those solutions (e.g. SHE1.1) have no
native HW support to prevent code execution after a secure boot verification failed, as due to the
SHE1.1 specification only key access is restricted by the outcome of the secure boot verification.
6.3.2 Overview Authenticated Boot
The Authenticated Boot shall ensure any change to software on the ECU is detected during or shortly
after the boot process and that therefore specific reactions can be applied.
The mechanisms implementing [QLAH_SecSWIntProt_107] shall meet the security requirements
defined in this document, but can technically be achieved by symmetric or asymmetric protection
schemes, detailed later in this document.
For authenticated boot the verification of the integrity must always be executed during or right after
the boot process.
In contrast to secure boot (see Chapter 1.3.1) authenticated boot must verify the integrity of all logical
blocks by a trusted element within the ECU and store the specific results for each block.
The trusted element must then verify the results of the different integrity checks and if there are
specific fails, defined actions have to be applied. This may include the shutdown of the system, the
switch to a fall-back system or making specific data (e.g. cryptographic keys) inaccessible to the
system.
[I: QLAH_SecSWIntProt_112]
The action for an invalid verification during authenticated boot must be approved by the functional
owner of the ECU, the security department of the OEM and the functional safety responsible of the
OEM if applicable.
7 Requirements for Organization and Documentation
7.1 Regulatory Requirements
Cited from GB44495-2024 Technical Requirements for Automotive Vehicle Information Security,
Section 7.3 Software Upgrade Safety Requirements - 7.3.1 General Safety Requirements - 7.3.1.1:
The onboard software upgrade system should utilize security protection mechanisms to
safeguard the trusted root of the onboard software upgrade system and the bootloader, ensuring
that the system is not altered or, if altered, cannot be started normally through security protection
mechanisms.
Note: Refer to the regulations for the original text.
7.2 Organizational Requirements
In order to be able to decide which measures are applicable for a certain ECU a Thread and Risk-


<!-- Page 16 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 7
INTERNAL
Analysis (e.g. based on TARA, STRIDE,..) has to be executed.
Before start of implementation a security concept must be prepared, describing which part of the
firmware / software is protected by secure boot / authenticated boot / runtime integrity protection and
what happens if the verification fails. This concept must be approved by the OEM.
7.3 Documentation Requirements
The supplier of the ECU must provide result documentation of the Thread and Risk-Analysis for his
ECU to the OEM.
The supplier of the ECU must provide the customer with software integrity protection documentation,
which details how each requirement from this document has been fulfilled.
The supplier of the ECU must document for each CPU, which of the methods is being used to vali-
date the authenticity and integrity of the software that executes on the CPU.
All deviations from the requirements of this document and all further applicable documents (see
chapter 1.2) the must be documented by the supplier and approved by the customer.


<!-- Page 17 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 8
INTERNAL
8 Technical Requirements
8.1 General System Requirements
Every programmable ECU must ensure, for all its CPUs (microprocessors, microcontrollers, or sim-
ilar), that only authentic software, whose integrity was successfully validated, can be executed.
Each CPU must validate the authenticity and integrity of its software (executable program code and
static configuration data) according to at least one of the methods specified in this document.
Methods specified are secure boot, authenticated boot.
8.1.1 Functional Requirements
All integrity mechanisms must support full and partial software updates of the ECU application soft-
ware.
All integrity mechanisms must be designed to support over the air software updates of the ECU
application software.
All integrity mechanisms shall be aligned with full and partial software updates logic where possible.
All integrity mechanisms shall be designed to securely trigger a refresh the internal reference values
after a successful software update.
All integrity mechanisms shall be designed to be able to send trusted status messages after a suc-
cessful verification.
8.1.2 Handling of cryptographic assets
If not already defined within general secure specification all cryptographic assets have to be
handled according to this document.
3.1.4.3 Data
3.1.4.3.1 Secret Keys
All used symmetric Secret Keys – if a symmetric approach is used - for secure boot / authenticated
boot protection must be ECU individual.
All used symmetric Secret Keys – if a symmetric approach is used - for secure boot / authenticated
boot protection shall be generated within the ECU in a trusted environment, sup- ported by specific
hardware.
All symmetric Secret Keys must be protected according to general secure specification to guarantee
authenticity and confidentiality.


<!-- Page 18 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 9
INTERNAL
Keys for testing may be generated outside the ECU of the OEM PKI, but test keys must never be
distributed within production ECUs (during or after SOP).
3.1.4.3.2 Private Keys
All used asymmetric Private Keys – if an asymmetric approach is used - for secure boot / authenti-
cated boot protection that have to be stored within the ECU must be ECU individ- ual.
All used asymmetric Private Keys – if an asymmetric approach is used - for secure boot / authenti-
cated boot protection that have to be used within the ECU shall be generated within the ECU in a
trusted environment, supported by specific hardware.
All asymmetric Private Keys stored within the ECU must be protected according to general secure
specification to guarantee authenticity and confidentiality.
All used asymmetric Private Keys – if an asymmetric approach is used - for secure boot / authenti-
cated boot that have to be used in the backend, shall be generated within the OEM PKI and shall be
used only there within hardware security modules.
Keys for testing may be generated outside the ECU of the OEM PKI, but test keys must never be
distributed within production ECUs (during or after SOP).
3.1.4.3.3 Root of Trust
Depending on whether the Root of Trust is based on a symmetric or asymmetric schema, the re-
quirements of either chapter 3.1.2.1.1 (symmetric) or chapter 3.1.2.1.2 (asymmetric) have to be ob-
served.
The Root of Trust shall be regarded as long term measure, and shall be chosen according to
general secure requirement chapter 5.2.1 .
The Root of Trust shall not be exchangeable within the ECU via regular SW Updates or via
debug access.
Any exchange concept for the Root of Trust must to be approved by the OEM.
An exchange concept for the Root of Trust shall always be based on a proof of knowledge of the
corresponding private key or the secret itself, as well as on at least one additionally proof for an
additional secret within the ECU.
3.1.4.3.4 Public Keys and Certificates
The integrity of a public key / certificate must be proven before it is regarded as valid.
Public Keys shall be stored as Public Key Certificates within the ECU, the certificate format must be
approved by the functional owner of the OEM.


<!-- Page 19 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 10
INTERNAL
Public Key Certificates may be stored in any memory area within the ECU but shall always be verified
up to the Root of Trust before being used.
If a Public Key Certificates is not part of a successfully verified data area (firmware, software) and
cannot be verified against a Root of Trust, the certificate shall not be trusted.
3.1.4.3.5 Reference Values / Authentication Codes
Depending on whether the integrity protection is based on a symmetric or asymmetric schema, Ref-
erence Values shall either be realized as CMACs / HMACs (symmetric) or digital signatures (asym-
metric).
The integrity of the used Reference Values must be assured. Those values shall only be updated
be the trusted hardware supporting the integrity protection.
The Reference Values shall not be writeable via Diagnostic Commandos, Debug Interfaces.
3.1.4.3.6 Digital Signatures
Digital Signatures may be stored in any memory area within the ECU but shall always be verified
up to the Root of Trust before being regarded as valid.
If a Digital Signatures cannot be verified against a Root of Trust, the Digital Signature and the asso-
ciated data shall not be trusted.
3.1.4.4 Algorithms
3.1.4.4.1 Generation of Reference Values
If a symmetric approach for integrity checks is used, Reference Value generation shall use a MAC
algorithm according to general secure requirement.
If an asymmetric approach for integrity checks is used, Reference Value generation shall use an
approved digital signature schema according to general secure requirement.
Symmetric Reference Value calculations (generation / verification) executed within the ECU shall be
executed within a trusted environment, supported by specific hardware.
Asymmetric Reference Value generation executed within the ECU shall be executed within a trusted
environment, supported by specific hardware.


<!-- Page 20 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 11
INTERNAL
Asymmetric Reference Value verification executed within the ECU may be executed in software, if
the software integrity was proven before.
3.1.4.4.2 Symmetric Crypto Functions
Symmetric Crypto functions (encryption / decryption) executed within the ECU shall be executed
within a trusted environment, supported by specific hardware.
3.1.4.4.3 Asymmetric Crypto Functions
Asymmetric crypto operations using private keys (Decryption / Signature generation) executed within
the ECU shall be executed within a trusted environment, supported by specific hardware.
Asymmetric crypto operations using public keys (Encryption / Signature Verification) executed within
the ECU may be executed in software, if the software integrity was proven before.
3.1.4.4.4 Secure Boot Requirements
A component implementing secure boot shall only execute code that has been verified in the boot
process prior to execution.
All system requirements of chapter 3.1 must be met.
8.1.3 Specific Hardware Requirements
The hardware shall support methods to prevent code execution if the initial, hardware based (native)
secure boot fails.
8.1.4 Specific Software Requirements
If a software block cannot be validated successfully, then secure boot must fail and the ECU must
transition into recovery mode, see chapter 4.1.
The implemented secure boot must not violate other functional requirements of the ECU, e.g. start-
up timings.
To validate the integrity of the measured software, the integrity validation function must compare the
measured integrity digest with the known good integrity digests (Reference Value) for the software.
If the measured integrity digest does not match any of the known good integrity digests, then secure
boot must fail.


<!-- Page 21 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 12
INTERNAL
8.2 Authenticated Boot Requirements
A component implementing authenticated boot shall verify all executable code in the boot process.
This verification may be performed in parallel or shortly after execution of the code.
All system requirements of chapter 3.1 must be met.
8.2.1 Specific Hardware Requirements
The authenticated boot must be supported by a trusted independent hardware, executing the meas-
urement and validation. The used hardware must be approved by the OEM.


<!-- Page 22 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 13
INTERNAL
9 Example Solution Scenarios
9.1 Example scenario for microcontroller based ECU
The following paragraph outline a possible solution scenario that would fit the requirements of this
QLAH – as long as all implementation details match the requirements of the additional relevant
documents.
ECU:
Micro controller based AUTOSAR architecture
HSM:
Hardware security module according to [?], e.g. EVITA medium
Scenario:
•
Micro-Controller by HW Supplier 1
•
ECU by Tier 1
•
ECU Application OEM specific
Solution Approach:
•
ECU support contains HSM
•
For ECU Bootloader (by HW Supplier 1) and Customer Bootloader (by Tier 1) symmetric
keys are used.
•
Those keys are ECU individual and shall be created by the HSM.
•
The keys are stored and protected by the HSM.
•
CMACs are generated by the ECU for ECU Bootloader (by HW Supplier 1) and Customer
Bootloader (by Tier 1) and stored and protected within the HSM
•
The verification of the ECU Bootloader is executed directly by the HSM Hardware.
•
The control is handed over to the ECU Bootloader.
•
The ECU Bootloader uses the HSM hardware (algorithms, stored symmetric keys, stored
CMAC) to verify the Customer Bootloader (by Tier 1).
•
The control is handed over to the Customer Bootloader.
•
The verification of the OEM Application is done asymmetrical.
•
The OEM Application was signed by the OEM with a asymmetric private key, stored securely
within the OEM PKI.
•
The corresponding public key for verification of that signature is stored within the customer
boot loader.
•
The customer bootloader is now responsible for the verification of the OEM application – this
could be done is software, still the usage of crypto hardware for the execution of the algo-
rithms is recommended.


<!-- Page 23 -->

Confidential. All rights reserved. No part of this document may be provided to third parties or reproduced without the prior written consent
of the appropriate Volkswagen AG department. This document is available to contracting parties solely via the appropriate Procurement
department.
The English translation is believed to be accurate. In case of discrepancies, the Chinese version controls.
P a g e  | 14
INTERNAL
10 Appendix
10.1 References Table
Ref.
Document/Source
Version
[1]
CyberSecurity_General Requirement_Specification
V2.1


