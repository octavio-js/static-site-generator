import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
  def test_props(self):
    node = HTMLNode("a", "hello world", None, {"href": "https://www.google.com", "target": "_blank"})
    p = node.props_to_html()
    self.assertEqual(p, ' href="https://www.google.com" target="_blank"')

  def test_no_props(self):
    node = HTMLNode("h1", "hello world")
    p = node.props_to_html()
    self.assertEqual(p, "")

  def test_empty_props(self):
    node = HTMLNode("h1", "hello world", None, {})
    p = node.props_to_html()
    self.assertEqual(p, "")

  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_a_props(self):
    node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com", "target": "_blank"})
    self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Hello, world!</a>')

  def test_leaf_to_html_h1(self):
    node = LeafNode("h1", "Hello, world!")
    self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")
