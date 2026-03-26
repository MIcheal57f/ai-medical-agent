import streamlit as st
from prompt import system_prompt
from services.agent import medical_agent
st.title("AI 医疗咨询助手")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

if "sources" not in st.session_state:
    st.session_state.sources = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("请输入你的症状")

if question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    messages_to_send = st.session_state.messages[-10:]

    answer, sources = medical_agent(
        question,
        st.session_state.messages
    )

    with st.chat_message("assistant"):
        st.write(answer)

        st.write("参考来源：")
        for s in sources:
            st.write(s)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    st.session_state.sources = sources
