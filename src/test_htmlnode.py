import unittest
from htmlnode import HTMLNode

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
