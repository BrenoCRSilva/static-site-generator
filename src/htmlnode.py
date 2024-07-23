import functools
import operator

class HtmlNode:
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props  
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props: return ""
        return functools.reduce(operator.add, map(lambda x: f" {x[0]}=\"{x[1]}\"", self.props.items()), "")
    
    def __repr__(self) -> str:
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HtmlNode):
    def __init__(self, tag: str, value: str, props: dict=None):
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if not self.value: 
            raise ValueError("Value cannot be empty")
        if not self.tag: 
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list, props: dict=None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self):
        if not self.tag: 
            raise ValueError("Tag cannot be empty")
        if not self.children: 
            raise ValueError("Children cannot be empty")
        for child in self.children:
            if not isinstance(child, HtmlNode):
                raise ValueError("Children must be instance of HtmlNode")
            
        return f"<{self.tag}>" + "".join(map(lambda x: x.to_html(), self.children)) + f"</{self.tag}>"