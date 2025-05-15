import unittest
from block_functions import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestMarkdownToBlocks(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEAD)
        block = "### This is a heading!"
        self.assertEqual(block_to_block_type(block), BlockType.HEAD)
        block = "```some code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = ">So quoth the raven."
        self.assertEqual(block_to_block_type(block), BlockType.QUO)
        block = "- List item ~"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. List item one."
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "Just a plain ol' paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PAR)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUO)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PAR)

    def test_block_to_block_type_errors(self):
        mixed_quote = "> This is a quote\nThis line doesn't start with >"
        self.assertEqual(block_to_block_type(mixed_quote), BlockType.PAR)
        mixed_list = "- This starts like a list\nBut this line doesn't"
        self.assertEqual(block_to_block_type(mixed_list), BlockType.PAR)
        mixed_ordered = "1. First item\nSecond item without number"
        self.assertEqual(block_to_block_type(mixed_ordered), BlockType.PAR)
        bad_ordered = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(bad_ordered), BlockType.PAR)


if __name__ == "__main__":
    unittest.main()