import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        """Test the example from the assignment for paragraphs"""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        """Test the example from the assignment for code blocks"""
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_headings(self):
        """Test heading blocks"""
        md = """# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        self.assertEqual(html, expected)
    
    def test_headings_with_inline_markdown(self):
        """Test headings with inline markdown"""
        md = "# **Bold** heading with _italic_ text"
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1><b>Bold</b> heading with <i>italic</i> text</h1></div>"
        self.assertEqual(html, expected)
    
    def test_quotes(self):
        """Test quote blocks"""
        md = """> This is a quote

> This is another quote
> with multiple lines
> of text"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote</blockquote><blockquote>This is another quote\nwith multiple lines\nof text</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_quotes_with_inline_markdown(self):
        """Test quotes with inline markdown"""
        md = "> This is a **bold** quote with `code` and _italic_ text"
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a <b>bold</b> quote with <code>code</code> and <i>italic</i> text</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_lists(self):
        """Test unordered list blocks"""
        md = """- First item
- Second item
- Third item

- Another list
- With more items"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul><ul><li>Another list</li><li>With more items</li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_lists_with_inline_markdown(self):
        """Test unordered lists with inline markdown"""
        md = "- **Bold** item\n- _Italic_ item\n- `Code` item"
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li><b>Bold</b> item</li><li><i>Italic</i> item</li><li><code>Code</code> item</li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_lists(self):
        """Test ordered list blocks"""
        md = """1. First item
2. Second item
3. Third item

1. Another list
2. With more items"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol><ol><li>Another list</li><li>With more items</li></ol></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_lists_with_inline_markdown(self):
        """Test ordered lists with inline markdown"""
        md = "1. **Bold** item\n2. _Italic_ item\n3. `Code` item"
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li><b>Bold</b> item</li><li><i>Italic</i> item</li><li><code>Code</code> item</li></ol></div>"
        self.assertEqual(html, expected)
    
    def test_mixed_blocks(self):
        """Test a mix of different block types"""
        md = """# Main Heading

This is a paragraph with **bold** text.

> This is a quote block
> with multiple lines

- List item 1
- List item 2

1. Ordered item 1
2. Ordered item 2

```
Code block here
```

Final paragraph."""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Check that all block types are present
        self.assertIn("<h1>Main Heading</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> text.</p>", html)
        self.assertIn("<blockquote>This is a quote block\nwith multiple lines</blockquote>", html)
        self.assertIn("<ul><li>List item 1</li><li>List item 2</li></ul>", html)
        self.assertIn("<ol><li>Ordered item 1</li><li>Ordered item 2</li></ol>", html)
        self.assertIn("<pre><code>Code block here\n</code></pre>", html)
        self.assertIn("<p>Final paragraph.</p>", html)
    
    def test_empty_markdown(self):
        """Test empty markdown input"""
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    def test_whitespace_only_markdown(self):
        """Test markdown with only whitespace"""
        md = "   \n\n   \n\n   "
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    def test_single_paragraph(self):
        """Test single paragraph without block separators"""
        md = "This is just one paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is just one paragraph.</p></div>")
    
    def test_links_and_images_in_blocks(self):
        """Test blocks containing links and images"""
        md = """This paragraph has a [link](https://example.com) and an ![image](https://example.com/image.jpg).

# Heading with [link](https://example.com)

> Quote with ![image](https://example.com/image.jpg)"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Check that links and images are properly converted
        self.assertIn('<a href="https://example.com">link</a>', html)
        self.assertIn('<img src="https://example.com/image.jpg" alt="image">', html)
    
    def test_code_block_preserves_inline_markdown(self):
        """Test that code blocks don't parse inline markdown"""
        md = "```\nThis text has **bold** and _italic_ and `code`\n```"
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # The inline markdown should remain as literal text
        self.assertIn("This text has **bold** and _italic_ and `code`", html)
        self.assertNotIn("<b>bold</b>", html)
        self.assertNotIn("<i>italic</i>", html)
        self.assertNotIn("<code>code</code>", html)


if __name__ == "__main__":
    unittest.main()
