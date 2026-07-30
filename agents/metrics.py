"""
metrics.py - Calculates parsed repository metrics and Code vs. Narrative ratios.
"""

def calculate_repository_metrics(parsed_data: dict) -> dict:
    """
    Analyzes parsed repository data and returns line counts, 
    narrative string volume, and percentage ratios.
    """
    total_code_lines = 0
    total_narrative_snippets = 0

    if not parsed_data:
        return {
            "total_lines": 0,
            "snippet_count": 0,
            "code_pct": 100,
            "narrative_pct": 0,
            "ratio_str": "0:0 (100% / 0%)"
        }

    for file_name, file_info in parsed_data.items():
        if "error" in file_info:
            continue
        
        total_code_lines += file_info.get("line_count", 0)
        snippets = file_info.get("narrative_snippets", [])
        total_narrative_snippets += len(snippets)

    # Weighting: Estimate ~3 lines of text per extracted narrative snippet block
    narrative_weight = total_narrative_snippets * 3
    total_volume = total_code_lines + narrative_weight

    if total_volume > 0:
        code_pct = round((total_code_lines / total_volume) * 100)
        narrative_pct = 100 - code_pct
    else:
        code_pct, narrative_pct = 100, 0

    return {
        "total_lines": total_code_lines,
        "snippet_count": total_narrative_snippets,
        "code_pct": code_pct,
        "narrative_pct": narrative_pct,
        "ratio_str": f"{total_code_lines}:{total_narrative_snippets} ({code_pct}% / {narrative_pct}%)"
    }