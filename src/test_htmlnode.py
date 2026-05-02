import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
  # HTMLNode tests
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

  # LeafNode tests
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_a_props(self):
    node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com", "target": "_blank"})
    self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Hello, world!</a>')

  def test_leaf_to_html_h1(self):
    node = LeafNode("h1", "Hello, world!")
    self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

  # ParentNode tests
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

  def test_to_html_with_multiple_children(self):
    child1 = LeafNode("span", "first")
    child2 = LeafNode("p", "second")
    child3 = LeafNode("b", "third")
    parent_node = ParentNode("div", [child1, child2, child3])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span>first</span><p>second</p><b>third</b></div>"
    )
