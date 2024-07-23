import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode



class TestHtmlNode(unittest.TestCase):
    def test_something(self):
        html_node = HtmlNode("p", "This is a paragraph", [],{
            "href": "https://www.google.com", 
            "target": "_blank",
            
        })
        self.assertEqual(html_node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")   
        
    def test_something2(self):
        html_node = HtmlNode()
        self.assertEqual(html_node.props_to_html(), "")   
        
    def test_something3(self):
        html_node = HtmlNode("p", "This is a paragraph", [],{
            "href": "https://www.google.com", 
            "target": "_blank",
            "rel": "nofollow"
            
        })
        self.assertEqual(html_node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\" rel=\"nofollow\"") 
        
class TestLeafNode(unittest.TestCase):
    def test_something(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf_node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_something2(self):
        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    
    def test_something3(self):
        leaf_node = LeafNode(None, "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(leaf_node.to_html(), "Click me!")
    
    def test_something4(self):
        leaf_node = LeafNode("a", None, {"href": "https://www.google.com", "target": "_blank", "rel": "nofollow"})
        with self.assertRaises(ValueError) as err: 
            leaf_node.to_html()
        self.assertEqual(str(err.exception), "Value cannot be empty")

class TestParentNode(unittest.TestCase):
    def test_something(self):
        parent_node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_something2(self):
        parent_node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            345,
        ])
        with self.assertRaises(ValueError) as err:
            parent_node.to_html()
        self.assertEqual(str(err.exception), "Children must be instance of HtmlNode")
        
    def test_something3(self):
        parent_node = ParentNode(None, [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            345,
        ])
        with self.assertRaises(ValueError) as err:
            parent_node.to_html()
        self.assertEqual(str(err.exception), "Tag cannot be empty")
        
    def test_something4(self):
        parent_node = ParentNode("p", [])
        with self.assertRaises(ValueError) as err:
            parent_node.to_html()
        self.assertEqual(str(err.exception), "Children cannot be empty")
    
    def test_something5(self):
        parent_node = ParentNode("p", [
                                 ParentNode("i", [
                                    LeafNode("b", "Bold text"), 
                                    LeafNode(None, "Normal text"), 
                                    LeafNode("i", "italic text"), 
                                    LeafNode(None, "Normal text")
                                 ]), 
                                  LeafNode(None, "Normal text")])
        self.assertEqual(parent_node.to_html(), "<p><i><b>Bold text</b>Normal text<i>italic text</i>Normal text</i>Normal text</p>")
        
        
if __name__ == "__main__":
    unittest.main()