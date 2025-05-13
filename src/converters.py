import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    if text_node.text_type in TextType:
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        if text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        if text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        if text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        if text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        if text_node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid or missing text node type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        first_index = node.text.find(delimiter) 
        if first_index == -1:
            new_nodes.append(node)
            continue
        start_content = first_index + len(delimiter)
        second_index = node.text.find(delimiter, start_content)
        if second_index == -1:
            raise Exception(f"Invalid markdown formatting: missing closing delimiter {delimiter}")
        end_content = second_index + len(delimiter)
        if first_index > 0:
            new_nodes.append(TextNode(node.text[0:first_index], TextType.TEXT))
        new_nodes.append(TextNode(node.text[start_content:second_index], text_type))
        if end_content < len(node.text):
            remaining_node = TextNode(node.text[end_content:], TextType.TEXT)
            new_nodes.extend(split_nodes_delimiter([remaining_node], delimiter, text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches