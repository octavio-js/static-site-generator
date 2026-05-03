from htmlnode import ParentNode
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from split_delimiter import text_to_textnodes
from textnode import text_node_to_html_node

def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  html_nodes = []
  for node in text_nodes:
    html_nodes.append(text_node_to_html_node(node))
  return html_nodes

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  child_nodes = []

  for block in blocks:
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
      stripped_block = block.replace("\n", " ")
      children = text_to_children(stripped_block)
      child_nodes.append(ParentNode("p", children))

    elif block_type == BlockType.HEADING:
      level = 0
      for char in block:
        if char == '#':
          level += 1
        else:
          break
      
      content = block[level + 1:]
      children = text_to_children(content)
      child_nodes.append(ParentNode(f"h{level}", children))

    elif block_type == BlockType.CODE:
      if block.startswith("```\n"): content = block[4:-3]
      else: content = block[3:-3] 
      from textnode import TextNode, TextType
      text_node = TextNode(content, TextType.PLAIN)
      code_node = text_node_to_html_node(text_node)
      child_nodes.append(ParentNode("pre", [ParentNode("code", [code_node])]))

    elif block_type == BlockType.QUOTE:
      lines = block.split("\n")
      new_lines = []
      for line in lines:
        if line.startswith("> "):
          new_lines.append(line[2:])
        elif line.startswith(">"):
          new_lines.append(line[1:])
        else:
          new_lines.append(line)
      content = " ".join(new_lines)
      children = text_to_children(content)
      child_nodes.append(ParentNode("blockquote", children))

    elif block_type == BlockType.UNORDERED_LIST:
      lines = block.split("\n")
      li_nodes = []
      for line in lines:
        content = line[2:]
        children = text_to_children(content)
        li_nodes.append(ParentNode("li", children))
      child_nodes.append(ParentNode("ul", li_nodes))

    elif block_type == BlockType.ORDERED_LIST:
      lines = block.split("\n")
      li_nodes = []
      for line in lines:
        dot_index = line.find(". ")
        content = line[dot_index + 2:]
        children = text_to_children(content)
        li_nodes.append(ParentNode("li", children))
      child_nodes.append(ParentNode("ol", li_nodes))

    else:
      raise Exception("Unknown block type")

  return ParentNode("div", child_nodes)
