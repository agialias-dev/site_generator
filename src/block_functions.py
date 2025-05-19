import re
from enum import Enum

class BlockType(Enum):
    PAR = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUO = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block.split():
            block = block.strip()
            filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEAD
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PAR
        return BlockType.QUO
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PAR
        return BlockType.ULIST
    if re.match(r'^ *\d+\. ', block):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PAR
            i += 1
        return BlockType.OLIST
    return BlockType.PAR