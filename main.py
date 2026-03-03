import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel
from typing import List
from pypdf import PdfReader

# -------------------------
# Initialize LLM (UPDATED)
# -------------------------
llm = ChatOllama(
    model="llama3.1",   # You already have this
    temperature=0
)

# -------------------------
# Pydantic Models
# -------------------------

class JobDetails(BaseModel):
    job_title: str
    required_skills: List[str]
    experience_required: int
    tools: List[str]
    soft_skills: List[str]


class ResumeSuggestions(BaseModel):
    missing_skills: List[str]
    improvement_points: List[str]
    overall_fit_summary: str


# -------------------------
# Parsers
# -------------------------

job_parser = PydanticOutputParser(pydantic_object=JobDetails)
resume_parser = PydanticOutputParser(pydantic_object=ResumeSuggestions)
cover_letter_parser = StrOutputParser()


# -------------------------
# Prompts
# -------------------------

job_prompt = PromptTemplate(
    template="""
You are an information extraction system.

Extract structured information from the job description.

Return ONLY valid JSON.
No explanation.
No markdown.

{format_instructions}

Job Description:
{job_description}
""",
    input_variables=["job_description"],
    partial_variables={
        "format_instructions": job_parser.get_format_instructions()
    },
)

resume_prompt = PromptTemplate(
    template="""
You are an AI career coach.

Compare the job details with the resume and provide structured suggestions.

{format_instructions}

Job Details:
{job_details}

Resume:
{resume}
""",
    input_variables=["job_details", "resume"],
    partial_variables={
        "format_instructions": resume_parser.get_format_instructions()
    },
)

cover_letter_prompt = PromptTemplate(
    template="""
Write a professional and concise cover letter.

Job Title: {job_title}

Job Details:
{job_details}

Candidate Resume:
{resume}

Return only the cover letter text.
""",
    input_variables=["job_title", "job_details", "resume"],
)

# -------------------------
# Chains
# -------------------------

job_chain = job_prompt | llm | job_parser
resume_chain = resume_prompt | llm | resume_parser
cover_letter_chain = cover_letter_prompt | llm | cover_letter_parser


# -------------------------
# Streamlit UI
# -------------------------

st.set_page_config(page_title="AI Job Assistant", layout="wide")
st.title("🤖 AI Job Application Assistant (Local — Ollama)")

st.subheader("📄 Paste Job Description")
job_description = st.text_area("Job Description", height=250)

st.subheader("📎 Upload Resume (PDF)")
uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

resume_text = ""

if uploaded_file is not None:
    try:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text
        st.success("Resume uploaded successfully!")
    except Exception:
        st.error("Error reading PDF file.")

# -------------------------
# Run Analysis
# -------------------------

if st.button("🚀 Analyze & Generate"):

    if not job_description:
        st.warning("Please paste a job description.")
    elif not resume_text:
        st.warning("Please upload a valid resume PDF.")
    else:

        with st.spinner("Analyzing with local AI model..."):

            # Feature 1 — Extract Job Details
            job_details = job_chain.invoke({
                "job_description": job_description
            })

            # Feature 2 — Resume Suggestions
            suggestions = resume_chain.invoke({
                "job_details": job_details,
                "resume": resume_text
            })

            # Feature 3 — Cover Letter
            cover_letter = cover_letter_chain.invoke({
                "job_title": job_details.job_title,
                "job_details": job_details,
                "resume": resume_text
            })

        st.success("Analysis Complete!")

        st.subheader("📊 Extracted Job Details")
        st.json(job_details.model_dump())

        st.subheader("🛠 Resume Improvement Suggestions")
        st.json(suggestions.model_dump())

        st.subheader("✉️ Generated Cover Letter")
        st.text_area("Cover Letter", cover_letter, height=300)

        st.download_button(
            "⬇ Download Cover Letter",
            cover_letter,
            file_name="cover_letter.txt"
        )