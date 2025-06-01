import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.schema import SystemMessage, HumanMessage
from langchain_chroma import Chroma


def load_vectordb():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    return vectordb


def retrieve_docs(vectordb, query, k=15):
    docs = vectordb.similarity_search(query, k=k)
    return docs


def run_chatbot():
    st.header("🤖 Chatbot ART + RAG")

    if "llm" not in st.session_state:
        st.session_state.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.0-flash",
            max_output_tokens=512,
            temperature=0.0,
        )
    llm = st.session_state.llm

    if "vectordb" not in st.session_state:
        st.session_state.vectordb = load_vectordb()
    vectordb = st.session_state.vectordb

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Você:", placeholder="Escreva sua mensagem...", key="input_chat"
        )
        enviar = st.form_submit_button("Enviar")

    if enviar and user_input:
        retrieved_docs = retrieve_docs(vectordb, user_input, k=15)
        retrieved_text = (
            "\n\n".join([doc.page_content for doc in retrieved_docs])
            if retrieved_docs
            else ""
        )

        system_content = "Você é um assistente útil. Seja cuidadoso com characters especiais em markdown, por exemplo, se é reais 'R$' use 'R\$'"
        if retrieved_text:
            system_content += (
                "\n\nConsidere as seguintes informações relevantes do contexto:\n"
                + retrieved_text
            )

        system_msg = SystemMessage(content=system_content)
        human_msg = HumanMessage(content=user_input)

        ai_message = llm.predict_messages([system_msg, human_msg])
        resposta = ai_message.content.strip()

        st.session_state.chat_history.append(("Você", user_input))
        st.session_state.chat_history.append(("Chatbot", resposta))

    for speaker, msg in st.session_state.chat_history:
        if speaker == "Você":
            st.markdown(
                f"<div style='text-align: right; color: blue;'><b>Você:</b> {msg}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='text-align: left; color: green;'><b>Chatbot:</b> {msg}</div>",
                unsafe_allow_html=True,
            )

    if st.button("Limpar Conversa"):
        st.session_state.chat_history = []
        st.rerun()
