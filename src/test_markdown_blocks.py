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

class TestHeading(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.HEADING)

    def test_h3(self):
        self.assertEqual(block_to_block_type("### Section"), BlockType.HEADING)

    def test_h6(self):
        self.assertEqual(block_to_block_type("###### Deep"), BlockType.HEADING)

    def test_seven_hashes_is_paragraph(self):
        self.assertNotEqual(block_to_block_type("####### Too many"), BlockType.HEADING)

    def test_hash_without_space_is_paragraph(self):
        self.assertNotEqual(block_to_block_type("#NoSpace"), BlockType.HEADING)

    def test_hash_only_is_paragraph(self):
        self.assertNotEqual(block_to_block_type("#"), BlockType.HEADING)


class TestCode(unittest.TestCase):
    def test_basic_code_block(self):
        self.assertEqual(block_to_block_type("```\nprint('hello')\n```"), BlockType.CODE)

    def test_multiline_code_block(self):
        block = "```\ndef foo():\n    return 42\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_no_newline_after_backticks_is_not_code(self):
        self.assertNotEqual(block_to_block_type("```print('hello')```"), BlockType.CODE)

    def test_missing_closing_backticks_is_not_code(self):
        self.assertNotEqual(block_to_block_type("```\nsome code"), BlockType.CODE)

    def test_missing_opening_backticks_is_not_code(self):
        self.assertNotEqual(block_to_block_type("some code\n```"), BlockType.CODE)


class TestQuote(unittest.TestCase):
    def test_single_line_quote(self):
        self.assertEqual(block_to_block_type("> Hello"), BlockType.QUOTE)

    def test_quote_without_space(self):
        self.assertEqual(block_to_block_type(">Hello"), BlockType.QUOTE)

    def test_multiline_quote(self):
        block = "> line one\n> line two\n> line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_mixed_quote_and_plain_is_not_quote(self):
        self.assertNotEqual(block_to_block_type("> quoted\nnot quoted"), BlockType.QUOTE)

    def test_quote_with_space_after_arrow(self):
        block = "> with space\n> also space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


class TestUnorderedList(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_multiple_items(self):
        self.assertEqual(block_to_block_type("- one\n- two\n- three"), BlockType.UNORDERED_LIST)

    def test_dash_without_space_is_not_unordered(self):
        self.assertNotEqual(block_to_block_type("-no space"), BlockType.UNORDERED_LIST)

    def test_mixed_lines_is_not_unordered(self):
        self.assertNotEqual(block_to_block_type("- item\nno dash"), BlockType.UNORDERED_LIST)

    def test_asterisk_is_not_unordered(self):
        self.assertNotEqual(block_to_block_type("* item"), BlockType.UNORDERED_LIST)


class TestOrderedList(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ORDERED_LIST)

    def test_multiple_items(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_must_start_at_one(self):
        self.assertNotEqual(block_to_block_type("2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_non_sequential_is_not_ordered(self):
        self.assertNotEqual(block_to_block_type("1. first\n3. third"), BlockType.ORDERED_LIST)

    def test_missing_space_after_dot_is_not_ordered(self):
        self.assertNotEqual(block_to_block_type("1.no space\n2.also no space"), BlockType.ORDERED_LIST)

    def test_mixed_with_plain_line_is_not_ordered(self):
        self.assertNotEqual(block_to_block_type("1. first\nsecond"), BlockType.ORDERED_LIST)

    def test_large_ordered_list(self):
        block = "\n".join(f"{i}. item" for i in range(1, 11))
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


class TestParagraph(unittest.TestCase):
    def test_plain_text(self):
        self.assertEqual(block_to_block_type("Just some text."), BlockType.PARAGRAPH)

    def test_multiline_plain_text(self):
        self.assertEqual(block_to_block_type("First line.\nSecond line."), BlockType.PARAGRAPH)

    def test_empty_string(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
