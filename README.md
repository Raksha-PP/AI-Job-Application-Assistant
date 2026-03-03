# AI-Job-Application-Assistant
An AI-powered application that assists candidates in optimizing their job applications. It analyzes job descriptions, evaluates resumes, and generates tailored cover letters. The system runs fully locally using Ollama, ensuring privacy and zero API cost.

## Tech Stack
1. Streamlit – User interface
2. LangChain – LLM workflow management
3. Ollama – Local language model
4. Pydantic – Structured output validation
5. PyPDF – Resume text extraction

## Core Features
-> Job Description Analyzer
-> Extracts structured details such as job title, required skills, experience level, tools, and soft skills.
-> Resume Gap Analysis
-> Compares the uploaded resume with the job description and identifies matching skills, missing skills, improvement areas, and overall fit.
-> Cover Letter Generator
-> Creates a professional, concise, and job-specific cover letter based on the resume and job description.

## Project Structure
-> Main application file
-> Modules for job description analysis, resume parsing, gap analysis, and cover letter generation
-> Schema definitions for structured outputs
-> Utility components for LLM setup and prompt management
-> Upload directory for resume files
-> Dependency configuration file

This project demonstrates practical use of local LLMs for real-world career assistance.
