#!/usr/bin/env python3
"""
generate_restructured_en.py
Restructures DRAFT_JURNAL_IJG_ENGLISH.md into the rigorous 9-section structure:
1. Introduction
2. Related Work
3. Methodology
4. System Implementation
5. Experimental Design
6. Results
7. Discussion
8. Threats to Validity and Limitations
9. Conclusion and Future Work
"""

import os
import re

JURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(JURNAL_DIR, "DRAFT_JURNAL_IJG_ENGLISH.md")
OUT_PATH = os.path.join(JURNAL_DIR, "DRAFT_JURNAL_IJG_ENGLISH.md")

with open(SRC_PATH, "r", encoding="utf-8") as f:
    src = f.read()

def get_block(start_str, end_str, text=src):
    p1 = text.find(start_str)
    if p1 == -1:
        raise ValueError(f"Start string not found: {start_str[:40]}...")
    p1 += len(start_str)
    if end_str:
        p2 = text.find(end_str, p1)
        if p2 == -1:
            raise ValueError(f"End string not found: {end_str[:40]}...")
        return text[p1:p2].strip()
    else:
        return text[p1:].strip()

# 0. HEADER & ABSTRACT
p_sec1 = src.find("## 1. INTRODUCTION")
header_abstract = src[:p_sec1].strip()

# Standardize bounded results in abstract
header_abstract = header_abstract.replace(
    "92.50%** (37/40) (**90.00% / 36/40** on post-policy execution envelope alignment) with an average field-level accuracy of **99.25% (398/401)**",
    "87.50%** (35/40) (**90.00% / 36/40** on post-policy execution envelope alignment) with an average field-level accuracy of **98.62% (748/758)**"
)

# SECTION 1: INTRODUCTION
sec1_1 = get_block("### 1.1 Background and Urban Spatial Context", "### 1.2 Research Lineage")
sec1_lineage = get_block("### 1.2 Research Lineage: From Conventional Exploration to AI-Mediated Spatial Querying", "### 1.3 Limitations of Existing Approaches")
sec1_gaps = get_block("### 1.3 Limitations of Existing Approaches: Hallucination Hazards and Vector RAG Inadequacy", "### 1.4 Scientific Positioning")
sec1_pos = get_block("### 1.4 Scientific Positioning and Problem Formulation", "### 1.5 Principal Scientific Contributions")
sec1_contrib = get_block("### 1.5 Principal Scientific Contributions", "## 2. THEORETICAL FOUNDATION")

sec1_rqs = """### 1.3 Research Questions (RQs)
To systematically evaluate the efficacy of the proposed structured semantic control layer and factual grounding firewall, this study formulates four core Research Questions (RQs):
* **RQ1 (Semantic Parsing Fidelity):** To what extent can large language models reliably parse natural-language spatial queries into formal canonical intent representations (Raw SIR and Validated CSIR) while strictly adhering to the *No Intent Alteration* principle?
* **RQ2 (Spatial Execution Safety & Correctness):** Does the integration of a deterministic 6-dimensional validator and parameterized query compiler guarantee safety invariants (preventing unauthorized query execution or SQL injection) and compute spherical spatial predicates with precision via native `ST_Distance_Sphere` under acceptable latency constraints?
* **RQ3 (Factual Grounding & Zero Fabrication):** How effectively does the post-generation algorithmic proof firewall (*Claim-Level Grounding Validator*) eliminate destination entity hallucinations (*zero fabricated POIs*) and enforce factual alignment with the underlying relational database?
* **RQ4 (Cognitive Efficiency & Usability):** How does shifting from conventional multi-step WIMP form manipulation to guided conversational interaction impact cognitive Task Completion Time (TCT) and user satisfaction measured via the standardized System Usability Scale (SUS)?
"""

sec1_parts = [
    "## 1. INTRODUCTION\n",
    "### 1.1 Background and Urban Spatial Context\n" + sec1_1 + "\n",
    "### 1.2 Research Gaps and Specific Problem Formulation\n" + sec1_gaps + "\n\n" + sec1_pos + "\n",
    sec1_rqs,
    "### 1.4 Principal Scientific Contributions\n" + sec1_contrib
]
sec1_out = "\n".join(sec1_parts)

