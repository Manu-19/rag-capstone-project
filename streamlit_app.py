import streamlit as st
import requests
import json

API_QUERY = "http://localhost:8000/api/v1/query"
API_ADMIN_UPLOAD = "http://localhost:8000/api/v1/admin/upload"

st.set_page_config(page_title="RAG Assistant", layout="wide")


st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
[data-testid="stChatMessage"] {
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)


if "role" not in st.session_state:
    st.session_state.role = None

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.title("Navigation")
    if st.session_state.role:
        st.markdown(f"**Role:** {st.session_state.role.capitalize()}")
        if st.button("Logout"):
            st.session_state.role = None
            st.session_state.messages = []
            st.rerun()

# Login Page

if st.session_state.role is None:
    st.title("Login")

    role = st.selectbox("Select Role", ["User", "Admin"])

    if role == "Admin":
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if password == "admin123":
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("Invalid password")
    else:
        if st.button("Continue"):
            st.session_state.role = "user"
            st.rerun()

    st.stop()


if st.session_state.role == "admin":
    st.title(" Document Upload (Admin)")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file and st.button("Upload"):
        try:
            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }
            response = requests.post(API_ADMIN_UPLOAD, files=files)

            if response.status_code == 200:
                st.success(f"Uploaded: {uploaded_file.name}")
            else:
                st.error(response.text)
        except Exception as e:
            st.error(str(e))


if st.session_state.role == "user":
    st.title("Intelligent Credit‑Risk RAG Assistant")

    # Optional metadata
    st.subheader("User Profile Details (Optional)")
    user_data_text = st.text_area(
        "Enter User Details as JSON",
        placeholder='{ "customer_id": "BORR001",  "employment_type": "Salaried",   "loan_type": "Personal Loan", ... }'
    )

  
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            if msg["role"] == "assistant":
                st.markdown("### Source Information")
                st.markdown(f"**Document Name:** {msg.get('document_name', 'NA')}")
                st.markdown(f"**Page No.:** {msg.get('page_no', 'NA')}")
                st.markdown(f"**Section:** {msg.get('section', 'NA')}")

                chunks = msg.get("chunks", [])
                if not chunks:
                    st.markdown("No citation text available.")
                else:
                    for i, chunk in enumerate(chunks):
                        st.markdown(f"**Snippet {i+1}:**")
                        st.markdown(chunk)
                        st.markdown("---")

    
    if prompt := st.chat_input("Ask your question..."):

        # Parse user metadata safely
        try:
            user_data = json.loads(user_data_text) if user_data_text.strip() else {}
        except json.JSONDecodeError:
            st.error("Invalid JSON in user metadata")
            user_data = {}

        query = prompt + " " + str(user_data)

    
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

       
        try:
            response = requests.post(API_QUERY, json={"query": query})
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            st.error(f"Backend error: {e}")
            st.stop()

        answer = data.get("answer", "No answer found.")
        document_name = data.get("document_name", "NA")
        page_no = data.get("page_no", "NA")
        section = data.get("section", "NA")
        chunks = data.get("chunks", [])

        
        with st.chat_message("assistant"):
            if "No relevant data found" in answer:
                st.markdown(answer)
            else:
                st.markdown(answer)

                st.markdown("### Source Information")
                st.markdown(f"**Document Name:** {document_name}")
                st.markdown(f"**Page No.:** {page_no}")
                st.markdown(f"**Section:** {section}")

            # if not chunks:
            #     st.markdown("No citation text available.")
            # else:
            for i, chunk in enumerate(chunks):
                st.markdown(f"**Snippet {i+1}:**")
                st.markdown(chunk)
                st.markdown("---")

        # Save assistant response
        if "No relevant data found" not in answer:
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "document_name": document_name,
                "page_no": page_no,
                "section": section,
                # "chunks": chunks
            })



