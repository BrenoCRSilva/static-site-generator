class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text_type = text_type
        self.url = url
        self.text = text

    def __eq__(self, other: object) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode(text={self.text}, text_type={self.text_type}, url={self.url})"