# SECTION 2: RELATED WORK
sec2_parts = [
    "## 2. RELATED WORK\n",
    """### 2.1 Conversational GIS and Autonomous Spatial Interaction
The integration of natural language processing into Geographic Information Systems has catalyzed the emergence of *Conversational GIS* and *Autonomous GIS* [35], [36]. Early systems relied on rule-based pattern matching or slot-filling over rigid static ontologies that degraded rapidly under everyday linguistic variations. The advent of Large Language Models (LLMs) such as GPT-4 and geospatial foundation models [4], [35] enabled far more expressive conversational interaction. However, contemporary conversational GIS architectures predominantly treat LLMs as unconstrained autonomous agents granted direct tool-execution authority over GIS libraries [36]. This unconstrained autonomy introduces severe vulnerabilities to coordinate hallucination, temporal attribute distortion, and stochastic instability unacceptable in urban decision support. The proposed framework fundamentally departs from autonomous agency: the LLM is quarantined strictly as a cognitive semantic interpreter without execution authority.
""",
    """### 2.2 Text-to-SQL and Relational Database Interfaces
Translating natural language into structured queries (*Text-to-SQL*) has been extensively investigated on standard benchmarks such as Spider, DIN-SQL [28], and RESDSQL [29]. In geospatial domains, unconstrained Text-to-SQL architectures encounter three acute failure modes: (1) **Schema and Syntax Hallucinations:** LLMs frequently invent non-existent table names, columns, or join relations; (2) **Inability to Optimize Spherical Spatial Functions:** LLMs often construct erroneous manual trigonometric formulas, suffer floating-point truncation, or fail to leverage native database kernel spatial primitives such as `ST_Distance_Sphere`; and (3) **Security Vulnerabilities:** Permitting LLMs to synthesize raw SQL strings exposes database engines to prompt-injection vulnerabilities and unauthorized data manipulation. In response, this work adopts *Parameterized Semantic Compilation*, wherein the LLM emits strictly typed intent semantics (SIR), while SQL syntax is synthesized entirely by an application-layer, non-LLM parameterized compiler.
""",
    """### 2.3 Grounded Generation and Mitigation of Spatial Hallucinations
The prevalence of factual hallucination in LLMs [5], [31] prompted the widespread adoption of Retrieval-Augmented Generation (RAG) [6], [7]. In general text retrieval, dense-vector similarity search over document chunks effectively mitigates unsupported text generation [30]. However, in urban geospatial environments governed by multi-criteria constraints (such as spherical distance radii, budgetary limits, and circadian opening schedules), vector RAG fundamentally fails. Vector embeddings cannot evaluate exact mathematical inequalities ($d \\le 10\\text{ km}$, $\\text{price} \\le 15,000$). Furthermore, post-generation hallucination mitigation relying on secondary LLM judges (*LLM-as-a-judge*) introduces additional stochastic noise and excessive latency overhead. This research introduces a deterministic, rule-based algorithmic verification firewall (*Claim-Level Grounding Validator*) that mathematically audits every generated factual claim against database tuples without secondary generative models.
""",
    """### 2.4 Constraint-Based Spatial Recommendation Systems
Within the taxonomy of tourism retrieval and decision support systems [1], [3], [14], [18], spatial recommendation systems are broadly categorized into collaborative filtering, content-based filtering, and constraint-based recommendation [18]. Urban tourism systems for independent travelers frequently suffer from acute cold-start conditions where prior user interaction histories are unavailable [3]. Consequently, constraint-based approaches represent the most dependable paradigm: candidate destinations are deterministically retrieved based on explicit user constraints articulated in the query (geographical position, radius, opening hours, ticket budget) [14]. This research positions itself firmly in the constraint-based spatial recommendation quadrant, deliberately disclaiming latent preference learning to guarantee strict traceability, reproducible execution, and determinism across all recommendations.
""",
    "### 2.5 Research Lineage: From Conventional WIMP Exploration (DTExplorer) to Reliability-Controlled Systems\n" + sec1_lineage
]
sec2_out = "\n".join(sec2_parts)

