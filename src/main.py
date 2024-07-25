
from htmlnode import markdown_to_text_nodes

from textnode import TextNode
def main():
    print(markdown_to_text_nodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"))
main()
