import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        """Test extracting a simple title"""
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
    
    def test_title_with_whitespace(self):
        """Test extracting title with leading/trailing whitespace"""
        markdown = "  #  Hello World  "
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_title_with_content_after(self):
        """Test extracting title when there's content after it"""
        markdown = "# My Title\n\nThis is some content."
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")
    
    def test_title_with_content_before(self):
        """Test extracting title when there's content before it"""
        markdown = "Some content here.\n\n# My Title"
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")
    
    def test_title_in_middle(self):
        """Test extracting title when it's in the middle of content"""
        markdown = "Content before.\n# Middle Title\nContent after."
        result = extract_title(markdown)
        self.assertEqual(result, "Middle Title")
    
    def test_title_with_special_characters(self):
        """Test extracting title with special characters"""
        markdown = "# My Title: With Special Characters! @#$%"
        result = extract_title(markdown)
        self.assertEqual(result, "My Title: With Special Characters! @#$%")
    
    def test_title_with_multiple_words(self):
        """Test extracting title with multiple words"""
        markdown = "# This Is A Multi Word Title"
        result = extract_title(markdown)
        self.assertEqual(result, "This Is A Multi Word Title")
    
    def test_no_title_found(self):
        """Test that exception is raised when no h1 header is found"""
        markdown = "This is just some content.\nNo title here."
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_empty_markdown(self):
        """Test that exception is raised for empty markdown"""
        markdown = ""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_whitespace_only_markdown(self):
        """Test that exception is raised for whitespace-only markdown"""
        markdown = "   \n  \n  "
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_h2_header_not_extracted(self):
        """Test that h2 headers are not extracted"""
        markdown = "## This is not a title\n# This is the title"
        result = extract_title(markdown)
        self.assertEqual(result, "This is the title")
    
    def test_h3_header_not_extracted(self):
        """Test that h3 headers are not extracted"""
        markdown = "### This is not a title\n# This is the title"
        result = extract_title(markdown)
        self.assertEqual(result, "This is the title")
    
    def test_multiple_h1_headers(self):
        """Test that first h1 header is extracted when multiple exist"""
        markdown = "# First Title\n# Second Title"
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")
    
    def test_title_with_inline_markdown(self):
        """Test extracting title that contains inline markdown"""
        markdown = "# **Bold** Title with _italic_ text"
        result = extract_title(markdown)
        self.assertEqual(result, "**Bold** Title with _italic_ text")
    
    def test_title_with_code(self):
        """Test extracting title that contains code"""
        markdown = "# Title with `code` in it"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with `code` in it")


if __name__ == "__main__":
    unittest.main()
