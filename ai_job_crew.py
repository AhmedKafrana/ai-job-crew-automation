# ai_job_crew.py

"""
AI-powered Job Search Automation with CrewAI Agents

Automates the search, extraction, and summarization of job postings
using the CrewAI framework, Tavily Search API, and ScrapeGraph.
"""

import os
import json
from typing import List
from pydantic import BaseModel, Field

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from tavily import TavilyClient
from scrapegraph_py import Client
import agentops

# === Configuration ===

OUTPUT_DIR = "./ai-agent-output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SCRAPEGRAPH_API_KEY = os.getenv("SCRAPEGRAPH_API_KEY")

# === Initialize AgentOps ===
agentops.init(
    api_key=AGENTOPS_API_KEY,
    skip_auto_end_session=True,
    default_tags=['crewai']
)

# === LLM and Clients ===
basic_llm = LLM(model="gpt-4o", temperature=0)
search_client = TavilyClient(api_key=TAVILY_API_KEY)
scrape_client = Client(api_key=SCRAPEGRAPH_API_KEY)

# === Step 1: Search Query Generation Agent ===

NUM_QUERIES = 10

class SuggestedSearchQueries(BaseModel):
    queries: List[str] = Field(
        ..., title="Suggested search queries for job postings",
        min_items=1, max_items=NUM_QUERIES
    )

search_queries_recommendation_agent = Agent(
    role="Job Search Queries Recommendation Agent",
    goal=(
        "Generate a list of optimized Google search queries for specific job titles and countries "
        "using best search practices and operators."
    ),
    backstory=(
        "Expert at constructing search engine queries to maximize the relevancy of job search results."
    ),
    llm=basic_llm, verbose=True
)

search_queries_recommendation_task = Task(
    description=(
        "Generate up to {no_keywords} Google job search queries for the following job titles: {jobs_titles}. "
        "Focus on jobs in {country_name}, in {language}. "
        "Leverage Google search operators (quotes, OR, intitle:, inurl:) and best practices."
    ),
    expected_output="A JSON object containing suggested search queries.",
    output_json=SuggestedSearchQueries,
    output_file=os.path.join(OUTPUT_DIR, "step_1_suggested_job_search_queries.json"),
    agent=search_queries_recommendation_agent
)

# === Step 2: Search Engine Agent ===

class SingleSearchResult(BaseModel):
    title: str
    url: str
    content: str
    search_query: str

class AllSearchResults(BaseModel):
    results: List[SingleSearchResult] = Field(..., min_items=20)

@tool
def search_engine_tool(query: str):
    """Search for job postings using the Tavily API."""
    return search_client.search(query)

search_engine_agent = Agent(
    role="Job Search Engine Agent",
    goal="Retrieve at least 20 high-quality job postings for specified search queries.",
    backstory="Specialist in gathering and filtering job postings from multiple sources.",
    llm=basic_llm, verbose=True, tools=[search_engine_tool]
)

search_engine_task = Task(
    description=(
        "Using suggested Google search queries, collect at least 20 job postings. "
        "Include title, URL, snippet, and the originating search query."
    ),
    expected_output="A JSON list of at least 20 job postings.",
    output_json=AllSearchResults,
    output_file=os.path.join(OUTPUT_DIR, "step_2_job_search_results.json"),
    agent=search_engine_agent
)

# === Step 3: Scraping Agent ===

class JobSpec(BaseModel):
    specification_name: str
    specification_value: str

class SingleExtractedJob(BaseModel):
    page_url: str
    job_title: str
    company_name: str
    location: str
    job_posting_url: str
    job_posting_date: str
    salary: str = None
    job_specs: List[JobSpec]
    agent_recommendation_rank: int
    agent_recommendation_notes: List[str]

class AllExtractedJobs(BaseModel):
    jobs: List[SingleExtractedJob]

@tool
def web_scraping_tool(page_url: str):
    """Extract structured job data from a job posting page."""
    details = scrape_client.smartscraper(
        website_url=page_url,
        user_prompt=f"Extract ```json\n{SingleExtractedJob.schema_json()}\n``` from the job posting web page."
    )
    return {"page_url": page_url, "details": details}

scraping_agent = Agent(
    role="Job Web Scraping Agent",
    goal="Extract detailed, structured, and ranked job information from posting URLs.",
    backstory="Expert at parsing job details for candidate decision-making.",
    llm=basic_llm, verbose=True, tools=[web_scraping_tool]
)

scraping_task = Task(
    description=(
        "From the provided URLs, extract structured details for each job posting: "
        "title, company, location, date, salary (if present), and up to 5 specs. "
        "Add recommendation notes and rank each job."
    ),
    expected_output="A JSON object with all extracted job details.",
    output_json=AllExtractedJobs,
    output_file=os.path.join(OUTPUT_DIR, "step_3_extracted_jobs.json"),
    agent=scraping_agent
)

# === Step 4: Recruitment Report Author Agent ===

recruitment_report_author_agent = Agent(
    role="Recruitment Report Author Agent",
    goal="Generate a professional, Bootstrap-styled HTML report summarizing all jobs.",
    backstory="Expert in creating clear, actionable recruitment reports.",
    llm=basic_llm, verbose=True
)

recruitment_report_author_task = Task(
    description=(
        "Create a Bootstrap-styled HTML page with a job table including: job title, company, location, date, salary, "
        "direct job links, and a summary for each job."
    ),
    expected_output="An HTML file with a responsive job report.",
    output_file=os.path.join(OUTPUT_DIR, "step_4_recruitment_report.html"),
    agent=recruitment_report_author_agent
)

# === Crew Assembly and Execution ===

rankyx_crew = Crew(
    agents=[
        search_queries_recommendation_agent,
        search_engine_agent,
        scraping_agent,
        recruitment_report_author_agent,
    ],
    tasks=[
        search_queries_recommendation_task,
        search_engine_task,
        scraping_task,
        recruitment_report_author_task,
    ],
    process=Process.sequential
)

if __name__ == "__main__":
    crew_results = rankyx_crew.kickoff(
        inputs={
            "jobs_titles": "AI/ML Engineer",
            "country_name": "Egypt",
            "no_keywords": NUM_QUERIES,
            "language": "English"
        }
    )
    print("Job search automation complete. See output in", OUTPUT_DIR)
