from langchain_aws import BedrockEmbeddings
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from services.prompts import therapy_prompt
from config import llm_model, s3, supabase, BUCKET_NAME, KB_KEY, embedding_model
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# Retrieve relevant therapy content
def retrieve(query, match_count=3):
    results = supabase.rpc(
        'match_data', {
            'query_embedding': embedding_model.embed_query(query),
            'match_threshold': 0.1,
            'match_count': match_count
        }
    ).execute()

    results = results.data
    all_matches = [result.get('content', '') for result in results if result.get('content')]
    all_matches = "\n\n".join(all_matches)
    
    return all_matches
    

# Augment prompt creation + Generate LLM response
def augment_and_generate(user_profile, retrieved_content, conversation_history="", user_message=""):
    augmented_prompt = therapy_prompt.format(
        retrieved_content=retrieved_content,
        age=getattr(user_profile, 'age', 'Not specified'),
        platform_goals=getattr(user_profile, 'platform_goals', 'Not specified'),
        mental_health_rating=getattr(user_profile, 'mental_health_rating', 'Not specified'),
        sleep_quality=getattr(user_profile, 'sleep_quality', 'Not specified'),
        stress_frequency=getattr(user_profile, 'stress_frequency', 'Not specified'),
        employment_status=getattr(user_profile, 'employment_status', 'Not specified'),
        relationship_status=getattr(user_profile, 'relationship_status', 'Not specified'),
        upbringing_description=getattr(user_profile, 'upbringing_description', 'Not specified'),
        ai_communication_style=getattr(user_profile, 'ai_communication_style', 'Conversational'),
        mental_health_conditions=getattr(user_profile, 'mental_health_conditions', 'None specified'),
        conversation_history=conversation_history
    )
    
    messages = [
        SystemMessage(content=augmented_prompt),
        HumanMessage(content=user_message)
    ]
    
    response = llm_model.invoke(messages)
    
    return response.content
