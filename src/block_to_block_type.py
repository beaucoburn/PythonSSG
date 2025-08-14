from block_type import BlockType


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block (str): A single block of markdown text (whitespace already stripped)
        
    Returns:
        BlockType: The type of the block
    """
    lines = block.split('\n')
    
    # Check if it's a code block (starts and ends with 3 backticks)
    if block.startswith('```') and block.endswith('```') and len(block) >= 6:
        return BlockType.CODE
    
    # Check if it's a heading (starts with 1-6 # characters followed by a space)
    if lines[0].startswith('#'):
        # Count the # characters
        hash_count = 0
        for char in lines[0]:
            if char == '#':
                hash_count += 1
            else:
                break
        
        # Check if it's 1-6 # characters followed by a space
        if 1 <= hash_count <= 6 and lines[0][hash_count:].startswith(' '):
            return BlockType.HEADING
    
    # Check if it's a quote block (every line starts with >)
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check if it's an unordered list (every line starts with - followed by a space)
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check if it's an ordered list (every line starts with number. followed by a space)
    if len(lines) > 0:
        # Check if first line matches the pattern
        if lines[0].startswith('1. '):
            # Check if all subsequent lines increment properly
            for i, line in enumerate(lines):
                expected_number = i + 1
                expected_prefix = f"{expected_number}. "
                if not line.startswith(expected_prefix):
                    break
            else:
                # All lines matched the pattern
                return BlockType.ORDERED_LIST
    
    # If none of the above, it's a paragraph
    return BlockType.PARAGRAPH
