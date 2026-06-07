# Methodology: NexusIQ Digital Evidence Intelligence System

The NexusIQ platform follows a multi-stage, automated intelligence pipeline designed for cybercrime forensics. The architecture is modular, ingesting unstructured digital evidence and transforming it into structured, interconnected, and risk-assessed insights. The methodology is divided into four primary modules: Data Ingestion & Entity Extraction, AI Intelligence Processing, Graph Engine & Network Link Analysis, and Semantic Similarity Search.

## 1. Data Ingestion & Entity Extraction (Module 1)

The first phase of the pipeline focuses on securely ingesting evidence and extracting structured forensic artifacts from raw, unstructured text.

### Techniques Used:
- **Cryptographic Hashing:** Secure Hash Algorithm 256 (SHA-256)
- **Regular Expressions (Regex):** For deterministic pattern matching.
- **Natural Language Processing (NLP):** For contextual entity recognition.
- **Text Normalization:** Standardizing data formats.

### Workflow & Implementation:
1. **Chain of Custody Generation:** Upon ingestion of a digital evidence file (e.g., text document), a unique `CASE-ID` is assigned, and a SHA-256 hash of the content is generated. This ensures cryptographic integrity and establishes a verifiable chain of custody.
2. **Parsing & Normalization:** The file is parsed to extract raw text, which is then cleaned and normalized (e.g., stripping special characters, standardizing case) using a dedicated `TextPreprocessor`.
3. **Hybrid Entity Extraction:** 
   - A `RegexEntityExtractor` scans for highly structured indicators of compromise (IoCs) such as Cryptocurrency Wallets, Phone Numbers, Emails, and URLs.
   - Concurrently, an `NLPEntityExtractor` scans for contextual entities such as Persons/Names.
4. **Entity Merging:** Extracted entities from both extractors are merged, de-duplicated based on confidence scores, and grouped by type. 
5. **Serialization:** The resulting structured data is packaged into a JSON object containing the raw text, the hash, timestamp, and grouped entities, which is then persisted to the local file system (`/output`).

## 2. AI Intelligence Engine (Module 2)

Once the data is structured, it is passed to the AI Intelligence Engine, which determines the overarching intent of the evidence and calculates a risk score.

### Techniques Used:
- **Transformer-based Sequence Classification:** Utilizing models like DistilBERT (`distilbert-base-uncased`).
- **Heuristic Risk Scoring:** Rule-based impact assessment.
- **Vector Embeddings:** Transforming text into high-dimensional numerical representations.

### Workflow & Implementation:
1. **Intent Detection:** The cleaned text is tokenized and fed into a fine-tuned sequence classification model. The model categorizes the text into established cybercrime typologies: `investment_scam`, `romance_scam`, `phishing`, `job_scam`, `impersonation`, or `general_fraud`. The model outputs a classification label alongside a statistical confidence score.
2. **Risk Assessment:** A dedicated module assesses the case's severity. The risk score (0-100) and risk level (LOW, MEDIUM, HIGH, CRITICAL) are computed by combining the extracted entities (e.g., presence of multiple crypto wallets) and the detected intent.
3. **Embedding Generation:** The raw text is passed through an embedding model (e.g., SentenceTransformers) to generate a 384-dimensional dense vector representing the semantic meaning of the evidence.
4. **Insight Aggregation:** The generated intent, risk metrics, embeddings, and entity-specific metadata are appended to the case file and passed downstream.

## 3. Graph Engine & Network Link Analysis (Module 3)

To uncover organized crime rings and interconnected fraud campaigns, the structured case data and entities are ingested into a Neo4j Graph Database.

### Techniques Used:
- **Graph Database Modeling:** Nodes and Edges representation (Neo4j).
- **Jaccard Similarity:** For measuring intersection over union between different cases' entities.
- **Graph-based Clustering:** Detecting dense subgraphs (fraud rings).

### Workflow & Implementation:
1. **Graph Ingestion:** The engine creates dedicated nodes for the `Case` and individual `Entities` (e.g., a specific Bitcoin wallet node or Email node).
2. **Relationship Mapping:** `RELATED_TO` edges are drawn between Case nodes and their respective Entity nodes. 
3. **Cross-Case Linking:** When multiple Case nodes connect to the exact same Entity node (e.g., two different victims reporting the same crypto wallet), the engine automatically detects a shared infrastructure.
4. **Network Risk & Jaccard Similarity:** The engine calculates the Jaccard Similarity between cases to identify highly correlated events. Cases passing a similarity threshold are explicitly linked.
5. **Fraud Ring Detection:** Graph clustering algorithms group interconnected cases into "fraud rings," computing an aggregate threat level and average risk for the entire cluster.
6. **Alert Generation:** High-risk entity sharing triggers automated alerts within the system for investigators.

## 4. Semantic Similarity Search

To facilitate rapid intelligence retrieval, the platform incorporates a semantic search feature that transcends simple keyword matching.

### Techniques Used:
- **Cosine Similarity:** Mathematical measurement of vector alignment in high-dimensional space.

### Workflow & Implementation:
1. **Query Embedding:** When an investigator searches for a concept (e.g., "Send Bitcoin to wallet for guaranteed returns"), the search query is converted into a 384-dimensional vector using the same embedding model used in Module 2.
2. **Similarity Computation:** The system computes the Cosine Similarity between the query vector and the pre-computed embedding vectors of all historical cases.
3. **Retrieval:** The system returns the Top-K matching cases, enabling investigators to find historically similar modus operandi (M.O.) even if the exact keywords or entities differ.

## Summary of Technologies
- **Backend Framework:** FastAPI (Python)
- **Database:** Neo4j (Graph Database), Local JSON state.
- **Machine Learning:** PyTorch, HuggingFace Transformers (DistilBERT).
- **Frontend / Visualization:** React, Cytoscape.js (for interactive graph rendering).
