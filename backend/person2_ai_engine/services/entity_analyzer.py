import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import re

class EntityAnalyzer:
    def __init__(self):
        self.suspicious_contexts = {
            "wallet": ["invest", "send", "transfer", "bitcoin", "crypto"],
            "email": ["contact", "reply", "urgent"],
            "phone": ["call", "urgent", "now"],
            "url": ["click", "visit", "link"]
        }

    def analyze(self, entities: dict, raw_text: str) -> list:
        insights = []
        text_lower = raw_text.lower()

        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                risk = "LOW"
                context = "No suspicious context"

                if entity_type in self.suspicious_contexts:
                    matches = [word for word in self.suspicious_contexts[entity_type] if word in text_lower]
                    if matches:
                        risk = "HIGH" if len(matches) > 1 else "MEDIUM"
                        context = f"Associated with: {', '.join(matches)}"

                insights.append({
                    "entity": entity,
                    "type": entity_type,
                    "risk": risk,
                    "context": context
                })

        return insights