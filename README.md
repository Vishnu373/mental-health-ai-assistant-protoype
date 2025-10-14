# Mental Health AI Assistant

A personalized AI-powered mental health support system that provides tailored therapeutic guidance through an intelligent two-phase conversation approach.
Try it out at: [MhelpAI](https://mental-health-ai-assistant-protoype.vercel.app)

## How It Works

The assistant operates in two distinct modes that seamlessly transition based on user profile completeness:

### Info Collection Mode

```
User Message → LangChain Conversation → Field Detection → Data Extraction → PostgreSQL Database
     ↓
Friendly AI Response ← Conversation History ← Profile Building
```

The initial phase where the AI acts as a friendly conversational companion to naturally gather personal information from users. This mode uses simple chatbot conversation without any retrieval mechanisms. The AI asks contextual questions about age, mental health goals, stress levels, sleep quality, and other relevant personal details while maintaining an empathetic, non-clinical tone. All collected information is securely stored and used to create a comprehensive user profile.

### Therapy Mode

```
User Message → Profile Retrieval → Query Creation → Vector Search (Supabase)
     ↓                ↓                              ↓
Personalized    +    User Data    +    Retrieved Medical Content
Response        ←    (Database)   ←    (MedlinePlus Knowledge)
     ↑
LangChain RAG Pipeline → Claude 3.5 Haiku → Therapeutic Response
```

Once sufficient personal information is collected, the system automatically transitions to therapy mode. This phase combines the user's profile data with a Retrieval-Augmented Generation (RAG) system that accesses evidence-based mental health knowledge. The AI retrieves relevant therapeutic content based on the user's specific conditions and circumstances, then generates personalized therapeutic responses that consider their unique background, goals, and mental health needs.

## Key Features

- **Seamless Mode Switching**: Users experience a natural flow from information gathering to therapeutic support
- **Personalized Responses**: Every interaction is tailored using the user's complete profile
- **Evidence-Based Content**: Therapeutic guidance backed by reliable mental health resources
- **Conversation Memory**: Maintains context across sessions for continuous support

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Vector Database**: Supabase (pgvector)
- **LLM**: Claude 3.5 Haiku via AWS Bedrock
- **Embeddings**: Amazon Titan Text Embeddings v2
- **Framework**: LangChain for RAG pipeline
- **Data Models**: Pydantic for validation

## Data Attribution

The knowledge base used in therapy mode is built from medical and mental health information provided by [MedlinePlus](https://medlineplus.gov/), ensuring reliable and evidence-based therapeutic content.

---

*This is a proof-of-concept implementation focused on demonstrating personalized mental health AI assistance.*
