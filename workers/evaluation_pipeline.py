"""
Answer Evaluation Pipeline
"""

import logging
from typing import Any

from workers._stubs import _seeded_unit

logger = logging.getLogger(__name__)

# ---------------- MAIN PIPELINE ---------------- #


def evaluate_answers(session_id: str) -> dict[str, Any]:
    quality = evaluate_answer_quality(session_id)
    accuracy = evaluate_technical_accuracy(session_id)
    clarity = evaluate_communication(session_id)
    feedback = generate_feedback(session_id)

    result = {
        "session_id": session_id,
        "answer_quality_score": quality,
        "technical_accuracy": accuracy,
        "communication_clarity": clarity,
        "feedback": feedback,
    }

    result["risk_score"] = calculate_evaluation_risk_score(result)
    return result


# ---------------- STUB FUNCTIONS ---------------- #


def evaluate_answer_quality(session_id: str) -> dict[str, Any]:
    base = 0.6 + _seeded_unit(session_id, "quality") * 0.4
    return {"overall_quality_score": round(base * 100, 2)}


def evaluate_technical_accuracy(session_id: str) -> dict[str, Any]:
    base = 0.5 + _seeded_unit(session_id, "accuracy") * 0.5
    return {"accuracy_score": round(base * 100, 2)}


def evaluate_communication(session_id: str) -> dict[str, Any]:
    base = 0.6 + _seeded_unit(session_id, "comms") * 0.4
    return {"clarity_score": round(base * 100, 2)}


def generate_feedback(session_id: str) -> dict[str, Any]:
    return {
        "strengths": ["clear"],
        "improvements": ["more depth"],
        "recommendation": "progress",
    }


# ---------------- RISK SCORE ---------------- #


def calculate_evaluation_risk_score(results: dict[str, Any]) -> float:
    quality = results["answer_quality_score"]["overall_quality_score"] / 100
    accuracy = results["technical_accuracy"]["accuracy_score"] / 100
    clarity = results["communication_clarity"]["clarity_score"] / 100

    score = (1 - quality) + (1 - accuracy) + (1 - clarity)
    return round(min(score / 3, 1.0), 3)
