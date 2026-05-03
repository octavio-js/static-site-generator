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
