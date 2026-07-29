import os
import json
import re

def scan_repository(repo_path):
    """Scans the repository for code and narrative files (.cs, .gd, .json, .txt)."""
    valid_extensions = ('.cs', '.gd', '.json', '.txt')
    discovered_files = []
    
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(valid_extensions):
                full_path = os.path.join(root, file)
                discovered_files.append(full_path)
                
    return discovered_files

import os
import json
import re

def scan_repository(repo_path):
    """Scans the repository for code and narrative files (.cs, .gd, .json, .txt, .py)."""
    valid_extensions = ('.cs', '.gd', '.json', '.txt', '.py')
    discovered_files = []
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(valid_extensions):
                full_path = os.path.join(root, file)
                discovered_files.append(full_path)
                
    return discovered_files

def extract_game_mechanics(file_paths):
    """Extracts code logic and specifically targets dialogue strings for sentiment analysis."""
    parsed_data = {}
    
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        file_data = {"line_count": 0, "variables": {}, "narrative_snippets": []}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                file_data["line_count"] = len(lines)
                content = "".join(lines)
                
                if file_path.endswith('.json'):
                    try:
                        data = json.loads(content)
                        file_data["narrative_snippets"] = extract_strings_from_json(data)
                    except json.JSONDecodeError:
                        file_data["narrative_snippets"] = ["Error parsing JSON structure."]
                else:
                    # Extract literal string quotes from C# / GDScript (e.g., "heya.", "NHEHEHEH!")
                    string_literals = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', content)
                    # Filter out short technical strings like tags or empty spaces
                    meaningful_snippets = [s for s in string_literals if len(s.strip()) > 3]
                    
                    file_data["narrative_snippets"] = meaningful_snippets
                    
                    # Also grab basic variables for the technical breakdown
                    extracted_lines = []
                    for line in lines:
                        stripped = line.strip()
                        if stripped and not stripped.startswith(('//', '#', '/*')):
                            extracted_lines.append(stripped)
                    file_data["variables"] = {"code_preview": extracted_lines[:15]}
                    
            parsed_data[filename] = file_data
        except Exception as e:
            parsed_data[filename] = {"error": str(e)}
            
    return parsed_data

def extract_strings_from_json(data):
    """Recursively pulls string values from JSON dialogue/lore files."""
    strings = []
    if isinstance(data, dict):
        for k, v in data.items():
            strings.extend(extract_strings_from_json(v))
    elif isinstance(data, list):
        for item in data:
            strings.extend(extract_strings_from_json(item))
    elif isinstance(data, str) and len(data.strip()) > 3:
        strings.append(data.strip())
    return strings[:30]

def extract_strings_from_json(data):
    """Recursively pulls string values from JSON dialogue/lore files."""
    strings = []
    if isinstance(data, dict):
        for k, v in data.items():
            strings.extend(extract_strings_from_json(v))
    elif isinstance(data, list):
        for item in data:
            strings.extend(extract_strings_from_json(item))
    elif isinstance(data, str) and len(data.strip()) > 3:
        strings.append(data.strip())
    return strings[:20]  # Limit to prevent prompt overflow