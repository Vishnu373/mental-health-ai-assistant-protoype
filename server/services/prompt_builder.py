import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict
from services.prompts import info_collection_prompt, therapy_prompt

def remaining_information(context: Dict) -> str:
    profile_status = context["profile_status"]
    recent_history = context["recent_history"]
    conversation_state = context["conversation_state"]
    
    # Build context information for the LLM
    context_info = """**CURRENT SESSION CONTEXT:**
"""
    
    if profile_status["profile_exists"]:
        completed = ", ".join(profile_status["completed_fields"]) if profile_status["completed_fields"] else "None"
        missing = ", ".join(profile_status["missing_fields"]) if profile_status["missing_fields"] else "None"
        
        context_info += f"""- Profile completion: {profile_status["completion_percentage"]:.0f}%
- Fields already collected: {completed}
- Still needed: {missing}
- Conversation state: {conversation_state}
"""
    else:
        context_info += f"""- New user: No profile exists yet
- Conversation state: {conversation_state}
- Need to start with data consent
"""
    
    if recent_history:
        context_info += f"""- Recent conversation history: {len(recent_history)} recent messages
- Continue naturally from where you left off
"""
    else:
        context_info += """- No recent conversation history
- This is the start of your interaction
"""
    
    remaining_info_collection_prompt = context_info + "\n\n" + info_collection_prompt
    
    return remaining_info_collection_prompt
