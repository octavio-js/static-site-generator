import unittest
from markdown_blocks import *

class TestMarkdownToBlocks(unittest.TestCase):
  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
        [
          "This is **bolded** paragraph",
          "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
          "- This is a list\n- with items",
        ],
    )

  def test_extra_blank_lines_between_blocks_are_ignored(self):
    md = "first block\n\n\n\nsecond block"
    result = markdown_to_blocks(md)
    self.assertEqual(result, ["first block", "second block"])

  def test_leading_and_trailing_whitespace_is_stripped(self):
    md = "   trimmed block   \n\n   another block   "
    result = markdown_to_blocks(md)
    self.assertEqual(result, ["trimmed block", "another block"])

  def test_empty_string_returns_empty_list(self):
    result = markdown_to_blocks("")
    self.assertEqual(result, [])

  def test_single_block_no_double_newline(self):
    md = "just one block\nstill one block"
    result = markdown_to_blocks(md)
    self.assertEqual(result, ["just one block\nstill one block"])
