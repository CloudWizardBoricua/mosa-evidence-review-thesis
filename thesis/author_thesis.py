import json
import re
from pathlib import Path

BASE = Path(__file__).parent

def paragraphs(text):
    return [re.sub(r'\s+', ' ', p.strip()) for p in text.strip().split('\n\n') if p.strip()]

def section(title, text, **extra):
    return {'title': title, 'paragraphs': paragraphs(text), **extra}

def chapter(number, title, sections):
    return {'number': number, 'title': title, 'sections': sections}

content = {
    'schema_version': 1,
    'metadata': {
        'title': 'A CONFORMANCE HARNESS FOR VERIFIABLE MODULAR OPEN SYSTEMS OUTCOMES IN DEFENSE ACQUISITION: DESIGN, IMPLEMENTATION, AND CONTROLLED EVALUATION',
        'author': 'Daren Jadiel Diaz',
        'university': 'University of Oklahoma',
        'graduate_college': 'Graduate College',
        'college': 'Gallogly College of Engineering and the Polytechnic Institute',
        'degree': 'Master of Science',
        'city': 'Tulsa, Oklahoma',
        'year': 2026,
        'committee': ['Dr. John Hassell, Chair', 'Dr. Christopher Freeze'],
        'copyright': 'Copyright by Daren Jadiel Diaz 2026. All Rights Reserved.',
        'revision_label': 'Condensed revision with agent supported evidence review',
        'approval_status': 'Revised research draft. Author review and committee approval of this revision are pending.',
        'source_preservation': 'The confirmed completed thesis remains unchanged.',
    },
    'front': {
        'abstract': paragraphs('''
        A Modular Open Systems Approach, or MOSA, aims to make systems easier to inspect, replace, and upgrade through clearly defined connections. An acquisition team still needs evidence that a proposed software component follows the declared design. This thesis develops a conformance harness, a set of repeatable checks that compares supplied evidence with explicit requirements. The revised study asks when an agent helps a person review MOSA evidence and what checks keep its recommendations reliable.

        The work connects an earlier conformance experiment with a bounded agent prototype developed for an Agentic Systems capstone. The prototype examines a module description, interface contract, software component inventory, test record, and evidence history. Three controllers share the same validators and decision guard: a fixed workflow, a rule based adaptive workflow, and a model agent. The agent may choose checks and draft a recommendation. It may not alter the evidence or approve its own review. A person retains the approval decision.

        The original experiment used 20 synthetic modules and showed that stronger executable checks detected all 18 seeded faults, compared with five detected by the minimal baseline. A separate capstone pilot used 20 development cases. The model matched 17 raw disposition labels; deterministic guard checks increased the match to 20. The pilot reported fewer validator selections but much longer elapsed time than the fixed workflow. These observations motivate an adaptive rule comparison and do not establish an operational advantage for artificial intelligence.

        A new benchmark contains 40 neutral cases divided into development and additional evaluation sets. It distinguishes supported readiness, known problems, and incomplete evidence. An offline preflight exposed one structural citation issue before hosted evaluation, and the final protocol records the resulting amendment. {{study.abstract}} The contribution is an inspectable review method and a reproducible comparison of controller behavior. Claims remain limited to the synthetic evidence profile, and independent label review remains pending.
        '''),
        'keywords': ['Modular Open Systems Approach', 'MOSA', 'conformance testing', 'agent supported review', 'evidence provenance', 'human approval', 'reproducibility'],
        'reader_guide': paragraphs('''
        Start with the problem in Chapter 1, then follow the example of a sensor software replacement through Chapter 3. A reader does not need to program to understand the review. The controller decides what to inspect. Validators perform explicit checks. The decision guard checks whether the resulting recommendation follows those observations. A person decides whether to record approval.

        Five colors provide navigation. Blue identifies evidence and fixed checks. Purple identifies model choices. Green means the required profile checks support readiness. Amber means information or review is still needed. Crimson marks a known blocking problem. Every color also has a text label, so the meaning remains clear in a printed copy or for a reader who cannot distinguish the colors.

        Technical terms are explained near their first important use. The glossary adds an example and explains why the term matters. Chapter 4 explains the evaluation, and Chapter 5 keeps the original experiment, capstone pilot, and new benchmark separate. The public companion website provides saved walkthroughs, diagrams, data tables, and reproduction instructions. It presents research evidence; the live model and its credentials remain in a private development environment.
        '''),
        'research_status': 'This revision is a research draft. It preserves the original title and does not assert committee approval. Missing empirical results must remain visibly identified until a recorded evaluation supplies them.',
    },
    'chapters': [],
}

content['chapters'].append(chapter(1, 'Problem and research questions', [
    section('Why replaceable software needs evidence', '''
    Defense software often remains in service while sensors, processors, suppliers, and threats change. A team may need to replace one component without rebuilding the whole system. The challenge is practical: the replacement must send the right information, use the expected connections, and supply enough evidence for another organization to inspect its behavior. A claim that a component is modular does not answer those questions by itself.

    Consider a sensor that sends an observation to a processing service. The message includes an event identifier, a measured value, and its unit. The processor returns an alert. A supplier offers a replacement processor with the same advertised connection. If the replacement interprets a distance in feet when the sensor provides meters, the connection may work while the result is wrong. If its component inventory omits a required library, another supplier may struggle to reproduce or maintain it. These are evidence questions with consequences for replacement and review.

    The Modular Open Systems Approach, abbreviated MOSA, addresses change through an integrated business and technical strategy. In plain language, it means designing systems so parts can be separated and connected through defined interfaces. An interface is the shared boundary where parts exchange information or services. The legal definition includes verification of relevant interfaces, so evidence review belongs within the approach rather than after it (10 U.S.C. § 4401, 2026).

    This study focuses on software evidence that a small prototype can inspect. It does not infer a weapon system's readiness from a few files. Its narrower aim is to make the route from a declared requirement to a review recommendation visible and repeatable. That route gives a reader a way to ask what was checked, what was missed, and who remains responsible for the decision.
    '''),
    section('The gap between a claim and a supported recommendation', '''
    Public oversight gives a reason to study this gap. The U.S. Government Accountability Office, or GAO, examined 20 acquisition programs in its 2025 MOSA report. It identified weaknesses in planning, coordination, and assessment of benefits. The report also described inconsistent plans for verifying implementation at important acquisition points. These findings motivate clearer evidence practices. They do not measure this prototype or establish that an agent is the solution (GAO, 2025).

    A review can go wrong in several ways. A required file may be absent. Two supplied files may disagree. A tool may fail before it checks an artifact. A reviewer may receive a confident recommendation that does not follow the recorded observations. Each situation needs a different explanation. Missing information should lead to a request for evidence. A demonstrated inconsistency should lead to a correction. A tool failure should remain visible so another reviewer can complete the inspection.

    A language model can summarize material and choose among permitted tools. That capability creates a possible role in organizing a review, but it creates another point where a recommendation can depart from evidence. The capstone therefore separates the model's proposed decision from the final supported disposition. A disposition is the recorded outcome of the technical review. Human approval is a separate action that acknowledges the review record and does not change a failed check into a passing one.
    '''),
    section('Research questions and success criteria', '''
    The central research question is: When does an agent help a person review MOSA evidence, and what checks are needed to keep its recommendations reliable? Three supporting questions make that question testable. First, do the controllers reach the expected disposition for the same unique cases? Second, how often does the decision guard correct or block a controller's draft? Third, does adaptive selection reduce validation effort enough to justify its time, cost, and added complexity?

    Success means producing a review that another person can inspect and reproduce. The review must identify its evidence, distinguish known problems from unknowns, cite locations that support its findings, and preserve the person's approval role. The evaluation must compare the model with both a fixed workflow and an adaptive rule workflow. A useful result may show that explicit rules produce the same supported decisions at lower cost. The study does not require the agent to win a comparison.

    The prototype will be assessed through recorded behavior rather than persuasive prose. A correct disposition is necessary, but a finding also needs a supported location and an understandable remedy. A lower tool count is useful only when required coverage remains intact. A completed run must keep failures and uncertainty visible. These criteria connect the research question to the actual review record and prevent a single headline percentage from hiding important differences.
    '''),
    section('Scope and contribution', '''
    The work uses constructed software evidence packages, not classified data or operational weapon systems. It tests a declared course profile with a small set of permitted validators. The profile is an explicit list of checks and input expectations. Passing it means those checks support readiness for this exercise. It does not certify compliance with every MOSA requirement, complete OpenAPI or CycloneDX standards, cybersecurity requirements, safety requirements, or contractual obligations.

    The contribution has three parts. The harness turns selected requirements into repeatable observations. The agent extension preserves those checks while comparing different ways of selecting them. The public repository links the explanation to code, tests, diagrams, and saved results. Together, these artifacts let a committee member move from a plain language claim to the evidence behind it. The revision keeps the original conformance study as a foundation while concentrating the main argument on the capstone's review design and its evaluation.
    '''),
]))

