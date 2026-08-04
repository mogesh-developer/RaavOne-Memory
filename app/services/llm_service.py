from raavone import AIService
from raavone.schemas.memory_extraction import MemoryExtractionResponse
from app.prompts.memory_extraction import MEMORY_EXTRACTION_PROMPT

model = AIService()


def extract_memory(conversation: str) -> MemoryExtractionResponse:

    prompt = f"""
{MEMORY_EXTRACTION_PROMPT}

Conversation:

{conversation}
"""

    return model.generate_json(prompt, MemoryExtractionResponse)