# SECTION 3: METHODOLOGY
sec2_framework = get_block("### 2.0 The Dual Control Boundaries Framework for Conversational Spatial Systems", "### 2.1 The Decoupling Axiom")
sec2_decoupling = get_block("### 2.1 The Decoupling Axiom: Semantics vs. Computation", "### 2.2 Spatial Operator Ontology")
sec2_onto = get_block("### 2.2 Spatial Operator Ontology", "### 2.3 Formalization of Spatial Intent")
sec2_sir = get_block("### 2.3 Formalization of Spatial Intent: Conceptual Unification of SIR and CSIR", "### 2.4 Spatial Distance Computation")
sec2_dist = get_block("### 2.4 Spatial Distance Computation: Native In-Database Function (`ST_Distance_Sphere`) vs Topological Routing", "### 2.5 Dataset Provenance")
sec3_val = get_block("### 3.2 Six-Dimensional SIR Validation Algorithm and the No Intent Alteration Principle", "### 3.3 Role of System Prompt")
sec3_comp = get_block("### 3.4 Deterministic Spatial Query Compiler & Safety Invariants", "### 3.5 Strict Grounding Contract")
sec3_grnd = get_block("### 3.5 Strict Grounding Contract and Post-Generation Algorithmic Validator", "## 4. EMPIRICAL RESULTS AND DISCUSSION")

sec3_parts = [
    "## 3. METHODOLOGY\n",
    "### 3.1 Cognitive-Computational Decoupling: The Tripartite Correctness Framework\n" + sec2_framework + "\n\n" + sec2_decoupling + "\n",
    "### 3.2 Formalization of Spatial Intent: Conceptual Unification of Raw SIR (17 Attributes) vs. Validated CSIR (19 Attributes)\n" + sec2_sir + "\n",
    "### 3.3 Spatial Operator Ontology and Deterministic Entity Resolution\n" + sec2_onto + "\n",
    "### 3.4 Six-Dimensional SIR Validation Algorithm (SirValidator) and No Intent Alteration Principle\n" + sec3_val + "\n",
    "### 3.5 Deterministic Spatial Query Compilation and ST_Distance_Sphere Evaluation\n" + sec2_dist + "\n\n" + sec3_comp + "\n",
    "### 3.6 Strict Grounding Contract and Algorithmic Grounding Validator\n" + sec3_grnd
]
sec3_out = "\n".join(sec3_parts)

# SECTION 4: SYSTEM IMPLEMENTATION
sec3_evol = get_block("### 3.1 Architectural Evolution: From Three-Tier Web GIS to Five-Layer Semantic-Controlled Web GIS", "### 3.2 Six-Dimensional SIR Validation")
sec2_prov = get_block("### 2.5 Dataset Provenance and Spatial Ground Truth Specification", "## 3. SYSTEM ARCHITECTURE AND METHODOLOGY")
sec4_prov_detail = get_block("#### 4.2.3 Data Provenance and Scientific Scope Boundaries of the 22 Tourism POI Dataset", "### 4.3 Spatial Failure Taxonomy")
sec3_trace = get_block("#### 3.3.2 Concrete End-to-End System Execution Trace (The Complete 8-Step Trace)", "### 3.4 Deterministic Spatial Query Compiler")
sec4_ui = get_block("### 4.1 System Implementation and Dual-Synchronized Interface", "### 4.2 Empirical Benchmark Performance")

sec4_parts = [
    "## 4. SYSTEM IMPLEMENTATION\n",
    """### 4.1 Minimum Reproducible Components
To guarantee full empirical reproducibility, the system implementation is constructed on an entirely open-source technology stack with zero proprietary vendor lock-in. The minimum reproducible components comprise four decoupled core software modules:
1. **Data Transfer Object (DTO) `SpatialIntent`:** An object-oriented PHP 8.2 domain class encapsulating the lifecycle transitions from the 17-slot Raw SIR (`toRawSirArray()`) to the 19-attribute canonical CSIR (`toCsirFlatArray()`).
2. **Invariant Engine `SirValidator`:** An independent deterministic validation module executing six-dimensional schema, type, coordinate, operator, temporal/budget, and scope boundary checks under the *No Intent Alteration* principle prior to database compilation.
3. **Query Synthesizer `SpatialQueryCompiler`:** A non-LLM SQL compilation engine that translates validated CSIR objects into parameterized prepared SQL statements, binding reference coordinates directly to MySQL 8.0's native spherical function `ST_Distance_Sphere`.
4. **Evidence Verifier `GroundingValidator`:** A post-generation algorithmic regex parser auditing destination entities, ticket pricing, opening schedules, and proximity assertions against relational database facts with a deterministic fail-closed fallback.
""",
    "### 4.2 Spatial Relational Database Model (Normalized 3NF and Session Auditing)\n" + sec3_evol + "\n",
    "### 4.3 Data Curation and Corpus Provenance of Padang Tourism POIs\n" + sec2_prov + "\n\n" + sec4_prov_detail + "\n",
    "### 4.4 Dual-Synchronized User Interface Architecture and Digital Map Integration\n" + sec4_ui + "\n",
    "### 4.5 The Complete 8-Step Trace (Concrete End-to-End System Execution Trace)\n" + sec3_trace
]
sec4_out = "\n".join(sec4_parts)