content['chapters'].append(chapter(2, 'MOSA and evidence review foundations', [
    section('Modularity and the boundary of change', '''
    A module is a component that can be described and changed as a distinct part of a system. Good boundaries reduce the amount of surrounding work needed when a design decision changes. Parnas's information hiding principle places likely changes behind a stable boundary, so other components do not need to depend on internal details (Parnas, 1972). Applied here, a sensor client should rely on the processor's published messages rather than on the processor's private source structure.

    A visible connection alone is not enough. A shared message needs defined fields, units, allowed values, and expected behavior. Two suppliers can agree on a field name but disagree on its meaning. A contract that says value is a number still leaves a question about whether it represents meters, feet, seconds, or a count. The conformance harness therefore treats both structure and meaning as evidence concerns. The original prototype tested behavior as well as document presence.

    Modularity also has a business side. A replacement may be technically possible but practically difficult if the customer lacks needed interface information, test access, or rights to use relevant data. The 2025 Department of Defense implementation guide connects MOSA planning with design, interfaces, verification, and acquisition considerations (Department of Defense, 2025). The present prototype addresses a selected technical evidence slice. It does not resolve licensing negotiations, intellectual property rights, or the availability of competing suppliers.

    Replaceability should therefore be described as a claim with conditions. A processor may be replaceable under a named interface version, a given message format, and a declared dependency set. The evidence should say which conditions were inspected. If the mission, message, or environment changes, the earlier review may no longer apply. This conditional statement is more useful than a broad declaration that a component is open.
    '''),
    section('A source hierarchy for defensible claims', '''
    Different sources answer different questions. Statute establishes requirements within its stated scope. Department guidance explains implementation expectations. Oversight reports describe observed gaps. Standards describe technical formats or procedures. Research papers supply theories and tested methods. Project files show what this prototype actually did. Keeping these roles separate prevents a strong source in one area from supporting a claim it did not examine.

    The source hierarchy in this thesis gives legal and official engineering material priority for MOSA context. It gives executable artifacts and saved run records priority for prototype results. Academic work supports the research method and agent design. Industry examples can help explain an implementation pattern, but they are not treated as authority for defense compliance. A diagram is an explanation of the design, while a run trace is evidence that a particular implementation followed that design on a particular input.

    Three levels of claim are kept explicit. A documented claim reports what a file or publication says. A verified observation reports what a check established under a named condition. An inferred implication explains what the observation may mean. For example, a matching interface version is a verified consistency observation. Easier supplier replacement is a possible implication that requires additional evidence. Reduced lifecycle cost is a broader outcome that this study does not measure.

    This separation matters when discussing artificial intelligence, abbreviated AI. An agent may explain a finding well without discovering a new issue. A guarded output may be correct because deterministic code repaired it. A reader should be able to identify which part of the system produced each result. The evaluation therefore records the original draft, tool observations, guard action, and final supported disposition separately.
    '''),
    section('What a conformance harness checks', '''
    Conformance means satisfying a stated requirement under a stated test. A harness is the surrounding code that prepares inputs, runs checks, and records results. Together, a conformance harness gives a review a repeatable procedure. The National Institute of Standards and Technology, or NIST, provides published conformance testing frameworks that connect requirements with test assertions and observable results (NIST, 2012). The thesis applies that general idea to a small MOSA evidence profile.

    The original harness inspected module descriptions, interface contracts, evidence history, dependencies, declared software components, behavior, determinism, and latency. Determinism means the same input produces the same relevant output under the same conditions. Latency means the elapsed time before a response is available. The experiment used modules with known faults to test whether the harness could observe those faults. Its evidence is retained as a separate foundation for this revision.

    The capstone narrows that broad harness into three callable validators. A validator is a tool that checks explicit conditions and returns findings. The first inspects package completeness, identity, hashes, and test records. The second compares interface declarations. The third compares declared dependencies with the software component inventory and a dated advisory fixture. This smaller scope makes controller behavior easier to compare without claiming full system assurance.

    A check has value when its consequence is clear. If two interface versions disagree, the review should identify both declarations and ask for alignment. If the required inventory is missing, the review should ask for the inventory and preserve uncertainty. The same green outcome should never stand for both checked agreement and unchecked absence. The three disposition categories in Chapter 3 give those situations distinct names.
    '''),
    section('Evidence identity and traceability', '''
    Evidence is useful only when a reader can connect it to the reviewed component. A manifest is a short module description that identifies the build, interface version, endpoints, and dependencies. A build is a particular produced version of the software. The test record should identify that build rather than an earlier one. A passing test record for a different build does not establish the current build's behavior.

    Provenance means the recorded origin and history of an artifact. In this prototype it includes declared source information and hashes for selected files. A hash is a compact fingerprint calculated from a file's bytes. Changing the file normally changes that fingerprint. The prototype uses the Secure Hash Algorithm with a 256 bit output, written SHA 256, to bind a review to particular input files (NIST, 2015). Matching hashes support identity; they do not prove that the supplier is truthful or that the software is safe.

    Traceability means a reader can follow a finding back to the evidence that supports it. A useful finding cites a file and a field location, explains the observed condition, and names a remedy. A reference to interface.json /info/version tells the reviewer where the declared interface version appears. A missing file needs a different citation: the inspected package inventory and the profile's requirement. The evaluator must recognize that absence cannot be proved by resolving a field that does not exist.

    Traceability also extends forward. A later decision should record which draft was reviewed and whether the input fingerprint still matches. If a supplier updates the component inventory after review, the person should request a new review. The previous trace remains useful as history, but it no longer describes the current evidence. This approach protects the meaning of approval without pretending the local file store is an authenticated production audit service.
    '''),
    section('Why consider an agent and why compare it with rules', '''
    An agent in this thesis is a language model that observes tool results, chooses a permitted next check, and drafts a review. A language model predicts and generates text from input context. The ReAct research demonstrated a way to interleave model reasoning with actions that gather information (Yao et al., 2023). Toolformer explored models that select and use external tools (Schick et al., 2023). These studies motivate tool mediated designs. They do not establish accuracy for this MOSA profile.

    The possible benefit is selective effort. If the package is incomplete, further interface comparison may not answer the immediate question. If two interface versions disagree, checking that boundary early may help the reviewer understand a blocking issue sooner. A model might also express the result in understandable language. These benefits must be measured against added remote calls, variability, and the risk of unsupported decisions.

    A rule based adaptive controller provides an essential comparison. It can inspect completeness first, follow explicit priority hints, and stop at an allowed point without invoking a language model. If the permitted decisions are simple and stable, rules may provide the same value more directly. The comparison asks what model selection adds beyond adaptive control itself. Without it, fewer checks could be attributed to intelligence when an explicit stopping rule would have achieved the same result.

    Reliability has several dimensions. Correctness on one run does not show consistency across runs or useful behavior after a tool fails. Rabanser and colleagues (2026) propose assessing consistency, robustness, predictability, and safety separately when evaluating agents. This study uses that distinction to report repeated behavior, controlled failure cases, guard interventions, and cost limits alongside disposition accuracy. It does not claim to implement their entire evaluation framework.
    '''),
]))

