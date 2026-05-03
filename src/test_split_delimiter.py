import unittest
from split_delimiter import *
from textnode import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
  def test_single_bold_word_middle(self):
    node = TextNode("Hello **world** today", TextType.PLAIN)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(result[0], TextNode("Hello ", TextType.PLAIN))
    self.assertEqual(result[1], TextNode("world", TextType.BOLD))
    self.assertEqual(result[2], TextNode(" today", TextType.PLAIN))

  def test_single_code_word(self):
    node = TextNode("Use `print()` here", TextType.PLAIN)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(result[0], TextNode("Use ", TextType.PLAIN))
    self.assertEqual(result[1], TextNode("print()", TextType.CODE))
    self.assertEqual(result[2], TextNode(" here", TextType.PLAIN))

  def test_italic_delimiter(self):
    node = TextNode("This is *italic* text", TextType.PLAIN)
    result = split_nodes_delimiter([node], "*", TextType.ITALIC)
    self.assertEqual(result[1], TextNode("italic", TextType.ITALIC))

  def test_result_length_single_delimited_word(self):
    node = TextNode("a **b** c", TextType.PLAIN)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(len(result), 3)

  def test_multiple_delimited_sections(self):
    node = TextNode("**a** and **b**", TextType.PLAIN)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(len(result), 5)
    self.assertEqual(result[1], TextNode("a", TextType.BOLD))
    self.assertEqual(result[3], TextNode("b", TextType.BOLD))

  def test_non_plain_node_passes_through(self):
    node = TextNode("already bold", TextType.BOLD)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0], TextNode("already bold", TextType.BOLD))

  def test_non_plain_node_is_not_modified(self):
    node = TextNode("`code`", TextType.CODE)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(result[0], node)

  def test_mixed_plain_and_non_plain(self):
    nodes = [
      TextNode("already bold", TextType.BOLD),
      TextNode("hello **world**", TextType.PLAIN),
    ]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    self.assertEqual(result[0], TextNode("already bold", TextType.BOLD))
    self.assertEqual(result[2], TextNode("world", TextType.BOLD))

  def test_no_delimiter_in_text(self):
    node = TextNode("plain text only", TextType.PLAIN)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0], TextNode("plain text only", TextType.PLAIN))

  def test_delimiter_at_start_produces_empty_plain_node(self):
    node = TextNode("**bold** then text", TextType.PLAIN)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(result[0], TextNode("", TextType.PLAIN))
    self.assertEqual(result[1], TextNode("bold", TextType.BOLD))

  def test_delimiter_at_end_produces_empty_plain_node(self):
    node = TextNode("text then **bold**", TextType.PLAIN)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(result[-1], TextNode("", TextType.PLAIN))

  def test_empty_node_list(self):
    result = split_nodes_delimiter([], "**", TextType.BOLD)
    self.assertEqual(result, [])

  def test_empty_string_node(self):
    node = TextNode("", TextType.PLAIN)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0], TextNode("", TextType.PLAIN))
