import unittest
from textnode import *
from htmlnode import *
from inline_functions import *


class TestTexttoHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is an image"})

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([TextNode("This is text with a ", TextType.TEXT), TextNode("bolded", TextType.BOLD), TextNode(" word", TextType.TEXT)], new_nodes)

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT), TextNode("bolded", TextType.BOLD), TextNode(" word and ", TextType.TEXT), TextNode("another", TextType.BOLD)], new_nodes)

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([TextNode("This is text with a ", TextType.TEXT), TextNode("bolded word", TextType.BOLD), 
                              TextNode(" and ", TextType.TEXT), TextNode("another", TextType.BOLD)], new_nodes)

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.TEXT)], new_nodes)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual([TextNode("bold", TextType.BOLD), TextNode(" and ", TextType.TEXT), TextNode("italic", TextType.ITALIC)], new_nodes)

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual([TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)], new_nodes)

    
class TestImageandLinkExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)")
        self.assertListEqual([("link", "https://boot.dev"), ("another link", "https://blog.boot.dev")], matches)


class TestImageandLinkSplitters(unittest.TestCase):
    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT), TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")], new_nodes)
    
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG")], new_nodes)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT), TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")], new_nodes)

    def test_split_links(self):
        node = TextNode("This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev"), TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"), TextNode(" with text that follows", TextType.TEXT)], new_nodes)
        
class TestFinalConversion(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("This is ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev")], nodes)

class TestTitleExtraction(unittest.TestCase):
    def test_title_extraction(self):
        text = "/home/agialias/projects/site_generator/content/index.md"
        title = extract_title(text)
        self.assertEqual(title, "# Tolkien Fan Club")
    
    #def test_title_extraction_no_title(self):
    #    text = "This is not a title"
    #    self.assertRaises(ValueError, extract_title, text)

    #def test_title_extraction_h2(self):
    #    text = "## This is a h2 title"
    #    self.assertRaises(ValueError, extract_title, text)

    #def test_title_extraction_whitspace(self):
    #    text = " #  This is a title"
    #    self.assertRaises(ValueError, extract_title, text)

if __name__ == "__main__":
    unittest.main()