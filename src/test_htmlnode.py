import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("tag", "value", None, {"class": "prop", "href": "http://example.com"})
        node2 = HTMLNode("tag", "value", None, {"class": "prop", "href": "http://example.com"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("tag", "value", "child", {"class": "prop", "href": "http://example.com"})
        self.assertEqual(node.props_to_html(), ' class="prop" href="http://example.com"')

    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(node.__repr__(), "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})")

if __name__ == "__main__":
    unittest.main()