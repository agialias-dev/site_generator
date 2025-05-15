def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block.split():
            block = block.strip()
            filtered_blocks.append(block)
    return filtered_blocks