content['chapters'].append(chapter(3, 'Agent design and human review', [
    section('A small review system with clear responsibilities', '''
    The system separates evidence, controller, validators, decision guard, and person. Evidence enters as a read only package. The controller chooses how to inspect it. Validators return observations using named finding codes. The guard checks whether the proposed disposition follows those observations and whether the required coverage is present. The person reviews the saved report and records an approval, rejection, or request for revision.

    These roles make the design easier to inspect. A model cannot hide a failed interface check by writing a reassuring summary. A validator cannot grant approval. A person cannot turn a blocking inconsistency into technical readiness by clicking approve. Recording a decision means acknowledging the review record, including its disposition and uncertainty. The distinction keeps both technical observations and human accountability visible.

    The live application runs in the existing course Codespace, a development environment hosted for the class repository. Its web server presents review controls and saved records. A separate public GitHub Pages site presents static explanations and approved research exports. Static means the site delivers stored content without running the agent. A public reader can inspect a saved example without receiving access to model credentials or the private review state.

    The system topology uses blue for evidence and deterministic checks, purple for model choices, green for supported readiness, amber for incomplete review, and crimson for blocking problems. These colors are aids to navigation rather than measures of certainty. The diagram labels every role and outcome in words. A reader can follow the same flow in print even if all colors appear as gray.
    ''', figure={'id': 'system-topology', 'caption': 'System topology showing evidence, controllers, validators, the decision guard, and the human review boundary.', 'alt': 'A package enters a controller. The controller calls fixed validators. A deterministic guard checks the recommendation. A person records approval separately.'}),
    section('The evidence package and its limits', '''
    Each package has five required JavaScript Object Notation files, abbreviated JSON. JSON is a structured text format that represents fields, lists, numbers, and objects in a form a computer can read (Bray, 2017). The manifest describes the module. The interface file describes its declared connections. The software bill of materials lists its components. The test file records selected outcomes. The provenance file records evidence origin and selected file fingerprints.

    A software bill of materials, abbreviated SBOM, is an ingredient list for software. It helps a reviewer see which libraries and versions a component declares. The National Telecommunications and Information Administration, or NTIA, published an earlier baseline for such records (NTIA, 2021). The prototype uses selected CycloneDX fields for a defined course exercise. CycloneDX is a published format for software and other bills of materials (OWASP Foundation, 2025). Passing these selected comparisons does not establish complete CycloneDX compliance.

    The interface file uses selected OpenAPI fields. API means application programming interface, the software connection used to request data or a service. OpenAPI describes those connections in a format that people and tools can inspect (OpenAPI Initiative, 2021). The profile compares the declared version, endpoint presence, response types, and dependency declarations. An endpoint is the named route a client calls, such as a route that accepts a sensor event. The prototype does not execute the service, prove every response behavior, or validate every rule in the OpenAPI specification.

    Input limits keep the exercise bounded. Artifacts must be JSON objects within the declared size limit. The package reader rejects paths that escape the package directory and rejects symbolic links, which are pointers to other filesystem locations. These checks reduce ambiguity about what was reviewed. They are specific controls with tests, not a claim that all possible hostile inputs have been ruled out. The public fixtures contain constructed evidence and no operational defense information.
    '''),
    section('Three validators shared by every controller', '''
    The package inspection tool first records which required files are available. It checks selected required fields, whether test evidence identifies the current build, and whether recorded hashes agree with current bytes. Missing evidence is marked unknown. A recorded hash that disagrees with the present file is a known inconsistency. This difference is central to a defensible disposition: the reviewer should not confuse a lack of proof with proof of a particular fault.

    The interface validator compares the manifest and interface contract. It checks whether their versions agree, declared endpoints exist, selected response types match expectations, and declared dependencies remain consistent. The result names the finding, file, and relevant field. For an interface version mismatch, the remedy is to reconcile the declarations and rerun the checks. The prototype does not infer that either declaration is the correct one; that decision belongs to the supplier and reviewer.

    The SBOM validator compares required dependencies against listed components and checks selected license information. It also compares declared component identities with a fixed synthetic advisory. An advisory is a notice about a known software issue. This fixture intentionally invents one advisory so the test can be repeated without relying on changing online data. It is not a real vulnerability notice. An optional live advisory lookup is outside the reported frozen benchmark unless a separate run explicitly records that setting.

    All controllers use the same tool implementations. That choice prevents a comparison from quietly giving one controller stronger inspection capabilities. Tool selection can differ, but the observations returned by a given validator on unchanged input remain the basis for the recommendation. Each invocation records the tool name, returned findings, relevant input identity, and elapsed time. Repeated calls count as repeated work even when the name is the same.
    ''', table={'id': 'validator-scope', 'caption': 'The three validators and the limits of their evidence.', 'columns': ['Validator', 'Question answered', 'Important limit'], 'rows': [['Package inspection', 'Are required records available and consistent with their declared identity?', 'Hashes support file identity, not supplier trust.'], ['Interface comparison', 'Do selected interface declarations agree?', 'Selected fields only, not full service behavior.'], ['SBOM comparison', 'Are declared components present and is the synthetic advisory matched?', 'Not a complete vulnerability or license assessment.']]}),
    section('Fixed and adaptive rule workflows', '''
    The fixed workflow runs the package inspection, interface comparison, and SBOM comparison in a declared order. Its strength is predictable coverage. It does not need a remote model or pricing information. Its weakness is that it may run checks that cannot change an already incomplete review. For this small profile, that extra work may still be inexpensive enough to justify the simpler procedure.

    The adaptive rule workflow starts with package inspection. If the profile's halt condition shows that necessary evidence is missing or unusable, it records the missing requirement and returns a request for review. Otherwise, it uses an explicit priority hint to choose whether the interface or SBOM check runs next, then performs the remaining required comparison. A known failure does not excuse skipping unrelated required coverage when the evidence remains available.

    The rules define which stopping points are legitimate. Early stopping is useful only when the reason is visible and the outcome preserves uncertainty. A failure in one validator may be relevant to one part of the package while other available evidence still needs inspection. The guard therefore checks the recorded halt reason and coverage rather than accepting every short trace as efficient. A short but unsupported review counts as an incomplete review.

    The adaptive controller uses no expected case labels and no knowledge of benchmark identifiers. It sees the same evidence and validator outputs as the other controllers. Its behavior is frozen before the separate evaluation set is run. This makes it a direct comparison for the model's selection behavior, while keeping the evidence profile and final decision rules common across all approaches.
    '''),
    section('The bounded model loop', '''
    The model agent receives the profile instructions, neutral package identifier, and allowed tool descriptions. It can request a validator, read the result, and choose another permitted step. The loop limits the number of model turns, remote retries, and output tokens. A token is a unit of text used by the provider to count input and output. The model identity and settings are stored with the run so later readers can see what produced the draft.

    The agent's final draft contains a proposed disposition, the exact finding identifiers returned by tools, an explanation, and remaining uncertainties. The allowed outcomes are ready, not_ready, and needs_review. The first means required checks support readiness within the profile. The second means observed evidence contains a blocking problem. The third means the review lacks enough supported information for a complete conclusion. The report displays plain language labels beside these stored values.

    Evidence text is treated as data. A file cannot grant the model new permission, remove a required check, or tell it to approve the package. The permitted tools expose inspection actions only. Approval, source editing, and public communication are unavailable to the model. This narrow action set limits what an erroneous model instruction can do in the prototype. A prompt instruction alone is not treated as proof of safety; enforcement also occurs in the allowed tool dispatcher and guard.

    A provider timeout, malformed response, unavailable model, or exhausted allowance leaves an inspectable failed or incomplete run. The application does not silently relabel a fixed workflow as a successful model run. Completed observations remain saved, and the report tells the person what remains unknown. This behavior matters because a comparison that removes failed model attempts would make the model appear more reliable than the complete record supports.
    ''', figure={'id': 'review-sequence', 'caption': 'A bounded review sequence from inspection to draft and guard decision.', 'alt': 'The controller inspects evidence, selects permitted tools, drafts a recommendation, and receives a deterministic coverage and disposition check.'}),
    section('The decision guard and three possible dispositions', '''
    The decision guard is ordinary deterministic code. Deterministic means its declared inputs and rules produce the same result under the same conditions. It does not ask a second model to vote on the first model's answer. It checks whether findings use known identifiers, whether necessary validations or a justified halt occurred, and whether the proposed disposition follows the collected evidence. Unsupported or malformed drafts remain incomplete.

    The guard derives the supported outcome from recorded observations. Incomplete coverage, an invalid draft, or changed source evidence requires further review. When those conditions are absent, a known blocker takes precedence over an unknown finding. If no blocker exists but evidence remains unknown, the result asks for review. Required coverage with no blocker or unknown finding supports readiness within the profile. The report preserves every finding even when one severity determines the disposition.

    A guard intervention is recorded whenever the guard changes a proposed disposition or blocks completion. These interventions are part of the result, not cleanup to be erased. A correct guarded output can coexist with an incorrect raw recommendation. Separating them lets the reader see whether reliability came from the controller, the guard, or both. It also shows whether the agent repeatedly depends on repair in the same class of case.

    A guard can enforce only rules represented in its implementation. If the profile never checks units, a matching version and component list cannot establish correct units. If a validator reports the wrong observation, the guard may faithfully follow it. The shared validators and guard make the controller comparison fair, but they also create a common source of error. Independent labels and tests are needed to challenge that shared boundary.
    ''', callout={'color': 'amber', 'title': 'Unknown evidence is a result', 'text': 'A missing test record does not establish that the component failed a test. It establishes that the reviewer lacks required evidence. The report asks for that record and explains what still needs checking.'}),
    section('A report a person can act on', '''
    Every report follows five questions: What was checked? What was found? Why does it matter? What should be corrected? What remains unknown? The first identifies coverage. The second names evidence based findings. The third connects the finding to replacement or maintenance. The fourth gives a practical next action. The fifth prevents the explanation from sounding more complete than the trace.

    For example, a report may state that the manifest declares interface version 1.0 while the contract declares 2.0. It explains that a replacement supplier cannot rely on both declarations as the same contract. It asks the owner to select the intended version, update the related files, regenerate evidence history, and rerun review. It does not claim the component will fail in every environment or choose the correct version without additional authority.

    A citation is checked at the file and field level. JSON Pointer is a standard way to address a location inside a JSON document (Bryan et al., 2013). The pointer /info/version refers to the version field within info. The evaluator resolves such pointers for existing evidence and uses explicit inventory references for absence. It separately records whether a citation exists and whether it supports the named finding. A plausible looking string alone is insufficient.

    The report retains the raw draft and guard explanation alongside the plain language summary. A committee reader can read the summary first and open technical evidence only when needed. This layered presentation gives readers detail without requiring them to understand every implementation field. It also prevents color or a polished narrative from replacing the underlying inspection record.
    '''),
    section('Human approval source changes and rollback', '''
    Review output starts as a draft. A person supplies a reviewer name and explicitly selects an action. The prototype compares the current package fingerprint with the fingerprint saved at review time. If source evidence has changed, the old draft cannot be used as a current approval record. The person must rerun review or request revision. This check binds an action to the evidence actually inspected.

    Approval updates a separate pointer to the recorded review. A pointer here means a stored reference to a run identifier. Rollback restores the prior approved pointer and adds a history event. It does not edit the input package or erase the newer trace. Keeping both records gives the person a way to inspect what was accepted and what was later withdrawn. The distinction is useful when demonstrating a corrected interface package after an earlier review.

    The local prototype records a supplied reviewer name, not a verified organizational identity. It is not an authenticated acquisition approval system or a tamper resistant audit service. That limit is stated beside the approval demonstration. A production extension would need access control, verified identity, protected storage, and organization specific decision authority. Those are future requirements rather than capabilities inferred from the demonstration.

    NIST's AI Risk Management Framework describes the importance of context, measurement, governance, and risk management for AI systems (NIST, 2023). Its generative AI profile addresses additional risks in systems that generate content (NIST, 2024). This design adopts a narrow practical response: keep model actions bounded, preserve evidence and failures, and assign approval to a person. The study does not present those choices as full implementation of either NIST publication.
    ''', figure={'id': 'approval-rollback', 'caption': 'Human review and rollback preserve source identity and review history.', 'alt': 'A draft may be approved only after a source fingerprint check. A separate approval pointer records the decision. Rollback restores the prior pointer and preserves both review traces.'}),
]))

