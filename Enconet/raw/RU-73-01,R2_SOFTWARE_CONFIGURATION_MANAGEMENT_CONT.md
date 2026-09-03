ENCONET logo

# SOFTWARE CONFIGURATION MANAGEMENT CONTROL

| Title:                | Radna uputa RU-73-01 |
|----------------------:|:---------------------|
| Revision No.:         | 2                    |
| Date Released:        | 17.11.2017.          |
| Controlled Copy No.:  |                      |

| Role      | Name and Title                                    | Signature | Date       |
|-----------|---------------------------------------------------|-----------|------------|
| Prepared: | mr.sc. Ilijana Iveković, dipl.ing., Project Engineer | [signature] | 13.11.2017. |
| Reviewed: | Vladimir Križe, dipl.ing., QA Leader              | [signature] | 14.11.2017. |
| Approved: | dr.sc. Nenad Debrecin, Director                   | [signature] | 15.11.2017. |

## Periodični pregled

| Pregledao: | Datum: | Slijedeći pregled: |
|------------|--------|---------------------|
|            |        |                     |
|            |        |                     |
|            |        |                     |
---
| Radna uputa | Naziv dok: RU-73-01 |
|-------------|-------------------|
| SOFTWARE CONFIGURATION MANAGEMENT CONTROL | Rev.2  Page 2 of 16 |

# Summary

This document presents the procedure developed to perform software configuration management control.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                 Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL              Rev.2  Page 3 of 16

# TABLE OF CONTENTS

## 1    INTRODUCTION ........................................................................................... 5

### 1.1 Purpose ....................................................................................................... 5
### 1.2 Scope........................................................................................................... 5

## 2    ABBREVIATIONS AND DEFINITIONS......................................................... 6

### 2.1 Abbreviations ............................................................................................. 6
### 2.2 Definitions................................................................................................... 6

## 3    RESPONSIBILITIES ..................................................................................... 8

### 3.1 Director........................................................................................................ 8
### 3.2 Lead Software Engineer............................................................................. 8
### 3.3 Software Engineer...................................................................................... 8
### 3.4 QA Engineer................................................................................................ 8

## 4    INSTRUCTIONS............................................................................................ 9

### 4.1 Specific Activities....................................................................................... 9
### 4.2 The Software Release Process ............................................................... 10
### 4.3 Change Control ........................................................................................ 11
### 4.4 Audits and Reviews.................................................................................. 12

## 5    REFERENCES ............................................................................................ 13

## 6    APPENDICES ............................................................................................. 14

### 6.1 OB-SCR-047 Software Change Request, Rev. 2 .................................... 15
### 6.2 OB-SCRG-048 Software Change Register Rev. 2 .................................. 16

ENCONET d.o.o., Zagreb
---
Radna uputa                                             Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL               Rev.2 Page 4 of 16

## LIST OF TABLES

N/A

## LIST OF FIGURES

N/A

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                 Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                   Rev.2 Page 5 of 16

# 1 INTRODUCTION

## 1.1 Purpose

The purpose of this procedure is to describe methods for managing software configuration including identifying a configuration, controlling a configuration, and reporting on the status of software configuration. This procedure applies to all developed software used for performing activities described in ENCONET d.o.o. Quality Assurance Program. This procedure affects personnel involved in the management of the software configuration.

## 1.2 Scope

This procedure gives the instructions for specific activities, software release process, change control activities, audits and reviews which have to be conducted in the process of software configuration management control.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                  Rev.2 Page 6 of 16

## 2 ABBREVIATIONS AND DEFINITIONS

### 2.1 Abbreviations

| Abbreviation | Full Form |
|--------------|-----------|
| CSA | Configuration Status Accounting |
| SCM | Software Configuration Management |
| QA | Quality Assurance |

### 2.2 Definitions

1. Baseline – software that has been formally reviewed and agreed upon, and that can only be changed through predefined change control procedures.

2. Configuration Control – process of evaluating and coordinating changes to software after establishment of baselines.

3. Configuration Item – a collection of hardware or software elements treated as a unit for the purpose of configuration control.

4. Configuration Status Accounting – the formal process of tracking software entities through the steps in their evolution that provides the lead software engineer with the data necessary to gauge and report project progress.

5. Major Revision of Existing Software – more than 30% of the source code has been rewritten or software operating environment has been completely changed.

6. Personal Libraries – newly created or modified versions of software entities maintained by the responsible developer.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                 Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                   Rev.2 Page 7 of 16

7. Project libraries – Periodically, work products are promoted from Personal Libraries to the Project Library where access is granted to other developers or interested parties who require all or part of the promoted entity to be stable enough for their portion of the development effort.

8. Software Configuration Management – the process of identifying and defining the configuration items in a system, controlling the release and change of these items throughout the system life cycle, recording and reporting the status of configuration items and change requests, and verifying the completeness and correctness of Configuration Items [IEE90-a]. The basic purpose of configuration management is to control code and its associated documentation so that final code and its description are consistent and represent those items that were actually reviewed and tested.

