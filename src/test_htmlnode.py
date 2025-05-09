import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("tag", "value", None, {"class": "prop", "href": "http://example.com"})
        node2 = HTMLNode("tag", "value", None, {"class": "prop", "href": "http://example.com"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("tag", "value", "child", {"class": "prop", "href": "http://example.com"})
        node.props_to_html()

if __name__ == "__main__":
    unittest.main()