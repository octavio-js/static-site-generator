from textnode import TextNode, TextType
from markdown_extract import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []

  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
      continue

    separated = node.text.split(delimiter)

    if len(separated) % 2 == 0:
      raise Exception("Invalid Markdown syntax!")

    for i, text in enumerate(separated):
      text_node = None
      if i % 2 == 0:
        text_node = TextNode(text, TextType.PLAIN)
      else:
        text_node = TextNode(text, text_type)

      new_nodes.append(text_node)

  return new_nodes

def split_nodes_image(old_nodes):
  new_nodes = []

  for node in old_nodes:
    images = extract_markdown_images(node.text)

    if not images or node.text_type != TextType.PLAIN:
      new_nodes.append(node)
      continue

    remaining_text = node.text

    for alt_text, image_url in images:
      original_link_text = f"![{alt_text}]({image_url})"
      text_before_image, text_after_image = remaining_text.split(original_link_text, 1)

      if text_before_image:
        new_nodes.append(TextNode(text_before_image, TextType.PLAIN))

      new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
      remaining_text = text_after_image

    if remaining_text:
      new_nodes.append(TextNode(remaining_text, TextType.PLAIN))

  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []

  for node in old_nodes:
    links = extract_markdown_links(node.text)

    if not links or node.text_type != TextType.PLAIN:
      new_nodes.append(node)
      continue

    remaining_text = node.text

    for link_text, link_url in links:
      original_link_text = f"[{link_text}]({link_url})"
      text_before_link, text_after_link = remaining_text.split(original_link_text, 1)

      if text_before_link:
        new_nodes.append(TextNode(text_before_link, TextType.PLAIN))

      new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
      remaining_text = text_after_link

    if remaining_text:
      new_nodes.append(TextNode(remaining_text, TextType.PLAIN))

  return new_nodes

def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.PLAIN)]
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)

  return nodes
