# Evaluation pre-fill

"""
For every query, think recursively and exhaustively until no further depth, perspectives, contradictions, or implications remain, self-audıting and stress-testing all reasoning before presenting only the most complete, consistent, and uncertainty-qualified conclusion possible.

----
Adopt a **strictly objective narrative**. Use **third-person perspective** only. Avoid personal pronouns (no 'I', 'me', 'you', or 'your'). Focus exclusively on the **objects**. Use passive voice where appropriate to maintain a de-personalized tone. Make it easy to read and keep it beginner-friendly (Flesch‑Kincaid ≤9). 

-----
Think carefully. I will provide you a multi-part context. Perform user input analysis and wait for further user input. Let me know when you're ready to continue.

"""


# Evaluation Method

"""
Think hard. You are expert quality assurance system auditor. 

GOAL: 
Perform a objective and impartial audit of quality assurance system. The audit reference framework is 10CFR50 Appendix B. 

TASK
Your task is to perform the thorough evaluation, and assess a degree of complience between `Document_2`  and 10CFR50  Appendix B requirements (`Document_1`)  as interpreted by ASME NQA-1. 

CONTEXT 
After documentation review of TEKOL's (company) quality assurance system, user generated audit notes (aka "crumbs"). Analyze them thoroughly. Remember them well as you will reference those notes repeatedly. 

<<see appended file - "tek_crumbs.csv">>

It is paramount that you use user provided "crumbs" as grounded facts (factual, verified information obtained from direct and objective observation) to enhance the objectivity of the evaluation (citations, references).

EVALUATION METHOD:
```
    Custom instruction:

    Axiom: max(ConformanceScore(Document_1, Document_2))
    subject to ∀req ∈ Document_1,
    (
        coverage(req, C) ∧
        completeness(req, L) ∧
        accuracy(req, A) ∧
        clarity(req, R) ∧
        alignment(req, G) ∧
        evidence_supported(req, E)
    )

    Core Evaluation Parameters:
    • C = f(requirement_extraction, content_relevance)
    • L = g(detail_depth, sub-requirement_inclusion)
    • A = h(information_precision, factual_correctness)
    • R = i(interpretation_clarity, unambiguous_mapping)
    • G = j(objective_consistency, process_alignment)

    Evidence Constraint:
    • E = set of objective evidence (“crumbs”) extracted from Document_2
    • evidence_supported(req, E) = TRUE if and only if:
      – at least one objective, directly observable statement, procedure, role,
        control, or record explicitly present in Document_2
        unambiguously supports req or its sub-requirement
    • Reasoning, inference, or interpretation SHALL NOT substitute for evidence

    Implementation Vectors:
    1. **max(requirements_coverage)**  
       where coverage = {
         requirement_list_exhaustiveness +
         references_matching +
         partial_gaps_detection
       }

    2. **max(comparison_quality)**  
       where comparison = {
         direct_requirement_mapping +
         partial_match_identification +
         clarity_of_alignment
       }

    3. **min(conformance_gaps)**  
       where gaps = {
         missing_requirements +
         insufficient_detail +
         unclear_mappings +
         missing_objective_evidence
       }

    Document Comparison Protocol:
    1. **Requirement Extraction**  
       - Parse Document_1 into labeled requirements  
       - Catalog each requirement with a unique ID  
       - Identify sub-requirements if present  

    2. **Implementation Extraction**  
       - Segment Document_2 into indexed sections  
       - Identify statements, procedures, controls, or records addressing each requirement  
       - Extract objective evidence items (“crumbs”) with precise references  

    3. **Conformance Analysis**  
       - Match each requirement (Document_1) with corresponding items in Document_2  
       - Evaluate coverage, completeness, accuracy, clarity, alignment  
       - Verify existence of objective evidence for each positive claim  
       - Mark requirement as fulfilled, partially fulfilled, unmet,
         or undetermined due to missing evidence  

    4. **Gap Detection**  
       - Highlight all partially met, unmet, or evidence-unsupported requirements  
       - Explicitly record missing or insufficient objective evidence  
       - Distinguish between:
         • missing implementation
         • missing documentation
         • reliance on interpretation or assumed practice  
       - Provide recommended auditor verification actions  

    5. **Synthesis & Reporting**  
       - Aggregate evidence-supported conformance results into a structured summary  
       - Generate a final compliance score based solely on evidence-supported evaluations  
       - Provide improvement and verification recommendations  

    Compliance Classification Rule:
    • A requirement SHALL NOT be classified as Fully or Substantially Compliant
      unless evidence_supported(req, E) = TRUE
    • Requirements relying on interpretation without evidence
      SHALL be downgraded accordingly

    Output Requirements:
    1. **Coverage Summary**  
       - Requirements satisfied / partially satisfied / not satisfied  
       - Explicit identification of evidence-supported vs. evidence-missing conclusions  

    2. **Gap Analysis**  
       - Detailed listing of missing or incomplete aspects  
       - Explicit listing of missing objective evidence (“crumbs”)  

    3. **Recommendations**  
       - Clear, actionable suggestions for remedying gaps  
       - Specific guidance on what an auditor must verify  

    4. **Consolidated Conformance Score**  
       - Single metric reflecting degree of evidence-supported compliance  

    Execution Standards:
    - Maintain consistency in requirement labeling and referencing  
    - Ensure thorough sub-requirement exploration  
    - Do not substitute reasoning for evidence  
    - Make all assumptions and evidence gaps explicit  
    - Present a clear, audit-defensible summary with a conformance score  

    Terminal Condition:
    ConformanceScore ≥ threshold_conformance_level
    AND
    No requirement classified as Fully or Substantially Compliant
    without objective evidence

    Begin comparative evaluation sequence now.
    END AXIOM
```

```
Query:

**Objective**  
Evaluate the conformance of *Document_2* against the requirements in *Document_1* through a structured debate simulation.  

**Debate Roles**  
- **Judge**: Oversees the debate, rules on each requirement, and maintains logical consistency.  
- **Affirmative**: Argues that *Document_2* meets each requirement of *Document_1.*  
- **Contrary**: Argues that *Document_2* does not meet the requirements and points out gaps.  

**Instructions**  
1. **Requirement-by-Requirement Debate**  
   - For each requirement from *Document_1*, Affirmative and Contrary present their points.  
   - Each must provide a likelihood score for their assertion and cite specific sections or line references from *Document_1* or *Document_2.*  
   - Each side can challenge the other’s claim up to three times *for that requirement.* If a flaw is identified, the debaters can backtrack once to correct their logic.  
   - The Judge rules whether the requirement is **Fully Met**, **Partially Met**, or **Unmet**, based on the evidence and arguments.  

2. **Mapping Process**  
   - **Parse Document_1** to extract a structured list of requirements.  
   - **Parse Document_2** to identify specific implementation details that correspond to each requirement.  
   - **Debate each requirement** (step above).  
   - **Judge’s Ruling**: Affirmative (Fully or Partially Met) or Contrary (Unmet).  

3. **Final Summary**  
   - **List of Fully Matched Requirements**: Include references to *Document_2* that support compliance.  
   - **List of Partially Matched Requirements**: Summarize gaps or conditions that are missing.  
   - **List of Missing Requirements**: State why these are not met and how it affects overall conformance.  
   - **Overall Conformance Assessment**: Provide an overview of *Document_2*’s strengths, weaknesses, and recommendations.  

DOCUMENT_1 CONTENT:
# Appendix B to Part 50—Quality Assurance Criteria for Nuclear Power Plants and Fuel Reprocessing Plants
[Appendix B To Part 50—Quality Assurance Criteria For Nuclear Power Plants And Fuel Reprocessing Plants | NRC.gov](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb.html)

While the term "applicant" is used in these criteria, the requirements are, of course, applicable after such a person has received a license to construct and operate a nuclear power plant or a fuel  reprocessing plant or has received an early site permit, design approval, design certification, or manufacturing license, as applicable. These criteria will also be used for guidance in evaluating the adequacy of quality assurance programs in use by holders of construction permits, operating licenses, early site permits, design approvals, combined licenses, and manufacturing licenses.

# Introduction. 
Every applicant for a construction permit is required by the provisions of § 50.34 to include in its preliminary safety analysis report a description of the quality assurance program to be applied to the design, fabrication, construction, and testing of the structures, systems, and components of the facility. Every applicant for an operating license is required to include, in its final safety analysis report, information pertaining to the managerial and administrative controls to be used to assure safe operation. Every applicant for a combined license under part 52 of this chapter is required by the provisions of § 52.79 of this chapter to include in its final safety analysis report a description of the quality assurance applied to the design, and to be applied to the fabrication, construction, and testing of the structures, systems, and components of the facility and to the managerial and administrative controls to be used to assure safe operation. For applications submitted after September 27, 2007, every applicant for an early site permit under part 52 of this chapter is required by the provisions of § 52.17 of this chapter to include in its site safety analysis report a description of the quality assurance program applied to site activities related to the design, fabrication, construction, and testing of the structures, systems, and components of a facility or facilities that may be constructed on the site. Every applicant for a design approval or design certification under part 52 of this chapter is required by the provisions of 10 CFR 52.137 and 52.47, respectively, to include in its final safety analysis report a description of the quality assurance program applied to the design of the structures, systems, and components of the facility. Every applicant for a manufacturing license under part 52 of this chapter is required by the provisions of 10 CFR 52.157 to include in its final safety analysis report a description of the quality assurance program applied to the design, and to be applied to the manufacture of, the structures, systems, and components of the reactor. Nuclear power plants and fuel reprocessing plants include structures, systems, and components that prevent or mitigate the consequences of postulated accidents that could cause undue risk to the health and safety of the public. This appendix establishes quality assurance requirements for the design, manufacture, construction, and operation of those structures, systems, and components. The pertinent requirements of this appendix apply to all activities affecting the safety-related functions of those structures, systems, and components; these activities include designing, purchasing, fabricating, handling, shipping, storing, cleaning, erecting, installing, inspecting, testing, operating, maintaining, repairing, refueling, and modifying.

As used in this appendix, "quality assurance" comprises all those planned and systematic actions necessary to provide adequate confidence that a structure, system, or component will perform satisfactorily in service.

Quality assurance includes quality control, which comprises those quality assurance actions related to the physical characteristics of a material, structure, component, or system which provide a means to control the quality of the material, structure, component, or system to predetermined requirements.


# I. Organization

The applicant shall be responsible for the establishment and execution of the quality assurance  
program. The applicant may delegate to others, such as contractors, agents, or consultants, the work of establishing and executing the quality assurance program, or any part thereof, but shall retain responsibility for the quality assurance program. The authority and duties of persons and organizations performing activities affecting the safety-related functions of structures, systems, and components shall be clearly established and delineated in writing. These activities include both the performing functions of attaining quality objectives and the quality assurance functions. The quality assurance functions are those of:  
(1) assuring that an appropriate quality assurance program is established and effectively executed; and  
(2) verifying, such as by checking, auditing, and inspecting, that activities affecting the safety-related  
functions have been correctly performed.

The persons and organizations performing quality assurance functions shall have sufficient authority and organizational freedom to identify quality problems; to initiate, recommend, or provide solutions; and to verify implementation of solutions. The persons and organizations performing quality assurance functions shall report to a management level so that the required authority and  
organizational freedom, including sufficient independence from cost and schedule when opposed to safety considerations, are provided. Because of the many variables involved, such as the number of personnel, the type of activity being performed, and the location or locations where activities are performed, the organizational structure for executing the quality assurance program may take various forms, provided that the persons and organizations assigned the quality assurance functions have the required authority and organizational freedom. Irrespective of the organizational structure, the individual(s) assigned the responsibility for assuring effective execution of any portion of the quality assurance program at any location where activities subject to this appendix are being performed, shall  
have direct access to the levels of management necessary to perform this function.

# II. Quality Assurance Program

The applicant shall establish at the earliest practicable time, consistent with the schedule for accomplishing the activities, a quality assurance program which complies with the  requirements of this appendix. This program shall be documented by written policies, procedures, or  instructions and shall be carried out throughout plant life in accordance with those policies, procedures, or instructions. The applicant shall identify the structures, systems, and components to be covered by the quality assurance program and the major organizations participating in the program, together with the designated functions of these organizations. The quality assurance program shall provide control over activities affecting the quality of the identified structures, systems, and components, to an extent consistent with their importance to safety. Activities affecting quality shall be accomplished under suitably controlled conditions. Controlled conditions include the use of appropriate equipment; suitable environmental conditions for accomplishing the activity, such as adequate cleanness; and assurance that all prerequisites for the given activity have been satisfied. The program shall take into account the need for ==special controls==, processes, test equipment, tools, and skills to attain the required quality, and the need for verification of quality by inspection and test. The program shall provide for indoctrination and training of personnel performing activities affecting quality as necessary to assure that suitable proficiency is achieved and maintained. The applicant shall regularly review the status and adequacy of the quality assurance program. Management of other organizations participating in the quality assurance program shall regularly review the status and adequacy of that part of the quality assurance program which they are executing.

# III. Design Control

Measures shall be established to assure that applicable regulatory requirements and the design basis, as defined in § 50.2 and as specified in the license application, for those structures, systems, and components to which this appendix applies are correctly translated into specifications, drawings, procedures, and instructions. These measures shall include provisions to assure that appropriate quality standards are specified and included in design documents and that deviations from such standards are controlled.

Measures shall also be established for the selection and review for suitability of application of materials, parts, equipment, and processes that are essential to the safety-related functions of the structures, systems and components.

Measures shall be established for the identification and control of design interfaces and for coordination among participating design organizations. These measures shall include the establishment of procedures among participating design organizations for the review, approval, release, distribution, and revision of documents involving design interfaces.

The design control measures shall provide for verifying or checking the adequacy of design, such as by the performance of design reviews, by the use of alternate or simplified calculational methods, or by the performance of a suitable testing program. The verifying or checking process shall be performed by individuals or groups other than those who performed the original design, but who may be from the same organization. Where a test program is used to verify the adequacy of a specific design feature in lieu of other verifying or checking processes, it shall include suitable qualifications testing of a prototype unit under the most adverse design conditions. Design control measures shall be applied to items such as the following: reactor physics, stress, thermal, hydraulic, and accident analyses; compatibility of materials; accessibility for inservice inspection, maintenance, and repair; and delineation of  acceptance criteria for inspections and tests.

Design changes, including field changes, shall be subject to design control measures commensurate with those applied to the original design and be approved by the organization that performed the original design unless the applicant designates another responsible organization.

# IV. Procurement Document Control

Measures shall be established to assure that applicable regulatory  
requirements, design bases, and other requirements which are necessary to assure adequate quality are suitably included or referenced in the documents for procurement of material, equipment, and services, whether purchased by the applicant or by its contractors or subcontractors. To the extent necessary, procurement documents shall require contractors or subcontractors to provide a quality assurance program consistent with the pertinent provisions of this appendix.

# V. Instructions, Procedures, and Drawings

Activities affecting quality shall be prescribed by documented instructions, procedures, or drawings, of a type appropriate to the circumstances and shall be accomplished in accordance with these instructions, procedures, or drawings. Instructions, procedures, or drawings shall include appropriate quantitative or qualitative acceptance criteria for determining that important activities have been satisfactorily accomplished.

# VI. Document Control

Measures shall be established to control the issuance of documents, such as instructions, procedures, and drawings, including changes thereto, which prescribe all activities affecting quality. These measures shall assure that documents, including changes, are reviewed for adequacy and approved for release by authorized personnel and are distributed to and used at the location where the prescribed activity is performed. Changes to documents shall be reviewed and approved by the same organizations that performed the original review and approval unless the applicant designates another responsible organization.

# VII. Control of Purchased Material, Equipment, and Services

Measures shall be established to assure that purchased material, equipment, and services, whether purchased directly or through contractors and subcontractors, conform to the procurement documents. These measures shall include provisions, as appropriate, for source evaluation and selection, objective evidence of quality furnished by the contractor or subcontractor, inspection at the contractor or subcontractor source, and examination of products upon delivery. Documentary evidence that material and equipment conform to the procurement requirements shall be available at the nuclear powerplant or fuel reprocessing plant site prior to installation or use of such material and equipment. This documentary evidence shall be retained at the nuclear powerplant or fuel reprocessing plant site and shall be sufficient to identify the specific requirements, such as codes, standards, or specifications, met by the purchased material and equipment. The effectiveness of the control of quality by contractors and subcontractors shall be assessed by the applicant or designee at intervals consistent with the importance, complexity, and quantity of the product or services.

# VIII. Identification and Control of Materials, Parts, and Components

Measures shall be established for the identification and control of materials, parts, and components, including partially fabricated assemblies. These measures shall assure that identification of the item is maintained by heat number, part number, serial number, or other appropriate means, either on the item or on records traceable to the item, as required throughout fabrication, erection, installation, and use of the item. These identification and control measures shall be designed to prevent the use of incorrect or defective material, parts, and components.

# IX. Control of Special Processes

Measures shall be established to assure that special processes, including welding, heat treating, and nondestructive testing, are controlled and accomplished by qualified personnel using qualified procedures in accordance with applicable codes, standards, specifications, criteria, and other special requirements.

# X. Inspection

A program for inspection of activities affecting quality shall be established and executed by or for the organization performing the activity to verify conformance with the documented instructions, procedures, and drawings for accomplishing the activity. Such inspection shall be performed by individuals other than those who performed the activity being inspected. Examinations, measurements, or tests of material or products processed shall be performed for each work operation where necessary to  
assure quality. If inspection of processed material or products is impossible or disadvantageous,  
indirect control by monitoring processing methods, equipment, and personnel shall be provided. Both inspection and process monitoring shall be provided when control is inadequate without both. If mandatory inspection hold points, which require witnessing or inspecting by the applicant's designated representative and beyond which work shall not proceed without the consent of its designated representative are required, the specific hold points shall be indicated in appropriate documents.

# XI. Test Control

A test program shall be established to assure that all testing required to demonstrate that structures, systems, and components will perform satisfactorily in service is identified and performed in accordance with written test procedures which incorporate the requirements and acceptance limits contained in applicable design documents. The test program shall include, as appropriate, proof tests prior to installation, preoperational tests, and operational tests during nuclear power plant or fuel reprocessing plant operation, of structures, systems, and components. Test procedures shall include provisions for  
assuring that all prerequisites for the given test have been met, that adequate test instrumentation is  
available and used, and that the test is performed under suitable environmental conditions. Test results shall be documented and evaluated to assure that test requirements have been satisfied.

# XII. Control of Measuring and Test Equipment

Measures shall be established to assure that tools, gages, instruments, and other measuring and testing devices used in activities affecting quality are properly controlled, calibrated, and adjusted at specified periods to maintain accuracy within necessary limits.

# XIII. Handling, Storage and Shipping

Measures shall be established to control the handling, storage, shipping, cleaning and preservation of material and equipment in accordance with work and inspection instructions to prevent damage or  
deterioration. When necessary for particular products, special protective environments, such as inert gas atmosphere, specific moisture content levels, and temperature levels, shall be specified and provided.

# XIV. Inspection, Test, and Operating Status

Measures shall be established to indicate, by the use of markings such as stamps, tags, labels, routing cards, or other suitable means, the status of inspections and tests performed upon individual items of the nuclear power plant or fuel reprocessing plant. These measures shall provide for the identification of items which have satisfactorily passed required inspections and tests, where necessary to preclude inadvertent bypassing of such inspections and tests. Measures shall also be established for  
indicating the operating status of structures, systems, and components of the nuclear power plant or fuel reprocessing plant, such as by tagging valves and switches, to prevent inadvertent operation.

# XV. Nonconforming Materials, Parts, or Components

Measures shall be established to control materials, parts, or components which do not conform to  requirements in order to prevent their inadvertent use or installation. These measures shall include, as appropriate, procedures for identification, documentation, segregation, disposition, and notification to affected organizations. Nonconforming items shall be reviewed and accepted, rejected, repaired or reworked in accordance with documented procedures.

# XVI. Corrective Action

Measures shall be established to assure that conditions adverse to quality, such as failures, alfunctions, deficiencies, deviations, defective material and equipment, and nonconformances are promptly identified and corrected. In the case of significant conditions adverse to quality, the measures shall assure that the cause of the condition is determined and corrective action taken to preclude repetition. The identification of the significant condition adverse to quality, the cause of the condition, and the corrective action taken shall be documented and reported to appropriate levels of management.

# XVII. Quality Assurance Records

Sufficient records shall be maintained to furnish evidence of activities affecting quality. The records shall include at least the following: Operating logs and the results of reviews, inspections, tests, audits, monitoring of work performance, and materials analyses. The records shall also include closely-related data such as qualifications of personnel, procedures, and equipment. Inspection and test records shall, as a minimum, identify the inspector or data recorder, the type of observation, the results, the acceptability, and the action taken in connection with any deficiencies noted. Records shall be  
identifiable and retrievable. Consistent with applicable regulatory requirements, the applicant shall establish requirements concerning record retention, such as duration, location, and assigned responsibility.

# XVIII. Audits

A comprehensive system of planned and periodic audits shall be carried out to verify compliance with all aspects of the quality assurance program and to determine the effectiveness of the program. The audits shall be performed in accordance with the written procedures or check lists by appropriately trained personnel not having direct responsibilities in the areas being audited. Audit results shall be documented and reviewed by management having responsibility in the area audited. Followup action,  
including reaudit of deficient areas, shall be taken where indicated.
END OF DOCUMENT_1 CONTENT


---------------------------------------------------------
DOCUMENT_2 CONTENT:

`DOCUMENT_2` will be provided in the next user input. Note that `DOCUMENT_2` is a set of documents - a main part and few appendices. The rest of documentation is available only through user provided audit notes (crumbs).

END OF DOCUMENT_2 CONTENT
---------------------------------------------------------

````

REQUESTED OUTPUT:
1. A structured debate transcript per requirement (optional if only final results are needed).  
2. A classification for each requirement. Use 5-step metric: Fully Matched, Substantially Matched, Partially Matched, Minimally Matched, Unmet). Keep in mind that some criteria may not be applicable (N/A), or in some cases further instructions/clarifications may be required to determine conformance score (Undetermined and/or Missing ).
3. A summary of overall conformance with recommendations for improvement.

-------

Perform user input analysis and wait for further user input. Let me know when you're ready to continue.

"""

