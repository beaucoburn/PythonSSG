import unittest
from block_to_block_type import block_to_block_type
from block_type import BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        """Test that regular text blocks are identified as paragraphs"""
        block = "This is a regular paragraph with some text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_with_newlines(self):
        """Test that multi-line text blocks are identified as paragraphs"""
        block = "This is a paragraph\nwith multiple lines\nof text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_heading_level_1(self):
        """Test level 1 heading"""
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_level_2(self):
        """Test level 2 heading"""
        block = "## This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_level_6(self):
        """Test level 6 heading (maximum level)"""
        block = "###### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_level_7_invalid(self):
        """Test that 7+ # characters are not recognized as headings"""
        block = "####### This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_heading_no_space_after_hash(self):
        """Test that headings must have a space after the # characters"""
        block = "#This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_heading_with_content_after_space(self):
        """Test heading with content after the space"""
        block = "# This is a heading with content"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_code_block(self):
        """Test code block with 3 backticks"""
        block = "```\nThis is a code block\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_with_content(self):
        """Test code block with content between backticks"""
        block = "```python\ndef hello():\n    print('Hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_minimum_length(self):
        """Test that code block must be at least 6 characters (``` ```)"""
        block = "``` ```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_too_short(self):
        """Test that very short code blocks are not recognized"""
        block = "```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_code_block_no_closing_backticks(self):
        """Test that code blocks must end with backticks"""
        block = "```\nThis is not a code block"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_quote_block_single_line(self):
        """Test single-line quote block"""
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_block_multiple_lines(self):
        """Test multi-line quote block"""
        block = "> This is a quote\n> with multiple lines\n> of text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_block_mixed_content(self):
        """Test that quote blocks must have > on every line"""
        block = "> This is a quote\nThis is not a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_unordered_list_single_item(self):
        """Test single-item unordered list"""
        block = "- This is a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multiple_items(self):
        """Test multi-item unordered list"""
        block = "- First item\n- Second item\n- Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_no_space_after_dash(self):
        """Test that unordered list items must have a space after the dash"""
        block = "-This is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_unordered_list_mixed_content(self):
        """Test that unordered lists must have - on every line"""
        block = "- First item\nThis is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_single_item(self):
        """Test single-item ordered list"""
        block = "1. This is a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_multiple_items(self):
        """Test multi-item ordered list"""
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_no_space_after_period(self):
        """Test that ordered list items must have a space after the period"""
        block = "1.This is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_must_start_with_one(self):
        """Test that ordered lists must start with 1."""
        block = "2. This is not a valid ordered list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_must_increment(self):
        """Test that ordered lists must increment by 1"""
        block = "1. First item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_mixed_content(self):
        """Test that ordered lists must have proper numbering on every line"""
        block = "1. First item\nThis is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_priority_order(self):
        """Test that code blocks take priority over other types"""
        block = "```\n# This looks like a heading\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_empty_block(self):
        """Test empty block (should be paragraph)"""
        block = ""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_block_with_only_whitespace(self):
        """Test block with only whitespace (should be paragraph)"""
        block = "   \n  "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_heading_with_inline_markdown(self):
        """Test heading with inline markdown"""
        block = "# This is a **bold** heading with _italic_ text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_quote_with_inline_markdown(self):
        """Test quote with inline markdown"""
        block = "> This is a quote with **bold** and `code`"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)


if __name__ == "__main__":
    unittest.main()
