from transformers import pipeline
import random

class IntentModel:
    def __init__(self, model_path: str = None):
        # For demo, use a sentiment analysis pipeline as proxy
        # In production, load your trained model
        if model_path:
            # Load trained model
            from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
            self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
            self.model = DistilBertForSequenceClassification.from_pretrained(model_path)
            self.use_trained = True
        else:
            # Fallback to sentiment analysis for demo
            self.sentiment_pipeline = pipeline("sentiment-analysis")
            self.use_trained = False

        # Scam categories
        self.labels = [
            "investment_scam",
            "romance_scam",
            "phishing",
            "job_scam",
            "impersonation",
            "general_fraud"
        ]

    def predict(self, text: str) -> dict:
        if self.use_trained:
            # Use trained model
            import torch
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(device)
            self.model.eval()

            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
                confidence, predicted_class = torch.max(probabilities, dim=1)

            return {
                "labels": [self.labels[predicted_class.item()]],
                "confidence": round(confidence.item(), 2)
            }
        else:
            # Demo fallback: classify based on keywords
            text_lower = text.lower()
            if "invest" in text_lower or "return" in text_lower or "profit" in text_lower:
                label = "investment_scam"
                confidence = 0.85
            elif "love" in text_lower or "darling" in text_lower or "relationship" in text_lower:
                label = "romance_scam"
                confidence = 0.80
            elif "click" in text_lower or "link" in text_lower or "verify" in text_lower:
                label = "phishing"
                confidence = 0.90
            elif "job" in text_lower or "opportunity" in text_lower or "resume" in text_lower:
                label = "job_scam"
                confidence = 0.75
            elif "irs" in text_lower or "government" in text_lower or "tax" in text_lower:
                label = "impersonation"
                confidence = 0.95
            else:
                label = "general_fraud"
                confidence = 0.60

            return {
                "labels": [label],
                "confidence": confidence
            }