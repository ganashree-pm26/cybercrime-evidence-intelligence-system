import re

class RiskScorer:
    def __init__(self):
        self.urgency_words = ["urgent", "immediate", "now", "quick", "fast", "rush"]
        self.investment_words = ["invest", "return", "profit", "money", "bitcoin", "crypto"]

    def calculate_score(self, intent_confidence: float, entities: dict, raw_text: str) -> dict:
        score = 0
        reasons = []
        trigger_words = []

        # Intent confidence
        if intent_confidence > 0.8:
            score += 30
            reasons.append("High intent confidence")
        elif intent_confidence > 0.6:
            score += 20
            reasons.append("Medium intent confidence")

        # Wallets
        if entities.get("wallets"):
            score += 25 * len(entities["wallets"])
            reasons.append(f"{len(entities['wallets'])} wallet(s) detected")
            trigger_words.extend(entities["wallets"])

        # URLs
        if entities.get("urls"):
            score += 15 * len(entities["urls"])
            reasons.append(f"{len(entities['urls'])} URL(s) detected")
            trigger_words.extend(entities["urls"])

        # Urgency patterns
        urgency_matches = [word for word in self.urgency_words if word in raw_text.lower()]
        if urgency_matches:
            score += 10 * len(urgency_matches)
            reasons.append(f"Urgency language detected ({len(urgency_matches)} instances)")
            trigger_words.extend(urgency_matches)

        # Investment patterns
        invest_matches = [word for word in self.investment_words if word in raw_text.lower()]
        if invest_matches:
            score += 5 * len(invest_matches)
            reasons.append(f"Investment language detected ({len(invest_matches)} instances)")
            trigger_words.extend(invest_matches)

        # Cap score
        score = min(score, 100)

        # Determine level
        if score >= 80:
            level = "CRITICAL"
        elif score >= 60:
            level = "HIGH"
        elif score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "score": score,
            "level": level,
            "reasons": reasons,
            "trigger_words": list(set(trigger_words))
        }