# SECTION 5: EXPERIMENTAL DESIGN
sec5_parts = [
    "## 5. EXPERIMENTAL DESIGN\n",
    """### 5.1 Benchmark Dataset and Ground Truth Specification
Empirical validation was performed over a standardized benchmark corpus consisting of **40 standardized conversational scenarios** reflecting the full spectrum of urban tourist requirements across 8 query taxonomies:
1. *Single-attribute spatial queries* (e.g., nearest beach from current position).
2. *Multi-criteria spatial & operational queries* (radius, free admission, and active opening schedule).
3. *Entity lookup & alias resolution* (specific POI names, partial names, or local spelling variants).
4. *Relative spatial references* (attractions relative to another landmark, such as *"culinary spots near Adityawarman Museum"*).
5. *Numerical boundary cases* (0 km radius, upper boundary 50 km, budget exactly matching ticket prices).
6. *Circadian & midnight temporal constraints* (24-hour operations or late-night venues open after 20:00).
7. *Negative & out-of-scope requests* (requests outside Padang City or non-tourism domains).
8. *Conversational chit-chat & greetings* (conversational interactions without spatial intent).

Each benchmark scenario is paired with a dual ground truth specification: (a) *Gold-Standard Raw SIR* (17 intent slots), and (b) *Gold-Standard CSIR* (19 canonical attributes with resolved WGS84 spatial coordinates).
""",
    """### 5.2 Baseline Systems
To evaluate scientific significance and isolate the architectural contributions, the proposed system was benchmarked against four representative baselines:
* **Baseline 1 (Direct Text-to-SQL):** The LLM directly generates raw SQL statements from table DDL definitions without intermediate SIR abstraction or deterministic validation.
* **Baseline 2 (Unconstrained LLM with System Prompting):** The LLM generates natural language recommendations directly from general pre-trained knowledge without database grounding (*zero-shot ungrounded generation*).
* **Baseline C (Vector RAG):** Dense-vector embedding retrieval over document summaries of tourist attractions using cosine similarity.
* **Baseline D (DTExplorer - Afnarius et al., 2026 [2]):** Conventional Web GIS utilizing dropdown menus, radius sliders, and static SQL queries without conversational intelligence.
""",
    """### 5.3 Model Configurations and Server Computing Environment
* **AI Foundation Models:** DeepSeek-V3 (`deepseek-chat`) and Google Gemini (`gemini-2.5-flash`), configured with deterministic temperature T = 0.0, top_p = 1.0, max_tokens = 300 under structured JSON output mode.
* **Server Environment:** Linux Ubuntu 22.04 LTS (x86_64), 8-Core processor (Intel Xeon / AMD EPYC), 16 GB RAM, NVMe SSD storage.
* **Software Stack:** PHP 8.2.27, CodeIgniter 4.6.0 framework, MySQL 8.0.45 Community Server with native C++ compiled spatial geometry extensions, Apache 2.4.52.
* **Client Environment:** Chromium-based browser with Leaflet.js 1.9.4 and vanilla responsive CSS.
""",
    """### 5.4 Ablation Study Design (Configurations A1–A6 and B1–B2)
To isolate and quantify the specific contribution of each architectural component, eight systematic ablation configurations were executed:
* **Semantic Control Boundary Ablations (A1–A6):**
  - **A1:** Disabling schema and data-type validation (Dimension 1).
  - **A2:** Disabling Padang WGS84 bounding-box spatial boundary enforcement (Dimension 2).
  - **A3:** Disabling operator consistency and radius clamping (Dimension 3).
  - **A4:** Disabling reference landmark coordinate resolution (Dimension 4).
  - **A5:** Disabling operational consistency for pricing and temporal schedules (Dimension 5).
  - **A6:** Disabling domain ontology and out-of-scope validation (Dimension 6).
* **Evidence Control Boundary Ablations (B1–B2):**
  - **B1:** Disabling spatial fallback policies (dynamic radius expansion).
  - **B2:** Disabling the *Algorithmic Claim-Level Grounding Validator*.
""",
    """### 5.5 Multi-Layer Evaluation Metrics (Layers A–D)
System performance was evaluated across four orthogonal assessment layers:
* **Layer A (Semantic Intent Extraction):** *Exact CSIR Match Rate* (percentage of scenarios exactly matching ground truth across all 19 canonical attributes), *Execution Envelope Alignment* (post-policy execution envelope match), *Mean Field-Level Accuracy* (attribute-level accuracy across 758 evaluations), and *Validation Decision Accuracy*.
* **Layer B (Spatial Execution & Security):** *Pure Spatial Predicate Correctness* (percentage of spatial queries executed without predicate distortion, N=36), *Overall Scenario Execution Compliance* (N=40), and *Database Query Execution Latency*.
* **Layer C (Factual Grounding & Integrity):** *Entity Fabrication Rate* (percentage of scenarios generating non-existent destinations), *Claim-Level Grounding Fidelity* (CGF, percentage of audited factual claims verified by database facts across 4 sub-dimensions), *Entity Grounding Fidelity* (EGF, valid POI mention ratio), and *Honest Rejection Rate* (HRR, rejection of out-of-scope requests).
* **Layer D (Human-Centered Usability & Cognitive Efficiency):** *Task Completion Time* (TCT in seconds) and *System Usability Scale* (SUS composite score, 0–100 scale).
""",
    """### 5.6 Replicability Protocol and Deterministic Testing (N=120 Runs)
All empirical evaluations were conducted under standardized protocols with 3 independent replications per scenario (40 scenarios x 3 = 120 executions). The evaluation framework supports two execution modes:
1. **Standardized Replay Mode (`--mock` / default):** Offline deterministic evaluation using frozen baseline model inferences, verifying all architectural invariants and executing real queries against local MySQL 8.0 `geo_db` to guarantee *bit-exact offline reproducibility*.
2. **Live API Mode (`--live`):** Dynamic online inference via live cloud endpoints.

All evaluation logs, environment configurations, composer dependency lockfiles, and SHA-256 integrity hashes are permanently cataloged in `benchmark/reproducibility/` verified by `SHA256SUMS.txt`."""
]
sec5_out = "\n".join(sec5_parts)

