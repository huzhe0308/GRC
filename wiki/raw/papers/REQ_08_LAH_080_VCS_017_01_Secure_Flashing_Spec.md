---
source_url: ""
ingested: 2026-08-06
sha256: 055c3fa27b551a286c90e9386fea41d8d540a3136b963e55a0f8f6ffbd0f3f54
---

# REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec

<!-- Page 1 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page1_img1.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page1_img2.png)

080_VCS_017_01_Secure Flash
整车网络安全技术定义安全升级_安全刷写规范
更新记录:
日期
版本号
修订类别
作者
描述
2025/09/11
v0.9D
I
谢元辉
初始版本
非正式释放版，内容还需与各相关方对齐信息
2025/11/19
v1.0F
M
对于供应商章节生成释放版本
类别：
I - 初始
A - 增加
M - 修改
D - 删除
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
1 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 2 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page2_img1.png)

目录
1   介绍
.
3
1.1   缩写
1.2   术语
2   需求输入
4
3   范围
4   安全升级功能描述
4.1   升级方式定义
5   安全升级功能基本要求
6
5.1   软件升级的安全要求
5.1.1   实现安全措施的依赖项
5.1.2   安全升级软件的基本要求
5.2   升级过程的安全要求
8
5.3   密码学算法要求
5.4   密钥的要求
6   安全升级功能实现方案
11
6.1   OTA升级系统的安全
6.2   安全刷写功能概述
6.2.1   基本功能描述
6.2.1.1   功能基本描述：
6.2.1.2   刷写包结构：
12
6.2.1.3   基于UDS协议的安全刷写流程：
6.2.1.3.1   数字签名验证流程和服务
6.2.1.3.2   车端ECU验证签名流程：
6.2.2   VW Group自研件功能实现架构：
6.2.2.1   安全刷写密钥要求：
6.2.2.2   核心功能实现流程图：
6.2.2.3   刷写包结构
6.2.2.4   ECU零部件研发密钥-量产密钥切换及工厂产线刷写场景：
6.2.3   对于Bootloader Update的网络安全要求
7   参考文档
24
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
2 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 3 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page3_img1.png)

1 介绍
本方案书对整个安全升级流程以及相应的依赖事项提出了安全保护要求。从国家标准以及企业要求引入，提出了对升级包及
安全升级流程的整体要求，技术上包括对升级包的安全加密签名等算法需求，升级过程的安全通信等要求，实现对安全升级
的覆盖。
本方案书的第4章和第5章主要描述了通用性的安全需求，尽量和项目以及技术方案无明显依赖关系，相关的引用作为参考内
容。
本方案书的第6章给出了安全升级功能在CEA项目中的实现方案，6.1章节定义了OTA升级系统的安全技术方案和规范，6.2章
节定义了安全刷写功能的技术方案和规范。
1.1 缩写
AES
Advanced Encryption Standard
高级加密标准
CBC
Cipher Block Chaining; mode of a block cipher algorithm
密码块链接
CMAC
Cipher-based message authentication code
基于加密消息认证码
DH
Diffie-Hellman
迪夫-霍尔曼
ECC
Elliptic curve cryptography
椭圆曲线加密
ECDH
Elliptic curve Diffie-Hellman
椭圆曲线密钥交换
ECDSA
Elliptic Curve Digital Signature Algorithm
椭圆曲线数字签名
PKI
Public key infrastructure
公钥基础设施
RSA
Asymmetric cryptographic algorithm as per Rivest, Shamir,
and Adleman
罗纳德-萨莫尔-阿德
曼非对称加密
1.2 术语
Term
术语
解释
ECU signature
ECU 签名
在 ECU 中验证的容器内特定内容（刷写数据、地址和长
度
信息）的签名。
Development signature 开发签名
供应商在开发密钥的帮助下生成的 ECU 签名的表现形
式，
这在 ECU 开发阶段中使用。
Production signature 量产签名
在量产密钥的帮助下生成的 ECU 签名的表现形式，这在
ECU 量产阶段中使用。
Development key
开发密钥
PrivateKey
私钥
这在供应商生成开发签名的过程中是必要的。
PublicKey
公钥
这在 ECU 中用于验证开发签名。
Production key
量产密钥
这是用于量产车辆的。
这在生成量产签名的过程中是必要的。
这在 ECU 中用于验证量产签名。
Bootloader
引导加载程序
在本文中主要用来辅助刷写流程的实现
Logical block
逻辑块
可以进行独立使用的完整的数据实体在存储设备上的一
种
表现形式，在本文中主要指待刷写的软件镜像
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
3 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 4 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page4_img1.png)

