# 🧠 MindGuard — AI Mobile Addiction Detector

> An intelligent, AI-powered system that analyzes mobile usage behavior, predicts addiction levels, and recommends personalized interventions using machine learning, probabilistic reasoning, intelligent agents, and rule-based logic.

---

## 📌 Overview

MindGuard is a full-stack AI application built with Python (Flask) and a responsive dark-themed web dashboard. It maps directly to core Artificial Intelligence concepts and demonstrates a working intelligent system pipeline — from raw data input to actionable AI-driven decisions.

---

## 🚀 Features

| Feature | AI Concept |
|---|---|
| Multi-level addiction classification (Low/Moderate/High/Severe) | Bayesian Classification, Supervised Learning |
| Digital Health Score (composite 0–100) | Multi-objective Utility Functions |
| Usage prediction & weekly forecast | Regression Models, Probability Theory |
| Intelligent intervention agent | Rational Agents, Utility-Based Decisions |
| Prolog-style rule engine (10 rules) | First-Order Logic, Knowledge Representation |
| User archetype clustering | K-Means, Unsupervised Learning |
| Personalized recommendations | Reinforcement Learning, Optimization |
| AI-optimized daily schedule | Search Algorithms, Local Search |
| Smart probability alerts | Conditional Probability, Random Variables |
| Bias-Variance model monitor | Bias-Variance Tradeoff, Model Evaluation |
| Behavioral pattern analysis | Feature Engineering, Time-Series |

---

## 🗂️ Project Structure

```
mobile-addiction-detector/
│
├── app.py                      # Main Flask application & API routes
├── config.json                 # App configuration & model thresholds
├── requirements.txt            # Python dependencies
├── run.sh                      # Start script (dev & prod)
├── .gitignore
├── README.md
├── statementofpurpose.md
│
├── models/
│   ├── __init__.py
│   ├── classifier.py           # Addiction level classifier (Bayesian)
│   ├── predictor.py            # Usage regression predictor
│   ├── agent.py                # Intervention agent (rational + RL)
│   ├── clustering.py           # K-Means user clustering
│   └── health_score.py         # Digital Health Score engine
│
├── utils/
│   ├── __init__.py
│   ├── feature_extractor.py    # Feature engineering pipeline
│   ├── rule_engine.py          # Prolog-style forward-chaining rules
│   └── schedule_optimizer.py   # Greedy local search scheduler
│
├── templates/
│   └── index.html              # Main dashboard HTML
│
├── static/
│   ├── css/
│   │   └── style.css           # Dark futuristic UI theme
│   └── js/
│       └── app.js              # Dashboard rendering & API calls
│
└── tests/
    └── test_basic.py           # Unit tests (pytest)
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip

### Quick Start

```bash
# 1. Clone or download the project
cd mobile-addiction-detector

# 2. Make run script executable
chmod +x run.sh

# 3. Run the app (auto-installs dependencies)
./run.sh

# 4. Open browser
open http://localhost:5000
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

---

## 🧪 Running Tests

```bash
# Via run script
./run.sh --test

# Or directly with pytest
source venv/bin/activate
python -m pytest tests/test_basic.py -v
```

Expected output: **40+ passing tests** covering all AI model components.

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Main dashboard UI |
| `POST` | `/api/analyze` | Full AI analysis pipeline |
| `POST` | `/api/quick-check` | Fast addiction level check |
| `POST` | `/api/recommendations` | Personalized recommendations |
| `POST` | `/api/schedule` | AI-optimized daily schedule |
| `GET` | `/api/cluster-map` | Cluster visualization data |
| `GET` | `/api/health` | System health check |

### Sample Request — `/api/analyze`

```json
POST /api/analyze
Content-Type: application/json

{
  "daily_hours": 6.5,
  "sleep_hours": 5.5,
  "social_hours": 4.0,
  "study_hours": 0.5,
  "gaming_hours": 1.0,
  "night_usage_days": 5,
  "app_switches_per_hour": 22,
  "notification_clicks_per_hour": 18,
  "days_tracked": 10,
  "weekday_avg_hours": 5.5,
  "weekend_avg_hours": 9.0,
  "time_of_day": "evening"
}
```

### Sample Response (abbreviated)

```json
{
  "addiction": {
    "level": "High",
    "score": 68.4,
    "color": "#f97316",
    "confidence": 78.2,
    "probabilities": { "Low": 4.1, "Moderate": 15.3, "High": 52.7, "Severe": 27.9 }
  },
  "health_score": {
    "total": 38.5,
    "grade": "D",
    "status": "Poor"
  },
  "prediction": {
    "predicted_hours": 7.8,
    "will_exceed_limit": true,
    "probability_exceed": 87.3
  },
  "cluster": {
    "cluster_id": "social_media_addict",
    "label": "Social Media Addict"
  }
}
```

---

## 🧠 AI Concepts Mapping

### 1. Intelligent Agents
The `InterventionAgent` class models a rational agent with:
- **Perception**: reads usage features as environment state
- **Decision**: selects highest-utility actions via utility-based reasoning
- **Action**: returns ranked intervention recommendations

### 2. Bayesian Classification
The `AddictionClassifier` computes:
- **Prior**: `P(class)` from population base rates
- **Likelihood**: weighted feature scores as evidence
- **Posterior**: updated probability after evidence — `P(class | features)`

### 3. Regression & Prediction
The `UsagePredictor` uses:
- Linear regression with trend factors
- Normal CDF approximation: `P(X > limit) = 1 - Φ((limit - μ) / σ)`
- 95% confidence intervals for uncertainty quantification

### 4. First-Order Logic (Rule Engine)
10 Prolog-style rules, e.g.:
```prolog
high_addiction(X) :- daily_usage(X,H), H > 5, sleep(X,S), S < 6.
low_risk(X) :- study_ratio(X,S), social_ratio(X,R), S > R.
```
Implemented as a forward-chaining inference engine.

### 5. K-Means Clustering
4 pre-trained cluster centroids in a 5-dimensional feature space:
- `[daily_hours, social_ratio, gaming_ratio, productivity_ratio, late_night]`
- Soft membership via inverse-distance weighting

### 6. Reinforcement Learning (Simulated)
Intervention utility scores simulate learned Q-values:
- Higher utility = historically more effective reward
- Context adjustments simulate environment-dependent policy updates

### 7. Search-Based Schedule Optimization
`ScheduleOptimizer` uses greedy local search:
- State: time blocks with types (study, phone, health, sleep)
- Objective: maximize `(1 - phone_ratio) × 40 + study_ratio × 35 + sleep_ok × 25`

### 8. Bias-Variance Tradeoff
Model confidence adapts based on `days_tracked`:
- Few days → high variance → lower confidence → user warned
- Many days → more stable → higher confidence

---

## 🔧 Configuration

Edit `config.json` to customize:
- Risk thresholds (hours per day)
- Model types and parameters
- Health score dimension weights
- Feature toggles

---

## 🏗️ Extending the Project

### Add a new rule
In `utils/rule_engine.py`, add to `_get_rules()`:
```python
{
    "id": "R11",
    "name": "Your Rule Name",
    "prolog": "your_predicate(X) :- condition(X).",
    "conclusion": "YOUR CONCLUSION",
    "severity": "medium",  # critical / high / medium / positive
    "icon": "🔸",
    "condition": lambda f: f.get("your_feature", 0) > threshold,
},
```

### Add a new cluster
In `models/clustering.py`, add to `CENTROIDS`:
```python
"new_cluster": {
    "centroid": [hours, social, gaming, productivity, late_night],
    "label": "New Cluster Label",
    ...
}
```

---

## 📋 Dependencies

| Package | Version | Purpose |
|---|---|---|
| Flask | 3.0.3 | Web framework & API |
| flask-cors | 4.0.1 | Cross-origin request handling |
| gunicorn | 22.0.0 | Production WSGI server |
| python-dotenv | 1.0.1 | Environment variable management |

> **Note**: No heavy ML libraries (scikit-learn, TensorFlow) are required. All AI models are implemented from scratch using pure Python math, making the concepts transparent and exam-friendly.

---

## 📄 License

MIT License — Free for academic and educational use.

---

## 👥 Authors

Built as an AI course project demonstrating intelligent systems, machine learning, probabilistic reasoning, and agent-based design.
