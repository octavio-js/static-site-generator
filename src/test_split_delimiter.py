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

class TestSplitNodesImage(unittest.TestCase):
  def test_single_image_only(self):
    node = TextNode("![cat](cat.png)", TextType.PLAIN)
    result = split_nodes_image([node])
    self.assertEqual(result, [TextNode("cat", TextType.IMAGE, "cat.png")])

  def test_image_with_surrounding_text(self):
    node = TextNode("before ![cat](cat.png) after", TextType.PLAIN)
    result = split_nodes_image([node])
    self.assertEqual(result[0], TextNode("before ", TextType.PLAIN))
    self.assertEqual(result[1], TextNode("cat", TextType.IMAGE, "cat.png"))
    self.assertEqual(result[2], TextNode(" after", TextType.PLAIN))

  def test_multiple_images(self):
    node = TextNode("![a](a.png)![b](b.png)", TextType.PLAIN)
    result = split_nodes_image([node])
    self.assertEqual(result[0], TextNode("a", TextType.IMAGE, "a.png"))
    self.assertEqual(result[1], TextNode("b", TextType.IMAGE, "b.png"))

  def test_non_plain_node_passes_through_unchanged(self):
    node = TextNode("![cat](cat.png)", TextType.BOLD)
    result = split_nodes_image([node])
    self.assertEqual(result, [node])

  def test_no_images_passes_through_unchanged(self):
    node = TextNode("no images here", TextType.PLAIN)
    result = split_nodes_image([node])
    self.assertEqual(result, [node])


class TestSplitNodesLink(unittest.TestCase):
  def test_single_link_only(self):
    node = TextNode("[click](https://example.com)", TextType.PLAIN)
    result = split_nodes_link([node])
    self.assertEqual(result, [TextNode("click", TextType.LINK, "https://example.com")])

  def test_link_with_surrounding_text(self):
    node = TextNode("visit [example](https://example.com) now", TextType.PLAIN)
    result = split_nodes_link([node])
    self.assertEqual(result[0], TextNode("visit ", TextType.PLAIN))
    self.assertEqual(result[1], TextNode("example", TextType.LINK, "https://example.com"))
    self.assertEqual(result[2], TextNode(" now", TextType.PLAIN))

  def test_multiple_links(self):
    node = TextNode("[a](a.com) and [b](b.com)", TextType.PLAIN)
    result = split_nodes_link([node])
    self.assertEqual(result[0], TextNode("a", TextType.LINK, "a.com"))
    self.assertEqual(result[2], TextNode("b", TextType.LINK, "b.com"))

  def test_non_plain_node_passes_through_unchanged(self):
    node = TextNode("[click](https://example.com)", TextType.BOLD)
    result = split_nodes_link([node])
    self.assertEqual(result, [node])

  def test_no_links_passes_through_unchanged(self):
    node = TextNode("no links here", TextType.PLAIN)
    result = split_nodes_link([node])
    self.assertEqual(result, [node])

class TestTextToTextNodes(unittest.TestCase):
  def test_plain_text_returns_single_plain_node(self):
    result = text_to_textnodes("just plain text")
    self.assertEqual(result, [TextNode("just plain text", TextType.PLAIN)])

  def test_bold_text(self):
    result = text_to_textnodes("**bold**")
    bold_nodes = [n for n in result if n.text_type == TextType.BOLD]
    self.assertEqual(bold_nodes, [TextNode("bold", TextType.BOLD)])

  def test_all_types_in_one_string(self):
    text = "**bold** _italic_ `code` ![img](img.png) [link](https://example.com)"
    result = text_to_textnodes(text)
    types = [n.text_type for n in result]
    self.assertIn(TextType.BOLD, types)
    self.assertIn(TextType.ITALIC, types)
    self.assertIn(TextType.CODE, types)
    self.assertIn(TextType.IMAGE, types)
    self.assertIn(TextType.LINK, types)

  def test_image_node_has_correct_url(self):
    result = text_to_textnodes("![cat](cat.png)")
    image_nodes = [n for n in result if n.text_type == TextType.IMAGE]
    self.assertEqual(image_nodes, [TextNode("cat", TextType.IMAGE, "cat.png")])

  def test_link_node_has_correct_url(self):
    result = text_to_textnodes("[click](https://example.com)")
    link_nodes = [n for n in result if n.text_type == TextType.LINK]
    self.assertEqual(link_nodes, [TextNode("click", TextType.LINK, "https://example.com")])