2 需求输入
GB 44495-2024《汽车整车信息安全技术要求》
GB 44496—2024《汽车软件升级通用技术要求》
3 范围
安全升级整体要求：
本方案书确定了安全升级过程中所需的所有密码学方法和升级过程中的安全措施，以及公司范围内使用这些方法和措施的流
程。
本方案书描述了对公司内部和供应商重要且必须在安全升级项目范围内执行的所有流程。主要对使用数字签名和加密等方式
保护升级软件的方法及其对应的相应流程进行了说明
本方案书没有详细显示所有操作流程。必要时引用了相关基础文档。
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
4 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 5 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page5_img1.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page5_img2.png)

4 安全升级功能描述
4.1 升级方式定义
CEA-CSC-48874 - 安全升级功能概述
本方案书将软件升级方式分为在线升级和离线升级方式。具体升级方式以及使用的升级工具应根据项目实际情况确定。本方
案书只描述了通用情形的要求。
通过OTA 平台升级方式为在线升级，而通过工程诊断仪或USB等其他方式升级则称为离线升级。OTA 在线升级是指车辆自动
通过OTA-Master从云端OTA平台下载软件升级包进行升级。而工程诊断仪方式则是人工将软件升级包通过工程诊断仪将软件
升级直接导入到 ECU 再进行升级，升级过程如下图所示：
为保证软件升级过程中软件本身和整个流程的安全性，本方案书依照CEA项目的OTA升级过程对应的设计了OTA升级系统的安
全功能和安全刷写功能。
OTA升级系统的安全（Secure OTA）功能保障了了软件包从CEA的Onebackend的OTA云端平台下载到车端OTA-Master的软件升
级过程的安全性。
安全刷写（Secure Flash）功能保障了车端OTA-Master将软件包分发并刷写进入到车内的各个Slave ECU过程中的安全性。
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
5 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 6 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page6_img1.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page6_img2.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page6_img3.png)

5 安全升级功能基本要求
本章节描述了创建升级软件和软件安全升级过程中需要遵守的操作流程，以保证整个过程的安全性。
5.1 软件升级的安全要求
5.1.1 实现安全措施的依赖项
CEA-CSR-48884 - 安全升级功能的基础依赖
在项目开始时，相关方应具备保证升级包数据安全所必需的各种依赖项。
安全服务
安全服务是为待升级软件包提供安全保护措施。安全服务中可以包括实现数字签字、加密、压缩等功能，同时相应的密钥管
理、存储服务也可以在安全服务中部署。应支持使用不同的算法实现数字签名，至少支持RSA和ECC的算法。
数字签名密钥
密钥对应的公钥用来验证 ECU 的升级包的数字签名。
密钥对应的私钥在安全服务中，用于生成 ECU 的数字签名。注：私钥（量产密钥）必须采取严格的保护措施保证私钥的安
全。
5.1.2 安全升级软件的基本要求
CEA-CSR-48617 - 安全升级软件的基本要求
本节描述了 ECU 开发过程中通过签名和/或加密及压缩的方式保护的升级软件所需的操作流程的基本要求。
根据整车安全部门经过风险分析得出的结果对于有安全升级要求的零部件，在使用软件包数据前，必须要进行数字签名验
证，其真实性和完整性校验通过后才可以使用。为了进一步加强安全性，可以考虑使用加密和/或压缩的方式对升级软件做
进一步的保护。实现安全需求的偏差应与整车安全部门达成一致，并记录在相应的文件/系统中。
在 ECU 上集成含有安全升级的机制的软件时，必须确保正确校准和使用文档 [1] 《
080_VCS_001_01_CyberSecurity
Specification General Requirement_CEA2.x 》中算法要求的密钥。
数字签名算法应按照整车安全部门释放的算法要求实现。参考 [1] 和后续章节 5.3。通过这种方式，对该升级包数据的成
功签名验证确保了升级包的真实性和完整性。
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
6 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 7 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page7_img1.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page7_img2.png)

