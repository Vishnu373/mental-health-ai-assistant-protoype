# Architecture

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

---

## System Flow

```
                              User Message
                                   │
                                   ▼
                          ┌────────────────┐
                          │  FastAPI /chat │
                          └───────┬────────┘
                                  │
                                  ▼
                          ┌────────────────┐
                          │ Mode Switcher  │
                          │ (Profile Check)│
                          └───────┬────────┘
                                  │
              ┌───────────────────┴───────────────────┐
              │ Required fields filled?               │
              ▼ NO                                YES ▼
┌─────────────────────────┐            ┌─────────────────────────┐
│   INFO COLLECTION MODE  │            │      THERAPY MODE       │
├─────────────────────────┤            ├─────────────────────────┤
│ LangChain Conversation  │            │ Profile Retrieval       │
│         ↓               │            │         ↓               │
│ Field Detection         │            │ Query Creation          │
│         ↓               │            │         ↓               │
│ Data Extraction (LLM)   │            │ Vector Search (Supabase)│
│         ↓               │            │         ↓               │
│ PostgreSQL Update       │            │ RAG Pipeline + LLM      │
│         ↓               │            │         ↓               │
│ Friendly AI Response    │            │ Therapeutic Response    │
└───────────┬─────────────┘            └─────────────────────────┘
            │                                          ^
            │ Once all required fields filled          |
            └──────────────────────────────────────────┘
                         ↑ Auto-switches to Therapy Mode
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI (Python) |
| **LLM** | Claude 3.5 Haiku via AWS Bedrock |
| **Embeddings** | Amazon Titan Embed v2 |
| **Database** | PostgreSQL (Supabase) |
| **Vector Store** | Supabase pgvector |
| **Frontend** | React + Vite |
| **Auth** | Clerk |
| **Storage** | AWS S3 (knowledge base) |

---

## Backend Structure

```
server/
├── app/
│   ├── main.py          # API endpoints
│   └── config.py        # External clients
├── core/
│   ├── fields.py        # Dynamic field detection
│   ├── session.py       # Session utilities
│   ├── summary.py       # Conversation summarization
│   └── modes/
│       ├── info_collection.py
│       ├── therapy.py
│       └── switcher.py
├── db/
│   ├── models.py        # SQLAlchemy tables
│   └── schemas.py       # Pydantic schemas
└── prompts/
    └── templates.py     # LLM prompts
```

---

## Frontend Structure

```
client/src/
├── App.jsx              # Route definitions
├── main.jsx             # Entry point + providers
├── api/
│   └── chat.js          # API calls to backend
├── auth/
│   └── clerk-provider.jsx
├── components/
│   ├── ChatContainer.jsx
│   ├── MessageList.jsx
│   └── MessageInput.jsx
├── pages/
│   ├── ChatPage.jsx
│   ├── SignInPage.jsx
│   └── SignUpPage.jsx
└── styles/
    └── app.css
```

---

## Key Features

### Dynamic Field Collection
- Fields defined in `db/schemas.py` (Pydantic model)
- No hardcoded keyword detection
- LLM extracts values from natural conversation

### Conversation Summarization
- On session end, conversation is summarized
- Summary stored in `session_summaries` table
- Fed to LLM when returning user resumes

### RAG Pipeline
- User conditions → embedding → vector search
- Retrieved content augments therapy prompt
- Personalized responses based on user profile

---

## Database Tables

| Table | Purpose |
|-------|---------|
| `user_profile` | Stores all user data (mandatory + optional fields) |
| `chats` | Conversation history (user_id, session_id, messages) |
| `session_summaries` | LLM-generated summaries for context persistence |
