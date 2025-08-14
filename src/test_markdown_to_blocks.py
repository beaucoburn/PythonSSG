import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_blocks(self):
        """Test basic block separation with double newlines"""
        md = "Block 1\n\nBlock 2\n\nBlock 3"
        result = markdown_to_blocks(md)
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(result, expected)
    
    def test_blocks_with_whitespace(self):
        """Test that leading and trailing whitespace is stripped"""
        md = "  Block 1  \n\n  Block 2  \n\n  Block 3  "
        result = markdown_to_blocks(md)
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(result, expected)
    
    def test_empty_blocks_filtered(self):
        """Test that empty blocks due to excessive newlines are removed"""
        md = "Block 1\n\n\n\nBlock 2\n\n\n\n\nBlock 3"
        result = markdown_to_blocks(md)
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(result, expected)
    
    def test_single_block(self):
        """Test markdown with no block separators"""
        md = "This is just one block"
        result = markdown_to_blocks(md)
        expected = ["This is just one block"]
        self.assertEqual(result, expected)
    
    def test_empty_string(self):
        """Test empty string input"""
        md = ""
        result = markdown_to_blocks(md)
        expected = []
        self.assertEqual(result, expected)
    
    def test_only_whitespace(self):
        """Test string with only whitespace and newlines"""
        md = "   \n\n   \n\n   "
        result = markdown_to_blocks(md)
        expected = []
        self.assertEqual(result, expected)
    
    def test_multiline_blocks(self):
        """Test blocks that contain multiple lines"""
        md = "Line 1\nLine 2\nLine 3\n\nAnother block\nWith multiple lines"
        result = markdown_to_blocks(md)
        expected = [
            "Line 1\nLine 2\nLine 3",
            "Another block\nWith multiple lines"
        ]
        self.assertEqual(result, expected)
    
    def test_assignment_example(self):
        """Test the example from the assignment"""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        result = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(result, expected)
    
    def test_heading_paragraph_list_example(self):
        """Test the heading, paragraph, and list example from the assignment description"""
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        
        result = markdown_to_blocks(md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        self.assertEqual(result, expected)
    
    def test_blocks_with_markdown(self):
        """Test blocks that contain inline markdown"""
        md = "**Bold text**\n\n_Italic text_\n\n`Code text`"
        result = markdown_to_blocks(md)
        expected = ["**Bold text**", "_Italic text_", "`Code text`"]
        self.assertEqual(result, expected)
    
    def test_trailing_newlines(self):
        """Test markdown with trailing newlines"""
        md = "Block 1\n\nBlock 2\n\n"
        result = markdown_to_blocks(md)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)
    
    def test_leading_newlines(self):
        """Test markdown with leading newlines"""
        md = "\n\nBlock 1\n\nBlock 2"
        result = markdown_to_blocks(md)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
