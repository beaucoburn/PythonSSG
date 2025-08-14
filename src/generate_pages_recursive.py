import os
from generate_page import generate_page


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively crawl the content directory and generate HTML pages for all markdown files.
    
    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory where HTML files will be written
        basepath (str): Base path for the site (e.g., "/" for local, "/REPO_NAME/" for GitHub Pages)
    """
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    # Walk through the content directory recursively
    for root, dirs, files in os.walk(dir_path_content):
        # Calculate the relative path from content directory
        rel_path = os.path.relpath(root, dir_path_content)
        
        # Create corresponding destination directory
        dest_subdir = os.path.join(dest_dir_path, rel_path)
        if not os.path.exists(dest_subdir):
            os.makedirs(dest_subdir)
        
        # Process each file in the current directory
        for file in files:
            if file.endswith('.md'):
                # Construct source and destination paths
                source_path = os.path.join(root, file)
                
                # Create destination HTML filename (replace .md with .html)
                html_filename = file[:-3] + '.html'  # Remove .md extension
                dest_path = os.path.join(dest_subdir, html_filename)
                
                # Generate the HTML page
                print(f"Generating page from {source_path} to {dest_path} using {template_path}")
                generate_page(source_path, template_path, dest_path, basepath)


def generate_pages_recursive_alt(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Alternative implementation using pathlib for more modern Python path handling.
    
    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory where HTML files will be written
        basepath (str): Base path for the site (e.g., "/" for local, "/REPO_NAME/" for GitHub Pages)
    """
    try:
        from pathlib import Path
    except ImportError:
        # Fallback to os.path if pathlib is not available
        return generate_pages_recursive(dir_path_content, template_path, dest_dir_path)
    
    content_path = Path(dir_path_content)
    dest_path = Path(dest_dir_path)
    
    # Ensure the destination directory exists
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Walk through the content directory recursively
    for md_file in content_path.rglob('*.md'):
        # Calculate the relative path from content directory
        rel_path = md_file.relative_to(content_path)
        
        # Create corresponding destination directory
        dest_subdir = dest_path / rel_path.parent
        dest_subdir.mkdir(parents=True, exist_ok=True)
        
        # Create destination HTML filename (replace .md with .html)
        html_filename = rel_path.stem + '.html'
        dest_file = dest_subdir / html_filename
        
        # Generate the HTML page
        print(f"Generating page from {md_file} to {dest_file} using {template_path}")
        generate_page(str(md_file), template_path, str(dest_file), basepath)