9. Software Identification Code – assures that unique name shall be used to track the software within the documents. It contains as a minimum abbreviation of the software name and version number.

10. Version Description Document – the documentation included in the software release package.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                               Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                 Rev.2 Page 8 of 16

## 3 RESPONSIBILITIES

### 3.1 Director

1. To establish appropriate measures and resources for software
   configuration management.

### 3.2 Lead Software Engineer

1. Planning and organization of software configuration management activities
   for software package.
2. Implementation of software configuration management.

### 3.3 Software Engineer

1. Conduction of software configuration management activities.

### 3.4 QA Engineer

1. The responsibility of QA engineer is that all activities related to software
   configuration management should be planned and performed in
   accordance with approved Quality Assurance Program and this Procedure.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                  Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                    Rev.2 Page 9 of 16

# 4 INSTRUCTIONS

For every software developed by ENCONET d.o.o. it shall be established specific
set of instructions for configuration management control. These instructions shall
satisfy following requirements.

## 4.1 Specific Activities

### 4.1.1 Configuration Identification:

1. Identifying a configuration items that need to be controlled.
2. These items should have accurate definition and be recorded in
   configuration documentation and baselined.
3. Baselining an item forces formal configuration change control
   processes to be effected in the event that these items are
   changed.
4. Identifying documents that describe a Software System.
5. Define software identification code which shall be used to track
   all the changes specified for this software.

### 4.1.2 Configuration Control:

1. Set the approval stages required to change a configuration item
   and to re-baseline them.
2. Prevent the unauthorized changes.
3. The need for any proposed changes to the issue should be
   carefully reviewed for need versus impact (necessity of the
   change versus cost of retesting).
4. When requirements change, configuration management
   activities should be used to control changes to design and delete
   any obsolete code.

### 4.1.3 Configuration Status Accounting:

1. Ensure the ability to record and report on the configuration
   baselines associated with each configuration item at any
   moment of time.
2. Keeping the record of all the changes made to the previous
   baseline to reach the new baseline.
3. Ensure that status of problems is identified and proposed
   changes are recorded and reported.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                   Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                     Rev.2 Page 10 of 16

## 4.2 The Software Release Process

### 4.2.1 After a software program or module is thoroughly reviewed and tested, it is considered baseline and is given an issue or version number.

### 4.2.2 Preparation of formal backups

#### 4.2.2.1 Backups should be prepared for all files that are needed to rebuild and test the software: all source files, build procedure files, data files, and executable files.

#### 4.2.2.2 Instructions should be prepared describing reinstallation and testing of the system from the backups.

### 4.2.3 Verification that all necessary documentation has been completed and matches the code approved for release.

### 4.2.4 Verification that all necessary documentation is included in Version Description Document:

