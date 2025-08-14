def markdown_to_blocks(markdown):
    """
    Split markdown text into blocks separated by blank lines.
    
    Args:
        markdown (str): Raw markdown text representing a full document
        
    Returns:
        list: List of block strings with leading/trailing whitespace stripped
    """
    # Split by double newlines to separate blocks
    blocks = markdown.split("\n\n")
    
    # Strip whitespace from each block and filter out empty blocks
    cleaned_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only add non-empty blocks
            cleaned_blocks.append(stripped_block)
    
    return cleaned_blocks
