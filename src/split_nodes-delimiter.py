from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        parts = old_node.text.split(delimiter)
        
        # If there's only one part, no delimiter was found
        if len(parts) == 1:
            new_nodes.append(old_node)
            continue
        
        # Check if we have an even number of parts (matching delimiters)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: unmatched delimiter '{delimiter}'")
        
        # Process the parts
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Even indices are regular text (outside delimiters)
                if part:  # Only add non-empty parts
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd indices are content between delimiters
                if not part:  # Empty content between delimiters is invalid
                    raise ValueError(f"Invalid markdown syntax: empty content between '{delimiter}' delimiters")
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes
