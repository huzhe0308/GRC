<!-- Page 1 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
1 
ICS 43.0420.40T 24
 
 
National Standard of the People’s Republic of China 
 
GB/T 30677-2014
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
   
 
 
 
 
 
 
 
 
 
Performance Requirements and TestingMethods for Electronic Stability Control System(ESC) for Light Vehicles
 
 
 
 
 
 
 
 
 
 
 
 
Issued on 2014-12-31
 
 
 
 
Effective from 2015-07-01
 
Promulgated by
General Administration of Quality Supervision, Inspection and 
Quarantine of the People’s Republic of China 
Standardization Administration of the People’s Republic of China 


<!-- Page 2 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
2 
This Standard is drafted in accordance with the rules given by GB/T 1.1-2009. 
The text of this Standard is modified in relation to GTR 8 “Electronic stability control system 
(ESC)”.
This Standard was proposed by Ministry of Industry and Information Technology. 
This Standard is under the jurisdiction of National Technical Committee of Auto 
Standardization (SAC/TC 114).
The drafting units of this Standard: China Automotive Technology & Research Center 
(CATARC), Pan Asia Technical Automotive Center Co., Ltd., Bosch Automotive Products 
(Suzhou) Co., Ltd., Wuhu Bethel Electronic Control Systems Co., Ltd., Xiangyang Daan 
Automotive Testing Center and CATARC Yancheng Automotive Proving Ground Co., Ltd.. 
Drafters of this Standard: Wang Zhao, Jin Yuefu, Liu Di, Guo Kuiyuan, Gao Mingqiu, Xu 
Zhiguang, Zhao Xiangdong, Yuan Xuliang, Tian Feng, Qian Haibing, Shui Haojun, Wang Yue, 
Huang Xiaomei, Xiong Gongxiang, Ouyang Tao and Yi Ming. 


<!-- Page 3 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
3 
Performance Requirements and Testing Methods for Electronic Stability 
Control System (ESC) for Light Vehicles
1 
 
This Standard specifies the performance requirements and testing methods for 
Electronic Stability Control System (ESC) for light vehicles. 
This Standard applies to electronic stability control system of all vehicles of 
categories M and N with a maximum design total mass no more than 3,500kg. 
Vehicles of categories M and N with a maximum design total mass more than 
3,500kg but no more than 5,000kg may make reference to this Standard. 
2 
 
Normative references
The following documents for the application of this document is essential. For dated 
reference documents, only the dated edition applies to this document. For undated 
reference documents, the latest edition (including all amendments) applies to this 
document.GB/T 12549Automotive controllability and stability -- Terms anddefinitionsGB 21670-2008Technical requirements and testing methods for passenger
car braking systemsGB/T 26987-2011Road vehicles -- Measurement of roadsurface friction (ISO8349:2002, IDT)
3 
 
Terms and definitions
For the purpose of this document, the terms and definitions established in GB/T 
12549 and below shall apply.3.1Ackerman steer angle (δA)
Arc-tangent of the ratio of wheelbase to radius of gyration at low speed. 


<!-- Page 4 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
4 
[GB/T 12549-2013, definition in 3.1.1]3.2Electronic stability control system, ESC
An active safety system that monitors vehicle operation conditions in real time and 
modifies brake force and engine torque as necessary to change vehicle yaw torque, 
so that driver can drive vehicle as per intention. The basic characteristics of the 
system are as follows:
In order to improve the stability of the vehicle's direction, at least having the ability to 
automatically control individually the braking torques of the left and right wheels on 
each axle or an axle of each axle group 1) to induce a correcting yaw moment based 
on the evaluation of actual vehicle condition in comparison with vehicle condition 
demanded by the driver;a)
With the computer using a closed-loop control to limit vehicle oversteer and to 
limit vehicle understeer based on the evaluation of actual vehicle condition in 
comparison with a vehicle condition demanded by the driver; 
b)
Has a means to determine directly the value of vehicle's yaw rate and to 
estimate its side slip or side slip derivative with respect to time; 
c)Has a means to monitor driver steering inputs;d)
Has an algorithm to determine the need and a means to modify propulsion 
torque as necessary, so as to assist the driver in maintaining control of the 
vehicle.3.3Side slip angle
The arc-tangent of the ratio of the lateral velocity to the longitudinal velocity at the 
center of mass of the vehicle.3.4Yaw rate
The rate of change of the vehicle's heading angle, i.e. the angle per unit time of 
rotation about an axis of perpendicular to the ground around the vehicle's center of 
mass.3.5Lateral acceleration
                                                     
1)Dual wheels shall be treated as a single wheel.


<!-- Page 5 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
5 
The component of the vehicle acceleration vector in the plane perpendicular to the 
vehicle X axis (longitudinal axis) and parallel to the road surface. 
[GB/T 12549-2013, definition in 6.4.16]3.6Oversteer
The actual vehicle's yaw rate that is greater than the yaw rate that would occur at a 
certain vehicle speed as result of the Ackerman steer angle. 
[GB/T 12549-2013 definition in 7.3.3]3.7Understeer
The actual vehicle's yaw rate that is less than the yaw rate that would occur at a 
certain vehicle speed as result of the Ackerman steer angle. 
[GB/T 12549-2013, definition in 7.3.2]3.8Peak braking coefficient, PBCPeak friciton coefficient, PFC
The measured value of tyre to road surface friction coefficient based on the max 
deceleration of a rolling tyre.3.9Common space
An area on which more than one warning signal, signaling device, identification 
symbol or other message may be displayed but not simultaneously. 
3.10Static stability factor, SSF
Characteristic geometric parameters that features the static stability characteristics 
of the vehicle; its calculation formula is: SSF=T/2H. 
In which,SSF is static stability factor;T is track width 2) , with unit of meter (m);
H is height of the center of mass of the vehicle, with unit of meter (m). 
                                                     
2)
For vehicles with more than one track width, the average is used; for axles with dual wheels, the 
outer wheels are used when calculating.


<!-- Page 6 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
6 
4 
 
General requirementsESC should feature following functions:a)
Is capable of applying braking torques individually to all four wheels 1) as per a 
certain control logic;
b) Is capable of normal operation during all phases of driving including acceleration, 
coasting,deceleration(includingbraking),followingcircumstances:
1)The driver has disabled ESC;2)The vehicle speed is below 20km/h;3)
The self-test of system are completed, and vehicle driven under the 
conditions specified in 7.9.2 is not more than 2min; 
4)The vehicle is being driven in reverse.c)
ESC is capable of normal operation even if the antilock braking system (ABS) or 
traction control system (TCS) is also activated. 
5 
 
Performance requirements5.1Direction stability and response characteristics5.1.1
During test performed under the test conditions specified in Chapter 6 and the test 
procedures specified in 7.7.3-7.7.7, the vehicle with the ESC system engaged shall 
satisfy the directional stability criteria of 5.1.2 and 5.1.3, and it shall satisfy the 
responsiveness criterion of 5.1.4 during each of those tests conducted with a 
commanded steering wheel angle of 5A (A is benchmark steering wheel angle, 
determined by test in 7.6)) and greater (but not more than the limits specified in 
7.7.6).5.1.2
The yaw rate measured 1s after completion of the Sine with Dwell steering input 
(time T0+1 in Figure 1) shall not exceed 35% of the first peak value of yaw rate 
recorded after the steering wheel angle direction changes (between first and second 
peaks) (ΨPeak in Figure 1).


<!-- Page 7 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
7 
Steering wheel angle
 
Figure 1 Steering wheel position and yaw angular velocity information used 
for evaluation of lateral stability5.1.3
The yaw rate measured 1.75s after completion of the Sine with Dwell steering input 
shall not exceed 20% of the first peak value recorded after the steering wheel angle 
direction changes in this test (between first and second peaks) (ΨPeak in Figure 1). 
5.1.4
The lateral displacement of the vehicle center of mass with respect to its initial 
straight path shall be no less than 1.83m for vehicles with a maximum design total 
mass no more than 3,500kg, and 1.52m for vehicles with a maximum design total 
mass more than 3,500kg, 1.07s after the beginning of steer (BOS). For determining 
method of the beginning of steer (BOS), see 7.10.7. 
5.1.5
The lateral displacement (DL) is calculated by by the following formula. 
𝐷L = ∬ayCG𝑑𝑡In which,
ayCG is the lateral acceleration measured at the vehicle center of mass. 
As an alternative, a method based on GPS can be used. 
5.1.6
Initial point for the integration is the instant of steering initiation, i.e. beginning of 


<!-- Page 8 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
8 
steer (BOS) is the initial point for the integration. For determining method of the 
beginning of steer (BOS), see 7.10.7.5.2ESC fault detection5.2.1
The vehicle shall be equipped with a ESC signaling device that provides a warning to 
the driver of the occurrence of any fault that affects the generation or transmission of 
ESC control or response signals in the system. 
5.2.2
The ESC fault signaling device should meet following requirements: 
a)
Shall be displayed in front and clear view of the driver so that driver can inspect 
whether signaling device is normal while in the driver's designated seating 
position;b)
Shall appear perceptually upright to the driver while driving, its location is shown 
in Figure 2;c)
Shall be identified by the “ESC fault signal” symbol or the text “ESC” shown in 
Figure 2;d)Shall be yellow or amber in color;e)
When illuminated, signaling device shall be sufficiently bright to be visible to the 
driver under both daylight and night time driving conditions, when the driver has 
adapted to the ambient roadway light conditions; 
 
Figure 2 Marking symbol “ESC fault signal” 
f)
Except as provided in 5.2.2g), the ESC fault signaling device shall illuminate 
when a fault exists; and shall remain continuously illuminated under the 
conditions specified in 5.2.2 for as long as the fault exists, whenever the ignition 
system switch is in the “ON” (“RUN”) position; 
g)
Except as provided in 5.2.3, ESC fault signaling device shall be activated as a 
check of signaling device function either when the ignition locking system switch 
is turned to the “ON” (“RUN”) position when the engine is not running, or when 
the ignition locking system switch is in a position between “ON” (“RUN”) and 


<!-- Page 9 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
9 
“Start” that is designated by the manufacturer as a check position; 
h)
Signaling device shall extinguish at the next ignition cycle after the fault has 
been corrected in accordance with 7.9.4; 
i)
May also be used to indicate the fault of related systems/functions of ESC, 
including traction control, trailer stability assist, corner brake control, and other 
similar functions that use throttle and/or individual wheel torque control to 
operate and share common components with ESC. 
5.2.3
The ESC fault signaling device need not be activated when a starter interlock is in 
operation.5.2.4
The requirement of 5.2.2g) does not apply to signaling devices shown in a common 
space.5.2.5
The manufacturer may use the ESC fault signaling device in a flashing mode to 
indicate ESC operation.5.3ESC close control device and other system control device5.3.1
The manufacturer may configure an ESC close control device, which shall be 
illuminated when the vehicle's headlamps are activated and which place the ESC 
system in a mode in which it may no longer satisfy the performance requirements of 
5.1.1, 5.1.2, 5.1.3 and 5.1.4. Manufacturers may also provide other systems that 
have an ancillary effect upon ESC operation. Controls devices that place the ESC 
system in a mode in which it may no longer satisfy the performance requirements 
specified in 5.1.2, 5.1.3 and 5.1.4 are permitted, provided that the system also meets 
the requirements of 5.3.2-5.3.4.5.3.2
The vehicle's ESC system shall always return to the manufacturer's original default 
mode which meeting the requirements of Chapter 4 and Chapter 5 at the initiation of 
vehicle ignition system, regardless of what mode the driver had previously selected. 
However, the vehicle's ESC need not return to a mode that satisfies the requirements 
of 5.1.1-5.1.4 at the initiation of each new ignition cycle under following conditions: 
a)
For a four-wheel drive vehicle, the driver selects low-speed and off-road driving. 
The driving mode has the effect of locking the drive gears at the front and rear 
axles together and providing an additional gear reduction between the engine 
speed and wheel speed of at least 1.6;b)
For a four-wheel drive vehicle, the driver selects modes that is designed for 


<!-- Page 10 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
10 
operation at higher speeds on snow, sand or dirt-packed roads. The mode has 
the effect of locking the drive gears at the front and rear axles together, provided 
that in this mode the vehicle meets the stability performance requirements of 
5.1.2 and 5.1.3 under the test conditions specified in Chapter 6. However, if the 
system has more than one ESC mode that satisfies the requirements of 5.1.2 
and 5.1.3 within the drive mode selected for the previous driving, after the 
ignition system is restarted, the ESC shall return to the manufacturer's original 
default ESC mode configured for that drive mode. 
5.3.3
For a ESC control device whose only purpose is to place the ESC in a mode in which 
it will no longer satisfy the performance requirements of 5.1.1, 5.1.2, 5.1.3 and 5.1.4, 
ESC condition shall be identified by the symbol shown in Figure 3 or the text 
“ESC OFF”.
 
Figure 3 Marking symbol of ESC close control device 
5.3.4
For a control device for an ESC whose purpose is to place the ESC system in 
different modes, at least one of which may no longer satisfy the performance 
requirements of 5.1.1, 5.1.2, 5.1.3 and 5.1.4, it shall be identified by the symbol 
shown in Figure 2 with the text “OFF” adjacent to the control position for this mode. 
For a vehicle in which the ESC system mode is controlled by a multi-functional 
control device, when the control device is under the mode, the driver information 
display system shall identify clearly that the control is under this mode using either 
the symbol in 5.3.3 or the text “ESC OFF”. 
5.3.5
For a control device for another system that has the effect of placing the ESC system 
in a mode in which it no longer satisfies the performance requirements of 5.1.1, 5.1.2, 
5.1.3 and 5.1.4, it unnecessary to be identified by the mode in 5.3.3. 
5.4ESC close signaling device5.4.1
If the manufacturer installs a control device to turn OFF or reduce the performance of 
the ESC system under 5.3, the signaling device requirements of 5.4.2-5.4.5 shall be 
met in order to alert the driver to the lessened state of ESC system functionality. This 
requirement does not apply for the driver-selected mode referred to in 5.3.2b). 


<!-- Page 11 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
11 
5.4.2
The vehicle manufacturer shall provide a signaling device indicating that the vehicle 
has been put into a mode that renders ESC system unable to satisfy the 
requirements of 5.1.1, 5.1.2, 5.1.3 and 5.1.4, if such a mode is provided. 
5.4.3Signaling device should meet following requirements:a)
Shall be displayed within the driver's visual field in front, facilitate the driver in 
the driving position to check whether the status of a signaling device is normal; 
b)
Shall appear perceptually upright to the driver while driving, its location is shown 
in Figure 3;c)
Shall be identified by the symbol shown for ESC close in 5.3.3 or the text “ESC 
OFF”; Shall be identified with the English word “OFF” on or adjacent to either the 
control device referred to in 5.3.3 or 5.3.5 or the illuminated fault signaling 
device;d)Shall be yellow or amber in color;e)
When illuminated, signaling device shall be sufficiently bright to be visible to the 
driver under both daylight and night time driving conditions, when the driver has 
adapted to the ambient roadway light conditions; 
f)
Signaling device shall remain continuously illuminated for as long as the ESC is 
in a mode that renders it unable to satisfy the requirements of 5.1.1, 5.1.2, 5.1.3 
and 5.1.4;g)
Except as specified in 5.4.4 and 5.4.5, “ESC OFF” signaling device shall be 
activated as a check of signaling device function either whenever the ignition 
locking system switch is turned to the “On” (“RUN”) position, but the engine is 
not running, or when the ignition locking system switch is in a position between 
“ON” (“RUN”) and “Start” that is designated by the manufacturer as a check 
position;h)
Signaling device shall extinguish after the ESC system has been returned to its 
manufacturer's original default mode.5.4.4
The “ESC OFF” signaling device need not be activated when a starter lock is in 
operation.5.4.5
The requirement of 5.4.3g) does not apply to signaling devices shown in a common 
space.


<!-- Page 12 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
12 
5.4.6
The manufacturer may use the “ESC OFF” warning to indicate a function other than 
the default mode even if the vehicle would meet 5.1.1, 5.1.2, 5.1.3 and 5.1.4 under 
the condition.
6 
 
Test conditions6.1Ambient conditions6.1.1Ambient temperature is 0ºC-45ºC.6.1.2
The maximum wind speed is not more than 10m/s for vehicles with static stability 
factor more than 1.25; the maximum wind speed is not more than 5m/s for vehicles 
with static stability factor no more than 1.25. 
6.2Test road surface6.2.1
The tests are conducted on a dry, uniform and solid-paved surface. Surfaces with 
irregularities and undulations (such as dips and large cracks) are unsuitable. 
6.2.2
Unless otherwise specified, the road test surface has a peak braking coefficient (PBC) 
no less than 0.9 in accordance with Chapter 6 of GB/T 26987-2011 when measured 
on dry road surface; as alternative, it is allowed to measure as per 5.6.4 of GB 
21670-2008.6.2.3
The test road shall be the consistent slope and the slope is not more than 1%. 
6.3Vehicle conditions6.3.1
The ESC system under normal work condition is enabled for all testing. 
6.3.2
Vehicle is in a state of kerb mass of the complete vehicle, and total interior load mass 
of 168kg, including the test driver, test equipment and ballast as required by 
differences in the mass of test drivers, test equipment and the specified total interior 
load mass (168kg), ballast shall be placed on the floor behind the occupant front seat 
or if necessary in the front occupant foot well area. All ballast shall be secured in a 
way that prevents it from becoming dislodged during test conduct. 
6.3.3
The tyres are inflated to the vehicle manufacturer's recommended cold tyre inflation 
pressure (as specified on the vehicle's nameplate or the tyre inflation pressure label). 
Tubes may be installed to prevent tyre de-beading if necessary. 


<!-- Page 13 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
13 
6.3.4
Outriggers may be used for testing if deemed necessary for test drivers' safety. The 
outrigger should meet following requirements: 
a)
Vehicles with kerb mass less than 1,513kg in running order shall be equipped 
with light outriggers, which shall be designed with mass no more than 27kg and 
moment of inertia no more than 27kg/m2.b)
Vehicles with kerb mass of 1,513kg~2,647kg in running order shall be equipped 
with standard outriggers, which shall be designed with mass no more than 32kg 
and moment of inertia no more than 35.9kg/m2. 
c)
Vehicles with kerb mass more than 2,647kg in running order shall be equipped 
with heavy outriggers, which shall be designed with mass of no more than 39kg 
and moment of inertia of no more than 40.7kg/m2. 
6.3.5
An automatic steering device should be adopted in steering operation specified in 
7.5.3, 7.5.4, 7.6.1 and 7.7.3. The automatic steering device shall be capable of 
supplying steering torques between 40Nm-60Nm when operating with steering wheel 
velocities no more than 1,200º/s.6.3.6
Brake of test vehicle is subject to running-in in accordance with stipulations of 
Chapter 7 of GB 21670-2008.
7 
 
