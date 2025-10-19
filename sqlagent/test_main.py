import os
import pytest
import tempfile
import shutil
from main import write_markdown_report


class TestWriteMarkdownReport:
    """Test suite for the write_markdown_report function."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test reports
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        """Clean up test environment after each test."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_write_markdown_report_creates_file(self):
        """Test that write_markdown_report creates a markdown file with correct content."""
        # Arrange
        report_content = "# Test Report\n\nThis is a test report."
        report_title = "test_report"
        expected_path = os.path.join("reports", f"{report_title}.md")

        # Act
        write_markdown_report(report_content, report_title)

        # Assert
        assert os.path.exists(expected_path), "Report file was not created"

        with open(expected_path, "r") as f:
            content = f.read()

        assert content == report_content, "Report content does not match expected content"

    def test_write_markdown_report_creates_reports_directory(self):
        """Test that write_markdown_report creates the reports directory if it doesn't exist."""
        # Arrange
        report_content = "# Another Test"
        report_title = "another_test"
        reports_dir = "reports"

        # Ensure reports directory doesn't exist
        if os.path.exists(reports_dir):
            shutil.rmtree(reports_dir)

        # Act
        write_markdown_report(report_content, report_title)

        # Assert
        assert os.path.exists(reports_dir), "Reports directory was not created"
        assert os.path.isdir(reports_dir), "Reports path is not a directory"