1. A list of the contents.
2. A brief description of the contents.
3. A functional description of the release to inform the user of any new capabilities not included in previous releases.
4. A list of previously identified problems which have been corrected in the release.
5. A discussion of special user considerations such as actions required to use the new release (updated pages of the User's Manual). Limitations or potential problems with the new release should also be discussed along with any plans to correct these limitations or problems in future releases.
6. An inventory of the source, executable, and data units included in the release.
7. Special instructions, for installing the software on user computing systems.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                 Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                   Rev.2 Page 11 of 16

4.2.5 If the release is a new software product (i.e., not a revision of existing
software) or a major revision of existing software, it is necessary to
provide more extensive documentation than that included in the Version
Description Document. This additional documentation, which is referred
to as a User's Manual or a Code Reference Manual, should describe in
much greater detail the structure of the code and the individual program
units.

4.2.6 In applications, such as computer modeling of physical phenomena, the
theory underlying the actual source code should be described in a
separate document referred to as a Code Theory Manual.

### 4.3 Change Control

4.3.1 Primary libraries for controlling changes

1. Personal Libraries

2. Project Libraries

4.3.2 To request a change of the software OB-SCR-047 Software Change
Request (Appendix 2) has to be filled in.

4.3.3 Approval of change requests and subsequent change implementation to
the Project Library should be handled by the Lead Software Engineer.

4.3.3.1 The Lead Software Engineer takes responsibility for ensuring
that changes are implemented and tested according to
predefined procedures and that hardware/software interfaces
and interfaces between software modules are not violated.

4.3.3.2 The Lead Software Engineer also focuses on overall project
management responsibility for ensuring that design or
requirements specifications are not violated.

4.3.4 QA Engineer shall fill in OB-SCRG-048 Software Change Register
(Appendix Error! Reference source not found.).

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                    Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                      Rev.2 Page 12 of 16

## 4.4 Audits and Reviews

4.4.1 Audits and reviews are performed to verify that the software product
      matches the capabilities defined in the specifications or other contractual
      documentation and that the performance of the product fulfills the
      requirements of the user or customer.

4.4.2 Two types of audits should be performed to assure that all
      documentation (change requests, test data, and reports, etc.) relevant to
      the release are updated and complete.

      4.4.2.1 Audits shall be performed prior to the release of software or a
              major revision of existing software at minimum every 2 years.

      4.4.2.2 Physical configuration audit should be performed to determine
              whether all configuration items which should be part of the
              product baseline are present in the version specified in the
              current status report.

      4.4.2.3 A functional configuration audit ensures that functional and
              performance attributes of a configuration item are achieved as
              defined in the specifications.

4.4.3 Both audits should assure that all documentation (change requests, test
      data, and reports, etc.) relevant to the release are current and complete.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                              Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                Rev.2 Page 13 of 16

## 5 REFERENCES

[1.] ENCONET Nuklearni QA Plan, NP-SUK-001

[2.] ENCONET, PRIRUČNIK KVALITETE NORMA - ISO 9001:2015, PK-SUK-001

[3.] IAEA, Quality Assurance for Safety in Nuclear Power Plants and other Nuclear Installations, Code and Safety Guides Q1–Q14, Safety Series No. 50-C/SG-Q (1996).

[4.] 10CFR50, Appendix B, Quality Assurance

[5.] ANSI/ASME NQA-1-1994, "Quality Assurance Requirements for Nuclear Facility Applications"

[6.] Handbook of Software Quality Assurance Techniques Applicable to Nuclear Industry, Battelle Pacific Northwest Labs, Richland, WA, NUREG-CR-4640, August 1987

[7.] Manual on Quality Assurance for Computer Software Related to the Safety of Nuclear Power Plants, Technical Reports Series No. 282, IAEA, 1988

[8.] NE Krško Quality Specification QS600, Quality Assurance Program Specification for Software

[9.] IEEE Software Engineering Standards, Third Edition

[10.] ANSI/IEEE Std 828-1990

[11.] HRN EN ISO 9001:2015

[12.] IAEA Leadership and Management for Safety, IAEA Safety Standards Series, No. GSR Part 2, IAEA Vienna, 2016.

ENCONET d.o.o., Zagreb
---
Radna uputa                                             Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL               Rev.2 Page 14 of 16

## 6   APPENDICES

6.1 OB-SCR-047 Software Change Request, Rev. 2

6.2 OB-SCRG-048 Software Change Register, Rev. 2

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                                  Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                                    Rev.2 Page 15 of 16

## 6.1 OB-SCR-047 Software Change Request, Rev. 2

# Software Change Request

| Field | Value |
|-------|-------|
| Software Change Request No.: | ________________ |
| Number of Requirements: | ________________ |

**CHANGE REQUEST INITIATION:**
| Field | Value |
|-------|-------|
| Originator: | __________________________________ Date Submitted: __/__/__ |
| Software: | ____________________ Version Number: _________________ |

**CHANGE TYPE:**
- New Requirement: ___
- Requirement Change: ___
- Design Change: ___
- Other: ________________________

**REASON:**
- Performance: ___
- Customer Request: ___
- Defect: ______
- Other: ________________________

**PRIORITY:**
- Emergency: ___
- Urgent: ___
- Routine: ___
- Date Required: __/__/__

**CHANGE DESCRIPTION** (Detail functional and/or technical information. Use attachment if necessary)

Attachments: Yes / No

**TECHNICAL EVALUATION:** (To be completed by Software engineer. Use attachment if necessary.)

| Field | Value |
|-------|-------|
| Received by: | ____________________ Date Received: __/__/__ |

Modules/Screens/Tables/Files Affected:
____________________________________________________________________________
____________________________________________________________________________

Documentation Affected:                                                                 Section             Page
________________________________________________________ _______ ____
________________________________________________________ _______ ____

Attachments: Yes / No

**APPROVALS:**
| Field | Value |
|-------|-------|
| Change Approved: ______ | Change Not Approved: ______ | Hold (Future Enhancement): ______ |
| Lead Software Engineer: _____________________ Signature _______________ Date: ___/___/___ |
| QA Engineer: _________________________ Signature _________________Date: ___/___/____ |
| Date/Time for scheduled change: _______________________________ |

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                                  Naziv dok: RU-73-01
SOFTWARE CONFIGURATION MANAGEMENT CONTROL                                                               Rev.2 Page 16 of 16

## 6.2 OB-SCRG-048 Software Change Register Rev. 2

| Software Change Register | Software: |
|--------------------------|------------|
|                          | Version:   |

| Software Change Request No. | Date | Initiated by | Change Finalized by | Completion Date | QA Engineer |
|---------------------------|------|--------------|---------------------|-----------------|-------------|
|                           |      |              |                     |                 | Name:       |
|                           |      |              |                     |                 | Signature:  |
|                           |      |              |                     |                 | Name:       |
|                           |      |              |                     |                 | Signature:  |
|                           |      |              |                     |                 | Name:       |
|                           |      |              |                     |                 | Signature:  |
|                           |      |              |                     |                 | Name:       |
|                           |      |              |                     |                 | Signature:  |
|                           |      |              |                     |                 | Name:       |
|                           |      |              |                     |                 | Signature:  |
|                           |      |              |                     |                 | Name:       |
|                           |      |              |                     |                 | Signature:  |

ENCONET d.o.o., Zagreb