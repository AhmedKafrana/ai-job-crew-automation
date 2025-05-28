# AI-Powered Job Search Automation with CrewAI

This project automates the process of searching, extracting, and reporting job postings for any role and location using an orchestrated crew of AI agents. It leverages [CrewAI](https://github.com/Vision-CAIR/crewai), Tavily Search API, ScrapeGraph, and modern LLMs.

---

## Features

- **Automated Query Generation:** Creates optimized Google search queries for target roles and locations.
- **Intelligent Web Search:** Finds current job postings from public web sources.
- **Structured Data Extraction:** Parses, structures, and ranks job data from each posting.
- **Recruitment Reporting:** Generates a professional, Bootstrap-styled HTML report with interactive tables and concise summaries.

---

## Project Structure
.
├── ai_job_crew.py # Main Python script
├── README.md # This documentation
└── ai-agent-output/ # Output folder for search results, extractions, and reports

---

## Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/AhmedKafrana/ai-job-crew-automation.git
    cd ai-job-crew-automation
    ```

2. **Install Dependencies**
    - Ensure Python 3.9+.
    - Recommended: Use a virtual environment.
    ```bash
    pip install crewai[tools,agentops]==0.114.0
    pip install tavily-python scrapegraph-py
    ```

3. **Set API Keys**

    Set the following environment variables before running:

    - `OPENAI_API_KEY`: Your OpenAI API key
    - `AGENTOPS_API_KEY`: Your AgentOps API key ([get it here](https://app.agentops.ai/get-started))
    - `TAVILY_API_KEY`: [Tavily Search API key](https://docs.tavily.com/)
    - `SCRAPEGRAPH_API_KEY`: [ScrapeGraph API key](https://scrapegraph.com/)

    You can use a `.env` file with [python-dotenv](https://pypi.org/project/python-dotenv/) or export manually:
    ```bash
    export OPENAI_API_KEY=your-key
    export AGENTOPS_API_KEY=your-key
    export TAVILY_API_KEY=your-key
    export SCRAPEGRAPH_API_KEY=your-key
    ```

---

## Usage

1. **Run the Automation Script**
    ```bash
    python ai_job_crew.py
    ```

2. **Review Output**
    - All intermediate and final results are saved in the `ai-agent-output` directory:
        - `step_1_suggested_job_search_queries.json`
        - `step_2_job_search_results.json`
        - `step_3_extracted_jobs.json`
        - `step_4_recruitment_report.html`

3. **Customize Inputs**
    - Edit the `inputs` dictionary in the `if __name__ == "__main__":` section to change job roles, location, language, or number of queries.

---

## How It Works

- **Step 1:** The Search Query Agent generates optimized search queries using LLM.
- **Step 2:** The Search Engine Agent finds job postings using Tavily.
- **Step 3:** The Scraping Agent extracts and structures job data with ScrapeGraph.
- **Step 4:** The Report Author Agent creates an interactive HTML report with all results.

---

## Credits

- [Abu Bakr Soliman, MSc](https://www.linkedin.com/in/bakrianoo/)
- [CrewAI](https://github.com/Vision-CAIR/crewai)
- [Tavily](https://docs.tavily.com/)
- [ScrapeGraph](https://scrapegraph.com/)
- [AgentOps](https://agentops.ai/)

---

## Troubleshooting

- Ensure all required API keys are set.
- Some APIs may have request/usage limits.
- If you encounter package or import errors, upgrade your pip and reinstall dependencies.

---

*For questions or contributions, please open an issue or pull request.*