content['chapters'].append(chapter(4, 'Evaluation method', [
    section('Design science and the unit of analysis', '''
    Design science studies a problem by building and evaluating an artifact. Hevner and colleagues (2004) describe the relation between a practical problem, a designed solution, and evidence from its use. Peffers and colleagues (2007) provide a process that moves through problem identification, objectives, development, demonstration, evaluation, and communication. This thesis follows that approach by tying each design choice to an inspectable implementation and a measured review outcome.

    The artifact is the evidence review harness and its bounded controllers. The unit of analysis is one unique evidence package. A unit of analysis is the thing counted as a distinct observation when answering the research question. Running the same package three times gives information about consistency and elapsed time. It does not create three independent examples of correctness. This distinction prevents repeated execution from inflating the apparent strength of the evidence.

    The study uses a controlled synthetic benchmark because the intended faults and unknowns can be specified before the controllers run. Synthetic means constructed for testing rather than collected from operational programs. Deliberately changing a valid input follows the general testing idea of mutation, which introduces a known change to challenge a test (Jia & Harman, 2011). The method makes errors observable and keeps the data safe for public sharing. Its limitation is representativeness: constructed records reflect the author's selected problem model rather than the full range of acquisition evidence or supplier behavior.

    The three studies in this revision answer different questions. The original experiment asks whether a stronger harness observes more seeded faults than a minimal review. The capstone pilot asks whether a bounded model can select tools and draft a guarded disposition. The new benchmark compares fixed, adaptive rule, and model control under the same profile. Their datasets are never pooled into one accuracy percentage.
    '''),
    section('Constructing a neutral forty case benchmark', '''
    The benchmark contains 40 cases: 10 ready cases, 20 cases with known blocking problems, and 10 cases needing further review. The categories describe expected outcomes under the profile, not universal judgments about the software. Ready cases provide all required evidence and pass selected comparisons. Blocking cases contain observable inconsistencies. Further review cases omit necessary evidence or exercise controlled uncertainty.

    Each package receives a neutral identifier that does not disclose its intended condition. The earlier pilot used descriptive names that could reveal a fault to the model. Neutral identifiers remove that simple hint. Expected dispositions, required findings, and evaluation membership remain in a separate label file. They are available to the evaluator after a run, not to the model prompt or tool descriptions during review.

    The ready group varies permitted evidence details without changing expected conformance. The problem group varies versions, endpoints, types, declarations, evidence identities, and component records. The unknown group includes absent records, malformed or unusable evidence where inspection cannot establish coverage, and an unavailable tool case. A case that contains malformed evidence is classified according to the published profile: a confirmed violation and an inability to complete inspection are not automatically the same condition.

    A benchmark should challenge its own labels. Each case records the specific change from a ready package, the reason for the expected disposition, and the evidence location expected to support that reason. Labels are reviewed against the written profile instead of merely copying the current guard's answer. The author and assisted implementation process are disclosed. Independent review remains pending and is not described as completed simply because automated checks pass.
    '''),
    section('Development and separate evaluation sets', '''
    Twenty cases come from the earlier development fixtures, copied with neutral identifiers. They include three ready, 12 blocking, and five further review cases. Twenty additional cases include seven ready, eight blocking, and five further review cases. The sets therefore have different category proportions. Results show category counts beside overall accuracy so that a reader can assess that difference. The additional cases provide the primary reported comparison, while development results remain separate.

    The initial plan aimed to hold out the additional cases from development. An offline preflight of all 40 cases exposed a structural issue in handling provenance hashes. When the hash container had the wrong shape, the validator produced a root problem and four dependent child references that were not meaningful. The amendment retains the root PROVENANCE_SHAPE blocker and suppresses those invalid dependent references. The original freeze and 240 offline preflight runs are preserved separately. No hosted model runs occurred before that amendment.

    The primary dataset is therefore described as additional evaluation cases, not untouched external holdout evidence. The same research process produced the profile, fixtures, and preflight amendment. This shared origin is a limitation even when model inputs contain no labels. External cases and independent label review would provide a stronger test of generalization. Daren's verification of the labels and independent review remain pending at this revision's preparation.

    The final case files, labels, prompt, model identity, controller settings, and source version are frozen in a manifest before the main evaluation. A manifest is an inventory of inputs and fingerprints. If a later correction is required, it receives a new version and explanation. The final additional set is primary and the development set has its own table. A combined total may show run completeness, but it is not substituted for primary accuracy. This preserves the relation between development, amendment, and measurement.
    ''', figure={'id': 'benchmark-split', 'caption': 'Development and additional evaluation cases have distinct category counts, and the preflight amendment is disclosed.', 'alt': 'Forty cases include ten ready, twenty blocking, and ten uncertain cases. Development has three ready, twelve blocking, and five uncertain cases. Additional evaluation has seven ready, eight blocking, and five uncertain cases. An offline preflight precedes the disclosed final freeze.'}),
    section('Running three approaches with repeatable settings', '''
    Each controller is scheduled to run three times on each unique package. A complete schedule therefore contains 360 runs: 40 cases multiplied by three controllers and three repetitions. Scheduling is distinct from completion. A failed or budget stopped run remains a recorded attempt, with its status and reason, rather than disappearing from the denominator. The published completion table shows what actually ran.

    All controllers use the same frozen validators, evidence files, and decision guard. The model uses the existing OpenRouter configuration, with the actual model value recorded at execution. OpenRouter is the service used to access the hosted model. Remote settings include permitted model turns, retries, response size, and timeout. Any setting changed from the capstone pilot is disclosed before interpreting a comparison across those studies.

    Run order is recorded so that timing patterns can be inspected. Local checks may warm caches, and remote calls may experience changing network conditions. Elapsed time is measured across the complete review, including model waiting and guard work. Tool time is also recorded where available. The study does not attribute all latency differences to model reasoning when transport, provider load, and local processing contribute to the measurement.

    The first scheduled repetition on each unique evaluation case supplies the primary accuracy comparison. All repetitions supply a stability measure and descriptive timing summaries. If the first attempt fails, it remains the primary outcome for that schedule position. A retry performed within the configured request policy remains part of the same run. A new review after a completed failure is separately identified rather than quietly replacing the failure.
    '''),
    section('Measurements that separate correctness from presentation', '''
    Raw disposition match measures whether the controller's proposed outcome equals the case label. Guarded disposition match measures whether the final supported outcome equals that label. The two measures answer different questions. If the guard repairs an incorrect draft, raw match records the error and guarded match records the recovered outcome. A report that publishes only the second would hide reliance on the guard.

    Finding quality is measured by expected and returned finding identifiers. A missed finding is an expected problem absent from the report. An extra finding is a finding beyond the label's predeclared target list. It may be a grounded follow on execution error, so it is not automatically an invented problem. The trace shows whether evidence supports it. Because unknown cases can legitimately stop before later checks, expected findings are defined for the permitted coverage of that case. A controller is not credited with an invented explanation merely because its final disposition happens to match.

    Evidence reference quality checks the cited file and location against the package. Existing fields must resolve to real locations that support the named finding. Missing fields and missing files use explicit absence checks rather than nonexistent pointers. This distinction avoids giving a valid citation failure to a legitimate missing evidence report. The evaluator records citation failures so readers can inspect them case by case.

    Validation effort counts actual invocation events. The previous pilot's summary counted distinct tool names held in a result mapping. If a controller called one tool twice, that summary could undercount the work. The corrected evaluator counts the event list and retains both unique tool coverage and total invocations. Coverage describes which checks occurred. Invocations describe how much work was requested. They are related, but they are not interchangeable measurements.

    Additional measurements include elapsed time, input and output tokens, provider reported cost, guard interventions, and source integrity. Tokens and cost are unavailable for some interactive demonstrations and should remain unavailable rather than being converted to zero. A zero for offline controllers means no hosted model calls occurred. A zero in a missing provider field would mean something different and cannot be treated as evidence of a free model run.
    ''', table={'id': 'metric-definition', 'caption': 'Measurements and the questions they answer.', 'columns': ['Measure', 'Reader question'], 'rows': [['Raw disposition match', 'Did the controller propose the expected outcome?'], ['Guarded disposition match', 'Did the complete review support the expected outcome?'], ['Missed and extra findings', 'Was the explanation complete and supported?'], ['Evidence references', 'Can a reader locate the basis for the finding?'], ['Actual tool invocations', 'How much validation work was requested?'], ['Elapsed time and provider cost', 'What did the review require in time and paid usage?'], ['Guard interventions', 'How often did fixed rules repair or block a draft?']]}),
    section('A five dollar ceiling with recorded stopping', '''
    The new hosted evaluation has a total spending ceiling of five U.S. dollars. The cost ledger records planned reservations, completed provider usage, and unresolved charges. Before a request, the runner estimates a conservative maximum charge from the known input size, response limit, and reliable provider prices. It reserves that allowance before sending the request. A request is refused if the reservation would exceed the remaining ceiling.

    A reservation protects the ceiling only when it bounds the billable work. Any billable internal or additional usage permitted by the provider must be accounted for, or the runner must stop because it cannot establish a reliable bound. After a response, actual usage reconciles the reservation. A timeout with unresolved billing does not immediately release the full reservation. The ledger preserves uncertainty rather than assuming the request was free.

    This limit is part of the experimental constraint, not evidence that the model is economical in general. The earlier pilot's low observed charge cannot guarantee that a larger study will cost the same amount. Provider pricing or behavior may change. If reliable price information cannot be obtained, the study records the hosted comparison as incomplete and still preserves the offline results. Incomplete evidence is a legitimate study outcome, provided it is explained accurately.

    Cost comparisons separate dollars from time. A remotely hosted model can be inexpensive in billed tokens while taking much longer than local checks. A fixed or adaptive controller can incur no provider charge while still requiring local computing and human review. The study reports the measured provider charge and elapsed time directly and does not claim a complete organizational cost model.
    '''),
    section('Analysis and limits of inference', '''
    Accuracy is reported as a numerator and denominator for unique cases, with category results beside the overall result. A result states how many of the seven ready additional cases received a ready recommendation, how many of the eight blocking cases were correctly identified, and how many of the five uncertain cases remained requests for review. This lets the reader see whether an apparently strong total hides confusion about a particular disposition.

    A confidence interval describes uncertainty around a proportion under an assumed sampling model. It is not a numerical confidence assigned to an individual agent recommendation. Wilson score intervals are appropriate for small proportions and extreme observed counts (Wilson, 1927; Newcombe, 1998). In this synthetic study they summarize finite case results under the stated model; they do not transform constructed cases into a representative sample of defense programs.

    Paired comparisons use the same unique cases under different controllers. The exact McNemar test compares the numbers of cases where one approach is correct and the other is not (McNemar, 1947). If exploratory comparisons are shown for all controller pairs, their descriptive status is stated and raw counts remain primary. Repetitions are used for stability and timing rather than entered as independent correctness observations. With only 20 primary evaluation cases, interpretation should emphasize observed differences and uncertainty.

    Three threats remain important. First, profile and fixture design may favor the shared validators. Second, labels and implementation currently lack independent human adjudication. Third, the benchmark excludes operational conditions such as diverse suppliers, authenticated approval, classified environments, and full service execution. The study tests a review mechanism within a bounded exercise. It does not establish acquisition savings, mission effectiveness, or acceptance authority outside that exercise.
    '''),
]))

content['chapters'].append(chapter(5, 'Results and discussion', [
    section('Three evidence sets with different meanings', '''
    Results are presented in three layers. The original conformance experiment establishes the value of stronger executable checks for its seeded fault model. The capstone pilot shows how a model selected tools and how the guard handled its decisions. The new benchmark provides the primary controller comparison for this revision. Keeping the layers separate prevents a result produced under one profile from being presented as validation of another.

    The original study contains 20 module packages, with two conformant controls and 18 single fault candidates. The pilot contains 20 generated development cases, including 17 faulted cases under the course review profile. The new benchmark contains 40 neutral cases divided between development and additional evaluation, with different category proportions in the two sets. Different inputs, criteria, and expected outcomes mean that an aggregate across all three would lack a coherent denominator.

    The public result tables link each published measure to its source record. A saved run includes evidence identity, controller settings, tool events, proposed disposition, guard output, and completion status. Charts are generated from the same verified export used for the tables. A committee member can therefore follow a summary result to a case outcome and then to the supporting trace. Any unavailable measure remains identified as unavailable.
    ''', table={'id': 'study-separation', 'caption': 'The evidence sets are distinct and are not pooled.', 'columns': ['Evidence set', 'Unique inputs', 'Main purpose', 'Main limit'], 'rows': [['Original conformance experiment', '20 modules with 18 seeded faults', 'Observe faults through stronger checks', 'Constructed fault model and two controls'], ['Capstone pilot', '20 development evidence packages', 'Demonstrate bounded model review', 'Descriptive names and one hosted sweep'], ['New benchmark', '40 neutral packages with 20 separate evaluation cases', 'Compare three controllers', 'Synthetic profile and pending independent label review']]}),
    section('The original experiment as a foundation', '''
    The original minimal baseline detected five of 18 seeded nonconformances. The conformance harness detected all 18. Both accepted the two conformant controls. Fault detection was therefore 27.8 percent for the minimal baseline and 100 percent for the harness on that constructed set. The respective Wilson 95 percent intervals were approximately 12.5 to 50.9 percent and 82.4 to 100 percent. The upper result should be read as complete detection of the selected faults, not proof that every possible fault would be found.

    Thirteen unique packages were correct under the harness and incorrect under the minimal baseline; none favored the baseline. The exact two sided McNemar result was p = 0.000244. A p value describes how unusual the paired difference would be under the test's equal correctness assumption. It does not measure the probability that MOSA works, nor does it quantify an operational program's likelihood of success. The constructed fault set determines the scope of this result.

    Both controls passed, but two controls offer little information about false positives in a larger population. Their 100 percent observed acceptance has a wide Wilson interval of approximately 34.2 to 100 percent. This matters because a harness that detects seeded problems may still reject legitimate supplier variation not represented by the controls. More diverse conformant packages would strengthen that part of the evidence.

    The archive also records greater computational effort. Its primary result fields contain median durations of about 0.348 milliseconds for the minimal baseline and 7.042 milliseconds for the harness, with median check counts of 14 and 177. The completed thesis contains other rounded timing summaries, so this revision names the archived primary fields rather than mixing timing populations. The inference remains narrow: more checks bought more observed evidence in a small local experiment.

    This foundation does not show that a model is needed. The successful harness is executable deterministic validation. The capstone preserves that logic and asks a new question about selecting and communicating checks. That separation protects the original research contribution while allowing the revision to evaluate a different controller layer.
    '''),
    section('The capstone pilot and guard corrections', '''
    The fixed course workflow matched all 20 expected disposition labels in the pilot. The standalone OpenRouter model matched 17 of 20 raw labels, and the guarded outcome matched all 20. Expected fault localization was recorded for all 17 faulted cases. The pilot thus demonstrates that the guard materially affected the final result. It does not justify describing the unguarded agent as fully correct.

    The raw model called three missing evidence cases not ready: missing manifest, missing SBOM, and missing provenance. The profile expected further review because required evidence was absent. The guard changed those recommendations to needs_review. This correction illustrates a practical distinction. A missing ingredient list means the reviewer cannot inspect the required component declaration. It does not establish that every declared or undeclared component is defective.

    Another saved pilot trace showed a failed SBOM validator followed by skipped interface comparison. The guard blocked completion because required coverage was incomplete. This fourth intervention concerned the path through the checks rather than a simple label correction. Together, the examples show that guard value depends on both disposition rules and coverage rules. The final label alone would not reveal the failure mode.

    The archived pilot summary reports 51 model selected validator calls compared with 60 for the fixed workflow. The model made 71 remote calls, used 42,016 input tokens and 2,354 output tokens, and reported a provider charge of $0.0205728. Median elapsed time was 3,916.684 milliseconds for the model and 4.98 milliseconds for the fixed workflow in the same Codespace. Reduced recorded validator selections therefore did not produce faster reviews.

    Those call totals come from the pilot's earlier evaluator, which counted distinct tool names in each saved result mapping. They describe that archived export and should not be treated as a reliable general measure of repeated invocation effort. The new evaluator uses event counts. The pilot also used descriptive case names and one sweep rather than a blinded repeated design. Its results motivate the new benchmark and are not substituted for it.
    '''),
    section('Interactive demonstrations are a separate kind of evidence', '''
    Six selected Codex traces demonstrated different validator order and an early stop for missing evidence. They matched the expected labels for those selected examples and recorded 16 validator selections compared with 18 for the same fixed reviews. These traces are useful for showing the file bridge and bounded workflow. They are not an independently blinded model accuracy study.

    The interactive controller had surrounding developer context that the standalone OpenRouter prompt did not necessarily receive. Its token usage was not available through the prototype's remote provider counters. A recorded zero in those counters therefore does not establish that the interactive model used no tokens or incurred no underlying cost. The public explanation keeps that missing measurement visible.

    Replaying a saved selection sequence demonstrates reproducibility of the recorded steps, not a new autonomous decision by the model. This distinction applies to the public website's walkthroughs as well. A reader opening a saved trace can see what happened in one recorded run. The page does not perform another model review merely because its diagram animates or expands the saved steps.
    '''),
    section('Primary results from the separate evaluation cases', '''
    The frozen benchmark's completion record is the starting point for interpretation. {{study.completion}} Offline controller results remain separate from hosted results, and any incomplete hosted schedule retains its failure or stopping reason. A completed offline comparison cannot supply missing model measurements. No model accuracy percentage is inferred from a controller that did not complete the relevant primary attempts.

    The first scheduled repetition on each of the 20 unique evaluation cases defines the primary disposition comparison. {{study.heldout_accuracy}} Category counts show whether each approach distinguishes readiness, a known blocker, and insufficient evidence. Raw and guarded measures appear side by side so that correct final outcomes cannot hide incorrect draft recommendations.

    Finding and citation results describe the support behind those decisions. {{study.heldout_findings}} A case that receives the expected disposition but omits a required finding is reported as a separate evidence quality failure. A cited location must either resolve to supporting content or satisfy the explicit absence rule for a missing requirement. These checks concern traceability within the profile, not the completeness of all possible MOSA evidence.

    The development cases are reported separately. {{study.development}} They show whether the implementation behaved as expected on inputs used to refine it. They provide a useful implementation record but a weaker basis for judging generalization than the separate evaluation cases. Agreement in both sets would still be limited by their shared synthetic construction.
    ''', figure={'id': 'accuracy-chart', 'caption': 'Raw and guarded recommendation match on 20 unique additional cases; the incomplete model comparison remains unestimated.', 'alt': 'Bars compare raw and guarded disposition match for fixed, adaptive, and model control. Unavailable model results are labeled unavailable, not displayed as zero accuracy.'}, table={'id': 'new-study-accuracy', 'source': 'study.primary', 'caption': 'Primary disposition results from the first scheduled repetition of unique evaluation cases.', 'columns': ['Controller', 'Raw match', 'Guarded match', 'Completed repeated runs'], 'rows': [['Fixed', '{{study.fixed.raw}}', '{{study.fixed.guarded}}', '{{study.fixed.completed}}'], ['Adaptive rules', '{{study.adaptive.raw}}', '{{study.adaptive.guarded}}', '{{study.adaptive.completed}}'], ['Model agent', '{{study.model.raw}}', '{{study.model.guarded}}', '{{study.model.completed}}']]}),
    section('Effort elapsed time cost and stability', '''
    Validation effort uses actual tool event counts in the new benchmark. {{study.effort}} The fixed controller's complete schedule defines a predictable amount of requested validation. Adaptive stopping can reduce that effort only when the halt satisfies the profile and preserves an appropriate disposition. Repeated or redundant model calls remain part of the total rather than disappearing behind unique tool coverage.

    Elapsed time and billed cost are reported independently. {{study.latency_cost}} Local timing describes the machine and execution conditions recorded in the manifest. Hosted timing includes provider and network waits as well as local checks. The provider charge is the recorded billed amount under the experiment's settings. It is not an estimate of the total cost of deploying or maintaining an acquisition review service.

    Repetitions show whether the same evidence leads to the same raw and guarded outcome across the scheduled runs. {{study.stability}} A stable guarded result may conceal unstable drafts if the guard repeatedly repairs them. Both forms of stability are therefore shown. Any timeout, invalid output, or stopped request appears in the stability and completion record rather than being omitted as an inconvenient outlier.

    The five dollar ceiling is also evaluated as a control. {{study.budget}} The ledger provides the basis for that statement. A successful refusal before an unsafe request is useful reliability evidence, while an incomplete hosted study is still an incomplete empirical comparison. The refusal does not supply the result that the prevented request might have produced.
    ''', figure={'id': 'effort-latency-cost', 'caption': 'Validation effort, elapsed time, and provider charge answer different performance questions.', 'alt': 'Separate panels report actual validator events, median elapsed time, and recorded provider dollars. Missing hosted data is labeled clearly.'}),
    section('What the comparison can establish', '''
    The pilot already shows that fewer recorded validator selections can coexist with slower reviews and weaker raw decisions. The new comparison asks whether that pattern persists when neutral cases and an adaptive rule alternative are used. {{study.interpretation}} The conclusion is based on the actual primary records rather than on an assumption that an agent adds value simply by selecting tools.

    If adaptive rules match guarded accuracy while using fewer checks than the fixed workflow, the study supports selective control for this profile. If the model achieves the same outcome while adding latency and cost, the additional model layer needs another measured benefit to justify it. Potential benefits such as clearer explanations or reduced human effort would require their own evaluation with readers; this benchmark does not measure them by intuition.

    If the model identifies different useful checks or improves a measured outcome, the report should show which cases produced that difference and whether it survived the guard. A model's plausible explanation is not a substitute for a supported finding. Likewise, an accuracy tie does not establish equal behavior when guard interventions, missed findings, citations, and failures differ. The design keeps those differences visible.

    The narrow result can still be valuable. An inspectable example of a model needing deterministic correction helps explain where human oversight and guard rules matter. A rule workflow that performs well gives a practical alternative for a small stable profile. A failed hosted schedule identifies a feasibility limit. Each outcome contributes evidence when reported with the same clarity as a favorable comparison.
    '''),
    section('Limitations and the next evidence needed', '''
    The study's inputs are small synthetic records. They do not include the ambiguity, document volume, varied suppliers, or changing operational conditions of a full acquisition review. The same author directed the profile, cases, and implementation. Independent label review remains pending. A public repository improves inspectability, but inspectability does not by itself make the evaluation independent.

    The shared validators are another boundary. A defect in a common validator can affect every controller and still produce an apparent tie. Tests cover declared behaviors and selected failure paths; they do not prove the absence of every implementation defect. The guard prevents unsupported dispositions only within its encoded rules. It does not validate requirements that the profile omits.

    Human review remains demonstrated rather than measured as a user study. The project shows approval, revision requests, source change checks, and rollback, but it does not quantify committee comprehension or time saved for acquisition staff. It also does not establish an authenticated approval chain. A later study could ask independent reviewers to interpret saved reports, locate evidence, and choose a justified action before comparing their effort across report formats.

    The strongest next evidence would come from independently labeled packages, additional conformant variation, and realistic but releasable supplier examples. New checks could test executed message semantics and broader component inventories. Any extension should keep versioned profiles and repeat the controller comparison, because a model's value may depend on how complex the permitted decisions become. The present study gives a reproducible starting point for that investigation.
    '''),
]))

