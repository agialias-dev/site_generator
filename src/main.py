from textnode import TextNode, TextType

def main():
    textnode = TextNode("Anchor text.", TextType.LINK, "https://www.trollolol.lol")

    print(textnode)

if __name__ == "__main__":
    main()
