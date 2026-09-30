# 🔎 Multi-Agent Research System

An AI research assistant built from four cooperating agents. Give it a topic and it searches the web, reads the best source in depth, writes a structured report, and then critiques that report. It runs from the terminal or from a Streamlit web UI.

<!-- Add a screenshot or GIF here: ![Demo](assets/demo.png) -->

## How it works

```
Topic ──► Search Agent ──► Reader Agent ──► Writer Chain ──► Critic Chain ──► Report + Feedback
```

| Step | Component | Role |
|------|-----------|------|
| 1 | **Search Agent** | Finds recent, reliable information about the topic |
| 2 | **Reader Agent** | Picks the most relevant URL and scrapes it for deeper content |
| 3 | **Writer Chain** | Combines search results and scraped content into a report |
| 4 | **Critic Chain** | Reviews the report and returns feedback |

## Features

- Four-stage pipeline: search, read, write, critique
- Streamlit UI with live step-by-step progress
- Tabbed results: report, critic feedback, raw search results, scraped content
- One-click report download as Markdown
- Session history of past runs
- Terminal mode for quick runs without the UI

## Project structure

```
.
├── agents.py          # Agent and chain definitions (search, reader, writer, critic)
├── tools.py           # Tools used by the agents (web search, scraping)
├── pipeline.py        # Orchestrates the four steps
├── app.py             # Streamlit web interface
├── requirements.txt
├── .env               # API keys (not committed)
└── .gitignore
```

## Getting started

### Prerequisites

- Python 3.10+
- API keys for your LLM provider and search tool (see `.env` below)

### Installation

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# Replace with the keys your agents.py / tools.py actually use
OPENAI_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
```



## Usage

### Web UI

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, enter a topic, and click **Run research**.

### Terminal

```bash
python pipeline.py
```

You will be prompted for a topic, and each step's output is printed as it completes.

### Use it in your own code

```python
from pipeline import run_research_pipeline

state = run_research_pipeline("AI applications in precision agriculture")

print(state["report"])
print(state["feedback"])
```

The returned `state` dictionary contains `search_results`, `scraped_content`, `report`, and `feedback`.

## Deployment

The app can be deployed for free on [Streamlit Community Cloud](https://share.streamlit.io):

1. Push the repo to GitHub (without `.env`).
2. Create a new app and set the main file to `app.py`.
3. Add your API keys under **Advanced settings → Secrets**.

## Limitations

- The Reader Agent scrapes one page per run, so report depth depends on that source.
- Output quality depends on the underlying LLM and search results.
- Runs take a while because the four steps execute sequentially.
- Reports should be fact-checked before being relied on.

## Roadmap

- [ ] Scrape multiple sources per run
- [ ] Add citations and source links to the report
- [ ] Let the Writer revise its report using the Critic's feedback
- [ ] Export reports to PDF/DOCX
- [ ] Stream agent output token by token in the UI

## Tech stack

- Python
- LangChain (agents and chains)
- Streamlit (UI)

## Contributing

Issues and pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## License

Distributed under the MIT License. See `LICENSE` for details.

## Author

**Dipesh** — CSIT student, Tribhuvan University
GitHub: [@your-username](https://github.com/dipesh-bhattarai)