# SECTION 6: RESULTS
sec4_res = get_block("### 4.2 Empirical Benchmark Performance", "#### 4.2.3 Data Provenance")
sec4_fail = get_block("### 4.3 Spatial Failure Taxonomy (F1–F8) and Edge Case Analysis", "### 4.4 Multi-Baseline Comparative Analysis")
sec4_base = get_block("### 4.4 Multi-Baseline Comparative Analysis", "### 4.5 Ablation Study")
sec4_ablat = get_block("### 4.5 Ablation Study", "### 4.6 End-to-End Latency Profile")
sec4_lat = get_block("### 4.6 End-to-End Latency Profile", "### 4.7 Scalability Stress Test on Massive Spatial POIs")
sec4_scale = get_block("### 4.7 Scalability Stress Test on Massive Spatial POIs", "### 4.8 Secondary Evaluation")
sec4_usab = get_block("### 4.8 Secondary Evaluation: Human-Centered Usability and Conversational Interaction (SUS & Cognitive Task Efficiency)", "### 4.9 Spatial Transferability")

sec6_parts = [
    "## 6. RESULTS\n",
    "### 6.1 Empirical Benchmark Performance (Layers A–C)\n" + sec4_res + "\n",
    "### 6.2 Multi-Baseline Comparative Analysis\n" + sec4_base + "\n",
    "### 6.3 Ablation Study Results and Pairwise Comparison\n" + sec4_ablat + "\n",
    "### 6.4 5-Stage Latency Profile and Massive Spatial Query Stress Test\n" + sec4_lat + "\n\n" + sec4_scale + "\n",
    "### 6.5 Usability Evaluation and Cognitive Task Efficiency (SUS & TCT)\n" + sec4_usab + "\n",
    """### 6.6 Automated Test Suite Verification (45 Tests, 172 Assertions, 100% PASS)
The structural integrity of the architecture was verified via an automated PHPUnit regression test suite. The suite comprises **45 unit and integration tests** yielding **172 assertions** testing:
* Spherical distance calculation consistency against real coordinates of the 22 POIs (`SpatialDatabaseIntegrationTest`, 6 tests, 33 assertions, 100% pass).
* `GroundingValidator` robustness across edge-case temporal formats, POI aliases, numeric ambiguity, negative claims, missing facts, and unstructured responses (`GroundingValidatorTest`, 16 tests, 65 assertions, 100% pass).
* Compiler security invariants against diverse SQL injection payloads (`SpatialQueryCompilerTest`, 100% pass).
* Strict compliance with 6-dimensional validation rules under the *No Intent Alteration* principle (`SirValidatorTest`, 100% pass).

All 45 automated tests passed with a 100% success rate (*zero failures, zero errors*), establishing production-grade software stability.
""",
    "### 6.7 Spatial Failure Taxonomy (F1–F8) and Edge Case Analysis\n" + sec4_fail + "\n",
    """#### Isolated Case Deviation Analysis on Benchmark Scenarios
Across the 40 evaluated benchmark scenarios, five isolated non-fatal deviations were observed during initial LLM extraction before being safely resolved by system policies:
1. **Scenario S03 (Category Ambiguity vs. Specific Landmark - F1):** The user inquired about historical collections without naming a specific museum. The LLM extracted `category = 'Museum'` without `target_name`. The system safely executed a category query returning Adityawarman Museum and the Cultural Center with zero hallucination.
2. **Scenario S13 (POI Name Alias Resolution - F3):** The user specified *"Kawasan Kota Tua Padang"*, whereas the database registered *"Kota Tua Padang (Muaro)"*. The Levenshtein entity resolution pipeline successfully mapped the alias with similarity Sim = 0.88 >= 0.75, extracting accurate database facts.
3. **Scenario S16 (Zero-Fare Assertion on Public Bridge - F7 Mitigation):** The grounded NLG synthesized a statement that Siti Nurbaya Bridge requires no entrance fee (Rp0). `GroundingValidator` confirmed that `ticket_price = 0` was registered in the database for the public bridge facility, verifying the claim as true.
4. **Scenario S17 (Cultural Center Diction Variation - F3):** The user asked for *"Taman Budaya Padang"*. The system detected phonetic proximity to *"Gedung Kebudayaan Sumbar"* and prompted user confirmation via the `clarify_user` policy, preventing erroneous data retrieval.
5. **Scenario S30 (Complex Descriptive Query - F2):** The user submitted a query seeking scenic hilltop views at night. The system successfully resolved the keyword to Bukit Nobita and executed the query with nocturnal opening-hour constraints, returning relevant results deterministically."""
]
sec6_out = "\n".join(sec6_parts)

