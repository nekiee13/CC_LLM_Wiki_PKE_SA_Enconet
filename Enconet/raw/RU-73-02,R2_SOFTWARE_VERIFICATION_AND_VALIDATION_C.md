ENCONET logo

# SOFTWARE VERIFICATION AND VALIDATION CONTROL

| Title:                | Radna uputa RU-73-02 |
|-----------------------|----------------------|
| Revision No.:         | 2                    |
| Date Released:        | 17.11.2017.          |
| Controlled Copy No.:  |                      |

| Role      | Name and Title                                    | Date       |
|-----------|---------------------------------------------------|------------|
| Prepared: | mr.sc. Ilijana Iveković, dipl.ing., Project Engineer | 13.11.2017. |
| Reviewed: | Vladimir Križe, dipl.ing., QA Leader              | 14.11.2017. |
| Approved: | dr.sc. Nenad Debrecin, Director                   | 15.11.2017. |

## Periodični pregled

| Pregledao: | Datum: | Slijedeći pregled: |
|------------|--------|---------------------|
|            |        |                     |
|            |        |                     |
|            |        |                     |
---
| Radna uputa | Naziv dok: RU-73-02 |
|-------------|---------------------|
| SOFTWARE VERIFICATION<br>AND VALIDATION CONTROL | Rev.2 Page 2 of 13 |

# Summary

This document describes methods for control of verification and validation of software.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                                            Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                                                                                   Rev.2 Page 3 of 13

# TABLE OF CONTENTS

## 1 INTRODUCTION ............................................................................................ 5

### 1.1 Purpose ........................................................................................................ 5
### 1.2 Scope............................................................................................................. 5

## 2 ABBREVIATIONS AND DEFINITIONS.......................................................... 6

### 2.1 Abbreviations .............................................................................................. 6
### 2.2 Definitions.................................................................................................... 6

## 3 RESPONSIBILITIES ...................................................................................... 7

### 3.1 Director......................................................................................................... 7
### 3.2 Lead Software Engineer.............................................................................. 7
### 3.3 Software Engineer....................................................................................... 7
### 3.4 QA Engineer................................................................................................. 7

## 4 INSTRUCTIONS............................................................................................. 8

### 4.1 V&V of Software Developed by ENCONET d.o.o. .................................... 8
### 4.2 V&V of Purchased Software ...................................................................... 9

## 5 REFERENCES ............................................................................................. 10

## 6 APPENDICES .............................................................................................. 11

### 6.1 OB-SNCR-049 Software Non-Conformance Report Rev.2 .................... 12
### 6.2 OB-SNCL-050 Software Non-Conformance Report Log Form
    Rev.2.......................................................................................................... 13

ENCONET d.o.o., Zagreb
---
Radna uputa                                     Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                           Rev.2 Page 4 of 13

## LIST OF TABLES

N/A

## LIST OF FIGURES

N/A

ENCONET d.o.o., Zagreb
---
| Radna uputa | Naziv dok: RU-73-02 |
|-------------|----------------------|
| SOFTWARE VERIFICATION | |
| AND VALIDATION CONTROL | Rev.2 Page 5 of 13 |

# 1 INTRODUCTION

## 1.1 Purpose

The purpose of this procedure is to describe methods for control of verification and validation of software. This procedure applies to all developed software used for performing activities described in ENCONET d.o.o. Quality Assurance Program. This procedure affects personnel involved in the control and implementation of software verification and validation.

## 1.2 Scope

This procedure gives instructions for verification and validation of software developed by ENCONET d.o.o. V&V activities shall be planed and performed for each software developed. Individuals and organizations developing software for ENCONET d.o.o. under contract shall be required to have procedures that meet the requirements of this document and project specified requirements.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                                                      Rev.2 Page 6 of 13

## 2 ABBREVIATIONS AND DEFINITIONS

### 2.1 Abbreviations

| Abbreviation | Definition |
|--------------|------------|
| PC           | Personal Computer |
| QA           | Quality Assurance |
| V&V          | Verification and Validation |

### 2.2 Definitions

1. Software Validation – The process of testing and evaluation of the integrated computer system (hardware and software) to ensure compliance with the functional, performance and interface requirements.

2. Software Verification – the process of determining whether or not the product of a given phase of the software development cycle fulfils the requirements imposed by the previous phase.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                    Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                                                          Rev.2 Page 7 of 13

## 3 RESPONSIBILITIES

### 3.1 Director

1. To establish appropriate measures and resources for software verification
   and validation.

### 3.2 Lead Software Engineer

1. Planning and organization of verification and validation activities for
   software package.
2. Implementation of software verification and validation.

### 3.3 Software Engineer

1. Conduction of verification and validation.

### 3.4 QA Engineer

1. The responsibility of QA engineer is that all activities related to verification
   and validation should be planned and performed in accordance with
   approved Quality Assurance Program and this Procedure.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                 Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                                                       Rev.2 Page 8 of 13

# 4 INSTRUCTIONS

## 4.1 V&V of Software Developed by ENCONET d.o.o.

### 4.1.1 Each software developed shall contain specifically developed V&V plan.

### 4.1.2 Preparation of the V&V Plan includes
1. Software Requirements Specification
2. Software Design Specification
3. Software Verification Test Plan
4. Software Validation Test Plan

### 4.1.3 Software Verification shall be performed during the software development for each determined phase of the software development cycle.

### 4.1.4 Software validation is performed at the end of the implementation phase to ensure that the code satisfies the requirements.

### 4.1.5 The results of software V&V activities shall be documented.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                                   Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                                                         Rev.2 Page 9 of 13

