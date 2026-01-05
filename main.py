import os
from io import BytesIO
import streamlit as st
import PyPDF2
from langchain_community.document_loaders import WebBaseLoader

from chain import Chain
from utils import clean_text

# Good practice: set UA once (some sites block requests without it)
os.environ["USER_AGENT"] = "lavanya-ml-app/1.0"

def extract_text_from_upload(uploaded_file) -> str:
    """Extract plain text from uploaded file (PDF or TXT)."""
    if uploaded_file is None:
        return ""

    name = uploaded_file.name.lower()

    # PDF
    if name.endswith(".pdf"):
        pdf_bytes = uploaded_file.getvalue()
        reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text.strip()

    # TXT fallback
    return uploaded_file.getvalue().decode("utf-8", errors="ignore").strip()


def create_streamlit_app(llm, clean_text_fn):
    st.title("Cold Mail Generator")

    # Restrict types to avoid accidental binary uploads
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or TXT)",
        type=["pdf", "txt"]
    )

    # Always define string_data (prevents NameError)
    string_data = extract_text_from_upload(uploaded_file)

    # Optional preview
    if uploaded_file is not None and string_data:
        with st.expander("Preview extracted resume text"):
            st.text_area("Resume Text (preview)", string_data[:2000], height=250)

    url_input = st.text_input(
        "Enter job URL:",
        value="https://www.amazon.jobs/en/jobs/3105047/agentic-ai-teacher-agi-data-services"
    )

    submit_button = st.button("Submit")

    if submit_button:
        # Validate inputs early (better UX + fewer crashes)
        if not url_input.strip():
            st.error("Please enter a valid URL.")
            return

        if not string_data.strip():
            st.error("Please upload a resume (PDF or TXT) before submitting.")
            return

        try:
            with st.spinner("Loading job page..."):
                loader = WebBaseLoader([url_input])
                page = loader.load().pop()
                data = clean_text_fn(page.page_content)

            with st.spinner("Extracting job details..."):
                jobs = llm.extract_job(data)

            # Normalize to list
            if isinstance(jobs, dict):
                jobs = [jobs]
            elif not isinstance(jobs, list):
                jobs = []

            if not jobs:
                st.warning("No job roles were extracted from the URL content.")
                return

            for i, job in enumerate(jobs, start=1):
                st.subheader(f"Job {i}: {job.get('role', 'Unknown Role')}")

                with st.spinner("Generating email..."):
                    email = llm.write_email(job, string_data)

                st.markdown("**Generated Email:**")
                st.code(email or "⚠️ No email generated", language="markdown")

        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Cold Mail Generator")
    chain = Chain()
    create_streamlit_app(chain, clean_text)
