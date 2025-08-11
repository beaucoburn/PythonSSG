import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_multiple_attributes(self):
        node = HTMLNode(
            tag="a",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_with_single_attribute(self):
        node = HTMLNode(
            tag="img",
            props={"src": "image.jpg"}
        )
        expected = ' src="image.jpg"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_with_no_props(self):
        node = HTMLNode(tag="p", value="Hello world")
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_with_none_props(self):
        node = HTMLNode(tag="div", props=None)
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_raises_not_implemented_error(self):
        node = HTMLNode(tag="p", value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_method(self):
        node = HTMLNode(
            tag="a",
            value="Click me",
            children=[HTMLNode(tag="span", value="inner")],
            props={"href": "https://example.com"}
        )
        repr_str = repr(node)
        
        # Check that all components are present in the repr
        self.assertIn("tag='a'", repr_str)
        self.assertIn("value='Click me'", repr_str)
        self.assertIn("children=", repr_str)
        self.assertIn("props=", repr_str)
        self.assertIn("https://example.com", repr_str)

    def test_initialization_with_all_none_values(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


if __name__ == "__main__":
    unittest.main()