Test methods7.1Tyre pressure check
Confirm that tyres are inflated to the manufacturer's recommended cold tyre inflation 
pressure.7.2Signaling device check
With the vehicle stationary and the ignition system switch in the “LOCK” or “OFF” 
position, activate the ignition system switch to the “ON” (“RUN”) position or the 
appropriate position for the signaling device check. The ESC fault signaling device 
shall be activated during check of signaling device function as specified in 5.2.2g), 
and if equipped, the “ESC OFF” signaling device shall also be activated during check 
of signaling device as specified in 5.4.3g). The signaling device check is not required 
for a warning device shown in a common space as specified in 5.2.4 and 5.4.5. 
7.3ESC close control check


<!-- Page 14 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
14 
For vehicles equipped with an “ESC OFF” control device, with the vehicle stationary 
and the ignition system switch in the “LOCK” or “OFF” position, activate the ignition 
system switch to the “ON” (“RUN”) position; activate the “ESC OFF” control device 
and verify that the “ESC OFF” signaling device is illuminated as specified in 5.4.3; 
turn the ignition system to the “LOCK” or “OFF” position; again, activate the ignition 
system to the “ON” (“RUN”) position and verify that the “ESC OFF” signaling device 
has extinguished indicating that the ESC system has been reactivated as specified in 
5.3.2.7.4Brake conditioning7.4.1
Ten stops are performed from an initial speed of 56km/h, with an average 
deceleration of approximately 0.5g.7.4.2
Immediately following the series of initial speed 56km/h stops, three additional stops 
are performed from initial speed 72km/h. 
7.4.3
When executing the stops in 7.4.2, sufficient force is applied to the brake pedal to 
activate the vehicle's ABS for a majority of each braking event. 
7.4.4
Following completion of the final stop in 7.4.2, the vehicle is driven at a speed 
of 72km/h for 5min to cool the brakes.7.5Tyres wear7.5.1
Condition the tyres as per 7.5.2-7.5.4 to wear away mold sheen and achieve 
operating temperature before beginning the test items of 7.6-7.7. 
7.5.2
The test vehicle is driven around a circle 30m in diameter at a speed that produces a 
lateral acceleration of approximately 0.5g-0.6g for three clockwise laps followed by 
three counterclockwise laps.7.5.3
Using a sinusoidal steering input at a frequency of 1Hz, a peak steering wheel angle 
amplitude corresponding to a peak lateral acceleration of 0.5g-0.6g, and a vehicle 
speed of 56km/h, the vehicle is driven through four passes performing 10 cycles of 
sinusoidal steering during each test.7.5.4
The steering wheel angle amplitude of the final cycle of the final test is twice that of 
the other cycles. The maximum time permitted between all tests is 5min. 
7.6Slowly increasing steer test


<!-- Page 15 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
15 
7.6.1
The test vehicle is subjected to respectively two series of the slowly increasing steer 
test, one series uses counterclockwise steering and the other series uses clockwise 
steering; three repetitions are performed for each test series, the maximum time 
permitted between each test is 5min. Test should be performed at a constant vehicle 
speed of 80km±2km and a steering pattern that increases by 13.5º/s until a lateral 
acceleration of approximately 0.5g is obtained. 
7.6.2
Taking steering wheel angle that produces lateral acceleration of 3.0m/s2 for the test 
vehicle as a benchmark steering wheel angle, the “A” is determined, (corrected 
values according to the method specified in 7.10.4). Utilizing linear regression, “A” of 
each slowly increasing steer test is calculated and rounded to the nearest 0.1º, the 
absolute value of the six A's slowly increasing steer test is averaged and rounded to 
the nearest 0.1º and is used for sine with dwell steer test. 
7.7Sine with dwell steer tests7.7.1
The quantity “A” is determined, and initiation of the first sine with dwell steer test 
series shall begin within two hours after completion of the slowly increasing steer 
tests of 7.6.1. Prior to test without replacing the tyres, the tyre conditioning procedure 
is performed immediately prior to conducting the sine with dwell steer test of 7.5. 
7.7.2
Check that the ESC is enabled by checking that the ESC fault and “ESC OFF” (if 
provided) signaling devices are not illuminated. 
7.7.3
Perform two series of sine with dwell steering input test as shown in Figure 4: a sine 
steering input at 0.7Hz frequency with a 500ms delay beginning at the second peak 
amplitude. In which, one series uses counterclockwise steering for the first half cycle, 
and the other series uses clockwise steering for the first half cycle. The vehicle is 
allowed to cool-down between each test of 1.5min to 5min, with the vehicle 
stationary.7.7.4
The steering operation is initiated with the vehicle coasting in high gear at 80±2km. 
7.7.5
The steering wheel angle amplitude for the initial run of each series is 1.5A, then 
steering wheel steering angle amplitude is increased by amplitude 0.5A until 
reaching the steering wheel angle of the last test determined in 7.7.6. 


