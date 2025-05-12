from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import text_node_to_html_node

def main():
    textnode = TextNode("Anchor text.", TextType.LINK, "https://www.trollolol.lol")
    htmlnode = HTMLNode("p", "monkeys enjoy swinging", "child", {"class": "prop", "href": "http://example.com"})
    leafnode = LeafNode("b", "in the trees")
    parentnode = ParentNode("div", [LeafNode("i", "all the time")])
    
    print(f"{textnode}\n{htmlnode.props_to_html()}\n{leafnode.to_html()}\n{parentnode.to_html()}")
    print(text_node_to_html_node(textnode))

if __name__ == "__main__":
    main()