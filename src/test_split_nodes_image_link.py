import unittest
from textnode import TextNode, TextType
from split_nodes_image_link import split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):

    def test_split_images(self):
        """Test splitting with multiple images"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_single_image(self):
        """Test splitting with a single image"""
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and some more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and some more text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_image_at_start(self):
        """Test image at the beginning of text"""
        node = TextNode(
            "![start image](https://example.com/start.jpg) and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start image", TextType.IMAGE, "https://example.com/start.jpg"),
            TextNode(" and some text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_image_at_end(self):
        """Test image at the end of text"""
        node = TextNode(
            "Some text and ![end image](https://example.com/end.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Some text and ", TextType.TEXT),
            TextNode("end image", TextType.IMAGE, "https://example.com/end.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_image_only(self):
        """Test text that is only an image"""
        node = TextNode(
            "![only image](https://example.com/image.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("only image", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_no_images(self):
        """Test text with no images returns original node"""
        node = TextNode("This is just plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_non_text_node_passed_through(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Code text", TextType.CODE),
        ]
        new_nodes = split_nodes_image(nodes)
        
        # The BOLD and CODE nodes should be unchanged
        self.assertEqual(new_nodes[1].text, "Bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "Code text")
        self.assertEqual(new_nodes[2].text_type, TextType.CODE)

    def test_multiple_nodes_input(self):
        """Test processing multiple nodes in input list"""
        nodes = [
            TextNode("First ![image](https://example.com/first.jpg) node", TextType.TEXT),
            TextNode("Already image", TextType.IMAGE, "https://example.com/already.jpg"),
            TextNode("Second ![image](https://example.com/second.jpg) node", TextType.TEXT),
        ]
        
        new_nodes = split_nodes_image(nodes)
        
        # Should have: First + image + node + already image + Second + image + node
        # The IMAGE node should be unchanged
        image_node = None
        for node in new_nodes:
            if node.text_type == TextType.IMAGE and node.url == "https://example.com/already.jpg":
                image_node = node
                break
        
        self.assertIsNotNone(image_node)
        self.assertEqual(image_node.text, "Already image")

    def test_empty_input_list(self):
        """Test empty input list"""
        new_nodes = split_nodes_image([])
        self.assertEqual(len(new_nodes), 0)

    def test_image_with_spaces_in_alt_text(self):
        """Test image with spaces in alt text"""
        node = TextNode(
            "Here's an ![alt text with spaces](https://example.com/image.jpg) in the middle",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Here's an ", TextType.TEXT),
            TextNode("alt text with spaces", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_image_with_special_chars_in_alt_text(self):
        """Test image with special characters in alt text"""
        node = TextNode(
            "Here's an ![alt-text_with.special@chars](https://example.com/image.jpg) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Here's an ", TextType.TEXT),
            TextNode("alt-text_with.special@chars", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_image_with_complex_url(self):
        """Test image with complex URL"""
        node = TextNode(
            "Here's an ![image](https://example.com/path/to/image.jpg?param=value&other=123) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Here's an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/path/to/image.jpg?param=value&other=123"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_adjacent_images(self):
        """Test adjacent images with no text between them"""
        node = TextNode(
            "![first](https://example.com/first.jpg)![second](https://example.com/second.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "https://example.com/first.jpg"),
            TextNode("second", TextType.IMAGE, "https://example.com/second.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_image_with_empty_alt_text(self):
        """Test image with empty alt text"""
        node = TextNode(
            "Here's an ![]() image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Here's an ", TextType.TEXT),
            TextNode("", TextType.IMAGE, ""),
            TextNode(" image", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)


class TestSplitNodesLink(unittest.TestCase):

    def test_split_links(self):
        """Test splitting with multiple links"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_single_link(self):
        """Test splitting with a single link"""
        node = TextNode(
            "This is text with a [single link](https://example.com) and some more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("single link", TextType.LINK, "https://example.com"),
            TextNode(" and some more text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_link_at_start(self):
        """Test link at the beginning of text"""
        node = TextNode(
            "[start link](https://example.com/start) and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start link", TextType.LINK, "https://example.com/start"),
            TextNode(" and some text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_link_at_end(self):
        """Test link at the end of text"""
        node = TextNode(
            "Some text and [end link](https://example.com/end)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Some text and ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "https://example.com/end"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_link_only(self):
        """Test text that is only a link"""
        node = TextNode(
            "[only link](https://example.com/link)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("only link", TextType.LINK, "https://example.com/link"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_no_links(self):
        """Test text with no links returns original node"""
        node = TextNode("This is just plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_non_text_node_passed_through(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Link text", TextType.LINK, "https://example.com"),
        ]
        new_nodes = split_nodes_link(nodes)
        
        # The BOLD and LINK nodes should be unchanged
        self.assertEqual(new_nodes[1].text, "Bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "Link text")
        self.assertEqual(new_nodes[2].text_type, TextType.LINK)

    def test_multiple_nodes_input(self):
        """Test processing multiple nodes in input list"""
        nodes = [
            TextNode("First [link](https://example.com/first) node", TextType.TEXT),
            TextNode("Already link", TextType.LINK, "https://example.com/already"),
            TextNode("Second [link](https://example.com/second) node", TextType.TEXT),
        ]
        
        new_nodes = split_nodes_link(nodes)
        
        # Should have: First + link + node + already link + Second + link + node
        # The LINK node should be unchanged
        link_node = None
        for node in new_nodes:
            if node.text_type == TextType.LINK and node.url == "https://example.com/already":
                link_node = node
                break
        
        self.assertIsNotNone(link_node)
        self.assertEqual(link_node.text, "Already link")

    def test_empty_input_list(self):
        """Test empty input list"""
        new_nodes = split_nodes_link([])
        self.assertEqual(len(new_nodes), 0)

    def test_link_with_spaces_in_anchor_text(self):
        """Test link with spaces in anchor text"""
        node = TextNode(
            "Here's a [link with spaces](https://example.com/page) in the middle",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here's a ", TextType.TEXT),
            TextNode("link with spaces", TextType.LINK, "https://example.com/page"),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_link_with_special_chars_in_anchor_text(self):
        """Test link with special characters in anchor text"""
        node = TextNode(
            "Here's a [link-with.special@chars](https://example.com/page) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here's a ", TextType.TEXT),
            TextNode("link-with.special@chars", TextType.LINK, "https://example.com/page"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_link_with_complex_url(self):
        """Test link with complex URL"""
        node = TextNode(
            "Here's a [link](https://example.com/path/to/page?param=value&other=123#section) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here's a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/path/to/page?param=value&other=123#section"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_adjacent_links(self):
        """Test adjacent links with no text between them"""
        node = TextNode(
            "[first](https://example.com/first)[second](https://example.com/second)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "https://example.com/first"),
            TextNode("second", TextType.LINK, "https://example.com/second"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_link_with_empty_anchor_text(self):
        """Test link with empty anchor text"""
        node = TextNode(
            "Here's a []() link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here's a ", TextType.TEXT),
            TextNode("", TextType.LINK, ""),
            TextNode(" link", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_mixed_images_and_links(self):
        """Test text with both images and links"""
        node = TextNode(
            "Here's an ![image](https://example.com/img.jpg) and a [link](https://example.com/page)",
            TextType.TEXT,
        )
        
        # Test image splitting
        image_nodes = split_nodes_image([node])
        expected_images = [
            TextNode("Here's an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" and a [link](https://example.com/page)", TextType.TEXT),
        ]
        self.assertListEqual(expected_images, image_nodes)
        
        # Test link splitting on the result
        link_nodes = split_nodes_link(image_nodes)
        expected_final = [
            TextNode("Here's an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/page"),
        ]
        self.assertListEqual(expected_final, link_nodes)

    def test_links_not_confused_with_images(self):
        """Test that links are not confused with images"""
        node = TextNode(
            "Here's a ![image](https://example.com/img.jpg) and a [link](https://example.com/page)",
            TextType.TEXT,
        )
        
        # Should only find the link, not the image
        link_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here's a ![image](https://example.com/img.jpg) and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/page"),
        ]
        self.assertListEqual(expected, link_nodes)


if __name__ == "__main__":
    unittest.main()