# SECTION 7: DISCUSSION
sec4_9 = get_block("### 4.9 Spatial Transferability, OSRM Service Provenance, and System Limitations", "## 5. CONCLUSION AND FUTURE WORK")
sec4_9_p1 = get_block("**1. Geographic Portability with Limited Domain-Specific Reconfiguration:**", "**2. Positioning of OSRM Service", sec4_9)
sec4_9_p2 = get_block("**2. Positioning of OSRM Service and External Computation Boundaries:**", "", sec4_9)

sec7_parts = [
    "## 7. DISCUSSION\n",
    """### 7.1 Mechanisms of Success: Why the Layered Control Architecture Succeeds
The complete elimination of destination hallucinations (*0.00% Entity Fabrication Rate*) and the 100.00% spatial predicate correctness achieved by the architecture stem directly from the principle of *Separation of Responsibilities*:
1. **Cognitive Air-Gap (Preventing Direct Database Access):** By prohibiting the LLM from generating raw SQL strings or interacting directly with database tables, all syntax failures, schema hallucinations, and SQL injection vectors are architecturally eliminated. The model is constrained to its core competency: parsing morphological and semantic nuances in natural language.
2. **Non-LLM Deterministic Validation:** Unlike self-correction approaches where an LLM is tasked with auditing its own output (often reproducing its own biases), validation in this architecture is executed by an independent non-LLM module (*6D SirValidator*). Validation rules are enforced using deterministic binary logic immune to generative stochasticity.
3. **Firewall-Protected Post-Generation Evidence Grounding:** The algorithmic *Claim-Level Grounding Validator* ensures that the generative model cannot introduce fictitious attributes. Any entity mention, pricing assertion, or spatial claim absent from the verified relational fact set $F$ triggers deterministic filtering or fallback suppression before reaching the user.
""",
    """### 7.2 Latency Trade-offs and Computational Efficiency
Introducing structured semantic validation and post-generation grounding raises questions regarding computational overhead. The latency profile (Table 8) demonstrates that the total deterministic computational overhead introduced by *SirValidator* (0.42 ms) and *GroundingValidator* (0.81 ms) is a mere **1.23 ms**—representing less than **0.1%** of the total server-side response latency (1,252.17 ms).

Conversely, over **93% of the total latency** is consumed by cloud network transit and LLM inference across the two API calls (Call #1 for SIR extraction: 465.12 ms; Call #2 for grounded NLG narrative generation: 785.42 ms). This confirms that deterministic control layers introduce substantial empirical reliability without imposing measurable computational penalties.
""",
    "### 7.3 Generalization Boundaries and Geographic Portability\n" + sec4_9_p1 + "\n",
    """### 7.4 Scientific Progression Beyond Prior Art (DTExplorer)
The proposed architecture directly resolves the key research limitations articulated by Afnarius et al. (2026) in *DTExplorer* [2]:
* **Interaction Modality:** *DTExplorer* constrained users to WIMP dropdown menus and radius sliders, inducing substantial cognitive friction. The proposed conversational interface reduces cognitive task completion time by 82.43% (Table 10).
* **Spatial Computation Model:** *DTExplorer* relied on planar Euclidean approximations that induce latitude distortion. This study transitioned to native MySQL 8.0 `ST_Distance_Sphere`, computing great-circle distances directly on the database kernel in 1.21 ms.
* **Dynamic Multi-Criteria Filtering:** *DTExplorer* lacked support for temporal opening hours or admission budgets. The proposed system natively coordinates `open_now`, `open_24h`, `max_price`, and `is_free` predicates within a single unified query execution pass.
* **Millisecond-Level Profiling & Standardized Usability:** Fulfilling the explicit research recommendations of Afnarius et al. (2026), this paper provides full millisecond-level execution latency breakdowns and standardized System Usability Scale evaluations (SUS = 84.25 ± 6.80, Grade A) across 30 empirical participants."""
]
sec7_out = "\n".join(sec7_parts)

