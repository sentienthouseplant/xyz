import pytest
import os
import tempfile
import duckdb
from unittest.mock import patch, MagicMock
from main import duckdb_query, write_markdown_report, create_model


def test_duckdb_query():
    """Test the duckdb_query function with a simple query."""
    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        temp_db_path = temp_db.name

    try:
        # Set up test data
        conn = duckdb.connect(temp_db_path)
        conn.execute("CREATE TABLE test_table (id INTEGER, name VARCHAR)")
        conn.execute("INSERT INTO test_table VALUES (1, 'Alice'), (2, 'Bob')")
        conn.close()

        # Patch the database path in the function
        with patch('main.duckdb.connect') as mock_connect:
            mock_conn = MagicMock()
            mock_connect.return_value = mock_conn

            # Mock the query result
            mock_df = MagicMock()
            mock_df.head.return_value.to_json.return_value = '[{"id": 1, "name": "Alice"}]'
            mock_conn.query.return_value.df.return_value = mock_df

            # Test the function
            result = duckdb_query("SELECT * FROM test_table", max_rows=1)

            # Assertions
            assert isinstance(result, str)
            mock_connect.assert_called_once_with("ads.db")
            mock_conn.query.assert_called_once_with("SELECT * FROM test_table")
            mock_df.head.assert_called_once_with(1)

    finally:
        # Clean up
        if os.path.exists(temp_db_path):
            os.unlink(temp_db_path)


def test_write_markdown_report():
    """Test the write_markdown_report function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Test data
            report_content = "# Test Report\n\nThis is a test report."
            report_title = "test_report"

            # Call the function
            write_markdown_report(report_content, report_title)

            # Verify the file was created
            expected_path = os.path.join("reports", f"{report_title}.md")
            assert os.path.exists(expected_path)

            # Verify the content
            with open(expected_path, 'r') as f:
                content = f.read()
            assert content == report_content

        finally:
            os.chdir(original_cwd)


@patch('main.OpenAIServerModel')
def test_create_model(mock_openai_model):
    """Test the create_model function."""
    # Mock environment variable
    with patch.dict('os.environ', {'OPENROUTER_KEY': 'test-key'}):
        # Call the function
        create_model()

        # Verify OpenAIServerModel was called with correct parameters
        mock_openai_model.assert_called_once_with(
            model_id="google/gemini-2.5-flash-preview-05-20",
            api_key="test-key",
            api_base="https://openrouter.ai/api/v1"
        )