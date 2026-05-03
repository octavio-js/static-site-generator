import os
import shutil
import sys

from textnode import TextNode, TextType
from markdown_to_html import markdown_to_html_node
from markdown_extract import extract_title

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  
  with open(from_path, "r") as f:
    markdown_content = f.read()
    
  with open(template_path, "r") as f:
    template_content = f.read()

  html_node = markdown_to_html_node(markdown_content)
  html_string = html_node.to_html()
  
  title = extract_title(markdown_content)
  
  final_html = template_content.replace("{{ Title }}", title)
  final_html = final_html.replace("{{ Content }}", html_string)
  
  dest_dir = os.path.dirname(dest_path)
  if dest_dir != "" and not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
  with open(dest_path, "w") as f:
    f.write(final_html)

def copy_files_recursive(source_dir_path, dest_dir_path):
  if not os.path.exists(source_dir_path):
    raise ValueError(f"Source directory '{source_dir_path}' does not exist.")

  if os.path.exists(dest_dir_path):
    print(f"Deleting {dest_dir_path}...")
    shutil.rmtree(dest_dir_path)
  
  print(f"Creating {dest_dir_path}...")
  os.mkdir(dest_dir_path)

  for filename in os.listdir(source_dir_path):
    source_path = os.path.join(source_dir_path, filename)
    dest_path = os.path.join(dest_dir_path, filename)

    if os.path.isfile(source_path):
      print(f"Copying {source_path} to {dest_path}")
      shutil.copy(source_path, dest_path)
    else:
      copy_files_recursive(source_path, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  for filename in os.listdir(dir_path_content):
    from_path = os.path.join(dir_path_content, filename)
    dest_path = os.path.join(dest_dir_path, filename)
    
    if os.path.isfile(from_path):
      if from_path.endswith(".md"):
        dest_path = dest_path[:-3] + ".html"
        generate_page(from_path, template_path, dest_path)
    else:
      generate_pages_recursive(from_path, template_path, dest_path)

def main():
  if len(sys.argv) > 1:
    basepath = sys.argv[1]
  else:
    basepath = "/"

  print("Copying static files to public directory...")
  copy_files_recursive("./static", "./docs")
  generate_pages_recursive("./content", "./template.html", "./docs", basepath)

if __name__ == "__main__":
  main()
