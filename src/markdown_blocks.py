from enum import Enum
import re

def markdown_to_blocks(markdown):
  split_blocks = markdown.split("\n\n")
  final_blocks = []

  for block in split_blocks:
    if block == "":
      continue

    stripped = block.strip()

    if stripped != "":
      final_blocks.append(stripped)

  return final_blocks


class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
  if re.match(r"^#{1,6} ", block):
    return BlockType.HEADING

  if block.startswith("```\n") and block.endswith("```"):
    return BlockType.CODE

  lines = block.split("\n")

  if all(re.match(r"^> ?", line) for line in lines):
    return BlockType.QUOTE

  if all(line.startswith("- ") for line in lines):
    return BlockType.UNORDERED_LIST

  is_ordered = True
  for i, line in enumerate(lines, start=1):
    if not line.startswith(f"{i}. "):
      is_ordered = False
      break

  if is_ordered:
    return BlockType.ORDERED_LIST

  return BlockType.PARAGRAPH
