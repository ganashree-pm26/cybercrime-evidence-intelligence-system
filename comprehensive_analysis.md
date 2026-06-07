# NexusIQ: Comprehensive Technical Architecture & Analysis
*A Deep-Dive System Analysis for IEEE/Springer Research Publications*

## 1. Complete Architecture Understanding
NexusIQ is an end-to-end Cybercrime Digital Evidence Intelligence System. It follows a multi-tiered, service-oriented architecture (SOA) bridging high-performance backend processing, machine learning intelligence, graph-based link analysis, and an interactive front-end workspace.

### System Tiers
1. **Frontend (Presentation Tier):** Built with React, Vite, and TailwindCSS. It provides the interactive workspaces (dashboard, interactive Cytoscape.js link analysis, geospatial map, timeline, and watchlists).
2. **Backend (API & Orchestration Tier):** A Python FastAPI server. It acts as the orchestration layer, handling multi-part file uploads, chain of custody, and coordinating the pipeline modules.
3. **AI Intelligence Engine (Compute Tier):** An isolated pipeline (`person2_ai_engine`) dedicated to NLP, intent detection via DistilBERT, embedding generation (SentenceTransformers `all-MiniLM-L6-v2`), and heuristic risk scoring.
4. **Graph Engine (Data Tier):** Interfaces with a Neo4j Aura cloud database to model complex relationships (Nodes/Edges) for fraud ring detection and network analysis.
5. **Storage Layer:** Local state JSONs (`output/`, `pipeline_test_results.json`, `audit_events.json`) for persistence, ensuring fallback capabilities and asynchronous graph reconciliation.

---

## 2. Workflow and Pipeline Explanation

### End-to-End Pipeline
1. **Ingestion & Chain of Custody:** The user uploads unstructured text evidence (e.g., a phishing email or scam message) via the frontend. The backend (`routes.py`) receives this, assigns a UUID, and immediately hashes the content (SHA-256) to establish forensic integrity.
2. **Text Parsing & Normalization:** `EvidenceProcessor` extracts the raw text and passes it to `TextPreprocessor` for sanitization.
3. **Hybrid Entity Extraction:** `RegexEntityExtractor` (IoCs like Wallets, Phones, URLs) and `NLPEntityExtractor` (Named Entities) run in parallel. Results are merged and de-duplicated.
4. **Intelligence Processing:** The data is pushed to `IntelligenceProcessor`, which triggers:
   - **Intent Detection:** Classifies the text into categories (e.g., `investment_scam`).
   - **Vector Embeddings:** Generates a 384-dimensional dense vector.
   - **Risk Scoring:** Assigns a 0-100 score based on entities and trigger words.
5. **Graph Ingestion:** The structured metadata (Entities, Risk, Intent) is ingested into Neo4j via `process_case`. Nodes for the case and specific entities are created, and `RELATED_TO` edges are mapped.
6. **Network Analysis & Alerting:** Neo4j computes Jaccard Similarity across case entities to find connected cases and fraud rings, updating the graph's network risk levels.

---

## 3. Frontend/Backend Flow & APIs

- **`POST /evidence/upload`**: The critical entry point. It accepts multipart files, runs the full processing pipeline synchronously, and immediately triggers Neo4j ingestion.
- **`GET /cases/list`**: Fetches all cases. Interestingly, the backend reconciles Neo4j graph data with local file metadata (`_ensure_case_analysis`) before returning, ensuring the frontend always sees the materialized ML state.
- **`GET /evidence/results/{case_id}`**: Retrieves processed evidence from the `output/` directory, exposing extracted entities.
- **`GET /graph/{case_id}` (Inferred)**: Fetches the Cytoscape JSON payload representing the localized subgraph around a specific case.

**Hidden Design Decision:** The system utilizes a "Reconciliation Loop" (`_ensure_case_analysis`). If graph ingestion fails during upload, the API can backfill missing ML/Graph data during subsequent page loads, making the system highly fault-tolerant.

---

## 4. Neo4j Graph Workflow

The Graph workflow fundamentally shifts analysis from tabular data to interconnected networks.
- **Node Topology:** 
  - `(:Case {id, risk_score, intent})`
  - `(:Entity {type, value})` (e.g., `type: 'wallet'`, `value: '1BvBM...'`)
- **Edge Topology:** 
  - `(:Case)-[:RELATED_TO]->(:Entity)`
- **Fraud Detection Logic:** By leveraging graph traversals (e.g., Cypher queries matching `(c1:Case)-[:RELATED_TO]->(e:Entity)<-[:RELATED_TO]-(c2:Case)`), the system identifies shared infrastructure.
- **Jaccard Similarity:** Used for Case Linking. It measures the intersection of entities between two cases divided by their union. If similarity > threshold, a `[:SIMILAR_TO]` edge is explicitly drawn between cases.
- **Graph Clustering:** Dense subgraphs (fraud rings) are detected using community detection algorithms, allowing the system to aggregate the "Threat Level" of an entire organized group.

---

## 5. Entity Extraction & Fraud Detection Logic