<!-- Page 16 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
16 
7.7.6
The steering amplitude of the final run in each series is the greater of 6.5A or 270º, 
provided the calculated magnitude of 6.5A is less than or equal to 300º. If any 
steering wheel angle amplitude (up to 6.5A) is greater than 300º, then the steering 
amplitude of the final run in each series shall be 300º. 
7.7.7
Upon completion of the two series of test runs, post processing of yaw rate and 
lateral acceleration data is done as specified in 7.10. 
Steering wheel angle
 
Figure 4 Schematic diagram of sine with dwell 
7.8Ice/snow road test
See ice/snow road test conditions and methods as per Annex A. 
7.9ESC fault inspection7.9.1
Simulate one or more ESC fault(s) by disconnecting the power source to any ESC 
component, or disconnecting any electrical connection between ESC components 
with the vehicle power OFF. When simulating an ESC fault, the electrical connections 
for the signaling device and/or optional ESC system control device are not to be 
disconnected.7.9.2
With the vehicle stationary and the ignition system switch in the “LOCK” or “OFF” 
position, activate the ignition system switch to the “Start” position and start the 
engine. Drive the vehicle forward to obtain a vehicle speed of 48±8km at the 
latest 30s after the engine has been started and within the next 2min at this speed, 
conduct at least one left and one right smooth turning operation without losing 
directional stability and one brake application. Verify that the ESC fault signaling 
device illuminates in accordance with 5.2 by the end of these operations. 
7.9.3
Stop the vehicle, turn the ignition system switch to the “OFF” or “LOCK” position. 
After a 5min, activate the vehicle's ignition system switch to the “Start” position and 


<!-- Page 17 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
17 
start the engine. Verify that the ESC fault signaling device again illuminates to signal 
a fault and remains illuminated as long as the engine is running or until the fault is 
corrected.7.9.4
Turn the ignition system switch to the “OFF” or “LOCK” position. Turn ESC back to 
normal condition, activate the vehicle’s ignition system switch to the “Start” position 
and start the engine, perform the operation specified in 7.9.2 again, and confirm that 
signaling device is extinguished in the same or similar time. 
7.10Data processing7.10.1
Yaw rate and lateral displacement measurements and calculations shall be 
processed utilizing the techniques specified in 7.10.2-7.10.9. 
7.10.2
Raw steering wheel angle data is filtered with a 12-pole phaseless Butterworth filter 
and a cut-off frequency of 10Hz. The filtered data is then zeroed to remove sensor 
offset utilizing static pre-test data.7.10.3
Raw yaw rate data is filtered with a 12-pole phaseless Butterworth filter and a cut-off 
frequency of 6Hz. The filtered data is then zeroed to remove sensor offset utilizing 
static pre-test data.7.10.4
Raw transverse angular velocity data is filtered with a 12-pole phaseless Butterworth 
filter and a cut-off frequency of 6Hz. The filtered data is then zeroed to remove 
sensor offset utilizing static pre-test data. The lateral acceleration data at the vehicle 
center of mass is determined by removing the effects caused by vehicle body roll and 
by correcting for sensor placement. For lateral acceleration data collection, the 
sensor shall be located as close as possible to the position of the vehicle's 
longitudinal and lateral centers of mass. 
7.10.5
Steering wheel velocity is determined by differentiating the filtered steering wheel 
angle data. The steering wheel velocity data is then filtered with a moving 0.1s 
running average filter.7.10.6
Lateral acceleration, yaw rate and steering wheel angle data channels are zeroed 
utilizing a defined “zeroing range”.
 
Using the steering wheel rate data calculated using the methods described in 7.10.5, 
the first instant steering wheel rate exceeding 75º/s is identified. From this point, 
steering wheel rate shall remain greater than 75º/s for at least 200ms. If the steering 
wheel rate cannot remain greater than 75º/s for at least 200ms, the next instant 


<!-- Page 18 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
18 
steering wheel rate exceeding 75º/s is identified again and the 200ms validity check 
applied. This iterative process continues until both conditions are ultimately satisfied. 
 
