import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
  # TextNode tests
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_not_eq_text(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is another text node", TextType.BOLD)
    self.assertNotEqual(node, node2)

  def test_not_eq_text_type(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.PLAIN)
    self.assertNotEqual(node, node2)

  def test_not_eq_url(self):
    node = TextNode("This is a text node", TextType.BOLD, "https://youtube.com")
    node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
    self.assertNotEqual(node, node2)

  def test_eq_none_url(self):
    node = TextNode("This is a text node", TextType.BOLD, None)
    node2 = TextNode("This is a text node", TextType.BOLD, None)
    self.assertEqual(node, node2)

  # text_node_to_html_node tests
  def test_text(self):
    node = TextNode("This is a text node", TextType.PLAIN)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_bold(self):
    node = TextNode("bold text", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "bold text")

  def test_italic(self):
    node = TextNode("italic text", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "italic text")

  def test_code(self):
    node = TextNode("code text", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "code text")

  def test_link(self):
    node = TextNode("click me", TextType.LINK, "https://example.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "click me")
    self.assertEqual(html_node.props, {"href": "https://example.com"})

  def test_image(self):
    node = TextNode("alt text", TextType.IMAGE, "https://example.com/img.png")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(html_node.props, {"src": "https://example.com/img.png", "alt": "alt text"})


if __name__ == "__main__":
  unittest.main()
