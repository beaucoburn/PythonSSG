import unittest
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_basic_text(self):
        """Test that plain text returns a single TextNode"""
        text = "Hello world"
        result = text_to_textnodes(text)
        expected = [TextNode("Hello world", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_bold_text(self):
        """Test bold text with double asterisks"""
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_italic_text(self):
        """Test italic text with single underscores"""
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_code_text(self):
        """Test code blocks with backticks"""
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_link_text(self):
        """Test markdown links"""
        text = "This is a [link](https://example.com) here"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_image_text(self):
        """Test markdown images"""
        text = "This is an ![image](https://example.com/image.jpg) here"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_combined_markdown(self):
        """Test the example from the assignment"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)
    
    def test_nested_markdown(self):
        """Test that markdown elements don't interfere with each other"""
        text = "**Bold** and _italic_ and `code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)
    
    def test_empty_text(self):
        """Test empty string input"""
        text = ""
        result = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_text_without_markdown(self):
        """Test text that contains no markdown elements"""
        text = "Just some plain text without any formatting"
        result = text_to_textnodes(text)
        expected = [TextNode("Just some plain text without any formatting", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_multiple_links(self):
        """Test text with multiple links"""
        text = "Link1 [here](https://link1.com) and link2 [there](https://link2.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Link1 ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://link1.com"),
            TextNode(" and link2 ", TextType.TEXT),
            TextNode("there", TextType.LINK, "https://link2.com"),
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_images(self):
        """Test text with multiple images"""
        text = "Image1 ![alt1](https://img1.com) and image2 ![alt2](https://img2.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Image1 ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "https://img1.com"),
            TextNode(" and image2 ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "https://img2.com"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
