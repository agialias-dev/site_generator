import re, textwrap, os
from htmlnode import ParentNode
from inline_functions import text_node_to_html_node, text_to_textnodes, extract_title
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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path, "r")
    markdown = markdown_file.read()
    markdown_file.close()
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()
    html = markdown_to_html(markdown).to_html()
    title = extract_title(from_path)
    output =template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    html_file = open(f"{dest_path}/index.html", "w")
    html_file.write(output)
    html_file.close()
    print(f"Page generated in: {dest_path}")

def generate_pages_recursively(from_dir, template_path, dest_dir):
    for filename in os.listdir(from_dir):
        source_file_path = os.path.join(from_dir, filename)
        try:
            if os.path.isdir(source_file_path):
                os.mkdir(f"{dest_dir}/{filename}")
                recursive_src = f"{from_dir}/{filename}"
                recursive_dest = f"{dest_dir}/{filename}"
                generate_pages_recursively(recursive_src, template_path, recursive_dest)
            elif (os.path.isfile(source_file_path) or os.path.islink(source_file_path) and source_file_path.endswith(".md")):
                dest_file = f"{dest_dir}/{filename}"
                generate_page(source_file_path, template_path, dest_dir)
        except Exception as e:
            print('Failed to generate a HTML page from %s. Reason: %s' % (source_file_path, e))