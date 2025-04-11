
import streamlit as st
from chatbot_chain import get_response
from context_tracker import ChatContext
from summarizer import summarize_chat, generate_pdf

st.title("🧑‍⚕️ AI Medical Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []
    st.session_state.ctx = ChatContext()
    st.session_state.user_info = {}

if "name" not in st.session_state.user_info:
    with st.form("patient"):
        st.subheader("👤 Enter Patient Info")
        name = st.text_input("Name")
        age = st.text_input("Age")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        if st.form_submit_button("Start"):
            st.session_state.user_info = {"name": name, "age": age, "gender": gender}
            st.rerun()

st.subheader("💬 Ask a Question")
query = st.text_area("Enter your symptoms or question")

if st.button("Submit"):
    answer = get_response(query, st.session_state.ctx, **st.session_state.user_info)
    st.session_state.chat.append({"Patient": query, "Doctor": answer})

if st.session_state.chat:
    st.subheader("📜 Chat History")
    for c in st.session_state.chat[::-1]:
        st.markdown(f"**You:** {c['Patient']}")
        st.markdown(f"**Doctor:** {c['Doctor']}")
        st.markdown("---")

    if st.button("🧠 Summarize Diagnosis"):
        summary = summarize_chat(st.session_state.chat)
        st.text_area("📝 Summary", value=summary, height=150)

    if st.button("📄 Download PDF"):
        path = generate_pdf(st.session_state.chat, st.session_state.user_info)
        with open(path, "rb") as f:
            st.download_button("Download PDF", f, file_name="summary.pdf")

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat = []
        st.session_state.ctx = ChatContext()
        st.rerun()
