---
source_url: ""
ingested: 2026-08-06
sha256: 0744037307036f0786075792062a997c7c4cf3c856aad9a69a4f51bf25dca685
---

# REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27

<!-- Page 1 -->

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page1_img1.png)

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page1_img2.png)

080_VCS_005_01_Secured_Diagnosis
整车网络安全方案安全诊断规范
MQB_Release
080_VCS_005_01_Secured_Diagnosis (rev. 1523045)
1 | Page
Polarion ALM 2404
2026-03-06 11:07


<!-- Page 2 -->

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page2_img1.png)

更新记录:
日期
版本号
修订类别
作者
描述
2025/09/12
V0.1
I
乔匀
草稿版本
2025/10/24
V1.0
M&D
乔匀
初版释放版本，调整
27服务算法，27服务
密钥规格。
类别：
I - 初始
A - 增加
M - 修改
D - 删除
MQB_Release
080_VCS_005_01_Secured_Diagnosis (rev. 1523045)
2 | Page
Polarion ALM 2404
2026-03-06 11:07


<!-- Page 3 -->

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page3_img1.png)

MQB_Release
080_VCS_005_01_Secured_Diagnosis (rev. 1523045)
3 | Page
Polarion ALM 2404
2026-03-06 11:07


<!-- Page 4 -->

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page4_img1.png)

1 介绍
1.1 概览
本文对诊断27服务，29服务的过程和保护范围提出了安全要求，从公司通用安全需求引入，提出了
对安全诊断的整体要求。
1.2 范围
本规范定义的需求适用于MQB@CEA项目车型。
1.3 相关文档
《整车网络安全方案-通用安全技术需求》
《整车网络安全方案-密钥管理系统》
《整车网络安全方案-公钥基础设施PKI》
2 缩略语和术语
缩写
英文全称
中文全称
CBC
Cipher Block Chaining
密码块链接
CCU
Central Control Unit
中央域控制器
CMAC
Cipher-based Message Authentication Code
基于加密消息认证码
ECDHE
Elliptic Curve Diffie-Hellman Ephemeral
椭圆曲线密钥交换
ECDSA
Elliptic Curve Digital Signature Algorithm
椭圆曲线数字签名
EOL
End of line
下线检测
KMS
Key Management System
密钥管理系统
MAC
Message Authentication Code
消息认证码
PBKDF2
Password-Based Key Derivation Function 2
基于密码的密钥派生
PRNG
Pseudorandom Number Generator
伪随机数发生器
TLS
Transport Layer Security
传输层加密
TRNG
True Random Number Generator
真随机数发生器
MQB_Release
080_VCS_005_01_Secured_Diagnosis (rev. 1523045)
4 | Page
Polarion ALM 2404
2026-03-06 11:07


<!-- Page 5 -->

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page5_img1.png)

SHA
Secure Hash Algorithm
安全散列算法
SOC
System on Chip
片上系统
3 功能定义
3.1 27服务
MQB-CSC-13067 - 27服务
27服务提供了一种访问那些权限受限或与排放及安全因素有关的数据及服务的方法。例如，上传/
下载程序或数据至ECU、从ECU中读取特殊位置内存数据等诊断服务一般需要执行安全访问。因为下
载不恰当的程序或数据至ECU可能破坏电子设备或其它汽车部件，或对汽车的排放、安全性及安全
标准造成风险。
3.2 29服务
MQB-CSC-13069 - 29服务
29服务为用户提供了一种证明其身份的功能，以允许用户访问数据或诊断服务。向ECU写入数据、
从ECU读取数据、启动特定例程或诊断服务都可能需要认证服务。因为这些操作可能会损坏电子设
备或其他车辆部件，违反排放、功能安全或网络安全的相关标准。同时，从ECU读取数据时可能会
违反数据安全的相关规定。
4 功能规范
4.1.1 通用诊断网络安全要求
MQB-CSR-13068 - 禁止读写敏感数据/Prohibit reading and writing sensitive data
在UDS诊断其他相关服务中，应禁止直接读写敏感数据（例如，加密密钥，身份证明证书，人脸信
息，OTA相关记录等信息），相关数据需要通过安全访问措施加以保护后进行读写操作。
In other related services of UDS diagnosis, direct reading and writing of sensitive
data (such as encryption keys, identity certificates, facial information, OTA-related
records, etc.) should be prohibited. Relevant data needs to be protected through
security access measures before being read or written.
MQB-CSR-13072 - 诊断调查表定义范围外的诊断服务管理/Diagnostic service management
MQB_Release
080_VCS_005_01_Secured_Diagnosis (rev. 1523045)
5 | Page
Polarion ALM 2404
2026-03-06 11:07


<!-- Page 6 -->

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page6_img1.png)

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page6_img2.png)

