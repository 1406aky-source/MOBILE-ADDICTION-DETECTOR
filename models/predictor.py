"""
Usage Predictor
Predicts future mobile usage using regression and probability theory.
Concepts: Regression Models, Probability Theory, Conditional Probability
"""

import math


class UsagePredictor:
    """
    Regression-based predictor for future mobile usage.
    Simulates a trained time-series regression model.
    """

    DAILY_LIMIT = 4.0  # Recommended daily limit in hours

    def predict(self, features: dict) -> dict:
        """Predict today's total usage and risk of exceeding limit."""
        daily_hours = features.get("daily_hours", 0)
        time_of_day = features.get("time_of_day_factor", 0.5)  # 0=morning, 1=night
        weekend_spike = features.get("weekend_spike", 0)
        is_weekend = features.get("is_weekend", False)

        # Regression prediction: estimate end-of-day usage
        base = daily_hours
        trend_factor = 1 + (0.15 * weekend_spike if is_weekend else 0)
        time_adjustment = 1 + (time_of_day * 0.2)  # More usage predicted later in day
        predicted_hours = base * trend_factor * time_adjustment

        # Add noise (simulate model uncertainty)
        std_dev = 0.5 + 0.1 * daily_hours
        confidence_interval = (
            round(max(0, predicted_hours - 1.96 * std_dev), 1),
            round(predicted_hours + 1.96 * std_dev, 1),
        )

        # Conditional probability of exceeding limit
        prob_exceed = self._prob_exceed_limit(predicted_hours, std_dev)

        # 7-day usage trend (simulated)
        trend = self._generate_trend(daily_hours, features)

        # Weekly forecast
        weekly_forecast = self._weekly_forecast(daily_hours, features)

        return {
            "predicted_hours": round(predicted_hours, 2),
            "daily_limit": self.DAILY_LIMIT,
            "will_exceed_limit": predicted_hours > self.DAILY_LIMIT,
            "probability_exceed": round(prob_exceed * 100, 1),
            "confidence_interval": confidence_interval,
            "std_deviation": round(std_dev, 2),
            "trend": trend,
            "weekly_forecast": weekly_forecast,
            "regression_r2": 0.82,  # Simulated model quality metric
        }

    def _prob_exceed_limit(self, predicted: float, std: float) -> float:
        """
        P(X > limit) using normal CDF approximation.
        Z = (limit - predicted) / std
        """
        if std == 0:
            return 1.0 if predicted > self.DAILY_LIMIT else 0.0
        z = (self.DAILY_LIMIT - predicted) / std
        # Approximate standard normal CDF using error function
        prob_below = 0.5 * (1 + math.erf(z / math.sqrt(2)))
        return max(0.0, min(1.0, 1 - prob_below))

    def _generate_trend(self, current: float, features: dict) -> list:
        """Generate simulated 7-day historical trend."""
        trend = []
        base = current
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            # Simulate slight variation
            variation = math.sin(i * 0.8) * 0.5
            weekend_bump = 1.5 if i >= 5 else 1.0
            val = max(0.5, (base + variation) * weekend_bump * (0.85 + i * 0.02))
            trend.append({"day": day, "hours": round(val, 2), "is_weekend": i >= 5})
        return trend

    def _weekly_forecast(self, current: float, features: dict) -> dict:
        """Forecast next 7 days."""
        growth_rate = 0.05 if features.get("addiction_trend", "stable") == "worsening" else -0.02
        forecast = []
        for i in range(1, 8):
            projected = current * (1 + growth_rate) ** i
            projected *= (1.3 if i % 7 in [6, 0] else 1.0)  # weekend bump
            forecast.append(round(projected, 2))

        return {
            "days": forecast,
            "total_week": round(sum(forecast), 1),
            "average": round(sum(forecast) / 7, 1),
            "peak_day": forecast.index(max(forecast)),
            "trend_direction": "increasing" if growth_rate > 0 else "improving",
        }
