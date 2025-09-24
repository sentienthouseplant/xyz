import pytest
import os
import tempfile
import duckdb
from unittest.mock import patch, MagicMock
from sqlagent.main import duckdb_query, write_markdown_report, create_model, init_db


def test_write_markdown_report():
    """Test the markdown report writing functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to the temporary directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Test data
            test_report = "# Test Report\n\nThis is a test report with some content."
            test_title = "test_analysis"

            # Call the function
            write_markdown_report(test_report, test_title)

            # Verify the file was created
            report_path = os.path.join("reports", f"{test_title}.md")
            assert os.path.exists(report_path)

            # Verify the content
            with open(report_path, "r") as f:
                content = f.read()

            assert content == test_report

        finally:
            # Restore original directory
            os.chdir(original_cwd)


def test_create_model():
    """Test model creation with environment variables."""
    with patch.dict(os.environ, {'OPENROUTER_KEY': 'test_api_key'}):
        with patch('sqlagent.main.OpenAIServerModel') as mock_model_class:
            mock_model_instance = MagicMock()
            mock_model_class.return_value = mock_model_instance

            result = create_model()

            # Verify the model was created with correct parameters
            mock_model_class.assert_called_once_with(
                model_id="google/gemini-2.5-flash-preview-05-20",
                api_key="test_api_key",
                api_base="https://openrouter.ai/api/v1"
            )

            assert result == mock_model_instance


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    # Create a test database with sample data
    conn = duckdb.connect(db_path)
    conn.execute("""
        CREATE TABLE ads (
            id INTEGER,
            name TEXT,
            category TEXT,
            price DECIMAL
        );
    """)
    conn.execute("""
        INSERT INTO ads VALUES
        (1, 'Product A', 'Electronics', 99.99),
        (2, 'Product B', 'Clothing', 29.99),
        (3, 'Product C', 'Electronics', 149.99);
    """)
    conn.close()

    yield db_path

    # Cleanup
    os.unlink(db_path)


def test_duckdb_query_json_format(temp_db):
    """Test duckdb_query function with JSON output format."""
    with patch('sqlagent.main.duckdb.connect') as mock_connect:
        # Mock the database connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Mock query result
        import pandas as pd
        sample_data = pd.DataFrame([
            {'id': 1, 'name': 'Product A', 'category': 'Electronics', 'price': 99.99}
        ])
        mock_conn.query.return_value.df.return_value = sample_data

        # Test the query
        result = duckdb_query("SELECT * FROM ads WHERE id = 1", max_rows=5, output_format="json")

        # Verify the connection and query were called
        mock_connect.assert_called_once_with("ads.db")
        mock_conn.query.assert_called_once_with("SELECT * FROM ads WHERE id = 1")
        mock_conn.close.assert_called_once()

        # Verify the result format
        assert isinstance(result, str)
        import json
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]['name'] == 'Product A'