CEA-CSR-48863 - 软件安全升级流程要求
软件安全升级流程示意图如下面图 2 所示：
在量产后软件的升级过程必须通过前文提到的安全升级机制进行。用于量产使用的软件升级包必须至少使用签名的方式以作
保护。为了能够在升级期间校验升级数据的量签名，必须使用与之匹配的公钥。公钥必须在 ECU 中受到保护，防止被操纵
（未经授权和未被注意的更改）。
在量产后用于对软件升级的工具/仪器/服务等必须通过安全访问或身份认证等方式保证接入端 (需要升级的ECU）的安全
性。
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
7 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 8 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page8_img1.png)

5.2 升级过程的安全要求
此部分主要阐述整个软件升级过程的安全要求。包括从后端到车的软件升级包下载过程和在车内的软件升级包的刷写过程。
CEA-CSR-48864 - 在线升级过程的安全要求
在使用在线升级时，车辆与升级后端在通信时应对通信对象的身份的进行验证，验证其身份的真实性，防止非授权的升级连
接。应使用基于证书的方式对通信双方身份做认证和校验，校验前应对证书的合法性做检查。同时在升级前，所定义身份认
证方式或协议应使用公开的认证协议，并得到安全部门的批准。
在使用在线升级时，车辆与升级后端在进行通信时，应建立安全的通信信道。整个升级过程中，在进行升级数据传输以及相
应指令的传输时，应保证真实性和完整性，必要时需实施机密性保护措施。建议使用端到端的安全通信，保护整个通信链路
的通信数据。必须对相应的下载的升级包做完整性和真实性校验。
CEA-CSR-48865 - 离线升级过程的安全要求
在使用离线升级时, 应采取保护措施保证刷写接入端的安全性和软件升级包的真实性和完整性。具体方案应与整车安全部门
达成一致。
CEA-CSR-48866 - 安全升级过程的故障恢复要求
为防止外部（意外断电，认为重启）或内部（程序故障等）的故障导致升级进程中断，应支持故障恢复，至少应支持对
ECU 软件的重新升级或继续升级。还可以通过分区刷写的方式，升级时刷写非活动分区，升级成功后，切换启动标识，ECU
再次启动时，根据启动标识切换分区。对启动分区标识应写入到非易失存储区，并对相应数据做写入保护，防止非预期篡
改。具体请参考《安全启动规范》中的要求。特殊情况应与安全团队达成一致。
CEA-CSR-48867 - 安全升级功能的日志要求
如果安全升级功能流程中任一过程出错，ECU应立即停止当前进程；云端应记录相应的安全升级日志。
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
8 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 9 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page9_img1.png)

5.3 密码学算法要求
CEA-CSR-48868 - 安全升级功能使用的签名算法要求
发布的签名算法是 “RSA ”和 “ECC ”部分提到的算法。在实现安全升级功能时，可选择使用其中一种算法。若使用其他
算法，应保证算法强度至少和下文提到的算法强度保持一致，且要与安全部门协商一致后方可使用。
数字签名算法：
RSA： 若使用 RSA 算法，则必须至少使用 RSA 3072 或以上的算法。
RSA 3072： RSA 3072 算法介绍如下： 签名的生成和验证必须按照 Public Key Cryptography Standard PKCS#1 v1.5以上
进行，使用签名算法 RSASSA-PSS（3072 位）和安全散列算法 SHA-256。 推荐使用Public Key Cryptography Standard
PKCS#1 v2.2，使用带有 SHA-256 的掩码生成功能 MGF1 作为掩码算法。公钥的指数必须符合参考文档[1]的规定。
RSA 8192 (可选）： RSA 8192 算法描述如下：若使用 RSA 8192算法，签名计算和验证推荐按照 Public Key
Cryptography Standard PKCS#1 v2.2 使用 RSASSA-PSS（8192 位）和 SHA-384 进行。 推荐使用带有 SHA-384 的 MGF1
作为掩码算法。 公开密钥的指数必须符合参考文档[1] 的规定。
RSA 16384 (可选）： RSA 16384 算法描述如下： 若使用 RSA 16384算法，签名计算和验证推荐按照 Public Key
Cryptography Standard PKCS#1 v2.2 使用 RSASSA-PSS（16 384 位）和 SHA-512 进行。 推荐使用带有 SHA-512 的
MGF1 作为掩码算法。 公开密钥的指数必须符合参考文档[1] 的规范。
ECC： 若使用 ECC 算法，则必须至少使用 ECC 256 或以上的算法。
ECC 256： 基于 ECC 和 SHA-256 的椭圆曲线数字签名算法（ECDSA）描述如下: 使用的椭圆曲线为美国国家标准与技术研
究院（NIST）指定的 P-256 曲线，域参数见参考文档[2]。
ECC 384 (可选）： 基于 ECC 和 SHA-384 的椭圆曲线数字签名算法（ECDSA）描述如下 使用的椭圆曲线指定为 NIST
P-384 曲线，域参数见参考文档[2]。
ECC 512(可选）： 基于 ECC 和 SHA-512 的椭圆曲线数字签名算法（ECDSA）描述如下 使用的椭圆曲线指定为 NIST
P-521 曲线，域参数见参考文档[2]。
国密算法：
采用的密码算法必须符合国家密码管理相关政策法规，优先采用国家密码管理局批准的算法。
SM2：
其中本方案书中描述的数字签名应采用SM2椭圆曲线公钥密码算法，和SM3 （哈希算法）相结合使用。
SM2算法的实现必须符合《GM/T 0003-2012 SM2椭圆曲线公钥密码算法》的规定，并使用该标准第5部分推荐的椭圆曲线参数
域。
在数字证书、数字签名等涉及算法标识的场景中，必须使用国家标准OID进行明确标识。参考《GM/T 0006-2012 密码应用标
识规范》
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
9 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 10 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page10_img1.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page10_img2.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page10_img3.png)

5.4 密钥的要求
CEA-CSR-48869 - 安全升级功能使用的密钥基本要求
安全升级过程中用到的密钥材料应实施完整性和/或机密性保护措施。
密钥的存储要求：
对于对称密钥，所有对称密钥必须实施机密性和完整性保护措施。
对于非对称密钥，私钥应实施严格的安全保护措施，包括但不限于机密性，完整性等措施；应对公钥实施完整性保护措施。
密钥存储的详细要求应按照《
080_VCS_002_02_Secured Storage 》中的要求。
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
10 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 11 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page11_img1.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page11_img2.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page11_img3.png)

6 安全升级功能实现方案
通过加密，签名和压缩等安全措施，可以保证软件升级过程中的安全性，称为安全升级过程。可以将软件安全升级过程分为
安全下载和安全刷写过程。
6.1 OTA升级系统的安全
具体方案请参考
080_VCS_003_01_Secure OTA 方案书
6.2 安全刷写功能概述
6.2.1 基本功能描述
6.2.1.1 功能基本描述：
CEA-CSR-48870 - ECU实现安全刷写功能的基本要求
在云端One Backend调用云端的安全服务，使用严格安全保护的私钥对刷写数据进行数字签名的操作。
在车端各ECU中，在刷写数据写入过程中使用对应的公钥对刷写数据进行签名验证和Hash校验。
本章节6.2中的要求适用范围为：诊断刷写规范使用了CEA项目中的基础技术规范《020_VCS_006_03_Flash Reprogramming
Specification_EN (For both out sourcing ECU & inhouse domain controller》进行刷写功能开发的ECU。
6.2.1章节为根据整车网络安全风险分析的Tara结果，需要使用安全刷写功能保护刷写包的真实性和完整的所有相关ECU的技
术实现时的基本要求。
6.2.2章节只适用于VW Group负责研发的ECU的安全刷写功能实现的方案设计。
6.2.3章节专门适用于有些ECU可支持Bootloader的更新做出安全的设计和要求
注：对于使用了其他流程和方案完成软件刷写功能的ECU：根据整车网络安全风险分析的Tara结果，若结果为需要实现安全
刷写功能，则实现方案可使用供应商自己的平台方案。但方案需要满足第5章中的安全升级功能的通用要求。
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
11 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 12 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page12_img1.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page12_img2.png)

6.2.1.2 刷写包结构：
CEA-CSR-48871 - ECU实现安全刷写功能的刷写包要求
Head Info: 不参与实际刷写，只是描述信息，可参照 UDS基础技术规范《020_VCS_006_03_Flash Reprogramming
Specification_EN (For both out sourcing ECU & inhouse domain controller》：
The following is a theoretical example of an Intel Hex-32 bit configuration data file:
APPLICATION>David 2.0 with BCM
FILE NAME>8045001DA0000000A_APP.HEX
RELEASE DATE>01/25/2018
CAR Model>David 2.0
FLASH ADDRESS 1>0x007F9C00
FLASH LENGTH 1>0x30
MODULE NAME>Body Control Module
MODULE ID>0x720
DATA CRC-32>0x 9D3367AD
FLASH ERASE SECTORS>0x007F9C00,0x30;0x008F9C00,0x30
$
New Data: 实际刷写进ECU的数据，包含Signature和写入的数据。签名具体位置需在数据中，可自行设计位置，示例如
下：
:02000004007F7B
:109C0000A55A20FF0000444739542D3134433634DF
:109C1000372D484500000000000000000000000053
:109C2000000000000000000000110D7F7F110D22D8
:02000004008F6B
: 签名字段
:00000001FF
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
12 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 13 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page13_img1.png)

6.2.1.3 基于UDS协议的安全刷写流程：
6.2.1.3.1 数字签名验证流程和服务
CEA-CSR-48872 - ECU实现安全刷写功能的诊断服务要求
应通过文件完整性校验例程检查升级文件：DRI文件未检验通过不允许软件擦除，APP文件未校验通过不允许软件生效。
参考诊断服务：
DRI文件：
有感升级（NormalFlash）：RID 0202
无感升级（NWFlash）：RID 0202
APP文件：
RoutineControl – “checkRoutine” 服务格式定义
Data byte
Parameter name
Hex value
#0
RoutineControl Request Service Id
31
#1
routineControlType
startRoutine
01
#2 - #3
routineIdentifier
checkRoutine
0202
#4 -#7
CRC32 value, 4 bytes
00-FF
RoutineControl – “checkRoutine” 服务响应格式定义
RoutineControl Response Service Id
71
#4
routineStatusRecord
correctResult
CRC incorrectResult
Signature incorrectResult
00
02
签名和Hash验证响应回复优先级应高于CRC校验；
CEA-CSR-48891 - 安全刷写日志描述要求
当安全刷写功能验证成功或失败时，云端OTA日志中需要记录为：SecFlash Signature&Hash Verify pass/failed
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
13 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 14 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page14_img1.png)

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page14_img2.png)

