"""RAG pipeline for therapy mode."""
from prompts.templates import therapy_prompt
from app.config import llm_model, supabase, embedding_model
from langchain_core.messages import SystemMessage, HumanMessage


def retrieve(query: str, match_count: int = 3) -> str:
    """Retrieve relevant therapy content from vector store."""
    results = supabase.rpc(
        'match_data', {
            'query_embedding': embedding_model.embed_query(query),
            'match_threshold': 0.1,
            'match_count': match_count
        }
    ).execute()

    all_matches = [r.get('content', '') for r in results.data if r.get('content')]
    return "\n\n".join(all_matches)


def augment_and_generate(user_profile, retrieved_content: str, conversation_history: str, user_message: str) -> str:
    """Augment prompt with context and generate response."""
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

    messages = [SystemMessage(content=augmented_prompt), HumanMessage(content=user_message)]
    return llm_model.invoke(messages).content