content['chapters'].append(chapter(6, 'Conclusions and future work', [
    section('What this thesis contributes', '''
    MOSA review needs a clear connection between a claim, the evidence supplied for it, and the decision a person records. This thesis develops that connection through a conformance harness and a bounded agent extension. The original experiment supports the value of stronger executable checks within its seeded fault model. The capstone shows why model drafts and deterministic guard outcomes must remain separate. The new benchmark compares controller choices using common validators and an explicit evidence profile.

    {{study.conclusion}} The conclusion does not require a model advantage. If a rule based workflow achieves the same supported outcomes with lower time or cost, that result provides a useful design choice. If the hosted evaluation remains incomplete, the conclusion reports that limit and relies only on the completed evidence. A failed or stopped run is part of the research record.

    The most defensible role for the agent in this implementation is assistance with inspection choices and a draft explanation. Required observations remain in validator outputs, the guard checks the supported disposition, and the person retains approval. These boundaries make the prototype reviewable. They do not establish official certification or unrestricted readiness for defense use.
    '''),
    section('A focused path for further work', '''
    Further work should strengthen the evidence before expanding the system's authority. Independent label review is the first priority. Additional packages should vary legitimate interfaces and supplier practices, because detecting designed faults does not establish a low false rejection rate. A reader study could then measure whether plain language reports help people find evidence and understand uncertainty without concealing technical detail.

    Technical extensions can add executed semantic tests, broader standards validation, live advisory snapshots, and stronger identity controls. Each addition needs a defined profile, expected outcomes, and a recorded comparison. A larger document search agent would require separate evaluation of retrieval and citation support. Multiple agents or additional model providers should be introduced only when a concrete evidence need justifies their extra complexity.

    The class repository and its checkpoint history remain intact. After course submission, a tested release can be copied to the thesis repository with its source commit, hashes, and evaluation configuration. The public reading site will remain a static guide to the research, while live review remains in a private environment. This separation allows the committee to inspect the work easily and lets later thesis development proceed with a clear source history.
    '''),
]))

content['references'] = [
    {'id': 'law2026', 'text': '10 U.S.C. § 4401. (2026). Requirement for modular open system approach in major defense acquisition programs; definitions. Office of the Law Revision Counsel, U.S. House of Representatives.', 'url': 'https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section4401&num=0&edition=prelim', 'role': 'MOSA statutory context'},
    {'id': 'bray2017', 'text': 'Bray, T. (Ed.). (2017). The JavaScript Object Notation (JSON) data interchange format (RFC 8259). Internet Engineering Task Force.', 'url': 'https://www.rfc-editor.org/info/rfc8259/', 'role': 'Structured evidence format'},
    {'id': 'bryan2013', 'text': 'Bryan, P., Zyp, K., & Nottingham, M. (2013). JavaScript Object Notation (JSON) Pointer (RFC 6901). Internet Engineering Task Force.', 'url': 'https://www.rfc-editor.org/info/rfc6901/', 'role': 'Evidence field locations'},
    {'id': 'diazlegacy', 'text': 'Diaz, D. J. (2026a). A conformance harness for verifiable modular open systems outcomes in defense acquisition: Design, implementation, and controlled evaluation [Completed research draft and accompanying executable archive]. University of Oklahoma.', 'url': 'https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/tree/main/evidence/legacy', 'role': 'Original experiment source records'},
    {'id': 'diazpilot', 'text': 'Diaz, D. J. (2026b). MOSA evidence review agent: Capstone design review and progress checkpoint [Software prototype and recorded pilot evidence]. Agentic Systems course.', 'url': 'https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis/tree/main/evidence/pilot', 'role': 'Separate capstone pilot source records'},
    {'id': 'diazbenchmark', 'text': 'Diaz, D. J. (2026c). MOSA evidence review thesis: Frozen benchmark, evaluation protocol, and recorded controller results [Research software and dataset].', 'url': 'https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis', 'role': 'New benchmark and reproducibility'},
    {'id': 'dod2025', 'text': 'Department of Defense. (2025). Implementing a Modular Open Systems Approach in Department of Defense programs. Office of the Under Secretary of Defense for Research and Engineering.', 'url': 'https://www.cto.mil/wp-content/uploads/2025/03/MOSA-Implementation-Guidebook-27Feb2025-Cleared.pdf', 'role': 'Official implementation context'},
    {'id': 'gao2025', 'text': 'U.S. Government Accountability Office. (2025). Weapon systems acquisition: DOD needs better planning to attain benefits of modular open systems (GAO 25 106931).', 'url': 'https://www.gao.gov/products/gao-25-106931', 'role': 'Oversight findings and motivation'},
    {'id': 'hevner2004', 'text': 'Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75 to 105.', 'url': 'https://doi.org/10.2307/25148625', 'role': 'Research method'},
    {'id': 'jia2011', 'text': 'Jia, Y., & Harman, M. (2011). An analysis and survey of the development of mutation testing. IEEE Transactions on Software Engineering, 37(5), 649 to 678.', 'url': 'https://doi.org/10.1109/TSE.2010.62', 'role': 'Known changes as test challenges'},
    {'id': 'mcnemar1947', 'text': 'McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. Psychometrika, 12(2), 153 to 157.', 'url': 'https://doi.org/10.1007/BF02295996', 'role': 'Paired correctness analysis'},
    {'id': 'nist2012', 'text': 'National Institute of Standards and Technology. (2012). Conformance testing methodology for ANSI/NIST ITL 1 2011, data format for the interchange of fingerprint, facial and other biometric information, Release 1.0 (NIST SP 500 295; F. L. Podio, D. Yaga, & C. J. McGinnis, Eds.).', 'url': 'https://doi.org/10.6028/NIST.SP.500-295', 'role': 'Conformance assertion method, not a MOSA standard'},
    {'id': 'nist2015', 'text': 'National Institute of Standards and Technology. (2015). Secure hash standard (Federal Information Processing Standards Publication 180 4).', 'url': 'https://doi.org/10.6028/NIST.FIPS.180-4', 'role': 'Evidence fingerprints'},
    {'id': 'nist2023', 'text': 'National Institute of Standards and Technology. (2023). Artificial intelligence risk management framework (AI RMF 1.0) (NIST AI 100 1).', 'url': 'https://doi.org/10.6028/NIST.AI.100-1', 'role': 'AI risk context'},
    {'id': 'nist2024', 'text': 'National Institute of Standards and Technology. (2024). Artificial intelligence risk management framework: Generative artificial intelligence profile (NIST AI 600 1).', 'url': 'https://doi.org/10.6028/NIST.AI.600-1', 'role': 'Risks specific to generated content'},
    {'id': 'ntia2021', 'text': 'National Telecommunications and Information Administration. (2021). The minimum elements for a software bill of materials (SBOM). U.S. Department of Commerce.', 'url': 'https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom', 'role': 'Historical component inventory baseline, not claimed as the latest rule'},
    {'id': 'newcombe1998', 'text': 'Newcombe, R. G. (1998). Two sided confidence intervals for the single proportion: Comparison of seven methods. Statistics in Medicine, 17(8), 857 to 872.', 'url': 'https://doi.org/10.1002/(SICI)1097-0258(19980430)17:8<857::AID-SIM777>3.0.CO;2-E', 'role': 'Intervals for small proportions'},
    {'id': 'openapi2021', 'text': 'OpenAPI Initiative. (2021). OpenAPI specification, version 3.1.0.', 'url': 'https://spec.openapis.org/oas/v3.1.0.html', 'role': 'Interface format reference, profile checks selected fields only'},
    {'id': 'cyclonedx2025', 'text': 'OWASP Foundation. (2025). CycloneDX specification, version 1.7.', 'url': 'https://cyclonedx.org/specification/overview/', 'role': 'Component inventory format reference'},
    {'id': 'parnas1972', 'text': 'Parnas, D. L. (1972). On the criteria to be used in decomposing systems into modules. Communications of the ACM, 15(12), 1053 to 1058.', 'url': 'https://doi.org/10.1145/361598.361623', 'role': 'Modularity theory'},
    {'id': 'peffers2007', 'text': 'Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. Journal of Management Information Systems, 24(3), 45 to 77.', 'url': 'https://doi.org/10.2753/MIS0742-1222240302', 'role': 'Artifact development and evaluation process'},
    {'id': 'rabanser2026', 'text': 'Rabanser, S., Kapoor, S., Kirgis, P., Liu, K., Utpala, S., & Narayanan, A. (2026). Towards a science of AI agent reliability [Preprint]. arXiv.', 'url': 'https://arxiv.org/abs/2602.16666', 'role': 'Reliability dimensions, supplementary to MOSA authority'},
    {'id': 'schick2023', 'text': 'Schick, T., Dwivedi Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. Advances in Neural Information Processing Systems, 36.', 'url': 'https://arxiv.org/abs/2302.04761', 'role': 'Model tool selection research'},
    {'id': 'wilson1927', 'text': 'Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. Journal of the American Statistical Association, 22(158), 209 to 212.', 'url': 'https://doi.org/10.1080/01621459.1927.10502953', 'role': 'Proportion intervals'},
    {'id': 'yao2023', 'text': 'Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. International Conference on Learning Representations.', 'url': 'https://arxiv.org/abs/2210.03629', 'role': 'Interleaving observations and model actions'},
]

content['glossary'] = [
    {'term': 'MOSA', 'definition': 'Modular Open Systems Approach. A business and technical strategy for changing separable system parts through defined interfaces.', 'example': 'Replace a processor while keeping an agreed sensor message.', 'relevance': 'The thesis tests a small evidence slice of this broader approach.', 'color': 'blue'},
    {'term': 'Agent', 'definition': 'A model that observes results, selects permitted actions, and drafts a response.', 'example': 'Choose interface comparison after package inspection.', 'relevance': 'Its selection and draft are evaluated separately from guard output.', 'color': 'purple'},
    {'term': 'Adaptive workflow', 'definition': 'A process whose next step follows an explicit condition found during review.', 'example': 'Stop and request a missing manifest.', 'relevance': 'Rules can provide selective effort without a model.', 'color': 'blue'},
    {'term': 'Artifact', 'definition': 'A file or record used as evidence.', 'example': 'An interface contract or saved test result.', 'relevance': 'A review needs identifiable inputs.', 'color': 'blue'},
    {'term': 'Conformance', 'definition': 'Satisfaction of a declared requirement under a declared check.', 'example': 'Two files declare the same interface version.', 'relevance': 'A passing check has a bounded meaning.', 'color': 'green'},
    {'term': 'Decision guard', 'definition': 'Deterministic code that checks coverage and the support for a proposed disposition.', 'example': 'Convert a missing evidence draft to needs_review.', 'relevance': 'A correct final result may depend on guard correction.', 'color': 'blue'},
    {'term': 'Disposition', 'definition': 'The technical outcome recorded for a review.', 'example': 'Ready, not ready, or further review needed.', 'relevance': 'It is distinct from human approval.', 'color': 'amber'},
    {'term': 'Interface', 'definition': 'The defined boundary through which components exchange data or services.', 'example': 'A message from a sensor to a processor.', 'relevance': 'Replacement requires a dependable boundary.', 'color': 'blue'},
    {'term': 'JSON', 'definition': 'JavaScript Object Notation. A structured text format for fields, objects, and lists.', 'example': 'A version field stored inside an info object.', 'relevance': 'Validators can read the evidence consistently.', 'color': 'blue'},
    {'term': 'JSON Pointer', 'definition': 'A standard field address inside a JSON document.', 'example': '/info/version addresses the version inside info.', 'relevance': 'A reader can find the support for a finding.', 'color': 'blue'},
    {'term': 'SBOM', 'definition': 'Software bill of materials. An inventory of software components and related details.', 'example': 'A processor lists a library and its version.', 'relevance': 'A reviewer can compare declared dependencies with supplied ingredients.', 'color': 'blue'},
    {'term': 'Provenance', 'definition': 'Recorded origin and history of evidence.', 'example': 'A source identifier and hashes for produced files.', 'relevance': 'A review should apply to the evidence actually inspected.', 'color': 'blue'},
    {'term': 'Hash', 'definition': 'A fingerprint calculated from file bytes.', 'example': 'A new file produces a different SHA 256 fingerprint.', 'relevance': 'Detects changes but does not prove supplier trust.', 'color': 'blue'},
    {'term': 'Unknown evidence', 'definition': 'Information that is absent or could not be established.', 'example': 'A required validator is unavailable.', 'relevance': 'It cannot be described as a passed check.', 'color': 'amber'},
    {'term': 'Blocker', 'definition': 'An observed condition that violates a required profile check.', 'example': 'Manifest and interface versions disagree.', 'relevance': 'The report names a correction before readiness.', 'color': 'crimson'},
    {'term': 'Held out case', 'definition': 'An evaluation input kept separate from controller development.', 'example': 'A neutral package first run after settings are frozen.', 'relevance': 'Reduces tuning on reported cases but does not create independent authorship.', 'color': 'amber'},
    {'term': 'Latency', 'definition': 'Elapsed time before the complete review result is available.', 'example': 'A model waits for a remote provider response.', 'relevance': 'Fewer checks may still take longer.', 'color': 'blue'},
    {'term': 'Token', 'definition': 'A provider counted unit of model input or output text.', 'example': 'An evidence message contributes input tokens.', 'relevance': 'Helps account for paid model usage.', 'color': 'purple'},
    {'term': 'Confidence interval', 'definition': 'A statistical range describing uncertainty around a measured proportion under stated assumptions.', 'example': 'Two accepted controls produce a wide interval.', 'relevance': 'It is not the model\'s personal confidence score.', 'color': 'amber'},
    {'term': 'Rollback', 'definition': 'Restoring a previous approval reference while retaining history.', 'example': 'Return to an earlier accepted review record.', 'relevance': 'It changes the current pointer without erasing evidence.', 'color': 'blue'},
]

content['appendices'] = [
    {'title': 'Reproducing and inspecting the study', 'sections': [
        section('Begin with a saved example', '''
        The companion site's Start Here page links to the thesis, a saved review, the comparison results, the glossary, and reproduction instructions. Begin with a ready case and a missing evidence case. Compare the proposed disposition with the guard output. Then open the file and field cited by one finding. A reader can inspect this route without running a model or entering credentials.

        The repository separates original evidence, pilot evidence, and the new benchmark. Each has its own manifest or saved source record. The chart data comes from the verified result export, so the same numerator and denominator appear in the thesis, README, and site. README means the introductory repository document. It explains the folder map and directs readers to a suitable level of detail.
        '''),
        section('Run offline checks before hosted evaluation', '''
        A fresh checkout should first run the documented offline tests and fixed and adaptive evaluations. Use the Python version stated by the tested release. Python is the programming language used by the prototype. No hosted credential is needed for the offline controllers. Compare the resulting logical outcomes with the published case records. Local timings may differ on another machine and should not be required to match byte for byte.

        Hosted reproduction requires a privately configured OpenRouter credential and a new explicit spending allowance. A credential is the secret that authorizes use of the provider account. Keep it outside tracked files, screenshots, public logs, and the website. The five dollar ceiling in the reported study applies to that recorded experiment; it is not automatically a continuing allowance for future reruns. The recorded model and settings should be copied exactly when investigating repeatability.
        '''),
        section('Preserve a change record', '''
        If a case, label, prompt, validator, or guard changes, save a new study version and identify the reason. Preserve the earlier records. Update diagrams and prose when they describe altered behavior, then regenerate tables and charts from the new result export. A version label alone is insufficient if the underlying inputs cannot be recovered. The frozen manifest provides the fingerprints needed to inspect that relationship.
        '''),
    ]},
    {'title': 'Migration and research boundaries', 'sections': [
        section('Copy a tested release after course submission', '''
        Keep the class repository, its original checkpoint files, and its course history intact. After submission, select a tested capstone commit. Copy only the approved prototype release, public fixtures, tests, and releasable evaluation exports to the thesis repository. Record the source commit, relative file map, SHA 256 hashes, profile version, and evaluation settings. Exclude secrets, private review state, temporary service addresses, and unrelated coursework.

        Test the copied release from a fresh checkout of the thesis repository. It must run without importing code from the class folder. Compare the logical outcomes and execute the offline tests. Preserve author and inherited license notices. After that verification, the thesis repository becomes the source for later thesis work, while the class repository remains the historical course submission. The migration guide supplies exact commands for the tested release rather than asking the reader to infer which files are safe to publish.
        ''', figure={'id': 'migration', 'caption': 'A tested release moves to the thesis repository after course submission while class history remains intact.', 'alt': 'The class repository produces a tested release. A manifest and hashes accompany a copy into the thesis repository. A fresh checkout verifies independent operation.'}),
        section('What the public site does and does not claim', '''
        The public website hosts stored research explanations and evidence. It does not run the model, grant approval authority, or provide a certification service. Its readiness labels refer to the synthetic profile. The evidence packages are constructed examples, and the advisory fixture is explicitly synthetic. Independent label review and committee approval of the revision remain pending unless later dated records establish them.

        Topics such as full acquisition governance, financial forecasting, legal rights negotiation, organization wide rollout, and domain specific mission certification remain outside this condensed study. They may affect a real implementation, but this prototype does not measure them. Model based systems engineering, or MBSE, is the use of structured models to support system design. Connecting such models to this profile is a possible extension rather than a demonstrated feature of the present evaluation.
        '''),
    ]},
]