4.1.6 The V&V Documentation shall include:

4.1.6.1 Tasks and criteria for accomplishing the verification of the
        software in each phase.

4.1.6.2 Tasks and criteria for accomplishing the validation of the software
        at the end of the development cycle.

4.1.6.3 Specification of the hardware and software configurations
        pertinent to the software verification and validation.

4.1.6.4 Results of the execution of the software verification and validation
        activities.

4.1.6.5 Results of reviews and tests.

4.1.6.6 Summary of the status of the software.

4.1.7 Verification Reviews shall be established to ensure that planning
      process of software development and testing is adequately performed.

4.1.7.1 Verification reviews are organized by lead software engineer.

4.1.7.2 Verification reviews shall consist of:

        1. Review of Software Requirements
        2. Review of Software Design
        3. Development Documentation Review

4.1.8 Nonconformance identified during the V&V verification reviews shall be
      documented by the Software Non-Conformance Report (Annex 6.1) and
      the Software Non-Conformance Report Log Form (Annex 6.2).

4.2 V&V of Purchased Software

4.2.1 All purchased engineering software should have Verification and
      Validation documentation.

ENCONET d.o.o., Zagreb
---
Radna uputa                                                               Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                                                      Rev.2 Page 10 of 13

## 5   REFERENCES

[1.]      ENCONET Nuklearni QA Plan, NP-SUK-001

[2.]      ENCONET, PRIRUČNIK KVALITETE NORMA - ISO 9001:2015, PK-
          SUK-001

[3.]      IAEA, Quality Assurance for Safety in Nuclear Power Plants and other
          Nuclear Installations, Code and Safety Guides Q1–Q14, Safety Series
          No. 50-C/SG-Q (1996).

[4.]      10CFR50, Appendix B, Quality Assurance

[5.]      ANSI/ASME NQA-1-1994, "Quality Assurance Requirements for
          Nuclear Facility Applications"

[6.]      Handbook of Software Quality Assurance Techniques Applicable to
          Nuclear Industry, Battelle Pacific Northwest Labs, Richland, WA,
          NUREG-CR-4640, August 1987

[7.]      Manual on Quality Assurance for Computer Software Related to the
          Safety of Nuclear Power Plants, Technical Reports Series No. 282,
          IAEA, 1988

[8.]      NE Krško Quality Specification QS600, Quality Assurance Program
          Specification for Software

[9.]      IEEE Software Engineering Standards, Third Edition

[10.]     ANSI/IEEE Std 828-1990

[11.]     HRN EN ISO 9001:2015

[12.]     IAEA Leadership and Management for Safety, IAEA Safety Standards
          Series, No. GSR Part 2, IAEA Vienna, 2016.


ENCONET d.o.o., Zagreb
---
Radna uputa                                                       Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                                             Rev.2 Page 11 of 13

## 6   APPENDICES

6.1. OB-SNCR-049 Software Non-Conformance Report , Rev.2

6.2. OB-SNCL-050 Software Non-Conformance Report Log Form, Rev.2

ENCONET d.o.o., Zagreb
---

Radna uputa                                                                          Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                                                              Rev.2 Page 12 of 13

## 6.1 OB-SNCR-049 Software Non-Conformance Report Rev.2

### Software Non-Conformance Report

| Field | Value |
|-------|-------|
| Non-Conformance Report No.: | ________________ |
| Audit No.: | ________________ (if applicable) | Date: __/__/__ |

**DESCRIPTION OF NON-CONFORMANCE:**

Raised due to: V&V: ___            Internal Audit: ___        Customer Complaint: ___
Normal Working: ___

| Field | Value |
|-------|-------|
| Software: | ________________________ |
| Version Number: | _________________ |
| Procedure Reference: | _________________ |
| Reported by: | __________________________________ Date: __/__/__ |

**CORRECTIVE / PREVENTIVE ACTION PROPOSED:**

**Approval of Corrective / Preventive Action**

| Field | Value |
|-------|-------|
| Lead Software Engineer: | _____________________ Signature _______________ |
| Estimated Completion Date: | ___/___/____ |

**CORRECTIVE ACTION FINALISED:**

| Field | Value |
|-------|-------|
| Software Engineer: | ____________________ Signature ______________ Date: ___/___/____ |
| Lead Software Engineer: | _______________________ Signature _____________ Date: ___/___/____ |
| QA Engineer: | __________________________ Signature ______________Date: ___/___/____ |

ENCONET d.o.o., Zagreb

---
Radna uputa                                                                                                         Naziv dok: RU-73-02
SOFTWARE VERIFICATION
AND VALIDATION CONTROL                                                                                             Rev.2 Page 13 of 13

## 6.2   OB-SNCL-050 Software Non-Conformance Report Log Form Rev.2

| Software Non-Conformance Report Log Form | | |
|------------------------------------------|--|--|
| | Issue: | |
| | Date: | |

| Non-Conformance Report No. | Date | Reported by | Estimated Completion Date | Corrective Action Finalized by | Completion Date | QA Engineer |
|----------------------------|------|-------------|---------------------------|--------------------------------|-----------------|-------------|
| | | | | | | Name: |
| | | | | | | Signature: |
| | | | | | | Name: |
| | | | | | | Signature: |
| | | | | | | Name: |
| | | | | | | Signature: |
| | | | | | | Name: |
| | | | | | | Signature: |
| | | | | | | Name: |
| | | | | | | Signature: |
| | | | | | | Name: |
| | | | | | | Signature: |

ENCONET d.o.o., Zagreb