# SECTION 8: THREATS TO VALIDITY AND LIMITATIONS
sec8_parts = [
    "## 8. THREATS TO VALIDITY AND LIMITATIONS\n",
    """### 8.1 Internal Validity
Threats to internal validity concern potential bias within prompt engineering and benchmark scenario curation:
* **Prompt Sensitivity and Dialect Variation:** Although the 40 benchmark scenarios encompass 8 query taxonomies, localized Minangkabau colloquialisms or colloquial slang variants might exhibit differing extraction performance. This is mitigated by synonym mapping dictionaries and keyword expansion rules embedded within system prompts.
* **Model Inference Stability:** While setting temperature T = 0.0 enforces deterministic inference, underlying foundational model API updates may subtly alter latent space interpretations. Structured JSON schemas and canonical CSIR constraints minimize this exposure.
""",
    """### 8.2 External Validity
Threats to external validity concern the generalizability of findings beyond the experimental environment:
* **Destination Catalog Scale:** Primary evaluations focused on 22 curated destinations in Padang City. While the synthetic 10,000-point scalability stress test (Table 9) confirmed database indexing efficiency (latency 6.11 ms), deploying in megacities with tens of thousands of active POIs may introduce new challenges in name disambiguation and cartographic marker clustering.
* **Administrative Jurisdictions:** The system is optimized for city-scale municipal jurisdictions (694.96 km²). Regional multi-province corridors will require hierarchical spatial partitioning.
""",
    """### 8.3 Construct Validity
Threats to construct validity concern the alignment between measured metrics and underlying theoretical constructs:
* **Regex-Based Grounding Validator Scope:** The 100.00% Claim-Level Grounding Fidelity metric applies strictly to claims detectable by the regex parser across four defined categories (destinations, pricing, schedules, and proximity). Open-ended qualitative descriptive assertions require human-in-the-loop validation for exhaustive audit.
* **Cognitive Task Efficiency (TCT):** Participant typing habits and smartphone reading proficiencies may affect recorded completion times, although balanced Latin-Square counterbalancing designs were employed to neutralize ordering bias.
""",
    "### 8.4 External Service Dependencies and Fault Tolerance\n" + sec4_9_p2
]
sec8_out = "\n".join(sec8_parts)

