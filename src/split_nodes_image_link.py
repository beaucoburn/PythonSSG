from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_image(old_nodes):
    """
    Split TextNodes based on markdown images.
    Only processes TEXT type nodes, others are passed through unchanged.
    
    Args:
        old_nodes (list): List of TextNode objects
        
    Returns:
        list: New list of TextNode objects with images split out
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all images from the text
        images = extract_markdown_images(old_node.text)
        
        # If no images found, add the original node
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Split the text around each image
        remaining_text = old_node.text
        
        for alt_text, url in images:
            # Find the image markdown in the remaining text
            image_markdown = f"![{alt_text}]({url})"
            
            # Split the remaining text around this image
            parts = remaining_text.split(image_markdown, 1)
            
            if len(parts) == 2:
                before_text, after_text = parts
                
                # Add text before the image (if not empty)
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.TEXT))
                
                # Add the image node
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                
                # Update remaining text for next iteration
                remaining_text = after_text
            else:
                # This shouldn't happen if extract_markdown_images worked correctly
                # Just add the remaining text as-is
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                break
        
        # Add any remaining text after the last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNodes based on markdown links.
    Only processes TEXT type nodes, others are passed through unchanged.
    
    Args:
        old_nodes (list): List of TextNode objects
        
    Returns:
        list: New list of TextNode objects with links split out
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all links from the text
        links = extract_markdown_links(old_node.text)
        
        # If no links found, add the original node
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Split the text around each link
        remaining_text = old_node.text
        
        for anchor_text, url in links:
            # Find the link markdown in the remaining text
            link_markdown = f"[{anchor_text}]({url})"
            
            # Split the remaining text around this link
            parts = remaining_text.split(link_markdown, 1)
            
            if len(parts) == 2:
                before_text, after_text = parts
                
                # Add text before the link (if not empty)
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.TEXT))
                
                # Add the link node
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                
                # Update remaining text for next iteration
                remaining_text = after_text
            else:
                # This shouldn't happen if extract_markdown_links worked correctly
                # Just add the remaining text as-is
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                break
        
        # Add any remaining text after the last link
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes
