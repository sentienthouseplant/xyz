import os
import tempfile
import shutil
import duckdb
import pytest
from pathlib import Path


def test_init_db():
    """Test that init_db creates the ads table successfully."""
    # Create a temporary directory for the test
    temp_dir = tempfile.mkdtemp()
    original_dir = os.getcwd()

    try:
        # Change to temp directory
        os.chdir(temp_dir)

        # Create a sample CSV file
        csv_content = "id,name,clicks\n1,Ad1,100\n2,Ad2,200\n"
        with open("ads.csv", "w") as f:
            f.write(csv_content)

        # Import and run init_db
        import sys
        sys.path.insert(0, original_dir)
        from main import init_db

        # Initialize the database
        init_db()

        # Verify the table was created
        conn = duckdb.connect("ads.db")
        result = conn.execute("SELECT COUNT(*) FROM ads").fetchone()
        conn.close()

        # Assert we have the expected number of rows
        assert result[0] == 2, f"Expected 2 rows, got {result[0]}"

    finally:
        # Clean up
        os.chdir(original_dir)
        shutil.rmtree(temp_dir)
