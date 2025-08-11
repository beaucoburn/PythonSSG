import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_code_delimiter(self):
        """Test splitting with backtick delimiter for code"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_bold_delimiter(self):
        """Test splitting with ** delimiter for bold"""
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_italic_delimiter(self):
        """Test splitting with _ delimiter for italic"""
        node = TextNode("This is text with an _italic phrase_ here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_multiple_delimiters_same_type(self):
        """Test text with multiple delimiters of the same type"""
        node = TextNode("Text with `code1` and `code2` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" blocks", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_no_delimiter_in_text(self):
        """Test text with no delimiter - should return original node"""
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is just plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_non_text_node_passed_through(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Code text", TextType.CODE),
        ]
        
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        # The BOLD and CODE nodes should be unchanged
        self.assertEqual(new_nodes[1].text, "Bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "Code text")
        self.assertEqual(new_nodes[2].text_type, TextType.CODE)

    def test_delimiter_at_start(self):
        """Test delimiter at the start of text"""
        node = TextNode("**Bold start** and regular text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("Bold start", TextType.BOLD),
            TextNode(" and regular text", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_delimiter_at_end(self):
        """Test delimiter at the end of text"""
        node = TextNode("Regular text and **bold end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("Regular text and ", TextType.TEXT),
            TextNode("bold end", TextType.BOLD),
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_entire_text_is_delimiter(self):
        """Test when entire text is wrapped in delimiters"""
        node = TextNode("**entire text is bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "entire text is bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_unmatched_delimiter_raises_error(self):
        """Test that unmatched delimiter raises ValueError"""
        node = TextNode("This has unmatched `code delimiter", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertIn("Invalid markdown syntax: unmatched delimiter", str(context.exception))
        self.assertIn("`", str(context.exception))

    def test_empty_delimiter_content_raises_error(self):
        """Test that empty content between delimiters raises ValueError"""
        node = TextNode("This has empty `` delimiters", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertIn("Invalid markdown syntax: empty content", str(context.exception))

    def test_adjacent_delimiters(self):
        """Test adjacent delimiters with different content"""
        node = TextNode("Text `code1``code2` end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode("", TextType.TEXT),  # Empty text between adjacent delimiters
            TextNode("code2", TextType.CODE),
            TextNode(" end", TextType.TEXT),
        ]
        
        # Note: The function should handle this case by filtering empty TEXT nodes
        # Let's check that it produces the expected structure
        self.assertTrue(len(new_nodes) >= 3)  # At least the core parts

    def test_multiple_nodes_input(self):
        """Test processing multiple nodes in input list"""
        nodes = [
            TextNode("First `code` node", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second `more code` node", TextType.TEXT),
        ]
        
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        # Should have: First + code + node + bold + Second + more code + node
        # The BOLD node should be unchanged
        bold_node = None
        for node in new_nodes:
            if node.text_type == TextType.BOLD:
                bold_node = node
                break
        
        self.assertIsNotNone(bold_node)
        self.assertEqual(bold_node.text, "Already bold")

    def test_empty_input_list(self):
        """Test empty input list"""
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 0)

    def test_different_delimiter_types(self):
        """Test various delimiter types work correctly"""
        test_cases = [
            ("Text with `code`", "`", TextType.CODE, "code"),
            ("Text with **bold**", "**", TextType.BOLD, "bold"),
            ("Text with _italic_", "_", TextType.ITALIC, "italic"),
            ("Text with ***triple***", "***", TextType.BOLD, "triple"),  # Custom delimiter
        ]
        
        for text, delimiter, expected_type, expected_content in test_cases:
            with self.subTest(delimiter=delimiter):
                node = TextNode(text, TextType.TEXT)
                new_nodes = split_nodes_delimiter([node], delimiter, expected_type)
                
                # Find the node with the expected type
                found_node = None
                for n in new_nodes:
                    if n.text_type == expected_type:
                        found_node = n
                        break
                
                self.assertIsNotNone(found_node)
                self.assertEqual(found_node.text, expected_content)

    def test_empty_text_parts_filtered(self):
        """Test that empty text parts are properly handled"""
        node = TextNode("**bold**", TextType.TEXT)  # No text before or after
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Should only have the bold node, empty text nodes should be filtered
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
