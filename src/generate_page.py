import os
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from markdown content using a template.
    
    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the HTML template file
        dest_path (str): Path where the generated HTML file should be written
        basepath (str): Base path for the site (e.g., "/" for local, "/REPO_NAME/" for GitHub Pages)
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title from the markdown
    title = extract_title(markdown_content)
    
    # Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Replace absolute paths with basepath for GitHub Pages compatibility
    if basepath != "/":
        final_html = final_html.replace('href="/', f'href="{basepath}')
        final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Ensure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the generated HTML to the destination file
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
