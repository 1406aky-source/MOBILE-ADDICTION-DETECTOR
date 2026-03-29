"""
Rule-Based Reasoning Engine
Implements Prolog-style first-order logic rules for addiction assessment.
Concepts: Propositional Logic, First Order Predicate Logic, Knowledge Representation
"""


class RuleEngine:
    """
    Forward-chaining rule engine with Prolog-inspired syntax.
    Rules are evaluated against extracted features to derive conclusions.
    """

    def evaluate(self, features: dict) -> dict:
        """Evaluate all rules and return fired rules with conclusions."""
        fired = []
        conclusions = set()

        for rule in self._get_rules():
            if rule["condition"](features):
                fired.append({
                    "id": rule["id"],
                    "name": rule["name"],
                    "prolog": rule["prolog"],
                    "conclusion": rule["conclusion"],
                    "severity": rule["severity"],
                    "icon": rule["icon"],
                })
                conclusions.add(rule["conclusion"])

        # Meta-conclusion from fired rules
        meta = self._meta_conclusion(fired)

        return {
            "fired_rules": fired,
            "total_rules": len(self._get_rules()),
            "fired_count": len(fired),
            "conclusions": list(conclusions),
            "meta_conclusion": meta,
            "logic_summary": self._build_logic_summary(fired),
        }

    def _get_rules(self) -> list:
        """Define all Prolog-style rules."""
        return [
            {
                "id": "R01",
                "name": "Severe Overuse + Poor Sleep",
                "prolog": "high_addiction(X) :- daily_usage(X,H), H > 5, sleep(X,S), S < 6.",
                "conclusion": "HIGH ADDICTION RISK",
                "severity": "critical",
                "icon": "🔴",
                "condition": lambda f: f.get("daily_hours", 0) > 5 and f.get("sleep_hours", 8) < 6,
            },
            {
                "id": "R02",
                "name": "Study Apps Dominate → Low Risk",
                "prolog": "low_risk(X) :- study_ratio(X,S), social_ratio(X,R), S > R.",
                "conclusion": "PROTECTIVE: STUDY-DOMINANT USAGE",
                "severity": "positive",
                "icon": "✅",
                "condition": lambda f: f.get("study_app_ratio", 0) > f.get("social_media_ratio", 0),
            },
            {
                "id": "R03",
                "name": "Late Night + High Social Media",
                "prolog": "sleep_disorder_risk(X) :- late_night(X,N), N > 0.4, social_ratio(X,R), R > 0.5.",
                "conclusion": "SLEEP DISORDER RISK",
                "severity": "high",
                "icon": "🌙",
                "condition": lambda f: f.get("late_night_usage", 0) > 0.4 and f.get("social_media_ratio", 0) > 0.5,
            },
            {
                "id": "R04",
                "name": "Extreme App Switching → Attention Deficit",
                "prolog": "attention_deficit(X) :- switch_rate(X,R), R > 20.",
                "conclusion": "ATTENTION DEFICIT PATTERN",
                "severity": "medium",
                "icon": "🔄",
                "condition": lambda f: f.get("app_switch_rate", 0) > 20,
            },
            {
                "id": "R05",
                "name": "Gaming + Late Night → Behavioral Addiction",
                "prolog": "behavioral_addiction(X) :- gaming_ratio(X,G), G > 0.4, late_night(X,N), N > 0.5.",
                "conclusion": "BEHAVIORAL GAMING ADDICTION",
                "severity": "high",
                "icon": "🎮",
                "condition": lambda f: f.get("gaming_ratio", 0) > 0.4 and f.get("late_night_usage", 0) > 0.5,
            },
            {
                "id": "R06",
                "name": "Productivity > 50% → Healthy",
                "prolog": "healthy_usage(X) :- productivity_ratio(X,P), P > 0.5.",
                "conclusion": "HEALTHY PRODUCTIVE USAGE",
                "severity": "positive",
                "icon": "💼",
                "condition": lambda f: f.get("productivity_ratio", 0) > 0.5,
            },
            {
                "id": "R07",
                "name": "Moderate Use with Poor Sleep",
                "prolog": "sleep_impacted(X) :- daily_usage(X,H), H > 3, sleep(X,S), S < 7.",
                "conclusion": "SLEEP QUALITY IMPACTED",
                "severity": "medium",
                "icon": "😴",
                "condition": lambda f: f.get("daily_hours", 0) > 3 and f.get("sleep_hours", 8) < 7,
            },
            {
                "id": "R08",
                "name": "Worsening Trend Over Time",
                "prolog": "trend_risk(X) :- trend(X,T), T = worsening.",
                "conclusion": "WORSENING USAGE TREND",
                "severity": "high",
                "icon": "📈",
                "condition": lambda f: f.get("addiction_trend") == "worsening",
            },
            {
                "id": "R09",
                "name": "Weekend Spike Behavior",
                "prolog": "weekend_binge(X) :- weekend_spike(X,W), W > 0.5.",
                "conclusion": "WEEKEND BINGE PATTERN",
                "severity": "medium",
                "icon": "📅",
                "condition": lambda f: f.get("weekend_spike", 0) > 0.5,
            },
            {
                "id": "R10",
                "name": "Notification Overload",
                "prolog": "distraction_risk(X) :- notifications(X,N), N > 15.",
                "conclusion": "HIGH DISTRACTION FROM NOTIFICATIONS",
                "severity": "medium",
                "icon": "🔔",
                "condition": lambda f: f.get("notification_clicks", 0) > 15,
            },
        ]

    def _meta_conclusion(self, fired: list) -> str:
        """Derive top-level conclusion from fired rules."""
        if not fired:
            return "No significant risk patterns detected."
        critical = [r for r in fired if r["severity"] == "critical"]
        high = [r for r in fired if r["severity"] == "high"]
        positive = [r for r in fired if r["severity"] == "positive"]

        if critical:
            return f"CRITICAL: {len(critical)} critical rule(s) fired. Immediate intervention required."
        elif len(high) >= 2:
            return f"HIGH RISK: Multiple high-severity patterns detected ({len(high)} rules)."
        elif high:
            return f"ELEVATED RISK: {high[0]['conclusion']}."
        elif positive and len(positive) >= 2:
            return "POSITIVE: Multiple healthy patterns detected. Keep it up!"
        else:
            return f"{len(fired)} behavioral pattern(s) identified. Monitor closely."

    def _build_logic_summary(self, fired: list) -> str:
        if not fired:
            return "∅ — No rules fired. Usage appears within normal parameters."
        parts = [f"R{r['id']}" for r in fired[:3]]
        return f"Fired: {', '.join(parts)}{'...' if len(fired) > 3 else ''} → {self._meta_conclusion(fired)}"
