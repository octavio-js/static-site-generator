import os
import shutil

from textnode import TextNode, TextType

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

def main():
  print("Copying static files to public directory...")
  copy_files_recursive("./static", "./public")

if __name__ == "__main__":
  main()
