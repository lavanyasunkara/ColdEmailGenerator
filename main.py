import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import os
import PyPDF2
os.environ["USER_AGENT"] = "lavanya-ml-app/1.0"

from chain import Chain
#from portfolio import Portfolio
from utils import clean_text
from io import StringIO

def create_streamlit_app(llm,clean_text):
    st.title("Cold Mail Generator")
    uploaded_file = st.file_uploader("Choose a file")
      # add this import at top

    if uploaded_file is not None:
        # If it’s a PDF file, extract text
        if uploaded_file.name.lower().endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            string_data = ""
            for page in pdf_reader.pages:
                string_data += page.extract_text() or ""
        else:
            # For txt/docx files, fallback
            string_data = uploaded_file.getvalue().decode(errors="ignore")

       # st.text_area("Resume Preview", string_data[:1500], height=250)
    url_input=st.text_input("Enter URL:",value="https://www.amazon.jobs/en/jobs/3105047/agentic-ai-teacher-agi-data-services")
    submit_button=st.button("Submit")

    if submit_button:
        try:
            loader=WebBaseLoader([url_input])
            data= clean_text(loader.load().pop().page_content)

            jobs=llm.extract_job(data)


            if isinstance(jobs, dict):
                jobs = [jobs]

            for i, job in enumerate(jobs, start=1):
                st.subheader(f"Job {i}: {job.get('role', 'Unknown Role')}")
                #st.write("**Skills:**", job.get('skills', []))



                email = llm.write_email(job, string_data)
                st.markdown("**Generated Email:**")
                st.code(email or "⚠️ No email generated", language="markdown")

        except Exception as e:
            st.error(e)

if __name__ == "__main__":
    chain=Chain()
    #portfolio = Portfolio()
    st.set_page_config(layout="wide",page_title="Cold Mail Generator")
    create_streamlit_app(chain,clean_text)

