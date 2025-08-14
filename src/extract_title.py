def extract_title(markdown):
    """
    Extract the h1 header from markdown content.
    
    Args:
        markdown (str): Raw markdown text
        
    Returns:
        str: The title from the h1 header (without # and whitespace)
        
    Raises:
        ValueError: If no h1 header is found
    """
    lines = markdown.split('\n')
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('# '):
            # Extract the title (remove the # and leading/trailing whitespace)
            title = stripped_line[1:].strip()
            return title
    
    # If no h1 header is found, raise an exception
    raise ValueError("No h1 header found in markdown")
