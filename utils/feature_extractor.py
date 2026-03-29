"""
Feature Extractor
Transforms raw user input into ML-ready feature vectors.
Concepts: Feature Learning, Data Representation, Time-series Analysis
"""

from datetime import datetime


class FeatureExtractor:
    """
    Extracts and engineers features from raw usage data.
    Handles missing values and normalizes inputs.
    """

    def extract(self, raw: dict) -> dict:
        """
        Extract features from raw user input form data.
        Returns a normalized feature dictionary.
        """
        # Core usage features
        daily_hours = float(raw.get("daily_hours", 3.0))
        sleep_hours = float(raw.get("sleep_hours", 7.0))
        social_hours = float(raw.get("social_hours", 1.5))
        study_hours = float(raw.get("study_hours", 0.5))
        gaming_hours = float(raw.get("gaming_hours", 0.5))
        night_usage_days = int(raw.get("night_usage_days", 2))
        app_switches_per_hour = int(raw.get("app_switches_per_hour", 10))
        notification_clicks_per_hour = int(raw.get("notification_clicks_per_hour", 8))
        days_tracked = int(raw.get("days_tracked", 7))
        is_weekend = bool(raw.get("is_weekend", False))
        time_of_day = raw.get("time_of_day", "afternoon")

        # Prevent division by zero
        safe_daily = max(daily_hours, 0.01)

        # --- Derived Features ---
        social_media_ratio = min(1.0, social_hours / safe_daily)
        study_app_ratio = min(1.0, study_hours / safe_daily)
        gaming_ratio = min(1.0, gaming_hours / safe_daily)
        productivity_ratio = min(1.0, (study_hours + raw.get("work_hours", 0)) / safe_daily)

        # Late night usage: days/week as probability
        late_night_usage = min(1.0, night_usage_days / 7.0)

        # Weekend spike: ratio of weekend to weekday usage
        weekday_avg = float(raw.get("weekday_avg_hours", daily_hours * 0.9))
        weekend_avg = float(raw.get("weekend_avg_hours", daily_hours * 1.3))
        weekend_spike = min(1.0, max(0, (weekend_avg - weekday_avg) / max(weekday_avg, 0.1)))

        # App switch rate per hour
        app_switch_rate = min(60, app_switches_per_hour)

        # Time of day factor (morning=0, night=1)
        tod_map = {"morning": 0.1, "afternoon": 0.4, "evening": 0.7, "night": 0.95}
        time_of_day_factor = tod_map.get(time_of_day, 0.5)

        # Sleep deficit
        sleep_deficit = max(0, 8 - sleep_hours)

        # Attention burst indicator (many switches = short attention)
        attention_burst_score = min(1.0, app_switches_per_hour / 30.0)

        # Addiction trend (simple heuristic from historical data if available)
        hist = raw.get("history_hours", [])
        trend = self._compute_trend(hist) if hist else "stable"

        return {
            # Raw
            "daily_hours": daily_hours,
            "sleep_hours": sleep_hours,
            "social_hours": social_hours,
            "study_hours": study_hours,
            "gaming_hours": gaming_hours,
            "days_tracked": days_tracked,
            "is_weekend": is_weekend,
            # Derived
            "social_media_ratio": round(social_media_ratio, 3),
            "study_app_ratio": round(study_app_ratio, 3),
            "gaming_ratio": round(gaming_ratio, 3),
            "productivity_ratio": round(productivity_ratio, 3),
            "late_night_usage": round(late_night_usage, 3),
            "weekend_spike": round(weekend_spike, 3),
            "app_switch_rate": app_switch_rate,
            "notification_clicks": notification_clicks_per_hour,
            "time_of_day_factor": time_of_day_factor,
            "sleep_deficit": round(sleep_deficit, 1),
            "attention_burst_score": round(attention_burst_score, 3),
            "addiction_trend": trend,
        }

    def _compute_trend(self, history: list) -> str:
        """Compute trend direction from historical daily hours."""
        if len(history) < 3:
            return "stable"
        recent = sum(history[-3:]) / 3
        older = sum(history[:3]) / 3
        delta = recent - older
        if delta > 0.5:
            return "worsening"
        elif delta < -0.5:
            return "improving"
        return "stable"
