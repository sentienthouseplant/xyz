import os
import dotenv
import duckdb
import pandas as pd
from typing import Literal
from smolagents import OpenAIServerModel, CodeAgent, tool

# Load environment variables
dotenv.load_dotenv()

# Configuration
MODEL = "google/gemini-2.5-flash-preview-05-20"
BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY")
DATASET_PATH = "ads.csv"


def init_db():
    """Initialize the DuckDB database with ads data."""
    conn = duckdb.connect("ads.db")
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS ads AS
        SELECT * FROM '{DATASET_PATH}';
    """)
    conn.close()


@tool
def duckdb_query(query: str, max_rows: int = 10, output_format: Literal["json", "pandas", "dict"] = "json") -> str | list[dict] | pd.DataFrame:
    """
    Query the duckdb database using the provided SQL query.

    Args:
        query: The SQL query to execute.
        max_rows: The maximum number of rows to return, max 20.
        output_format: The format to return the results in. Defaults to a json string.
    Returns:
        A JSON string of the results or a list of dictionaries of the result rows.
    """
    conn = duckdb.connect("ads.db")
    df = conn.query(query).df()
    conn.close()

    df_chunk = df.head(max_rows)

    match output_format:
        case "json":
            output = df_chunk.to_json(orient="records")
        case "dict":
            output = df_chunk.to_dict(orient="records")
        case "pandas":
            output = df_chunk
    
    return output


@tool
def write_markdown_report(report: str, title: str) -> None:
    """
    Write a markdown report.

    Args:
        report: The report to write. Use triple quotes to pass in the report.
        title: The title of the report.
    Returns:
        None
    """
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{title}.md", "w") as f:
        f.write(report)


def create_model():
    """Create and return the OpenAI server model."""
    return OpenAIServerModel(
        model_id=MODEL,
        api_key=OPENROUTER_API_KEY,
        api_base=BASE_URL
    )


def create_agent(model):
    """Create and return the CodeAgent with tools."""
    return CodeAgent(
        model=model,
        tools=[duckdb_query, write_markdown_report],
        max_steps=50,
        additional_authorized_imports=["pandas", "duckdb", "json", "re"]
    )


def main():
    """Main execution function."""
    # Initialize database
    init_db()
    
    # Create model and agent
    model = create_model()
    agent = create_agent(model)
    
    # Run the analysis
    agent.run("""
You are a expert data analyst. You have been given a database of advertising data to explore.

Explore this data deeply and try to find interesting insights which would be useful for a business.

When you are done, write a markdown report of your findings.
""")


if __name__ == "__main__":
    # check for ads.csv in the current directory
    if not os.path.exists(DATASET_PATH):
        print(f"{DATASET_PATH} not found in the current directory. Download from https://data.mendeley.com/datasets/wrvjmdtjd9/1")
        exit(1)

    main()
