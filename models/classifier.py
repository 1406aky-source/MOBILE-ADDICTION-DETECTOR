"""
Addiction Level Classifier
Implements multi-level classification: Low, Moderate, High, Severe
Uses Bayesian-inspired scoring with statistical decision theory.
"""

import math
import random


class AddictionClassifier:
    """
    Supervised-style multi-class classifier for addiction levels.
    Simulates a trained model using weighted feature scoring.
    Concepts: Supervised Learning, Bayesian Classification, Statistical Decision Theory
    """

    LEVELS = [
        {
            "name": "Low",
            "range": (0, 25),
            "color": "#22c55e",
            "bg": "#dcfce7",
            "emoji": "✅",
            "description": "Healthy usage. You maintain good digital balance.",
        },
        {
            "name": "Moderate",
            "range": (25, 50),
            "color": "#f59e0b",
            "bg": "#fef3c7",
            "emoji": "⚠️",
            "description": "Borderline usage. Some habits need attention.",
        },
        {
            "name": "High",
            "range": (50, 75),
            "color": "#f97316",
            "bg": "#ffedd5",
            "emoji": "🚨",
            "description": "High addiction risk. Intervention recommended.",
        },
        {
            "name": "Severe",
            "range": (75, 100),
            "color": "#ef4444",
            "bg": "#fee2e2",
            "emoji": "🔴",
            "description": "Severe addiction. Immediate action required.",
        },
    ]

    # Feature weights (simulated trained model coefficients)
    WEIGHTS = {
        "daily_hours": 0.35,
        "late_night_usage": 0.20,
        "app_switch_rate": 0.15,
        "social_media_ratio": 0.12,
        "productivity_ratio": -0.15,  # negative = reduces risk
        "study_app_ratio": -0.10,
        "weekend_spike": 0.08,
        "notification_clicks": 0.05,
    }

    # Bayesian prior probabilities (base rates from population data)
    PRIORS = {
        "Low": 0.35,
        "Moderate": 0.30,
        "High": 0.22,
        "Severe": 0.13,
    }

    def classify(self, features: dict) -> dict:
        """Classify addiction level from extracted features."""
        raw_score = self._compute_raw_score(features)
        bayesian_score = self._apply_bayesian_update(raw_score, features)
        score = max(0, min(100, bayesian_score))

        level_info = self._get_level(score)
        probabilities = self._compute_class_probabilities(score)
        confidence = self._compute_confidence(features, score)
        key_factors = self._identify_key_factors(features)

        return {
            "level": level_info["name"],
            "score": round(score, 1),
            "color": level_info["color"],
            "bg": level_info["bg"],
            "emoji": level_info["emoji"],
            "description": level_info["description"],
            "probabilities": probabilities,
            "confidence": round(confidence, 1),
            "key_factors": key_factors,
        }

    def _compute_raw_score(self, features: dict) -> float:
        """Compute weighted linear score (linear model layer)."""
        score = 0.0

        # Daily hours component (0-100 mapping)
        daily_hours = features.get("daily_hours", 0)
        # Normalize: 0h→0, 10h→100
        score += (daily_hours / 10.0) * 100 * self.WEIGHTS["daily_hours"]

        # Late night usage (0-1 probability → 0-100)
        score += features.get("late_night_usage", 0) * 100 * self.WEIGHTS["late_night_usage"]

        # App switch rate (normalize: 0-30 range → 0-100)
        switch_rate = min(features.get("app_switch_rate", 0), 30)
        score += (switch_rate / 30) * 100 * self.WEIGHTS["app_switch_rate"]

        # Social media ratio (0-1 → 0-100)
        score += features.get("social_media_ratio", 0) * 100 * self.WEIGHTS["social_media_ratio"]

        # Protective factors (reduce score)
        score += features.get("productivity_ratio", 0) * 100 * self.WEIGHTS["productivity_ratio"]
        score += features.get("study_app_ratio", 0) * 100 * self.WEIGHTS["study_app_ratio"]

        # Weekend spike
        score += features.get("weekend_spike", 0) * 100 * self.WEIGHTS["weekend_spike"]

        # Notification behavior
        notif = min(features.get("notification_clicks", 0), 100)
        score += (notif / 100) * 100 * self.WEIGHTS["notification_clicks"]

        return score

    def _apply_bayesian_update(self, raw_score: float, features: dict) -> float:
        """Apply Bayesian posterior update based on behavioral evidence."""
        # Evidence strength: hours > threshold increases posterior
        evidence_multiplier = 1.0
        if features.get("daily_hours", 0) > 7:
            evidence_multiplier *= 1.15
        if features.get("sleep_hours", 8) < 6:
            evidence_multiplier *= 1.10
        if features.get("study_app_ratio", 0) > 0.3:
            evidence_multiplier *= 0.90

        return raw_score * evidence_multiplier

    def _compute_class_probabilities(self, score: float) -> dict:
        """Compute softmax-style class probabilities."""
        # Map score to logits for each class
        centers = {"Low": 12.5, "Moderate": 37.5, "High": 62.5, "Severe": 87.5}
        logits = {cls: -abs(score - center) / 15.0 for cls, center in centers.items()}

        # Softmax
        exp_vals = {cls: math.exp(v) for cls, v in logits.items()}
        total = sum(exp_vals.values())
        probs = {cls: round(v / total * 100, 1) for cls, v in exp_vals.items()}
        return probs

    def _compute_confidence(self, features: dict, score: float) -> float:
        """Confidence based on how far score is from decision boundaries (25, 50, 75)."""
        boundaries = [25, 50, 75]
        min_dist = min(abs(score - b) for b in boundaries)
        # Farther from boundary = more confident
        confidence = min(95, 50 + min_dist * 1.5)

        # Penalize confidence if few data points
        if features.get("days_tracked", 7) < 3:
            confidence *= 0.8

        return confidence

    def _get_level(self, score: float) -> dict:
        for lvl in self.LEVELS:
            low, high = lvl["range"]
            if low <= score < high:
                return lvl
        return self.LEVELS[-1]

    def _identify_key_factors(self, features: dict) -> list:
        """Identify top contributing risk factors."""
        factors = []
        if features.get("daily_hours", 0) > 5:
            factors.append({"factor": "High daily screen time", "impact": "high", "value": f"{features['daily_hours']:.1f}h/day"})
        if features.get("late_night_usage", 0) > 0.4:
            factors.append({"factor": "Late-night scrolling", "impact": "medium", "value": f"{int(features['late_night_usage']*100)}% nights"})
        if features.get("social_media_ratio", 0) > 0.5:
            factors.append({"factor": "Excessive social media", "impact": "high", "value": f"{int(features['social_media_ratio']*100)}% of usage"})
        if features.get("app_switch_rate", 0) > 20:
            factors.append({"factor": "Frequent app switching", "impact": "medium", "value": f"{int(features['app_switch_rate'])}x/hour"})
        if features.get("study_app_ratio", 0) > 0.2:
            factors.append({"factor": "Productive app usage", "impact": "positive", "value": f"{int(features['study_app_ratio']*100)}% productive"})
        return factors[:4]

    def get_bias_variance_status(self, features: dict) -> dict:
        """Report bias-variance tradeoff status of the model."""
        days = features.get("days_tracked", 7)
        if days < 3:
            status = "high_variance"
            msg = "Too few data points. Model may overfit to short-term behavior."
            recommendation = "Track for at least 7 days for reliable results."
        elif days > 30:
            status = "balanced"
            msg = "Sufficient data. Model shows good bias-variance balance."
            recommendation = "Continue tracking to maintain accuracy."
        else:
            status = "learning"
            msg = "Model is calibrating. Predictions improve with more data."
            recommendation = f"Track for {max(0, 7-days)} more days to reach optimal accuracy."

        return {
            "status": status,
            "days_tracked": days,
            "message": msg,
            "recommendation": recommendation,
            "model_confidence": min(95, 50 + days * 2),
        }