----
# Crumbs

"""
These are "crumbs" (audit notes, facts):

<<see appended file - crumbs.md>>

Perform "crumbs" analysis and wait for further user input. Let me know when you're ready to continue.

```Crumbs.md


```
| filename | criterion_id | item_type | statement | evidence_quote_1 | rule_ref_keys | doc_id | criterion_name |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_II | requirement | Sistem vodenja kakovosti je vzpostavljen skladno z zahtevami standardov ISO 9001:2015, ISO 14001:2015, ISO 45001:2018 in predpisa 10 CFR 50 Appendix B ter 10 CFR Part 21. Obsega glavne dejavnosti projektiranja in inženiringa na področju procesne in energetske opreme ter jeklenih konstrukcij, vključno z delom na jedrskih elektrarnah. | Sistem vodenja zajema vse zahteve mednarodnega standarda ISO 9001, ISO 14001, ISO 45001 in predpisa 10 CFR 50 Appendix B ter 10 CFR Part 21 | 10CFR50_APPB::Criterion II; 10CFR21 | PS MOR - R08 | Quality Assurance Program |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_I | role_responsibility | Vodstvo podjetja določa odgovornosti in pooblastila, ki so dokumentirana v organizacijski shemi in matriki odgovornosti. Skrbnik sistema vodenja ima specifična pooblastila za zagotavljanje skladnosti sistema, poročanje vodstvu in spodbujanje osredotočenosti na odjemalce. | Vodstvo zagotavlja določenost odgovornosti z: organizacijsko shemo (Priloga - PPS 02), matriko odgovornosti (Priloga - PPS 04), opisi delovnih mest |  | PS MOR - R08 | Organization |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_II | process_step | Kompetentnost osebja se zagotavlja s planiranjem usposabljanja, uvajanjem novozaposlenih z mentorstvom in preverjanjem pridobljenega znanja. Zahteve glede kompetenc so opredeljene v opisih delovnih mest. | Kompetentnost zaposlenih in pogodbenih sodelavcev se zagotavlja na podlagi planiranja usposabljanja in izobraževanja ali pridobivanjem izkušenj. |  | PS MOR - R08 | Quality Assurance Program |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_V | requirement | Sistem vodenja temelji na dokumentiranih informacijah, ki vključujejo poslovnik, sistemske postopke, operativne postopke, navodila za delo in obrazce. Aktivnosti se izvajajo na podlagi predpisane dokumentacije. | Dokumentirana informacija (v nadaljevanju dokumenti) s katero so predpisane zahteve za izvajanje sistema vodenja... sistemska dokumentacija (poslovnik, opisi procesov, postopki, navodila, ...) |  | PS MOR - R08 | Instructions, Procedures, and Drawings |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_VI | control | Vzpostavljen je postopek za ustvarjanje, posodabljanje in obvladovanje dokumentov. Dokumenti se pred uporabo pregledajo, odobrijo in identificirajo (naslov, datum, revizija). Neveljavni dokumenti se odstranijo ali ustrezno označijo. | Za obvladovano izdelavo in spreminjanje dokumentirane informacije izvajamo naslednje aktivnosti: pred izdelavo se preveri potrebnost dokumentov, izdelani dokumenti se pregledajo in po potrebi posodobijo ter odobrijo za uporabo |  | PS MOR - R08 | Document Control |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_XVII | requirement | Zapisi, ki dokazujejo opravljene aktivnosti in rezultate, se hranijo, vzdržujejo in ščitijo pred poškodbami. Postopek SP 01.02 podrobneje določa obvladovanje zapisov. | Hranjenje dokumentirane informacije (v nadaljevanju zapisi) se izvede predvsem za tisto, ki nastane kot rezultat neke aktivnosti in služi za dokazovanje opravljenih aktivnostih |  | PS MOR - R08 | Quality Assurance Records |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_III | process_step | Proces projektiranja (snovanja in razvoja) je planiran in obvladovan. Vključuje določitev vhodnih zahtev, preglede razvoja, overjanje (verifikacijo) in validacijo. Spremembe razvoja se identificirajo, pregledajo in odobrijo. | Določen je način obvladovanja snovanja in razvoja izdelkov (SP 02.01) kot glavnega procesa |  | PS MOR - R08 | Design Control |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_VII | control | Dobavitelji se ocenjujejo in izbirajo na podlagi sposobnosti. Vzdržuje se seznam odobrenih dobaviteljev. Dobavljeno blago se preverja (overja) glede skladnosti z zahtevami ob prevzemu ali pri dobavitelju. | Dobavitelji so ocenjeni in izbrani na osnovi njihove sposobnosti z dokumentom Ocenjevanje dobaviteljev. |  | PS MOR - R08 | Control of Purchased Material, Equipment, and Services |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_IV | control | Nabavni dokumenti (naročila) morajo vsebovati natančno opredelitev blaga, zahteve za kakovost, roke in druge pogoje. Naročila se pred izdajo pregledajo glede popolnosti. | Naročilni dokumenti vsebujejo zahtevane karakteristike... kot so: natančna opredelitev naročenega blaga/storitev, kakovostne karakteristike... relevantne okoljske zahteve... posebne zahteve |  | PS MOR - R08 | Procurement Document Control |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_VII | process_step | Za komercialno opremo v varnostni klasi se izvaja postopek dedikacije po postopku SP 03.03. | V primeru nabave komercialne opreme in storitev za katero so s strani naročnika postavljene posebne zahteve (oprema v varnostni klasi) se izvaja postopek dedikacije opreme in/ali storitev po postopku SP 03.03. |  | PS MOR - R08 | Control of Purchased Material, Equipment, and Services |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_IX | control | Specialni procesi, kot so varjenje, toplotna obdelava in protikorozijska zaščita, se validirajo in izvajajo pod nadzorom usposobljenega osebja z uporabo preverjene opreme. | validirajo se osnovni in specialni procesi. |  | PS MOR - R08 | Control of Special Processes |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_VIII | control | Izdelki in storitve so identificirani z namenom sledljivosti (npr. številka projekta, šarža, šifra). Sledljivost se vzdržuje od materialov do končnega izdelka. | Identifikacija storitev se izvaja predvsem preko dokumentacije in sicer za projektiranje in inženiring projekte s številko projekta kot osnovnim identifikacijskim podatkom |  | PS MOR - R08 | Identification and Control of Materials, Parts, and Components |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_XIII | requirement | Ohranitev izdelkov se zagotavlja s postopki za identifikacijo, pakiranje, skladiščenje in transport, da se preprečijo poškodbe ali poslabšanje kakovosti. | Ohranitev izdelkov in sicer lastnih, dobaviteljevih in odjemalčevih se zagotavlja z izvajanjem postopkov za identifikacijo, ravnanje, pakiranje, skladiščenje, transport, dostavo/predajo in preprečevanje poškodb. |  | PS MOR - R08 | Handling, Storage, and Shipping |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_XII | control | Merilna oprema se obvladuje (označuje, overja, kalibrira) v skladu z zahtevami. Če se uporablja oprema dobaviteljev, se njena ustreznost preverja. | Viri potrebni za nadzor in merjenje skladnosti izdelkov z zahtevami so merilna oprema... Nadzorna in merilna oprema uporabljena pri inženiring procesih je obvladovana preko dobavitelja oz. pogodbenih izvajalcev, ki izvajajo pogodbene zahteve glede označevanja, overjanja in/ali kalibriranja |  | PS MOR - R08 | Control of Measuring and Test Equipment |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_X | process_step | Izvaja se nadzor in merjenje skozi celoten proces izvedbe. Sprostitev izdelkov se izvede šele, ko so opravljeni vsi predpisani nadzori in izpisana dokumentacija o skladnosti. | Izdelki in storitve so nadzirani skozi ves proces izvedbe. Nadzor se planira s samo izvedbo procesa ter ustreznimi procesnimi dokumenti |  | PS MOR - R08 | Inspection |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_XV | control | Neskladni izdelki se identificirajo in obvladujejo, da se prepreči njihova nenamerna uporaba. Možni ukrepi vključujejo korekcijo, izločitev, zadržanje ali sprejem s koncesijo. | Neskladnosti se ugotavljajo in evidentirajo (SP 01.06) v celotnem sistemu vodenja. Neskladnosti se odpravijo in evidentirajo. |  | PS MOR - R08 | Nonconforming Materials, Parts, or Components |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_XVI | process_step | Korektivni ukrepi se izvajajo za odpravo vzrokov neskladnosti in preprečitev njihovega ponavljanja. Vsi ukrepi se evidentirajo in preverjajo glede učinkovitosti. | Korektivni ukrepi se izvedejo na osnovi že opravljenih aktivnostih in ugotovljenih vzrokov neskladnosti, da se prepreči ponavljanje neskladnosti. |  | PS MOR - R08 | Corrective Action |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_XVIII | process_step | Notranje presoje se izvajajo periodično (vsaj enkrat letno) za preverjanje skladnosti in učinkovitosti sistema vodenja. Izvajajo jih usposobljeni in neodvisni presojevalci. | Notranje presoje so planirane in se za sistem izvedejo vsaj enkrat letno. |  | PS MOR - R08 | Audits |
| Poslovnik sistemov PS MOR - R08 - SI - 01.09.2025 | APP_B_XV | process_step | Poseben poudarek je na obvladovanju neskladnosti pri projektih jedrske tehnologije, kjer se upoštevajo posebne zahteve odjemalca in postopki poročanja. | Posebej se obravnavajo neskladnosti pri izvedbi projektov na področju jedrske tehnologije kjer se izvedejo aktivnosti po posebnem postopku oz. v skladu z zahtevami odjemalca kar je podrobneje opisano v sistemskem postopku SP 01.06. |  | PS MOR - R08 | Nonconforming Materials, Parts, or Components |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 3 (Predstavitev podjetja in dejavnosti) maps to 10 CFR 50 Appendix B Criterion I. | 3 PREDSTAVITEV PODJETJA IN DEJAVNOSTI \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 4 (Kontekst organizacije) maps to 10 CFR 50 Appendix B Criterion II. | 4 KONTEKST ORGANIZACIJE \| ... \| II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 4.3 (Področje uporabe in obseg sistema vodenja) maps to 10 CFR 50 Appendix B Criterion I. | 4.3 Področje uporabe in obseg sistema vodenja \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 4.4 (Sistem vodenja in njegovi procesi) maps to 10 CFR 50 Appendix B Criterion I. | 4.4 Sistem vodenja in njegovi procesi \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 4.4 (Sistem vodenja in njegovi procesi) maps to 10 CFR 50 Appendix B Criterion II. | 4.4 Sistem vodenja in njegovi procesi \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 5 (Voditeljstvo) maps to 10 CFR 50 Appendix B Criterion I. | 5 VODITELJSTVO \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 5.1 (Voditeljstvo in zavezanost) maps to 10 CFR 50 Appendix B Criterion I. | 5.1 Voditeljstvo in zavezanost \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 5.1 (Voditeljstvo in zavezanost) maps to 10 CFR 50 Appendix B Criterion II. | 5.1 Voditeljstvo in zavezanost \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 5.2 (Politika) maps to 10 CFR 50 Appendix B Criterion I. | 5.2 Politika \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 5.2 (Politika) maps to 10 CFR 50 Appendix B Criterion II. | 5.2 Politika \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 5.3 (Organizacijske vloge, odgovornosti in pooblastila) maps to 10 CFR 50 Appendix B Criterion I. | 5.3 Organizacijske vloge, odgovornosti in pooblastila \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 6 (Planiranje) maps to 10 CFR 50 Appendix B Criterion I. | 6 PLANIRANJE \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 6 (Planiranje) maps to 10 CFR 50 Appendix B Criterion II. | 6 PLANIRANJE \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 6.1 (Ukrepi za obravnavanje tveganj in priložnosti) maps to 10 CFR 50 Appendix B Criterion I. | 6.1 Ukrepi za obravnavanje tveganj in priložnosti \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 6.1 (Ukrepi za obravnavanje tveganj in priložnosti) maps to 10 CFR 50 Appendix B Criterion II. | 6.1 Ukrepi za obravnavanje tveganj in priložnosti \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 6.1.1 (Splošno) maps to 10 CFR 50 Appendix B Criterion I. | 6.1.1 Splošno \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 6.1.1 (Splošno) maps to 10 CFR 50 Appendix B Criterion II. | 6.1.1 Splošno \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 6.2 (Cilji in planiranje za njihovo doseganje) maps to 10 CFR 50 Appendix B Criterion I. | 6.2 Cilji in planiranje za njihovo doseganje \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 6.2 (Cilji in planiranje za njihovo doseganje) maps to 10 CFR 50 Appendix B Criterion II. | 6.2 Cilji in planiranje za njihovo doseganje \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_V | reference | Internal Section 6.3 (Planiranje sprememb) maps to 10 CFR 50 Appendix B Criterion V. | 6.3 Planiranje sprememb \| ... \| V. Navodila, postopki in načrti |  | PPS_01_Priloga_R07 | Instructions, Procedures, and Drawings |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 7 (Podpora) maps to 10 CFR 50 Appendix B Criterion I. | 7 PODPORA \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 7.1 (Viri) maps to 10 CFR 50 Appendix B Criterion I. | 7.1 Viri \| ... \| I. Organizacija XII. Kontrola merilne in testne opreme V. Navodila, postopki in načrti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_XII | reference | Internal Section 7.1 (Viri) maps to 10 CFR 50 Appendix B Criterion XII. | 7.1 Viri \| ... \| I. Organizacija XII. Kontrola merilne in testne opreme V. Navodila, postopki in načrti |  | PPS_01_Priloga_R07 | Control of Measuring and Test Equipment |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_V | reference | Internal Section 7.1 (Viri) maps to 10 CFR 50 Appendix B Criterion V. | 7.1 Viri \| ... \| I. Organizacija XII. Kontrola merilne in testne opreme V. Navodila, postopki in načrti |  | PPS_01_Priloga_R07 | Instructions, Procedures, and Drawings |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 7.2 (Kompetentnost) maps to 10 CFR 50 Appendix B Criterion I. | 7.2 Kompetentnost \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 7.2 (Kompetentnost) maps to 10 CFR 50 Appendix B Criterion II. | 7.2 Kompetentnost \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 7.3 (Ozaveščenost) maps to 10 CFR 50 Appendix B Criterion I. | 7.3 Ozaveščenost \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 7.3 (Ozaveščenost) maps to 10 CFR 50 Appendix B Criterion II. | 7.3 Ozaveščenost \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 7.4 (Komuniciranje) maps to 10 CFR 50 Appendix B Criterion I. | 7.4 Komuniciranje \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 7.4 (Komuniciranje) maps to 10 CFR 50 Appendix B Criterion II. | 7.4 Komuniciranje \| ... \| I. Organizacija II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 7.5 (Dokumentirane informacije) maps to 10 CFR 50 Appendix B Criterion II. | 7.5 Dokumentirane informacije \| ... \| II. Zagotavljanje kakovosti V. Navodila, postopki in načrti VI. Obvladovanje dokumentov XVII. QA zapisi |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_V | reference | Internal Section 7.5 (Dokumentirane informacije) maps to 10 CFR 50 Appendix B Criterion V. | 7.5 Dokumentirane informacije \| ... \| II. Zagotavljanje kakovosti V. Navodila, postopki in načrti VI. Obvladovanje dokumentov XVII. QA zapisi |  | PPS_01_Priloga_R07 | Instructions, Procedures, and Drawings |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_VI | reference | Internal Section 7.5 (Dokumentirane informacije) maps to 10 CFR 50 Appendix B Criterion VI. | 7.5 Dokumentirane informacije \| ... \| II. Zagotavljanje kakovosti V. Navodila, postopki in načrti VI. Obvladovanje dokumentov XVII. QA zapisi |  | PPS_01_Priloga_R07 | Document Control |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_XVII | reference | Internal Section 7.5 (Dokumentirane informacije) maps to 10 CFR 50 Appendix B Criterion XVII. | 7.5 Dokumentirane informacije \| ... \| II. Zagotavljanje kakovosti V. Navodila, postopki in načrti VI. Obvladovanje dokumentov XVII. QA zapisi |  | PPS_01_Priloga_R07 | Quality Assurance Records |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 8 (Delovanje) maps to 10 CFR 50 Appendix B Criterion I. | 8 DELOVANJE \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 8.1 (Planiranje in obvladovanje delovanja) maps to 10 CFR 50 Appendix B Criterion I. | 8.1 Planiranje in obvladovanje delovanja \| ... \| I. Organizacija III. Projektiranje V. Navodila, postopki in načrti |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_III | reference | Internal Section 8.1 (Planiranje in obvladovanje delovanja) maps to 10 CFR 50 Appendix B Criterion III. | 8.1 Planiranje in obvladovanje delovanja \| ... \| I. Organizacija III. Projektiranje V. Navodila, postopki in načrti |  | PPS_01_Priloga_R07 | Design Control |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_V | reference | Internal Section 8.1 (Planiranje in obvladovanje delovanja) maps to 10 CFR 50 Appendix B Criterion V. | 8.1 Planiranje in obvladovanje delovanja \| ... \| I. Organizacija III. Projektiranje V. Navodila, postopki in načrti |  | PPS_01_Priloga_R07 | Instructions, Procedures, and Drawings |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 8.2 (Zahteve za izdelke in storitve) maps to 10 CFR 50 Appendix B Criterion II. | 8.2 Zahteve za izdelke in storitve \| ... \| II. Zagotavljanje kakovosti V. Navodila, postopki in načrti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_V | reference | Internal Section 8.2 (Zahteve za izdelke in storitve) maps to 10 CFR 50 Appendix B Criterion V. | 8.2 Zahteve za izdelke in storitve \| ... \| II. Zagotavljanje kakovosti V. Navodila, postopki in načrti |  | PPS_01_Priloga_R07 | Instructions, Procedures, and Drawings |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_III | reference | Internal Section 8.3 (Snovanje in razvoj izdelkov in storitev) maps to 10 CFR 50 Appendix B Criterion III. | 8.3 Snovanje in razvoj izdelkov in storitev \| ... \| III. Projektiranje |  | PPS_01_Priloga_R07 | Design Control |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_IV | reference | Internal Section 8.4 (Obvladovanje procesov... zunanjih ponudnikov) maps to 10 CFR 50 Appendix B Criterion IV. | 8.4 Obvladovanje procesov, izdelkov in storitev zunanjih ponudnikov \| ... \| IV. Obvladovanje nabavnih dokumentov VII. Kontrola nabavljenih materialov, opreme in storitev |  | PPS_01_Priloga_R07 | Procurement Document Control |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_VII | reference | Internal Section 8.4 (Obvladovanje procesov... zunanjih ponudnikov) maps to 10 CFR 50 Appendix B Criterion VII. | 8.4 Obvladovanje procesov, izdelkov in storitev zunanjih ponudnikov \| ... \| IV. Obvladovanje nabavnih dokumentov VII. Kontrola nabavljenih materialov, opreme in storitev |  | PPS_01_Priloga_R07 | Control of Purchased Material, Equipment, and Services |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_VIII | reference | Internal Section 8.5 (Proizvodnja in izvedba storitev) maps to 10 CFR 50 Appendix B Criterion VIII. | 8.5 Proizvodnja in izvedba storitev \| ... \| VIII. Označevanje in kontrola materiala in opreme |  | PPS_01_Priloga_R07 | Identification and Control of Materials, Parts, and Components |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_IX | reference | Internal Section 8.5 (Proizvodnja in izvedba storitev) maps to 10 CFR 50 Appendix B Criterion IX. | 8.5 Proizvodnja in izvedba storitev \| ... \| IX. Nadzor specialnih procesov |  | PPS_01_Priloga_R07 | Control of Special Processes |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_X | reference | Internal Section 8.5 (Proizvodnja in izvedba storitev) maps to 10 CFR 50 Appendix B Criterion X. | 8.5 Proizvodnja in izvedba storitev \| ... \| X. Kontrola |  | PPS_01_Priloga_R07 | Inspection |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_XIII | reference | Internal Section 8.5 (Proizvodnja in izvedba storitev) maps to 10 CFR 50 Appendix B Criterion XIII. | 8.5 Proizvodnja in izvedba storitev \| ... \| XIII. Rokovanje z opremo in materiali, skladiščenje in transport |  | PPS_01_Priloga_R07 | Handling, Storage, and Shipping |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_XIV | reference | Internal Section 8.5 (Proizvodnja in izvedba storitev) maps to 10 CFR 50 Appendix B Criterion XIV. | 8.5 Proizvodnja in izvedba storitev \| ... \| XIV. Status kontrole, testiranj in izvedbe |  | PPS_01_Priloga_R07 | Inspection, Test, and Operating Status |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_IX | reference | Internal Section 8.6 (Sprostitev izdelkov in storitev) maps to 10 CFR 50 Appendix B Criterion IX. | 8.6 Sprostitev izdelkov in storitev \| ... \| IX. Nadzor specialnih procesov X. Kontrola XI. Testiranje |  | PPS_01_Priloga_R07 | Control of Special Processes |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_X | reference | Internal Section 8.6 (Sprostitev izdelkov in storitev) maps to 10 CFR 50 Appendix B Criterion X. | 8.6 Sprostitev izdelkov in storitev \| ... \| IX. Nadzor specialnih procesov X. Kontrola XI. Testiranje |  | PPS_01_Priloga_R07 | Inspection |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_XI | reference | Internal Section 8.6 (Sprostitev izdelkov in storitev) maps to 10 CFR 50 Appendix B Criterion XI. | 8.6 Sprostitev izdelkov in storitev \| ... \| IX. Nadzor specialnih procesov X. Kontrola XI. Testiranje |  | PPS_01_Priloga_R07 | Test Control |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 9 (Vrednotenje izvedbe) maps to 10 CFR 50 Appendix B Criterion I. | 9 VREDNOTENJE IZVEDBE \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 9.1 (Nadzorovanje, merjenje, analiziranje in vrednotenje) maps to 10 CFR 50 Appendix B Criterion II. | 9.1 Nadzorovanje, merjenje, analiziranje in vrednotenje \| ... \| II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 9.1.1 (Splošno) maps to 10 CFR 50 Appendix B Criterion II. | 9.1.1 Splošno \| ... \| II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 9.1.2 (Zadovoljstvo odjemalcev) maps to 10 CFR 50 Appendix B Criterion II. | 9.1.2 Zadovoljstvo odjemalcev \| ... \| II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_II | reference | Internal Section 9.1.3 (Analiziranje in vrednotenje) maps to 10 CFR 50 Appendix B Criterion II. | 9.1.3 Analiziranje in vrednotenje \| ... \| II. Zagotavljanje kakovosti |  | PPS_01_Priloga_R07 | Quality Assurance Program |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_XVIII | reference | Internal Section 9.2 (Notranja presoja) maps to 10 CFR 50 Appendix B Criterion XVIII. | 9.2 Notranja presoja \| ... \| XVIII. Presoje |  | PPS_01_Priloga_R07 | Audits |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 9.3 (Vodstveni pregled) maps to 10 CFR 50 Appendix B Criterion I. | 9.3 Vodstveni pregled \| ... \| I. Organizacija XVIII. Presoje |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_XVIII | reference | Internal Section 9.3 (Vodstveni pregled) maps to 10 CFR 50 Appendix B Criterion XVIII. | 9.3 Vodstveni pregled \| ... \| I. Organizacija XVIII. Presoje |  | PPS_01_Priloga_R07 | Audits |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 10 (Izboljšave) maps to 10 CFR 50 Appendix B Criterion I. | 10 IZBOLJŠAVE \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 10.1 (Splošno) maps to 10 CFR 50 Appendix B Criterion I. | 10.1 Splošno \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_XV | reference | Internal Section 10.2 (Neskladnosti, incidenti in korektivni ukrepi) maps to 10 CFR 50 Appendix B Criterion XV. | 10.2 Neskladnosti, incidenti in korektivni ukrepi \| ... \| XV. Neskladnosti materialov, opreme ali storitev XVI. Korektivni ukrepi |  | PPS_01_Priloga_R07 | Nonconforming Materials, Parts, or Components |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_XVI | reference | Internal Section 10.2 (Neskladnosti, incidenti in korektivni ukrepi) maps to 10 CFR 50 Appendix B Criterion XVI. | 10.2 Neskladnosti, incidenti in korektivni ukrepi \| ... \| XV. Neskladnosti materialov, opreme ali storitev XVI. Korektivni ukrepi |  | PPS_01_Priloga_R07 | Corrective Action |
| Priloga PPS 01 - Primerjava poslovnika in standardov R07.docx | APP_B_I | reference | Internal Section 10.3 (Nenehno izboljševanje) maps to 10 CFR 50 Appendix B Criterion I. | 10.3 Nenehno izboljševanje \| ... \| I. Organizacija |  | PPS_01_Priloga_R07 | Organization |
| Priloga PPS 02 - Organizacijska shema MOR d.o.o. R04.doc | APP_B_I | role_responsibility | The organizational structure establishes the Director as the top management authority, directly overseeing the System Administrator, QA Engineer, Commercial department, Administration, Design, and Engineering Projects. | DIR["**MOR d.o.o.**<br>Direktor"] |  | Priloga PPS 02 | Organization |
| Priloga PPS 02 - Organizacijska shema MOR d.o.o. R04.doc | APP_B_I | role_responsibility | The Quality Assurance function is represented by the QA Engineer and System Administrator, who report directly to the Director, ensuring organizational independence from production/execution lines. | SKR["SKRBNIK SISTEMA"] |  | Priloga PPS 02 | Organization |
| Priloga PPS 02 - Organizacijska shema MOR d.o.o. R04.doc | APP_B_I | role_responsibility | The Commercial function encompasses sales and purchasing (nabava) responsibilities. | KOM["KOMERCIALA<br>(prodaja, nabava)"] |  | Priloga PPS 02 | Organization |
| Priloga PPS 02 - Organizacijska shema MOR d.o.o. R04.doc | APP_B_I | process_step | Operational processes for Design (Projektiranje) and Engineering Projects (Inženiring Projekti) are structured to flow from Planning and Preparation to Execution. | PROJ["PROJEKTIRANJE"] |  | Priloga PPS 02 | Organization |
| Priloga PPS 02 - Organizacijska shema MOR d.o.o. R04.doc | APP_B_VII | definition | The scope of Suppliers includes provision of materials (raw, auxiliary), equipment (devices, protective equipment), and services (calculations, production, assembly, welding, supervision, measurements, destructive and non-destructive testing, transport). | DOB["**DOBAVITELJI**<br><br>• materiali – surovine, pomožni materiali<br>• naprave, oprema, zaščitna oprema<br>• storitve (izračuni, proizvodnja, montaža, varjenje,<br>nadzor, meritve, porušne in neporušne preiskave,<br>transport, ...)"] |  | Priloga PPS 02 | Control of Purchased Material, Equipment, and Services |
| Priloga PPS 02 - Organizacijska shema MOR d.o.o. R04.doc | APP_B_I | role_responsibility | External interfaces establish information flows between Management/Commercial functions and Customers/Suppliers, and material flows from Suppliers to Project Execution and then to Customers. | DIR -.-> KUP |  | Priloga PPS 02 | Organization |
| Priloga PPS 02 - Organizacijska shema MOR d.o.o. R04.doc | APP_B_VI | record | The organizational schema is a controlled document (Revision 4), approved by Barbara Maček on March 27, 2017. | Odobrila: Barbara Maček |  | Priloga PPS 02 | Document Control |
| POLITIKA_PODJETJA.md | APP_B_II | requirement | MOR d.o.o. has defined and accepted a quality, environmental, and health and safety policy as an integral part of its management policy to satisfy customer needs in engineering and design. | Podjetje MOR d.o.o. je opredelilo in sprejelo politiko kakovosti, okoljsko politiko in politiko varnosti in zdravja pri delu kot sestavni del politike vodenja podjetja |  | MOR_POLITIKA_2020 | Quality Assurance Program |
| POLITIKA_PODJETJA.md | APP_B_II | requirement | The company maintains its management system in compliance with the requirements of 10 CFR 50 Appendix B and 10 CFR Part 21. | vzdržujemo skladnost sistema vodenja z zahtevami predpisa 10 CFR50 Appendix B in 10 CFR Part 21 | 10CFR50_APPB::APP_B_II; 10CFR21::General | MOR_POLITIKA_2020 | Quality Assurance Program |
| POLITIKA_PODJETJA.md | APP_B_II | process_step | The company provides appropriate and satisfactory resources, including training, to achieve sustainable compliance with the set policy and goals. | zagotavljamo primerne in zadovoljive vire, vključujoč usposabljanje, za doseganje trajne skladnosti z zastavljeno politiko in cilji |  | MOR_POLITIKA_2020 | Quality Assurance Program |
| POLITIKA_PODJETJA.md | APP_B_II | process_step | The company evaluates its performance against the set policy and goals and seeks opportunities for improvement in quality management. | ocenjujemo uspešnost podjetja glede na postavljeno politiko in cilje ter iščemo možnosti izboljševanja vodenja kakovosti |  | MOR_POLITIKA_2020 | Quality Assurance Program |
| POLITIKA_PODJETJA.md | APP_B_XVIII | process_step | A process of auditing and reviewing the management system is established to determine opportunities for improvement and effectiveness in quality management. | vzpostavljen je proces presojanja in pregledovanja sistema vodenja z namenom določevanja priložnosti za izboljševanje sistema ter posledično večje učinkovitosti na področju kakovosti |  | MOR_POLITIKA_2020 | Audits |
| POLITIKA_PODJETJA.md | APP_B_I | role_responsibility | The policy represents a commitment by management and employees to quality management, environmental protection, and risk management. | V skladu z zavezanostjo vodstva in zaposlenih za vodenje kakovosti, varovanju okolja ter obvladovanju tveganj |  | MOR_POLITIKA_2020 | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For general content (Content, General, Presentation of company and activities) (clauses 1, 2, 3), the Director is Responsible (O). | 1 2 3 \| VSEBINA SPLOŠNO PREDSTAVITEV PODJETJA IN DEJAVNOSTI \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 4 'Context of the organization', the Director is Responsible (O). | 4 \| KONTEKST ORGANIZACIJE \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 4.1 'Organization and its context', the Director is Responsible (O). The System Administrator and QA Engineer Cooperate (S). The Head of Commercial, Head of Design, Head of Engineering Project, Head of Administration, and Executors are Informed (I). | 4.1 \| Organizacija in njen kontekst \| O (Direktor), S (Skrbnik), S (QA) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 4.2 'Needs and expectations of interested parties', the Director is Responsible (O). All other roles (System Administrator, QA Engineer, Head of Commercial, Head of Design, Head of Engineering Project, Head of Administration, Executors) Cooperate (S). | 4.2 \| Potrebe in pričakovanja zainteresiranih strani \| O (Direktor), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 4.3 'Scope of the management system', the Director is Responsible (O). The System Administrator and QA Engineer Cooperate (S). Others are Informed (I). | 4.3 \| Področje uporabe in obseg sistema vodenja \| O (Direktor), S (Skrbnik), S (QA) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 4.4 'Management system and its processes', the Director is Responsible (O). The System Administrator, QA Engineer, Head of Commercial, Head of Design, Head of Engineering Project, and Head of Administration Cooperate (S). Executors are Informed (I). | 4.4 \| Sistem vodenja in njegovi procesi \| O (Direktor), S (Ostali vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 5 'Leadership', the Director is Responsible (O). | 5 \| VODITELJSTVO \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 5.1 'Leadership and commitment', the Director is Responsible (O). Most other heads Cooperate (S). Executors are Informed (I). | 5.1 \| Voditeljstvo in zavezanost \| O (Direktor), S (Vodje), I (Izvajalci) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 5.2 'Policy', the Director is Responsible (O). The System Administrator, QA Engineer, and other heads Cooperate (S). Executors are Informed (I). | 5.2 \| Politika \| O (Direktor), S (Vodje), I (Izvajalci) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 5.3 'Organizational roles, responsibilities and authorities', the Director is Responsible (O). All other heads Cooperate (S). Executors are Informed (I). | 5.3 \| Organizacijske vloge, odgovornosti in pooblastila \| O (Direktor), S (Vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 5.4 'Consultation and participation of workers', the Director is Responsible (O). All other roles Cooperate (S). | 5.4 \| Posvetovanje z zaposlenimi in njihovo sodelovanje \| O (Direktor), S (Vsi) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 6 'Planning', the Director is Responsible (O). | 6 \| PLANIRANJE \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 6.1 'Actions to address risks and opportunities', the Director is Responsible (O). All other heads are also marked Responsible (O). Executors are Informed (I). | 6.1 \| Ukrepi za obravnavanje tveganj in priložnosti \| O (Direktor), O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 6.1.1 'General (Planning)', the Director, System Administrator, and QA Engineer are Responsible (O). Other heads Cooperate (S). Executors are Informed (I). | 6.1.1 \| Splošno \| O (Direktor, Skrbnik, QA) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 6.1.2 'Environmental aspects and hazard identification...', all management roles are Responsible (O). Executors are Informed (I). | 6.1.2 \| Okoljski vidiki in identifikacija nevarnosti... \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 6.1.3 'Compliance obligations', all management roles are Responsible (O). Executors are Informed (I). | 6.1.3 \| Obveznosti glede skladnosti \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 6.1.4 'Planning of action', all management roles are Responsible (O). Executors are Informed (I). | 6.1.4 \| Planiranje ukrepov \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 6.2 'Quality objectives and planning', the Director is Responsible (O). All other roles Cooperate (S). | 6.2 \| Cilji in planiranje za njihovo doseganje \| O (Direktor), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 6.3 'Planning of changes', all management roles are Responsible (O). Executors are Informed (I). | 6.3 \| Planiranje sprememb \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 7 'Support', the Director is Responsible (O). | 7 \| PODPORA \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 7.1 'Resources', the Director is Responsible (O). All other roles Cooperate (S) or are Informed (I). | 7.1 \| Viri \| O (Direktor), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 7.1.1 'General (Resources)', the Director is Responsible (O). All other roles Cooperate (S) or are Informed (I). | 7.1.1 \| Splošno \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 7.1.2 'People', the Director is Responsible (O). All other roles Cooperate (S) or are Informed (I). | 7.1.2 \| Ljudje \| O (Direktor), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 7.1.3 'Infrastructure', the Head of Design is Responsible (O) and Executors Cooperate (S). Others are Informed (I). | 7.1.3 \| Infrastruktura \| O (Vodja projektiranja), S (Izvajalci) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 7.1.4 'Environment for the operation of processes', the Director is Responsible (O). Other roles Cooperate (S). Executors are Informed (I). | 7.1.4 \| Okolje za delovanje procesov \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_XII | role_responsibility | For Clause 7.1.5 'Monitoring and measuring resources', the QA Engineer and Head of Engineering Project are Responsible (O). The Director and System Administrator Cooperate (S). Head of Design is also Responsible (O). | 7.1.5 \| Viri nadzorovanja in merjenja \| O (QA Inženir), O (Vodja Inženiring projekta), S (Direktor, Skrbnik) |  | PPS_04_Priloga_Matrika_Odgovornosti | Control of Measuring and Test Equipment |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 7.1.6 'Organizational knowledge', all management roles are Responsible (O). Executors are Informed (I). | 7.1.6 \| Organizacijsko znanje \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 7.2 'Competence', all management roles are Responsible (O). Executors are Informed (I). | 7.2 \| Kompetentnost \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 7.3 'Awareness', all management roles are Responsible (O). Executors are Informed (I). | 7.3 \| Ozaveščenost \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 7.4 'Communication', all management roles are Responsible (O). Executors are Informed (I). | 7.4 \| Komuniciranje \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_VI | role_responsibility | For Clause 7.5 'Documented information', all management roles are Responsible (O). Executors are Informed (I). | 7.5 \| Dokumentirane informacije \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Document Control |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 8 'Operation', the Director is Responsible (O). | 8 \| DELOVANJE \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_V | role_responsibility | For Clause 8.1 'Operational planning and control', the Director is Responsible (O). All other roles Cooperate (S) or are Informed (I). | 8.1 \| Planiranje in obvladovanje delovanja \| O (Direktor), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Instructions, Procedures, and Drawings |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 8.1.1 'Emergency preparedness and response', the Director is Responsible (O). All other roles Cooperate (S). | 8.1.1 \| Pripravljenost in odziv na izredne razmere \| O (Direktor), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_III | role_responsibility | For Clause 8.2 'Requirements for products and services', the QA Engineer, Head of Commercial, and Head of Engineering Project are Responsible (O). Head of Design and Executors Cooperate (S). Director and System Administrator are Informed (I). | 8.2 \| Zahteve za izdelke in storitve \| O (QA, Komerciale, Inženiring), S (Projektiranje, Izvajalci) |  | PPS_04_Priloga_Matrika_Odgovornosti | Design Control |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_III | role_responsibility | For Clause 8.3 'Design and development of products and services', the QA Engineer is Responsible (O) and Head of Design is Responsible (O). Head of Commercial and Head of Engineering Project Cooperate (S). | 8.3 \| Snovanje in razvoj izdelkov in storitev \| O (QA), O (Vodja projektiranja), S (Komerciale, Inženiring) |  | PPS_04_Priloga_Matrika_Odgovornosti | Design Control |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_VII | role_responsibility | For Clause 8.4 'Control of externally provided processes, products and services', the QA Engineer and Head of Commercial are Responsible (O). Others Cooperate (S). | 8.4 \| Obvladovanje procesov, izdelkov in storitev zunanjih ponudnikov \| O (QA, Komerciale) |  | PPS_04_Priloga_Matrika_Odgovornosti | Control of Purchased Material, Equipment, and Services |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_V | role_responsibility | For Clause 8.5 'Production and service provision', the QA Engineer and Head of Engineering Project are Responsible (O). Head of Commercial, Head of Design, and Executors Cooperate (S). | 8.5 \| Proizvodnja in izvedba storitev \| O (QA, Inženiring), S (Komerciale, Projektiranje, Izvajalci) |  | PPS_04_Priloga_Matrika_Odgovornosti | Instructions, Procedures, and Drawings |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_X | role_responsibility | For Clause 8.6 'Release of products and services', the QA Engineer, Head of Engineering Project, and Head of Design are Responsible (O). Head of Commercial Cooperates (S). | 8.6 \| Sprostitev izdelkov in storitev \| O (QA, Inženiring, Projektiranje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Inspection |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_XV | role_responsibility | For Clause 8.7 'Control of nonconforming outputs', the QA Engineer and Head of Engineering Project are Responsible (O). Head of Commercial, Head of Design, and Executors Cooperate (S). | 8.7 \| Obvladovanje neskladnih izhodov \| O (QA, Inženiring), S (Ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Nonconforming Materials, Parts, or Components |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 9 'Performance Evaluation', the Director is Responsible (O). | 9 \| VREDNOTENJE IZVEDBE \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_X | role_responsibility | For Clause 9.1 'Monitoring, measurement, analysis and evaluation', the Director is Responsible (O). All other roles Cooperate (S). | 9.1 \| Nadzorovanje, merjenje, analiziranje in vrednotenje \| O (Direktor), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Inspection |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_X | role_responsibility | For Clause 9.1.1 'General (Monitoring)', the Director is Responsible (O). All other roles Cooperate (S). | 9.1.1 \| Splošno \| O (Direktor), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Inspection |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 9.1.2 'Customer satisfaction', the Director, System Administrator, QA Engineer, Head of Design, Head of Engineering Project, and Head of Administration Cooperate (S). Head of Commercial is Responsible (O). | 9.1.2 \| Zadovoljstvo odjemalcev \| S (Direktor, Skrbnik, QA, Projekt, Inž, Admin), O (Vodja komerciale) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_XVI | role_responsibility | For Clause 9.1.3 'Analysis and evaluation', all management roles are Responsible (O). Executors are Informed (I). | 9.1.3 \| Analiziranje in vrednotenje \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Corrective Action |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_XVIII | role_responsibility | For Clause 9.2 'Internal audit', the System Administrator is Responsible (O). All other roles (Director, QA, Heads, Executors) Cooperate (S). | 9.2 \| Notranja presoja \| O (Skrbnik), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Audits |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_II | role_responsibility | For Clause 9.3 'Management review', the Director is Responsible (O). All other roles Cooperate (S). | 9.3 \| Vodstveni pregled \| O (Direktor), S (Vsi ostali) |  | PPS_04_Priloga_Matrika_Odgovornosti | Quality Assurance Program |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_I | role_responsibility | For Clause 10 'Improvement', the Director is Responsible (O). | 10 \| IZBOLJŠEVANJE \| O (Direktor) |  | PPS_04_Priloga_Matrika_Odgovornosti | Organization |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_XVI | role_responsibility | For Clause 10.1 'General (Improvement)', all management roles are Responsible (O). Executors are Informed (I). | 10.1 \| Splošno \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Corrective Action |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_XVI | role_responsibility | For Clause 10.2 'Nonconformity, incidents and corrective action', all management roles are Responsible (O). Executors are Informed (I). | 10.2 \| Neskladnosti, incidenti in korektivni ukrepi \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Corrective Action |
| Priloga PPS 04 - Matrika odgovornosti R06.docx | APP_B_XVI | role_responsibility | For Clause 10.3 'Continual improvement', all management roles are Responsible (O). Executors are Informed (I). | 10.3 \| Nenehno izboljševanje \| O (Vsi vodje) |  | PPS_04_Priloga_Matrika_Odgovornosti | Corrective Action |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_I | role_responsibility | Appointment of Mr. Jože Žunkovič as the Management System Custodian (Skrbnik sistema vodenja) for Quality, Environment, and Health & Safety, effective June 20, 2017. | Z dnem 20.06.2017 se g. Jože Žunkovič pooblašča za izvajanje funkcije skrbnika sistema vodenja za področje sistema vodenja kakovosti, sistema ravnanja z okoljem ter sistema vodenja varnosti in zdravja pri delu |  | pooblastilo_skrbnik_2017 | Organization |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_I | role_responsibility | The Management System Custodian has superiority over company processes regarding the management system. | nadrejenost procesom podjetja glede sistema vodenja |  | pooblastilo_skrbnik_2017 | Organization |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_I | role_responsibility | Responsibility to ensure processes required for the management system are established, implemented, and maintained. | zagotavlja vzpostavljenost procesov potrebnih za sistem vodenja ter izvajanje in vzdrževanje procesov |  | pooblastilo_skrbnik_2017 | Organization |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_II | role_responsibility | Responsibility for monitoring standards and regulations in the field of management systems. | spremljanje standardov in regulative s področja sistemov vodenja |  | pooblastilo_skrbnik_2017 | Quality Assurance Program |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_II | role_responsibility | Responsibility for planning and monitoring the implementation of training in quality, environment, and H&S. | planiranje in spremljanje izvajanja usposabljanja s področja kakovosti, okolja in VZD |  | pooblastilo_skrbnik_2017 | Quality Assurance Program |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_I | role_responsibility | Authority and responsibility to detect management system issues and coordinate their resolution. | odkrivanje problematike sistema vodenja ter koordinacijo pri reševanju problematike |  | pooblastilo_skrbnik_2017 | Organization |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_XVIII | role_responsibility | Responsibility for preparing the plan for regular and extraordinary internal audits of the management system. | pripravo plana rednih in izrednih notranjih presoj sistema vodenja |  | pooblastilo_skrbnik_2017 | Audits |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_I | role_responsibility | Responsibility to report to company leadership on the operation of the management system and improvement needs. | poročanje vodstvu podjetja o delovanju sistema vodenja in o potrebah po izboljševanju |  | pooblastilo_skrbnik_2017 | Organization |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_VI | role_responsibility | Responsibility for organizing periodic reviews or executing revisions of system documentation. | organiziranje periodičnih pregledov oziroma organiziranje izvedbe revizij sistemske dokumentacije |  | pooblastilo_skrbnik_2017 | Document Control |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_VI | role_responsibility | Responsibility for the controlled distribution of system documentation. | kontrolirano razdeljevanje sistemske dokumentacije |  | pooblastilo_skrbnik_2017 | Document Control |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_IV | role_responsibility | Authorization for internal ordering of goods and services necessary for the smooth operation of the management system. | Kot skrbnik sistema vodenja se zaposleni pooblasti tudi za notranje naročanje blaga in storitev potrebnega za nemoteno delovanje sistema vodenja. |  | pooblastilo_skrbnik_2017 | Procurement Document Control |
| Pooblastilo_Skrbnik_Sistema_Vodenja.pdf | APP_B_I | role_responsibility | The Management System Custodian is a member of company leadership regarding management system matters. Conflicts are resolved by the Director. | Skrbnik sistema je član vodstva podjetja v zadevah sistema vodenja. |  | pooblastilo_skrbnik_2017 | Organization |

"""
