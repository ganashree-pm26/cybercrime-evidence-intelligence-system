import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.intent_model import IntentModel

class IntentDetector:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Load Kaggle Dataset Model
        path_saved = os.path.join(base_dir, "intent_model_saved")
        self.model_saved = IntentModel(model_path=path_saved)
        
        # Load Synthetic Dataset Model
        path_ready = os.path.join(base_dir, "intent_model_ready")
        self.model_ready = IntentModel(model_path=path_ready)

    def detect(self, text: str) -> dict:
        try:
            res1 = self.model_saved.predict(text)
        except Exception as e:
            print(f"Error predicting with public dataset model: {e}")
            res1 = {"labels": [], "confidence": 0.0}
            
        try:
            res2 = self.model_ready.predict(text)
        except Exception as e:
            print(f"Error predicting with ready model: {e}")
            res2 = {"labels": [], "confidence": 0.0}
            
        # Combine labels, remove duplicates
        combined_labels = list(set(res1.get("labels", []) + res2.get("labels", [])))
        
        # Take the maximum confidence between the two models
        combined_confidence = max(res1.get("confidence", 0.0), res2.get("confidence", 0.0))
        
        return {
            "labels": combined_labels,
            "confidence": combined_confidence,
            "ensemble_details": {
                "kaggle_model": res1,
                "synthetic_model": res2
            }
        }