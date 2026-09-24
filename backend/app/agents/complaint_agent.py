"""
CIVICFLOW AI — Complaint Understanding Agent
Parses raw citizen complaints, extracts entities & urgency cues, calculates sentiment, and standardizes categories.
"""
import json
import logging
from typing import Optional
import httpx

from app.agents.base import BaseAgent
from app.agents.schemas import ComplaintUnderstandingInput, ComplaintUnderstandingOutput
from app.core.config import settings

logger = logging.getLogger("civicflow.agents.complaint")


class ComplaintUnderstandingAgent(BaseAgent[ComplaintUnderstandingInput, ComplaintUnderstandingOutput]):
    def __init__(self):
        super().__init__(name="ComplaintUnderstandingAgent", version="1.0.0", model_name="gemini-3.8-flash")

    async def _execute_core(self, input_data: ComplaintUnderstandingInput) -> ComplaintUnderstandingOutput:
        if settings.GEMINI_API_KEY:
            try:
                return await self._call_gemini(input_data)
            except Exception as e:
                logger.warning(f"Gemini API call failed in ComplaintUnderstandingAgent: {e}, using heuristic")
        return self._fallback_heuristic(input_data, None)

    async def _call_gemini(self, input_data: ComplaintUnderstandingInput) -> ComplaintUnderstandingOutput:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        system_instruction = (
            "You are an expert civic triage analyst. Analyze this citizen complaint. "
            "Output JSON conforming strictly to: standardized_title, refined_summary, detected_category "
            "(one of: pothole, garbage, water_supply, drainage, streetlights, electricity, sanitation, public_infrastructure), "
            "sentiment_score (-1.0 to 1.0), urgency_cues (list), extracted_entities (dict with landmarks, road, etc.), "
            "confidence (0.0 to 1.0), and reasoning_summary."
        )
        prompt = f"Title: {input_data.title}\nDescription: {input_data.description}\nClaimed Category: {input_data.raw_category}\nLocation: {input_data.location_address}"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "systemInstruction": {"parts": [{"text": system_instruction}]},
                    "generationConfig": {"responseMimeType": "application/json"}
                }
            )
            resp.raise_for_status()
            data = resp.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(raw_text)
            return ComplaintUnderstandingOutput(**parsed)

    def _fallback_heuristic(self, input_data: ComplaintUnderstandingInput, error: Optional[Exception]) -> ComplaintUnderstandingOutput:
        text = f"{input_data.title} {input_data.description}".lower()
        
        # Category detection heuristics
        cat = "public_infrastructure"
        if any(w in text for w in ["pothole", "crater", "road", "asphalt", "flyover", "footpath", "bridge"]):
            cat = "pothole"
        elif any(w in text for w in ["garbage", "trash", "waste", "dump", "debris", "litter"]):
            cat = "garbage"
        elif any(w in text for w in ["water", "pipe", "burst", "leak", "drinking water", "supply"]):
            cat = "water_supply"
        elif any(w in text for w in ["drain", "sewage", "gutter", "overflow", "stagnant"]):
            cat = "drainage"
        elif any(w in text for w in ["light", "streetlight", "dark", "lamp", "pole"]):
            cat = "streetlights"
        elif any(w in text for w in ["electric", "wire", "spark", "transformer", "shock"]):
            cat = "electricity"

        urgency_cues = []
        for cue in ["danger", "school", "hospital", "bus", "swerving", "spark", "child", "accident", "emergency", "severe"]:
            if cue in text:
                urgency_cues.append(cue)

        sentiment = -0.5
        if len(urgency_cues) >= 2:
            sentiment = -0.8
        elif "thank" in text or "please fix" in text:
            sentiment = -0.3

        entities = {}
        if input_data.location_address:
            entities["location"] = input_data.location_address
        if "near" in text:
            parts = text.split("near", 1)
            entities["proximate_landmark"] = parts[1].split(".")[0].strip().title()

        return ComplaintUnderstandingOutput(
            standardized_title=input_data.title.strip().capitalize(),
            refined_summary=f"Citizen reported {cat} issue at {input_data.location_address}. Urgency factors: {', '.join(urgency_cues) if urgency_cues else 'Standard priority'}.",
            detected_category=cat,
            sentiment_score=sentiment,
            urgency_cues=urgency_cues,
            extracted_entities=entities,
            confidence=0.92 if urgency_cues else 0.85,
            reasoning_summary=f"Categorized as '{cat}' via keyword-entity heuristic with {len(urgency_cues)} urgency cues detected."
        )


complaint_agent = ComplaintUnderstandingAgent()
