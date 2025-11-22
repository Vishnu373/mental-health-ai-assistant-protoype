from modes.conversation import Conversation
from database.user_profile_db import UserProfile, SessionLocal
from sqlalchemy import Integer, Boolean
from config import llm_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from threading import Thread
from prompts.info_collection_prompt import INFO_COLLECTION_PROMPT

class InfoCollectionMode:
    def __init__(self, user_id):
        self.user_id = user_id
        self.conversation = Conversation(user_id)
        
        # Check if returning user
        self.is_returning = self.conversation.is_returning_user()
        
        # Get last session summary for context (if returning)
        self.last_session_summary = None
        if self.is_returning:
            self.last_session_summary = self.conversation.get_last_session_summary()
        
        # Always create new session
        self.session_id = self.conversation.start_session()
        self.tool = self.extraction_tool()

    # 1. user information fields schema designed using the user_profile table
    def extraction_tool(self):
        properties = {}

        for column in UserProfile.__table__.columns:
            if column.name in ["user_id", "created_at", "updated_at"]:
                continue

            properties[column.name] = {
                            "type": "integer" if isinstance(column.type, Integer) else 
                                    "boolean" if isinstance(column.type, Boolean) else "string"
            }

        return {
            "name": "user_information",
            "description": "extract the user information from the conversations",
            "input_schema": {
                "type": "object",
                "properties": properties
                }
        }
    
    # 2. Communicate with the user and extract useful details
    def chat_and_extract(self, user_message, prompt):
        # 0. Chat logic (same as base_conversation) with info_collection_mode set
        history = self.conversation.get_conversation_history()
        
        messages = [SystemMessage(content=prompt)]
        
        if history:
            for user_msg, ai_msg in history:
                messages.append(HumanMessage(content=user_msg))
                messages.append(AIMessage(content=ai_msg))
        
        messages.append(HumanMessage(content=user_message))
        
        # 1. Extraction logic using anthropic function calling
        response = llm_model.invoke(
            messages,
            tools=[self.tool],
            tool_choice={"type": "auto"}
        )
        
        ai_response = response.content
        self.conversation.save_conversation_history(user_message, ai_response)
        
        # 2. Extract the data
        if hasattr(response, 'tool_calls') and response.tool_calls:
            extracted_data = response.tool_calls[0]['args']
            Thread(target=self.store_information, args=(extracted_data,), daemon=True).start()
        
        return ai_response

    # 3. Store the extracted details into the db
    def store_information(self, extracted_data):
        db = SessionLocal()

        try:
            profile = db.query(UserProfile).filter(
                UserProfile.user_id == self.user_id
            ).first()

            if not profile:
                profile = UserProfile(user_id = self.user_id)
                db.add(profile)

            for field, value in extracted_data.items():
                if hasattr(profile, field):
                    setattr(profile, field, value)

            db.commit()
            print(f"✓ Saved: {extracted_data}")

        except Exception as e:
            print(f"✗ DB error: {e}")
            db.rollback()
        
        finally:
            db.close()

    # 4. Main pipeline - production entry point
    def run_pipeline(self, user_message):
        info_collection_prompt = INFO_COLLECTION_PROMPT

        # Add last session context to prompt if returning user
        if self.last_session_summary:
            info_collection_prompt += f"\n\nPrevious session context: {self.last_session_summary}"
        
        # Chat + extract + store (store happens async in chat_and_extract)
        return self.chat_and_extract(user_message, info_collection_prompt)


"""
if __name__ == "__main__":
    print("\n=== InfoCollectionMode Test ===")
    
    # Test setup
    test_user_id = "test_user_123"
    test_session_id = "test_session_456"
    
    # Initialize mode
    info_mode = InfoCollectionMode(test_user_id, test_session_id)
    
    print(f"\nUser ID: {test_user_id}")
    print(f"Session ID: {test_session_id}")
    print("\n" + "="*50)
    
    # Interactive chat loop
    print("\nStart chatting! (Type 'quit' to exit)\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nEnding conversation...")
            break
        
        # Get AI response
        ai_response = info_mode.chat_and_extract(user_input, INFO_COLLECTION_PROMPT)
        
        print(f"\nAI: {ai_response}\n")
    
    # Check what was saved in DB
    print("\n" + "="*50)
    print("\nChecking database...\n")
    
    db = SessionLocal()
    profile = db.query(UserProfile).filter(UserProfile.user_id == test_user_id).first()
    
    if profile:
        print("✓ Profile found in database!\n")
        print("Extracted fields:")
        for column in UserProfile.__table__.columns:
            if column.name not in ["user_id", "created_at", "updated_at"]:
                value = getattr(profile, column.name)
                if value is not None:
                    print(f"  - {column.name}: {value}")
    else:
        print("✗ No profile found in database")
    
    db.close()
    print("\n" + "="*50)
"""