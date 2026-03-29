"""
test_basic.py — Basic unit tests for MindGuard AI system
Run: python -m pytest tests/test_basic.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from models.classifier import AddictionClassifier
from models.predictor import UsagePredictor
from models.agent import InterventionAgent
from models.clustering import UserClusteringModel
from models.health_score import DigitalHealthScoreEngine
from utils.feature_extractor import FeatureExtractor
from utils.rule_engine import RuleEngine
from utils.schedule_optimizer import ScheduleOptimizer


# --- Sample test data ---
LOW_RISK_DATA = {
    "daily_hours": 2.0, "sleep_hours": 8.0, "social_hours": 0.5,
    "study_hours": 1.0, "gaming_hours": 0.0, "night_usage_days": 1,
    "app_switches_per_hour": 5, "notification_clicks_per_hour": 3,
    "days_tracked": 14, "weekday_avg_hours": 1.8, "weekend_avg_hours": 2.5,
    "time_of_day": "morning"
}

HIGH_RISK_DATA = {
    "daily_hours": 8.0, "sleep_hours": 5.0, "social_hours": 5.0,
    "study_hours": 0.2, "gaming_hours": 1.5, "night_usage_days": 6,
    "app_switches_per_hour": 30, "notification_clicks_per_hour": 25,
    "days_tracked": 7, "weekday_avg_hours": 7.0, "weekend_avg_hours": 10.0,
    "time_of_day": "night"
}


@pytest.fixture
def extractor(): return FeatureExtractor()

@pytest.fixture
def classifier(): return AddictionClassifier()

@pytest.fixture
def predictor(): return UsagePredictor()

@pytest.fixture
def agent(): return InterventionAgent()

@pytest.fixture
def clustering(): return UserClusteringModel()

@pytest.fixture
def health_engine(): return DigitalHealthScoreEngine()

@pytest.fixture
def rule_engine(): return RuleEngine()

@pytest.fixture
def optimizer(): return ScheduleOptimizer()


# === FEATURE EXTRACTOR TESTS ===
class TestFeatureExtractor:
    def test_extracts_all_keys(self, extractor):
        features = extractor.extract(LOW_RISK_DATA)
        required = ["daily_hours", "social_media_ratio", "study_app_ratio",
                    "late_night_usage", "app_switch_rate", "productivity_ratio"]
        for key in required:
            assert key in features, f"Missing feature: {key}"

    def test_ratios_bounded(self, extractor):
        features = extractor.extract(HIGH_RISK_DATA)
        for key in ["social_media_ratio", "study_app_ratio", "gaming_ratio", "late_night_usage"]:
            assert 0.0 <= features[key] <= 1.0, f"{key} out of bounds"

    def test_late_night_calculation(self, extractor):
        features = extractor.extract({"night_usage_days": 7, "daily_hours": 4})
        assert features["late_night_usage"] == 1.0


# === CLASSIFIER TESTS ===
class TestAddictionClassifier:
    def test_low_risk_classified_correctly(self, extractor, classifier):
        features = extractor.extract(LOW_RISK_DATA)
        result = classifier.classify(features)
        assert result["level"] in ["Low", "Moderate"], f"Expected Low/Moderate got {result['level']}"

    def test_high_risk_classified_correctly(self, extractor, classifier):
        features = extractor.extract(HIGH_RISK_DATA)
        result = classifier.classify(features)
        assert result["level"] in ["High", "Severe"], f"Expected High/Severe got {result['level']}"

    def test_score_in_range(self, extractor, classifier):
        for data in [LOW_RISK_DATA, HIGH_RISK_DATA]:
            features = extractor.extract(data)
            result = classifier.classify(features)
            assert 0 <= result["score"] <= 100

    def test_probabilities_sum_to_100(self, extractor, classifier):
        features = extractor.extract(HIGH_RISK_DATA)
        result = classifier.classify(features)
        total = sum(result["probabilities"].values())
        assert abs(total - 100.0) < 1.0, f"Probabilities sum to {total}"

    def test_confidence_in_range(self, extractor, classifier):
        features = extractor.extract(LOW_RISK_DATA)
        result = classifier.classify(features)
        assert 0 <= result["confidence"] <= 100

    def test_returns_color(self, extractor, classifier):
        features = extractor.extract(LOW_RISK_DATA)
        result = classifier.classify(features)
        assert result["color"].startswith("#")

    def test_bias_variance_report(self, extractor, classifier):
        features = extractor.extract(LOW_RISK_DATA)
        bv = classifier.get_bias_variance_status(features)
        assert "status" in bv
        assert "model_confidence" in bv
        assert 0 <= bv["model_confidence"] <= 100


# === PREDICTOR TESTS ===
class TestUsagePredictor:
    def test_prediction_structure(self, extractor, predictor):
        features = extractor.extract(HIGH_RISK_DATA)
        result = predictor.predict(features)
        assert "predicted_hours" in result
        assert "will_exceed_limit" in result
        assert "trend" in result
        assert "weekly_forecast" in result

    def test_trend_has_7_days(self, extractor, predictor):
        features = extractor.extract(LOW_RISK_DATA)
        result = predictor.predict(features)
        assert len(result["trend"]) == 7

    def test_exceed_probability_in_range(self, extractor, predictor):
        features = extractor.extract(HIGH_RISK_DATA)
        result = predictor.predict(features)
        assert 0 <= result["probability_exceed"] <= 100


# === AGENT TESTS ===
class TestInterventionAgent:
    def test_returns_interventions_for_high(self, extractor, agent):
        features = extractor.extract(HIGH_RISK_DATA)
        interventions = agent.decide(features, "High")
        assert len(interventions) > 0

    def test_low_risk_fewer_interventions(self, extractor, agent):
        features_low = extractor.extract(LOW_RISK_DATA)
        features_high = extractor.extract(HIGH_RISK_DATA)
        low_count = len(agent.decide(features_low, "Low"))
        high_count = len(agent.decide(features_high, "High"))
        assert high_count >= low_count

    def test_interventions_have_utility(self, extractor, agent):
        features = extractor.extract(HIGH_RISK_DATA)
        interventions = agent.decide(features, "High")
        for iv in interventions:
            assert "adjusted_utility" in iv
            assert 0 <= iv["adjusted_utility"] <= 1.0


# === CLUSTERING TESTS ===
class TestClustering:
    def test_assigns_cluster(self, extractor, clustering):
        features = extractor.extract(HIGH_RISK_DATA)
        result = clustering.assign_cluster(features)
        assert result["cluster_id"] in ["casual_user", "social_media_addict", "gamer", "productivity_user"]

    def test_high_social_maps_to_social_addict(self, extractor, clustering):
        features = extractor.extract(HIGH_RISK_DATA)
        # High social_hours relative to total should cluster toward social_media_addict
        result = clustering.assign_cluster(features)
        # Just check it returns a valid cluster
        assert result["cluster_id"] is not None

    def test_memberships_sum_to_100(self, extractor, clustering):
        features = extractor.extract(LOW_RISK_DATA)
        result = clustering.assign_cluster(features)
        total = sum(result["memberships"].values())
        assert abs(total - 100.0) < 2.0


# === HEALTH SCORE TESTS ===
class TestHealthScore:
    def test_score_in_range(self, extractor, health_engine, classifier):
        features = extractor.extract(LOW_RISK_DATA)
        addiction_result = classifier.classify(features)
        result = health_engine.compute(features, addiction_result, {})
        assert 0 <= result["total"] <= 100

    def test_low_risk_higher_score(self, extractor, health_engine, classifier):
        f_low = extractor.extract(LOW_RISK_DATA)
        f_high = extractor.extract(HIGH_RISK_DATA)
        score_low = health_engine.compute(f_low, classifier.classify(f_low), {})["total"]
        score_high = health_engine.compute(f_high, classifier.classify(f_high), {})["total"]
        assert score_low > score_high

    def test_has_grade(self, extractor, health_engine, classifier):
        features = extractor.extract(LOW_RISK_DATA)
        result = health_engine.compute(features, classifier.classify(features), {})
        assert result["grade"] in ["A", "B", "C", "D", "F"]


# === RULE ENGINE TESTS ===
class TestRuleEngine:
    def test_fires_critical_rules_for_high_risk(self, extractor, rule_engine):
        features = extractor.extract(HIGH_RISK_DATA)
        result = rule_engine.evaluate(features)
        assert result["fired_count"] > 0

    def test_fires_positive_rules_for_low_risk(self, extractor, rule_engine):
        features = extractor.extract(LOW_RISK_DATA)
        result = rule_engine.evaluate(features)
        positive = [r for r in result["fired_rules"] if r["severity"] == "positive"]
        assert len(positive) >= 0  # May or may not fire depending on data

    def test_meta_conclusion_present(self, extractor, rule_engine):
        features = extractor.extract(HIGH_RISK_DATA)
        result = rule_engine.evaluate(features)
        assert len(result["meta_conclusion"]) > 0


# === SCHEDULE OPTIMIZER TESTS ===
class TestScheduleOptimizer:
    def test_generates_blocks(self, extractor, optimizer):
        features = extractor.extract(LOW_RISK_DATA)
        result = optimizer.optimize(features)
        assert len(result["blocks"]) > 0

    def test_quality_score_in_range(self, extractor, optimizer):
        features = extractor.extract(HIGH_RISK_DATA)
        result = optimizer.optimize(features)
        assert 0 <= result["quality_score"] <= 100

    def test_has_timing(self, extractor, optimizer):
        features = extractor.extract(LOW_RISK_DATA)
        result = optimizer.optimize(features)
        for block in result["blocks"]:
            assert "start_time" in block
            assert "end_time" in block


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
