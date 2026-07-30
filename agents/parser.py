import os
import json
import re
from typing import Dict, Any, List

try:
    from tree_sitter_languages import get_parser
    HAS_TREE_SITTER = True
except ImportError:
    HAS_TREE_SITTER = False

# Mapping extensions to Tree-sitter language names
TS_LANGUAGE_MAP = {
    '.cs': 'c_sharp',
    '.py': 'python',
}

STRING_NODE_TYPES = {
    'string', 
    'string_literal', 
    'interpolated_string_expression', 
    'raw_string_literal'
}

def scan_repository(repo_path: str, ignore_dirs=None) -> List[str]:
    """
    Scans the repository for game source and narrative files (.cs, .gd, .json, .txt, .py).
    Handles path sanitization and case-insensitive extensions automatically.
    """
    if ignore_dirs is None:
        ignore_dirs = {'.git', 'bin', 'obj', 'node_modules', '__pycache__', '.vs', 'Build', 'Builds'}
        
    valid_extensions = ('.cs', '.gd', '.json', '.txt', '.py')
    discovered_files = []
    
    # 1. Clean and normalize path string (removes quotes & fixes Windows backslashes)
    clean_path = repo_path.strip().strip('"').strip("'").replace('\\', '/')
    abs_path = os.path.abspath(clean_path)

    if not os.path.exists(abs_path):
        return []

    # 2. Walk directory tree
    for root, dirs, files in os.walk(abs_path):
        # Filter out hidden or build folders in-place
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignore_dirs]
        for file in files:
            # Lowercase check handles both .CS and .cs
            if file.lower().endswith(valid_extensions):
                full_file_path = os.path.join(root, file).replace('\\', '/')
                discovered_files.append(full_file_path)
                
    return discovered_files

def extract_strings_from_json(data: Any) -> List[str]:
    """Recursively extracts dialogue and string values from JSON files."""
    strings = []
    if isinstance(data, dict):
        for v in data.values():
            strings.extend(extract_strings_from_json(v))
    elif isinstance(data, list):
        for item in data:
            strings.extend(extract_strings_from_json(item))
    elif isinstance(data, str) and len(data.strip()) > 3:
        strings.append(data.strip())
    return strings[:20]

def extract_game_mechanics(file_paths: List[str]) -> Dict[str, Any]:
    """Extracts code logic previews and narrative strings safely using Tree-sitter or Regex."""
    parsed_data = {}
    
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        file_data = {"line_count": 0, "variables": {}, "narrative_snippets": []}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content_text = f.read()
                lines = content_text.splitlines()
                file_data["line_count"] = len(lines)
                
            ext = os.path.splitext(file_path)[1].lower()
            
            # JSON File Parser
            if ext == '.json':
                try:
                    data = json.loads(content_text)
                    file_data["narrative_snippets"] = extract_strings_from_json(data)
                except json.JSONDecodeError:
                    file_data["narrative_snippets"] = ["Error parsing JSON structure."]
                parsed_data[filename] = file_data
                continue

            snippets = []
            parsed_successfully = False

            # PRIMARY AST: Tree-sitter AST Parsing (for C# and Python)
            if HAS_TREE_SITTER and ext in TS_LANGUAGE_MAP:
                try:
                    parser = get_parser(TS_LANGUAGE_MAP[ext])
                    content_bytes = content_text.encode('utf-8')
                    tree = parser.parse(content_bytes)
                    
                    def traverse_ast(node):
                        if node.type in STRING_NODE_TYPES:
                            raw_val = content_bytes[node.start_byte:node.end_byte]
                            val = raw_val.decode('utf-8', errors='ignore').strip('"' + "'")
                            if len(val) > 3:
                                snippets.append(val)
                        
                        for child in node.children:
                            traverse_ast(child)
                            
                    traverse_ast(tree.root_node)
                    if snippets:
                        parsed_successfully = True
                except Exception:
                    parsed_successfully = False

            # FALLBACK PARSER: Regex String Matching (for GDScript, TXT, or unparsed code)
            if not parsed_successfully:
                string_literals = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', content_text)
                snippets = [s for s in string_literals if len(s.strip()) > 3]

            # Extract non-comment code lines for preview
            extracted_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith(('//', '#', '/*')):
                    extracted_lines.append(stripped)

            file_data["narrative_snippets"] = list(dict.fromkeys(snippets))[:25]
            file_data["variables"] = {"code_preview": extracted_lines[:15]}
            
            parsed_data[filename] = file_data

        except Exception as e:
            parsed_data[filename] = {"error": str(e)}
            
    return parsed_data