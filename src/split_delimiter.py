from textnode import TextNode, TextType
import re

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
