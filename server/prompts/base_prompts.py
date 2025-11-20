SESSION_METADATA_PROMPT = """Analyze this conversation and provide:
1. A short title (max 6 words)
2. A detailed summary capturing:
   - Key topics discussed
   - User's concerns or emotional state
   - Important details shared
   - Any progress or insights

Conversation:
{conversation}

Respond in this exact format:
Title: [your title here]
Summary: [your summary here]"""
