import os
import shutil
import logging
from textnode import TextNode, TextType
from generate_page import generate_page

# Set up logging to see what's happening during the copy process
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def copy_static_files(source_dir, dest_dir):
    """
    Recursively copy all contents from source directory to destination directory.
    First deletes all contents of destination directory to ensure clean copy.
    
    Args:
        source_dir (str): Source directory path
        dest_dir (str): Destination directory path
    """
    # Ensure source directory exists
    if not os.path.exists(source_dir):
        logger.error(f"Source directory '{source_dir}' does not exist")
        return
    
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        logger.info(f"Removing existing destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create destination directory
    logger.info(f"Creating destination directory: {dest_dir}")
    os.makedirs(dest_dir)
    
    # Copy all files and subdirectories recursively
    copy_directory_contents(source_dir, dest_dir)
    
    logger.info(f"Successfully copied all files from '{source_dir}' to '{dest_dir}'")


def copy_directory_contents(source_dir, dest_dir):
    """
    Recursively copy contents of a directory.
    
    Args:
        source_dir (str): Source directory path
        dest_dir (str): Destination directory path
    """
    # Get all items in source directory
    items = os.listdir(source_dir)
    
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            # Copy file
            logger.info(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy2(source_path, dest_path)
        elif os.path.isdir(source_path):
            # Create subdirectory and copy its contents
            logger.info(f"Creating subdirectory: {dest_path}")
            os.makedirs(dest_path)
            copy_directory_contents(source_path, dest_path)


def main():
    """Main function to run the static site generator"""
    print("Starting static site generator...")
    
    # Define source and destination directories
    static_dir = "static"
    public_dir = "public"
    
    # Copy static files to public directory
    print(f"Copying static files from '{static_dir}' to '{public_dir}'...")
    copy_static_files(static_dir, public_dir)
    
    print("Static file copying completed!")
    
    # Generate the main page from markdown
    print("Generating HTML pages...")
    generate_page("content/index.md", "template.html", "public/index.html")
    
    # Generate blog pages
    generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    
    # Generate contact page
    generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
    
    print("Page generation completed!")
    print("Site is ready!")


if __name__ == "__main__":
    main()
