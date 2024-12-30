#!/usr/bin/env python3

import sys
import json
import os

sys.stderr.write("Preprocessor started.\n")

def load_snippets(snippets_folder):
    """Load snippets from individual files in a specified folder."""
    snippets = {}
    if not os.path.isdir(snippets_folder):
        sys.stderr.write(f"Error: Snippets folder '{snippets_folder}' not found.\n")
        sys.exit(1)
    for filename in os.listdir(snippets_folder):
        filepath = os.path.join(snippets_folder, filename)
        if os.path.isfile(filepath):
            snippet_name = f"{{{{{filename}}}}}"  # Match the placeholder format
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    snippets[snippet_name] = f.read().strip()
            except Exception as e:
                sys.stderr.write(f"Error: Failed to read snippet '{filename}': {e}\n")
    return snippets

def process_chapter(chapter, snippets):
    content = ''
    if 'Chapter' in chapter.keys():
        content = chapter['Chapter']['content']
    else:
        return chapter
    for placeholder, html in snippets.items():
        content = content.replace(placeholder, html)
    chapter['Chapter']['content'] = content
    return chapter

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        # Indicate support for all renderers.
        sys.exit(0)

    # Load the input data from stdin.
    input_data = json.load(sys.stdin)

    # Define the path to the external snippets folder.
    snippets_folder = os.getenv("SNIPPETS_FOLDER", "snippets/html")
    snippets = load_snippets(snippets_folder)

    # Process the book sections.
    book = input_data[1]
    book["sections"] = [process_chapter(section, snippets) for section in book["sections"]]

    # Output the modified book structure to stdout.
    json.dump(book, sys.stdout, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

