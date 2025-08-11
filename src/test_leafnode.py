import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("a", "Google", {"href": "https://www.google.com", "target": "_blank"})
        expected = '<a href="https://www.google.com" target="_blank">Google</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")

    def test_leaf_to_html_different_tags(self):
        # Test h1
        node = LeafNode("h1", "Main Title")
        self.assertEqual(node.to_html(), "<h1>Main Title</h1>")
        
        # Test span
        node = LeafNode("span", "Some text")
        self.assertEqual(node.to_html(), "<span>Some text</span>")
        
        # Test b (bold)
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_img_tag(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image"></img>')

    def test_leaf_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "All leaf nodes must have a value")

    def test_leaf_empty_string_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_children_always_none(self):
        node = LeafNode("p", "Test")
        self.assertIsNone(node.children)

    def test_leaf_constructor_inheritance(self):
        node = LeafNode("div", "Content", {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Content")
        self.assertEqual(node.props, {"class": "container"})
        self.assertIsNone(node.children)


if __name__ == "__main__":
    unittest.main()
