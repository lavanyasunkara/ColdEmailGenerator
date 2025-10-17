import os

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import  OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0,groq_api_key=os.getenv("GROQ_API_KEY"),model_name="llama-3.1-8b-instant")

    def extract_job(self,cleaned_text):
            prompt_extract = PromptTemplate.from_template(
                """
                ### SCRAPED TEXT FROM WEBSITE:
                {page_data}
                ### INSTRUCTION:
                The scraped text is from the career's page of a website.
                Your job is to extract the job postings and return them in JSON format containing the 
                following keys: `role`, `experience`, `skills` and `description`.
                Only return the valid JSON.
                ### VALID JSON (NO PREAMBLE):    
                """
            )

            chain_extract = prompt_extract | self.llm
            res = chain_extract.invoke(input={'page_data': cleaned_text})
            try:
                json_parser=JsonOutputParser()
                res=json_parser.parse(res.content)
            except OutputParserException:
                raise OutputParserException("Context too big.Unable to parse jobs")
            return res if isinstance(res,list) else [res]

    def write_email(self, job, resume_text):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CANDIDATE RESUME:
            {resume}

            ### INSTRUCTION:
            You are an expert career coach and professional recruiter who writes highly personalized and effective cold emails for job seekers.

            ### Task
            Read both the job description and the candidate's résumé above. Compose a **cold email** that the candidate can send to a hiring manager or recruiter.

            ### Guidelines
            1. **Tone** – Polite, confident, and concise (100–150 words).
            2. **Structure** –
               - **Opening**: Introduce yourself briefly (based on résumé highlights).
               - **Middle**: Mention relevant skills and explain the projects, or experiences that align with this specific job description.
               - **Closing**: Express enthusiasm and include a call to action such as “I’d be happy to share more details or discuss how I could contribute.”
            3. **Add a subject line** for the email.
            4. **Output Format**:
               - Subject:
               - Body:

            ### OUTPUT (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res1 = chain_email.invoke({"job_description": str(job), "resume": resume_text})
        return res1.content