The “zeroing range” is defined as the 1s time period prior to the instant of the 
steering wheel rate exceeds 75º/s. In which, the instant of the steering wheel velocity 
exceeds 75º/s defines the end of the “zeroing range”). 
7.10.7
The beginning of steer (BOS) is defined as the first instance filtered and zeroed 
steering wheel angle data reaches -5º (when the steering input is counterclockwise) 
or 5º (when the steering input is clockwise) after time defining the end of the “zeroing 
range”. The value for time at the beginning of steer (BOS) is determined by 
interpolation.7.10.8
The completion of steer (COS) is defined as the time the steering wheel angle 
returns to zero at the completion of the sine with dwell steering operation. The value 
for time at the zero degree steering wheel angle is determined by interpolation. 
7.10.9
The second peak yaw rate is defined as the first local yaw rate peak produced by the 
reversal of the steering wheel. The yaw rates at 1.000s and 1.750s after completion 
of steer (COS) are determined by interpolation. 
7.10.10 Determine lateral velocity by integrating corrected, filtered and zeroed lateral 
acceleration data. Zero lateral velocity at beginning of steer (BOS). Determine lateral 
displacement by integrating zeroed lateral velocity. Zero lateral displacement at 
beginning of steer (BOS). Lateral displacement at 1.07s from beginning of steer 
(BOS) is determined by interpolation.
8 
 
ESC system technical documents8.1
To ensure a vehicle is equipped with an ESC system that meets the definition of 
Chapter 3, the vehicle manufacturer shall make available to the technical service 
upon request the documentation specified in 8.2-8.5. 
8.2
System block diagram of all hardware of ESC. The diagram shall identify what 
components are used to generate brake torques at each wheel, determine vehicle 
yaw rate, estimated side slip and driver steering inputs. 
8.3
A brief written explanation sufficient to describe the ESC system basic operational 
characteristics. This explanation shall include the outline description of the system's 
capability to apply brake torques at each wheel and how the system modifies 


<!-- Page 19 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
19 
propulsion torque during ESC system activation and show that the vehicle yaw rate is 
directly determined. Furthermore, the explanation shall also identify the vehicle 
speed range and the driving modes (acceleration, deceleration, uniform, during 
activation of the ABS or TCS) under which the ESC system can activate. 
8.4
Logic diagram. This diagram supports the explanation provided under 8.3. 
8.5
Understeer information. An outline description of the pertinent inputs to the computer 
that control ESC system hardware and how they are used to limit vehicle understeer. 


<!-- Page 20 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
20 
Annex A(Informative Annex)Ice/snow road testA.1
This Annex specifies the test items and methods for electronic stability control 
system of light vehicle performed on ice/snow road. 
A.2Double lane change testA.2.1Requirements on test site and road
A.2.1.1 Double lane change test should be performed on even and flat compact snow road 
or road with a similar peak braking power; the road peak braking coefficient should 
not have obvious change before and after test. Test site should be sufficiently 
spacious to ensure test safety.
A.2.1.2 Test passage should adopt marking pile with prominent color. In which, test passage 
and dimension of all road sections should be in compliance with stipulations of Table 
A.1 and Figure A.1; marking pile should be arranged evenly in accordance with road 
section length and interval no more than 5m as per Figure A.2. 
 
Note:
Number in the Figure is road section number, W is road section width, m; D is offset, 
m.Figure A.1 Schematic diagram of test passage


<!-- Page 21 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
21 
Table A.1 Requirements on test passage dimension 
Road section numberLength, LmOffset, DmWidth, w
m
1 
15 
--- 
1.1w + 1.25
2 
30 
--- 
--- 
3 
25 
1 
1.2w + 1.25
4 
25 
--- 
--- 
5 
15 
--- 
1.3w + 1.25Note:w is vehicle width, m;
 
Note:
Number in the Figure is road section number, and letter is marking pile number; W 
is road section width, m; D is offset, m. 
Figure A.2 Requirements on arrangement of test passage marking pile 
A.2.2Test equipment
Test equipment should be capable to measure and record vehicle speed, and should 
feature triggering device to make record of test vehicle speed at a certain instance. 
Vehicle speed measurement error should not more than ±0.5km/h. 
A.2.3Preparation of the vehicle
A.2.3.1 Vehicle mass condition should be in compliance with stipulations of 6.3.2. 
A.2.3.2 Vehicle tyre should be all-season tyre or snow tyre recommended by manufacturer, 
and should be in compliance with stipulations of 6.3.3. 
A.2.4Test procedures
A.2.4.1 Test should be performed respectively under condition of ESC ON/OFF. 


| Road section number | Length, L m | Offset, D m | Width, w m |
| --- | --- | --- | --- |
|  | 15 | --- | 1.1w + 1.25 |
|  | 30 | --- | --- |
|  | 25 |  | 1.2w + 1.25 |
|  | 25 | --- | --- |
|  | 15 | --- | 1.3w + 1.25 |



