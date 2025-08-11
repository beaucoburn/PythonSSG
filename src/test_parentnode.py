import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_complex_nesting_example(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_multiple_children(self):
        children = [
            LeafNode("h1", "Heading"),
            LeafNode("p", "Paragraph 1"),
            LeafNode("p", "Paragraph 2"),
        ]
        parent_node = ParentNode("div", children)
        expected = "<div><h1>Heading</h1><p>Paragraph 1</p><p>Paragraph 2</p></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_deeply_nested_structure(self):
        # Deep nesting: div > section > article > p > b
        deepest = LeafNode("b", "Deep content")
        level3 = ParentNode("p", [deepest])
        level2 = ParentNode("article", [level3])
        level1 = ParentNode("section", [level2])
        root = ParentNode("div", [level1])
        
        expected = "<div><section><article><p><b>Deep content</b></p></article></section></div>"
        self.assertEqual(root.to_html(), expected)

    def test_mixed_parent_and_leaf_children(self):
        leaf1 = LeafNode("span", "Start")
        nested_parent = ParentNode("strong", [LeafNode("em", "emphasized")])
        leaf2 = LeafNode("span", "End")
        
        parent = ParentNode("p", [leaf1, nested_parent, leaf2])
        expected = "<p><span>Start</span><strong><em>emphasized</em></strong><span>End</span></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_with_props(self):
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        expected = '<div class="container" id="main"><span>content</span></div>'
        self.assertEqual(parent.to_html(), expected)

    def test_nested_parents_with_props(self):
        grandchild = LeafNode("a", "Link", {"href": "#"})
        child = ParentNode("li", [grandchild], {"class": "item"})
        parent = ParentNode("ul", [child], {"class": "list"})
        
        expected = '<ul class="list"><li class="item"><a href="#">Link</a></li></ul>'
        self.assertEqual(parent.to_html(), expected)

    def test_no_tag_raises_error(self):
        child = LeafNode("span", "child")
        parent = ParentNode(None, [child])  # This would actually fail in constructor
        # But let's test by manually setting tag to None
        parent.tag = None
        
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_no_children_raises_error(self):
        parent = ParentNode("div", [])  # Empty list
        parent.children = None  # Manually set to None to test
        
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children")

    def test_empty_children_list(self):
        parent = ParentNode("div", [])
        # Empty list should render as empty tag
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_single_raw_text_child(self):
        child = LeafNode(None, "Just raw text")
        parent = ParentNode("p", [child])
        self.assertEqual(parent.to_html(), "<p>Just raw text</p>")

    def test_multiple_raw_text_children(self):
        children = [
            LeafNode(None, "First "),
            LeafNode(None, "second "),
            LeafNode(None, "third"),
        ]
        parent = ParentNode("span", children)
        self.assertEqual(parent.to_html(), "<span>First second third</span>")

    def test_constructor_inheritance(self):
        child = LeafNode("span", "test")
        parent = ParentNode("div", [child], {"class": "test"})
        
        self.assertEqual(parent.tag, "div")
        self.assertIsNone(parent.value)  # ParentNode should never have a value
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, {"class": "test"})

    def test_large_tree_structure(self):
        # Build a complex document structure
        header = ParentNode("header", [
            ParentNode("h1", [LeafNode(None, "Main Title")]),
            ParentNode("nav", [
                ParentNode("ul", [
                    ParentNode("li", [LeafNode("a", "Home", {"href": "/"})]),
                    ParentNode("li", [LeafNode("a", "About", {"href": "/about"})]),
                ])
            ])
        ])
        
        content = ParentNode("main", [
            ParentNode("p", [
                LeafNode(None, "This is a "),
                LeafNode("strong", "complex"),
                LeafNode(None, " example with "),
                LeafNode("em", "nested"),
                LeafNode(None, " elements."),
            ])
        ])
        
        page = ParentNode("body", [header, content])
        
        expected = ('<body>'
                   '<header>'
                   '<h1>Main Title</h1>'
                   '<nav>'
                   '<ul>'
                   '<li><a href="/">Home</a></li>'
                   '<li><a href="/about">About</a></li>'
                   '</ul>'
                   '</nav>'
                   '</header>'
                   '<main>'
                   '<p>This is a <strong>complex</strong> example with <em>nested</em> elements.</p>'
                   '</main>'
                   '</body>')
        
        self.assertEqual(page.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
