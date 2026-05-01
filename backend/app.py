from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@dataclass
class Metric:
    name: str
    score: int
    weight: float


AUSTRALIA_BASE_METRICS = {
    "social": [
        Metric("Health & Wellbeing", 78, 0.18),
        Metric("Education", 82, 0.16),
        Metric("Safety & Security", 75, 0.18),
        Metric("Sports & Recreation", 81, 0.16),
        Metric("Culture & Lifestyle", 79, 0.16),
        Metric("Community Inclusion", 77, 0.16),
    ],
    "environment": [
        Metric("Public Transport Access", 74, 0.2),
        Metric("Utilities Reliability", 85, 0.22),
        Metric("Air & Noise Quality", 76, 0.2),
        Metric("Walkability & Cycling", 80, 0.18),
        Metric("Climate Resilience", 73, 0.2),
    ],
    "economy": [
        Metric("Housing Affordability", 62, 0.3),
        Metric("Income Opportunity", 77, 0.24),
        Metric("Local Business Vitality", 74, 0.22),
        Metric("Cost of Living Pressure", 58, 0.24),
    ],
}

SUBURB_MODIFIERS = {
    "sydney": {"social": 1, "environment": -1, "economy": -4},
    "melbourne": {"social": 2, "environment": 1, "economy": -3},
    "brisbane": {"social": 1, "environment": 2, "economy": -1},
    "perth": {"social": 0, "environment": 2, "economy": 1},
    "adelaide": {"social": 0, "environment": 1, "economy": 2},
    "canberra": {"social": 2, "environment": 1, "economy": 1},
}


def clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, value))


def weighted_score(metrics: list[Metric]) -> int:
    return round(sum(m.score * m.weight for m in metrics))


def parse_city(address: str) -> str:
    address_lower = address.lower()
    for city in SUBURB_MODIFIERS:
        if city in address_lower:
            return city
    return "melbourne"


def assess_address(address: str) -> dict[str, Any]:
    city = parse_city(address)
    modifier = SUBURB_MODIFIERS[city]

    dimension_breakdown: dict[str, Any] = {}

    for dimension, metrics in AUSTRALIA_BASE_METRICS.items():
        adjusted: list[Metric] = []
        for m in metrics:
            adjusted.append(
                Metric(
                    name=m.name,
                    score=clamp(m.score + modifier[dimension]),
                    weight=m.weight,
                )
            )

        dimension_breakdown[dimension] = {
            "score": weighted_score(adjusted),
            "metrics": [asdict(item) for item in adjusted],
            "mainCategories": len(adjusted),
            "subCategories": len(adjusted) * 2,
            "otherIndicators": len(adjusted) * 3,
        }

    overall = round(
        dimension_breakdown["social"]["score"] * 0.42
        + dimension_breakdown["environment"]["score"] * 0.33
        + dimension_breakdown["economy"]["score"] * 0.25
    )

    return {
        "address": address,
        "country": "Australia",
        "cityContext": city.title(),
        "overallScore": overall,
        "assessmentTypes": [
            "Infrastructure Completion",
            "Facility Proximity",
            "Facility Capacity",
            "Quality of Life",
            "Community Engagement",
            "Other Indicators",
        ],
        "dimensions": dimension_breakdown,
        "marketSignals": {
            "medianPriceAUD": {
                "sydney": 1450000,
                "melbourne": 980000,
                "brisbane": 890000,
                "perth": 780000,
                "adelaide": 810000,
                "canberra": 920000,
            }[city],
            "monthlyTrendPct": {
                "sydney": 0.6,
                "melbourne": 0.4,
                "brisbane": 0.7,
                "perth": 0.9,
                "adelaide": 0.8,
                "canberra": 0.3,
            }[city],
            "annualTrendPct": {
                "sydney": 6.1,
                "melbourne": 4.8,
                "brisbane": 7.3,
                "perth": 8.4,
                "adelaide": 7.8,
                "canberra": 3.9,
            }[city],
            "rentalYieldPct": {
                "sydney": 3.4,
                "melbourne": 3.7,
                "brisbane": 4.2,
                "perth": 4.5,
                "adelaide": 4.1,
                "canberra": 3.8,
            }[city],
        },
        "nearby": {
            "schools": [
                {"name": "Primary School", "distanceKm": 0.8},
                {"name": "Secondary College", "distanceKm": 1.9},
            ],
            "transport": [
                {"name": "Train Station", "distanceKm": 1.1},
                {"name": "Bus Interchange", "distanceKm": 0.6},
            ],
            "health": [
                {"name": "GP Clinic", "distanceKm": 0.7},
                {"name": "Hospital", "distanceKm": 3.8},
            ],
            "lifestyle": [
                {"name": "Park", "distanceKm": 0.5},
                {"name": "Sport Centre", "distanceKm": 2.2},
            ],
        },
        "highlights": [
            "Balanced social and environment performance",
            "Transport access and utility resilience are key strengths",
            "Economy score is mostly constrained by affordability pressure",
        ],
    }


@app.get("/api/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@app.post("/api/assess")
def assess():
    payload = request.get_json(silent=True) or {}
    address = payload.get("address", "Docklands VIC, Australia")
    return jsonify(assess_address(address))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
