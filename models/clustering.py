"""
User Clustering Model
Groups users into behavioral clusters using unsupervised learning (K-Means simulation).
Concepts: Clustering (K-Means), Unsupervised Learning, Feature Representation
"""

import math
import random


class UserClusteringModel:
    """
    K-Means style clustering to identify user behavioral archetypes.
    Cluster centroids are pre-computed from simulated population data.
    """

    # Pre-trained cluster centroids (simulated)
    # Each centroid: [daily_hours, social_media_ratio, gaming_ratio, productivity_ratio, late_night]
    CENTROIDS = {
        "casual_user": {
            "centroid": [2.5, 0.25, 0.10, 0.30, 0.15],
            "label": "Casual User",
            "icon": "😊",
            "color": "#22c55e",
            "description": "Balanced and mindful phone usage. Mostly productivity and communication.",
            "population_percent": 35,
            "risk": "Low",
        },
        "social_media_addict": {
            "centroid": [6.5, 0.70, 0.05, 0.10, 0.55],
            "label": "Social Media Addict",
            "icon": "📱",
            "color": "#f97316",
            "description": "Heavy social media user. High late-night scrolling and low productivity.",
            "population_percent": 28,
            "risk": "High",
        },
        "gamer": {
            "centroid": [5.5, 0.15, 0.65, 0.10, 0.50],
            "label": "Mobile Gamer",
            "icon": "🎮",
            "color": "#8b5cf6",
            "description": "Extended gaming sessions, often late-night. Social usage is secondary.",
            "population_percent": 20,
            "risk": "High",
        },
        "productivity_user": {
            "centroid": [4.0, 0.20, 0.05, 0.60, 0.10],
            "label": "Productivity User",
            "icon": "💼",
            "color": "#3b82f6",
            "description": "Uses phone primarily for work, learning, and organization.",
            "population_percent": 17,
            "risk": "Low",
        },
    }

    FEATURE_KEYS = ["daily_hours", "social_media_ratio", "gaming_ratio", "productivity_ratio", "late_night_usage"]
    FEATURE_SCALES = [10.0, 1.0, 1.0, 1.0, 1.0]  # Normalization factors

    def assign_cluster(self, features: dict) -> dict:
        """Assign user to nearest cluster using Euclidean distance."""
        user_vector = self._extract_vector(features)
        distances = {}

        for cluster_id, cluster in self.CENTROIDS.items():
            dist = self._euclidean_distance(user_vector, cluster["centroid"])
            distances[cluster_id] = dist

        # Nearest cluster = best match
        best_cluster = min(distances, key=distances.get)
        cluster_info = self.CENTROIDS[best_cluster].copy()

        # Compute membership probabilities (soft assignment)
        total_inv = sum(1 / (d + 0.001) for d in distances.values())
        memberships = {
            k: round((1 / (d + 0.001)) / total_inv * 100, 1)
            for k, d in distances.items()
        }

        return {
            "cluster_id": best_cluster,
            "label": cluster_info["label"],
            "icon": cluster_info["icon"],
            "color": cluster_info["color"],
            "description": cluster_info["description"],
            "risk": cluster_info["risk"],
            "memberships": memberships,
            "distance_to_centroid": round(distances[best_cluster], 3),
            "similar_users_percent": cluster_info["population_percent"],
        }

    def get_cluster_map(self) -> dict:
        """Return cluster visualization data for chart rendering."""
        clusters = []
        for cluster_id, info in self.CENTROIDS.items():
            clusters.append({
                "id": cluster_id,
                "label": info["label"],
                "icon": info["icon"],
                "color": info["color"],
                "risk": info["risk"],
                "population_percent": info["population_percent"],
                "centroid_daily_hours": info["centroid"][0],
                "centroid_social": info["centroid"][1],
                "description": info["description"],
            })

        # Generate sample user scatter points for visualization
        points = self._generate_sample_points()

        return {"clusters": clusters, "sample_points": points}

    def _extract_vector(self, features: dict) -> list:
        """Extract and normalize feature vector."""
        raw = [features.get(k, 0) for k in self.FEATURE_KEYS]
        normalized = [r / s for r, s in zip(raw, self.FEATURE_SCALES)]
        return normalized

    def _euclidean_distance(self, v1: list, v2_raw: list) -> float:
        """Compute Euclidean distance between normalized vectors."""
        v2 = [r / s for r, s in zip(v2_raw, self.FEATURE_SCALES)]
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    def _generate_sample_points(self) -> list:
        """Generate synthetic scatter plot data for cluster visualization."""
        import random
        random.seed(42)
        points = []
        cluster_ids = list(self.CENTROIDS.keys())
        colors = {"casual_user": "#22c55e", "social_media_addict": "#f97316", "gamer": "#8b5cf6", "productivity_user": "#3b82f6"}
        for cluster_id in cluster_ids:
            centroid = self.CENTROIDS[cluster_id]["centroid"]
            for _ in range(15):
                x = centroid[0] + random.gauss(0, 0.8)
                y = centroid[1] + random.gauss(0, 0.08)
                points.append({
                    "x": round(max(0, x), 2),
                    "y": round(max(0, min(1, y)), 2),
                    "cluster": cluster_id,
                    "color": colors[cluster_id],
                })
        return points
