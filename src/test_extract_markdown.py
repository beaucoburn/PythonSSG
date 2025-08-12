import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        """Test extracting a single markdown image"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        """Test extracting multiple markdown images"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_images_with_spaces_in_alt_text(self):
        """Test extracting images with spaces in alt text"""
        text = "Here's an ![alt text with spaces](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("alt text with spaces", "https://example.com/image.jpg")], matches)

    def test_extract_images_with_special_chars_in_alt_text(self):
        """Test extracting images with special characters in alt text"""
        text = "Here's an ![alt-text_with.special@chars](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("alt-text_with.special@chars", "https://example.com/image.jpg")], matches)

    def test_extract_images_with_complex_urls(self):
        """Test extracting images with complex URLs"""
        text = "Here's an ![image](https://example.com/path/to/image.jpg?param=value&other=123)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/path/to/image.jpg?param=value&other=123")], matches)

    def test_no_images_in_text(self):
        """Test text with no images returns empty list"""
        text = "This is just plain text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_image_at_start_of_text(self):
        """Test image at the beginning of text"""
        text = "![start image](https://example.com/start.jpg) and some text"
        matches = extract_markdown_images(text)
        self.assertListEqual([("start image", "https://example.com/start.jpg")], matches)

    def test_image_at_end_of_text(self):
        """Test image at the end of text"""
        text = "Some text and ![end image](https://example.com/end.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("end image", "https://example.com/end.jpg")], matches)

    def test_extract_markdown_links(self):
        """Test extracting a single markdown link"""
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        """Test extracting multiple markdown links"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_links_with_spaces_in_anchor_text(self):
        """Test extracting links with spaces in anchor text"""
        text = "Here's a [link with spaces](https://example.com/page)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link with spaces", "https://example.com/page")], matches)

    def test_extract_links_with_special_chars_in_anchor_text(self):
        """Test extracting links with special characters in anchor text"""
        text = "Here's a [link-with.special@chars](https://example.com/page)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link-with.special@chars", "https://example.com/page")], matches)

    def test_extract_links_with_complex_urls(self):
        """Test extracting links with complex URLs"""
        text = "Here's a [link](https://example.com/path/to/page?param=value&other=123#section)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com/path/to/page?param=value&other=123#section")], matches)

    def test_no_links_in_text(self):
        """Test text with no links returns empty list"""
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_link_at_start_of_text(self):
        """Test link at the beginning of text"""
        text = "[start link](https://example.com/start) and some text"
        matches = extract_markdown_links(text)
        self.assertListEqual([("start link", "https://example.com/start")], matches)

    def test_link_at_end_of_text(self):
        """Test link at the end of text"""
        text = "Some text and [end link](https://example.com/end)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("end link", "https://example.com/end")], matches)

    def test_mixed_images_and_links(self):
        """Test text with both images and links"""
        text = "Here's an ![image](https://example.com/img.jpg) and a [link](https://example.com/page)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        self.assertListEqual([("image", "https://example.com/img.jpg")], image_matches)
        self.assertListEqual([("link", "https://example.com/page")], link_matches)

    def test_links_not_confused_with_images(self):
        """Test that links are not confused with images"""
        text = "Here's a ![image](https://example.com/img.jpg) and a [link](https://example.com/page)"
        link_matches = extract_markdown_links(text)
        
        # Should only find the link, not the image
        self.assertListEqual([("link", "https://example.com/page")], link_matches)

    def test_empty_alt_text_and_anchor_text(self):
        """Test handling of empty alt text and anchor text"""
        image_text = "Here's an ![]() image"
        link_text = "Here's a []() link"
        
        image_matches = extract_markdown_images(image_text)
        link_matches = extract_markdown_links(link_text)
        
        self.assertListEqual([("", "")], image_matches)
        self.assertListEqual([("", "")], link_matches)

    def test_nested_brackets_in_alt_text(self):
        """Test handling of nested brackets in alt text (should not match)"""
        text = "Here's an ![alt [text] with brackets](https://example.com/img.jpg)"
        matches = extract_markdown_images(text)
        # Should not match due to nested brackets
        self.assertListEqual([], matches)

    def test_nested_brackets_in_anchor_text(self):
        """Test handling of nested brackets in anchor text (should not match)"""
        text = "Here's a [link [text] with brackets](https://example.com/page)"
        matches = extract_markdown_links(text)
        # Should not match due to nested brackets
        self.assertListEqual([], matches)

    def test_nested_parentheses_in_urls(self):
        """Test handling of nested parentheses in URLs (should not match)"""
        image_text = "Here's an ![image](https://example.com/img.jpg(extra))"
        link_text = "Here's a [link](https://example.com/page(extra))"
        
        image_matches = extract_markdown_images(image_text)
        link_matches = extract_markdown_links(link_text)
        
        # Should not match due to nested parentheses
        self.assertListEqual([], image_matches)
        self.assertListEqual([], link_matches)


if __name__ == "__main__":
    unittest.main() 