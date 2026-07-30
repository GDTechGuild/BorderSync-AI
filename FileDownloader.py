import os
from datetime import datetime

def build_txt_export(repo_name: str, sections: dict, parsed_data: dict) -> str:
    """
    Generates a formatted plain-text documentation bundle from parsed repository data.
    
    Args:
        repo_name (str): Name of the repository/project.
        sections (dict): Key-value pairs of section titles and markdown content.
        parsed_data (dict): Structured AST parsing results per file.
        
    Returns:
        str: Formatted text ready for export.
    """
    lines = []
    divider = "=" * 80
    sub_divider = "-" * 80
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Header section
    lines.append(divider)
    lines.append(f"INDIEGEN GAME DOCUMENTATION BUNDLE: {repo_name.upper()}")
    lines.append(f"GENERATED ON: {timestamp}")
    lines.append(divider)
    lines.append("\n")

    # Narrative & design sections (GDD, Lore, Character Matrix)
    for title, content in sections.items():
        if title == "Technical Breakdown":
            continue
        lines.append(divider)
        lines.append(f"SECTION: {title.upper()}")
        lines.append(divider)
        lines.append(content)
        lines.append("\n\n")

    # Technical breakdown section
    lines.append(divider)
    lines.append("SECTION: TECHNICAL BREAKDOWN")
    lines.append(divider)

    if parsed_data:
        for filename, data in parsed_data.items():
            lines.append(f"\nFile: {filename}")
            lines.append(sub_divider)
            
            if "error" in data:
                lines.append(f"Error: {data['error']}")
                continue
                
            lines.append(f"Line Count: {data.get('line_count', 'N/A')}")
            
            snippets = data.get("narrative_snippets", [])
            if snippets:
                lines.append("Snippets:")
                for snippet in snippets[:5]:
                    lines.append(f"  - {snippet}")
                    
            vars_dict = data.get("variables", {})
            if vars_dict:
                lines.append("Variables / Code Details:")
                for key, val in vars_dict.items():
                    lines.append(f"  {key}: {val}")
    else:
        lines.append("No technical breakdown available.")

    return "\n".join(lines)


def generate_export_filename(repo_name: str) -> str:
    """
    Generates a sanitized filename slug for export downloads.
    """
    slug = repo_name.lower().strip().replace(" ", "_")
    return f"{slug}_documentation.txt"