# SECTION 9: CONCLUSION AND FUTURE WORK
sec9_fut = get_block("Future work will focus on", "## REFERENCES", src[src.find("## 5. CONCLUSION"):])

sec9_parts = [
    "## 9. CONCLUSION AND FUTURE WORK\n",
    """### 9.1 Conclusion (Answering Research Questions RQ1–RQ4)
This study designed, implemented, and empirically evaluated a **Reliability-Controlled Conversational Spatial Information System** across 22 curated tourism destinations in Padang City. The four core research questions are conclusively resolved:
1. **Answer to RQ1 (Semantic Parsing Fidelity):** Quarantining the LLM behind formal schema contracts enabled the extraction of user spatial intent with an Exact CSIR semantic accuracy of **87.50%** (35/40), an execution envelope alignment of **90.00%** (36/40), and an average field-level accuracy of **98.62% (748/758)**. Enforcing the *No Intent Alteration* principle prevented unauthorized silent parameter mutations.
2. **Answer to RQ2 (Spatial Execution Safety & Correctness):** The 6-dimensional validator and parameterized query compiler maintained a 100.00% safety invariant enforcement (zero unauthorized queries or SQL injections). Great-circle spherical distance evaluation via native MySQL 8.0 `ST_Distance_Sphere` achieved **100.00% Pure Spatial Predicate Correctness** (36/36) and 100.00% scenario compliance (40/40) with sub-two-millisecond database execution latency (**1.21 ms**).
3. **Answer to RQ3 (Factual Grounding & Zero Fabrication):** The post-generation algorithmic proof firewall (*Claim-Level Grounding Validator*) successfully reduced the **Entity Fabrication Rate to 0.00%** (zero fabricated attractions across all evaluated scenarios), compared to a 35.00% fabrication rate in unconstrained LLMs. The system achieved **100.00% Claim-Level Grounding Fidelity (270/270 claims)**, **100.00% Entity Grounding Fidelity (120/120 mentions)**, and a **100.00% Honest Rejection Rate (2/2)** on out-of-scope requests.
4. **Answer to RQ4 (Cognitive Efficiency & Usability):** Guided conversational interaction significantly outperformed conventional WIMP interfaces, **reducing cognitive Task Completion Time (TCT) by 82.43%** (from 37.11 s to 6.52 s, p < 0.001, Cohen's d = 5.19) while securing an "Excellent" **System Usability Scale (SUS) score of 84.25 ± 6.80 (Grade A)**. Architectural robustness was corroborated by **45 automated unit and integration tests (172 assertions, 100% PASS)**.
""",
    "### 9.2 Future Research Directions\n" + sec9_fut
]
sec9_out = "\n".join(sec9_parts)

# ASSEMBLE FULL DOCUMENT
references_and_appendix = src[src.find("## REFERENCES"):].strip()

full_doc = f"""{header_abstract}

---

{sec1_out}

---

{sec2_out}

---

{sec3_out}

---

{sec4_out}

---

{sec5_out}

---

{sec6_out}

---

{sec7_out}

---

{sec8_out}

---

{sec9_out}

---

{references_and_appendix}
"""

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(full_doc)

print(f"[✓] Successfully generated restructured English draft: {len(full_doc)} characters.")
