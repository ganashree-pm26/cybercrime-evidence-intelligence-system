# Person 2: Core Intelligence Engine

This module extends the Data Ingestion system with AI-powered intelligence analysis for cybercrime forensics.

## Features

- **Scam Intent Detection**: Classifies scam types using DistilBERT
- **Embedding Generation**: Creates semantic embeddings for case linking
- **Risk Scoring**: Hybrid scoring based on intent, entities, and patterns
- **Entity Context Analysis**: Analyzes entities in text context
- **Semantic Similarity**: Finds similar cases using cosine similarity

## Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Training the Intent Model

Run the training script in Google Colab:

```python
# In Colab
!pip install transformers torch sklearn pandas
from train_intent_model import train_intent_model
train_intent_model()
```

Then download the `intent_model/` folder and place it in `person2_ai_engine/models/`.

## Usage

```python
from person2_ai_engine.pipeline.intelligence_processor import IntelligenceProcessor

processor = IntelligenceProcessor()

# Input from Person 1 ingestion system
input_data = {
    "case_id": "CASE-20260502-1234",
    "source_file": "chat.txt",
    "entities": {...},
    "raw_text": "Invest now and get rich...",
    "timestamp": "...",
    "hash": "..."
}

# Process intelligence
result = processor.process_intelligence(input_data)

print(result["intent"])  # {"labels": ["investment_scam"], "confidence": 0.91}
print(result["risk_assessment"])  # {"score": 85, "level": "HIGH", ...}
```

## Output Format

The system extends Person 1's output with:

```json
{
  "case_id": "...",
  "source_file": "...",
  "entities": {...},
  "raw_text": "...",
  "timestamp": "...",
  "hash": "...",
  "intent": {
    "labels": ["investment_scam"],
    "confidence": 0.91
  },
  "risk_assessment": {
    "score": 85,
    "level": "HIGH",
    "reasons": ["High intent confidence", "Wallet detected", ...]
  },
  "embedding": [0.123, 0.456, ...],
  "entity_insights": [
    {
      "entity": "1ABC...",
      "type": "wallet",
      "risk": "HIGH",
      "context": "linked to investment request"
    }
  ],
  "ai_metadata": {
    "model": "distilbert",
    "embedding_model": "all-MiniLM-L6-v2",
    "processing_time": "0.45s",
    "version": "1.0"
  }
}
```

## Testing

Run the test script:

```bash
cd person2_ai_engine
python test_engine.py
```

This will demonstrate:
- Intent detection on sample texts
- Risk scoring
- Embedding generation
- Similarity search

## Integration with Person 1

The intelligence engine accepts Person 1's `ProcessedOutput` JSON directly without modification. It only adds new fields for AI insights.