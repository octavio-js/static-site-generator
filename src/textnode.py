from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
  PLAIN = "plain"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"

class TextNode:
  def __init__(self, text, text_type, url = None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, other):
    return True if self.text == other.text and self.text_type.value == other.text_type.value and self.url == other.url else False

  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
  if text_node.text_type.value not in TextType:
    raise ValueError("The text type of the node is not valid")

  match text_node.text_type.value:
    case "plain":
      return LeafNode(None, text_node.text)
    case "bold":
      return LeafNode("b", text_node.text)
    case "italic":
      return LeafNode("i", text_node.text)
    case "code":
      return LeafNode("code", text_node.text)
    case "link":
      return LeafNode("a", text_node.text, {"href": text_node.url})
    case "image":
      return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    case _:
      raise ValueError("idk, this should not happen. if it does, something weird is going on, or i didnt write this right")
