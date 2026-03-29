"""
Mobile Addiction Detector - Main Flask Application
An intelligent AI-powered system to analyze and predict mobile usage addiction patterns.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime

from models.classifier import AddictionClassifier
from models.predictor import UsagePredictor
from models.agent import InterventionAgent
from models.clustering import UserClusteringModel
from models.health_score import DigitalHealthScoreEngine
from utils.feature_extractor import FeatureExtractor
from utils.rule_engine import RuleEngine
from utils.schedule_optimizer import ScheduleOptimizer

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mad-secret-2024-xK9#pQ")
CORS(app)

# Load config
with open("config.json") as f:
    CONFIG = json.load(f)

# Initialize models
classifier = AddictionClassifier()
predictor = UsagePredictor()
agent = InterventionAgent()
clustering = UserClusteringModel()
health_engine = DigitalHealthScoreEngine()
feature_extractor = FeatureExtractor()
rule_engine = RuleEngine()
schedule_optimizer = ScheduleOptimizer()


@app.route("/")
def index():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    return render_template("index.html", config=CONFIG)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Core analysis endpoint - processes usage data and returns full AI report."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user_id = session.get("user_id", str(uuid.uuid4()))
    timestamp = datetime.now().isoformat()

    # --- Feature Extraction ---
    features = feature_extractor.extract(data)

    # --- Addiction Classification (Multi-Level) ---
    addiction_result = classifier.classify(features)

    # --- Usage Prediction ---
    prediction_result = predictor.predict(features)

    # --- Rule-Based Reasoning (Prolog-style) ---
    rules_result = rule_engine.evaluate(features)

    # --- Intelligent Agent Interventions ---
    interventions = agent.decide(features, addiction_result["level"])

    # --- User Clustering ---
    cluster_result = clustering.assign_cluster(features)

    # --- Schedule Optimization ---
    optimal_schedule = schedule_optimizer.optimize(features)

    # --- Digital Health Score ---
    health_score = health_engine.compute(features, addiction_result, prediction_result)

    # --- Smart Probability Alerts ---
    alerts = _generate_probability_alerts(features, prediction_result)

    # --- Bias-Variance Status ---
    bv_status = classifier.get_bias_variance_status(features)

    response = {
        "user_id": user_id,
        "timestamp": timestamp,
        "features": features,
        "addiction": addiction_result,
        "prediction": prediction_result,
        "rules": rules_result,
        "interventions": interventions,
        "cluster": cluster_result,
        "schedule": optimal_schedule,
        "health_score": health_score,
        "alerts": alerts,
        "bias_variance": bv_status,
    }

    return jsonify(response)


@app.route("/api/quick-check", methods=["POST"])
def quick_check():
    """Lightweight endpoint for quick addiction level check."""
    data = request.get_json()
    features = feature_extractor.extract(data)
    result = classifier.classify(features)
    health = health_engine.compute(features, result, {})
    return jsonify({
        "level": result["level"],
        "score": result["score"],
        "health_score": health["total"],
        "color": result["color"],
        "emoji": result["emoji"],
    })


@app.route("/api/recommendations", methods=["POST"])
def recommendations():
    """Get personalized app and habit recommendations."""
    data = request.get_json()
    features = feature_extractor.extract(data)
    addiction_result = classifier.classify(features)
    recs = agent.get_recommendations(features, addiction_result["level"])
    return jsonify(recs)


@app.route("/api/schedule", methods=["POST"])
def schedule():
    """Get AI-optimized daily schedule."""
    data = request.get_json()
    features = feature_extractor.extract(data)
    result = schedule_optimizer.optimize(features)
    return jsonify(result)


@app.route("/api/cluster-map", methods=["GET"])
def cluster_map():
    """Returns cluster visualization data."""
    data = clustering.get_cluster_map()
    return jsonify(data)


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "version": CONFIG["version"], "models": "loaded"})


def _generate_probability_alerts(features, prediction):
    alerts = []
    daily_hours = features.get("daily_hours", 0)
    late_night = features.get("late_night_usage", 0)
    switch_rate = features.get("app_switch_rate", 0)
    social_ratio = features.get("social_media_ratio", 0)

    # Instagram re-open probability
    if social_ratio > 0.4:
        prob = min(95, int(60 + social_ratio * 40))
        alerts.append({
            "type": "warning",
            "icon": "📱",
            "message": f"{prob}% chance you'll open a social app again within 10 minutes.",
            "action": "Enable Focus Mode now",
        })

    # Exceed daily limit
    if prediction.get("will_exceed_limit"):
        overage = prediction.get("predicted_hours", daily_hours) - CONFIG["thresholds"]["high_risk_hours"]
        alerts.append({
            "type": "danger",
            "icon": "⏰",
            "message": f"You are likely to exceed {CONFIG['thresholds']['high_risk_hours']} hours today by ~{overage:.1f}h.",
            "action": "Set app timer limits",
        })

    # Late night warning
    if late_night > 0.3:
        alerts.append({
            "type": "warning",
            "icon": "🌙",
            "message": f"Late-night usage detected on {int(late_night*100)}% of recent nights. Sleep quality at risk.",
            "action": "Enable bedtime mode at 10 PM",
        })

    # Short attention burst
    if switch_rate > 15:
        alerts.append({
            "type": "info",
            "icon": "🔄",
            "message": f"You switch apps ~{switch_rate:.0f} times/hour — indicating low focus span.",
            "action": "Try a 25-min Pomodoro session",
        })

    return alerts


if __name__ == "__main__":
    app.run(debug=CONFIG.get("debug", True), host="0.0.0.0", port=CONFIG.get("port", 5000))
