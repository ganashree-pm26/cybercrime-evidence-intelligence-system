import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.intent_detector import IntentDetector
from services.embedding_service import EmbeddingService
from services.risk_scorer import RiskScorer
from services.entity_analyzer import EntityAnalyzer
from utils.similarity import SimilarityFinder
import time
from datetime import datetime

class IntelligenceProcessor:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.embedding_service = EmbeddingService()
        self.risk_scorer = RiskScorer()
        self.entity_analyzer = EntityAnalyzer()
        self.similarity_finder = SimilarityFinder()

    def process_intelligence(self, input_json: dict) -> dict:
        start_time = time.time()

        # Extract fields from input
        raw_text = input_json["raw_text"]
        entities = input_json["entities"]

        # Detect intent
        intent = self.intent_detector.detect(raw_text)

        # Generate embedding
        embedding = self.embedding_service.generate_embedding(raw_text)

        # Calculate risk score
        risk_assessment = self.risk_scorer.calculate_score(
            intent["confidence"], entities, raw_text
        )

        # Analyze entity insights
        entity_insights = self.entity_analyzer.analyze(entities, raw_text)

        # Processing time
        processing_time = round(time.time() - start_time, 2)

        # AI metadata
        ai_metadata = {
            "model": "distilbert",
            "embedding_model": "all-MiniLM-L6-v2",
            "processing_time": f"{processing_time}s",
            "version": "1.0"
        }

        # Extend original JSON
        output = input_json.copy()
        output.update({
            "intent": intent,
            "risk_assessment": risk_assessment,
            "embedding": embedding,
            "entity_insights": entity_insights,
            "ai_metadata": ai_metadata
        })

        return output