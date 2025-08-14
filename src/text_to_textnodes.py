from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter
from split_nodes_image_link import split_nodes_image, split_nodes_link


def text_to_textnodes(text):
    """
    Convert raw markdown text into a list of TextNode objects.
    
    Args:
        text (str): Raw markdown text
        
    Returns:
        list: List of TextNode objects representing the parsed markdown
    """
    # Start with a single TextNode containing the entire text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split by images first (since they contain square brackets that could interfere with links)
    nodes = split_nodes_image(nodes)
    
    # Split by links
    nodes = split_nodes_link(nodes)
    
    # Split by bold text (double asterisks)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Split by italic text (single underscores)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # Split by code blocks (backticks)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes
