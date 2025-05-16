import re, textwrap
from htmlnode import ParentNode
from inline_functions import text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType
from block_functions import markdown_to_blocks, BlockType, block_to_block_type

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type in BlockType:
            if block_type == BlockType.PAR:
                child_block = ParentNode("p", text_to_children(" ".join(block.split())))
                children.append(child_block)
                continue
            if block_type == BlockType.HEAD:
                head = re.match(r'^#{1,6} ', block)
                head_level = len(head.group()) - 1
                block_slice = len(head.group())
                child_block = ParentNode(f"h{head_level}", text_to_children(block[block_slice:]))
                children.append(child_block)
                continue
            if block_type == BlockType.QUO:
                lines = block.split("\n")
                text = " ".join(map(lambda line : line.lstrip("> "), lines))
                child_block = ParentNode("blockquote", text_to_children(text))
                children.append(child_block)
                continue
            if block_type == BlockType.CODE:
                lines = block.split("\n")
                raw_list = []
                for line in lines:
                    if "```" in line:
                        continue
                    raw_list.append(line)
                raw_text = textwrap.dedent("\n".join(raw_list) + "\n")
                raw = TextNode(raw_text, TextType.TEXT)
                html = text_node_to_html_node(raw)
                child = ParentNode("code", [html])
                child_block = ParentNode("pre", [child])
                children.append(child_block)
                continue
            if block_type == BlockType.ULIST:
                lines = block.split("\n")
                textnode_lines = []
                for line in lines:
                    if line:
                        textnode_line = ParentNode("li", text_to_children(re.sub(r'^ *[*-] ', '', line)))
                        textnode_lines.append(textnode_line)
                child_block = ParentNode("ul", textnode_lines)
                children.append(child_block)
                continue
            if block_type == BlockType.OLIST:
                lines = block.split("\n")
                textnode_lines = []
                for line in lines:
                    if line:
                        textnode_line = ParentNode("li", text_to_children(re.sub(r'^ *\d+\. ', '', line)))
                        textnode_lines.append(textnode_line)
                child_block = ParentNode("ol", textnode_lines)
                children.append(child_block)
                continue
        raise ValueError(f"Invalid or missing block type")
    html_block = ParentNode("div", children)
    return html_block

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = list(map(lambda node : text_node_to_html_node(node), textnodes))
    return htmlnodes