6.2.1.3.2 车端ECU验证签名流程：
CEA-CSR-48873 - ECU实现安全刷写功能的签名验证流程
1.初始化诊断通信
2. 验证安全通信的身份认证UDS29服务(如果有）
3. 验证安全通信的安全访问UDS27服务
4. 开始刷写编程会话，为刷写包写入准备
5. 将带有签名的文件传输到ECU进行验证
6. 目标ECU会计算文件的Hash Value哈希值，使用安全存储的公钥验证签名
7. ECU内部进行哈希值的比对校验
8. 比对通过后可以继续刷写流程反馈结果，若以上比对过程有不通过都应停止进程，并返回报告结果。
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
14 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


<!-- Page 15 -->

![image](REQ_08_LAH_080_VCS_017_01_Secure_Flashing_Spec/images/page15_img1.png)

7 参考文档
[1] 080_VCS_001_01_CyberSecurity Specification General Requirement_CEA2.x
[2] FIPS PUB 186-4 Federal Information Processing Standards Publication – Digital Signature Standard (DSS)
[3] BSI Technical Guideline TR-03111 – Elliptic Curve Cryptography
[4] GM/T 0003-2012 SM2椭圆曲线公钥密码算法
[5] GM/T 0006-2012 密码应用标识规
[6] 020_VCS_006_03_Flash Reprogramming Specification_EN (For both out sourcing ECU & inhouse domain
controller
[7] 080_VCS_008_10_Cloud - based  Key Management System
[8] 080_VCS_018_01_Key_Distribution
EEA_CEA2.x
080_VCS_017_01_Secure Flash (rev. 1282374)
24 | Page
Polarion ALM 2404
2025-11-19 11:29
VCTC Xie, Yuanhui 160466 2025-11-19
VCTC Xie, Yuanh


