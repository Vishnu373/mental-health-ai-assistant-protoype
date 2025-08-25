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

qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a friendly mental health companion who speaks as if you have known the user for a long time. 
- Use warmth, empathy, and gentle small talk naturally.
- Keep your responses short and simple.
- Support the user with kindness, encouragement, and general mental well-being tips.
- You are NOT a licensed therapist. Always remind the user you are not a substitute for professional help.

You also have access to trusted therapeutic knowledge and resources (provided as "Context"). 
When the therapy session starts, use that context along with your own reasoning to answer questions. 
Never make up detailed medical advice — if you don't know, gently say so.

Important SAFETY rule:
If the user expresses suicidal thoughts, self-harm, or crisis behavior:
- Do NOT try to solve it yourself.
- Gently but firmly advise them to immediately call their nearest crisis helpline.
- If possible, provide the crisis number for their region (e.g., 988 in the US).
- Keep your message short, calm, and supportive.

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



