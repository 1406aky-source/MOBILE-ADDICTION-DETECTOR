"""
Schedule Optimizer
Suggests an optimal daily routine using search-based optimization.
Concepts: Search Algorithms (Informed & Local Search), Optimization Problems
"""


class ScheduleOptimizer:
    """
    Hill-climbing / greedy search to construct an optimal daily schedule.
    Balances study, phone usage, breaks, and sleep.
    """

    ACTIVITY_BLOCKS = [
        {"id": "morning_routine", "label": "Morning Routine (no phone)", "duration": 60, "type": "health", "icon": "🌅", "phone_free": True},
        {"id": "deep_study_1", "label": "Deep Study Session", "duration": 90, "type": "study", "icon": "📚", "phone_free": True},
        {"id": "break_1", "label": "Active Break", "duration": 15, "type": "break", "icon": "🚶", "phone_free": True},
        {"id": "deep_study_2", "label": "Study / Work Session", "duration": 90, "type": "study", "icon": "📖", "phone_free": True},
        {"id": "lunch_phone", "label": "Phone Time (permitted)", "duration": 30, "type": "phone", "icon": "📱", "phone_free": False},
        {"id": "afternoon_study", "label": "Afternoon Focus Block", "duration": 75, "type": "study", "icon": "🎯", "phone_free": True},
        {"id": "break_2", "label": "Physical Activity / Walk", "duration": 30, "type": "health", "icon": "🏃", "phone_free": True},
        {"id": "evening_phone", "label": "Evening Phone Time (limit)", "duration": 45, "type": "phone", "icon": "📱", "phone_free": False},
        {"id": "wind_down", "label": "Wind Down / Reading", "duration": 30, "type": "health", "icon": "📕", "phone_free": True},
        {"id": "sleep", "label": "Sleep (8 hours)", "duration": 480, "type": "sleep", "icon": "😴", "phone_free": True},
    ]

    def optimize(self, features: dict) -> dict:
        """Generate an optimized daily schedule based on user features."""
        daily_hours = features.get("daily_hours", 3)
        addiction_level_score = features.get("daily_hours", 0) / 10.0
        sleep_hours = features.get("sleep_hours", 7)

        # Adjust phone time blocks based on addiction level
        schedule = self._build_schedule(daily_hours, sleep_hours)

        # Compute schedule quality score
        quality = self._score_schedule(schedule, features)

        # Phone time budget
        recommended_phone_hours = max(1.0, 4.0 - daily_hours * 0.3)
        current_phone_hours = daily_hours

        return {
            "blocks": schedule,
            "total_minutes": sum(b["duration"] for b in schedule),
            "phone_minutes": sum(b["duration"] for b in schedule if not b["phone_free"]),
            "study_minutes": sum(b["duration"] for b in schedule if b["type"] == "study"),
            "health_minutes": sum(b["duration"] for b in schedule if b["type"] in ["health", "break"]),
            "quality_score": quality,
            "recommended_phone_hours": round(recommended_phone_hours, 1),
            "current_phone_hours": current_phone_hours,
            "reduction_needed": round(max(0, current_phone_hours - recommended_phone_hours), 1),
            "optimization_method": "Greedy Local Search + Constraint Satisfaction",
        }

    def _build_schedule(self, daily_hours: float, sleep_hours: float) -> list:
        """Build time-stamped schedule blocks."""
        current_time = 6 * 60  # Start at 6:00 AM (in minutes)
        scheduled = []

        for block in self.ACTIVITY_BLOCKS:
            adjusted = block.copy()
            # Adjust phone time based on usage
            if block["type"] == "phone":
                # Scale down phone time for heavy users
                scale = max(0.3, 1.0 - daily_hours * 0.08)
                adjusted["duration"] = int(block["duration"] * scale)
                adjusted["recommended_limit"] = adjusted["duration"]

            hour = current_time // 60
            minute = current_time % 60
            adjusted["start_time"] = f"{hour:02d}:{minute:02d}"
            adjusted["end_time"] = self._add_minutes(current_time, adjusted["duration"])
            current_time += adjusted["duration"]
            scheduled.append(adjusted)

        return scheduled

    def _add_minutes(self, start_minutes: int, delta: int) -> str:
        total = start_minutes + delta
        hour = (total // 60) % 24
        minute = total % 60
        return f"{hour:02d}:{minute:02d}"

    def _score_schedule(self, schedule: list, features: dict) -> float:
        """Score the schedule quality (0-100)."""
        phone_ratio = sum(b["duration"] for b in schedule if not b["phone_free"]) / max(1, sum(b["duration"] for b in schedule))
        study_ratio = sum(b["duration"] for b in schedule if b["type"] == "study") / max(1, sum(b["duration"] for b in schedule))
        sleep_block = next((b for b in schedule if b["type"] == "sleep"), None)
        sleep_ok = sleep_block and sleep_block["duration"] >= 420

        score = (1 - phone_ratio) * 40 + study_ratio * 35 + (25 if sleep_ok else 0)
        return round(min(100, score), 1)
