import codecs

def fix_unicode_escapes(input_path: str, output_path: str):
    """
    Reads a file containing unicode escape sequences (e.g. '\\u00e4'),
    decodes them into proper UTF-8 characters, and writes a clean
    Markdown file.
    
    Args:
        input_path (str): Path to the input file.
        output_path (str): Path where the cleaned Markdown file will be saved.
    """

    # Read the raw content
    with open(input_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Decode unicode escape sequences
    cleaned = codecs.decode(raw.encode("utf-8"), "unicode_escape")

    # Write clean UTF-8 markdown
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"✓ Clean Markdown written to: {output_path}")


fix_unicode_escapes("file.md", "cleaned_file.md")