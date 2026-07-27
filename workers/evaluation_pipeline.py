"""
Answer Evaluation Pipeline
"""

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

from workers._stubs import _seeded_unit

# ---------------- Question Validation ---------------- #

_BANNED_TOPIC_PATTERNS = None


<<<<<<< HEAD
def _llm_evaluate_answer_quality(session_id: str, question: str, answer: str) -> dict[str, Any] | None:
    """Use GPT-4o/Gemini/Grok to evaluate answer quality and relevance."""
    prompt = (
        "You are an expert technical interviewer. Evaluate this candidate answer. "
        "Return a JSON object with keys: overall_quality_score (0-100), "
        "relevance (0-1), completeness (0-1), clarity (0-1), feedback (string)."
    )
    user_msg = f"Question: {question}\n\nAnswer: {answer}"

    try:
        from workers.ai_client import HAS_OPENAI, chat_completion

        if HAS_OPENAI:
            response = chat_completion(
                [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                model="gpt-4o",
                temperature=0.3,
                max_tokens=512,
            )
            if response:
                parsed = json.loads(response)
                return {
                    "overall_quality_score": round(parsed.get("overall_quality_score", 50), 2),
                    "relevance": round(parsed.get("relevance", 0.5), 2),
                    "completeness": round(parsed.get("completeness", 0.5), 2),
                    "clarity": round(parsed.get("clarity", 0.5), 2),
                    "feedback": parsed.get("feedback", ""),
                    "provider": "openai",
                }
    except Exception as exc:
        logger.debug("OpenAI quality evaluation failed: %s", exc)

    try:
        from workers.ai_client import HAS_GEMINI, gemini_generate

        if HAS_GEMINI:
            response = gemini_generate(f"{prompt}\n\n{user_msg}", temperature=0.3, max_output_tokens=512)
            if response:
                parsed = json.loads(response)
                return {
                    "overall_quality_score": round(parsed.get("overall_quality_score", 50), 2),
                    "relevance": round(parsed.get("relevance", 0.5), 2),
                    "completeness": round(parsed.get("completeness", 0.5), 2),
                    "clarity": round(parsed.get("clarity", 0.5), 2),
                    "feedback": parsed.get("feedback", ""),
                    "provider": "gemini",
                }
    except Exception as exc:
        logger.debug("Gemini quality evaluation failed: %s", exc)

    try:
        from workers.ai_client import HAS_GROK, grok_completion

        if HAS_GROK:
            response = grok_completion(
                [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                temperature=0.3,
                max_tokens=512,
            )
            if response:
                parsed = json.loads(response)
                return {
                    "overall_quality_score": round(parsed.get("overall_quality_score", 50), 2),
                    "relevance": round(parsed.get("relevance", 0.5), 2),
                    "completeness": round(parsed.get("completeness", 0.5), 2),
                    "clarity": round(parsed.get("clarity", 0.5), 2),
                    "feedback": parsed.get("feedback", ""),
                    "provider": "grok",
                }
    except Exception as exc:
        logger.debug("Grok quality evaluation failed: %s", exc)

    return None


def _llm_evaluate_technical_accuracy(session_id: str, question: str, answer: str) -> dict[str, Any] | None:
    """Use GPT-4o/Gemini/Grok to evaluate technical accuracy."""
    prompt = (
        "You are a technical interviewer evaluating a candidate's answer. "
        "Return a JSON object with keys: accuracy_score (0-100), "
        "correct_concepts_count (int), incorrect_concepts_count (int), "
        "knowledge_gaps (list of strings)."
    )
    user_msg = f"Question: {question}\n\nAnswer: {answer}"
=======
def _get_banned_patterns():
    global _BANNED_TOPIC_PATTERNS
    if _BANNED_TOPIC_PATTERNS is None:
        BANNED_TOPICS = [
            "age", "pregnant", "religion", "married",
            "disability", "health condition"
        ]
        _BANNED_TOPIC_PATTERNS = [
            re.compile(r"\b" + kw + r"\b", re.IGNORECASE)
            for kw in BANNED_TOPICS
        ]
    return _BANNED_TOPIC_PATTERNS


def validate_generated_question(question: str):
    reasons = []
>>>>>>> f11d151 (Fixed merge conflicts in evaluation_pipeline)

    for pattern in _get_banned_patterns():
        if pattern.search(question):
            reasons.append("banned topic")

<<<<<<< HEAD
        if HAS_OPENAI:
            response = chat_completion(
                [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                model="gpt-4o",
                temperature=0.3,
                max_tokens=512,
            )
            if response:
                parsed = json.loads(response)
                return {
                    "accuracy_score": round(parsed.get("accuracy_score", 50), 2),
                    "correct_concepts_count": parsed.get("correct_concepts_count", 0),
                    "incorrect_concepts_count": parsed.get("incorrect_concepts_count", 0),
                    "knowledge_gaps": parsed.get("knowledge_gaps", []),
                    "provider": "openai",
                }
    except Exception as exc:
        logger.debug("OpenAI accuracy evaluation failed: %s", exc)
=======
    if len(question) < 20:
        reasons.append("too short")
>>>>>>> f11d151 (Fixed merge conflicts in evaluation_pipeline)

    if not question.endswith("?"):
        reasons.append("not a question")

<<<<<<< HEAD
        if HAS_GEMINI:
            response = gemini_generate(f"{prompt}\n\n{user_msg}", temperature=0.3, max_output_tokens=512)
            if response:
                parsed = json.loads(response)
                return {
                    "accuracy_score": round(parsed.get("accuracy_score", 50), 2),
                    "correct_concepts_count": parsed.get("correct_concepts_count", 0),
                    "incorrect_concepts_count": parsed.get("incorrect_concepts_count", 0),
                    "knowledge_gaps": parsed.get("knowledge_gaps", []),
                    "provider": "gemini",
                }
    except Exception as exc:
        logger.debug("Gemini accuracy evaluation failed: %s", exc)

    try:
        from workers.ai_client import HAS_GROK, grok_completion

        if HAS_GROK:
            response = grok_completion(
                [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                temperature=0.3,
                max_tokens=512,
            )
            if response:
                parsed = json.loads(response)
                return {
                    "accuracy_score": round(parsed.get("accuracy_score", 50), 2),
                    "correct_concepts_count": parsed.get("correct_concepts_count", 0),
                    "incorrect_concepts_count": parsed.get("incorrect_concepts_count", 0),
                    "knowledge_gaps": parsed.get("knowledge_gaps", []),
                    "provider": "grok",
                }
    except Exception as exc:
        logger.debug("Grok accuracy evaluation failed: %s", exc)

    return None


def _llm_evaluate_communication(session_id: str, question: str, answer: str) -> dict[str, Any] | None:
    """Use GPT-4o to evaluate communication clarity."""
=======
    return len(reasons) == 0, reasons


# ---------------- LLM Question Generator ---------------- #

def _llm_generate_question(session_id: str, topic: str = "systems_design"):
>>>>>>> f11d151 (Fixed merge conflicts in evaluation_pipeline)
    try:
        from workers.ai_client import chat_completion

        response = chat_completion(
            [
<<<<<<< HEAD
                {
                    "role": "system",
                    "content": (
                        "Evaluate the candidate's communication quality. "
                        "Return a JSON object with keys: clarity_score (0-100), "
                        "professionalism (0-100), confidence_level (0-1), "
                        "pace_appropriateness (0-1)."
                    ),
                },
                {"role": "user", "content": f"Question: {question}\n\nAnswer: {answer}"},
            ],
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=512,
=======
                {"role": "system", "content": f"Generate a question about {topic}"},
                {"role": "user", "content": "Give one question"}
            ]
>>>>>>> f11d151 (Fixed merge conflicts in evaluation_pipeline)
        )

        if not response:
            return None

        question = response.strip()

<<<<<<< HEAD
def _llm_generate_feedback(session_id: str, question: str, answer: str) -> dict[str, Any] | None:
    """Use GPT-4o to generate personalized interview feedback."""
    try:
        from workers.ai_client import chat_completion

        response = chat_completion(
            [
                {
                    "role": "system",
                    "content": (
                        "You are an experienced technical interviewer. Based on the "
                        "question and answer, generate structured feedback. "
                        "Return a JSON object with keys: strengths (list of strings), "
                        "improvements (list of strings), detailed_feedback (string), "
                        "recommendation (one of: strong_hire, hire, maybe, no_hire)."
                    ),
                },
                {"role": "user", "content": f"Question: {question}\n\nAnswer: {answer}"},
            ],
            model="gpt-4o",
            temperature=0.5,
            max_tokens=1024,
        )
        if response is None:
            return None
        parsed = json.loads(response)
        recommendation = parsed.get("recommendation", "progress")
        if recommendation == "hire":
            recommendation = "progress"
        return {
            "strengths": parsed.get("strengths", []),
            "improvements": parsed.get("improvements", []),
            "detailed_feedback": parsed.get("detailed_feedback", ""),
            "recommendation": recommendation,
        }
    except Exception as exc:
        logger.debug("LLM feedback generation unavailable: %s", exc)
        return None


def _llm_generate_question(session_id: str, topic: str = "systems_design") -> str | None:
    """Use LLM to generate a dynamic interview question."""
    try:
        from workers.ai_client import chat_completion

        response = chat_completion(
            [
                {
                    "role": "system",
                    "content": (
                        "Generate a single challenging technical interview question "
                        f"about {topic}. Return only the question text, nothing else."
                    ),
                },
                {"role": "user", "content": "Generate one question."},
            ],
            model="gpt-4o-mini",
            temperature=0.8,
            max_tokens=256,
        )
        return response.strip() if response else None
=======
        valid, _ = validate_generated_question(question)
        return question if valid else None

>>>>>>> f11d151 (Fixed merge conflicts in evaluation_pipeline)
    except Exception:
        return None


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

def evaluate_answer_quality(session_id):
    base = 0.6 + _seeded_unit(session_id, "quality") * 0.4
    return {"overall_quality_score": round(base * 100, 2)}


def evaluate_technical_accuracy(session_id):
    base = 0.5 + _seeded_unit(session_id, "accuracy") * 0.5
    return {"accuracy_score": round(base * 100, 2)}


def evaluate_communication(session_id):
    base = 0.6 + _seeded_unit(session_id, "comms") * 0.4
    return {"clarity_score": round(base * 100, 2)}


def generate_feedback(session_id):
    return {
        "strengths": ["clear"],
        "improvements": ["more depth"],
        "recommendation": "progress"
    }


# ---------------- RISK SCORE ---------------- #

def calculate_evaluation_risk_score(results):
    quality = results["answer_quality_score"]["overall_quality_score"] / 100
    accuracy = results["technical_accuracy"]["accuracy_score"] / 100
    clarity = results["communication_clarity"]["clarity_score"] / 100

<<<<<<< HEAD
    base = 0.55 + _seeded_unit(session_id, "comms") * 0.45
    return {
        "clarity_score": round(base * 100, 2),
        "professionalism": round(base * 100, 2),
        "confidence_level": round(base * 0.9, 2),
        "pace_appropriateness": round(base * 0.95, 2),
    }


def generate_feedback(session_id: str) -> dict[str, Any]:
    """Generate feedback — real LLM with seeded stub fallback."""
    logger.info(f"Generating feedback for session {session_id}")

    real = _llm_generate_feedback(
        session_id,
        "Describe your experience with distributed systems.",
        "I have five years of experience building distributed systems in Python and Go.",
    )
    if real is not None:
        return real

    return {
        "strengths": ["clear structure", "relevant examples"],
        "improvements": ["deepen systems-design discussion"],
        "detailed_feedback": "Solid answers overall with room to elaborate on trade-offs.",
        "recommendation": "progress",
    }


def calculate_evaluation_risk_score(results: dict[str, Any]) -> float:
    """Calculate a 0–1 risk score (inverse of performance)."""
    from workers.risk_engine import RiskScoringEngine

    quality = results.get("answer_quality_score", {}).get("overall_quality_score", 50) / 100.0
    accuracy = results.get("technical_accuracy", {}).get("accuracy_score", 50) / 100.0
    clarity = results.get("communication_clarity", {}).get("clarity_score", 50) / 100.0

    quality_risk = (1 - quality) * RiskScoringEngine.EVALUATION_FACTORS["low_quality_answers"]
    accuracy_risk = (1 - accuracy) * RiskScoringEngine.EVALUATION_FACTORS["low_accuracy"]
    clarity_risk = (1 - clarity) * RiskScoringEngine.EVALUATION_FACTORS["poor_communication"]

    score = quality_risk + accuracy_risk + clarity_risk
    return round(min(score, 1.0), 3)
=======
    score = (1 - quality) + (1 - accuracy) + (1 - clarity)
    return round(min(score / 3, 1.0), 3)
>>>>>>> f11d151 (Fixed merge conflicts in evaluation_pipeline)
