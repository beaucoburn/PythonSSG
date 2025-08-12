import re

def extract_markdown_images(text):
    """
    Extract markdown images from text using regex.
    Returns a list of tuples containing (alt_text, url).
    
    Args:
        text (str): Raw markdown text
        
    Returns:
        list: List of tuples with (alt_text, url)
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extract markdown links from text using regex.
    Returns a list of tuples containing (anchor_text, url).
    
    Args:
        text (str): Raw markdown text
        
    Returns:
        list: List of tuples with (anchor_text, url)
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches 