from fastapi import HTTPException
import markdown

def md_file_to_html(md_file, html_file):
    print(f"Converting {md_file} to {html_file}")
    
    if not md_file or not md_file.endswith(".md") or not html_file or not html_file.endswith(".html"):
        raise HTTPException(status_code=400, detail=f"Input file ({md_file}) must be a Markdown file and output file ({html_file}) must be an HTML file")
    
    """Convert a Markdown file to an HTML file"""
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_output = markdown.markdown(md_text)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"Converted {md_file} to {html_file}")
    return html_file
