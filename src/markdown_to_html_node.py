from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type
from block_type import BlockType
from text_to_textnodes import text_to_textnodes
from text_node_to_html_node import text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode


def text_to_children(text):
    """
    Convert text with inline markdown to a list of HTMLNodes.
    
    Args:
        text (str): Text that may contain inline markdown
        
    Returns:
        list: List of HTMLNode objects representing the inline markdown
    """
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    return html_nodes


def paragraph_to_html_node(block):
    """
    Convert a paragraph block to an HTMLNode.
    
    Args:
        block (str): The paragraph text
        
    Returns:
        ParentNode: A <p> tag containing the paragraph content
    """
    # Convert newlines to spaces for paragraphs
    normalized_block = block.replace('\n', ' ')
    
    children = text_to_children(normalized_block)
    return ParentNode(tag="p", children=children)


def heading_to_html_node(block):
    """
    Convert a heading block to an HTMLNode.
    
    Args:
        block (str): The heading text (e.g., "# Heading")
        
    Returns:
        ParentNode: An <h1> to <h6> tag containing the heading content
    """
    # Count the # characters to determine heading level
    hash_count = 0
    for char in block:
        if char == '#':
            hash_count += 1
        else:
            break
    
    # Extract the heading text (remove the # characters and leading space)
    heading_text = block[hash_count + 1:]
    
    # Create the appropriate heading tag
    tag = f"h{hash_count}"
    
    # Convert inline markdown in the heading
    children = text_to_children(heading_text)
    
    return ParentNode(tag=tag, children=children)


def code_to_html_node(block):
    """
    Convert a code block to an HTMLNode.
    
    Args:
        block (str): The code block text (with ``` delimiters)
        
    Returns:
        ParentNode: A <pre><code> structure containing the code
    """
    # Remove the opening and closing ``` delimiters
    code_content = block[3:-3]
    
    # Strip leading whitespace but preserve internal structure
    code_content = code_content.lstrip()
    
    # For code blocks, don't parse inline markdown - treat as plain text
    code_node = LeafNode(tag="code", value=code_content)
    
    return ParentNode(tag="pre", children=[code_node])


def quote_to_html_node(block):
    """
    Convert a quote block to an HTMLNode.
    
    Args:
        block (str): The quote text (with > prefixes)
        
    Returns:
        ParentNode: A <blockquote> tag containing the quote content
    """
    # Remove the > prefix from each line
    lines = block.split('\n')
    quote_lines = []
    
    for line in lines:
        if line.startswith('>'):
            quote_lines.append(line[1:].lstrip())  # Remove > and leading whitespace
    
    # Join the lines back together
    quote_text = '\n'.join(quote_lines)
    
    # Convert inline markdown in the quote
    children = text_to_children(quote_text)
    
    return ParentNode(tag="blockquote", children=children)


def unordered_list_to_html_node(block):
    """
    Convert an unordered list block to an HTMLNode.
    
    Args:
        block (str): The list text (with - prefixes)
        
    Returns:
        ParentNode: A <ul> tag containing <li> items
    """
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        if line.startswith('- '):
            # Remove the - prefix and convert inline markdown
            item_text = line[2:]
            item_children = text_to_children(item_text)
            list_item = ParentNode(tag="li", children=item_children)
            list_items.append(list_item)
    
    return ParentNode(tag="ul", children=list_items)


def ordered_list_to_html_node(block):
    """
    Convert an ordered list block to an HTMLNode.
    
    Args:
        block (str): The list text (with 1. 2. prefixes)
        
    Returns:
        ParentNode: An <ol> tag containing <li> items
    """
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Find the period and space after the number
        period_index = line.find('. ')
        if period_index != -1:
            # Remove the number, period, and space prefix
            item_text = line[period_index + 2:]
            item_children = text_to_children(item_text)
            list_item = ParentNode(tag="li", children=item_children)
            list_items.append(list_item)
    
    return ParentNode(tag="ol", children=list_items)


def block_to_html_node(block):
    """
    Convert a single block to an HTMLNode based on its type.
    
    Args:
        block (str): A single markdown block
        
    Returns:
        HTMLNode: The appropriate HTML node for the block type
    """
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unsupported block type: {block_type}")


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    
    Args:
        markdown (str): Raw markdown text representing a full document
        
    Returns:
        ParentNode: A <div> tag containing all the converted blocks
    """
    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Convert each block to an HTML node
    html_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        html_nodes.append(html_node)
    
    # Create a parent div containing all the blocks
    return ParentNode(tag="div", children=html_nodes)
