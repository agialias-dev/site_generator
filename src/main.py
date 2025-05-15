from textnode import *
from htmlnode import *
from inline_functions import *
from block_functions import *

def main():
    # This should be a quote block, but your code might classify it as a paragraph
    mixed_quote = "> This is a quote\nThis line doesn't start with >"

    # This should be paragraph, not an unordered list
    mixed_list = "- This starts like a list\nBut this line doesn't"

    # This should be paragraph, not an ordered list
    mixed_ordered = "1. First item\nSecond item without number"

    # This should be paragraph because the numbers don't increment properly
    bad_ordered = "1. First item\n3. Third item"

    print(f"{block_to_block_type(mixed_quote)} # Should be paragraph, not quote")
    print(f"{block_to_block_type(mixed_list)} # Should be paragraph, not unordered_list")
    print(f"{block_to_block_type(mixed_ordered)} # Should be paragraph, not ordered_list")
    print(f"{block_to_block_type(bad_ordered)} # Should be paragraph, not ordered_list")
    

if __name__ == "__main__":
    main()