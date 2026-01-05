import os

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Local dev only; on Streamlit Cloud, use Secrets -> environment variables
load_dotenv()

def _get_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(
            f"Missing environment variable: {name}. "
            f"Set it in Streamlit Cloud: App → Settings → Secrets."
        )
    return val

def _truncate(text: str, max_chars: int = 12000) -> str:
    """Prevent huge inputs from blowing context / causing messy output."""
    text = text or ""
    return text[:max_chars]

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=_get_env("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
        )

        # Create once (minor efficiency)
        self.json_parser = JsonOutputParser()

    def extract_job(self, cleaned_text: str):
        cleaned_text = _truncate(cleaned_text, max_chars=12000)

        prompt_extract = PromptTemplate.from_template(
            """
You are given scraped text from a careers page.

Return ONLY valid JSON (no markdown, no commentary).
If multiple jobs exist, return a JSON ARRAY of objects.
If a field is missing, use an empty string "" or empty list [].

JSON keys required for each job:
- role (string)
- experience (string)
- skills (list of strings)
- description (string)

SCRAPED TEXT:
{page_data}

OUTPUT (VALID JSON ONLY):
            """.strip()
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke({"page_data": cleaned_text})

        # Try parsing
        try:
            parsed = self.json_parser.parse(res.content)
        except OutputParserException:
            # One retry with even stricter instruction (common fix)
            retry_prompt = PromptTemplate.from_template(
                """
Fix the following output into VALID JSON ONLY.
No markdown, no extra text.
If it's a single object, keep it as an object.
If multiple, output an array.

TEXT TO FIX:
{bad_output}

OUTPUT (VALID JSON ONLY):
                """.strip()
            )
            retry_chain = retry_prompt | self.llm
            retry = retry_chain.invoke({"bad_output": res.content})

            try:
                parsed = self.json_parser.parse(retry.content)
            except OutputParserException as e:
                raise OutputParserException(
                    "Unable to parse job details as JSON. "
                    "Try a different URL or a simpler page."
                ) from e

        # Normalize to list
        return parsed if isinstance(parsed, list) else [parsed]

    def write_email(self, job, resume_text: str):
        # Truncate resume too (prevents context blow-up)
        resume_text = _truncate(resume_text, max_chars=12000)

        prompt_email = PromptTemplate.from_template(
            """
Write a cold email for a hiring manager/recruiter.

Constraints:
- 100–150 words
- Polite, confident, concise
- Must include a subject line
- Use resume highlights relevant to the job
- No preamble, no explanations

JOB (JSON/object):
{job_description}

RESUME TEXT:
{resume}

OUTPUT FORMAT:
Subject: ...
Body: ...
            """.strip()
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": job, "resume": resume_text})
        return res.content