<!-- Page 22 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
22 
A.2.4.2 For the sake of test safety, it is necessary to gradually increase test vehicle speed by 
increment no more than 5km/h starting from initial vehicle speed 30km/h. 
A.2.4.3 During each test, it is necessary to accelerate vehicle speed to the specified test 
vehicle speed and maintain vehicle speed stable, and adjust vehicle condition so that 
vehicle enters test passage along the center line of test passage entrance; at the 
instance when vehicle enters road section 1 shown in Figure A.1 and Figure A.2 and 
passes pile a/a’, trigger the recording of the vehicle speed at the instance, i.e. the 
vehicle speed at entrance.
A.2.4.4 After vehicle enters test passage, driver should adjust vehicle steering device as 
much as possible, so that vehicle passes through test passage without any 
acceleration or deceleration operation of vehicle. 
A.2.4.5 If vehicle neither touches any marking pile nor deviates from test passage when 
passing through test passage, it is deemed that the test is valid; otherwise the test is 
deemed as failed, it is necessary to perform one time of test again. 
A.2.4.6 In case of continuous five times of failure under a certain vehicle speed, the test 
should be terminated, entrance speed of the last valid test is taken as test results. 
A.2.4.7 After completion of test under condition of ESC ON/OFF, compare and analyze the 
maximum entrance vehicle speed under the two conditions. The maximum entrance 
speed under condition of ESC ON should be prominently higher than the condition of 
ESC OFF.A.3Stable turning test (fixed turning radius method)A.3.1Requirements on test site and road
A.3.1.1 Vehicle stable turning test should be performed on even and flat compact snow road 
or road with a similar peak braking power; the road peak braking coefficient should 
not have obvious change before and after test. Test site should be sufficiently 
spacious to ensure test safety.
A.3.1.2 Test passage should adopt marking pile with prominent color. In which, test passage 
width and radius should be in compliance with stipulations of Figure A.3; marking pile 
should be arranged evenly along circumferential direction and as per interval of 15º. 


<!-- Page 23 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
23 
 
Note:
R is radius of a circle and should be no less than 100m, w is test vehicle width, and 
b is equivalent to 1.5m.Figure A.3 Schematic diagram of test passageA.3.2Test equipment
Test equipment should be capable of continuous measurement and record of vehicle 
driving speed, longitudinal acceleration and lateral acceleration, and should meet 
following requirements on accuracy:a)Vehicle forwarding speed: ±0.50km/h;b)Vehicle longitudinal acceleration: ±0.15m/s2;c)
Vehicle lateral acceleration: ±0.15m/s2. 
Test equipment should be capable of collection of brake pedal force or displacement, 
acceleration pedal displacement and engine rotation speed. 
A.3.3Preparation of the vehicle
A.3.3.1 Vehicle mass condition should be in compliance with stipulations of 6.3.2. 
A.3.3.2 Vehicle tyre should be all-season tyre or snow tyre recommended by manufacturer. 
A.3.4Test procedures
A.3.4.1 Test should be performed for three times respectively along clockwise and 
counterclockwise direction under condition of ESC ON/OFF. 
A.3.4.2 During the test, driver should adjust steering wheel angle, so that vehicle runs stably 
for at least two laps at as high as possible speed along circumferential test passage. 


<!-- Page 24 -->

  
  
 
 
 
 
 
 
 
 
 
 
 
April/2015
 
ACEA TranslationFor Reference Purposes Only
 
24 
A.3.4.3 Under condition of ESC OFF, it is necessary to start running along test passage at 
the minimum stable vehicle speed (or start from zero), then accelerate slowly, 
gradually and evenly (longitudinal acceleration is not more than 0.25m/s2) until the 
vehicle gets out of test passage due to instability. 
A.3.4.4 Under condition of ESC ON, it is necessary to start running along test passage at the 
minimum stable vehicle speed (or start from zero), then accelerate slowly, gradually 
and evenly (longitudinal acceleration is not more than 0.25m/s2) until the acceleration 
pedal reaches the limit position, make records of maximum stable speed after 
stability of vehicle speed.
During the test process, in case the vehicle runs out of test passage due to instability, 
it is deemed that the test fails.
A.3.4.5 After completion of test under condition of ESC ON/OFF, compare and analyze the 
maximum stable vehicle speed under the two conditions. The maximum stable speed 
under condition of ESC ON should be as close as possible to the condition of ESC 
OFF.
During the 6 times of test mentioned in A.3.4.4, in case of two times of failure of test, 
it is deemed that the stable turning test fails. 
 
 
 
 
 
 
 
 


