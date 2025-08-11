import unittest
from textnode import TextNode, TextType
from text_node_to_html_node import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props)

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("Alt text for image", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://example.com/image.jpg",
            "alt": "Alt text for image"
        })

    def test_link_without_url_raises_error(self):
        node = TextNode("Link text", TextType.LINK, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Link TextNode must have a URL")

    def test_image_without_url_raises_error(self):
        node = TextNode("Alt text", TextType.IMAGE, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Image TextNode must have a URL")

    def test_unsupported_text_type_raises_error(self):
        # Create a TextNode with an invalid text_type (simulate by directly setting)
        node = TextNode("Some text", TextType.TEXT)
        node.text_type = "INVALID_TYPE"  # Manually set invalid type
        
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Unsupported TextType:", str(context.exception))

    def test_empty_text_values(self):
        # Empty TEXT
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        
        # Empty BOLD
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "")

    def test_special_characters_in_text(self):
        node = TextNode("Text with <special> & characters", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "Text with <special> & characters")

    def test_conversion_output_html(self):
        # Test TEXT node rendering
        text_node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Plain text")
        
        # Test BOLD node rendering
        bold_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(bold_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")
        
        # Test LINK node rendering
        link_node = TextNode("Google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(link_node)
        self.assertEqual(html_node.to_html(), '<a href="https://google.com">Google</a>')
        
        # Test IMAGE node rendering
        img_node = TextNode("An image", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(img_node)
        self.assertEqual(html_node.to_html(), '<img src="image.jpg" alt="An image"></img>')

    def test_all_text_types_coverage(self):
        test_cases = [
            (TextType.TEXT, "text", None, None, "text"),
            (TextType.BOLD, "b", "bold text", None, "<b>bold text</b>"),
            (TextType.ITALIC, "i", "italic text", None, "<i>italic text</i>"),
            (TextType.CODE, "code", "code text", None, "<code>code text</code>"),
            (TextType.LINK, "a", "link text", "http://example.com", '<a href="http://example.com">link text</a>'),
            (TextType.IMAGE, "img", "alt text", "image.jpg", '<img src="image.jpg" alt="alt text"></img>'),
        ]
        
        for text_type, expected_tag, text, url, expected_html in test_cases:
            with self.subTest(text_type=text_type):
                node = TextNode(text, text_type, url)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, expected_tag)
                if expected_tag is not None:  # Skip HTML rendering test for raw text
                    self.assertEqual(html_node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
