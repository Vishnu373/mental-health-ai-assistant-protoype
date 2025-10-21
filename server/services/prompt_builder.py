import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict
from services.prompts import info_collection_prompt

def remaining_information(context: Dict) -> str:
    profile_status = context["profile_status"]
    recent_history = context["recent_history"]
    
    context_info = ""
    
    if recent_history:
        # RETURNING USER
        context_info = "**RETURNING USER: Continue your previous conversation naturally.**\n\n"
        
        if profile_status["profile_exists"]:
            completed = ", ".join(profile_status["completed_fields"]) if profile_status["completed_fields"] else "None"
            missing = ", ".join(profile_status["missing_fields"]) if profile_status["missing_fields"] else "None"
            
            context_info += f"Already collected: {completed}\n"
            context_info += f"Still need: {missing}\n\n"
            
            if profile_status["completion_percentage"] > 50:
                context_info += "Don't re-ask questions you already have answers to.\n\n"
    else:
        # NEW USER
        if not profile_status["profile_exists"]:
            context_info = "**NEW USER: Start with data consent.**\n\n"
    
    return context_info + info_collection_prompt
