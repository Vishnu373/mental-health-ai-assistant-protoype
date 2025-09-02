from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chat_models import init_chat_model
from chroma_utils import vectorstore

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

output_parser = StrOutputParser()

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])



# Onbarding questions prompt
qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a friendly companion who knows the user personally. 
Your goal is to collect the following details casually over multiple turns: 
- Age
- Gender
- Current role
- Relationship status
- Religious/spiritual preference & importance
- Current mental/emotional state
- Living situation
- Preferred tone

Rules:
1. Only ask 1-2 questions per turn.
2. Ask missing info in a natural way, like part of normal conversation.
3. Do NOT ask questions already answered (use memory/db to track).
4. Acknowledge answers and respond warmly.
5. Stop onboarding when all required fields are collected.
6. Maintain small talk and empathy throughout.


Always prioritize empathy, clarity, and safety."""

    ),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

def get_rag_chain():
    llm = init_chat_model("us.anthropic.claude-3-5-haiku-20241022-v1:0", model_provider="bedrock_converse")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return rag_chain



