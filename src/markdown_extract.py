import re

def extract_markdown_images(text):
  regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  return re.findall(regex, text)

def extract_markdown_links(text):
  regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  return re.findall(regex, text)

def extract_title(markdown):
  lines = markdown.split("\n")
  for line in lines:
    if line.startswith("# "):
      return line[2:].strip()
  raise Exception("No h1 header found in markdown")
