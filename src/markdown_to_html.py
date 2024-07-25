import re
from htmlnode import LeafNode
from textnode import TextNode



def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "text":
            return LeafNode(None, text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "image":
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Invalid text type: {text_node.text_type}")

def split_delimited_nodes(nodes: list, delimiter: str, text_type: str) -> list:
    new_nodes = []
    for node in nodes:
        if node.text_type in ["bold", "italic","code"] or (node.text_type == "text" and node.text.count(delimiter) == 0):
            new_nodes.append(node)
            continue
        
        if node.text_type == "text" and node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid markdown syntax")

        if node.text_type == "text" and node.text.count(delimiter) % 2 == 0:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, "text"))
                    else:
                        new_nodes.append(TextNode(part, text_type))
                    
    return new_nodes

def extract_markdown_links(text: str) -> list:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def extract_markdown_images(text: str) -> list:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def split_link_nodes(nodes):
    def helper(node, links):
        if not links:
            return [node]

        alt_text, url = links[0]
        before, link, after = node.text.partition(f"[{alt_text}]({url})")
        
        new_nodes = []

        if before:
            new_nodes.append(TextNode(before, "text"))

        new_nodes.append(TextNode(alt_text, "link", url))
        
        if after:
            remaining_node = TextNode(after, "text")
            new_nodes.extend(helper(remaining_node, links[1:]))

        return new_nodes

    result_nodes = []
    for node in nodes:
        links = extract_markdown_links(node.text)
        result_nodes.extend(helper(node, links))

    return result_nodes

def split_image_nodes(nodes):
    def helper(node, images):
        if not images:
            return [node]

        alt_text, url = images[0]
        before, image, after = node.text.partition(f"![{alt_text}]({url})")
        
        new_nodes = []

        if before:
            new_nodes.append(TextNode(before, "text"))

        new_nodes.append(TextNode(alt_text, "image", url))
        
        if after:
            remaining_node = TextNode(after, "text")
            new_nodes.extend(helper(remaining_node, images[1:]))

        return new_nodes

    result_nodes = []
    for node in nodes:
        images = extract_markdown_images(node.text)
        result_nodes.extend(helper(node, images))

    return result_nodes

def markdown_to_text_nodes(text: str) -> list:
    node = TextNode(text, "text")
    nodes = split_delimited_nodes([node], "**", "bold")
    nodes = split_delimited_nodes(nodes, "*", "italic")
    nodes = split_delimited_nodes(nodes, "`", "code")
    nodes = split_image_nodes(nodes)
    nodes = split_link_nodes(nodes)
    return nodes