- **Extraction:** Relies on deterministic regex for high-fidelity indicators (Cryptocurrency addresses, Emails) and probabilistic NLP for complex entities (Names, Organizations).
- **Rule-based Risk Scoring (`_derive_intelligence_from_processed`):**
  - Uses weighted heuristics: `wallet_count * 25 + url_count * 15 + urgency_hits * 6`.
  - Maps to discrete levels (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
  - **Strengths:** Highly transparent and explainable (crucial for legal evidence).

---

## 6. Semantic Search & Embeddings

- **Workflow:** When an investigator searches "Send Bitcoin for guaranteed returns", `SimilarityFinder` (`person2_ai_engine/utils/similarity.py`) converts this query into a 384-dimensional vector using `all-MiniLM-L6-v2`.
- **Retrieval:** It computes the Cosine Similarity against all historical case embeddings stored in memory/disk.
- **Research Relevance:** This represents a leap over traditional keyword search (e.g., Elasticsearch). It allows investigators to find structurally similar Modus Operandi (M.O.) even if the scammers change the specific wording, wallet addresses, or names.

---

## 7. Geospatial and IP Intelligence Possibilities

While the current codebase focuses on logical entities (Wallets, URLs), the architecture easily supports Geospatial expansions:
- **IP Extraction & Geo-projection:** Extracting IP addresses via Regex, calling a GeoIP database, and creating `(:Location {lat, long})` nodes in Neo4j.
- **Spatial Queries:** Investigators could run geospatial graph queries to find cases originating within a 50km radius.
- **Implementation in NexusIQ:** The frontend already has a `Geospatial projection` feature noted in the README, implying coordinate-based rendering of extracted physical locations.

---

## 8. Module & File Breakdown

1. **`backend/app/api/routes.py`**
   - *Role:* API Gateway & Orchestrator.
   - *I/O Flow:* HTTP JSON/Multipart In -> Python Dict -> HTTP JSON Out.
   - *Research Relevance:* Demonstrates state reconciliation between local file storage and graph DBs.
2. **`backend/app/services/evidence_processor.py`**
   - *Role:* Parsing & Entity Pipeline.
   - *I/O Flow:* Raw bytes -> Structured `ProcessedOutput` JSON.
   - *Research Relevance:* Highlights the importance of deterministic hashing (chain of custody) combined with probabilistic NLP.
3. **`backend/person2_ai_engine/pipeline/intelligence_processor.py`**
   - *Role:* ML integration layer.
   - *I/O Flow:* Structured Entities & Text -> Text Embeddings, Intent Labels, Risk Scores.
   - *Research Relevance:* The core AI logic enabling semantic understanding.
4. **`backend/Graph_engine/Graph_engine/db.py` & `graph_service.py`**
   - *Role:* Neo4j drivers and business logic.
   - *I/O Flow:* Case/Risk dicts -> Cypher execution -> Status dicts.
   - *Research Relevance:* Graph-based fraud ring detection methodology.

---

## 9. Strengths, Limitations, and Future Scope

### Strengths
- **Explainability (XAI):** The risk scorer outputs exact `reasons` and `trigger_words`, avoiding the "black box" problem of AI in law enforcement.
- **Hybrid Search:** Combines deterministic graph links (exact wallet matches) with probabilistic semantic search (similar M.O.).
- **Fault Tolerance:** Local JSON persistence ensures data is never lost if the cloud Neo4j instance drops.

### Limitations
- **Scalability:** `_load_processed_cases` reads JSON files from disk on every API call. This limits horizontal scalability compared to using a dedicated document DB (like MongoDB).
- **In-Memory Semantic Search:** `SimilarityFinder` loads all embeddings into NumPy arrays. For millions of cases, this requires a vector database (e.g., Milvus, Pinecone).

### Future Scope
- **Temporal Graph Neural Networks (TGN):** Utilizing the timestamps on edges to predict *when* a scammer will act next.
- **Cross-Lingual Embeddings:** Allowing the system to match a scam email in Spanish to a historically similar one in English.

---

## 10. Possible Research Contributions & Publishable Features

If you are writing an IEEE/Springer paper based on this project, focus your core contributions on these areas:

1. **"Hybrid Deterministic-Probabilistic Graph Modeling for Cybercrime Infrastructure Detection"**
   - *Novelty:* Proposing an architecture that combines deterministic IoC extraction (Neo4j Graph Links) with probabilistic semantic embeddings (Cosine Similarity) to detect polymorphic fraud rings that change their infrastructure.
2. **"Explainable AI (XAI) in Automated Digital Forensics"**
   - *Novelty:* Highlighting how the system uses trigger-word mapping and rule-weighted heuristics on top of LLM embeddings to generate legally defensible, explainable risk scores for investigators.
3. **"State-Reconciled Asynchronous Graph Processing in Forensic Architectures"**
   - *Novelty:* Documenting the dual-state architecture (JSON file system + Neo4j) that ensures zero data loss of forensic evidence while allowing complex graph analytics to eventually resolve.
