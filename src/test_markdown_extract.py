import unittest
from markdown_extract import *

class TestExtractMarkdownImages(unittest.TestCase):
  def test_single_image(self):
    result = extract_markdown_images("![alt text](https://example.com/img.png)")
    self.assertEqual(result, [("alt text", "https://example.com/img.png")])

  def test_multiple_images(self):
    result = extract_markdown_images("![cat](cat.png) and ![dog](dog.png)")
    self.assertEqual(result, [("cat", "cat.png"), ("dog", "dog.png")])

  def test_empty_alt_text(self):
    result = extract_markdown_images("![](https://example.com/img.png)")
    self.assertEqual(result, [("", "https://example.com/img.png")])

  def test_no_images_returns_empty_list(self):
    result = extract_markdown_images("just plain text with no images")
    self.assertEqual(result, [])

  def test_link_syntax_not_captured_as_image(self):
    result = extract_markdown_images("[not an image](https://example.com)")
    self.assertEqual(result, [])

class TestExtractMarkdownLinks(unittest.TestCase):
  def test_single_link(self):
    result = extract_markdown_links("[click here](https://example.com)")
    self.assertEqual(result, [("click here", "https://example.com")])

  def test_multiple_links(self):
    result = extract_markdown_links("[google](https://google.com) and [bing](https://bing.com)")
    self.assertEqual(result, [("google", "https://google.com"), ("bing", "https://bing.com")])

  def test_image_syntax_not_captured_as_link(self):
    result = extract_markdown_links("![image](https://example.com/img.png)")
    self.assertEqual(result, [])

  def test_no_links_returns_empty_list(self):
    result = extract_markdown_links("just plain text with no links")
    self.assertEqual(result, [])

  def test_mixed_images_and_links_only_returns_links(self):
    text = "![img](img.png) and [link](https://example.com)"
    result = extract_markdown_links(text)
    self.assertEqual(result, [("link", "https://example.com")])