outside the defined scope of the DPST
如ECU实现在诊断调查表定义范围外的DID，RID或UDS服务，供应商应告知OEM，由OEM审核。供应商
在软件冻结应提交实际开发的诊断调查表或相应的UDS服务扫描报告，由OEM进行审核是否有未定义
的DID，RID或UDS服务。
If the ECU implements DID, RID, or UDS services outside the defined scope of DPST, the
supplier should notify the OEM for review. The supplier should submit the actual
developed DPST or corresponding UDS service scan report for the OEM to review whether
there are any undefined DID, RID, or UDS services of software freeze version.
安全诊断服务必须可以满足诊断需求以及本份文档中的要求。
4.1.2 27服务
27服务采用挑战-应答机制进行身份校验，27服务的认证流程详见诊断需求，27服务保护范围以诊
断DPST需求为准。
27服务流程参考如下（以诊断释放需求内流程为准，本文档中流程仅作参考为方便理解）
MQB_Release
080_VCS_005_01_Secured_Diagnosis (rev. 1523045)
6 | Page
Polarion ALM 2404
2026-03-06 11:07


<!-- Page 7 -->

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page7_img1.png)

4.1.3 27服务密钥需求
MQB-CSR-13070 - 27服务算法/UDS 27 service algorithm
27服务使用AES-128-ECB算法，应答值Key=AES-128-ECB（seed，密钥）；具体算法需求参考诊断释
放的算法需求文档。
27 Service uses the AES-128-ECB algorithm, and the response value Key = AES-128-
ECB (seed, key); for specific algorithm requirements, refer to the algorithm
requirements document released by the diagnosis team.
MQB-CSR-13074 - 27服务密钥/The key for UDS 27 service algorithm
AES-128-ECB算法的入参中，明文为ECU传递的seed，各ECU使用的密钥为对应ECU诊断释放的算法需
求文档中的密钥。
In the input parameters of the AES-128-ECB algorithm, the plaintext is the seed sent
by the ECU, and the key used by each ECU is the key specified in the algorithm
requirement document released by the diagnosis team for corresponding ECU.
MQB-CSR-13073 - 27服务密钥更新保护/The key for 27 service algorithm update protection
27服务使用的AES-128-ECB算法密钥如需更新需要经过安全访问或存储区域读写保护等安全方案进
行保护。
If the key of the AES-128-ECB algorithm used for UDS Service 27 needs to be
updated, it must be protected by security measures such as secure access or
read/write protection of the storage area.
MQB-CSR-13076 - 27服务密钥安全存储/The key for UDS 27 service algorithm secured
storage
27服务使用标准密码学算法密钥需要安全存储，如ECU支持硬件安全模块，密钥需要存储在硬件安
全模块中，如不支持硬件安全存储，需采用混淆操作对密钥加以保护，密钥明文值不可以被未授权
读取/篡改/删除，对于使用混淆操作进行密钥保护的ECU，建议额外采取内存保护的方案保护密钥
存储部分内存区域的读写权限；安全存储需满足安全存储要求: 080_VCS_002_02_Secured
Storage。
The UDS 27 Service algorithm key needs to be securely stored. If the ECU
supports a hardware security module (e.g. HSM), the keys need to be stored in
the hardware security module; if it does not support hardware secure storage,
obfuscation operations must be used to protect the keys. The plaintext value of
the keys cannot be read/tampered/deleted without authorization. For ECUs that
use obfuscation operations to protect keys, it is recommended to additionally
adopt a memory protection scheme to protect the read and write permissions of
the memory area where the keys are stored; secure storage should meet the secure
storage requirement: 080_VCS_002_02_Secured Storage.
MQB_Release
080_VCS_005_01_Secured_Diagnosis (rev. 1523045)
7 | Page
Polarion ALM 2404
2026-03-06 11:07


<!-- Page 8 -->

![image](REQ_06_080_VCS_005_01_Secured_Diagnosis_UDS27/images/page8_img1.png)

4.1.4 27服务种子随机性需求
MQB-CSR-13075 - 27服务seed随机性要求/27 Service seed randomness
27服务ECU生成的seed需要满足通用网络安全需求：080_VCS_001_03_CyberSecurity General
Requirement Specification
中的随机性要求。
The seed generated by the ECU in UDS 27 process shall meet the general
cybersecurity requirement: 080_VCS_001_03_CyberSecurity General Requirement
Specification Random number generation requirements.
4.1.5 27服务防暴力破解
MQB-CSR-13071 - 27服务防暴力破解要求/UDS27 service anti-brute forcing
27服务安全访问应具备惩罚恶意访问的机制，防止暴力破解。防暴力破解使用的计数器需要存储在
非易失性存储器中。
UDS 27 service should have a mechanism to penalize malicious access and prevent brute
force attacks. The counter used for anti-brute force protection needs to be stored in
non-volatile memory.
MQB_Release
080_VCS_005_01_Secured_Diagnosis (rev. 1523045)
8 | Page
Polarion ALM 2404
2026-03-06 11:07


<!-- Page 9 -->


<!-- Page 10 -->


<!-- Page 11 -->


<!-- Page 12 -->


<!-- Page 13 -->


<!-- Page 14 -->