content['reduction_rationale'] = [
    {'source': 'Chapters 2 through 5', 'action': 'Retain the problem, source hierarchy, modularity, policy context, and need for verified evidence in new Chapters 1 and 2.', 'reason': 'These establish why the technical review matters.'},
    {'source': 'Chapters 6 and 7', 'action': 'Preserve the original experiment as a clearly separate foundation and develop new methods and results around the capstone.', 'reason': 'The two studies address different questions and must not be pooled.'},
    {'source': 'Chapters 8 through 15', 'action': 'Combine evidence identity, architecture, tools, gates, tests, and human review in Chapter 3 and the reproduction guide.', 'reason': 'The committee needs the implemented path, not a large ecosystem design.'},
    {'source': 'Enterprise implementation, acquisition, workforce, and roadmap material', 'action': 'Remove separate roadmap and organization chapters from the main thesis; preserve useful planning material as companion background.', 'reason': 'Those programs are not measured by this implementation.'},
    {'source': 'Chapters 19 through 24', 'action': 'Remove domain catalogs, financial models, extended legal treatment, mission scenarios, and MBSE as main chapters.', 'reason': 'They broaden the claim beyond the bounded capstone study.'},
    {'source': 'Extensive equations and technical catalogs', 'action': 'Move implementation details to inspectable repository documentation; retain only metrics used in the new evaluation.', 'reason': 'Readers need enough detail to assess the result without an oversized main document.'},
    {'source': 'Chapters 25 and 26', 'action': 'Replace with focused discussion, limitations, and conclusions tied to recorded results.', 'reason': 'The conclusion should match the smaller research question.'},
]

# Add near-topic explanations without changing the formal heading colors.
content['chapters'][1]['sections'][3]['callout'] = {'color': 'blue', 'title': 'A hash identifies bytes', 'text': 'A hash is like a fingerprint for a file. Matching fingerprints show that the saved review and current input have the same recorded bytes. They do not show that the file is truthful or safe.'}
content['chapters'][2]['sections'][4]['callout'] = {'color': 'purple', 'title': 'A model choice is a proposal', 'text': 'The agent may choose a permitted check and explain its result. Fixed validators supply the observations, the guard checks support, and a person records approval.'}
content['chapters'][3]['sections'][6]['callout'] = {'color': 'amber', 'title': 'Repeated runs are not new cases', 'text': 'Three reviews of one package show how consistent the workflow is. They still count as one distinct package when estimating correctness across cases.'}

# Condensed reading pass after the first layout preview. These paragraphs repeat
# principles explained elsewhere; methods, measurements, and limits remain.
remove_paragraphs = {
    (1, 2): [2], (1, 3): [2],
    (2, 1): [3], (2, 2): [1, 3], (2, 3): [1],
    (2, 4): [3], (2, 5): [1],
    (3, 1): [3], (3, 4): [3], (3, 7): [3],
    (4, 1): [3], (4, 6): [3], (4, 7): [3],
    (5, 1): [1], (5, 2): [4], (5, 7): [3],
}
revised_paragraphs = {
    (1, 1, 3): 'This study makes the route from a declared requirement to a review recommendation visible and repeatable. It focuses on software evidence that a small prototype can inspect. A reader can ask what was checked, what was missed, and who is responsible for the decision. A few files cannot establish an entire weapon system\'s readiness.',
    (2, 5, 0): 'An agent in this thesis is a language model that observes tool results, chooses a permitted next check, and drafts a review. This is one use of artificial intelligence, or AI. ReAct demonstrated interleaved reasoning and information gathering actions (Yao et al., 2023). Toolformer explored model selection of external tools (Schick et al., 2023). These studies motivate tool mediated designs; they do not establish accuracy for this MOSA profile.',
    (3, 3, 3): 'Every controller uses the same validators, so tool selection is the comparison rather than inspection capability. Each actual invocation records the tool, findings, input identity, and elapsed time. Repeated invocations count as repeated work.',
    (3, 4, 0): 'The fixed workflow runs package inspection, interface comparison, and SBOM comparison in a declared order. Coverage is predictable and needs no model or pricing information. It may do unnecessary work on an incomplete package, although that work can be inexpensive for this small profile.',
    (3, 6, 0): 'The decision guard is deterministic code: declared inputs and rules produce the same result. It checks known finding identifiers, required coverage or a justified halt, and support for the disposition. Unsupported or malformed drafts remain incomplete. A second model does not decide whether the first model is correct.',
    (3, 6, 2): 'A guard intervention occurs when the guard corrects a disposition or blocks completion. It remains in the record. Raw and guarded outcomes show whether reliability came from the controller, fixed checks, or both. A coverage block can leave the disposition unchanged while still counting as an intervention.',
    (3, 8, 3): 'NIST\'s AI Risk Management Framework addresses context, measurement, governance, and risk management (NIST, 2023). Its generative AI profile addresses risks of generated content (NIST, 2024). This design keeps model actions bounded, preserves failures, and assigns approval to a person. It does not claim full implementation of either publication.',
    (4, 4, 2): 'Run order and environment are recorded. Caches and changing network or provider conditions can affect timing. Elapsed time covers the full review, including model waiting and guard work. Where available, tool time is recorded separately. The study does not attribute every timing difference to model reasoning.',
    (4, 5, 4): 'Elapsed time, tokens, provider charge, guard interventions, and source integrity are also recorded. Missing provider measurements remain unavailable. Offline zeros mean no hosted calls occurred; missing interactive usage cannot be interpreted as a free model run.',
    (4, 6, 1): 'A reservation must bound all permitted billable work. The text only evaluation rejects search, plugins, multimodal content, and unknown request options. Verified token and request prices plus provider price caps define the bound. Unpriced reasoning or other usage causes a stop. Actual charges reconcile reservations; unresolved billing after a timeout does not immediately release the allowance.',
    (5, 4, 2): 'Replaying saved selections demonstrates those steps, not a new autonomous decision. The public walkthroughs likewise present recorded traces. Expanding or animating a saved review does not perform another model evaluation.',
    (5, 5, 0): 'The completion record identifies what actually ran. {{study.completion}} Failed and stopped attempts retain their reasons. Offline results cannot supply missing hosted measurements.',
    (5, 5, 1): 'The first scheduled repetition on the 20 unique additional cases defines primary accuracy. {{study.heldout_accuracy}} Raw, guarded, and category results show both controller decisions and reliance on the guard.',
    (5, 5, 2): '{{study.heldout_findings}} Missing target findings, additional findings, and invalid references remain distinct measures. A citation must resolve to supporting content or satisfy an explicit absence check.',
    (5, 5, 3): 'Development results remain separate. {{study.development}} Agreement on cases used to refine the implementation supplies a useful development record, while shared synthetic construction limits generalization in both sets.',
    (5, 6, 0): 'Effort counts actual invocation events. {{study.effort}} Required coverage and a justified halt determine whether reduced work supports a complete review.',
    (5, 6, 1): '{{study.latency_cost}} Hosted time includes network and provider waiting. The recorded provider charge is not a complete organizational cost estimate.',
    (5, 6, 2): '{{study.stability}} Raw and guarded stability remain separate. A stable final result can hide changing drafts repaired by the guard. Failed and stopped attempts remain visible.',
    (5, 6, 3): '{{study.budget}} A refused request can demonstrate a working spending control, but it cannot supply the empirical result of the request that did not run.',
    (5, 7, 0): 'The pilot motivates comparison with an adaptive rule alternative. {{study.interpretation}} Conclusions follow the primary records rather than assuming that model selected checks add value.',
}
for c in content['chapters']:
    for index, s in enumerate(c['sections'], 1):
        for pindex in range(len(s['paragraphs'])):
            replacement = revised_paragraphs.get((c['number'], index, pindex))
            if replacement is not None:
                s['paragraphs'][pindex] = replacement
        removed = set(remove_paragraphs.get((c['number'], index), []))
        s['paragraphs'] = [p for pindex, p in enumerate(s['paragraphs']) if pindex not in removed]
content['appendices'] = [{
    'title': 'Reproduction migration and research boundaries',
    'sections': content['appendices'][0]['sections'] + content['appendices'][1]['sections'],
}]

# The new hosted schedule stopped on unavailable service and unknown billing.
# The archived successful model pilot remains a different, measured study.
content['front']['abstract'][-1] = 'A new benchmark contains 40 neutral cases divided into development and additional evaluation sets. An offline preflight exposed a structural citation issue before hosted evaluation, and the protocol records the amendment. {{study.abstract}} The new hosted request failed with an unavailable resource response. Its charge could not be confirmed, so later paid requests stopped. A complete model comparison remains pending. The contribution is an inspectable review method and a reproducible offline comparison. Claims remain limited to the synthetic profile, and independent label review remains pending.'
content['chapters'][4]['sections'][4]['paragraphs'][0] = 'The completion record identifies what actually ran. {{study.completion}} The provider returned code 404 for the hosted Hypertext Transfer Protocol request, abbreviated HTTP. This indicates that a requested resource was not found. No reliable charge was supplied, so later paid requests stopped. Failed and unattempted slots retain their status. Offline results cannot supply missing hosted measurements.'
content['chapters'][5]['sections'][0]['paragraphs'][0] = 'MOSA review needs a clear connection between a claim, supplied evidence, and the decision a person records. This thesis develops that connection through a conformance harness and a bounded agent extension. The original experiment supports stronger executable checks within its seeded fault model. The capstone pilot shows why model drafts and guard outcomes must remain separate. The new benchmark provides an offline controller comparison and records a hosted stopping condition; it does not complete a new three controller comparison.'

def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)

all_strings = list(strings(content))
assert not any('\u2013' in t or '\u2014' in t for t in all_strings)
output = BASE / 'thesis_content.json'
output.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding='utf-8')
word_count = sum(len(re.findall(r'\b\w+\b', text)) for text in all_strings)
chapter_counts = {c['number']: sum(len(re.findall(r'\b\w+\b', p)) for s in c['sections'] for p in s['paragraphs']) for c in content['chapters']}
print(json.dumps({'output': str(output), 'all_content_words': word_count, 'chapter_prose_words': chapter_counts, 'chapter_prose_total': sum(chapter_counts.values()), 'references': len(content['references']), 'glossary_terms': len(content['glossary']), 'placeholders': sorted(set(re.findall(r'\{\{study[^}]+\}\}', '\n'.join(all_strings))))}, indent=2))
