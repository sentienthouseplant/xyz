# sqlagent: AI-Powered Data Analysis

An intelligent data analysis tool that uses AI agents to explore advertising data and generate insightful reports. The system leverages DuckDB for fast data processing and OpenRouter's API for AI capabilities.

For a fun overview, look at these [slides](docs/Writing%20A%20SQL%20Agent.pdf)!

## Features

- 🦆 **Fast Data Processing**: Uses DuckDB for efficient SQL queries on advertising data
- 🤖 **AI-Powered Analysis**: Employs AI agents to discover insights automatically
- 📊 **Automated Reporting**: Generates markdown reports with findings

## Prerequisites

- [uv](https://docs.astral.sh/uv/) - Python package manager
- An [OpenRouter](https://openrouter.ai/) API key
- Advertising data in CSV format (`ads.csv`)

## Setup

### 1. Install uv (if not already installed)

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Environment Variables

Create a `.env` file in the project directory with your OpenRouter API key:

```env
OPENROUTER_KEY=your_openrouter_api_key_here
```

To get an OpenRouter API key:
1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Generate an API key from your dashboard

### 3. Prepare Your Data

Ensure you have an `ads.csv` file in the project directory containing your advertising data. The script will automatically create a DuckDB database from this CSV file.

## Usage

Run the analysis with a single command:

```bash
uv run main.py
```

This will:
1. Initialize the DuckDB database with your advertising data
2. Create an AI agent with data analysis capabilities
3. Explore the data and identify interesting patterns
4. Generate a detailed markdown report in the `reports/` directory

## Project Structure

```
smol_duck/
├── main.py          # Main application script
├── ads.csv          # Your advertising data (you provide this)
├── ads.db           # DuckDB database (created automatically)
├── .env             # Environment variables
├── README.md        # This file
└── reports/         # Generated analysis reports (created automatically)
```

## Configuration

The project is configured to use:
- **Model**: `google/gemini-2.5-flash-preview-05-20` via OpenRouter
- **Max Analysis Steps**: 50
- **Database**: Local DuckDB instance
- **Output**: Markdown reports in `reports/` directory

## Available Tools

The AI agent has access to:

- **`duckdb_query`**: Execute SQL queries on the advertising database
- **`write_markdown_report`**: Generate formatted analysis reports

## Dependencies

The project automatically manages dependencies through uv. Key packages include:

- `smolagents`: AI agent framework
- `duckdb`: Fast analytical database
- `pandas`: Data manipulation and analysis
- `python-dotenv`: Environment variable management

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure your `.env` file contains a valid `OPENROUTER_KEY`
2. **No ads.csv**: Make sure your advertising data file is named `ads.csv` and in the project root
3. **uv not found**: Install uv following the instructions above

### Getting Help

If you encounter issues:
1. Check that all environment variables are set correctly
2. Verify your `ads.csv` file is properly formatted
3. Ensure your OpenRouter API key has sufficient credits

You can also DM me.

## License

This project is for educational and research purposes. 
