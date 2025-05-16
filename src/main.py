from textnode import *
from htmlnode import *
from inline_functions import *
from block_functions import *
from final_functions import *

def main():
    md = "#Heading with no space\n"

    md2 = "This   is   a   test\nfor   spacing."

    md3 = "  234. List item\n  2. Another item"

    md4 = "Not actually a quote\n> This is a quote"

    html = markdown_to_html(md)
    html2 = markdown_to_html(md2)
    html3 = markdown_to_html(md3)
    html4 = markdown_to_html(md4)

    print(html.to_html())
    print(html2.to_html())
    print(html3.to_html())
    print(html4.to_html())

if __name__ == "__main__":
    main()