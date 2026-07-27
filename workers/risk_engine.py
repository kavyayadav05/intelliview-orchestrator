"""
Risk Scoring Engine

Combines signals from all pipelines to calculate final interview risk score

Responsibilities:
- Normalize signals from different pipelines
- Apply weighted scoring
- Generate final risk score (0-1 scale)
- Provide risk classification

All weights and thresholds are configurable via RISK_CONFIG.
"""

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# ---------------- CONFIG ---------------- #

RISK_CONFIG: dict[str, float] = {
    "video_weight": float(os.getenv("RISK_VIDEO_WEIGHT", "0.4")),
    "audio_weight": float(os.getenv("RISK_AUDIO_WEIGHT", "0.3")),
    "evaluation_weight": float(os.getenv("RISK_EVALUATION_WEIGHT", "0.3")),
    "low_risk_threshold": float(os.getenv("RISK_LOW_RISK_THRESHOLD", "0.3")),
    "medium_risk_threshold": float(os.getenv("RISK_MEDIUM_RISK_THRESHOLD", "0.6")),
    "high_risk_threshold": float(os.getenv("RISK_HIGH_RISK_THRESHOLD", "0.8")),
    "video_multiple_persons": float(os.getenv("RISK_VIDEO_MULTIPLE_PERSONS", "0.35")),
    "video_phone_detected": float(os.getenv("RISK_VIDEO_PHONE_DETECTED", "0.25")),
    "video_suspicious_head_movement": float(os.getenv("RISK_VIDEO_SUSPICIOUS_HEAD", "0.20")),
    "video_no_face_detected": float(os.getenv("RISK_VIDEO_NO_FACE", "0.45")),
    "audio_background_voices": float(os.getenv("RISK_AUDIO_BACKGROUND_VOICES", "0.35")),
    "audio_suspicious_pattern": float(os.getenv("RISK_AUDIO_SUSPICIOUS_PATTERN", "0.25")),
    "audio_no_transcription": float(os.getenv("RISK_AUDIO_NO_TRANSCRIPTION", "0.40")),
    "eval_low_quality": float(os.getenv("RISK_EVAL_LOW_QUALITY", "0.30")),
    "eval_low_accuracy": float(os.getenv("RISK_EVAL_LOW_ACCURACY", "0.40")),
    "eval_poor_communication": float(os.getenv("RISK_EVAL_POOR_COMMUNICATION", "0.20")),
}


