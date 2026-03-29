"""
Digital Health Score Engine
Computes a composite "Digital Health Score" combining usage, sleep, and productivity.
Concepts: Multi-objective optimization, Utility functions, Composite scoring
"""


class DigitalHealthScoreEngine:
    """Computes a holistic Digital Health Score (0-100) from multiple dimensions."""

    DIMENSIONS = {
        "screen_time": {"weight": 0.30, "label": "Screen Time", "icon": "📱", "higher_is_better": False},
        "sleep_quality": {"weight": 0.25, "label": "Sleep Quality", "icon": "😴", "higher_is_better": True},
        "productivity": {"weight": 0.25, "label": "Productivity", "icon": "⚡", "higher_is_better": True},
        "digital_balance": {"weight": 0.20, "label": "Digital Balance", "icon": "⚖️", "higher_is_better": True},
    }

    def compute(self, features: dict, addiction_result: dict, prediction_result: dict) -> dict:
        """Compute composite Digital Health Score."""
        scores = {}

        # 1. Screen Time Score (inverse — less is better)
        daily_hours = features.get("daily_hours", 0)
        # 0h → 100, 4h → 70 (healthy), 8h → 20, 10h+ → 0
        screen_score = max(0, 100 - (daily_hours ** 1.5) * 8)
        scores["screen_time"] = round(screen_score, 1)

        # 2. Sleep Quality Score
        sleep_hours = features.get("sleep_hours", 7)
        late_night = features.get("late_night_usage", 0)
        # Ideal: 7-9 hours, penalize late-night usage
        sleep_base = 100 - abs(sleep_hours - 8) * 12
        sleep_score = max(0, sleep_base * (1 - late_night * 0.5))
        scores["sleep_quality"] = round(sleep_score, 1)

        # 3. Productivity Score
        prod_ratio = features.get("productivity_ratio", 0)
        study_ratio = features.get("study_app_ratio", 0)
        social_ratio = features.get("social_media_ratio", 0)
        productivity_score = min(100, (prod_ratio + study_ratio) * 100 - social_ratio * 30)
        productivity_score = max(0, productivity_score)
        scores["productivity"] = round(productivity_score, 1)

        # 4. Digital Balance Score
        switch_rate = features.get("app_switch_rate", 0)
        # Low switching + varied app usage = good balance
        balance_score = max(0, 100 - switch_rate * 3 - social_ratio * 40)
        scores["digital_balance"] = round(balance_score, 1)

        # Compute weighted total
        total = sum(
            scores[dim] * info["weight"]
            for dim, info in self.DIMENSIONS.items()
        )
        total = round(max(0, min(100, total)), 1)

        # Grade and status
        grade, status, color = self._grade(total)

        # Dimension details for UI
        dimensions = []
        for dim_id, info in self.DIMENSIONS.items():
            dimensions.append({
                "id": dim_id,
                "label": info["label"],
                "icon": info["icon"],
                "score": scores[dim_id],
                "weight": info["weight"],
                "contribution": round(scores[dim_id] * info["weight"], 1),
                "status": self._dim_status(scores[dim_id]),
            })

        return {
            "total": total,
            "grade": grade,
            "status": status,
            "color": color,
            "dimensions": dimensions,
            "scores": scores,
            "comparison": self._peer_comparison(total),
            "improvement_potential": round(100 - total, 1),
        }

    def _grade(self, score: float) -> tuple:
        if score >= 80:
            return "A", "Excellent", "#22c55e"
        elif score >= 65:
            return "B", "Good", "#84cc16"
        elif score >= 50:
            return "C", "Fair", "#f59e0b"
        elif score >= 35:
            return "D", "Poor", "#f97316"
        else:
            return "F", "Critical", "#ef4444"

    def _dim_status(self, score: float) -> str:
        if score >= 70:
            return "good"
        elif score >= 45:
            return "warning"
        else:
            return "critical"

    def _peer_comparison(self, score: float) -> dict:
        """Compare user's score against simulated population percentiles."""
        # Simulated population mean ~55, std ~15
        mean, std = 55, 15
        z = (score - mean) / std
        # Approximate percentile
        import math
        percentile = round(50 * (1 + math.erf(z / math.sqrt(2))), 1)
        return {
            "percentile": percentile,
            "population_mean": mean,
            "better_than": f"{percentile:.0f}% of users",
        }
