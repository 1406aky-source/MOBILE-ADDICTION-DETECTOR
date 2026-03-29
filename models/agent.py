"""
Intelligent Intervention Agent
Acts as a rational agent to suggest optimal interventions.
Concepts: Intelligent Agents, Rationality, Agent-Environment Interaction,
          Reinforcement Learning, Utility-based agents, Optimization
"""


class InterventionAgent:
    """
    Rational agent that perceives environment (usage data) and selects optimal interventions.
    Uses utility-based decision making with a reward function.
    """

    # Intervention library with utility values (simulated RL rewards)
    INTERVENTIONS = {
        "take_break": {
            "title": "Take a 15-Minute Break",
            "description": "Step away from all screens. Do light stretching or walk.",
            "icon": "☕",
            "type": "immediate",
            "utility": 0.85,
            "applicable_levels": ["Moderate", "High", "Severe"],
        },
        "focus_mode": {
            "title": "Enable Focus Mode",
            "description": "Lock distracting apps for the next 2 hours.",
            "icon": "🎯",
            "type": "app_control",
            "utility": 0.90,
            "applicable_levels": ["High", "Severe"],
        },
        "pomodoro": {
            "title": "Start Pomodoro Session",
            "description": "25 min work + 5 min break. Rebuilds focus span.",
            "icon": "🍅",
            "type": "productivity",
            "utility": 0.88,
            "applicable_levels": ["Moderate", "High", "Severe"],
        },
        "bedtime_mode": {
            "title": "Enable Bedtime Mode",
            "description": "No social apps after 10 PM to protect sleep quality.",
            "icon": "🌙",
            "type": "schedule",
            "utility": 0.92,
            "applicable_levels": ["Moderate", "High", "Severe"],
        },
        "app_timer": {
            "title": "Set App Timers",
            "description": "Limit Instagram/TikTok to 30 minutes daily.",
            "icon": "⏱️",
            "type": "app_control",
            "utility": 0.87,
            "applicable_levels": ["High", "Severe"],
        },
        "digital_detox": {
            "title": "24-Hour Digital Detox",
            "description": "Go phone-free for one day this weekend.",
            "icon": "🌿",
            "type": "long_term",
            "utility": 0.95,
            "applicable_levels": ["Severe"],
        },
        "study_challenge": {
            "title": "Study Challenge",
            "description": "Replace 1 hour of social media with a learning app today.",
            "icon": "📚",
            "type": "habit",
            "utility": 0.80,
            "applicable_levels": ["Low", "Moderate", "High"],
        },
        "notification_audit": {
            "title": "Notification Audit",
            "description": "Turn off non-essential notifications from 3 apps.",
            "icon": "🔕",
            "type": "settings",
            "utility": 0.75,
            "applicable_levels": ["Moderate", "High", "Severe"],
        },
        "grayscale_mode": {
            "title": "Enable Grayscale Display",
            "description": "Reduces visual appeal of social apps by 40%.",
            "icon": "⚫",
            "type": "visual",
            "utility": 0.70,
            "applicable_levels": ["High", "Severe"],
        },
        "accountability_buddy": {
            "title": "Set an Accountability Partner",
            "description": "Share your daily usage report with a trusted person.",
            "icon": "🤝",
            "type": "social",
            "utility": 0.85,
            "applicable_levels": ["High", "Severe"],
        },
    }

    # Recommendations library indexed by user cluster
    RECOMMENDATIONS = {
        "social_media_addict": [
            {"app": "Forest", "type": "Focus", "icon": "🌳", "reason": "Grows a virtual tree while you stay off your phone"},
            {"app": "BeReal", "type": "Mindful Social", "icon": "📸", "reason": "Authentic social media — one post per day only"},
            {"app": "Headspace", "type": "Mindfulness", "icon": "🧘", "reason": "Replaces scroll time with 10-min meditation"},
        ],
        "gamer": [
            {"app": "Khan Academy", "type": "Learning", "icon": "🎓", "reason": "Gamified learning as a healthier alternative"},
            {"app": "Duolingo", "type": "Language", "icon": "🦜", "reason": "Game-like language learning"},
            {"app": "Screen Time (iOS)", "type": "Control", "icon": "📊", "reason": "Built-in usage limits for games"},
        ],
        "casual_user": [
            {"app": "Notion", "type": "Productivity", "icon": "📓", "reason": "Channel screen time into organization"},
            {"app": "Spotify Focus", "type": "Focus Music", "icon": "🎵", "reason": "Background music for deep work"},
            {"app": "Any.do", "type": "Task Management", "icon": "✅", "reason": "Replace passive scrolling with active planning"},
        ],
        "default": [
            {"app": "Digital Wellbeing", "type": "Monitoring", "icon": "📈", "reason": "Track your own usage objectively"},
            {"app": "Freedom", "type": "App Blocker", "icon": "🚫", "reason": "Schedule blocks for distracting apps"},
            {"app": "Calm", "type": "Sleep", "icon": "😴", "reason": "Guided sleep stories instead of late-night scrolling"},
        ],
    }

    def decide(self, features: dict, addiction_level: str) -> list:
        """
        Rational agent decision: select highest-utility interventions.
        Simulates utility-based agent with environment perception.
        """
        # Perceive environment
        environment = self._perceive(features)

        # Select applicable interventions
        applicable = [
            {**v, "id": k}
            for k, v in self.INTERVENTIONS.items()
            if addiction_level in v["applicable_levels"]
        ]

        # Rank by utility (RL-style reward maximization)
        # Adjust utility based on environmental context
        for intervention in applicable:
            adjusted = intervention["utility"]
            if environment["is_night"] and intervention["id"] == "bedtime_mode":
                adjusted *= 1.2
            if environment["high_switch_rate"] and intervention["id"] == "pomodoro":
                adjusted *= 1.15
            if environment["severe_overuse"] and intervention["id"] == "digital_detox":
                adjusted *= 1.25
            intervention["adjusted_utility"] = round(min(1.0, adjusted), 3)

        # Sort by adjusted utility, return top 4
        applicable.sort(key=lambda x: x["adjusted_utility"], reverse=True)
        return applicable[:5]

    def get_recommendations(self, features: dict, addiction_level: str) -> dict:
        """Get personalized app recommendations based on cluster and level."""
        cluster = features.get("predicted_cluster", "casual_user")
        recs = self.RECOMMENDATIONS.get(cluster, self.RECOMMENDATIONS["default"])

        focus_apps = [
            {"app": "Forest", "icon": "🌳", "type": "Focus Timer"},
            {"app": "Cold Turkey", "icon": "🦃", "type": "Website Blocker"},
            {"app": "Be Focused", "icon": "⏰", "type": "Pomodoro"},
        ]
        break_reminders = [
            {"time": "Every 45 minutes", "activity": "5-min walk"},
            {"time": "After 2 hours", "activity": "15-min break"},
            {"time": "11 PM daily", "activity": "Phone-free bedtime"},
        ]
        focus_music = [
            "Lo-fi Hip Hop (YouTube)",
            "Brain.fm — AI Focus Music",
            "Spotify Deep Focus Playlist",
        ]

        return {
            "apps": recs,
            "focus_apps": focus_apps,
            "break_reminders": break_reminders,
            "focus_music": focus_music,
            "personalized_tip": self._get_tip(features, addiction_level),
        }

    def _perceive(self, features: dict) -> dict:
        """Agent perception of current environment state."""
        return {
            "is_night": features.get("late_night_usage", 0) > 0.4,
            "high_switch_rate": features.get("app_switch_rate", 0) > 15,
            "severe_overuse": features.get("daily_hours", 0) > 7,
            "low_sleep": features.get("sleep_hours", 8) < 6,
            "high_social": features.get("social_media_ratio", 0) > 0.5,
        }

    def _get_tip(self, features: dict, level: str) -> str:
        tips = {
            "Low": "You're doing well! Keep your current habits and try a 30-day digital wellness journal.",
            "Moderate": "Replace one daily social media session with a 15-minute walk. Small changes compound.",
            "High": "Consider deleting the 2 most-used social apps for one week. Notice the difference.",
            "Severe": "Your phone usage is significantly impacting your life. Talk to someone you trust today.",
        }
        return tips.get(level, tips["Moderate"])