class RiskScoringEngine:
    VIDEO_WEIGHT = RISK_CONFIG["video_weight"]
    AUDIO_WEIGHT = RISK_CONFIG["audio_weight"]
    EVALUATION_WEIGHT = RISK_CONFIG["evaluation_weight"]

    LOW_RISK_THRESHOLD = RISK_CONFIG["low_risk_threshold"]
    MEDIUM_RISK_THRESHOLD = RISK_CONFIG["medium_risk_threshold"]
    HIGH_RISK_THRESHOLD = RISK_CONFIG["high_risk_threshold"]

    VIDEO_FACTORS = {
        "multiple_persons": RISK_CONFIG["video_multiple_persons"],
        "phone_detected": RISK_CONFIG["video_phone_detected"],
        "suspicious_head_movement": RISK_CONFIG["video_suspicious_head_movement"],
        "no_face_detected": RISK_CONFIG["video_no_face_detected"],
    }

    AUDIO_FACTORS = {
        "background_voices": RISK_CONFIG["audio_background_voices"],
        "suspicious_pattern": RISK_CONFIG["audio_suspicious_pattern"],
        "no_transcription": RISK_CONFIG["audio_no_transcription"],
    }

    EVALUATION_FACTORS = {
        "low_quality_answers": RISK_CONFIG["eval_low_quality"],
        "low_accuracy": RISK_CONFIG["eval_low_accuracy"],
        "poor_communication": RISK_CONFIG["eval_poor_communication"],
    }

    # ---------------- CALCULATIONS ---------------- #

    @staticmethod
    def calculate_video_risk(video_result: dict[str, Any]) -> float:
        score = 0.0

        if video_result.get("multiple_persons", {}).get("multiple_persons_detected"):
            score += RiskScoringEngine.VIDEO_FACTORS["multiple_persons"]

        if video_result.get("phone_detected", {}).get("phone_detected"):
            score += RiskScoringEngine.VIDEO_FACTORS["phone_detected"]

        if video_result.get("head_movement_suspicious", {}).get("suspicious_movement_detected"):
            score += RiskScoringEngine.VIDEO_FACTORS["suspicious_head_movement"]

        if not video_result.get("face_detected", {}).get("faces_found"):
            score += RiskScoringEngine.VIDEO_FACTORS["no_face_detected"]

        return min(score, 1.0)

    @staticmethod
    def calculate_audio_risk(audio_result: dict[str, Any]) -> float:
        score = 0.0

        if audio_result.get("background_voices", {}).get("background_voices_detected"):
            score += RiskScoringEngine.AUDIO_FACTORS["background_voices"]

        if audio_result.get("suspicious_conversation", {}).get("suspicious_pattern_detected"):
            score += RiskScoringEngine.AUDIO_FACTORS["suspicious_pattern"]

        if not audio_result.get("transcription", {}).get("text"):
            score += RiskScoringEngine.AUDIO_FACTORS["no_transcription"]

        return min(score, 1.0)

    @staticmethod
    def calculate_evaluation_risk(evaluation_result: dict[str, Any]) -> float:
        score = 0.0

        quality = evaluation_result.get("answer_quality_score", {}).get("overall_quality_score", 50)
        accuracy = evaluation_result.get("technical_accuracy", {}).get("accuracy_score", 50)
        clarity = evaluation_result.get("communication_clarity", {}).get("clarity_score", 50)

        if quality < 40:
            score += RiskScoringEngine.EVALUATION_FACTORS["low_quality_answers"]
        if accuracy < 40:
            score += RiskScoringEngine.EVALUATION_FACTORS["low_accuracy"]
        if clarity < 40:
            score += RiskScoringEngine.EVALUATION_FACTORS["poor_communication"]

        return min(score, 1.0)

    @staticmethod
    def calculate_final_risk(video_risk: float, audio_risk: float, evaluation_risk: float) -> float:
        final = (
            RiskScoringEngine.VIDEO_WEIGHT * video_risk
            + RiskScoringEngine.AUDIO_WEIGHT * audio_risk
            + RiskScoringEngine.EVALUATION_WEIGHT * evaluation_risk
        )
        return round(min(max(final, 0.0), 1.0), 3)

    @staticmethod
    def classify_risk(score: float) -> str:
        if score < RiskScoringEngine.LOW_RISK_THRESHOLD:
            return "LOW"
        if score < RiskScoringEngine.MEDIUM_RISK_THRESHOLD:
            return "MEDIUM"
        if score < RiskScoringEngine.HIGH_RISK_THRESHOLD:
            return "HIGH"
        return "CRITICAL"

    # ---------------- MAIN REPORT ---------------- #

    @staticmethod
    def generate_risk_report(session_id, video_result, audio_result, evaluation_result):

        video_risk = RiskScoringEngine.calculate_video_risk(video_result)
        audio_risk = RiskScoringEngine.calculate_audio_risk(audio_result)
        evaluation_risk = RiskScoringEngine.calculate_evaluation_risk(evaluation_result)

        final_risk = RiskScoringEngine.calculate_final_risk(video_risk, audio_risk, evaluation_risk)

        decision_tree_result = RiskDecisionTree.classify(video_result, audio_result, evaluation_result)

        logger.info(f"Weighted={final_risk}, DecisionTree={decision_tree_result}")

        risk_factors = RiskScoringEngine._identify_risk_factors(video_result, audio_result, evaluation_result)

        return {
            "session_id": session_id,
            "final_risk_score": final_risk,
            "risk_classification": decision_tree_result,
            "component_risks": {
                "video_risk": video_risk,
                "audio_risk": audio_risk,
                "evaluation_risk": evaluation_risk,
            },
            "risk_factors": risk_factors,
            "recommendation": RiskScoringEngine._generate_recommendation(decision_tree_result),
        }

    # ---------------- HELPERS ---------------- #

    @staticmethod
    def _identify_risk_factors(video_result, audio_result, evaluation_result):
        factors = []

        if not video_result.get("face_detected", {}).get("faces_found"):
            factors.append("No face detected")

        if video_result.get("multiple_persons", {}).get("multiple_persons_detected"):
            factors.append("Multiple persons detected")

        if video_result.get("phone_detected", {}).get("phone_detected"):
            factors.append("Mobile phone detected")

        if audio_result.get("background_voices", {}).get("background_voices_detected"):
            factors.append("Background voices detected")

        if audio_result.get("suspicious_conversation", {}).get("suspicious_pattern_detected"):
            factors.append("Suspicious conversation detected")

        return factors

    @staticmethod
    def _generate_recommendation(risk):
        return {
            "LOW": "Safe",
            "MEDIUM": "Monitor",
            "HIGH": "Review",
            "CRITICAL": "Reject",
        }.get(risk, "Manual review")


# ---------------- DECISION TREE ---------------- #


class RiskDecisionTree:
    @staticmethod
    def classify(video, audio, evaluation):

        if video.get("multiple_persons", {}).get("multiple_persons_detected"):
            return "CRITICAL"

        if not video.get("face_detected", {}).get("faces_found"):
            return "HIGH"

        if video.get("phone_detected", {}).get("phone_detected"):
            return "HIGH"

        if audio.get("background_voices", {}).get("background_voices_detected"):
            return "MEDIUM"

        quality = evaluation.get("answer_quality_score", {}).get("overall_quality_score", 50)
        if quality < 40:
            return "MEDIUM"

        return "LOW"
