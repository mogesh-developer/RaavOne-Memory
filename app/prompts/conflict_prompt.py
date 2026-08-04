CONFLICT_RESOLUTION_PROMPT = """
You are an AI Memory Consolidation Engine.

Your task is to analyze if a new memory contradicts, updates, or replaces any of the existing user memories in the same category.

New Memory:
"{new_memory}"

Existing Memories in the same category:
{existing_memories}

Determine if the new memory is an update/replacement for an existing memory.
- If it is an update, return the exact ID of the existing memory that needs to be updated and the new updated content.
- If it is a completely new memory and does not conflict with or replace any existing memories, return null for both fields.

Return ONLY valid JSON matching this schema:
{{
    "updates_id": null or integer,
    "merged_content": null or string
}}
"""
